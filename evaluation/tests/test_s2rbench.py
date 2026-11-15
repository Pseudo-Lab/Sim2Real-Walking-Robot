import math, sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from s2rbench import Episode, Protocol, compute_metrics, classify
from s2rbench.report import aggregate, wilson

P = Protocol()
HZ = 50


def walk(task="straight", speed=0.15, cmd=0.15, seconds=10, fall_at=None, env="sim", cond="A", **meta):
    n = int((fall_at or seconds) * HZ)
    t = np.arange(n) / HZ
    rpy = np.zeros((n, 3))
    if fall_at:
        rpy[-1, 0] = np.radians(80)
    arrays = {"t": t, "base_rpy": rpy, "base_pos": np.stack([speed * t, 0 * t, 0 * t + 0.1], 1), "cmd_vel": np.tile([cmd, 0, 0], (n, 1))}
    return Episode({k: v.astype(np.float32) for k, v in arrays.items()},
                   {"env": env, "condition": cond, "task": task, "policy_id": "p", "trial": 0, **meta})


def judge(ep):
    m = compute_metrics(ep, P)
    ok = P.success(ep.meta["task"], m)
    return m, ok, classify(ep, m, ok, P)[0]


def test_straight_success_and_progress():
    m, ok, label = judge(walk())
    assert ok and label == "none"
    assert abs(m["progress"] - 1.0) < 0.02 and abs(m["distance_m"] - 1.5) < 0.02


def test_heading_is_respected():
    ep = walk()
    ep.arrays["base_rpy"][:, 2] = np.pi / 2            # facing +y but moving along +x: sideways, not forward
    m, ok, _ = judge(ep)
    assert not ok and abs(m["distance_m"]) < 0.05


def test_fall_and_slow_walk_are_labelled():
    assert judge(walk(fall_at=4))[1:] == (False, "fall")
    assert judge(walk(speed=0.01))[1:] == (False, "no_progress")
    assert judge(walk(speed=0.07))[1:] == (False, "tracking_error")


def test_recovery_time():
    n = 8 * HZ
    t = np.arange(n) / HZ
    rpy = np.zeros((n, 3))
    rpy[:, 0] = np.radians(15) * ((t >= 2.0) & (t < 3.0))       # tilted for 1 s after the push starts
    perturb = ((t >= 2.0) & (t < 2.1)).astype(float)
    ep = Episode({"t": t, "base_rpy": rpy, "base_pos": np.zeros((n, 3)), "perturb": perturb},
                 {"env": "sim", "condition": "A", "task": "push_recovery", "policy_id": "p", "trial": 0})
    m, ok, _ = judge(ep)
    assert ok and abs(m["recovery_time_s"] - 0.9) < 0.05


def test_real_log_without_tracking_uses_tape_measure():
    ep = walk(env="real", measured_distance_m=1.2)
    del ep.arrays["base_pos"]
    assert ep.validate() == []
    m, ok, _ = judge(ep)
    assert ok and abs(m["progress"] - 0.8) < 0.02


def test_schema_catches_bad_logs():
    ep = walk()
    ep.arrays["cmd_vel"] = ep.arrays["cmd_vel"][:10]
    ep.meta["env"] = "lab"
    assert len(ep.validate()) == 2


def test_gap_and_retention():
    rows = [{"condition": "A", "env": e, "task": "straight", "success": s, "failure": "none" if s else "fall", "distance_m": 1.0}
            for e, k in (("sim", 8), ("real", 4)) for s in [True] * k + [False] * (10 - k)]
    a = aggregate(rows, n_boot=200)["conditions"]["A"]
    assert math.isclose(a["gap"], 0.4) and math.isclose(a["retention"], 0.5)
    assert a["gap_ci"][0] <= 0.4 <= a["gap_ci"][1]
    lo, hi = wilson(8, 10)
    assert 0.44 < lo < 0.50 and 0.93 < hi < 0.98
