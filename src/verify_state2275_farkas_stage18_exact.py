#!/usr/bin/env python3
"""Exact replay of the 12 state-2275 depth-one surplus Farkas certificates.

This script DOES NOT invoke an LP/MIP optimizer.  It rebuilds the finite
state-2275 feasibility model's sparsity from state2275_hn_milp.py, replaces
all numerical coefficients/bounds by exact Fraction values, and verifies the
saved nonnegative Farkas multipliers.

For a system C x <= d, x >= 0, a certificate lambda >= 0 with
    C^T lambda >= 0   and   d^T lambda < 0
is a contradiction: for any x >= 0, the left side
(C^T lambda)^T x is >= 0, while summing the inequalities gives it <= d^T
lambda < 0.

The HN tangent-plane constants in this checkpoint are the exact rational values
reproduced by verify_stage18_restart_hn_gate.py.  Thus this replay uses the
Stage-18 rational gate itself, not rounded decimal surrogates.
"""
from __future__ import annotations

import json
import math
import sys
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
CERT_PATH = HERE / "STATE2275_FARKAS_CERTIFICATES_STAGE18_EXACT.json"
sys.path.insert(0, str(HERE))
import state2275_hn_milp as model  # noqa: E402


def frac(s: str) -> F:
    return F(s)


def load_cert():
    d = json.loads(CERT_PATH.read_text())
    p = d["exact_parameters"]
    A = frac(p["ALPHA"])
    B = frac(p["BETA"])
    R = frac(p["HRHS"])
    Z = frac(p["ZH"])
    assert Z == R - A - B
    return d, A, B, R, Z


def hn_weights(A: F, B: F):
    # The only HN moment-pair weights appearing in build_any.
    l3 = lambda e: (e + 1) ** 3 - e**3
    vals = set()
    for e in range(3):
        for b5 in range(2):
            for b7 in range(2):
                for b11 in range(2):
                    if e == b5 == b7 == b11 == 0:
                        continue
                    ell2 = (2 * e + 1) * (3 if b5 else 1) * (3 if b7 else 1) * (3 if b11 else 1)
                    ell3 = l3(e) * l3(b5) * l3(b7) * l3(b11)
                    vals.add(A * ell2 + B * ell3)
    return sorted(vals)


def exact_matrix_entry(v: float, Z: F) -> F:
    # build_any uses only -1, +1, and +ZH in its sparse matrix.
    candidates = [F(-1), F(1), Z]
    q = min(candidates, key=lambda z: abs(float(z) - v))
    if abs(float(q) - v) > 1e-12:
        raise AssertionError(f"unrecognized matrix coefficient {v!r}")
    return q


def exact_bound(v: float, Z: F, weights: list[F]) -> F:
    # Finite row bounds are 0, +/-1, +/-ZH, or an HN support budget weight.
    candidates = [F(-1), F(0), F(1), -Z, Z] + weights
    q = min(candidates, key=lambda z: abs(float(z) - v))
    if abs(float(q) - v) > 1e-11:
        raise AssertionError(f"unrecognized finite row bound {v!r}")
    return q


def inequalities(M: int, Z: F, weights: list[F]):
    """Return exact Cx<=d rows in the SAME row order used by certificate generation.

    Ordering is: all original upper bounds; then all negated original lower bounds;
    then finite variable upper bounds. Variable nonnegativity x>=0 is kept as the
    Farkas cone condition rather than encoded as rows.
    """
    built, meta = model.build_any(M)
    c, integ, bounds, con = built
    A = con.A.tocsr()
    n = A.shape[1]
    out = []

    # 1. Original upper bounds.
    for r, h in enumerate(con.ub):
        if math.isfinite(float(h)):
            row = A.getrow(r)
            coeff = {int(j): exact_matrix_entry(float(v), Z) for j, v in zip(row.indices, row.data)}
            out.append((coeff, exact_bound(float(h), Z, weights), ("row_hi", r)))

    # 2. Negated original lower bounds.
    for r, l in enumerate(con.lb):
        if math.isfinite(float(l)):
            row = A.getrow(r)
            coeff = {int(j): -exact_matrix_entry(float(v), Z) for j, v in zip(row.indices, row.data)}
            out.append((coeff, -exact_bound(float(l), Z, weights), ("row_lo", r)))

    # 3. Finite variable upper bounds. Lower bounds are all zero and define x>=0.
    for j, u in enumerate(bounds.ub):
        if math.isfinite(float(u)):
            assert abs(float(u) - 1.0) < 1e-15
            out.append(({j: F(1)}, F(1), ("var_ub", j)))
    for l in bounds.lb:
        assert abs(float(l)) < 1e-15

    return out, n, meta


def verify_one(key: str, rec: dict, Acoef: F, Bcoef: F, Z: F):
    M = int(key, 16)
    weights = hn_weights(Acoef, Bcoef)
    rows, n, meta = inequalities(M, Z, weights)
    den = int(rec["multiplier_denominator"])
    col = [F(0) for _ in range(n)]
    rhs = F(0)
    total_lam = F(0)

    prev = -1
    for idx, num in rec["active_multipliers"]:
        idx = int(idx); num = int(num)
        assert idx > prev, "active multiplier row indices must be strictly increasing"
        prev = idx
        assert 0 <= idx < len(rows)
        assert num > 0
        lam = F(num, den)
        total_lam += lam
        coeff, d, _tag = rows[idx]
        rhs += lam * d
        for j, q in coeff.items():
            col[j] += lam * q

    mincol = min(col)
    saved_rhs = F(int(rec["farkas_rhs_numerator"]), int(rec["farkas_rhs_denominator"]))
    saved_min = F(int(rec["min_column_numerator"]), int(rec["min_column_denominator"]))

    assert rhs == saved_rhs, (key, "rhs mismatch", rhs, saved_rhs)
    assert mincol == saved_min, (key, "min-column mismatch", mincol, saved_min)
    assert mincol >= 0, (key, "negative Farkas column", mincol)
    assert rhs < 0, (key, "nonnegative Farkas rhs", rhs)
    assert len(rec["active_multipliers"]) == int(rec["support"])

    return {
        "M": key,
        "variables": n,
        "inequalities": len(rows),
        "active_multipliers": len(rec["active_multipliers"]),
        "lambda_sum": total_lam,
        "rhs": rhs,
        "min_column": mincol,
        "model_rows": meta["rows"],
    }


def main():
    cert, Acoef, Bcoef, R, Z = load_cert()
    print("Erdos #7 state-2275 exact Farkas replay")
    print("No optimizer is called.")
    print("ALPHA =", Acoef)
    print("BETA  =", Bcoef)
    print("HRHS  =", R)
    print("ZH    =", Z)
    print()

    results = []
    for key, rec in cert["downsets"].items():
        z = verify_one(key, rec, Acoef, Bcoef, Z)
        results.append(z)
        print(
            f"{key:>4} PASS  vars={z['variables']:4d}  ineq={z['inequalities']:4d}  "
            f"support={z['active_multipliers']:4d}  "
            f"rhs={float(z['rhs']): .12g}  mincol={float(z['min_column']): .12g}"
        )

    assert len(results) == 12
    worst_rhs = max(z["rhs"] for z in results)  # closest to zero
    worst_col = min(z["min_column"] for z in results)
    print()
    print("ALL 12 DOWNSETS PASS")
    print("least-negative rhs (closest to 0) =", worst_rhs, "~", float(worst_rhs))
    print("smallest exact column margin       =", worst_col, "~", float(worst_col))


if __name__ == "__main__":
    main()
