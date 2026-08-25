#!/usr/bin/env python3
"""Simple verifier for the exact Hunter cut replay JSON."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))

from state2275_hunter_exact import exact_cutlog_records, verify_supports


def main() -> int:
    records = exact_cutlog_records()
    verify_supports(records)
    out = ROOT / 'artifacts' / 'card9_exact' / 'HUNTER_CUTS_EXACT.json'
    out.write_text(json.dumps(records, indent=2), encoding='utf-8')
    print(f'HUNTER_EXACT_REPLAY=PASS {len(records)} records')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
