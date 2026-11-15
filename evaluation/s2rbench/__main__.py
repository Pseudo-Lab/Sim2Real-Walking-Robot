"""Command line:
    python -m s2rbench validate runs/            check every log against the schema
    python -m s2rbench report runs/ -o report/   write report.md, results.json, report.png
"""
import argparse, sys
from .episode import load_dir
from .protocol import Protocol, DEFAULT
from .report import write_report, to_markdown, aggregate, evaluate

p = argparse.ArgumentParser(prog="s2rbench")
p.add_argument("command", choices=["validate", "report"])
p.add_argument("runs")
p.add_argument("-o", "--out", default="report")
p.add_argument("--protocol", default=str(DEFAULT))
a = p.parse_args()

episodes = load_dir(a.runs)
if not episodes:
    sys.exit(f"no .npz episodes under {a.runs}")
bad = 0
for ep in episodes:
    for e in ep.validate():
        bad += 1
        print(f"{ep.meta['_path']}: {e}")
if a.command == "validate" or bad:
    print(f"{len(episodes)} episodes, {bad} problems")
    sys.exit(1 if bad else 0)
proto = Protocol(a.protocol)
agg = write_report(episodes, proto, a.out)
print(to_markdown(agg, proto.version).split("## Per task")[0])
print(f"written to {a.out}/")
