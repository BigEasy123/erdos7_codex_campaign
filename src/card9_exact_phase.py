#!/usr/bin/env python3
"""Rational phase-system extraction and exact lower-bound certificate support."""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import json
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from eonly_phase_benders import PhaseOracle


def q(value: float | int) -> Fraction:
    return Fraction(str(value))


def rational_system(oracle: PhaseOracle, exhaustion: np.ndarray):
    """Return A,d,c for a nonnegative-variable min c*z subject to A*z <= d.

    The phase variables have zero lower bounds. Finite upper bounds are appended
    as rows, making the returned system suitable for an optimizer-free dual check.
    """
    rhs = oracle.rhs(exhaustion)
    rows = []
    bounds = []
    for row in range(oracle.B.shape[0]):
        entries = [(int(col), q(value)) for col, value in zip(oracle.B.getrow(row).indices, oracle.B.getrow(row).data) if value]
        rows.append(entries)
        bounds.append(q(rhs[row]))
    offset = oracle.B.shape[1]
    for col, bound in enumerate(oracle.bounds[:-1]):
        upper = bound[1]
        if upper is not None:
            rows.append([(col, Fraction(1))])
            bounds.append(q(upper))
    objective = [Fraction(0)] * oracle.B.shape[1]
    objective[-1] = Fraction(1)
    return rows, bounds, objective


def exact_dual_check(rows, bounds, objective, multipliers):
    """Check a lower-bound dual using only integer/Fraction arithmetic."""
    if len(multipliers) != len(rows) or any(value < 0 for value in multipliers):
        return False, None
    lhs = [Fraction(value) for value in objective]
    for multiplier, row in zip(multipliers, rows):
        for col, coefficient in row:
            lhs[col] -= multiplier * coefficient
    if any(value < 0 for value in lhs):
        return False, None
    lower_bound = -sum(multiplier * bound for multiplier, bound in zip(multipliers, bounds))
    return True, lower_bound


def write_float_candidate(path: Path, oracle: PhaseOracle, exhaustion: np.ndarray, result) -> None:
    rows, bounds, objective = rational_system(oracle, exhaustion)
    # SciPy's <= marginals are nonpositive in this minimization convention.
    multipliers = [q(max(0.0, -float(value))) for value in result.ineqlin.marginals]
    multipliers.extend(q(max(0.0, -float(value))) for value in result.upper.marginals[:-1])
    valid, lower_bound = exact_dual_check(rows, bounds, objective, multipliers)
    if not valid:
        raise ValueError("floating dual did not pass exact rational verification")
    nonzero = {str(index): str(value) for index, value in enumerate(multipliers) if value}
    path.write_text(json.dumps({"exhaustion": np.flatnonzero(exhaustion).tolist(), "multipliers": nonzero, "lower_bound": str(lower_bound)}, indent=2), encoding="utf-8")
