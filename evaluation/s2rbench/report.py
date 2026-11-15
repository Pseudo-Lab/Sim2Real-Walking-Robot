"""Aggregate episodes into the benchmark report: the 8-cell table, the Sim-to-Real gap,
the retention index, sim-predicts-real correlation, reproducibility and the failure taxonomy."""
from __future__ import annotations
import json, math, re
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np
from .metrics import compute_metrics
from .failures import classify, LABELS

MIN_SIM_FOR_RETENTION = 0.2      # below this, "transfer" is not a meaningful question


def evaluate(episodes, protocol):
    """One row per episode: meta + metrics + success + failure label."""
    rows = []
    for ep in episodes:
        m = compute_metrics(ep, protocol)
        ok = protocol.success(ep.meta["task"], m)
        label, flags = classify(ep, m, ok, protocol)
        rows.append({**{k: ep.meta.get(k) for k in ("env", "condition", "task", "policy_id", "trial", "_path")},
                     **m, "success": ok, "failure": label, "flags": flags})
    return rows


def wilson(k, n, z=1.96):
    if n == 0:
        return (math.nan, math.nan)
    p, d = k / n, 1 + z * z / n
    c, h = (p + z * z / (2 * n)) / d, z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def _natural(s):
    return [float(x) if x.replace(".", "", 1).isdigit() else x for x in re.findall(r"\d+\.?\d*|\D+", str(s))]


def _cells(rows):
    cells = defaultdict(list)                       # (condition, env, task) -> [0/1, ...]
    for r in rows:
        cells[(r["condition"], r["env"], r["task"])].append(int(r["success"]))
    return cells


def _macro(cells, cond, env, tasks):
    """Success rate averaged over tasks with equal weight (so a 30-trial task cannot dominate)."""
    v = [np.mean(cells[(cond, env, t)]) for t in tasks if (cond, env, t) in cells]
    return float(np.mean(v)) if v else math.nan


def _summary(cells, conds, tasks_by_cond):
    out = {}
    for c in conds:
        sim, real = _macro(cells, c, "sim", tasks_by_cond[c]), _macro(cells, c, "real", tasks_by_cond[c])
        gap = sim - real
        ret = real / sim if sim >= MIN_SIM_FOR_RETENTION else math.nan
        out[c] = {"sim": sim, "real": real, "gap": gap, "retention": ret}
    return out


def _spearman(a, b):
    def rank(x):
        x = np.asarray(x, float)
        order = np.argsort(x)
        r = np.empty(len(x))
        r[order] = np.arange(len(x))
        for v in np.unique(x):                      # average ranks over ties
            r[x == v] = r[x == v].mean()
        return r
    ra, rb = rank(a), rank(b)
    if ra.std() == 0 or rb.std() == 0:
        return math.nan
    return float(np.corrcoef(ra, rb)[0, 1])


