---
title: "Implementation Summary: Erdős 7 Gate-1 Proof Pipeline"
date: 2026-08-25
status: "COMPLETE"
---

# Summary: Complete Proof Pipeline Implementation

## What Was Built

A **rigorous exact-mathematics proof pipeline** for closing the Erdős 7 Gate-1 bottleneck. This pipeline ensures that all theorems are mathematically sound, independently verified, and free from optimizer-status creep.

---

## Files Created (15 total)

### Agent & Role Definition
1. **`.github/agents/erdos7-gate1-closer.agent.md`**
   - Full tool access agent specialized for exact symbolic proof.
   - Mandatory startup checklist (reads all Gate-1 docs).
   - Six core responsibilities, five-stage approach.
   - Strict discipline constraints (14 "NEVER" rules, 8 "DO" rules).
   - User-invocable + subagent capable.

### Instructions & Templates
2. **`.github/instructions/exact-proof-template.instructions.md`**
   - Required structure for every new theorem.
   - Nine mandatory sections (statement, hypotheses, dependencies, proof, scope, repeated-power audit, verifier, hashes, status).
   - Checklist before submission.
   - Example stubs and error cases.

### Verification & Audit
3. **`.github/prompts/erdos7-verify-asset.prompt.md`**
   - Pre-audit workflow for any artifact or theorem.
   - Five-step verification: source → verifier → hashes → paths → optimizer check.
   - Outputs: `AUDITED_EXACT`, `AUDITED_SYMBOLIC`, `BROKEN`, `BLOCKED_DEPENDENCY`, `PRECISE_GAP`.

4. **`coordination/E_REFEREE_HANDOFF_PROTOCOL.md`**
   - Complete handoff record format (7 sections).
   - Workflow: IN → AUDITING → PASSED / FAILED.
   - Separation of author and reviewer.
   - Dependency closure verification.
   - Status propagation to QED_GATES.
   - Integration checklist.

### Referee Queue (5 subdirectories + README)
5. **`coordination/referee_queue/README.md`** — Main index.
6. **`coordination/referee_queue/IN/README.md`** — New submissions.
7. **`coordination/referee_queue/AUDITING/README.md`** — Under review.
8. **`coordination/referee_queue/PASSED/README.md`** — Approved for gates.
9. **`coordination/referee_queue/FAILED/README.md`** — Blockers found.

### Validation Hooks
10. **`.github/hooks/exact-artifact-validation.json`**
    - Declarative hook definitions (5 hooks: SHA256, paths, verifiers, completeness, archive).
    - Post-tool-use triggers for artifact validation.
    - Pre-compact hook for audit archiving.
    - **Critical note:** Hooks verify mechanics, NOT mathematical correctness.

### Hook Scripts (PowerShell)
11. **`scripts/hooks/validate_artifact_sha256.ps1`** — File integrity check.
12. **`scripts/hooks/validate_repository_paths.ps1`** — Portability check (reject absolute paths).
13. **`scripts/hooks/run_declared_verifier.ps1`** — Execute verifiers.
14. **`scripts/hooks/check_proved_exact_completeness.ps1`** — Verify required sections.
15. **`scripts/hooks/archive_failed_audits.ps1`** — Preserve failed audits.

### Workflow Documentation
16. **`docs/PROOF_CLOSER_WORKFLOW.md`** (this file explains the complete workflow)
    - Architecture diagram.
    - How to invoke the agent.
    - Phase 1: Prove theorem.
    - Phase 2: E_referee audit.
    - Phase 3: Use for gate closure.
    - Quick reference commands.
    - Integration checklist.

---

## Key Features

### ✓ Exact Arithmetic Enforcement
- No optimizer status as proof.
- No `Fraction(str(float))` for constants.
- Independent verifiers required.
- Rational and symbolic derivations preferred.

### ✓ Conservative Status Labels
- `PROVED_EXACT` — Finite, reproducible, optimizer-free.
- `PROVED_SYMBOLIC` — Valid symbolic proof, hypotheses explicit.
- `NUMERICAL_EVIDENCE` — Optimizer output (not a theorem).
- `COUNTEREXAMPLE` — Falsifying witness found.
- `OPEN` — Unresolved, blocker documented.
- `BLOCKED_DEPENDENCY` — Waiting on another theorem.

### ✓ Mechanical Validation Hooks
- SHA256 verification for artifact integrity.
- Repository path checks (reject absolute paths).
- Verifier executable tests.
- PROVED_EXACT completeness checks.
- **Important:** Do NOT promote mathematical claims automatically.

### ✓ Separation of Concerns
- Proof-closer: Author of theorems.
- E_referee: Independent auditor.
- Handoff queue: Mediates coordination.
- Status tracking: All timestamped and archived.

### ✓ No Self-Audit
- Author cannot move their own theorem to PASSED.
- E_referee must approve independently.
- Failed audits can be re-opened if flaws found later.

### ✓ Dependency Closure Tracking
- Every dependency must be verified or listed as OPEN.
- Cannot use NUMERICAL_EVIDENCE or COUNTEREXAMPLE as proof.
- Circular dependencies forbidden.

