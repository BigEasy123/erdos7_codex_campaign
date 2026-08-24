#!/usr/bin/env python3
from __future__ import annotations
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / 'src'


def main() -> int:
    bad = []
    missing = []
    for rel in ['src/card9_sparse_exact_benders.py', 'src/eonly_phase_benders.py']:
        p = ROOT / rel
        if not p.exists():
            bad.append(f'missing file: {rel}')
            continue
        txt = p.read_text(encoding='utf-8', errors='replace')
        if '/mnt/data/erdos2275' in txt:
            bad.append(f'absolute path still present in {rel}')
    helper = SRC / 'eonly_card9_hybridprefix.py'
    if not helper.exists():
        missing.append(str(helper.relative_to(ROOT)))

    print('ROOT', ROOT)
    print('HELPER_EXISTS', helper.exists())
    print('MISSING_HELPER', missing or 'none')
    print('ABSOLUTE_PATHS', bad or 'none')

    if missing or bad:
        return 2

    sys.path.insert(0, str(SRC))
    try:
        import state2275_hn_milp as s  # type: ignore
        print('CORE_IMPORT_OK', len(s.R))
    except Exception as exc:  # pragma: no cover
        print('CORE_IMPORT_FAIL', type(exc).__name__, exc)
        return 3

    print('CARD9_REPO_RELATIVE_CHECK=PASS')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
