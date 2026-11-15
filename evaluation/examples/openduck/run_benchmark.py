"""Run the four protocol tasks on Open Duck Mini v2 in CPU MuJoCo with an ONNX walking policy.

Works out of the box with the public pretrained policy, so the whole benchmark can be tried
before training anything:

    git clone https://github.com/apirrone/Open_Duck_Playground
    # policy: BEST_WALK_ONNX_2.onnx from https://github.com/apirrone/Open_Duck_Mini
    python examples/openduck/run_benchmark.py --playground ../Open_Duck_Playground \\
        --onnx BEST_WALK_ONNX_2.onnx --condition A --out runs/openduck/sim
    python -m s2rbench report runs/openduck -o report

For your own policy: train in Open_Duck_Playground, export ONNX, pass it with --onnx and label
it with --condition (A, B, C or D). The observation layout mirrors
playground/open_duck_mini_v2/mujoco_infer.py; only needs numpy, mujoco and onnxruntime.
"""
import argparse, pickle, sys
from pathlib import Path
import numpy as np
import mujoco
import onnxruntime as ort

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from s2rbench import Recorder, Protocol
from s2rbench.mujoco_recorder import MujocoProbe

p = argparse.ArgumentParser()
p.add_argument("--playground", required=True, help="path to a clone of apirrone/Open_Duck_Playground")
p.add_argument("--onnx", required=True)
p.add_argument("--scene", default="scene_flat_terrain_backlash.xml", help="file in playground/open_duck_mini_v2/xmls (training uses the backlash scene)")
p.add_argument("--out", default="runs/openduck/sim")
p.add_argument("--condition", default="A")
p.add_argument("--policy-id", default=None)
p.add_argument("--tasks", nargs="+", default=["straight", "turn", "push_recovery", "endurance"])
p.add_argument("--trials", type=int, default=10)
p.add_argument("--push-n", type=float, default=8.0, help="sideways push force for push_recovery [N], applied 0.1 s")
p.add_argument("--seed", type=int, default=0)
a = p.parse_args()

ROOT = Path(a.playground) / "playground/open_duck_mini_v2"
CMD = {"straight": (0.15, 0.0, 0.0), "turn": (0.0, 0.0, 1.0), "push_recovery": (0.0, 0.0, 0.0), "endurance": (0.10, 0.0, 0.0)}
SIM_DT, DECIM, ACTION_SCALE, VEL_SCALE, MAX_MOTOR_VEL = 0.002, 10, 0.25, 0.05, 5.24
CTRL_DT = SIM_DT * DECIM
PUSH_AT, PUSH_LEN, WARMUP_S = 2.0, 0.1, 1.0

model = mujoco.MjModel.from_xml_path(str(ROOT / "xmls" / a.scene))
model.opt.timestep = SIM_DT
data = mujoco.MjData(model)
policy = ort.InferenceSession(a.onnx, providers=["CPUExecutionProvider"])
period = next(iter(pickle.load(open(ROOT / "data/polynomial_coefficients.pkl", "rb")).values()))["nb_steps_in_period"]
proto = Protocol()

home = model.keyframe("home")
base = model.jnt_bodyid[np.flatnonzero(model.jnt_type == mujoco.mjtJoint.mjJNT_FREE)[0]]
qadr = [model.jnt_qposadr[model.actuator_trnid[i, 0]] for i in range(model.nu)]
vadr = [model.jnt_dofadr[model.actuator_trnid[i, 0]] for i in range(model.nu)]
sens = lambda name: slice(model.sensor(name).adr[0], model.sensor(name).adr[0] + 3)
gyro, accel = sens("gyro"), sens("accelerometer")
floor = model.geom("floor").id
floor_body = model.geom_bodyid[floor]
feet = [model.body("foot_assembly").id, model.body("foot_assembly_2").id]
floor_friction = model.geom_friction[floor].copy()
probe = MujocoProbe(model, base_body=model.body(base).name, foot_sites=("left_foot", "right_foot"), floor_geom="floor")
mass, limit = float(model.body_subtreemass[base]), float(np.abs(model.actuator_forcerange).max())
policy_id = a.policy_id or Path(a.onnx).stem
rng = np.random.default_rng(a.seed)


def contacts():
    return [float(any({model.geom_bodyid[c.geom1], model.geom_bodyid[c.geom2]} == {f, floor_body}
                      for c in data.contact[:data.ncon])) for f in feet]


def run(task, trial):
    friction = float(rng.uniform(0.7, 1.0))                     # small per-trial variation so repeats are not identical
    model.geom_friction[floor] = floor_friction * friction
    mujoco.mj_resetDataKeyframe(model, data, home.id)
    data.qpos[qadr] += rng.normal(0, 0.02, model.nu)
    default = home.ctrl.copy()
    targets = prev_targets = default.copy()
    hist = [np.zeros(model.nu)] * 3
    phase_i, z0 = 0.0, None
    push_dir = rng.choice([-1.0, 1.0])
    duration = proto.tasks[task]["duration_s"]
    rec = Recorder(env="sim", condition=a.condition, task=task, policy_id=policy_id, trial=trial, robot="open_duck_mini_v2",
                   mass_kg=mass, torque_limit=limit, control_hz=1 / CTRL_DT, seed=a.seed,
                   gap_coordinates={"terrain": "flat", "floor_friction_scale": friction},
                   perturbation={"type": "external_force", "magnitude_n": a.push_n, "duration_s": PUSH_LEN} if task == "push_recovery" else None)
    termination = "timeout"
    for step in range(int((WARMUP_S + duration) / CTRL_DT)):
        t = step * CTRL_DT - WARMUP_S                           # t < 0: standing warm-up, not recorded
        cmd = np.array(CMD[task] if t >= 0 else (0, 0, 0), dtype=np.float32)
        phase_i = (phase_i + 1.0) % period
        acc = data.sensordata[accel].copy()
        acc[0] += 1.3
        obs = np.concatenate([data.sensordata[gyro], acc, cmd, np.zeros(4), data.qpos[qadr] - default,
                              data.qvel[vadr] * VEL_SCALE, *hist, targets, contacts(),
                              [np.cos(2 * np.pi * phase_i / period), np.sin(2 * np.pi * phase_i / period)]]).astype(np.float32)
        action = policy.run(None, {"obs": obs[None]})[0][0]
        hist = [action.copy(), hist[0], hist[1]]
        step_lim = MAX_MOTOR_VEL * CTRL_DT
        targets = np.clip(default + action * ACTION_SCALE, prev_targets - step_lim, prev_targets + step_lim)
        prev_targets = targets.copy()
        pushing = task == "push_recovery" and PUSH_AT <= t < PUSH_AT + PUSH_LEN
        data.xfrc_applied[base, 1] = push_dir * a.push_n if pushing else 0.0
        data.ctrl[:] = targets
        mujoco.mj_step(model, data, DECIM)
        if t < 0:
            continue
        z0 = z0 or data.xpos[base, 2]
        row = probe.read(data, cmd_vel=cmd, action=action, perturb=a.push_n if pushing else 0.0)
        row["t"] = t
        rec.step(**row)
        if data.xpos[base, 2] < 0.5 * z0:
            termination = "fall"
            break
    return rec.finish(termination)


for task in a.tasks:
    for trial in range(a.trials):
        ep = run(task, trial)
        ep.save(Path(a.out) / f"{a.condition}_{task}_{trial:02d}.npz")
    print(f"{task}: {a.trials} episodes")
print(f"saved to {a.out}/  (robot mass {mass:.2f} kg, policy {policy_id})")
