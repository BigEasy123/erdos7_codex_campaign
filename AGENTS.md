# Erdős #7 multi-agent campaign — repository rules

This repository is an attempted proof project for Erdős Problem #7 (odd distinct covering systems). It contains exact finite certificates, exploratory optimization code, and open theorem interfaces. **Do not claim QED unless every item in `docs/QED_GATES.md` is closed and independently replayed.**

## Read this first

1. `docs/CURRENT_FRONTIER.md` — current mathematical state and open bridge.
2. `docs/QED_GATES.md` — the only accepted definition of “finished”.
3. Your assigned `agents/<track>/BRIEF.md`.
4. `coordination/PROOF_STATUS.md` — allowed status labels and evidence standards.
5. Relevant source/certificate files named in your brief.

The root `AGENTS.md` is intentionally short. Treat `docs/` and the exact verifier code as the system of record.

## Global proof discipline

- Distinguish **PROVED_EXACT**, **PROVED_SYMBOLIC**, **NUMERICAL_EVIDENCE**, **COUNTEREXAMPLE**, **UNKNOWN/TIMEOUT**, and **HEURISTIC**.
- A solver timeout is never infeasibility.
- Floating-point LP/MILP output is never an exact theorem unless a rational/integer certificate is extracted and replayed without the optimizer.
- Do not silently replace arbitrary prime powers by squarefree supports.
- Do not assume a concentration-preserving canonical compression theorem; that is not proved.
- Do not revive routes listed in `docs/DEAD_ENDS.md` unless you explicitly explain what new hypothesis or inequality fixes the recorded failure.
- When you find a counterexample to a proposed lemma, preserve it in machine-readable form.
- When you prove a finite infeasibility, produce a standalone optimizer-free verifier whenever feasible.
- Never modify files under `artifacts/exact/`. They are immutable evidence; verify hashes against `artifacts/EXACT_SHA256SUMS.txt`.
- Put new work only in your agent directory and, if needed, new files under `src/experiments/<track>/`.

## Required deliverable for every track

At minimum create/update:

- `agents/<track>/RESULT.md`
- `agents/<track>/status.json`
- any certificate / counterexample / verifier used by the result

`status.json` must follow `coordination/status_schema.json`.

## Reproducibility

Record:

- command lines;
- package versions if solver behavior matters;
- SHA256 of important generated certificates;
- exact rational margins when a result is promoted to PROVED_EXACT.

## Collaboration rule

Agents are intentionally given different attack surfaces. Do not collapse into another track’s approach just because it is already in the repo. Cross-track results may be used only after you identify the dependency explicitly in `RESULT.md`.

## Final standard

The project wins only if an adversarial reader can reconstruct the least-counterexample argument and replay every finite certificate from a clean checkout with no hidden solver assumptions.
