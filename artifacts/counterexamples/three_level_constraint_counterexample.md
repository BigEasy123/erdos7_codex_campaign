# COUNTEREXAMPLE: Three-Level Constraint Issue

## Finding

The child-pooled relaxation model uses THREE separate load constraints (one per depth level $q \in \{0,1,2\}$):

```
For each parent a and each depth q ∈ {0,1,2}:
  e_a ≤ 3w·d[q] + w·(squarefree) + pool[q] + (tail)
```

This creates an issue: **a genuine continuation might satisfy the covering requirement at one depth level but not all three levels simultaneously**.

## Concrete Counterexample

**Genuine continuation:**
- Parent $a$ is covered by:
  - Resolved deep-3 class at depth $q^* = 0$ with weight $w_d = 0.3$
  - Squarefree coverage with weight $w_{\text{sf}} = 0.8$
- Total coverage: $0.3 + 0.8 = 1.1 \geq 1$ ✓ (covering requirement satisfied)

**Attempt to represent in relaxation:**
- Set $e_a = 1$ (parent is exhausted)
- Set $d_0 = 1, d_1 = 0, d_2 = 0$ (resolved deep-3 at depth 0)
- Set $x_{\text{sf}} = 1$ (squarefree selected)
- Set $\text{pool}_q = 0$ (no unresolved pooling)

**Load constraints:**
- At $q = 0$: $e_a \leq 3(0.3) + 0.8 + 0 + 0 = 1.7$ ✓ (satisfied)
- At $q = 1$: $e_a \leq 0 + 0.8 + 0 + 0 = 0.8$ ✗ (VIOLATED)
- At $q = 2$: $e_a \leq 0 + 0.8 + 0 + 0 = 0.8$ ✗ (VIOLATED)

**Conclusion:** The genuine continuation CANNOT be represented in the relaxation because the constraints at $q = 1$ and $q = 2$ are violated.

## Root Cause

The issue is that:
1. **Resolved deep-3 variables** ($d_q$) contribute to the load ONLY at their specific depth level $q$
2. **Squarefree variables** contribute to the load at ALL depth levels
3. There's a **weight imbalance**: resolved deep-3 is weighted by 3 at one level (to compensate for zero at other levels), but squarefree is NOT weighted by 3

This creates a fundamental asymmetry:
- If a parent relies on resolved deep-3 for coverage at depth $q^*$, it still needs coverage at OTHER depths from some other source (squarefree, unresolved pooling, or tail)
- The continuation might provide coverage only at depth $q^*$, leaving other depths uncovered

## Implications

**Option A: Model is broken**
- The relaxation is NOT a valid domination of genuine continuations
- This is a counterexample proving the Safe Relaxation Domination theorem is **FALSE**
- Status: `COUNTEREXAMPLE`

**Option B: "Genuine continuation" definition is incomplete**
- Genuine continuations should be redefined to require coverage at all three depth levels
- This would exclude continuations like the example above
- The model is valid for the restricted definition of continuation
- Status: `PROVED_SYMBOLIC` (but with restricted scope)

**Option C: Model design intent is different**
- Resolved deep-3 classes should not be used directly; all deep-3 coverage should go through unresolved pooling
- The pooling variables are designed to provide coverage at all depths
- Needs investigation of how pooling actually works

## Investigation Needed

1. **Check if resolved deep-3 classes are activated in practice:**
   - Examine solver output (e.g., POOLED_MIN_EXHAUST_LP.json)
   - Do any $d_q$ variables have non-zero values?

2. **Examine the unresolved pooling constraint:**
   - Does it force the pooled variables to provide coverage at all depths?
   - Are pooled variables used as a workaround for the resolved deep-3 limitation?

3. **Clarify the model design:**
   - Was the three-level structure intentionally restrictive?
   - Should resolved deep-3 classes be excluded from the model?

## Current Status

**Theorem status:** `COUNTEREXAMPLE_CANDIDATE` — awaiting clarification of model design intent.

**Next action:** Examine solver output to determine whether resolved deep-3 variables are actually used or remain at 0 in the optimal solution.

---

## Technical Details: Why This Matters

The Safe Relaxation Domination theorem is **critical for Gate-1 closure** because it establishes that:
$$\text{minimum}_{\text{genuine}} \sum_a e_a \geq \text{minimum}_{\text{relaxation}} \sum_a e_a$$

If the relaxation is more restrictive than genuine continuations (smaller feasible set), then the lower bound from the relaxation is **inflated** and does not represent the true minimum exhaustion needed for a genuine bad continuation.

In that case, the bound $\sum_a e_a \geq 8.764$ (from the LP) would be **invalid**, and the CARD9 phase rejection logic would be unfounded.

This would invalidate the entire argument for state-2275 closure.

