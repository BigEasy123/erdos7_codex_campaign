#!/usr/bin/env python3
"""Fail-closed state-2275 lift audit.

This script checks whether the repository contains the exact local theorem needed to
lift state-2275 to all 7,637 canonical partials. It does not invent such a theorem;
if the discrete lift theorem or exact dominion certificate is absent it exits with a
conservative BLOCKED result, which matches the current evidence.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def has_exact_lift_artifacts() -> bool:
    markers = [
        ROOT / 'artifacts' / 'exact' / 'STATE2275_FULL_EXACT_REPLAY.txt',
        ROOT / 'artifacts' / 'exact' / 'STATE2275_FARKAS_CERTIFICATES_STAGE18_EXACT.json',
        ROOT / 'src' / 'stage24_recompute_7637_fast.py',
    ]
    return all(p.exists() for p in markers)


def stage24_is_exact() -> bool:
    path = ROOT / 'src' / 'stage24_recompute_7637_fast.py'
    text = path.read_text(encoding='utf-8', errors='replace')
    return 'linprog' in text and 'FARKAS' not in text and 'exact' not in text.lower()


def main() -> int:
    exact_artifacts = has_exact_lift_artifacts()
    lp_only = stage24_is_exact()

    if not exact_artifacts:
        print('STATE2275_LIFT_STATUS=BLOCKED')
        print('REASON=MISSING_EXACT_LIFT_ARTIFACTS')
        return 2

    if lp_only:
        print('STATE2275_LIFT_STATUS=BLOCKED')
        print('REASON=STAGE24_RECOMPUTE_IS_NUMERICAL_NOT_EXACT')
        print('REQUIRED=AN_EXACT_DOMINATION_OR_FINITARY_CLASSIFICATION_CERTIFICATE')
        return 3

    # This is still intentionally conservative: exact artifacts exist, but a lift theorem
    # is not proven unless a separate exact dominion certificate is produced and replayed.
    print('STATE2275_LIFT_STATUS=OPEN')
    print('REASON=ARTIFACTS_EXIST_BUT_NO_EXACT_DOMINATION_THEOREM_REPLAYED')
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
