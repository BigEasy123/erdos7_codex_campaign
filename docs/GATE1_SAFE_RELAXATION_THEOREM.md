# GATE-1: Safe Relaxation Domination Theorem

## Status

**OPEN** — Theorem statement and proof strategy under development.

This document formalizes the exact mathematical claim that must be proved to establish that the child-pooled relaxation model is a mathematically sound domination of all genuine arbitrary-depth continuations of state 2275.

---

## Formal Statement

**Theorem (Safe Relaxation Domination for State 2275):**

For every genuine arbitrary-depth bad continuation of state 2275, there exists a feasible point in the exact child-pooled relaxation model that dominates the exhaustion profile.

**Precise formulation:**

Let:
- $\mathcal{R}$ = the set of 331 shallow residue classes not fixed by the canonical partition of state 2275
- $\mathcal{C}$ = a genuine arbitrary-depth bad continuation (defined below)
- $e_a(\mathcal{C})$ = the binary exhaustion indicator for parent $a \in \mathcal{R}$ under continuation $\mathcal{C}$
- $\mathcal{P}_{\text{relax}}$ = the exact child-pooled relaxation feasible set (defined below)

Then:
$$
\forall \mathcal{C} \text{ genuine bad continuation},\, \exists \mathbf{e}^* \in \mathcal{P}_{\text{relax}} : \sum_{a \in \mathcal{R}} e^*_a \geq \sum_{a \in \mathcal{R}} e_a(\mathcal{C})
$$

**Equivalently (contrapositive):** If a feasible point in the relaxation cannot exhaust 9 or more parents, then no genuine continuation can exhaust 9 or more parents.

---

## Definitions

### (1) Shallow Residue Classes $\mathcal{R}$

State 2275 is the canonical low-four partial partition with dimensions $D = (2,4,6,10)$.

The fixed partition is:
```
11**  1*1*  *22*  123*  1**1  *3*2  13*3
```

A shallow residue class is a 4-tuple $a = (a_1, a_2, a_3, a_4)$ with $a_i \in \{0, \ldots, D_i-1\}$.

$\mathcal{R}$ is the set of all shallow residues NOT covered by the fixed partition:
$$
\mathcal{R} = \{a \in [0,2) \times [0,4) \times [0,6) \times [0,10) : \text{not covered by FIX}\}
$$

**Fact:** $|\mathcal{R}| = 331$.

### (2) Heavy Exponent Vectors

For each prime modulus $m \in \{1, 2, \ldots, 15\}$, a heavy exponent vector is a tuple $\mathbf{e}_m = (e_p)_{p \in \pi(m)}$ where:
- $\pi(m) = \{p \in \{3, 5, 7, 11\} : p | m\}$ (the prime factors of $m$)
- $e_p \geq 1$ for each $p \in \pi(m)$
- The weight $w_m(\mathbf{e}_m) = \prod_{p \in \pi(m)} p^{1-e_p}$ satisfies $w_m(\mathbf{e}_m) \geq \text{cut} = \frac{1}{50}$

The set of valid heavy exponent vectors for modulus $m$ is denoted $\mathcal{H}_m$.

### (3) Genuine Arbitrary-Depth Continuation

A **genuine arbitrary-depth bad continuation** $\mathcal{C}$ is defined by:

**(Shallow layer):**
- An indicator $e_a \in \{0,1\}$ for each shallow parent $a \in \mathcal{R}$, specifying whether $a$ is exhausted.

**(Deep layer for each exhausted parent $a$):**
- For each modulus $m \in \{1, \ldots, 15\}$ (even or odd):
  - A choice of coverage at $m$:
    - Either: select a heavy exponent vector $\mathbf{e}_m \in \mathcal{H}_m$ and a residue class $v_m \in \text{valid}(m)$ **such that** $\text{restrict}(a, \pi(m)) = v_m$ ✓ (covering-compatible)
    - Or: allocate a fractional tail mass $t_m \in [0, \text{tail}(m)]$ (unresolved remainder)
    - Or: neither (not covering $m$)

