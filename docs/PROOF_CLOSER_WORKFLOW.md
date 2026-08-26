---
title: "Erdős 7 Gate-1 Proof Closer — Implementation & Workflow Guide"
date: 2026-08-25
status: "READY_TO_USE"
---

# Erdős 7 Gate-1 Proof Closer Implementation Guide

## Overview

You now have a complete **exact-mathematics proof pipeline** for closing the Erdős 7 Gate-1 bottleneck. This document ties together:

1. **The `erdos7-gate1-closer` agent** — Your specialist for exact symbolic proof.
2. **Companion instructions & prompts** — Templates and verification workflows.
3. **E_referee handoff protocol** — Mandatory independent audit queue.
4. **Mechanical validation hooks** — Auto-checks for artifacts (SHA256, paths, verifiers).

---

## Architecture

```
┌─────────────────────────────────────────┐
│  Proof-Closer Agent                     │
│  (erdos7-gate1-closer.agent.md)        │
│  Role: Prove theorems rigorously       │
└──────────────┬──────────────────────────┘
               │
               ├─ Reads: QED_GATES, CURRENT_FRONTIER, DEAD_ENDS
               ├─ Writes: docs/GATE1_*.md (exact theorems)
               ├─ Produces: exact artifacts + verifier scripts
               │
               ▼
┌─────────────────────────────────────────┐
│  Exact-Proof-Template.instructions.md   │
│  Ensures every theorem has:             │
│  - Exact statement                      │
│  - Explicit hypotheses                  │
│  - Independent verifier                 │
│  - SHA256 artifacts                     │
│  - Conservative status labels           │
└─────────────────────────────────────────┘
               │
               ├─ Mechanical validation hooks (auto-run)
               │  • SHA256 verification
               │  • Repository path checks
               │  • Verifier executable tests
               │  • PROVED_EXACT completeness checks
               │
               ▼
┌─────────────────────────────────────────┐
│  E_referee Handoff Queue                │
│  coordination/referee_queue/             │
│  - IN/        (new submissions)         │
│  - AUDITING/  (under review)            │
│  - PASSED/    (approved for gate)       │
│  - FAILED/    (blockers found)          │
└─────────────────────────────────────────┘
               │
               └─ E_referee Agent
                  Role: Independent replay + falsification
                  Protocol: E_REFEREE_HANDOFF_PROTOCOL.md
                  Output: AUDITED_EXACT / AUDITED_SYMBOLIC / BROKEN

               │
               ▼
        Only PASSED theorems count
        for closing QED-gate edges
```

---

## Files Created

### 1. **Agent Definition**
- **`.github/agents/erdos7-gate1-closer.agent.md`**
  - Full tool access (read, edit, search, execute, terminal).
  - User-invocable + subagent capable.
  - Mandatory startup checklist (read Gate-1 docs).
  - Six core responsibilities + five-stage approach.
  - Strict "NEVER" and "DO" constraints.

### 2. **Proof Template (Instructions)**
- **`.github/instructions/exact-proof-template.instructions.md`**
  - Required sections for every new theorem:
    1. Exact theorem statement
    2. Explicit hypothesis list
    3. Imported dependencies
    4. Proof / certificate construction
    5. Scope and limitations
    6. Repeated-power audit
    7. Independent verifier command
    8. Artifact hash (SHA256)
    9. Proof-status label
  - Checklist before submission.
  - Example stubs.

### 3. **Verification Prompt**
- **`.github/prompts/erdos7-verify-asset.prompt.md`**
  - Pre-audit any artifact or theorem.
  - Five-step verification workflow:
    1. Locate source derivation.
    2. Run independent verifier.
    3. Verify artifact hashes.
    4. Check repository paths.
    5. Confirm no optimizer status as proof.
  - Outputs: `AUDITED_EXACT`, `AUDITED_SYMBOLIC`, `BROKEN`, `BLOCKED_DEPENDENCY`, or `PRECISE_GAP`.

