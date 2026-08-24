# Track A — exact CARD9 / finite certificate attack

## Mission

Decide the current state-2275 exact-cardinality-9 exhaustion layer as rigorously and efficiently as possible.

Your primary target is:

> Under the safe pooled child-capacity + Hunter relaxation currently encoded in the project, can a set of exactly nine shallow parents be simultaneously exhausted while remaining on the BBMST-bad side?

A success is **either**:

1. an exact finite certificate that no such 9-set exists in the relaxation, with optimizer-free replay; **or**
2. a genuine phase-feasible 9-parent set, with enough continuous/discrete witness data to hand to Track C/D.

Do not assume that closing CARD9 alone proves state 2275; explain what further cardinalities or analytic implications remain.

## Start here

- `docs/CURRENT_FRONTIER.md`
- `src/card9_sparse_exact_benders.py`
- `src/eonly_phase_benders.py`
- `src/state2275_child_pooled_master.py`
- `artifacts/current_state/EONLY_CARD9_COMPACT30.pkl`
- `artifacts/current_state/EONLY_CARD9_FULLPREFIX.pkl`
- `artifacts/current_state/EONLY_CARD9_NOGOODS.pkl`
- `artifacts/current_state/CARD9_SPARSE_EXACT_RECORDS.json`
- `artifacts/current_state/POOLED_MIN_EXHAUST_LP.json`

The saved CARD9 records contain 31 rejected exact 9-parent candidates at the current snapshot; the compact database contains 42,459 constraints and the nogood database 3,150 orbit images. Treat those as a checkpoint, not as proof that the whole layer is empty.

## Required first audit

Before extending the computation:

1. Make all paths repository-relative.
2. Reconstruct any missing helper module from the mathematical derivation rather than inventing behavior. In particular, if `eonly_card9_hybridprefix.py` / a saved `PhaseOracle` object is missing, rebuild the phase oracle from `eonly_phase_benders.py` and validate it on at least 5 saved rejected sets by reproducing their positive `phi` values to a tight tolerance.
3. Check the 42 state-2275 symmetry maps preserve the fixed partial and the phase model.
4. Verify every exact nogood was generated only from a phase-infeasible exact 9-set.

If any of these fail, stop the theorem claim and report `COUNTEREXAMPLE` or `BLOCKED_DEPENDENCY`.

## Preferred attacks

Try several, preserving restartable checkpoints:

### A1. Exact sparse Benders completion

Continue the fast exact-cardinality-9 master with:

- compact dual consequences;
- exact symmetry nogoods;
- selectively activated strongest full-prefix consequences;
- no timeout-as-infeasible mistakes.

If the master becomes infeasible, extract a finite proof object. A raw MIP `status=2` is only a stepping stone; seek a rational Farkas/LP certificate after fixing the binary combinatorics, a branch certificate, or another independently replayable finite witness.

### A2. Stronger master formulation

Look for a SAT/PB/CP-SAT or custom hereditary branch-and-bound formulation of the capped-subset constraints. If it proves the 9-layer empty, export a compact proof trace or independently checkable exhaustive decomposition.

### A3. Rationalize the `8.764...` bound

Recover the LP dual for

```text
min sum e = 8.76416923252369...
```

and convert it to an exact rational certificate proving `sum e > 8`. This would independently justify the cardinality-9 starting layer.

### A4. If a phase-feasible 9-set appears

Freeze it immediately. Save:

- the exact nine parent indices and shallow coordinates;
- phase LP primal values;
- active heavy/tail classes;
- relevant next-3 digit pools;
- squarefree residue choices if determined;
- exact/float residual margins.

Then stop broad enumeration and hand the packet to C/D.

## Forbidden shortcuts

- Do not infer CARD9 emptiness from hundreds of rejected candidates.
- Do not infer exact infeasibility from a numerical phase margin alone.
- Do not change the pooled relaxation in a direction that excludes legal continuations without proving validity.

## Deliverable

Write `RESULT.md` and `status.json`. If exact closure is obtained, include a one-command verifier under this directory and a SHA256 manifest of its certificate inputs.
