"""Pull the benchmark's signals out of a MuJoCo model. Use from any sim loop:

    probe = MujocoProbe(model, base_body="trunk_base", foot_sites=("left_foot", "right_foot"))
    rec.step(**probe.read(data, cmd_vel=cmd, action=action))
"""
from __future__ import annotations
import numpy as np
import mujoco


class MujocoProbe:
    def __init__(self, model, base_body, foot_sites=None, floor_geom=None):
        self.model = model
        self.base = model.body(base_body).id
        self.sites = [model.site(s).id for s in foot_sites] if foot_sites else None
        # joints driven by actuators, in actuator order
        self.dofs = [model.jnt_dofadr[model.actuator_trnid[i, 0]] for i in range(model.nu)]
        self.floor = model.geom(floor_geom).id if floor_geom else None
        if self.sites:
            self.foot_bodies = [model.site_bodyid[s] for s in self.sites]

    def read(self, data, cmd_vel=(0, 0, 0), action=None, perturb=0.0):
        q = data.xquat[self.base]
        w, x, y, z = q
        rpy = [np.arctan2(2 * (w * x + y * z), 1 - 2 * (x * x + y * y)),
               np.arcsin(np.clip(2 * (w * y - z * x), -1, 1)),
               np.arctan2(2 * (w * z + x * y), 1 - 2 * (y * y + z * z))]
        out = {"t": data.time, "base_pos": data.xpos[self.base].copy(), "base_rpy": rpy, "cmd_vel": cmd_vel,
               "joint_torque": data.actuator_force.copy(), "joint_vel": data.qvel[self.dofs].copy(), "perturb": perturb}
        if action is not None:
            out["action"] = action
        if self.sites:
            out["foot_pos"] = np.stack([data.site_xpos[s] for s in self.sites])
            out["foot_contact"] = [self._touching(data, b) for b in self.foot_bodies]
        return out

    def _touching(self, data, body):
        """1.0 if any geom of `body` is in contact with the world (or the named floor geom)."""
        for c in data.contact[:data.ncon]:
            b1, b2 = self.model.geom_bodyid[c.geom1], self.model.geom_bodyid[c.geom2]
            other = c.geom2 if b1 == body else c.geom1 if b2 == body else None
            if other is None:
                continue
            if (self.floor is None and self.model.geom_bodyid[other] == 0) or other == self.floor:
                return 1.0
        return 0.0
