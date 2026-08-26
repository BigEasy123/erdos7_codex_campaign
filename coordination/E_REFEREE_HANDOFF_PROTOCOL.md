---
name: "E_referee Handoff Protocol"
description: "Mandatory coordination protocol between proof-closer and E_referee agent. Every candidate PROVED_EXACT or PROVED_SYMBOLIC result must be staged in coordination/referee_queue/ before closing a QED-gate edge."
---

# E_referee Handoff Protocol

## Overview

The **Erdős 7 Gate-1 Proof Closer** produces candidate theorems and exact artifacts.  
The **E_referee** agent independently verifies, replays, and attempts falsification.  
The **handoff queue** mediates coordination and enforces separation of concerns.

**No QED-gate edge may close until both author and referee sign off.**

---

## Handoff Queue Structure

All handoff records go into:

```
coordination/referee_queue/
├── IN/                          # New submissions from proof-closer
│   └── [THEOREM_NAME]_[DATE].md
├── AUDITING/                    # Currently under E_referee review
│   └── [THEOREM_NAME]_[DATE].md
├── PASSED/                      # Referee approved; locked for Gate closure
│   └── [THEOREM_NAME]_[DATE].md
├── FAILED/                      # Referee found blocker or counterexample
│   └── [THEOREM_NAME]_[DATE]_FAILED.md
└── README.md                    # Index of all historical audits
```

---

## Handoff Record Format

**File name:** `coordination/referee_queue/IN/[THEOREM_NAME]_[ISO_DATE].md`

**Required sections:**

### 1. **Metadata Header**
```markdown
---
theorem_name: "Arbitrary-Depth Child-Pooled Domination"
status: CANDIDATE_EXACT  # or CANDIDATE_SYMBOLIC
author: erdos7-gate1-closer
submission_date: 2026-08-25T14:32:00Z
gate_target: Gate-1 state-2275 closure
required_for: SAFE_RELAXATION_DOMINATION = PROVED_SYMBOLIC
---
```

### 2. **Theorem Statement (Copy from exact-proof-template)**
```markdown
## Theorem

**Claim:** [Exact formal statement]

**Scope:** [Precisely which objects/states/families]

**Status:** [CANDIDATE_EXACT | CANDIDATE_SYMBOLIC]

[Copy all sections from exact-proof-template.instructions.md]
```

### 3. **Changed Files & Artifacts**
```markdown
## Artifacts and Changes

All files added or modified by proof-closer:

| File | Path | SHA256 | Role |
|------|------|--------|------|
| Theorem doc | `docs/GATE1_SAFE_RELAXATION_THEOREM.md` | `abc123...` | Source |
| Verifier | `src/verify_safe_relaxation_domination.py` | `def456...` | Replay |
| Certificate (if applicable) | `artifacts/exact/safe_relaxation_cert.json` | `ghi789...` | Proof |
| Counterexamples (if any) | `artifacts/counterexamples/safe_relaxation_*.json` | `jkl012...` | Search results |

**All paths must be repository-relative.**

**New files:**
```bash
git diff --name-only HEAD~1 HEAD
```

[Output of git diff showing all new/modified files]

**Verifier command (from theorem):**
```bash
cd /workspace/root
python src/verify_safe_relaxation_domination.py
```

**Verifier output (latest run):**
```
[Full stdout/stderr from verifier; must show PASS or specific failure]
```
```

### 4. **Dependency Closure**
```markdown
## Dependency Audit Checklist

For each dependency listed in the theorem:

- [ ] **Dependency Name:** [Theorem/artifact name]
  - Status: [PROVED_EXACT | PROVED_SYMBOLIC | NUMERICAL_EVIDENCE | OPEN]
  - If OPEN or NUMERICAL_EVIDENCE: Cannot close Gate-1 edge until this is fixed.
  - How used: [Logical role in proof]

All dependencies must be PROVED_EXACT or PROVED_SYMBOLIC for this theorem to be CANDIDATE_EXACT.
If any dependency is OPEN or NUMERICAL_EVIDENCE, this record is BLOCKED_DEPENDENCY instead.
```

