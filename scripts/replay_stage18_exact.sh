#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../src"
python verify_full_state2275_exact.py