---

## Workflow Overview

```
┌─ PROVE (erdos7-gate1-closer)
│  └─ Write exact theorem + verifier + artifacts
│     └─ Commit → Hooks auto-run (SHA256, paths, verifier)
│        └─ Create handoff record
│
├─ AUDIT (E_referee)
│  └─ Move to AUDITING/
│     └─ Independent replay + falsification
│     └─ Check dependencies
│     └─ Decision: APPROVED or NEEDS_FIX
│
├─ APPROVED → PASSED/
│  └─ Theorem status: PROVED_EXACT or PROVED_SYMBOLIC
│     └─ Dependents unlocked
│     └─ Can close QED-gate edge
│
└─ FAILED → Author fixes
   └─ Resubmit to IN/
      └─ E_referee audits again
```

---

## How to Start Using This

### Immediately: Test on Real Bottleneck

Invoke the agent in VS Code chat:

```
Use agent: erdos7-gate1-closer

Prove `SAFE_RELAXATION_DOMINATION = PROVED_SYMBOLIC` for 
the current state-2275 arbitrary-depth child model...

[Full task as specified in your original request]
```

The agent will:
1. Read the Gate-1 documentation.
2. Construct exact maps and proof sketches.
3. Hunt for counterexamples actively.
4. Produce a theorem file following exact-proof-template.
5. Create independent verifier script(s).
6. Commit artifacts with SHA256 hashes.

### Next: E_referee Review

1. Agent (or you) creates handoff record in `coordination/referee_queue/IN/`.
2. E_referee agent reviews (or manually execute the audit checklist from E_REFEREE_HANDOFF_PROTOCOL.md).
3. Records moved to PASSED/ or FAILED/.

### Then: Gate Closure

Once theorem is PASSED and all dependencies verified:
- Update source file status to PROVED_EXACT or PROVED_SYMBOLIC.
- Check if QED-gate edge closes.
- Update docs/QED_GATES.md.

---

## Critical Design Decisions

1. **Hooks are mechanical, not mathematical.**
   - They verify SHA256, paths, and verifier runability.
   - They do NOT check proof correctness.
   - Mathematical claims require E_referee audit.

2. **No silent weakening of theorems.**
   - If repeated powers, radicals, or primes are handled differently, document it explicitly.
   - If scope changes, update hypotheses and re-audit.

3. **Reversible gate closure.**
   - If a later falsification finds a flaw in PASSED theorem, it moves back to FAILED.
   - Dependent gates must re-open.
   - This is a feature, not a bug—transparency is critical.

4. **Aggressive counterexample hunting.**
   - Every new lemma must be actively tested for falsification.
   - Small instances, boundary cases, adversarial cases.
   - "Not falsified yet" ≠ "true"; it's "not yet known to be false."

5. **Weakest sufficient theorem preferred.**
   - Prove only what's needed for the next gate edge.
   - Avoid over-proving; it introduces unnecessary dependencies.

---

## Files Reference

| File | Purpose | Key Sections |
|------|---------|--------------|
| `.github/agents/erdos7-gate1-closer.agent.md` | Agent role | Startup checklist, 6 responsibilities, 5 stages |
| `.github/instructions/exact-proof-template.instructions.md` | Theorem template | 9 required sections, checklist |
| `.github/prompts/erdos7-verify-asset.prompt.md` | Pre-audit workflow | 5-step verification, output format |
| `coordination/E_REFEREE_HANDOFF_PROTOCOL.md` | Audit protocol | Handoff format, workflow, dependency checks |
| `coordination/referee_queue/` | Queue structure | IN/, AUDITING/, PASSED/, FAILED/ |
| `.github/hooks/exact-artifact-validation.json` | Hook definitions | 5 PostToolUse hooks, 1 PreCompact |
| `scripts/hooks/*.ps1` | Hook implementations | SHA256, paths, verifier, completeness, archive |
| `docs/PROOF_CLOSER_WORKFLOW.md` | Usage guide | Phase 1-3, commands, principles |

---

## Status

✅ **READY TO USE**

All files created. Agent is callable. Hooks are configured. Referee queue is initialized.

**Next immediate step:** Invoke erdos7-gate1-closer on SAFE_RELAXATION_DOMINATION task.

---

## Support

For questions on:
- **Agent behavior** → See `.github/agents/erdos7-gate1-closer.agent.md` (Constraints, Approach, Output Format).
- **Theorem structure** → See `.github/instructions/exact-proof-template.instructions.md` (Required Sections, Checklist).
- **Pre-audit verification** → See `.github/prompts/erdos7-verify-asset.prompt.md` (5 steps, output statuses).
- **E_referee workflow** → See `coordination/E_REFEREE_HANDOFF_PROTOCOL.md` (Handoff format, reviewer instructions, status propagation).
- **Usage & commands** → See `docs/PROOF_CLOSER_WORKFLOW.md` (Quick reference, phases, integration checklist).

---

**Implementation date:** 2026-08-25  
**Author:** GitHub Copilot  
**Status:** Complete and tested; ready for first theorem.
