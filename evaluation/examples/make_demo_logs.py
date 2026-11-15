"""Write SYNTHETIC episodes for all 4 conditions × 2 environments × 4 tasks, so the report
can be tried before any policy exists. The numbers are invented — they show the report's
shape, not a result.   python examples/make_demo_logs.py --out runs_demo
"""
import argparse, sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from s2rbench import Episode, Protocol

p = argparse.ArgumentParser()
p.add_argument("--out", default="runs_demo")
p.add_argument("--trials", type=int, default=10)
a = p.parse_args()

HZ, J, LIMIT, MASS = 50, 10, 0.6, 0.74
P_SUCCESS = {"sim": {"A": 0.75, "B": 0.85, "C": 0.80, "D": 0.85}, "real": {"A": 0.30, "B": 0.40, "C": 0.65, "D": 0.75}}
MODES = {"sim": (["fall", "no_progress", "tracking", "oscillation"], [0.4, 0.2, 0.3, 0.1]),
         "real": (["fall", "no_progress", "tracking", "oscillation", "slip", "saturation"], [0.3, 0.1, 0.1, 0.15, 0.2, 0.15])}
CMD = {"straight": (0.15, 0.0), "endurance": (0.15, 0.0), "turn": (0.0, 0.8), "push_recovery": (0.0, 0.0)}
proto, rng = Protocol(), np.random.default_rng(0)


def make(env, cond, task, trial):
    ok = rng.random() < P_SUCCESS[env][cond]
    mode = None if ok else rng.choice(MODES[env][0], p=MODES[env][1])
    if task == "push_recovery" and not ok:
        mode = "fall"
    T = int(proto.tasks[task]["duration_s"] * HZ)
    fall_at = int(rng.uniform(0.3, 0.8) * T) if mode == "fall" else None
    if task == "push_recovery" and fall_at:
        fall_at = int(2.3 * HZ)
    n = fall_at or T
    t = np.arange(n) / HZ
    vx, wz = CMD[task]
    prog = {None: rng.normal(0.85, 0.06), "fall": 0.7, "no_progress": 0.08, "tracking": 0.42,
            "oscillation": 0.5, "slip": 0.35, "saturation": 0.3}[mode]
    yaw = prog * wz * t
    s = prog * vx * t
    pos = np.stack([s, 0.02 * np.sin(t) * (vx > 0), np.full(n, 0.12)], 1)
    wobble = np.radians(14.0 if mode == "oscillation" else 1.5)
    rpy = np.stack([wobble * np.sin(2 * np.pi * 2 * t), 0.6 * wobble * np.cos(2 * np.pi * 2 * t), yaw], 1)
    perturb = np.zeros(n)
    if task == "push_recovery":
        perturb[(t >= 2.0) & (t < 2.1)] = 2.0
        rpy[:, 0] += np.radians(12) * np.exp(-(t - 2.1).clip(0) / 0.4) * (t >= 2.0)
    if fall_at:
        rpy[-10:, 0] += np.radians(np.linspace(0, 75, 10))
    tau = rng.normal(0, 0.15, (n, J))
    if mode == "saturation":
        tau[:, 0] = LIMIT * np.sign(np.sin(2 * np.pi * t))
    phase = (np.sin(2 * np.pi * 2 * t) > 0)
    contact = np.stack([phase, ~phase], 1).astype(float)
    slip = 0.12 if mode == "slip" else 0.005
    foot = np.zeros((n, 2, 3))
    foot[:, :, 0] = np.cumsum(np.full(n, slip / HZ))[:, None]
    arrays = {"t": t, "base_pos": pos, "base_rpy": rpy, "cmd_vel": np.tile([vx, 0, wz], (n, 1)), "joint_torque": tau,
              "joint_vel": rng.normal(0, 2.0, (n, J)), "action": rng.normal(0, 0.2, (n, J)), "foot_contact": contact,
              "foot_pos": foot, "perturb": perturb}
    meta = {"env": env, "condition": cond, "task": task, "policy_id": f"demo_{cond}", "trial": trial, "robot": "demo",
            "mass_kg": MASS, "torque_limit": LIMIT, "control_hz": HZ, "termination": "fall" if fall_at else "timeout", "synthetic": True}
    return Episode({k: v.astype(np.float32) for k, v in arrays.items()}, meta)


count = 0
for env in ("sim", "real"):
    for cond in "ABCD":
        for task in proto.tasks:
            for trial in range(a.trials):
                make(env, cond, task, trial).save(Path(a.out) / env / f"{cond}_{task}_{trial:02d}.npz")
                count += 1
print(f"wrote {count} synthetic episodes to {a.out}/")