**(Deep-3 resolution):**
- For each modulus $m$ where $\pi(m) = \{3\}$ and the heavy selection would have $3$-exponent $e_3 \geq 2$ (unresolved):
  - Either: resolve the deep-3 descent to a specific residue class $z \in \{0,1,2\}$ **at depth** $e_3 - 1$
  - Or: leave the deep-3 continuation unresolved and allocate to a pooled group

**(Tail coverage):**
- The fractional tail mass for each modulus $m$ must not exceed $\text{tail}(m)$ (the residual budget after heavy vectors).

**(Covering constraint):**
- For each parent $a \in \mathcal{R}$ with $e_a = 1$ (exhausted):
  - The sum of all coverage (heavy weights, tail, deep-3 resolved, unresolved pooled mass) must satisfy:
  $$
  \sum_{m=1}^{15} \left( \sum_{\text{heavy}} w_m(\mathbf{e}_m) + t_m + \text{pooled}_m \right) \geq 1
  $$
  - This is the **covering requirement**: the exhausted parent must be covered by the deep continuation.

### (4) Child-Pooled Relaxation Model $\mathcal{P}_{\text{relax}}$

The relaxation is a linear feasible set defined by exact rational inequalities.

**Variables:**
1. **Exhaustion variables:** $e_a \in \{0,1\}$ for each $a \in \mathcal{R}$.
2. **Heavy-vector binary variables:** $x_{m,h,v} \in \{0,1\}$ for each modulus $m$, heavy vector index $h$, and valid residue $v$ at $m$ that appears in $\mathcal{R}$.
3. **Tail variables:** $t_{m,v} \in [0, \infty)$ for each modulus $m$ and residue $v$, representing fractional tail mass.
4. **Deep-3 resolution variables (resolved class):** $d_{z,j,q} \in \{0,1\}$ for selected deep-3 classes $j$ and depth choices $q \in \{0,1,2\}$ (only for "resolved" classes with weight $w \geq 0.2 = \frac{1}{5}$).
5. **Pooling variables (unresolved class):** $\text{pool}_{g,q} \in [0, \infty)$ for each unresolved deep-3 group $g$ and depth choice $q \in \{0,1,2\}$.

**Constraints (exact rational form):**

**C1: Heavy-vector selection (at most one per modulus, exactly one for future squarefree):**
$$
\sum_{h,v} x_{m,h,v} \leq 1 \quad \forall m
$$
(with equality for squarefree bases in future moduli $m \in \{12,13,14,15\}$)

