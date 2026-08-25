#!/usr/bin/env python3
"""Compare the repository's floating phase model against the exact provenance ledger.

This is deliberately a provenance check, not a proof of infeasibility. The script
inspects known exact families and surfaces any coefficient family that still
depends on float arithmetic.
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import state2275_child_pooled_master as pooled


def compare() -> dict:
    exact = json.loads((ROOT / "artifacts" / "card9_exact" / "RATIONAL_MODEL_SCHEMA.json").read_text(encoding="utf-8"))
    _, integrality, bounds, constraints, meta = pooled.build(.02, .2, True)

    comparators = {
        "integer_incidence": {
            "exact": True,
            "observed": {"n_rows": int(constraints.A.shape[0]), "n_vars": int(constraints.A.shape[1])},
        },
        "hn_constants": {
            "exact": True,
            "observed": {"alpha_from_doc": True, "beta_from_doc": True},
        },
        "pooled_child_weights": {
            "exact": False,
            "observed": {
                "status": "float-generated in state2275_child_pooled_master.py",
                "meta_keys": sorted(meta.keys())[:10],
            },
        },
        "hunter_cut_rows": {
            "exact": False,
            "observed": {"status": "historical cut log lacks exact coefficient provenance"},
        },
    }
    return {
        "status": "BLOCKED_DEPENDENCY",
        "provenance": exact,
        "comparison": comparators,
        "conclusion": "The repository still contains float-sourced phase coefficients; no exact certificate should be promoted from this model.",
    }


def main() -> None:
    result = compare()
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
