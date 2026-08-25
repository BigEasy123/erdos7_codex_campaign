#!/usr/bin/env python3
"""Fail-closed verifier for a future exact min-exhaustion certificate."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = ROOT / "artifacts" / "card9_exact" / "MIN_EXHAUST_GT8_FARKAS.json"


def main() -> int:
    if not CERTIFICATE.exists():
        print("MIN_EXHAUST_GT8_EXACT_REPLAY=BLOCKED")
        print("REASON=NO_EXACT_CERTIFICATE")
        return 2
    data = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if data.get("status") != "PROVED_EXACT":
        print("MIN_EXHAUST_GT8_EXACT_REPLAY=BLOCKED")
        print("REASON=EXACT_CERTIFICATE_NOT_PROVED")
        print("STATUS", data.get("status"))
        return 3
    raise SystemExit("CERTIFICATE_REPLAY_NOT_IMPLEMENTED")


if __name__ == "__main__":
    raise SystemExit(main())
