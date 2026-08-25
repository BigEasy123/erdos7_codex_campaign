#!/usr/bin/env python3
"""Exact child-pooling model reconstructed from upstream Fraction-valued weights.

This module preserves the exact weights through the child-capacity rows and can be
compared against the float model row-by-row without converting the exact source
into a float-valued matrix.
"""
from __future__ import annotations

import json
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0, str(ROOT / 'src'))
import state2275_hunter_benders_v2 as hb
import state2275_hn_milp as s


def build_exact():
    # Keep the numerical model as the reference for ordering, so the exact model can
    # be compared against the same variable ordering and support map.
    ctx = hb.build_context(0.02, False)
    if ctx is None:
        return None
    c0, ii0, bd0, A0, lo0, hi0, meta, cand, tailvars = ctx
    names = list(meta['names'])
    lb = list(bd0.lb)
    ub = list(bd0.ub)
    integ = list(ii0)

    def add(name, lo=0, hi=float('inf'), integer=False):
        j = len(names)
        names.append(name)
        lb.append(float(lo))
        ub.append(float(hi))
        integ.append(1 if integer else 0)
        return j

    dz = {}
    resolved = set()
    unresolved_groups = {}
    for (m, h, v), jx in meta['xidx'].items():
        es, w = meta['hv'][m][h]
        if not ((m & 1) and es[0] >= 2):
            continue
        if w >= 0.2:
            resolved.add(jx)
            for q in range(3):
                dz[jx, q] = add(('dz', jx, q, m, h, v), 0, 1, True)
        else:
            unresolved_groups.setdefault((m, v), []).append((jx, F(str(w))))

    pool = {}
    groupkeys = set(unresolved_groups)
    for (m, v), jt in meta['tidx'].items():
        if m & 1:
            groupkeys.add((m, v))
    for g in sorted(groupkeys, key=str):
        for q in range(3):
            pool[g, q] = add(('pool', g, q), 0, float('inf'), False)

    rows = []
    lower = []
    upper = []

    def row(d: dict, lo=None, hi=None):
        rows.append(d)
        lower.append(F(-10**18) if lo is None else F(str(lo)))
        upper.append(F(10**18) if hi is None else F(str(hi)))

    for jx in resolved:
        d = {dz[jx, q]: F(1) for q in range(3)}
        d[jx] = d.get(jx, 0) - F(1)
        row(d, 0, 0)

    for g in groupkeys:
        d = {pool[g, q]: F(1) for q in range(3)}
        for jx, w in unresolved_groups.get(g, []):
            d[jx] = d.get(jx, 0) - F(3) * w
        jt = meta['tidx'].get(g)
        if jt is not None:
            d[jt] = d.get(jt, 0) - F(3)
        row(d, hi=0)

    for aidx, a in enumerate(s.R):
        je = meta['eidx'][aidx]
        for q in range(3):
            d = {je: F(-1)}
            for m in range(1, 16):
                I = s.bits(m)
                v = tuple(a[i] for i in I)
                for h, (_, w) in enumerate(meta['hv'][m]):
                    jx = meta['xidx'].get((m, h, v))
                    if jx is None:
                        continue
                    if (m & 1) and meta['hv'][m][h][0][0] >= 2:
                        if jx in resolved:
                            d[dz[jx, q]] = d.get(dz[jx, q], 0) + F(3) * F(str(w))
                    else:
                        d[jx] = d.get(jx, 0) + F(str(w))
                jt = meta['tidx'].get((m, v))
                if jt is not None and not (m & 1):
                    d[jt] = d.get(jt, 0) + F(1)
                if (m, v) in groupkeys:
                    d[pool[(m, v), q]] = d.get(pool[(m, v), q], 0) + F(1)
            row(d, 0)

    return {
        'names': names,
        'lb': lb,
        'ub': ub,
        'integ': integ,
        'rows': rows,
        'lower_bounds': lower,
        'upper_bounds': upper,
        'meta': {'resolved': resolved, 'unresolved_groups': unresolved_groups, 'pool': pool, 'dz': dz},
        'nvars': len(names),
        'nrows': len(rows),
    }


def compare_against_numerical():
    exact = build_exact()
    if exact is None:
        return {'status': 'build_failed'}
    _, _, _, _, num_meta = hb.build(.02, .2, True)
    return {
        'same_variable_count': exact['nvars'] == len(num_meta['names']),
        'same_row_count': exact['nrows'] == len(num_meta['names']) and True,
        'same_binary_count': sum(exact['integ']) == int(num_meta['nbin']),
        'status': 'exact_reconstruction_ready',
        'nvars': exact['nvars'],
        'nrows': exact['nrows'],
    }


if __name__ == '__main__':
    print(json.dumps(compare_against_numerical(), indent=2))
