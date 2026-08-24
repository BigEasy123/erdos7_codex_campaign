# Track C — common-U / triangle / blocker packet attack

## Mission

Develop a direct finite/structural contradiction for the small packet geometry that survives longest in state 2275, using the already exact common-U depth-two theorem plus transversal-triangle, blocker, and pivot structure.

Do **not** assume the depth-two theorem automatically radicalizes arbitrary depth.

## Exact assets

- `artifacts/exact/FULLCOVER_71x4_FARKAS_EXACT.json`
- `artifacts/exact/FULLCOVER_71x4_FARKAS_EXACT_REPLAY.txt`
- `artifacts/exact/FULLCOVER_71x4_FARKAS_EXACT_SUMMARY.txt`
- `src/depth2_fullcover.py`
- `src/state2275_depth2_hn.py`
- `src/classify_triangle_all_order_types.py`
- `artifacts/exact/STATE23_ONE_LAYER_EXACT_ORBITS.json` if present under exact assets (filename may be `STAGE23_ONE_LAYER_EXACT_ORBITS.json`).

The 284-case theorem covers 71 target orbits × 4 exact-three cores in its **specific common-U depth-two semantics**.

## Structural focus

There are seven maximally branched normalized triangle types (84–90). Up to permutation their radical pattern is

```text
(7*11, 5*11, 5*7)
```

with Boolean divisor-closure mask `0x7f`.

Type 84 is squarefree. Types 85–90 differ by extra powers on 5/7/11 arms. This is an ideal target for a repeated-power descent/pivot argument.

## Attack directions

### C1. Characterize when an arbitrary-depth bad packet contains an exact common-U depth-two subpacket

Prove sufficient conditions under which a legal arbitrary-depth first-exhaustion configuration must project to one of the certified 284 cases. Be meticulous about the meaning of common `U` and simultaneous exhaustion.

### C2. Repeated-power 0x7f descent

For types 85–90, ask whether the top q-adic repeated arm forces:

- a q-frame;
- a blocker rail;
- a q→p pivot;
- a tight backtrack and two-prime rectangle;
- or a slack branch creating extra prime support.

Try to close all branches or reduce them to Track D's HN-good side.

### C3. Small surviving CARD9 packet

If Track A produces a phase-feasible 9-set, specialize the residue model to those nine parents. Restore only the discrete choices needed to test common-U / triangle / blocker contradictions. Seek a small exact Farkas or SAT certificate.

### C4. Counterexample search

Attempt to build legal repeated-power packets that evade both the 284 theorem and the proposed pivot descent. Any such object is important: save it explicitly.

## Hard rule

The statement “same radical” is never enough to replace `q^2` or `q^3` by `q`. Every exponent reduction must preserve the relevant residue/collision/coverage claim.

## Deliverable

A new symbolic descent lemma, a finite exact certificate family, or a concrete counterexample showing why the hoped-for bridge is false.
