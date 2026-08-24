# Track B — structural slab / concentration attack

## Mission

Explain mathematically why near-extremal CARD9 packets concentrate in the small `a0=0, a1=2` slab, and turn that pattern into a symbolic inequality or finite structural reduction that attacks **all** dangerous packets rather than enumerating them.

You are intentionally independent of Track A's Benders completion. Do not merely add more solver cuts.

## Inputs

- `docs/CURRENT_FRONTIER.md`
- `agents/A_card9/BRIEF.md` only for terminology, not results
- `artifacts/current_state/EONLY_CARD9_GREEDY_PHASE_RECORDS.json`
- `artifacts/current_state/CARD9_SPARSE_EXACT_RECORDS.json`
- `src/state2275_hn_milp.py`
- `src/state2275_child_pooled_master.py`
- `src/classify_triangle_all_order_types.py`

Representative near-extremal rejected packet:

```text
{10,27,33,34,36,48,55,90,138}
```

with phase margin about `0.0329460`.

## Questions to answer

1. Decode the parent indices into shallow coordinates and classify the low-margin candidates by slabs, fibers, and residue symmetries.
2. Is there a combinatorial reason that exhausting 9 parents while respecting common residue choices forces many of them into a common low-coordinate slab?
3. Can slab concentration be converted into one of:
   - a common-U obstruction;
   - a forced comparable-modulus collision;
   - a forced transversal triangle/blocker packet;
   - a lower bound on the number of distinct next-3 children / future squarefree residues;
   - an HN-good dispersion estimate?
4. Try to formulate the weakest clean lemma that would eliminate the observed extremal geometry.
5. Search explicitly for counterexamples to the lemma before trying to prove it.

## Preferred methodology

- Enumerate/plot parent coordinates and orbit invariants.
- Compute exact counts, not just visual patterns.
- State candidate lemmas first, then attempt exhaustive small counterexample searches.
- If a lemma appears true, prove it from the fixed state-2275 residue geometry rather than from properties of the optimizer objective.

## Structural facts you may use only if you re-check their hypotheses

- compatible terminal pair compression;
- exact p-frame hub/blocker rail;
- p=3 chain/fork exact-three geometry;
- compatible transversal triangle for surplus terminals;
- pair-overlap arms pairwise coprime;
- tight p→q backtrack forcing a two-prime exponent rectangle.

## Deliverable

A success is a **PROVED_SYMBOLIC** concentration/slab lemma or an exact finite reduction that materially shrinks Track A/C. A counterexample to a tempting structural lemma is also valuable and should be status `COUNTEREXAMPLE`.