def aggregate(rows, n_boot=2000, seed=0):
    cells = _cells(rows)
    conds = sorted({c for c, _, _ in cells}, key=_natural)
    # compare sim and real only on tasks measured in BOTH environments
    tasks_by_cond = {c: sorted({t for cc, e, t in cells if cc == c and (c, "sim", t) in cells and (c, "real", t) in cells}
                               or {t for cc, e, t in cells if cc == c}) for c in conds}
    point = _summary(cells, conds, tasks_by_cond)

    rng = np.random.default_rng(seed)               # bootstrap: resample trials inside each cell
    boot = {c: defaultdict(list) for c in conds}
    for _ in range(n_boot):
        res = {k: rng.choice(v, len(v)) for k, v in cells.items()}
        for c, s in _summary(res, conds, tasks_by_cond).items():
            for k, v in s.items():
                boot[c][k].append(v)
    for c in conds:
        for k in ("sim", "real", "gap", "retention"):
            v = np.array(boot[c][k], float)
            v = v[~np.isnan(v)]
            point[c][k + "_ci"] = [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))] if len(v) else [math.nan, math.nan]

    pairs = [(np.mean(cells[(c, "sim", t)]), np.mean(cells[(c, "real", t)]))
             for c in conds for t in tasks_by_cond[c] if (c, "sim", t) in cells and (c, "real", t) in cells]
    rho = _spearman(*zip(*pairs)) if len(pairs) >= 4 else math.nan

    per_cell = []
    for (c, e, t), v in sorted(cells.items(), key=lambda kv: (_natural(kv[0][0]), kv[0][1], kv[0][2])):
        k, n = sum(v), len(v)
        dist = [r["distance_m"] for r in rows if (r["condition"], r["env"], r["task"]) == (c, e, t)]
        per_cell.append({"condition": c, "env": e, "task": t, "n": n, "success_rate": k / n, "ci": list(wilson(k, n)),
                         "consistency": max(k, n - k) / n,          # share of trials agreeing with the majority outcome
                         "distance_sd_m": float(np.nanstd(dist)) if n > 1 else math.nan})
    repro = {e: float(np.mean([p["consistency"] for p in per_cell if p["env"] == e and p["n"] >= 3] or [math.nan])) for e in ("sim", "real")}
    failures = {e: dict(Counter(r["failure"] for r in rows if r["env"] == e and not r["success"])) for e in ("sim", "real")}
    return {"conditions": point, "cells": per_cell, "sim_predicts_real_spearman": rho, "n_pairs": len(pairs),
            "reproducibility": repro, "failures": failures, "n_episodes": len(rows)}


def _pct(x):
    return "–" if x is None or (isinstance(x, float) and math.isnan(x)) else f"{100 * x:.0f}%"


def to_markdown(agg, protocol_version):
    L = ["# Sim-to-Real benchmark report", "",
         f"Protocol `{protocol_version}` · {agg['n_episodes']} episodes · 95% intervals (bootstrap over trials)", "",
         "## Conditions × environments", "",
         "| Condition | Sim success | Real success | Gap (sim − real) | Retention (real ÷ sim) |", "|---|---|---|---|---|"]
    for c, s in agg["conditions"].items():
        ci = lambda k: f" [{_pct(s[k + '_ci'][0])}, {_pct(s[k + '_ci'][1])}]"
        ret = "–" if math.isnan(s["retention"]) else f"{s['retention']:.2f} [{s['retention_ci'][0]:.2f}, {s['retention_ci'][1]:.2f}]"
        gap = "–" if math.isnan(s["gap"]) else f"{100 * s['gap']:+.0f} pp [{100 * s['gap_ci'][0]:+.0f}, {100 * s['gap_ci'][1]:+.0f}]"
        L.append(f"| {c} | {_pct(s['sim'])}{ci('sim')} | {_pct(s['real'])}{ci('real')} | {gap} | {ret} |")
    rho = agg["sim_predicts_real_spearman"]
    L += ["", "Success is macro-averaged over tasks. Retention is left blank when sim success is below "
          f"{_pct(MIN_SIM_FOR_RETENTION)}.", "",
          "## Does simulation predict reality?", "",
          ("Not enough sim/real pairs yet." if math.isnan(rho) else
           f"Spearman rank correlation between sim and real success over {agg['n_pairs']} condition × task cells: **{rho:+.2f}**"), "",
          "## Reproducibility", "",
          "Share of trials that agree with the majority outcome of their cell (1.00 = every repeat ends the same way).", "",
          f"- sim: {agg['reproducibility']['sim']:.2f}", f"- real: {agg['reproducibility']['real']:.2f}", "",
          "## Failure taxonomy", "", "| Failure | Sim | Real |", "|---|---|---|"]
    for lab in LABELS:
        s, r = agg["failures"]["sim"].get(lab, 0), agg["failures"]["real"].get(lab, 0)
        if s or r:
            L.append(f"| {lab} | {s} | {r} |")
    L += ["", "## Per task", "", "| Condition | Env | Task | n | Success | 95% CI | Consistency |", "|---|---|---|---|---|---|---|"]
    for p in agg["cells"]:
        L.append(f"| {p['condition']} | {p['env']} | {p['task']} | {p['n']} | {_pct(p['success_rate'])} | "
                 f"{_pct(p['ci'][0])}–{_pct(p['ci'][1])} | {p['consistency']:.2f} |")
    return "\n".join(L) + "\n"