### 5. **Known Weak Points & Falsification Targets**
```markdown
## Known Weak Points (Author Self-Report)

**Points the author tried to break:**

1. [Description of potential counterexample or edge case]
   - **Tested:** [How was it tested?]
   - **Result:** [Did it falsify the theorem? If not, why not?]

2. [Another potential weakness]
   - **Tested:** [...]
   - **Result:** [...]

**Remaining unknowns:**
- [Any boundary case not yet tested?]
- [Any assumption that might be wrong?]
- [Any hidden dependence on numerical tolerances?]

**Priority falsification targets for E_referee:**
- [What the author thinks is most fragile]
- [What E_referee should focus on first]
```

### 6. **Reviewer Instructions**
```markdown
## For E_referee Review

**Your task:** Independent replay + adversarial falsification.

**Minimum checklist:**

1. **Verify exact arithmetic:**
   - Run verifier from clean checkout.
   - Confirm all constants are exact rationals (not floating-point approximations).
   - Check for any hidden `float()` or `Decimal` usage that should be `Fraction`.

2. **Verify hash integrity:**
   - Re-compute SHA256 for all artifacts.
   - Confirm they match the record above.
   - If mismatch: The proof has been modified post-generation. Reject.

3. **Check path portability:**
   - Scan all file paths in verifier, certificate, and proof.
   - No `/mnt/data/`, `C:\Users\`, or absolute paths.
   - All paths relative to workspace root.

4. **Falsify the theorem:**
   - Read the author's "weak points" (Section 5).
   - Try to find a counterexample to the main claim.
   - Try to find a counterexample to each sub-lemma.
   - Try edge cases: boundary indices, prime powers, radical substitutions.
   - Try the smallest non-trivial instances.
   - Synthesize adversarial cases that break the assumptions.

5. **Verify dependency closure:**
   - Every dependency must be independently verified (or be PROVED_EXACT).
   - If you find a dependency is actually OPEN or has hidden optimizer status, escalate.

6. **Check proof correctness:**
   - If proof is symbolic, verify each logical step.
   - If proof is a certificate, independently verify its structure (SAT check, Farkas check, CRT verification, etc.).

7. **Update QED_GATES.md if Gate closes:**
   - Only after this theorem is AUDITED and all Gate-1 dependencies are PROVED_EXACT/PROVED_SYMBOLIC.

**If you find a blocker, counterexample, or gap:**
- Move the handoff record to `FAILED/` with a detailed explanation.
- Author must fix and resubmit.

**If review passes:**
- Move to `PASSED/` and update the index.
- Report the status upward for QED-gate closure.
```

### 7. **Audit Log (Added by E_referee)**
```markdown
## Audit Log (Added by E_referee)

### Initial Submission
- **Date:** 2026-08-25T14:32:00Z
- **By:** erdos7-gate1-closer
- **Status:** CANDIDATE_EXACT

### E_referee First Review
- **Date:** [Filled by E_referee]
- **Reviewer:** E_referee
- **Verifier re-run:** [PASS | FAIL | TIMEOUT]
- **Hash check:** [PASS | FAIL]
- **Path check:** [PASS | FAIL]
- **Falsification attempt:** [Found counterexample? Y/N]
- **Dependency verification:** [All PROVED_EXACT/PROVED_SYMBOLIC? Y/N]
- **Status:** [APPROVED | NEEDS_FIX | BLOCKED_DEPENDENCY | BROKEN]
- **Notes:** [Details of any issues found]

### If NEEDS_FIX:
- **Blocker:** [Specific issue]
- **Returned to:** erdos7-gate1-closer
- **Expected fix:** [What needs to be corrected]

### If APPROVED:
- **Final audit sign-off:** [Date, time]
- **Locked at:** [Git commit hash]
- **Can now be used for:** [Which QED-gate edge?]
```

---

## Workflow (Proof-Closer → Queue → E_referee)

### Stage 1: Proof-Closer Submits

1. **Proof-closer completes a theorem** and reaches `PROVED_EXACT` or `PROVED_SYMBOLIC` status.
2. **Creates handoff record** at `coordination/referee_queue/IN/[THEOREM]_[DATE].md`.
3. **Includes all sections above** (1–6).
4. **Runs the verifier locally** and documents full output.
5. **Computes SHA256 for all artifacts.**
6. **Documents weak points** that were tested and any that remain.
7. **Commits and tags the submission:**
   ```bash
   git add coordination/referee_queue/IN/[THEOREM]_[DATE].md
   git commit -m "Handoff: [THEOREM_NAME] to E_referee queue"
   git tag handoff/[THEOREM_NAME]/[DATE]
   ```

