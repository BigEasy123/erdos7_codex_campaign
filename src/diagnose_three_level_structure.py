#!/usr/bin/env python3
"""
Investigate the three-level constraint structure in the child-pooled model.

Test whether resolved deep-3 classes can be used in a genuine continuation
without violating the three-level load constraints.
"""

import sys
import json
from pathlib import Path
from fractions import Fraction as F

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))

import state2275_child_pooled_exact as cpe
import state2275_hn_milp as s
import state2275_tower_heavy_bbmst_v3 as base

def analyze_model_structure():
    """Analyze the structure of load constraints."""
    exact = cpe.build_exact()
    if exact is None:
        print("ERROR: Could not build exact model")
        return
    
    nvars = exact['nvars']
    nrows = exact['nrows']
    rows = exact['rows']
    lower_bounds = exact['lower_bounds']
    upper_bounds = exact['upper_bounds']
    
    print(f"Model size: {nvars} variables, {nrows} constraints")
    print()
    
    # Find load constraints (those mentioning e_a variables)
    resolved = exact['meta']['resolved']
    pool = exact['meta']['pool']
    dz = exact['meta']['dz']
    
    # Map from variable index to variable name for debugging
    names = exact['names']
    
    # Find the e_a (exhaustion) variable indices
    e_indices = {}
    for j, name in enumerate(names):
        if name[0] == 'e':
            aidx = name[1]  # This is the parent index
            e_indices[aidx] = j
    
    print(f"Found {len(e_indices)} exhaustion variables (one per shallow parent)")
    print()
    
    # Find load constraints (those with e_a variables on LHS)
    load_constraints = []
    for row_idx, d in enumerate(rows):
        for j in d:
            if j in e_indices.values():
                load_constraints.append((row_idx, d, lower_bounds[row_idx], upper_bounds[row_idx]))
                break
    
    print(f"Found {len(load_constraints)} constraints involving e_a variables")
    print(f"Expected ~{len(e_indices)} * 3 = {len(e_indices) * 3} (one per parent per depth level)")
    print()
    
    # Analyze a specific example: first exhaustion variable
    if load_constraints:
        print("=== Example Load Constraint Analysis ===")
        print()
        
        # Group constraints by which e_a they involve
        e_to_constraints = {}
        for row_idx, d, lb, ub in load_constraints:
            for j in d:
                if j in e_indices.values():
                    aidx = [k for k, v in e_indices.items() if v == j][0]
                    if aidx not in e_to_constraints:
                        e_to_constraints[aidx] = []
                    e_to_constraints[aidx].append((row_idx, d, lb, ub))
        
        # Find first parent with constraints
        first_aidx = min(e_to_constraints.keys())
        constraints_for_first = e_to_constraints[first_aidx]
        
        print(f"Parent index: {first_aidx}")
        print(f"Number of load constraints for this parent: {len(constraints_for_first)}")
        print()
        
        for i, (row_idx, d, lb, ub) in enumerate(constraints_for_first):
            print(f"Constraint {i}: -e_{first_aidx} + ... >= {lb}")
            
            # Count variables by type
            resolved_count = sum(1 for j in d if j in dz.values())
            squarefree_count = sum(1 for j in d if 'x' in (names[j] if j < len(names) else ('?',))[0:1])
            pool_count = sum(1 for j in d if j in pool.values())
            tail_count = sum(1 for j in d if 'tail' in (names[j] if j < len(names) else ('?',))[0:1])
            
            print(f"  Variables in constraint: {len(d) - 1} (excluding e_a)")
            print(f"    Resolved deep-3 (dz): {resolved_count}")
            print(f"    Pool: {pool_count}")
            print()
    
    # Check: do all three constraints for a parent have the same RHS?
    print("=== Three-Level Constraint Homogeneity ===")
    print()
    for aidx in sorted(list(e_to_constraints.keys())[:5]):
        constraints_list = e_to_constraints[aidx]
        rhss = [ub for _, _, _, ub in constraints_list]
        is_homogeneous = len(set(rhss)) == 1
        print(f"Parent {aidx}: {len(constraints_list)} constraints, RHS values: {rhss}, homogeneous: {is_homogeneous}")
    
    return exact, e_to_constraints

if __name__ == '__main__':
    exact_model, e_constraints = analyze_model_structure()
    print("\n=== DIAGNOSIS ===")
    print()
    print("If the three-level constraints are NOT homogeneous (different RHS),")
    print("then the model indeed requires coverage at all three depth levels,")
    print("which could violate domination of genuine continuations.")
    print()
    print("If they ARE homogeneous, then the model is actually using some other mechanism.")
