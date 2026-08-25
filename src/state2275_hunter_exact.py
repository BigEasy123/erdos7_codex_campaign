#!/usr/bin/env python3
"""Exact Hunter cut regeneration from the upstream Fraction-valued source.

This is a provenance and replay check: the richer exact heavy weights are taken
from the upstream tower-heavy BBMST model and then used to rebuild the same cuts
stored in the historical cut log without reintroducing the float matrix.
"""
from __future__ import annotations

import json
import math
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

import sys
sys.path.insert(0, str(ROOT / 'src'))
import state2275_hn_milp as s
import state2275_tower_heavy_bbmst_v3 as base

P = (3, 5, 7, 11)
R = s.R
N = len(R)
CUTLOG = ROOT / 'artifacts' / 'current_state' / 'HUNTER_V2_CUTLOG.json'
OUTPUT = ROOT / 'artifacts' / 'card9_exact' / 'HUNTER_CUTS_EXACT.json'


def qres(m: int, es: tuple[int, ...]) -> int:
    q = 1
    for i, e in zip(s.bits(m), es):
        q *= P[i] ** (e - 1)
    return q


def heavy_vectors(m: int, cut: F = F(1, 50)):
    ps = [p for bit, p in ((1, 3), (2, 5), (4, 7), (8, 11)) if m & bit]
    maxes = [1 + int(math.floor(math.log(1 / float(cut), p))) + 1 for p in ps]
    out = []
    for es in __import__('itertools').product(*[range(1, M + 1) for M in maxes]):
        w = F(1)
        for p, e in zip(ps, es):
            w *= F(1, p ** (e - 1))
        if w < cut:
            continue
        if m not in {12, 13, 14, 15} and all(e == 1 for e in es):
            continue
        out.append((es, w))
    return out


def maxforest(nodes):
    edges = []
    for a in range(len(nodes)):
        for b in range(a + 1, len(nodes)):
            qa, qb = int(nodes[a][1]), int(nodes[b][1])
            if math.gcd(qa, qb) == 1:
                edges.append((F(1, qa * qb), a, b))
    edges.sort(reverse=True, key=lambda z: z[0])
    par = list(range(len(nodes)))

    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x

    out = []
    for w, a, b in edges:
        x, y = find(a), find(b)
        if x != y:
            par[x] = y
            out.append((w, a, b))
    return out


def build_context(cut: float = 0.02):
    z = base.build(cut)
    if z is None:
        return None
    _, _, _, _, meta = z
    exact_hv = {m: heavy_vectors(m, F(1, 50)) for m in range(1, 16)}
    cand = {aidx: [] for aidx in range(N)}
    for (m, h, v), j in meta['xidx'].items():
        es, _ = exact_hv[m][h]
        q = qres(m, es)
        I = s.bits(m)
        for aidx, a in enumerate(R):
            if tuple(a[i] for i in I) == v:
                cand[aidx].append((j, q, exact_hv[m][h][1], m, h))
    tailvars = {aidx: [] for aidx in range(N)}
    for (m, v), j in meta['tidx'].items():
        I = s.bits(m)
        for aidx, a in enumerate(R):
            if tuple(a[i] for i in I) == v:
                tailvars[aidx].append(j)
    return meta, cand, tailvars, exact_hv


def make_cut(aidx, active_nodes, all_nodes, tail_ids, meta, exact_hv):
    forest = maxforest(active_nodes)
    d = {meta['eidx'][aidx]: F(1)}
    for j, q, w, m, h in all_nodes:
        d[j] = d.get(j, 0) - w
    for j in tail_ids:
        d[j] = d.get(j, 0) - F(1)
    rhs = F(0)
    for wij, u, v in forest:
        ju = active_nodes[u][0]
        jv = active_nodes[v][0]
        rhs += wij
        d[ju] = d.get(ju, 0) + wij
        d[jv] = d.get(jv, 0) + wij
    return d, rhs, forest


def exact_cutlog_records():
    ctx = build_context(0.02)
    if ctx is None:
        raise RuntimeError('Reference build failed')
    meta, cand, tailvars, exact_hv = ctx
    logs = json.loads(CUTLOG.read_text(encoding='utf-8'))
    records = []
    for entry in logs:
        aidx = int(entry['aidx'])
        active_idx = set(entry['active'])
        active = [q for q in cand[aidx] if q[0] in active_idx]
        d, rhs, forest = make_cut(aidx, active, cand[aidx], tailvars[aidx], meta, exact_hv)
        record = {
            'aidx': aidx,
            'active': sorted(active_idx),
            'rhs': str(rhs),
            'forest': [[str(w), u, v] for w, u, v in forest],
            'support': [{'j': j, 'coeff': str(coeff)} for j, coeff in sorted(d.items()) if coeff != 0],
        }
        records.append(record)
    return records


def verify_supports(records):
    ctx = build_context(0.02)
    if ctx is None:
        raise RuntimeError('Reference build failed')
    meta, cand, tailvars, exact_hv = ctx
    for rec in records:
        aidx = int(rec['aidx'])
        active_idx = set(rec['active'])
        active = [q for q in cand[aidx] if q[0] in active_idx]
        d, rhs, forest = make_cut(aidx, active, cand[aidx], tailvars[aidx], meta, exact_hv)
        exact_support = {int(item['j']): F(item['coeff']) for item in rec['support']}
        if exact_support != {j: coeff for j, coeff in d.items()}:
            raise ValueError(f'CUT SUPPORT MISMATCH for aidx={aidx}')
        if F(rec['rhs']) != rhs:
            raise ValueError(f'CUT RHS MISMATCH for aidx={aidx}')
    return True


if __name__ == '__main__':
    records = exact_cutlog_records()
    verify_supports(records)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(records, indent=2), encoding='utf-8')
    print(f'WROTE {OUTPUT}')
    print(f'CUT_RECORDS {len(records)}')
