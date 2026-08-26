# Referee Audit Queue

Handoff staging area between **proof-closer** and **E_referee** agents.

## Structure

- **`IN/`** — New submissions from erdos7-gate1-closer. Awaiting E_referee pickup.
- **`AUDITING/`** — Currently under E_referee independent review and falsification.
- **`PASSED/`** — Referee approved and locked. Ready for QED-gate closure.
- **`FAILED/`** — Referee found blocker, counterexample, or gap. Returned to author for fix.

## Submission Workflow

1. **Proof-closer** creates a theorem and reaches `PROVED_EXACT` or `PROVED_SYMBOLIC`.
2. **Creates handoff record** at `IN/[THEOREM]_[DATE].md` following `E_REFEREE_HANDOFF_PROTOCOL.md`.
3. **Documents all artifacts, verifier command, weak points, and dependencies.**
4. **E_referee monitors `IN/`** and begins independent replay and falsification.
5. **E_referee moves record to `AUDITING/`** and fills in the audit log.
6. **Outcome:**
   - ✓ **APPROVED** → Move to `PASSED/`. Theorem closed for gate.
   - ✗ **NEEDS_FIX** → Move to `FAILED/`. Author must address blocker and resubmit.

See `E_REFEREE_HANDOFF_PROTOCOL.md` for detailed format and responsibilities.

## Historical Index

| Theorem | Author | Submitted | Auditor | Approved | Final Status |
|---------|--------|-----------|---------|----------|--------------|
| *(To be populated as submissions arrive)* | | | | | |

---

**Last updated:** 2026-08-25  
**Status:** Queue initialized, awaiting first proof-closer submission.