### Stage 2: E_referee Reviews

1. **Monitors `coordination/referee_queue/IN/` for new submissions.**
2. **For each submission:**
   - Reads the full handoff record.
   - Moves it to `AUDITING/` to signal active review.
   - Runs the verifier independently.
   - Checks hash integrity, path portability.
   - Attempts falsification (focus on weak points).
   - Verifies all dependencies are PROVED_EXACT or PROVED_SYMBOLIC.
3. **Fills in the Audit Log (Section 7).**
4. **Outcome:**
   - **APPROVED:** Move to `PASSED/`. Theorem can now close a QED-gate edge.
   - **NEEDS_FIX:** Move to `FAILED/`. Document blocker. Return to author.
   - **BLOCKED_DEPENDENCY:** Keep in `IN/` until dependency is proved. Notify author.

### Stage 3: Re-submission (If Needed)

If E_referee marks `NEEDS_FIX`:

1. **Author (proof-closer) fixes the issue.**
2. **Updates the handoff record** with new timestamp and audit details.
3. **Re-runs verifier** and documents new output.
4. **Recomputes all affected SHA256 hashes.**
5. **Re-commits and resubmits** to `coordination/referee_queue/IN/`.
6. **E_referee reviews again** until APPROVED.

---

## Access Control

- **Proof-closer** can write to `IN/` and read from `FAILED/` and `PASSED/`.
- **E_referee** can read from `IN/`, write to `AUDITING/`, `PASSED/`, and `FAILED/`.
- **Query only**: Any agent can query the status of past audits from `PASSED/` and `FAILED/` indexes.

---

## Status Propagation

Only when a theorem is `APPROVED` in the audit queue:

1. **Update the theorem's proof-status label** in its source file (e.g., `docs/GATE1_SAFE_RELAXATION_THEOREM.md`) to `PROVED_EXACT` or `PROVED_SYMBOLIC` (not `CANDIDATE_*`).
2. **Update the dependency list** in any downstream theorems that depend on this result.
3. **Check if any QED-gate edge is now closable** (all dependencies PROVED_EXACT or PROVED_SYMBOLIC).
4. **If a gate closes, update `docs/QED_GATES.md`** accordingly.

---

## Historical Record

The `README.md` in `coordination/referee_queue/` maintains a chronological index:

```markdown
# Referee Audit Queue Index

| Theorem | Author | Submitted | Approved | Status |
|---------|--------|-----------|----------|--------|
| Arbitrary-Depth Domination | erdos7-gate1-closer | 2026-08-25 | 2026-08-26 | AUDITED_EXACT |
| ... | ... | ... | ... | ... |

All historical records archived in `PASSED/` and `FAILED/`.
```

---

## Key Principles

1. **Separation of concerns:** Proof-closer and referee must be distinct roles (different agents or tracked separately).
2. **No self-audit:** Author cannot move their own theorem to `PASSED/`. E_referee must approve.
3. **Exact over convenient:** Optimizer status, floating-point bounds, and numerical evidence do NOT close gates. Only PROVED_EXACT or PROVED_SYMBOLIC (after audit) does.
4. **Reversible:** If a later falsification or audit finds a flaw in a `PASSED/` theorem, it can be moved back to `FAILED/` and the dependent gates are re-opened.
5. **Transparent:** All audits are recorded and time-stamped. The full history is preserved.

---

## Integration with QED_GATES.md

Gates close only when:

1. **All theorem dependencies** required for that gate are in `coordination/referee_queue/PASSED/`.
2. **E_referee has signed off** on the audit (Audit Log complete, status APPROVED).
3. **The gate's requirement statement** (from `docs/QED_GATES.md`) is mathematically satisfied by the proved theorems.
4. **The theorem is updated** to status `PROVED_EXACT` or `PROVED_SYMBOLIC` (not `CANDIDATE_*`).

Until all six gates are closed and audited, the project status remains `OPEN`.