### 4. **E_referee Handoff Protocol**
- **`coordination/E_REFEREE_HANDOFF_PROTOCOL.md`**
  - Handoff record format (all required sections).
  - Workflow: Proof-closer → IN → AUDITING → PASSED / FAILED.
  - Separation of concerns (author ≠ reviewer).
  - Status propagation rules.
  - Dependency closure checklist.
  - Integration with QED_GATES.md.

### 5. **Referee Queue Structure**
- **`coordination/referee_queue/`**
  - `IN/` — New submissions.
  - `AUDITING/` — Under review.
  - `PASSED/` — Approved and locked.
  - `FAILED/` — Blockers found; return to author.
  - `README.md` — Index and historical record.

### 6. **Validation Hooks**
- **`.github/hooks/exact-artifact-validation.json`**
  - Mechanical post-tool-use checks:
    - SHA256 verification for `artifacts/exact/**`.
    - Repository path validation (reject absolute paths).
    - Run declared verifiers (if present).
    - PROVED_EXACT completeness checks.
  - **Critical:** Hooks do NOT promote mathematical claims. E_referee audit is mandatory.

- **`scripts/hooks/*.ps1`** (PowerShell implementations)
  - `validate_artifact_sha256.ps1` — Check file integrity.
  - `validate_repository_paths.ps1` — Enforce portability.
  - `run_declared_verifier.ps1` — Execute verifiers.
  - `check_proved_exact_completeness.ps1` — Verify required sections.
  - `archive_failed_audits.ps1` — Preserve failed audits.

---

## How to Use

### Phase 1: Prove a Theorem

#### Step 1a: Invoke the Agent

**Manually in VS Code chat:**

```
Use agent: erdos7-gate1-closer

Task: Prove `SAFE_RELAXATION_DOMINATION = PROVED_SYMBOLIC` for the 
current state-2275 arbitrary-depth child model.

Read the Gate-1 reports first. Do not assume the existing child-pooled 
model is sound. Construct an explicit map from every genuine arbitrary-depth 
continuation into the relaxation...

[Full task as specified in your initial request]
```

**Or call as subagent from coordinator:**

```python
agent = subagent("erdos7-gate1-closer")
result = agent("""
    Prove SAFE_RELAXATION_DOMINATION = PROVED_SYMBOLIC...
""")
```

#### Step 1b: Follow the exact-proof-template

The agent writes a new theorem file, e.g., `docs/GATE1_SAFE_RELAXATION_THEOREM.md`.

It must include **all nine sections** from `.github/instructions/exact-proof-template.instructions.md`:

1. Theorem statement (exact and formal).
2. Explicit hypotheses (all sources traced).
3. Dependencies (all verified or listed as OPEN).
4. Proof / certificate (SAT/Farkas/symbolic/exhaustive).
5. Scope limitations (no silent assumptions).
6. Repeated-power audit (explicit handling).
7. Verifier command (runs without optimizer).
8. Artifact hashes (SHA256 for all files).
9. Status label (`PROVED_EXACT`, `PROVED_SYMBOLIC`, `NUMERICAL_EVIDENCE`, `COUNTEREXAMPLE`, `OPEN`, `BLOCKED_DEPENDENCY`).

#### Step 1c: Mechanical Hooks Auto-Run

After the agent commits:

```bash
git add docs/GATE1_SAFE_RELAXATION_THEOREM.md artifacts/exact/...
git commit -m "Theorem: SAFE_RELAXATION_DOMINATION"
```

**Hooks automatically:**
- ✓ Check SHA256 for new artifacts.
- ✓ Reject any absolute paths.
- ✓ Run the declared verifier (if present).
- ✓ Verify PROVED_EXACT has hash + verifier.

**Important:** Passing hooks ≠ proof correctness. They only verify mechanical properties.

---

