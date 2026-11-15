"""Protocol: task definitions and the success test. All thresholds live in protocol.yaml."""
from __future__ import annotations
from pathlib import Path
import yaml

DEFAULT = Path(__file__).resolve().parent.parent / "protocol.yaml"


class Protocol:
    def __init__(self, path=DEFAULT):
        self.cfg = yaml.safe_load(Path(path).read_text())
        self.tasks = self.cfg["tasks"]
        self.failure = self.cfg["failure"]
        self.fall_tilt_deg = self.cfg["fall"]["tilt_deg"]
        self.version = str(self.cfg["version"])

    def success(self, task, m):
        """m: metrics dict from compute_metrics. Returns True/False."""
        c = self.tasks[task]
        if m["fell"] or m["duration_s"] < 0.95 * c["duration_s"]:
            return False
        if task in ("straight", "endurance"):
            ok = m["progress"] >= c["min_progress"]
            if "max_drift" in c:
                ok = ok and m["drift_ratio"] <= c["max_drift"]
            return bool(ok)
        if task == "turn":
            return bool(m["progress"] >= c["min_progress"] and m["displacement_m"] <= c["max_drift_m"])
        if task == "push_recovery":
            return bool(m["recovery_time_s"] <= c["max_recovery_s"])
        raise KeyError(task)
