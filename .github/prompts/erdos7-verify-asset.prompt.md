---
description: "Use when: auditing a proof artifact or theorem for completeness, verifier integrity, and hash validation before E_referee review. Accept artifact path, verify independent reproducibility, hash integrity, exact arithmetic (no optimizer status), and repository portability."
argument-hint: "Path to artifact or theorem file to verify. Examples: 'artifacts/exact/stage18/farkas_cert.json', 'docs/GATE1_SAFE_RELAXATION_THEOREM.md', 'coordination/referee_queue/CARD9_THRESHOLD_PROOF.md'"
---

# Erdős 7 Artifact Verifier

Use this prompt to pre-audit a proof artifact or theorem statement before it enters the E_referee queue.

## Task

Given an artifact or theorem path, I will:

1. **Locate the source derivation** — find the `.py` verifier, proof document, or certificate definition.
2. **Run the independent verifier** — execute any optimizer-free verifier without trusting optimizer status codes.
3. **Verify artifact hashes** — confirm SHA256 matches recorded values; check against artifacts/ registry.
4. **Check repository paths** — ensure all paths are relative, portable, and workspace-scoped (no `/mnt/data/`, `C:\Users\`, or absolute paths).
5. **Confirm exact arithmetic** — verify that claims are backed by exact symbolic/rational proof, not optimizer output or floating-point approximations.
6. **Emit audit status** — output only one of: `AUDITED_EXACT`, `AUDITED_SYMBOLIC`, `BROKEN`, or a precise blocker/gap.

## Input Format

Provide the artifact or theorem path, and optionally:

```
Artifact: artifacts/exact/stage18/farkas_cert_merged.json
or
Theorem: docs/GATE1_SAFE_RELAXATION_THEOREM.md
or
Coordinator handoff: coordination/referee_queue/SAFE_RELAXATION_DOMINATION_2026-08-25.md
```

## Verification Workflow

### Step 1: Locate and Parse

- Find the file at the given path.
- If it's a JSON/Python dict certificate, locate the `.py` verifier referenced in it.
- If it's a `.md` theorem, extract the **Verifier Command** section (required by `exact-proof-template.instructions.md`).
- If it's a referee handoff record, locate the referenced theorem and verifier.

### Step 2: Run Independent Verifier

```bash
cd /workspace/root
python [verifier_path]
```

- **Accept only:** Exit code 0 with verifier-specific success markers.
- **Reject:** Exit code ≠ 0, or timeout (> 60 seconds).
- **Reject strongly:** Any mention of "optimizer status", "LP solver", "Gurobi", "CPLEX", "HiGHS", "SciPy optimize".

### Step 3: Check Artifact Hashes

For each artifact file (.json, .rational, .lp, .py):

```bash
sha256sum [artifact_path]
```

Compare against:
- The SHA256 value recorded in the theorem metadata.
- Any registry file under `artifacts/exact/**.sha256`.

- **PASS:** Hashes match exactly.
- **FAIL:** Hash mismatch → file has been modified after proof generation → `BROKEN`.

### Step 4: Check Repository Paths

Scan all file references in the certificate or theorem:

- **Portable:** All paths start with `.`, `src/`, `artifacts/`, `docs/`, `coordination/`, or `agents/` (relative paths only).
- **NOT portable:** `/mnt/data/`, `C:\Users\`, `/home/user/`, or any absolute path.

- **PASS:** All paths are relative.
- **FAIL:** Any absolute path → reject with error message.

### Step 5: Confirm No Optimizer Status

Scan the entire proof, certificate metadata, and verifier output for:

- Phrases like "optimal value", "solver status", "Gurobi found", "HiGHS terminated", "LP dual feasible", "MIP gap < 0.01", or similar.
- Usage of SciPy `.solve_() status codes` without independent verification.
- Claims like "verified by numerical LP bounds" without an exact verifier.

- **PASS:** Proof is backed by exact symbolic/rational arithmetic, SAT/LRAT/DRAT, combinatorial exhaustion, or CRT reconstruction.
- **FAIL:** Proof relies on optimizer status → `BROKEN`.

### Step 6: Emit Audit Result

Output **exactly one** of the following:

---

#### **`AUDITED_EXACT`**

All steps pass:
- [ ] Verifier runs to completion with exit code 0.
- [ ] All artifact hashes match.
- [ ] All paths are repository-relative.
- [ ] No optimizer status is used as proof.
- [ ] Proof is backed by exact finite computation, SAT/PB, or symbolic derivation.

```
ARTIFACT_PATH: [path]
VERIFIER_COMMAND: [command used to verify]
VERIFIER_STATUS: PASS
HASH_VERIFICATION: PASS
PATHS_VERIFICATION: PASS
OPTIMIZER_DEPENDENCY: NONE
FINAL_STATUS: AUDITED_EXACT

Ready for E_referee independent replay.
```

---

#### **`AUDITED_SYMBOLIC`**

All steps pass except:
- Verifier may not run (symbolic/algebraic proof, not computational).
- Hypotheses are explicit and all dependencies verified.
- No optimizer status is trusted.
- Proof is sound but not independently computable (e.g., a valid CRT reconstruction argument or pure algebraic derivation).

```
ARTIFACT_PATH: [path]
THEOREM_STATEMENT: [formal claim]
HYPOTHESIS_STATUS: ALL_EXPLICIT
DEPENDENCIES_STATUS: VERIFIED
VERIFIER_STATUS: SYMBOLIC_ONLY
HASH_VERIFICATION: PASS (if artifacts present) | N/A (if purely symbolic)
PATHS_VERIFICATION: PASS
OPTIMIZER_DEPENDENCY: NONE
FINAL_STATUS: AUDITED_SYMBOLIC

Hypotheses and proof chain sound. Ready for E_referee adversarial falsification.
```

---

#### **`BROKEN`**

One or more checks fail:

```
ARTIFACT_PATH: [path]
FAILURE_REASON: [exact blocker]
FAILED_STEP: [Which step (1–5) failed]
DETAILS:
  - [Specific error message or mismatch]
  - [Path to problem file if applicable]

RECOVERY_ACTION: [Suggest fix, e.g., "Run verifier from workspace root", "Recompute hash", "Rebuild from source"]

FINAL_STATUS: BROKEN
```

---

#### **`BLOCKED_DEPENDENCY`**

Proof is sound but depends on an unverified theorem or artifact:

```
ARTIFACT_PATH: [path]
BLOCKER_THEOREM: [Name and path of missing proof]
BLOCKER_STATUS: [OPEN | NUMERICAL_EVIDENCE | COUNTEREXAMPLE | ...]
CURRENT_READINESS: [Can run verification once blocker is PROVED_EXACT/PROVED_SYMBOLIC]

NEXT_STEP: Prove/fix [blocker_theorem], then re-run this verifier.

FINAL_STATUS: BLOCKED_DEPENDENCY
```

---

#### **`PRECISE_GAP`**

Proof is nearly sound but has a mathematical gap:

```
ARTIFACT_PATH: [path]
GAP_DESCRIPTION: [Exact description of the logical or mathematical gap]
AFFECTED_SECTION: [Which theorem section or proof step is affected]
SEVERITY: [CRITICAL | MAJOR | MINOR]
FIX_STRATEGY: [How to close the gap]

FINAL_STATUS: PRECISE_GAP
```

---

## Output Format (Exact)

Always output:

1. The final status line: `FINAL_STATUS: [AUDITED_EXACT | AUDITED_SYMBOLIC | BROKEN | BLOCKED_DEPENDENCY | PRECISE_GAP]`
2. Supporting details as above.
3. If status is not `AUDITED_EXACT` or `AUDITED_SYMBOLIC`, include a **recovery action** or **next step**.

---

## Use Cases

### Case 1: Verify a K2 228-case Farkas Certificate

```
Artifact: artifacts/exact/k2/k2_228_case_merged_certificate.json
```

→ Extract verifier: `src/verify_k2_228_farkas.py`  
→ Run: `python src/verify_k2_228_farkas.py` (should complete in < 5 seconds)  
→ Check hash: SHA256 matches recorded value  
→ Check paths: All relative  
→ No optimizer status detected  
→ **Result:** `AUDITED_EXACT`

---

### Case 2: Verify a GATE1_SAFE_RELAXATION_THEOREM (Currently OPEN)

```
Theorem: docs/GATE1_SAFE_RELAXATION_THEOREM.md
```

→ Extract hypothesis list, dependencies, and verifier command  
→ Verifier missing or incomplete  
→ Dependencies include unproved arbitrary-depth domination lemma  
→ **Result:** `BLOCKED_DEPENDENCY` + next step

---

### Case 3: Detect Optimizer Status Creep

```
Artifact: artifacts/current_state/phase_threshold_bound.json
```

→ File claims "phase feasibility infeasible"  
→ Verifier output contains "Gurobi dual bound confirms..."  
→ **Result:** `BROKEN` — optimizer status mistaken for proof; must rebuild with exact certificate.

---

## Notes for E_referee Integration

When a theorem produces `AUDITED_EXACT` or `AUDITED_SYMBOLIC`:

1. Create a handoff record in `coordination/referee_queue/` with full output.
2. E_referee must perform independent replay and adversarial falsification.
3. Only after E_referee signs off can the theorem be used to close a QED-gate edge.

Broken, blocked, or gapped artifacts are returned for fix before re-verification.
