# Coordinator synthesis

## Current project status

Status: OPEN

The exact local proof assets already in the repository are not yet sufficient to claim a final theorem. The cleanest evidence in-hand is the exact replay package for the low-prime state-2275 exact certificates:

- [artifacts/exact/STATE2275_FULL_EXACT_REPLAY.txt](../artifacts/exact/STATE2275_FULL_EXACT_REPLAY.txt)
- [artifacts/exact/STATE2275_FARKAS_CERTIFICATES_STAGE18_EXACT.json](../artifacts/exact/STATE2275_FARKAS_CERTIFICATES_STAGE18_EXACT.json)
- [artifacts/exact/FULLCOVER_71x4_FARKAS_EXACT_REPLAY.txt](../artifacts/exact/FULLCOVER_71x4_FARKAS_EXACT_REPLAY.txt)

These pass replay without optimizer calls and are therefore the only exact assets we can safely treat as evidence on the current path. They do not yet close the full state-2275 arbitrary-depth bridge.

## Safe exact evidence

- The exact Stage-18 replay passes and yields the current HN constants and exact rational margins.
- The 284-case common-U family passes the exact replay package with 284/284 cases accepted.
- The checkpoint validation passes: [scripts/validate_checkpoint.py](../scripts/validate_checkpoint.py).

## Unsafe or unverified claims

- Track A is currently blocked by a repository-portability and missing-helper failure. See [agents/A_card9/RESULT.md](../agents/A_card9/RESULT.md) and the verifier [agents/A_card9/verify_repo_relative.py](../agents/A_card9/verify_repo_relative.py).
- There is no theorem-level result yet from Track B, C, D, or F.
- No Track E referee audit has been produced yet. Because no dependency has been marked AUDITED_EXACT, no final proof path is eligible for promotion.

## Smallest current obstruction to QED

The smallest hard obstruction is the local CARD9 closure path:

1. the phase helper is missing;
2. the active solver still includes machine-specific absolute paths;
3. no replayable exact 9-parent certificate or genuine survivor has been frozen;
4. without that, the state-2275 bridge cannot be closed or handed to B/C/D/F in a certified form.

## Redirective plan

- If Track A finds a genuine phase-feasible 9-set, freeze it immediately and hand the exact packet to B/C/D with referee review.
- If Track A proves exact 9-layer infeasibility, then Track F must consume that certificate and prove the lift from the 9-layer to the wider canonical state family.
- If Track B or C produces a structural lemma, Track A must encode it as exact cuts or finite reductions while Track E attacks the assumptions.
- If Track D produces a valid analytic bridge, Track A must test it exhaustively and Track E must verify the exact hypotheses and directionality.

## Final gate condition

No QED claim is allowed until Track E marks every dependency on the final proof path as AUDITED_EXACT. Until then, the campaign remains OPEN.
