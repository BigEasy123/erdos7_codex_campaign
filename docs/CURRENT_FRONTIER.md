# Current frontier — 2026-08-24

## Problem target

Attempt to prove Erdős Problem #7 / nonexistence of odd distinct covering systems using a least-counterexample reduction, exact low-prime residue geometry, Hough–Nielsen (HN) and BBMST-type analytic termination.

This file is a **checkpoint, not a theorem paper**.

## Focal canonical state

State 2275 is the unique worst low-four canonical tower-capacity state among 7,637 canonical low-four partials:

```text
11**  1*1*  *22*  123*  1**1  *3*2  13*3
```

on the shallow box `2 x 4 x 6 x 10`, with `|R| = 331` residual shallow parents.

Exact arbitrary-depth low-four tower capacity is

```text
D(R) = 145247/480 = 302.597916...
1 - D(R)/331 = 13633/158880 > 0.
```

Thus low-four towers alone cannot complete the cover. This does **not** by itself control concentration statistics.

## Exact local certificates already available

1. Stage-18 depth-one surplus: all 12 divisor-closed surplus downsets have exact rational Farkas contradictions.
2. K2 depth-one: 228 cases have exact rational Farkas certificates and optimizer-free replay.
3. Depth-two common-U exact-three family: all 71 target orbits × 4 exact-three cores = **284/284** have exact rational Farkas certificates.
   - weakest exact/numerical displayed contradiction magnitude from the package is about `0.451772506962` on the negative side;
   - merged certificate SHA256 was recorded during generation as `2473c6a50c3dd802ebe19a0c5ba1fdf7498d2db5a116c80082d19aaa42c11c4f`.
4. Stage23 one-layer orbit audit: 140 symmetry orbits / 7,840 core checks pass; this is one-layer only, not arbitrary-depth radicalization.

See `artifacts/exact/` and the replay scripts in `src/`.

## HN constants currently used

```text
alpha = 51603567726348558328760981369659084133279683367
        /4373107200000000000000000000000000000000000000000

beta  = 14493601981951/13781250000000000

R_HN  = 1985876874482391730913463316715795569734245382761
        /4115865600000000000000000000000000000000000000000
```

The Stage-18 exact replay reconstructs these coefficients with rational arithmetic.

## The actual open state-2275 bridge

The remaining local problem is **correlated survivor dispersion**, not raw exponent-depth coverage.

Existing Hunter/CRT work has accumulated about 1.5k globally valid forest cuts. A next-3-adic child-capacity relaxation was then introduced to preserve global digit coupling.

A partially resolved child/Hunter LP produced the numerical lower bound

```text
min sum_a e_a = 8.76416923252369...
```

so a genuine integer BBMST-bad obstruction would need at least 9 exhausted shallow parents. This bound is currently **NUMERICAL_EVIDENCE** until its LP dual is rationalized and replayed.

The problem was projected to the exact-cardinality-9 binary master over the 331 parent indicators `e_a`:

```text
sum_a e_a = 9.
```

For each proposed 9-set, all tower/residue variables are put into a continuous phase-I LP. Positive phase optimum rejects the set; the LP dual yields a Benders inequality. Symmetry images and exact nogoods are added to the master.

Current checkpoint facts from the latest pass:

- many dozens of exact 9-parent masters have been produced and phase-rejected;
- smallest observed phase-I violations were about `0.0329460` and `0.0330494`, still positive;
- no phase-feasible 9-set has yet appeared;
- the 9-layer is **not yet proved empty**;
- near-extremal rejected sets concentrate strongly in the `a0=0, a1=2` slab.

Representative near-extremal rejected packet:

```text
E = {10,27,33,34,36,48,55,90,138}
phi(E) ≈ 0.03294603958899706 > 0.
```

Current CARD9 state is under `artifacts/current_state/`.

## Structural packet facts likely relevant

For normalized three-terminal cofactor order types there are 90 types. Exactly seven have all three pair arms nonempty (types 84–90). Their radical pattern is, up to permutation,

```text
(7*11, 5*11, 5*7)
```

with divisor closure mask `0x7f`. Type 84 is squarefree and the remaining six differ by repeated powers on the arms.

Known structural lemmas/checkpoints include:

- terminal pair compression and blocker residue;
- exact p-frame hub and blocker rail;
- p=3 chain/fork exact-three downsets;
- support-poor exact p-frame is a chain;
- tight p→q pivot can only backtrack q→p;
- tight backtrack forces a two-prime exponent rectangle;
- all nontrivial moduli on two odd primes have reciprocal mass ≤ 7/8, so outside support is forced;
- every surplus p=3 terminal lies in a compatible transversal triangle.

These derived lemmas still need independent proof-paper audit before final QED.

## Analytic facts / failures

Naive HN first-moment averaging fails: the known distortion/sensitivity product is > 1. Independent geometric inflation of all prime-power towers destroys the HN margin and is not valid as the missing bridge.

The correlated target should force every bad continuation into one of two outcomes:

1. BBMST-good survivor dispersion; or
2. an HN-good packet after preserving actual residue / child correlations.

## Immediate decision tree

1. Close CARD9, or obtain a genuine phase-feasible 9-packet.
2. If CARD9 closes, exactify the lower-bound/Benders layer and move to CARD10 only if the analytic bad gate still allows it.
3. If a 9-packet survives phase LP, restore the necessary discrete residue choices on that tiny packet and attack with common-U + triangle/blocker + HN.
4. Once state 2275 is closed for arbitrary depth, prove a legitimate lift/extremality theorem covering the other 7,636 canonical partials.
5. Audit the 13–73 and >73 HN/BBMST interfaces, especially repeated powers.
6. Assemble and independently referee the full least-counterexample proof.
