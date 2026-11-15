"""Perturbation audit on the real MicroDuck model in CPU MuJoCo — no trained policy needed.

The robot holds its STAND pose with plain position servos (stiffened to --kp, because the
MJCF default gain only stands up together with the BAM actuator model used in training) and
gets a sideways push of increasing force. This is a stand-in controller, not a walking policy. Each run is logged as a `push_recovery` episode, so this
doubles as an end-to-end test of Recorder -> metrics -> failure labels -> report.

    git clone https://github.com/pollen-robotics/microduck_rl
    python examples/microduck_stand_push.py --microduck-rl ../microduck_rl --out runs_push
    python -m s2rbench report runs_push -o report_push

To benchmark a trained policy instead, replace the `data.ctrl[:] = stand` line with your
policy's joint targets (see microduck_rl/scripts/infer_policy.py) and keep everything else.
"""
import argparse, sys
from pathlib import Path
import numpy as np
import mujoco

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from s2rbench import Recorder
from s2rbench.mujoco_recorder import MujocoProbe

p = argparse.ArgumentParser()
p.add_argument("--microduck-rl", required=True, help="path to a clone of pollen-robotics/microduck_rl")
p.add_argument("--out", default="runs_push")
p.add_argument("--forces", type=float, nargs="+", default=[1, 2, 4, 6, 8, 12])
p.add_argument("--trials", type=int, default=5)
p.add_argument("--kp", type=float, default=2.0, help="servo stiffness for the stand-in controller")
a = p.parse_args()

model = mujoco.MjModel.from_xml_path(str(Path(a.microduck_rl) / "src/mjlab_microduck/robot/microduck/scene.xml"))
model.actuator_gainprm[:, 0] = a.kp
model.actuator_biasprm[:, 1] = -a.kp
data = mujoco.MjData(model)
probe = MujocoProbe(model, base_body="trunk_base", foot_sites=("left_foot", "right_foot"))
trunk = model.body("trunk_base").id
mass = float(model.body_subtreemass[trunk])
limit = float(np.abs(model.actuator_forcerange).max()) or None
CONTROL_HZ, DURATION, PUSH_AT, PUSH_LEN = 50, 8.0, 2.0, 0.1
decim = int(round(1 / CONTROL_HZ / model.opt.timestep))
rng = np.random.default_rng(0)

for force in a.forces:
    for trial in range(a.trials):
        mujoco.mj_resetDataKeyframe(model, data, model.key("STAND").id)
        stand = data.ctrl.copy()
        direction = rng.uniform(0, 2 * np.pi)                  # push from a random side each trial
        f_xy = force * np.array([np.cos(direction), np.sin(direction)])
        rec = Recorder(env="sim", condition=f"push_{force:g}N", task="push_recovery", policy_id="pd_stand",
                       trial=trial, robot="microduck", mass_kg=mass, torque_limit=limit, control_hz=CONTROL_HZ,
                       perturbation={"type": "external_force", "magnitude_n": force, "direction_rad": direction})
        termination = "timeout"
        for step in range(int(DURATION * CONTROL_HZ)):
            pushing = PUSH_AT <= data.time < PUSH_AT + PUSH_LEN
            data.xfrc_applied[trunk, :2] = f_xy if pushing else 0.0
            data.ctrl[:] = stand
            mujoco.mj_step(model, data, decim)
            rec.step(**probe.read(data, perturb=force if pushing else 0.0))
            if data.xpos[trunk, 2] < 0.06:                     # trunk on the floor
                termination = "fall"
                break
        rec.finish(termination).save(Path(a.out) / f"pd_stand_push{force:g}N_{trial:02d}.npz")
print(f"wrote {len(a.forces) * a.trials} episodes to {a.out}/  (robot mass {mass:.2f} kg)")
