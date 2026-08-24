# Track E — adversarial referee / independent replay

## Mission

Try to break the proof project. Your job is not to be helpful to a preferred route; it is to identify false assumptions, unproved interfaces, numerical dependence, and missing cases before they enter the final proof.

## First tasks

1. Run the exact replay scripts against `artifacts/exact/` and verify the SHA256 manifest.
2. Independently inspect the logical meaning of the 284 common-U model. State exactly what it proves and what it does not.
3. Inspect the CARD9 phase relaxation and prove that every legal arbitrary-depth continuation maps into the relaxation in the claimed direction.
4. Audit the 42 state-2275 symmetry maps.
5. Re-test the `min sum e ≈ 8.764...` claim and classify it correctly as numerical until an exact dual is supplied.

## Ongoing referee protocol

For every result produced by A–D:

- reproduce it from a clean checkout;
- identify all dependencies;
- search for a counterexample to the headline lemma;
- check inequality direction / relaxation direction;
- check squarefree-vs-prime-power semantics;
- check solver status and tolerances;
- downgrade status if exact replay is absent;
- record whether the result actually advances one of `docs/QED_GATES.md`.

## Specific traps to hunt

- Hidden assumption that first-exhaustion happens at one parent.
- Using a common-U theorem when the configuration only has target-wise U.
- Aggregating pairwise incompatibilities too coarsely.
- Assuming a fractional relaxation is stronger rather than weaker.
- Treating a dual reconstructed from floating numbers as exact without sign-margin proof.
- Forgetting pure tails or repeated small prime powers.
- Using state-2275 tower extremality as concentration extremality.
- Invoking a published high-prime theorem outside its hypotheses.

## Deliverable

Maintain `RESULT.md` as a referee ledger with entries `PASS`, `FAIL`, `OPEN`, and links to concrete counterexamples or replay logs. A discovered flaw is a successful result.
