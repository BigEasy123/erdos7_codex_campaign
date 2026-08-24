# CARD9 exact-certificate audit

Audit status: **OPEN**. No CARD9 promotion is justified.

## Findings

1. The phase oracle minimizes `t` subject to `t >= 0` and generated inequality constraints. A positive optimum is a lower-bound claim, not a Farkas infeasibility claim. The requested signs `y >= 0`, `y^T A >= 0`, `y^T b < 0` do not directly certify this optimization rejection.
2. The source model constructs many coefficients through floating values. The canonical schema records their serialized rational spellings, but this does not prove those spellings are the intended mathematical constants.
3. The five-record replay matches saved floating `phi` values exactly, but this validates implementation compatibility only.
4. The raw solver dual for a saved rejection fails the exact rational dual check. No phase certificate was emitted.
5. The reconstructed compact helper produces conservative threshold consequences. The historical compact database has no derivation trace linking each stored subset cap to a certificate.
6. The sparse master has only numerical Benders cuts and nogoods. A one-iteration `ITER_LIMIT` result is not an UNSAT proof.
7. The 42 symmetry maps pass permutation/index checks, but symmetry preservation alone does not certify every transformed floating cut.
8. The arbitrary-depth interface remains open for repeated powers, pooled tail direction, and domination of all legal continuations.

## Required before `PROVED_EXACT`

- Freeze rational source constants and a deterministic phase matrix.
- Rationally repair and exactly verify one dual lower-bound certificate per rejected phase.
- Derive and verify every Benders cut and symmetry image from those certificates.
- Produce an optimizer-independent exhaustive/branch certificate for `sum(e)=9`.
- Prove the arbitrary-depth interface and independently replay it.
