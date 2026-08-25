#!/usr/bin/env python3
"""Attempt exact threshold Farkas certificates for a saved CARD9 packet."""
from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from card9_exact_phase import exact_dual_check, rational_system
from eonly_phase_benders import PhaseOracle

RECORD = ROOT / "artifacts" / "current_state" / "EONLY_CARD9_GREEDY_PHASE_RECORDS.json"
OUTPUT = ROOT / "artifacts" / "card9_exact" / "PHASE_THRESHOLD_FARKAS_001.json"
DELTAS = (Fraction(1, 100), Fraction(1, 200), Fraction(1, 500), Fraction(1, 1000))


def main() -> int:
    record = json.loads(RECORD.read_text(encoding="utf-8"))[0]
    exhaustion = np.zeros(331, dtype=float)
    exhaustion[record["E"]] = 1.0
    oracle = PhaseOracle()
    rows, bounds, objective = rational_system(oracle, exhaustion)

    matrix = np.zeros((len(rows), len(objective)), dtype=float)
    for row_index, row in enumerate(rows):
        for column, coefficient in row:
            matrix[row_index, column] = float(coefficient)
    result = linprog(
        c=np.asarray(objective, dtype=float),
        A_ub=matrix,
        b_ub=np.asarray(bounds, dtype=float),
        bounds=[(0.0, None)] * len(objective),
        method="highs",
    )
    if result.status != 0:
        raise SystemExit(f"NO_OPTIMAL_PHASE_DUAL status={result.status}")

    base_multipliers = [Fraction(str(max(0.0, -float(value)))) for value in result.ineqlin.marginals]
    attempts = []
    for delta in DELTAS:
        threshold_rows = rows + [[(len(objective) - 1, Fraction(1))]]
        threshold_bounds = bounds + [delta]
        multipliers = base_multipliers + [Fraction(1)]
        valid, lower_bound = exact_dual_check(
            threshold_rows,
            threshold_bounds,
            [Fraction(0)] * len(objective),
            multipliers,
        )
        attempts.append(
            {
                "delta": str(delta),
                "valid": valid,
                "lower_bound": str(lower_bound) if valid else None,
            }
        )
        if valid and lower_bound > 0:
            payload = {
                "status": "PROVED_EXACT",
                "exhaustion": record["E"],
                "delta": str(delta),
                "multipliers": {str(i): str(v) for i, v in enumerate(multipliers) if v},
                "lower_bound": str(lower_bound),
            }
            OUTPUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
            print("PHASE_THRESHOLD_EXACT_REPLAY=PASS")
            print("DELTA", delta)
            print("LOWER_BOUND", lower_bound)
            return 0

    print("PHASE_THRESHOLD_EXACT_REPLAY=BLOCKED")
    print("REASON=FLOAT_DUAL_NOT_EXACTLY_FEASIBLE_AT_TESTED_THRESHOLDS")
    print("ATTEMPTS", json.dumps(attempts, separators=(",", ":")))
    OUTPUT.write_text(
        json.dumps(
            {
                "status": "BLOCKED_DEPENDENCY",
                "exhaustion": record["E"],
                "reason": "FLOAT_DUAL_NOT_EXACTLY_FEASIBLE_AT_TESTED_THRESHOLDS",
                "attempts": attempts,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return 3


if __name__ == "__main__":
    raise SystemExit(main())
