# Proof status vocabulary

Use exactly one primary status in each `status.json`.

- `PROVED_EXACT`: finite/computational claim with exact certificate and optimizer-free replay, or exact arithmetic proof.
- `PROVED_SYMBOLIC`: human-readable mathematical proof with all hypotheses discharged, no floating numerical dependency.
- `NUMERICAL_EVIDENCE`: solver/float evidence with no exact replay yet.
- `COUNTEREXAMPLE`: explicit valid object disproving the target lemma/model claim.
- `HEURISTIC`: pattern/idea worth pursuing but not a theorem.
- `UNKNOWN_TIMEOUT`: computation ended without proof or counterexample.
- `BLOCKED_DEPENDENCY`: cannot advance without another precise lemma/artifact.

A result can list secondary evidence, but the primary status must be the weakest status needed for the headline claim.