### Phase 2: E_referee Independent Audit

#### Step 2a: Proof-Closer Submits Handoff

Once the agent reaches `PROVED_EXACT` or `PROVED_SYMBOLIC`:

1. Create handoff record at `coordination/referee_queue/IN/[THEOREM]_[DATE].md`.
2. Include all sections from `E_REFEREE_HANDOFF_PROTOCOL.md`:
   - Metadata header.
   - Full theorem (copy from proof file).
   - Changed files & artifacts.
   - Dependency closure checklist.
   - Known weak points (author's self-report).
   - Reviewer instructions.
   - Empty audit log (filled by E_referee).

3. Commit and tag:
```bash
git add coordination/referee_queue/IN/SAFE_RELAXATION_DOMINATION_2026-08-25.md
git commit -m "Handoff: SAFE_RELAXATION_DOMINATION to E_referee"
git tag handoff/SAFE_RELAXATION_DOMINATION/2026-08-25
```

#### Step 2b: E_referee Reviews

E_referee agent monitors `coordination/referee_queue/IN/`:

1. **Reads the full handoff record** (all sections).
2. **Moves to AUDITING/** to signal active review.
3. **Performs independent verification:**
   - Run verifier from clean checkout.
   - Verify SHA256 matches (re-compute all hashes).
   - Check paths are relative and portable.
   - Scan for optimizer status (reject if found).
   - **Actively attempt falsification** (focus on weak points).
   - Verify all dependencies are PROVED_EXACT or PROVED_SYMBOLIC.
4. **Fills in Audit Log** (Section 7 of handoff record).
5. **Decision:**
   - ✓ **APPROVED** → Move to `PASSED/`. Theorem ready for gate.
   - ✗ **NEEDS_FIX** → Move to `FAILED/`. Document blocker precisely.
   - ⊘ **BLOCKED_DEPENDENCY** → Keep in `IN/`. Notify author of dependency.

#### Step 2c: (If Needed) Fix and Resubmit

If marked `NEEDS_FIX`:

1. Author reads the blocker in the audit log.
2. Fixes the theorem or artifact.
3. Reruns verifier and recomputes hashes.
4. Updates the handoff record with new timestamp and output.
5. Resubmits to `coordination/referee_queue/IN/`.
6. E_referee reviews again.

---

### Phase 3: Use Approved Theorems for Gate Closure

Once a theorem is `PASSED`:

1. **Update the theorem source** to status `PROVED_EXACT` or `PROVED_SYMBOLIC` (not `CANDIDATE_*`).
2. **Mark dependent theorems** that now have verified dependencies.
3. **Check if any QED-gate edge closes** (all dependencies met).
4. **Update `docs/QED_GATES.md`** if a gate closes.

---

## Quick Reference: Commands

### Invoke the Agent

```
/erdos7-gate1-closer
Prove SAFE_RELAXATION_DOMINATION = PROVED_SYMBOLIC...
```

### Verify an Artifact

```
/erdos7-verify-asset
Artifact: artifacts/exact/safe_relaxation_cert.json
```

### Check Handoff Queue Status

```bash
# View new submissions
ls coordination/referee_queue/IN/

# View approved theorems
ls coordination/referee_queue/PASSED/

# View failures requiring fix
ls coordination/referee_queue/FAILED/
```

### Run Validation Hooks Manually

```bash
# SHA256 validation
powershell scripts/hooks/validate_artifact_sha256.ps1

# Path validation
powershell scripts/hooks/validate_repository_paths.ps1

# Run verifiers
powershell scripts/hooks/run_declared_verifier.ps1

# Completeness check
powershell scripts/hooks/check_proved_exact_completeness.ps1
```

### Commit & Tag a Handoff

```bash
git add coordination/referee_queue/IN/[THEOREM]_[DATE].md
git commit -m "Handoff: [THEOREM_NAME] to E_referee"
git tag handoff/[THEOREM_NAME]/[DATE]
git push origin [THEOREM_NAME] handoff/[THEOREM_NAME]/[DATE]
```

---

## Key Principles

1. **Exact over convenient:** No optimizer status, no `Fraction(str(float))`, no numerical evidence as proof.
2. **Separation of concerns:** Proof-closer writes theorems; E_referee audits independently.
3. **Conservative labeling:** Status is honest. PROVED_EXACT requires finite verifiable proof. PROVED_SYMBOLIC requires explicit hypotheses and algebraic chain.
4. **No self-promotion:** Author cannot move their theorem to PASSED. Only E_referee approves.
5. **Reversible:** If a flaw is found later, a PASSED theorem moves back to FAILED and dependent gates re-open.
6. **Transparent history:** All audits timestamped and archived. Full chain of custody preserved.

---

## Integration Checklist

- [x] Agent definition created (`.github/agents/erdos7-gate1-closer.agent.md`).
- [x] Exact-proof template instructions (`.github/instructions/exact-proof-template.instructions.md`).
- [x] Verification prompt (`.github/prompts/erdos7-verify-asset.prompt.md`).
- [x] E_referee handoff protocol (`.coordination/E_REFEREE_HANDOFF_PROTOCOL.md`).
- [x] Referee queue structure (`.coordination/referee_queue/` with IN, AUDITING, PASSED, FAILED).
- [x] Validation hooks (`.github/hooks/exact-artifact-validation.json` + scripts).
- [ ] **Next:** Test agent on SAFE_RELAXATION_DOMINATION.
- [ ] **Then:** Create E_referee agent if not already present.
- [ ] **Finally:** Establish approval chain in project CI/CD (optional).

---

## Known Limitations & Future Work

1. **Hooks are mechanical only.** They verify SHA256, paths, and verifier runability, but NOT mathematical correctness. E_referee audit is mandatory.

2. **Verifier discovery is regex-based.** If a verifier command is not in a standard section format, the hook may not find it. Maintain consistent section naming in theorems.

3. **No automatic gate closure.** Gates close only when E_referee approves AND all dependencies are verified. This is intentional—no automation shortcuts.

4. **Windows PowerShell hooks.** The hook scripts are written for PowerShell 5.1 (Windows). On Linux/Mac, convert to bash equivalents or use Git Hooks (`.git/hooks/`) integration.

5. **Multi-agent coordination.** The workflow assumes both erdos7-gate1-closer and E_referee agents are active. If using the default agent for E_referee, manually execute the audit checklist from `E_REFEREE_HANDOFF_PROTOCOL.md`.

---

## Getting Started: First Real Task

**Right now, you can invoke the agent on the actual bottleneck:**

```
Use agent: erdos7-gate1-closer

Prove `SAFE_RELAXATION_DOMINATION = PROVED_SYMBOLIC` for the current 
state-2275 arbitrary-depth child model.

Work from current HEAD and read the Gate-1 reports first. 
Do not assume the existing child-pooled model is sound.

Construct an explicit map from every genuine arbitrary-depth continuation 
into the relaxation, including arbitrary powers of 3,5,7,11,13, 
unresolved tails, shared next-3 digits, and divisor completion.

For every model inequality, prove: genuine feasible continuation ⊆ relaxation feasible set

Actively search for counterexamples to each pooling step.

Required deliverables:
- docs/GATE1_SAFE_RELAXATION_THEOREM.md
- exact/synthetic counterexample tests if relevant
- status PROVED_SYMBOLIC, COUNTEREXAMPLE, or OPEN
- exact next theorem needed for MIN_EXHAUST_GT8_EXACT_REPLAY=PASS
```

This is not a toy test—if the agent can make real progress here, the entire pipeline works.

---

**Created:** 2026-08-25  
**Status:** Ready to use.  
**Next:** Invoke agent, execute E_referee audit, close Gate-1 edges.
