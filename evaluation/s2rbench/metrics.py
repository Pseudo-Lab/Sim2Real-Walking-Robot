"""Per-episode metrics. Every function takes an Episode and works for sim and real alike.
Metrics that need a signal the episode lacks come back as NaN rather than a guess."""
from __future__ import annotations
import numpy as np

NAN = float("nan")
G = 9.81


def _tilt_deg(ep):
    return np.degrees(np.hypot(ep.base_rpy[:, 0], ep.base_rpy[:, 1]))


def _unwrap_yaw(ep):
    return np.unwrap(ep.base_rpy[:, 2])


def compute_metrics(ep, protocol):
    t, rpy = ep.t, ep.base_rpy
    dt = float(np.median(np.diff(t))) if ep.n > 1 else NAN
    dur = float(t[-1] - t[0]) + (dt if ep.n > 1 else 0.0)
    task = ep.meta["task"]
    m = {"duration_s": dur}

    # --- stability -----------------------------------------------------------
    tilt = _tilt_deg(ep)
    m["fell"] = bool(ep.meta.get("termination") == "fall" or tilt.max() > protocol.fall_tilt_deg)
    m["roll_rms_deg"] = float(np.degrees(np.sqrt(np.mean(rpy[:, 0] ** 2))))
    m["pitch_rms_deg"] = float(np.degrees(np.sqrt(np.mean(rpy[:, 1] ** 2))))

    # --- motion vs command ---------------------------------------------------
    cmd = ep.cmd_vel if ep.has("cmd_vel") else np.zeros((ep.n, 3), np.float32)
    cmd_dist = float(np.sum(np.hypot(cmd[:, 0], cmd[:, 1])) * dt)
    cmd_yaw = float(np.sum(cmd[:, 2]) * dt)
    if ep.has("base_pos"):
        d = ep.base_pos[-1, :2] - ep.base_pos[0, :2]
        yaw0 = rpy[0, 2]
        fwd = np.array([np.cos(yaw0), np.sin(yaw0)])
        # direction the robot was asked to go, in the world frame at the start
        cv = cmd[:, :2].mean(axis=0)
        if np.linalg.norm(cv) > 1e-6:
            c, s = np.cos(yaw0), np.sin(yaw0)
            fwd = np.array([c * cv[0] - s * cv[1], s * cv[0] + c * cv[1]]) / np.linalg.norm(cv)
        along = float(d @ fwd)
        m["distance_m"] = along
        m["displacement_m"] = float(np.linalg.norm(d))
        m["drift_ratio"] = float(abs(d @ np.array([-fwd[1], fwd[0]])) / max(abs(along), 1e-6))
        m["yaw_turned_deg"] = float(np.degrees(_unwrap_yaw(ep)[-1] - _unwrap_yaw(ep)[0]))
    else:                                   # real robot without tracking: tape-measure values
        m["distance_m"] = float(ep.meta.get("measured_distance_m", NAN))
        m["displacement_m"] = abs(m["distance_m"])
        m["drift_ratio"] = float(ep.meta.get("measured_drift_m", 0.0)) / max(abs(m["distance_m"]), 1e-6)
        m["yaw_turned_deg"] = float(ep.meta.get("measured_yaw_deg", np.degrees(_unwrap_yaw(ep)[-1] - _unwrap_yaw(ep)[0])))
    m["speed_mps"] = m["distance_m"] / dur if dur > 0 else NAN
    if task == "turn":
        m["progress"] = float(m["yaw_turned_deg"] / np.degrees(cmd_yaw)) if abs(cmd_yaw) > 1e-6 else NAN
    else:
        m["progress"] = m["distance_m"] / cmd_dist if cmd_dist > 1e-6 else NAN

    # --- effort --------------------------------------------------------------
    if ep.has("joint_torque"):
        tau = ep.joint_torque
        m["torque_integral"] = float(np.sum(np.abs(tau)) * dt)
        limit = ep.meta.get("torque_limit")
        m["saturation_frac"] = float(np.mean(np.any(np.abs(tau) >= protocol.failure["saturation_level"] * limit, axis=1))) if limit else NAN
        if ep.has("joint_vel") and ep.meta.get("mass_kg") and abs(m["distance_m"]) > 0.05:
            energy = float(np.sum(np.abs(tau * ep.joint_vel)) * dt)      # |mechanical power|, no regeneration
            m["cost_of_transport"] = energy / (ep.meta["mass_kg"] * G * abs(m["distance_m"]))
        else:
            m["cost_of_transport"] = NAN
    else:
        m["torque_integral"] = m["saturation_frac"] = m["cost_of_transport"] = NAN
    m["action_rate"] = float(np.mean(np.abs(np.diff(ep.action, axis=0))) / dt) if ep.has("action") and ep.n > 1 else NAN

    # --- contact -------------------------------------------------------------
    if ep.has("foot_contact", "foot_pos") and ep.n > 1:
        v = np.linalg.norm(np.diff(ep.foot_pos[:, :, :2], axis=0), axis=2) / dt
        on = ep.foot_contact[1:] > 0.5
        m["foot_slip_mps"] = float(v[on].mean()) if on.any() else NAN
    else:
        m["foot_slip_mps"] = NAN

    # --- push recovery -------------------------------------------------------
    m["recovery_time_s"] = _recovery_time(ep, tilt, dt, protocol) if task == "push_recovery" else NAN
    m["obs_invalid_frac"] = float(np.mean(ep.obs_valid < 0.5)) if ep.has("obs_valid") else 0.0
    return m


def _recovery_time(ep, tilt, dt, protocol):
    """Seconds from the end of the push until tilt stays inside the settle band."""
    c = protocol.tasks["push_recovery"]
    if not ep.has("perturb") or not np.any(ep.perturb != 0):
        return NAN
    idx = np.flatnonzero(ep.perturb != 0)
    start, end = idx[0], idx[-1]
    base = tilt[:start].mean() if start > 0 else 0.0
    inside = np.abs(tilt - base) < c["settle_deg"]
    hold = max(1, int(round(c["settle_hold_s"] / dt)))
    for i in range(end + 1, ep.n - hold + 1):
        if inside[i:i + hold].all():
            return float((i - end) * dt)
    return float("inf")
