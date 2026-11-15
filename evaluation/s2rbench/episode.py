"""Episode log: the single file format shared by simulation and the real robot.

One episode = one .npz file holding per-control-step arrays plus a JSON `meta` string.
If sim and real write the same columns, every metric below applies to both unchanged.
"""
from __future__ import annotations
import json
from dataclasses import dataclass, field
from pathlib import Path
import numpy as np

SCHEMA_VERSION = 1

# name -> trailing shape (None = any). Only `t` and `base_rpy` are mandatory:
# a real robot always has an IMU, but often has no position tracking.
ARRAYS = {
    "t": (),                 # [s] since episode start
    "base_rpy": (3,),        # [rad] roll, pitch, yaw
    "base_pos": (3,),        # [m] world x, y, z          (optional: needs tracking on real robot)
    "cmd_vel": (3,),         # commanded vx [m/s], vy [m/s], wz [rad/s]
    "joint_torque": (None,), # [N·m] (or estimated from current)
    "joint_vel": (None,),    # [rad/s]
    "action": (None,),       # raw policy output
    "foot_contact": (2,),    # 0/1 left, right
    "foot_pos": (2, 3),      # [m] world, left then right
    "perturb": (),           # applied disturbance magnitude (0 when none)
    "battery_v": (),         # [V]
    "obs_valid": (),         # 0/1: sensors healthy this step
}
REQUIRED = ("t", "base_rpy")
META_REQUIRED = ("env", "condition", "task", "policy_id", "trial")
ENVS = ("sim", "real")


@dataclass
class Episode:
    arrays: dict
    meta: dict = field(default_factory=dict)

    def __getattr__(self, name):
        if name in ARRAYS:
            return self.arrays.get(name)
        raise AttributeError(name)

    def has(self, *names):
        return all(self.arrays.get(n) is not None for n in names)

    @property
    def n(self):
        return len(self.arrays["t"])

    def validate(self):
        errors = []
        for k in REQUIRED:
            if k not in self.arrays:
                errors.append(f"missing array '{k}'")
        for k in META_REQUIRED:
            if k not in self.meta:
                errors.append(f"missing meta '{k}'")
        if self.meta.get("env") not in ENVS:
            errors.append(f"meta.env must be one of {ENVS}")
        n = len(self.arrays.get("t", []))
        for k, a in self.arrays.items():
            if k not in ARRAYS:
                errors.append(f"unknown array '{k}'")
                continue
            want = ARRAYS[k]
            if len(a) != n:
                errors.append(f"'{k}' has {len(a)} rows, expected {n}")
            if a.ndim != 1 + len(want) or any(w is not None and w != s for w, s in zip(want, a.shape[1:])):
                errors.append(f"'{k}' has shape {a.shape}, expected (T, {', '.join(str(w or 'J') for w in want)})")
        if n and "base_pos" not in self.arrays and "measured_distance_m" not in self.meta:
            errors.append("no base_pos: put tape-measured 'measured_distance_m' (and 'measured_yaw_deg') in meta")
        return errors

    def save(self, path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        meta = {"schema_version": SCHEMA_VERSION, **self.meta}
        np.savez_compressed(path, meta=json.dumps(meta), **self.arrays)
        return path

    @classmethod
    def load(cls, path):
        with np.load(path, allow_pickle=False) as z:
            meta = json.loads(str(z["meta"]))
            arrays = {k: z[k] for k in z.files if k != "meta"}
        meta["_path"] = str(path)
        return cls(arrays, meta)


class Recorder:
    """Call `step(...)` once per control tick, in sim or on the robot, then `finish()`.

        rec = Recorder(env="real", condition="C", task="straight", policy_id="c_v3", trial=4,
                       mass_kg=0.74, torque_limit=0.6)
        rec.step(t=..., base_rpy=..., cmd_vel=..., joint_torque=...)
        rec.finish(termination="timeout").save("runs/c_v3_real_straight_04.npz")
    """

    def __init__(self, **meta):
        self.meta = meta
        self.rows = {}

    def step(self, **values):
        for k, v in values.items():
            self.rows.setdefault(k, []).append(np.asarray(v, dtype=np.float32))

    def finish(self, termination="timeout", **extra_meta):
        arrays = {k: np.stack(v) for k, v in self.rows.items()}
        return Episode(arrays, {**self.meta, "termination": termination, **extra_meta})


def load_dir(path):
    return [Episode.load(p) for p in sorted(Path(path).rglob("*.npz"))]
