# Erdős #7 Codex multi-agent proof campaign

A coordinated six-track research repository for the ongoing attempted proof of Erdős Problem #7 (odd distinct covering systems).

**Current status: OPEN. No QED.**

## Why this repo exists

The project has reached a finite but delicate frontier around canonical state 2275. Several local families are exactly certified, while the remaining bridge is correlated survivor dispersion under arbitrary repeated prime powers. This repo packages the exact evidence and assigns six independent Codex workstreams so one line of attack does not dominate the search prematurely.

## Start

Read, in order:

1. `AGENTS.md`
2. `docs/CURRENT_FRONTIER.md`
3. `docs/QED_GATES.md`
4. `coordination/CAMPAIGN.md`
5. your assigned `agents/<track>/BRIEF.md`

## Tracks

- A — exact CARD9 / finite certificate
- B — structural slab/concentration theorem
- C — common-U / triangle / blocker descent
- D — HN / BBMST correlated analytic bridge
- E — adversarial referee / exact replay
- F — global 7,637-state lift and high-prime interface

## Immutable exact evidence

`artifacts/exact/` is read-only evidence. Verify with:

```bash
sha256sum -c artifacts/EXACT_SHA256SUMS.txt
```

where supported. Do not overwrite these files.

## Python environment

The checkpoint was produced with Python 3.13, NumPy 2.3.x and SciPy 1.17.x. See `requirements.txt`.

Some historical experimental scripts may have stale absolute paths or missing helper modules. Track A's first task is explicitly to make its active path repository-relative and validate any reconstructed helper against saved checkpoint outputs before using it for theorem claims.

## Proof status

Use the vocabulary in `coordination/PROOF_STATUS.md`. In particular, a solver saying `infeasible` is not the final proof artifact unless the result is converted into an independently replayable exact certificate/exhaustive proof.