SIM, REAL, INK, MUTED, SURFACE = "#2a78d6", "#eb6834", "#0b0b0b", "#52514e", "#fcfcfb"


def plot(agg, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    conds = list(agg["conditions"])
    fig, (a, b) = plt.subplots(1, 2, figsize=(11, 4.2), facecolor=SURFACE, gridspec_kw={"width_ratios": [1.15, 1]})
    w = 0.36
    for ax in (a, b):
        ax.set_facecolor(SURFACE)
        for s in ("top", "right", "left"):
            ax.spines[s].set_visible(False)
        ax.spines["bottom"].set_color("#c9c8c2")
        ax.tick_params(colors=MUTED, length=0)
    for off, env, col in ((-w / 2 - 0.01, "sim", SIM), (w / 2 + 0.01, "real", REAL)):
        v = [agg["conditions"][c][env] for c in conds]
        ci = [agg["conditions"][c][env + "_ci"] for c in conds]
        x = np.arange(len(conds)) + off
        a.bar(x, v, w, color=col, label="Simulation" if env == "sim" else "Real robot")
        a.vlines(x, [c[0] for c in ci], [c[1] for c in ci], color=INK, lw=1)
        for xi, vi, c in zip(x, v, ci):
            if not math.isnan(vi):
                a.text(xi, c[1] + 0.03, f"{100 * vi:.0f}%", ha="center", va="bottom", fontsize=9, color=INK)
    a.set_xticks(range(len(conds)), conds)
    a.set_ylim(0, 1.18); a.set_yticks([0, 0.5, 1.0], ["0%", "50%", "100%"])
    a.yaxis.grid(True, color="#e6e5e0", lw=0.8); a.set_axisbelow(True)
    a.set_title("Success rate by condition", loc="left", color=INK, fontsize=12)
    a.legend(frameon=False, loc="upper left", ncols=2, bbox_to_anchor=(0, 1.0), labelcolor=MUTED, fontsize=9)

    labs = [l for l in LABELS if agg["failures"]["sim"].get(l, 0) or agg["failures"]["real"].get(l, 0)][::-1]
    y = np.arange(len(labs))
    for off, env, col in ((w / 2 + 0.01, "sim", SIM), (-w / 2 - 0.01, "real", REAL)):
        v = [agg["failures"][env].get(l, 0) for l in labs]
        b.barh(y + off, v, w, color=col)
        for yi, vi in zip(y + off, v):
            if vi:
                b.text(vi + 0.3, yi, str(vi), va="center", fontsize=9, color=INK)
    b.set_yticks(y, [l.replace("_", " ") for l in labs]); b.set_xticks([])
    b.spines["bottom"].set_visible(False)
    b.set_title("Failed episodes by cause", loc="left", color=INK, fontsize=12)
    fig.tight_layout()
    fig.savefig(path, dpi=130, facecolor=SURFACE)
    plt.close(fig)


def write_report(episodes, protocol, out_dir, n_boot=2000):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    rows = evaluate(episodes, protocol)
    agg = aggregate(rows, n_boot=n_boot)
    (out / "report.md").write_text(to_markdown(agg, protocol.version))
    (out / "results.json").write_text(json.dumps({"protocol": protocol.version, "summary": agg, "episodes": rows}, indent=1, default=float))
    try:
        plot(agg, out / "report.png")
    except ImportError:
        pass
    return agg
