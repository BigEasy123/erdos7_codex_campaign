# Lemmas for Safe Relaxation Domination — Proof Development

## Status: ACTIVE — Lemma proofs under development

This document contains detailed proofs of the key lemmas needed to establish the Safe Relaxation Domination theorem.

---

## Lemma 2.1: Heavy-Vector Selection Constraint

**Statement:** For every modulus $m \in \{1, \ldots, 15\}$, the continuation $\mathcal{C}$ selects at most one heavy exponent vector per modulus, so the constraint
$$\sum_{h,v} x_{m,h,v}^* \leq 1$$
is satisfied.

**Proof:** 

By definition of a genuine continuation $\mathcal{C}$, for each modulus $m$, the coverage at $m$ is determined by exactly one of:
1. Selection of a heavy exponent vector $\mathbf{e}_m$ and compatible residue $v_m$
2. Allocation of fractional tail mass (heavy = 0)
3. No coverage at modulus $m$ (heavy = 0, tail = 0, pooled = 0)

In case (1), exactly one $(m, h(\mathbf{e}_m), v_m)$ tuple is active, so $\sum_{h,v} x_{m,h,v}^* = 1$.

In cases (2) and (3), no heavy vector is selected, so $\sum_{h,v} x_{m,h,v}^* = 0$.

Therefore, $\sum_{h,v} x_{m,h,v}^* \in \{0, 1\}$ and the constraint $\sum_{h,v} x_{m,h,v}^* \leq 1$ is satisfied. ∎

---

## Lemma 2.2: Divisor Completion Constraint

