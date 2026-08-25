#!/usr/bin/env python3
"""Exact-reconstruction parallel of the tower-heavy BBMST model.

This module intentionally rebuilds the upstream exact coefficient families from
Fractions before they are cast to floats. It is a provenance reconstruction and
comparison layer, not a theorem proof.
"""
from __future__ import annotations

import json
import math
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import numpy as np

ROOT = Path(__file__).resolve().parents[1]

# import the numerical reference model, but only for comparison and ordering
import sys
sys.path.insert(0, str(ROOT / 'src'))
import state2275_hn_milp as s
import state2275_tower_heavy_bbmst_v3 as numeric_model

PR = ((1, 3), (2, 5), (4, 7), (8, 11))
CUT_DEFAULT = F(1, 50)


def bits(m: int) -> Tuple[int, ...]:
    return tuple(i for i in range(4) if (m >> i) & 1)


def Gall(m: int) -> F:
    z = F(1)
    for bit, p in PR:
        if m & bit:
            z *= F(p, p - 1)
    return z


def heavy_vectors(m: int, cut: F = CUT_DEFAULT) -> List[Tuple[Tuple[int, ...], F]]:
    ps = [p for bit, p in PR if m & bit]
    maxes = [1 + int(math.floor(math.log(1 / float(cut), p))) + 1 for p in ps]
    arr: List[Tuple[Tuple[int, ...], F]] = []
    for es in product(*[range(1, M + 1) for M in maxes]):
        w = F(1)
        for p, e in zip(ps, es):
            w *= F(1, p ** (e - 1))
        if w < cut:
            continue
        if m not in {12, 13, 14, 15} and all(e == 1 for e in es):
            continue
        arr.append((es, w))
    return arr


def exact_build(cut: F = CUT_DEFAULT):
    R = s.R
    N = len(R)
    FIX = set(s.FIX)
    MIXED = {m for m in range(1, 16) if m.bit_count() >= 2}
    FUT = MIXED - FIX
    f = {m: (Gall(m) if m in FUT else Gall(m) - 1) for m in range(1, 16)}
    cyl = {}
    atom_cyl = {j: [] for j in range(N)}
    for m in range(1, 16):
        I = bits(m)
        groups = {}
        for j, a in enumerate(R):
            groups.setdefault(tuple(a[i] for i in I), []).append(j)
        for v, mem in groups.items():
            k = (m, v)
            cyl[k] = mem
            for j in mem:
                atom_cyl[j].append(k)
    keys = list(cyl)

    hv = {m: heavy_vectors(m, cut) for m in range(1, 16)}
    hsum = {m: sum((w for _, w in hv[m]), F(0)) for m in range(1, 16)}
    tail = {m: max(F(0), f[m] - hsum[m]) for m in range(1, 16)}

    names: List[str] = []
    lb: List[float] = []
    ub: List[float] = []
    integ: List[int] = []

    def add(name, lo=0, hi=float('inf'), integer=False):
        j = len(names)
        names.append(name)
        lb.append(float(lo))
        ub.append(float(hi))
        integ.append(1 if integer else 0)
        return j

    xidx = {}
    for m in range(1, 16):
        mkeys = [k for k in keys if k[0] == m]
        for h, (es, w) in enumerate(hv[m]):
            allowed = None
            if m in FUT and all(e == 1 for e in es):
                allowed = {tuple(v) for v in s.Q[m]}
            for k in mkeys:
                if allowed is not None and tuple(k[1]) not in allowed:
                    continue
                xidx[m, h, k[1]] = add(('x', m, h, es, k[1]), 0, 1, True)

    tidx = {k: add(('tail',) + k, 0, float(tail[k[0]])) for k in keys if tail[k[0]] > 0}
    eidx = {j: add(('e', j), 0, 1, True) for j in range(N)}
    yidx = {k: add(('y',) + k, 0, float('inf')) for k in keys}

    rows: List[Dict[int, F]] = []
    los: List[F] = []
    his: List[F] = []

    def row(d: Dict[int, F], lo: F | None = None, hi: F | None = None):
        rows.append(d)
        los.append(F(-10**18) if lo is None else lo)
        his.append(F(10**18) if hi is None else hi)

    for m in range(1, 16):
        for h, (es, w) in enumerate(hv[m]):
            ids = [j for (mm, hh, v), j in xidx.items() if mm == m and hh == h]
            if m in FUT and all(e == 1 for e in es):
                if not ids:
                    raise ValueError(f'No xids for future squarefree base {m} {h}')
                row({j: F(1) for j in ids}, lo=F(1), hi=F(1))
            else:
                row({j: F(1) for j in ids}, hi=F(1))

    # exact comparator constraints mirror the numerical model's logic.
    baseh = {}
    for m in FUT:
        for h, (es, w) in enumerate(hv[m]):
            if all(e == 1 for e in es):
                baseh[m] = h
                break
    for m in FUT:
        Im = bits(m)
        hm = baseh[m]
        for n in FUT:
            if m >= n or (m & ~n):
                continue
            In = bits(n)
            hn = baseh[n]
            for (mm, hh, mv), jm in list(xidx.items()):
                if mm != m or hh != hm:
                    continue
                js = []
                for (nn, h2, nv), jn in xidx.items():
                    if nn == n and h2 == hn and s.restrict(nv, In, Im) == mv:
                        js.append(jn)
                if js:
                    row({jm: F(1), **{j: F(1) for j in js}}, hi=F(1))

    for m in FUT:
        Im = bits(m)
        hm = baseh[m]
        for U in range(1, 16):
            if m & ~U:
                continue
            IU = bits(U)
            for hu, (es, w) in enumerate(hv[U]):
                if U == m and all(e == 1 for e in es):
                    continue
                for (mm, hh, mv), jm in list(xidx.items()):
                    if mm != m or hh != hm:
                        continue
                    js = []
                    for (uu, h2, uv), ju in xidx.items():
                        if uu == U and h2 == hu and s.restrict(uv, IU, Im) == mv:
                            js.append(ju)
                    if js:
                        row({jm: F(1), **{j: F(1) for j in js}}, hi=F(1))

    for m in range(1, 16):
        es_to_h = {tuple(es): h for h, (es, w) in enumerate(hv[m])}
        for h, (es, w) in enumerate(hv[m]):
            for i, e in enumerate(es):
                if e <= 1:
                    continue
                par = list(es)
                par[i] -= 1
                par = tuple(par)
                hp = es_to_h.get(par)
                if hp is None:
                    continue
                child = [j for (mm, hh, v), j in xidx.items() if mm == m and hh == h]
                parent = [j for (mm, hh, v), j in xidx.items() if mm == m and hh == hp]
                if child:
                    d = {j: F(1) for j in child}
                    for j in parent:
                        d[j] = d.get(j, 0) - F(1)
                    row(d, hi=F(0))

    for m in range(1, 16):
        ids = [tidx[k] for k in keys if k[0] == m and k in tidx]
        if ids:
            row({j: F(1) for j in ids}, hi=tail[m])

    for aidx in range(N):
        d = {eidx[aidx]: F(-1)}
        for m in range(1, 16):
            I = bits(m)
            v = tuple(R[aidx][i] for i in I)
            for h, (_, w) in enumerate(hv[m]):
                j = xidx.get((m, h, v))
                if j is not None:
                    d[j] = d.get(j, 0) + w
            j = tidx.get((m, v))
            if j is not None:
                d[j] = d.get(j, 0) + F(1)
        row(d, lo=F(0))

    for m in range(1, 16):
        row({yidx[k]: F(1) for k in keys if k[0] == m}, hi=F(3 ** m.bit_count()) - F(3, 4))

    for aidx in range(N):
        d = {eidx[aidx]: F(9, 19) if False else F(1)}
        # The original numerical model uses the fixed safety threshold ZF=9.019-0.25;
        # here we record its exact rational provenance without pretending it is a theorem constant.
        d = {eidx[aidx]: F(8769, 1000)}
        for k in atom_cyl[aidx]:
            d[yidx[k]] = F(1)
        row(d, lo=F(8769, 1000))

    row({eidx[j]: F(1) for j in range(N)}, hi=F(N - 1))

    out_meta = {
        'names': names,
        'eidx': eidx,
        'xidx': xidx,
        'tidx': tidx,
        'yidx': yidx,
        'hv': hv,
        'tail': tail,
        'nvars': len(names),
        'nbin': int(sum(integ)),
        'nrows': len(rows),
        'cut': str(cut),
        'ZF': '8769/1000',
    }
    return np.zeros(len(names)), np.array(integ), np.array(lb), np.array(ub), rows, los, his, out_meta


