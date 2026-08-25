#!/usr/bin/env python3
"""Fail-closed exact-phase dual replay check.

This script resolves the precise condition required for a real CARD9 dual:
  * build the exact phase system for a saved rejected 9-set;
  * compute the HiGHS dual numerically;
  * check the resulting multipliers with exact Fraction arithmetic;
  * if the exact check fails, emit a clean BLOCKED status instead of a theorem.

The point is not to manufacture a proof; it is to make the proof gate explicit and replayable.
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from card9_exact_phase import rational_system, exact_dual_check
from eonly_phase_benders import PhaseOracle


def load_record(path: Path):
    recs = json.loads(path.read_text(encoding='utf-8'))
    if not recs:
        raise SystemExit('NO_PHASE_RECORDS')
    return recs[0]


def main() -> int:
    data_path = ROOT / 'artifacts' / 'current_state' / 'EONLY_CARD9_GREEDY_PHASE_RECORDS.json'
    record = load_record(data_path)
    E = np.zeros(331, dtype=float)
    E[record['E']] = 1.0

    oracle = PhaseOracle()
    rows, bounds, objective = rational_system(oracle, E)
    A = np.zeros((len(rows), len(objective)), dtype=float)
    for i, row in enumerate(rows):
        for col, value in row:
            A[i, col] = float(value)
    b = np.asarray(bounds, dtype=float)

    result = linprog(
        c=np.asarray(objective, dtype=float),
        A_ub=A,
        b_ub=b,
        bounds=[(0.0, None)] * len(objective),
        method='highs',
    )
    if result.status != 0 or result.x is None:
        print('PHASE_DUAL_CERTIFICATE_STATUS=BLOCKED')
        print('REASON=NO_OPTIMAL_PHASE_DUAL_FOR_SAVED_RECORD')
        print('STATUS', result.status, result.message)
        return 2

    multipliers = [max(0.0, -float(v)) for v in result.ineqlin.marginals]
    valid, lower_bound = exact_dual_check(rows, bounds, objective, multipliers)
    if not valid:
        print('PHASE_DUAL_CERTIFICATE_STATUS=BLOCKED')
        print('REASON=FLOAT_DUAL_FAILED_EXACT_RATIONAL_VERIFICATION')
        print('PRIMAL_OBJECTIVE', result.fun)
        print('MULTIPLIER_COUNT', len(multipliers))
        print('NEGATIVE_MULTIPLIERS', sum(v < 0 for v in multipliers))
        return 3

    print('PHASE_DUAL_CERTIFICATE_STATUS=PASS')
    print('LOWER_BOUND', lower_bound)
    print('PRIMAL_OBJECTIVE', result.fun)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
