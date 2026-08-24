#!/usr/bin/env python3
"""Optimizer-free verifier for rational CARD9 phase lower-bound certificates."""
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from card9_exact_phase import exact_dual_check, rational_system
from eonly_phase_benders import PhaseOracle


def verify(path: Path) -> Fraction:
    data = json.loads(path.read_text(encoding="utf-8"))
    exhaustion = np.zeros(331)
    exhaustion[data["exhaustion"]] = 1
    oracle = PhaseOracle()
    rows, bounds, objective = rational_system(oracle, exhaustion)
    multipliers = [Fraction(0)] * len(rows)
    for index, value in data["multipliers"].items():
        multipliers[int(index)] = Fraction(value)
    valid, lower_bound = exact_dual_check(rows, bounds, objective, multipliers)
    if not valid:
        raise SystemExit("INVALID_EXACT_PHASE_CERTIFICATE")
    expected = Fraction(data["lower_bound"])
    if lower_bound != expected:
        raise SystemExit("CERTIFICATE_BOUND_MISMATCH")
    return lower_bound


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: verify_card9_phase_certificate.py CERTIFICATE.json")
    print("PHASE_CERTIFICATE_VALID", verify(Path(sys.argv[1])))