**Statement:** If a genuine continuation $\mathcal{C}$ selects a heavy exponent vector $\mathbf{e}_m = (e_p)_{p \in \pi(m)}$ at modulus $m$, then for every prime $p \in \pi(m)$ with $e_p > 1$, the immediate divisor exponent vector $\mathbf{e}'_m$ (with one exponent decremented) must also be selected at $m$ (or its mass is allocated to tail). Therefore, the divisor-completion constraint
$$\sum_{v} x_{m,h(\mathbf{e}_m),v} \leq \sum_{v} x_{m,h(\mathbf{e}'_m),v}$$
is satisfied.

**Proof Strategy (to be expanded):**

The divisor-completion property rests on the BBMST tower structure:

**Key observation:** In the low-four tower geometry (dimensions $D = (2,4,6,10)$), the tower divisor structure is induced by:
- Each modulus $m$ corresponds to a subset of primes $\{3,5,7,11\}$
- Each exponent vector $\mathbf{e}_m$ corresponds to a depth in the tower at that modulus
- The **divisor property** states: if a residue class is covered by the tower at exponent depth $\mathbf{e}_m$, then it must also be "potentially" covered by every divisor exponent depth

**Formal statement (to be proved separately):**

*Divisor Lattice Lemma:* In the low-four residue geometry, the set of residues covered by exponent vector $\mathbf{e}_m$ at modulus $m$ is a subset of the residues covered by the immediate divisor $\mathbf{e}'_m$. Therefore, if a continuation selects $\mathbf{e}_m$ at $m$, the divisor $\mathbf{e}'_m$ must be selected (or its mass allocated to tail).

**Proof sketch:**
1. The residues modulo $m = 3^{e_3} \times 5^{e_5} \times 7^{e_7} \times 11^{e_{11}}$ decompose into a product of residues modulo each prime power.
2. For a fixed modulus $m$ and fixed other prime powers, the residues modulo $3^{e_3}$ map surjectively to residues modulo $3^{e_3-1}$ (by the reduction map $r \mapsto r \bmod 3^{e_3-1}$).
3. The set of shallow residues $\mathcal{R}$ is constructed by filtering against the fixed partition. The covering relations are preserved under this reduction.
4. Therefore, covering a residue at depth $e_3$ requires implicit covering at all divisor depths.

**Current status:** Full proof requires formalization of the tower divisor lattice. Proceed to implementation of Lemma 2.4 (pooling decomposition) while this is refined.

---

## Lemma 2.3: Deep-3 Binary Resolution Constraint

**Statement:** For each resolved deep-3 class $j$ (with weight $w \geq 1/5$), the heavy-vector binary variable $x_{m,h,v}^*$ is decomposed into three binary variables $d_{z,j,q}^* \in \{0,1\}$ for $q \in \{0,1,2\}$ (representing the three possible depth levels). The constraint
$$\sum_{q=0}^{2} d_{z,j,q}^* = x_{m,h,v}^*$$
is satisfied.

**Proof:**

By definition of the continuation $\mathcal{C}$, for each heavy class at a resolved deep-3 modulus (i.e., a 3-power exponent vector $\mathbf{e}_m = (e_3, \ldots)$ with $e_3 \geq 2$ and weight $w \geq 1/5$), the continuation specifies exactly one depth choice $z \in \{0,1,2\}$ to which the 3-power descends.

The mapping (Step 1d) sets:
$$d_{z,j,q}^* = \begin{cases} 1 & \text{if } q = z \\ 0 & \text{otherwise} \end{cases}$$

Therefore, $\sum_{q=0}^{2} d_{z,j,q}^* = 1$. 

Since the continuation selects this heavy class, $x_{m,h,v}^* = 1$. Thus the constraint $\sum_q d_{z,j,q}^* = 1 = x_{m,h,v}^*$ is satisfied. ∎

---

## Lemma 2.4: Pooling Decomposition Constraint

**Statement:** For each unresolved group $g$ (collection of heavy classes with 3-power exponent $\geq 2$ but weight $w < 1/5$), the pooling variables are related to the weighted heavy selections by the constraint:
$$\sum_{q=0}^{2} \text{pool}_{g,q} = 3 \sum_{(m,h,v) \in g} w_m(\mathbf{e}_m) \cdot x_{m,h,v} + \text{pooling\_tail}$$

In particular, the constraint from the model code is:
$$\sum_{q=0}^{2} \text{pool}_{g,q} - 3 \sum_{(m,h,v) \in g} w_m(\mathbf{e}_m) \cdot x_{m,h,v} - 3 \cdot t_g = 0$$
which (rearranged) gives:
$$\sum_{q=0}^{2} \text{pool}_{g,q} = 3 \sum_{(m,h,v) \in g} w_m(\mathbf{e}_m) \cdot x_{m,h,v} + 3 t_g$$

**Proof Outline:**

The pooling constraint encodes a **three-way depth decomposition** of unresolved deep-3 classes.

**Key insight:** An unresolved deep-3 class with weight $w < 1/5$ represents a 3-power exponent vector $\mathbf{e}_m = (e_3, \ldots)$ where $e_3 \geq 2$ and the weight is small enough that the exact depth cannot be pinned down by the LP directly. Instead, the depth is "pooled" across three options $q \in \{0,1,2\}$, representing:
- $q = 0$: depth-0 (3-to-1 reduction, no 3-power refinement)
- $q = 1$: depth-1 (3-to-1-or-2 refinement)
- $q = 2$: depth-2 (arbitrary deep-3 continuation)

**Mapping from continuation to pooling:**

For a genuine continuation $\mathcal{C}$, if a class in group $g$ is selected at modulus $m$, it contributes weight $w_m(\mathbf{e}_m)$ to the load at the $\mathcal{R}$ parent it covers. The continuation also specifies which depth $q \in \{0,1,2\}$ the deep-3 descent takes.

The mapping (Step 1e) assigns:
$$\text{pool}_{g,q}^* = \sum_{(m,h,v) \in g, \text{depth } q \text{ in } \mathcal{C}} w_m(\mathbf{e}_m)$$

plus any unresolved tail $t_g$ at depths $q$.

**Verification of the pooling constraint:**

The constraint states:
$$\sum_{q=0}^{2} \text{pool}_{g,q}^* = 3 \left( \sum_{(m,h,v) \in g} w_m(\mathbf{e}_m) \cdot x_{m,h,v}^* + t_g \right)$$

By the mapping:
$$\text{LHS} = \sum_{q=0}^{2} \sum_{(m,h,v) \in g, \text{depth } q} w_m(\mathbf{e}_m) + \sum_q t_{g,q}^*$$

For each class in $g$ that is selected ($x_{m,h,v}^* = 1$), exactly one depth $q$ is chosen by the continuation, so:
$$\sum_{q=0}^{2} \mathbb{1}[\text{class at depth } q] = 1$$

Therefore:
$$\text{LHS} = \sum_{(m,h,v) \in g : x^* = 1} w_m(\mathbf{e}_m) + \sum_q t_{g,q}^*$$

For classes with $x_{m,h,v}^* = 1$, the right-hand side contributes $w_m(\mathbf{e}_m)$ exactly once (summed over $q$), so:
$$\text{RHS} = 3 \sum_{(m,h,v) \in g : x^* = 1} w_m(\mathbf{e}_m) + 3 t_g$$

**Discrepancy:** There is a factor-of-3 mismatch! 

**Resolution:** The factor of 3 is intentional and relates to the depth-level scaling in the load constraint (Lemma 2.5).

---

## Lemma 2.5: Load (Covering) Constraint

**Statement:** For each shallow parent $a \in \mathcal{R}$ with $e_a(\mathcal{C}) = 1$ (exhausted), the mapped relaxation point satisfies the load constraint
$$e_a^* \leq \sum_{m, h, v \text{ covering } a} w_m(\mathbf{e}_m) \cdot x_{m,h,v}^* + \sum_{\text{resolved deep-3}} 3 w_m(\mathbf{e}_m) \cdot d_{z,j,q}^* + \sum_{\text{unresolved}} \text{pool}_{g,q}^* + \sum_{\text{tail}} t_{m,v}^*$$

**Proof Outline:**

By definition of genuine continuation, parent $a$ with $e_a = 1$ is covered by the deep continuation:
$$\sum_{m=1}^{15} \left( \text{coverage at } m \right) \geq 1$$

The coverage at $m$ is a sum of:
1. **Heavy contributions** (squarefree and even moduli, or first copy of odd modulus): weight $w_m(\mathbf{e}_m)$
2. **Resolved deep-3 contributions** (3-power with weight $\geq 1/5$): a three-way split across depths, total weight $w_m(\mathbf{e}_m)$
3. **Unresolved deep-3 contributions** (3-power with weight $< 1/5$): pooled across depths, scaled by 3
4. **Tail contributions** (fractional remainder): 1 per unit at modulus $m$

**Key:** The pooling constraint (Lemma 2.4) ensures that when the pooled mass is decomposed across the three depth levels, the total load is accounted for correctly.

**Detailed accounting:**

For each modulus $m$ covering parent $a$:
- If heavy at $m$ and squarefree: contribute $w_m(\mathbf{e}_m) \cdot x_{m,h,v}^*$
- If heavy at $m$ and odd (resolved deep-3): contribute $w_m(\mathbf{e}_m) \cdot \sum_q d_{z,j,q}^* = w_m(\mathbf{e}_m)$ (since $\sum_q d_{z,j,q}^* = 1$)
- If unresolved deep-3: This is accounted for via the pooling constraint. The pooled variables $\text{pool}_{g,q}^*$ appear in the load constraint with coefficient 1 (not 3).

The factor of 3 in the pooling constraint (Lemma 2.4) is chosen so that the load constraint (Lemma 2.5) correctly accounts for the three-level decomposition. Specifically:

If an unresolved class with weight $w$ at modulus $m$ contributes to parent $a$, it is allocated across three depths with total mass $w$. The pooling constraint forces:
$$\sum_q \text{pool}_{g,q}^* = 3w$$

But when computing load, each depth choice $q$ contributes $\text{pool}_{g,q}^* / 3$ to the load (on average), so the total load contribution is $\sum_q (\text{pool}_{g,q}^* / 3) = w$.

However, the actual code constraint does not have this factor-of-3 division! Let me re-read the code.

**Code inspection (from state2275_child_pooled_exact.py lines 88-107):**

```python
for aidx, a in enumerate(s.R):
    je = meta['eidx'][aidx]
    for q in range(3):
        d = {je: F(-1)}
        for m in range(1, 16):
            I = s.bits(m)
            v = tuple(a[i] for i in I)
            for h, (_, w) in enumerate(meta['hv'][m]):
                jx = meta['xidx'].get((m, h, v))
                if jx is None:
                    continue
                if (m & 1) and meta['hv'][m][h][0][0] >= 2:  # odd m, 3-exponent >= 2
                    if jx in resolved:
                        d[dz[jx, q]] = d.get(dz[jx, q], 0) + F(3) * F(str(w))
                else:
                    d[jx] = d.get(jx, 0) + F(str(w))
            jt = meta['tidx'].get((m, v))
            if jt is not None and not (m & 1):
                d[jt] = d.get(jt, 0) + F(1)
            if (m, v) in groupkeys:
                d[pool[(m, v), q]] = d.get(pool[(m, v), q], 0) + F(1)
        row(d, 0)
```

The constraint is:
$$-e_a + \sum_{m, q} \left( 3w \cdot d_{z,j,q}^* + w \cdot x_{m,h,v}^* + \text{pool}_{(m,v),q} \right) + t_{m,v} \geq 0$$

Wait, there's a loop over $q \in \{0,1,2\}$ for each parent $a$! So there are actually **3 constraints per parent**, one for each depth level $q$.

**Reinterpretation:**

For each parent $a$ and each depth level $q \in \{0,1,2\}$, there is a constraint:
$$e_a \leq 3 \sum_{\text{resolved deep-3 at } m} w_m \cdot d_{z,j,q} + \sum_{\text{squarefree/even}} w_m \cdot x_{m,h,v} + \sum_{\text{unresolved}} \text{pool}_{(m,v),q} + \sum_{\text{tail}} t_{m,v}$$

This means the parent $a$ can be exhausted **if and only if** for some depth level $q$, the load at level $q$ is at least 1.

In other words, the relaxation is saying:
$$e_a = 1 \implies \exists q \in \{0,1,2\} : \text{load}_q(a) \geq 1$$

This is a **disjunctive constraint** encoded via the three depth levels.

**Continuation verification:**

For the mapped relaxation point:
- If $e_a(\mathcal{C}) = 0$, then $e_a^* = 0$, so the constraint is trivially satisfied.
- If $e_a(\mathcal{C}) = 1$, then parent $a$ is covered by the continuation. The continuation specifies which depths are used to cover $a$. We must show that for **at least one** depth level $q^* \in \{0,1,2\}$ used by the continuation, the load at level $q^*$ is at least 1.

By definition, the continuation achieves:
$$\sum_{m} (\text{coverage at } m \text{ at depth } q^*) \geq 1$$

The mapping places all contributions to the load constraint for depth $q^*$:
- Resolved deep-3: $d_{z,j,q^*}$ is set to 1 if depth $q^*$ is chosen, so it contributes $3w_m$. But wait, the continuation says the coverage is $w_m$, not $3w_m$!

**Critical issue:** There's a factor-of-3 discrepancy between the continuation's coverage ($w_m$) and the relaxation's contribution ($3w_m$ for resolved deep-3).

**Resolution via re-examination:**

The factor of 3 in the load constraint for resolved deep-3 (`d[dz[jx, q]] = d.get(dz[jx, q], 0) + F(3) * F(str(w))`) is exactly offset by the constraint that $\sum_q d_{z,j,q} = 1$ (Lemma 2.3).

Rearranging: if $d_{z,j,0}^* + d_{z,j,1}^* + d_{z,j,2}^* = 1$, then:
$$3w \cdot (d_{z,j,0}^* + d_{z,j,1}^* + d_{z,j,2}^*) = 3w$$

Distributing:
$$3w \cdot d_{z,j,q}^* \text{ for } q \in \{0,1,2\}$$

If exactly one $q = q^*$ has $d_{z,j,q^*}^* = 1$ and the rest are 0, then:
$$3w \cdot d_{z,j,q^*}^* = 3w$$

appears in the load constraint for level $q^*$, not for the other levels.

**But the constraint sums over all $q$ separately!** Let me re-examine the code.

Actually, looking again at the code (line 88): `for q in range(3):` — this creates **three separate load constraints**, one for each $q$. So the constraint for depth level $q$ is:
$$e_a \leq 3 \sum_{\text{resolved deep-3}} w_m \cdot d_{z,j,q} + \sum_{\text{squarefree}} w_m \cdot x_{m,h,v} + \text{pool}_{(m,v),q} + t_{m,v}$$

For the resolved deep-3 case:
- If $d_{z,j,q}^* = 1$ and $d_{z,j,q'}^* = 0$ for $q' \neq q$, then the load at level $q$ includes the full weight $3w_m$, but the load at other levels does not include it.

Wait, that doesn't make sense either. Let me re-read the code very carefully.

```python
d = {je: F(-1)}  # Start with -e_a on LHS
for m in range(1, 16):
    ...
    if (m & 1) and meta['hv'][m][h][0][0] >= 2:  # odd m, 3-exponent >= 2
        if jx in resolved:
            d[dz[jx, q]] = d.get(dz[jx, q], 0) + F(3) * F(str(w))
    else:
        d[jx] = d.get(jx, 0) + F(str(w))
    if (m, v) in groupkeys:
        d[pool[(m, v), q]] = d.get(pool[(m, v), q], 0) + F(1)
row(d, 0)  # Add constraint d >= 0, i.e., RHS - LHS >= 0, i.e., e_a <= RHS
```

So the constraint is:
$$d[\cdot] \geq 0$$
which means:
$$-e_a + \text{(contributions)} \geq 0$$
i.e.,
$$e_a \leq \text{(contributions)}$$

For each depth level $q$, **one constraint is added** with the contributions at level $q$.

So there are 3 constraints:
- Level $q=0$: $e_a \leq 3w \cdot d_{z,j,0} + w \cdot x_{\text{squarefree}} + \text{pool}_{\cdot, 0} + t_{\text{even}}$
- Level $q=1$: $e_a \leq 3w \cdot d_{z,j,1} + w \cdot x_{\text{squarefree}} + \text{pool}_{\cdot, 1} + t_{\text{even}}$
- Level $q=2$: $e_a \leq 3w \cdot d_{z,j,2} + w \cdot x_{\text{squarefree}} + \text{pool}_{\cdot, 2} + t_{\text{even}}$

For the continuation to satisfy all three constraints, it must have:
$$e_a \in \{0, 1\} \text{ and } e_a \leq \text{load at some level}$$

If $e_a = 1$, then at least one of the three constraints must have RHS $\geq 1$.

**Now the verification:**

For parent $a$ with $e_a(\mathcal{C}) = 1$, the continuation covers $a$ at some modulus $m$ with depth levels:
$$\sum_{m} \sum_q c_q(m) = 1$$
where $c_q(m)$ is the contribution at depth level $q$ from modulus $m$.

The mapping assigns:
- For resolved deep-3 at modulus $m$ with depth $q^*$: set $d_{z,j,q^*}^* = 1$, so it contributes $3w_m$ to level $q^*$
- For squarefree at modulus $m$: set $x_{m,h,v}^* = 1$, contributes $w_m$ to all levels
- For unresolved at modulus $m$ with depth $q^*$: set $\text{pool}_{(m,v),q^*}^* = w_m$ (from the pooling constraint), contributes $w_m$ to level $q^*$
- For tail at even modulus $m$: set $t_{m,v}^* = t_m$, contributes $t_m$ to all levels

Let me verify that for at least one level $q^*$, the load is $\geq 1$:

$$\text{load}_{q^*} = 3 w_m \cdot \mathbb{1}[\text{resolved deep-3 at depth } q^*] + \sum_{\text{squarefree}} w_m + \text{pool}_{q^*} + t_{\text{even}}$$

The continuation's coverage is:
$$\text{coverage} = 3 w_m \cdot \mathbb{1}[\text{resolved deep-3}] / 3 + \sum_{\text{squarefree}} w_m + \text{unresolved\_pooled} + t_{\text{even}} \geq 1$$

For resolved deep-3, the contribution is $w_m$, but the relaxation counts it as $3w_m$ **at one depth level** $q^*$. So:
$$\text{load}_{q^*} \geq w_m (\text{resolved at } q^*) + w_m (\text{squarefree}) + w_m (\text{unresolved\_pooled}) + t_m (\text{even})$$

But wait, unresolved pooled is $3w_m$ in the pooling constraint, so $w_m = 3w_m / 3$. And the pool variables are split across the three levels...

I think I need to reconsider the exact structure. Let me focus on what the model is actually doing: it's encoding a three-level decomposition where the resolution of deep-3 tails is deferred to the linear program.

**Simpler approach:**

The three constraints (one per depth level $q$) are a relaxation. A point $(e_a, x, t, d, \text{pool})$ is feasible iff it satisfies all three constraints:
$$e_a \leq \text{load}_q \quad \forall q \in \{0,1,2\}$$

This is equivalent to:
$$e_a \leq \min_q \text{load}_q$$

The LP optimizer will naturally find a feasible solution where each $e_a$ is pinned to the tightest of the three constraints (or 0 if all are negative).

**For our continuation mapping:**

If the continuation covers parent $a$ at depth levels, then we need to ensure that:
$$e_a^* \leq \max_q (\text{load}_q \text{ for the depth levels used})$$

Actually, the key is: **the LP has three constraints per parent, and any feasible point must satisfy all three.** So we need:
$$e_a^* \leq \text{load}_q \quad \forall q$$

If the continuation covers $a$ at depth $q^*$ with coverage $\geq 1$, then we need:
$$\text{load}_{q^*} \geq e_a^* = 1$$

For the other depths $q \neq q^*$, we need:
$$\text{load}_q \geq 1$$
as well, OR $e_a^* = 0$ (but $e_a^* = 1$ by assumption).

**This might be the issue!** The three-level constraint might not be feasible for a continuation that uses only one specific depth level.

Let me check if there's a constraint that forces the load to be uniform across levels for certain variables.

Actually, re-examining the code (line 98-99): the tail variables appear in all three constraints uniformly:
```python
jt = meta['tidx'].get((m, v))
if jt is not None and not (m & 1):
    d[jt] = d.get(jt, 0) + F(1)
```

So for each even modulus (not odd), the tail contributes to all three levels equally.

And squarefree heavy vectors also appear in all three levels.

So the load at level $q$ is:
$$\text{load}_q = \sum_{\text{squarefree}} w_m \cdot x_{m,h,v} + 3 w_m \cdot d_{z,j,q} + \text{pool}_{(m,v),q} + \sum_{\text{even}} t_{m,v}$$

If the continuation covers $a$ using **only squarefree and even-modulus classes** with total weight $\geq 1$, then:
$$\text{load}_q \geq 1 \quad \forall q$$
so all three constraints are satisfied.

If the continuation covers $a$ using **resolved deep-3 at depth $q^*$ with weight $w_m < 1$, plus other squarefree/even classes**, then:
$$\text{load}_{q^*} \geq 3 w_m + (\text{other}) \geq 1 \quad \text{ (possibly)}$$

But:
$$\text{load}_{q \neq q^*} = 0 \cdot d_{z,j,q} + (\text{other}) = (\text{other}) < 1$$

So the constraint at level $q \neq q^*$ would be violated!

**This suggests the continuation mapping needs to be adjusted to ensure all three constraints are satisfied.**

---

## Resolution: Corrected Continuation Mapping and Load Constraints

The issue is that the three-level constraints are genuinely three separate constraints, all of which must be satisfied. The continuation must provide enough coverage at ALL levels, not just one specific level.

**Key insight:** The unresolved pooling variables provide the link. The pooling constraint (Lemma 2.4) relates the pooled mass to the heavy selections, and the pooled mass appears in the load at all three levels.

**Revised statement of Lemma 2.5:**

For each shallow parent $a \in \mathcal{R}$ and each depth level $q \in \{0,1,2\}$, the mapped relaxation point satisfies:
$$e_a^* \leq \text{load}_q^*$$
where
$$\text{load}_q^* = 3 \sum_{\text{resolved deep-3 at } q} w_m \cdot d_{z,j,q}^* + \sum_{\text{squarefree/even}} w_m \cdot x_{m,h,v}^* + \text{pool}_{(m,v),q}^* + \sum_{\text{even tail}} t_{m,v}^*$$

**For this to hold**, the continuation must be such that its total coverage can be redistributed across the three levels to satisfy all constraints.

This is a **major constraint on what counts as a "genuine" continuation**: it must be representable in the three-level decomposition.

**Question:** Can every genuine continuation be so decomposed?

**Answer (to be determined):** This depends on the exact structure of the unresolved classes and how the pooling variables can be used.

---

## Status of Lemma Proofs

| Lemma | Status | Notes |
|-------|--------|-------|
| 2.1 (Heavy-vector selection) | ✓ PROVED | Direct from continuation definition |
| 2.2 (Divisor completion) | ⚠ OUTLINE | Requires tower divisor lattice formalization |
| 2.3 (Deep-3 binary resolution) | ✓ PROVED | Direct from continuation definition |
| 2.4 (Pooling decomposition) | ⚠ IN PROGRESS | Requires clarification of three-level constraint structure |
| 2.5 (Load constraint) | ⚠ CRITICAL ISSUE | Three-level constraint requires coverage at all depths |

---

## Next Steps

1. **Investigate the three-level constraint structure:** Is it possible for an unresolved pooling point to provide non-zero load at all three levels simultaneously?
2. **Clarify the "genuine continuation" definition:** Must continuations be representable in the three-level decomposition?
3. **Prove Lemma 2.4 correctly:** Show that the pooling constraint allows enough flexibility for continuations to be represented.
4. **If three-level constraint is too restrictive:** The model might be a *non-dominating* relaxation, which would be a counterexample.

