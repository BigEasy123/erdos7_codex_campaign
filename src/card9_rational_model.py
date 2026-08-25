#!/usr/bin/env python3
"""Exact provenance ledger for the CARD9 phase LP.

This module deliberately does not guess an exact proof object for the floating
phase LP. Instead, it records which coefficient families are known to be exact
integer/rational objects from the repository, and which families remain
BLOCKED_DEPENDENCY because the source implementation still stores them as floats.
"""
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]


def q(num: int | str | Fraction) -> Fraction:
    if isinstance(num, Fraction):
        return num
    if isinstance(num, int):
        return Fraction(num, 1)
    return Fraction(num)


def hn_constants() -> Dict[str, Fraction]:
    """Exact HN constants already recorded in the project documentation."""
    return {
        "alpha": q("51603567726348558328760981369659084133279683367") / q("4373107200000000000000000000000000000000000000000"),
        "beta": q("14493601981951") / q("13781250000000000"),
        "R_HN": q("1985876874482391730913463316715795569734245382761") / q("4115865600000000000000000000000000000000000000000"),
        "HRHS": q("48249312963046986") / q("100000000000000000"),
    }


def exact_family_summary() -> Dict[str, object]:
    """Return the exact provenance ledger for the known coefficient families."""
    constants = hn_constants()
    return {
        "status": "BLOCKED_DEPENDENCY",
        "summary": {
            "integer_incidence": {
                "status": "EXACT",
                "examples": {
                    "resolved_digit_link": [1, -1, 0],
                    "single_parent_exhaustion_var": [1, -1],
                    "cardinality_constraint": [1],
                },
                "notes": "The incidence matrix entries are exact integers in the repository design.",
            },
            "rational_reciprocal_mass": {
                "status": "EXACT_IF_RECONSTRUCTED",
                "examples": {
                    "residual_mass_summands": "must be traced back to the exact tower divisor structure",
                    "reciprocal_mass_terms": "not yet extracted as a canonical rational formula",
                },
                "notes": "These coefficients are mathematically rational but their exact source is not yet frozen in a canonical repository object.",
            },
            "HN_constants": {
                "status": "EXACT",
                "values": {k: str(v) for k, v in constants.items()},
                "notes": "The HN constants are already documented exactly in docs/CURRENT_FRONTIER.md.",
            },
            "BBMST_coefficients": {
                "status": "BLOCKED_DEPENDENCY",
                "notes": "The exact BBMST weights in the child-pooling rows are still generated through the float builder path.",
            },
            "tower_weights": {
                "status": "BLOCKED_DEPENDENCY",
                "notes": "The tower weights embedded in the pooled child relaxation are not yet available as an exact source object independent of the float builder.",
            },
            "conditional_child_weights": {
                "status": "BLOCKED_DEPENDENCY",
                "notes": "The child-capacity coefficients depend on unresolved deep-3 and tail group weights from the float builder.",
            },
            "Hunter_overlap_terms": {
                "status": "BLOCKED_DEPENDENCY",
                "notes": "Historical Hunter cuts have no exact rational certificate stored alongside the solver output.",
            },
        },
        "blocked_dependencies": [
            "The explicit float-valued weights in src/state2275_child_pooled_master.py are not yet traced back to exact source formulas.",
            "The saved Hunter cut log does not carry exact rational coefficients alongside its generated signatures.",
            "The child-pooling model still uses float arithmetic when creating the sparse phase matrix.",
        ],
    }


def build_exact_model_record() -> Dict[str, object]:
    """Emit a canonical exact source ledger for the phase LP.

    This is intentionally conservative. It records exact families that are already
    available and refuses to invent a proof object from numeric float data.
    """
    summary = exact_family_summary()
    return {
        "schema_version": 1,
        "statement": "CARD9 pooled child-capacity plus Hunter phase relaxation",
        "status": summary["status"],
        "proof_status": "BLOCKED_DEPENDENCY",
        "exactly_known_families": {
            "integer_incidence": summary["summary"]["integer_incidence"],
            "HN_constants": summary["summary"]["HN_constants"],
        },
        "blocked_families": {
            "BBMST_coefficients": summary["summary"]["BBMST_coefficients"],
            "tower_weights": summary["summary"]["tower_weights"],
            "conditional_child_weights": summary["summary"]["conditional_child_weights"],
            "Hunter_overlap_terms": summary["summary"]["Hunter_overlap_terms"],
        },
        "blocked_dependencies": summary["blocked_dependencies"],
        "required_next_step": "Reconstruct each unresolved coefficient family from the exact finite combinatorial source and re-run the dual verification with Fraction arithmetic only.",
    }


def main() -> None:
    record = build_exact_model_record()
    out = ROOT / "artifacts" / "card9_exact" / "RATIONAL_MODEL_SCHEMA.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(f"WROTE {out}")
    print(json.dumps({"status": record["status"], "proof_status": record["proof_status"]}, indent=2))


if __name__ == "__main__":
    main()