# Compatibility wrapper for the reference numerical build.
def compare_with_numeric(cut: F = CUT_DEFAULT, tol: float = 1e-8):
    exact = exact_build(cut)
    _, _, _, _, rows, lo, hi, meta = exact
    numeric = numeric_model.build(float(cut))
    _, _, numerical_bounds, numerical_constraint, numerical_meta = numeric

    result = {
        'same_variable_count': len(meta['names']) == len(numerical_meta['names']),
        'same_row_count': len(rows) == numerical_constraint.A.shape[0],
        'same_binary_count': meta['nbin'] == int(numerical_meta['nbin']),
        'cut': str(cut),
        'exact_row_pattern': 'mirrored-from-upstream-Fraction-sources',
    }

    if result['same_variable_count'] and result['same_row_count']:
        # dense numerical check on nonzero support, with a tight tolerance.
        for r in range(numerical_constraint.A.shape[0]):
            row_num = numerical_constraint.A.getrow(r)
            row_exact = rows[r]
            nz_num = {int(j): float(v) for j, v in zip(row_num.indices, row_num.data) if abs(float(v)) > 1e-12}
            nz_ex = {j: float(v) for j, v in row_exact.items() if abs(float(v)) > 1e-12}
            if set(nz_num) != set(nz_ex):
                result['support_match'] = False
                result['mismatch_row'] = r
                return result
            for j, v in nz_num.items():
                if abs(v - float(nz_ex[j])) > tol:
                    result['support_match'] = False
                    result['mismatch_row'] = r
                    result['mismatch_col'] = j
                    return result
        result['support_match'] = True
    else:
        result['support_match'] = False
    return result


if __name__ == '__main__':
    exact = exact_build(CUT_DEFAULT)
    _, _, _, _, _, _, _, meta = exact
    print('EXACT_MODEL_VARS', meta['nvars'])
    print('EXACT_MODEL_ROWS', meta['nrows'])
    print('EXACT_MODEL_BINARY', meta['nbin'])
    print(json.dumps(compare_with_numeric(CUT_DEFAULT), indent=2))
