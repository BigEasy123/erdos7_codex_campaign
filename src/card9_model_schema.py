#!/usr/bin/env python3
"""Emit a canonical, source-derived description of the CARD9 phase model."""
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import state2275_child_pooled_master as pooled
import state2275_hn_milp as state


def rational(value: float | int) -> str:
    return str(Fraction(str(value)))


def main() -> None:
    _, integrality, bounds, constraints, meta = pooled.build(.02, .2, True)
    row_count = constraints.A.shape[0]
    base_rows = row_count - meta["child_rows"] - meta["hunter_rows"]
    variables = []
    for index, name in enumerate(meta["names"]):
        variables.append({
            "index": index,
            "name": repr(name),
            "lower": rational(bounds.lb[index]),
            "upper": None if meta["names"][index] and bounds.ub[index] == float("inf") else rational(bounds.ub[index]),
            "integer": bool(integrality[index]),
        })
    schema = {
        "schema_version": 1,
        "statement": "CARD9 pooled child-capacity plus Hunter phase relaxation",
        "status": "NUMERICAL_MODEL_DESCRIPTION",
        "source_parameters": {
            "cut": rational(.02),
            "digit_cut": rational(.2),
            "shallow_parent_count": len(state.R),
            "shallow_parent_coordinates": "state2275_hn_milp.R",
            "exact_cardinality": {"expression": "sum_a e_a = 9", "lower": 9, "upper": 9},
        },
        "semantics": {
            "e": "binary exhaustion indicator for one of the 331 residual shallow parents",
            "x": "binary heavy class selection",
            "dz": "binary next-3 digit allocation for resolved deep-3 heavy classes",
            "pool": "continuous pooled child capacity for unresolved deep-3/tail groups",
            "q": "not present in this phase model; future squarefree choices are represented by pooled child constraints",
            "tail": "continuous residual support mass from the pooled builder",
            "y": "continuous Hunter/HN dual variables from the pooled builder",
        },
        "variable_families": {
            "e": {"count": len(meta["eidx"]), "indices": sorted(meta["eidx"].values()), "bounds": ["0", "1"], "integer": True},
            "x": {"count": len(meta["xidx"]), "indices": sorted(meta["xidx"].values()), "bounds": ["0", "1"], "integer": True},
            "tail": {"count": len(meta["tidx"]), "indices": sorted(meta["tidx"].values()), "integer": False},
            "dz": {"count": len(meta["dz"]), "indices": sorted(meta["dz"].values()), "bounds": ["0", "1"], "integer": True},
            "pool": {"count": len(meta["pool"]), "indices": sorted(meta["pool"].values()), "lower": "0", "upper": "+infinity", "integer": False},
            "other_continuous": {"count": len(meta["names"]) - len(meta["eidx"]) - len(meta["xidx"]) - len(meta["tidx"]) - len(meta["dz"]) - len(meta["pool"]), "note": "base builder variables not reclassified by the phase wrapper"},
        },
        "row_families": [
            {"id": "base_builder", "rows": base_rows, "meaning": "state2275_tower_heavy_bbmst_v3 base legality, support, divisor, and allocation constraints", "coefficients": "generated deterministically by source builder", "rhs": "generated deterministically by source builder", "exact_representation": "Fraction(str(float coefficient)) is only a serialization of current numeric source; no exact certificate", "validity": "relaxation-global"},
            {"id": "resolved_digit_link", "rows": len(meta["resolved"]), "meaning": "resolved deep-3 heavy mass equals the sum of its three child digit variables", "coefficients": "dz[j,q] - x[j] = 0", "rhs": "0", "exact_representation": "integer", "validity": "relaxation-global"},
            {"id": "pooled_child_capacity", "rows": len(meta["pool"]), "meaning": "pooled child capacity is at most three times unresolved parent/tail mass in each shallow cylinder", "coefficients": "sum_q pool[g,q] - 3 sum(w*x) - 3 tail <= 0", "rhs": "0", "exact_representation": "weights are source-generated rationalized floats", "validity": "relaxation-global"},
            {"id": "child_exhaustion", "rows": meta["child_rows"], "meaning": "each exhausted shallow parent requires capacity for all three next digits", "coefficients": "-e_a + incident resolved/heavy/tail/pool capacity >= 0", "rhs": "0", "exact_representation": "weights are source-generated rationalized floats", "validity": "relaxation-global under pooled relaxation"},
            {"id": "hunter_cuts", "rows": meta["hunter_rows"], "meaning": "historical Hunter cuts loaded from HUNTER_V2_CUTLOG", "coefficients": "cut_from_sig(ctx, signature)", "rhs": "signature-dependent", "exact_representation": "not retained as rational certificates", "validity": "global only if independently re-derived from the Hunter theorem"},
        ],
        "phase_objective": {"expression": "minimize t", "t_lower": "0", "rejection_condition": "optimal t > 0", "certificate_type": "exact dual lower bound, not Farkas infeasibility"},
        "symmetry": {"count": 42, "actions": "all permutations of residues 3,4,5 and cyclic shifts of residues 3,4,5,6,7,8,9", "verification": "agents/A_card9/verify_repo_relative.py plus replay check", "exact_status": "mapping semantics checked; cut certificates not yet exact"},
        "certificate_gap": "The current source constructs coefficients through Python floats and the saved phase artifacts retain no dual multipliers. An exact phase certificate must therefore first freeze a rational source model and a dual lower-bound witness.",
        "variables": variables,
    }
    output = ROOT / "artifacts" / "card9_exact" / "CARD9_MODEL_SCHEMA.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(schema, indent=2), encoding="utf-8")
    print(f"WROTE {output}")
    print(f"MODEL_VARS {len(variables)} MODEL_ROWS {row_count}")


if __name__ == "__main__":
    main()