**C2: Divisor completion (if heavy vector at exponent $(e_1, \ldots, e_k)$ is selected, then immediate divisor must be selected):**
For each $m$ and each heavy vector $\mathbf{e}_m = (e_p)_p$ with $\min_p e_p > 1$:
$$
\sum_{v} x_{m,h(\mathbf{e}_m),v} \leq \sum_{v} x_{m,h(\mathbf{e}'_m),v}
$$
where $\mathbf{e}'_m$ is the immediate divisor (one exponent decremented).

**C3: Deep-3 binary resolution (for resolved heavy classes):**

For each selected heavy class (resolved deep-3 at weight $w \geq 1/5$), decompose its weight into 3 depth choices:
$$
\sum_{q=0}^{2} d_{z,j,q} = x_{m,h,v} \quad \text{(for resolved class at depth split)}
$$

More precisely: if the heavy vector $\mathbf{e}_m$ has $3$-exponent $e_3 \geq 2$ and weight $w \geq 1/5$, then allocate its contribution across the three depth-level denominators.

**C4: Pooling constraint (for unresolved deep-3 classes):**

For each unresolved group $g$ (collection of heavy classes with $3$-exponent $\geq 2$ but weight $< 1/5$):
$$
\sum_{h \in g} w_m(\mathbf{e}_m) \cdot x_{m,h,v} = \sum_{q=0}^{2} \text{pool}_{g,q} - 3 \sum_{q} \text{pool}_{g,q} + \text{pooling\_tail}_g
$$

(Exact interpretation: the pooled mass equals the weighted sum of heavy selections in the group, minus the depth-slicing penalty, plus tail.)

**C5: Load (coverage) constraint:**

For each shallow parent $a \in \mathcal{R}$:
$$
e_a \leq \sum_{m, h, v: \text{covers } a} w_m(\mathbf{e}_m) \cdot x_{m,h,v} + \sum_{m, v: \text{covers } a} t_{m,v} + \sum_{g \text{ covers } a, q} \text{pool}_{g,q} + \text{unresolved\_tail}_a
$$

**C6: Tail budget:**
$$
\sum_{v} t_{m,v} \leq \text{tail}(m) = \max(0, f(m) - \sum_{h} w_m(\mathbf{e}_m)) \quad \forall m
$$

where $f(m) = G(m) - 1$ if $m$ is fixed-squarefree, else $f(m) = G(m)$, and $G(m) = \prod_{p|m} \frac{p}{p-1}$.

**C7: Total exhaustion bound (numerical safety):**
$$
\sum_{a} e_a \leq 330
$$

(Ensures the model remains LP-feasible.)

---

## Proof Strategy

The proof proceeds in stages:

### **Stage 1: Define Continuation Mapping**

For each genuine bad continuation $\mathcal{C}$, construct a feasible point $(e_a^*, x^*, t^*, d^*, \text{pool}^*) \in \mathcal{P}_{\text{relax}}$ as follows:

**Step 1a: Exhaustion variables**
$$
e_a^* := e_a(\mathcal{C}) \quad \forall a \in \mathcal{R}
$$

**Step 1b: Heavy-vector selection**

For each modulus $m$, if the continuation $\mathcal{C}$ selects a heavy exponent vector $\mathbf{e}_m$ and residue $v_m$:
$$
x_{m,h,v}^* := \begin{cases} 1 & \text{if } (m,h,v) = (m, h(\mathbf{e}_m), v_m) \\ 0 & \text{otherwise} \end{cases}
$$

**Step 1c: Tail variables**

For each modulus $m$, if the continuation $\mathcal{C}$ allocates tail mass $t_m$:
$$
t_{m,v}^* := t_m \quad \text{for the residue } v \text{ matching } \mathcal{C}
$$

**Step 1d: Deep-3 resolution (resolved classes)**

For each resolved deep-3 class $(j, z)$ with depth choice $z$ in $\mathcal{C}$:
$$
d_{z,j,q}^* := \begin{cases} 1 & \text{if } q = z \\ 0 & \text{otherwise} \end{cases}
$$

**Step 1e: Pooling variables (unresolved classes)**

For each unresolved group $g$ and depth choice $q$ in $\mathcal{C}$:
$$
\text{pool}_{g,q}^* := \text{(pooled mass allocated to depth } q \text{ in } \mathcal{C})
$$

### **Stage 2: Verify Feasibility**

**Lemma 2.1 (Constraint C1 — Heavy-vector selection):**
The continuation $\mathcal{C}$ selects at most one heavy exponent vector per modulus by definition. Therefore $\sum_{h,v} x_{m,h,v}^* \leq 1$.

**Lemma 2.2 (Constraint C2 — Divisor completion):**
If $\mathcal{C}$ includes a heavy vector at exponent $\mathbf{e}_m$, then by the covering requirement and tower structure, the immediate divisor must also be present (or the weight is allocated to tail). This holds because:
- The exponent-vector lattice has a covering property: deeper exponents cannot be supported without shallower ones.
- The proof uses the BBMST tower-divisor structure.

*Status: Requires formal proof using exponent-lattice structure.*

**Lemma 2.3 (Constraint C3 — Deep-3 binary resolution):**
For each resolved deep-3 class, exactly one depth choice is active in $\mathcal{C}$ (by the continuation definition). The decomposition $(d^*_{z,j,0}, d^*_{z,j,1}, d^*_{z,j,2})$ has exactly one 1 and two 0s, satisfying $\sum_q d_{z,j,q}^* = 1 = x_{m,h,v}^*$.

**Lemma 2.4 (Constraint C4 — Pooling):**
For each unresolved group $g$, the pooled mass is the sum of weighted heavy selections that map to that group, adjusted for depth choices. The continuation allocates this mass consistently:
$$
\sum_{q} \text{pool}_{g,q}^* = \sum_{(m,h,v) \in g, \text{active}} w_m(\mathbf{e}_m)
$$

*Status: Requires proof that the three-depth decomposition respects the unresolved-class weight distribution.*

**Lemma 2.5 (Constraint C5 — Load/covering):**
By definition of genuine bad continuation, each exhausted parent $a$ with $e_a(\mathcal{C}) = 1$ is covered by the deep continuation:
$$
\sum_{m, \text{coverage at } m} (\text{weight or tail}) \geq 1
$$

Mapping to the relaxation:
$$
e_a^* \leq \sum_{\text{heavy at } m \text{ covering } a} w_m \cdot x_{m,h,v}^* + \sum_{\text{tail at } m} t_{m,v}^* + \sum_{\text{pooled at } m} \text{pool}_{g,q}^*
$$

*Status: Requires matching the continuation's coverage allocation to the relaxation's load constraint.*

**Lemma 2.6 (Constraint C6 — Tail budget):**
The continuation respects the tail budget by definition. The tail variables in the mapped feasible point are bounded by $\text{tail}(m)$.

---

## Scope and Edge Cases

### **Repeated Powers: 3², 5², 7², 11²**

**Claim:** For any continuation with repeated powers of primes, the divisor-completion and deep-3 resolution constraints ensure that the mapped relaxation point satisfies all inequalities.

**Evidence needed:** Audit each exponent pattern:
- $3^2$ with unresolved tail: handled by deep-3 pooling (Lemma 2.4)
- $5^2, 7^2, 11^2$ (no deep unresolution): handled by divisor completion (Lemma 2.2)
- Mixed repeated powers (e.g., $3^2 \times 5^2$): combination of deep-3 resolution and heavy-vector constraints

**Status:** Requires case-by-case verification.

### **Unresolved Deep-3 Tails**

**Definition:** An unresolved deep-3 tail occurs when a heavy $3$-exponent vector has $e_3 \geq 2$ but weight $w < 1/5$ (the pooling threshold), so the depth-to-divisor mapping is deferred.

**Constraint:** The pooling variable $\text{pool}_{g,q}$ represents the fractional mass allocated to depth $q$ in group $g$. The load constraint (C5) must account for this fractional allocation.

**Proof approach:** Show that for every unresolved group $g$, the three-way decomposition into $\text{pool}_{g,q}$ for $q \in \{0,1,2\}$ exactly represents the continuation's coverage contribution.

**Status:** Requires proof of the pooling decomposition lemma (Lemma 2.4).

### **Divisor Closure**

**Definition:** The divisor-closure property requires that if a heavy exponent vector is selected, all immediate divisors in the exponent lattice must also be selected (or their mass is allocated to tail).

**Constraint:** Enforced by C2.

**Proof:** The BBMST tower structure guarantees that any covering of a residue class at exponent $\mathbf{e}_m$ can be backed by recursive covering at divisor exponents. A proof requires:
1. Formal statement of tower divisor structure.
2. Inductive argument over exponent depth.

**Status:** Requires formal lemma on tower structure.

---

## Hypotheses

1. **State 2275 fixed partition:** The canonical low-four partition is:
   ```
   11**  1*1*  *22*  123*  1**1  *3*2  13*3
   ```
   The set $\mathcal{R}$ is correctly identified as 331 uncovered residues.

2. **Heavy-vector weight computation:** For exponent vector $\mathbf{e}_m = (e_p)_p$ at modulus $m$:
   $$
   w_m(\mathbf{e}_m) = \prod_{p \in \pi(m)} p^{1-e_p} \quad (\text{exact rational})
   $$

3. **Tail budget:** For modulus $m$:
   $$
   \text{tail}(m) = \max\left(0, \prod_{p \in \pi(m)} \frac{p}{p-1} - \epsilon(m) - \sum_{h \in \mathcal{H}_m} w_m(\mathbf{e}_m) \right)
   $$
   where $\epsilon(m) = 1$ if $m$ is fixed-squarefree, else $0$ (exact rational).

4. **Covering-capability:** A shallow parent $a \in \mathcal{R}$ is **covering-capable** iff there exists at least one deep class (heavy, tail, or pooled) that matches the residue restrictions at each modulus.

5. **Arbitrary-depth class existence:** For each modulus $m$, the set $\mathcal{H}_m$ of heavy exponent vectors and tail variables provide continuous coverage of the exponent space.

---

## Dependent Theorems

This theorem depends on:

1. **Tower divisor structure** — A formal lemma on BBMST tower geometry showing that divisor completion is necessary for any consistent covering.
2. **Deep-3 pooling validity** — A lemma showing that the three-way depth decomposition in pooling variables is sufficient to represent all unresolved deep-3 continuations.
3. **Tail budget exactness** — Verification that $\text{tail}(m)$ is computed exactly (not numerically) from the tower structure.

---

## Verifier Command

To independently verify this theorem (once proved):

```bash
python3 src/verify_safe_relaxation_domination.py \
  --theorem docs/GATE1_SAFE_RELAXATION_THEOREM.md \
  --model src/state2275_child_pooled_exact.py \
  --continuation-family docs/GATE1_CONTINUATION_FAMILY_ENUMERATION.md \
  --exact-rational \
  --output artifacts/verification/safe_relaxation_verification.json
```

**Verification strategy:**
1. Load the exact rational model from `state2275_child_pooled_exact.py`.
2. For a random sample of 1000 genuine continuations (generated by exhaustive enumeration):
   a. Map each continuation to a relaxation feasible point via Stage 1 mapping.
   b. Check all constraints C1–C7 are satisfied (exact rational arithmetic).
3. Report:
   - Number of continuations verified
   - Constraint satisfaction statistics
   - Any violations found (with counterexample)

**Status:** Verifier code does not yet exist. Must be written as part of proof validation.

---

## Counterexample Hunt

**Objective:** For each constraint and each stage of the proof, attempt to construct a genuine continuation that would violate the relaxation.

### **Constraint C1 violations:**
Can a continuation select multiple heavy vectors at the same modulus? **No** — by definition, each modulus has a unique coverage layer.

### **Constraint C2 (divisor completion) violations:**
Can a continuation select a heavy vector at exponent $(e_1, \ldots, e_k)$ without selecting a divisor? **Needs investigation.**
- *Candidate counterexample:* A deep-3 class with heavy $3^3$ but no $3^2$?
- *Status:* Requires exponent-lattice audit.

### **Constraint C3 violations:**
Can a resolved deep-3 class have multiple active depth choices? **No** — each continuation specifies a unique depth $z \in \{0,1,2\}$.

### **Constraint C5 (covering) violations:**
Can an exhausted parent fail to satisfy the load constraint in the mapped relaxation point? **Critical case.**
- *Candidate counterexample:* An unresolved deep-3 class with weight near the 1/5 threshold?
- *Status:* Requires detailed audit of pooling decomposition.

---

## Current Status

**Stage:** Formal statement DRAFT (this document).

**Completed:**
- [ ] Formal definitions of genuine continuation, relaxation, domination
- [ ] Proof strategy outline

**Remaining:**
- [ ] Lemma 2.2 proof (divisor completion)
- [ ] Lemma 2.4 proof (pooling decomposition)
- [ ] Lemma 2.5 proof (load constraint matching)
- [ ] Repeated-power audit
- [ ] Counterexample hunt (systematic)
- [ ] Verifier code
- [ ] Status label assignment

---

## Next Step

**Action:** Prove Lemma 2.2 (divisor completion). This is the foundational constraint that validates that the heavy-vector selection in the relaxation is mathematically consistent with the continuation structure.

Once Lemma 2.2 is proved, proceed to Lemma 2.4 (pooling decomposition), which is the most complex and novel step.

**If any counterexample is found:** Document it to `artifacts/counterexamples/safe_relaxation_*.json` and revert to `COUNTEREXAMPLE` status.

---

## SHA256 Hash (for audit trail)

*To be computed after final proof is completed.*

---

## Audit Trail

- **2026-08-25:** Initial formal statement drafted. Definitions extracted from `state2275_child_pooled_exact.py`, `state2275_tower_heavy_bbmst_v3.py`, `state2275_hn_milp.py`.
- **Status:** OPEN, proof obligations identified.
