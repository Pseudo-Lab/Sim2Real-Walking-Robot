"""s2rbench — one log format, one set of metrics, for simulation and the real robot."""
from .episode import Episode, Recorder, load_dir
from .metrics import compute_metrics
from .failures import classify
from .protocol import Protocol

__version__ = "0.1.0"
