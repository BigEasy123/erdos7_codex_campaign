#!/usr/bin/env python3
"""Standalone exact replay driver for the Erdős #7 state-2275 checkpoint.

This driver invokes no optimizer. It verifies:
  1. the exact Stage-18 Hough--Nielsen restart/gate arithmetic; and
  2. all 12 exact rational Farkas contradictions for the state-2275
     depth-one surplus packet models.
"""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def run(script: str) -> str:
    p = subprocess.run(
        [sys.executable, str(ROOT / script)],
        cwd=ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    print(f"===== {script} =====")
    print(p.stdout, end="" if p.stdout.endswith("\n") else "\n")
    if p.returncode != 0:
        raise SystemExit(f"FAIL: {script} exited {p.returncode}")
    return p.stdout


stage18 = run("verify_stage18_restart_hn_gate.py")
saved = (ROOT / "STAGE18_RESTART_HN_EXACT_OUTPUT.txt").read_text()
if stage18 != saved:
    raise SystemExit("FAIL: Stage-18 exact output does not byte-match saved reference")
print("Stage-18 saved-output byte comparison: PASS\n")

farkas = run("verify_state2275_farkas_stage18_exact.py")
if "ALL 12 DOWNSETS PASS" not in farkas:
    raise SystemExit("FAIL: missing all-12 Farkas pass marker")

print("===== OVERALL =====")
print("STATE2275_FULL_EXACT_REPLAY=PASS")
print("optimizer_calls=0")
