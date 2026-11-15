"""Failure taxonomy: every failed episode gets one primary label plus all flags that fired.
Rules are checked from most to least specific, so 'fall' explains a run before 'no_progress' does."""
from __future__ import annotations
import math

LABELS = ["observation_failure", "recovery_failure", "fall", "actuator_saturation",
          "foot_slip", "oscillation", "no_progress", "tracking_error"]


def classify(ep, m, success, protocol):
    """Returns (primary_label, flags). primary_label is 'none' for a successful episode."""
    f, task = protocol.failure, ep.meta["task"]

    def over(key, thr):
        v = m.get(key, math.nan)
        return not math.isnan(v) and v > thr

    flags = {
        "observation_failure": over("obs_invalid_frac", f["obs_invalid_frac"]),
        "recovery_failure": task == "push_recovery" and (m["fell"] or m["recovery_time_s"] == math.inf),
        "fall": m["fell"],
        "actuator_saturation": over("saturation_frac", f["saturation_frac"]),
        "foot_slip": over("foot_slip_mps", f["slip_speed_mps"]),
        "oscillation": over("roll_rms_deg", f["oscillation_deg"]) or over("pitch_rms_deg", f["oscillation_deg"]),
        "no_progress": task != "push_recovery" and not math.isnan(m["progress"]) and m["progress"] < f["no_progress"],
        "tracking_error": True,          # catch-all: failed the task criteria with no clearer cause
    }
    fired = [k for k in LABELS if flags[k]]
    if success:
        return "none", [k for k in fired if k != "tracking_error"]
    # a fall caused by a saturated or slipping run is more usefully labelled by its cause
    for cause in ("observation_failure", "recovery_failure", "actuator_saturation", "foot_slip"):
        if flags[cause]:
            return cause, fired
    return fired[0], fired
