---
name: "exact-proof-template"
description: "Use when: creating a new theorem, lemma, certificate, or structural result for the Erdős 7 Gate-1 closure. Every claimed proof must follow this template to ensure exact provenance, machine-readable verification, and audit compliance."
applyTo: "docs/GATE1_*.md, docs/*_THEOREM*.md, artifacts/exact/**.md, coordination/referee_queue/**.md"
---

# Exact Proof Template

Every mathematical theorem, lemma, or exact certificate in the Erdős 7 Gate-1 proof chain must include all sections below.

## Required Sections

### 1. **Theorem Statement**
```markdown
## Theorem: [Formal name]

**Claim:** [Exact mathematical statement in symbolic notation]

**Scope:** [Precisely which objects/states/families this applies to]

**Strength:** [PROVED_EXACT | PROVED_SYMBOLIC | NUMERICAL_EVIDENCE | COUNTEREXAMPLE | OPEN]
```

**Why:** The theorem statement must be exact and unambiguous. No informal "roughly we prove X" phrasing.

---

### 2. **Explicit Hypothesis List**
```markdown
## Hypotheses

1. **Hypothesis A:** [Precise statement]
   - Source: [Where this comes from: combinatorial derivation, prior theorem, exact computation]
   - Verified: [Yes/No, with justification]

2. **Hypothesis B:** [Precise statement]
   - Source: [...]
   - Verified: [...]

...
```

**Why:** Every claim must state what it assumes. No silent assumptions. Every hypothesis must be traceable to exact source or prior verified result.

---

### 3. **Imported Dependencies**
```markdown
## Dependencies

- **Theorem/Lemma X:** [Full citation or path to artifact]
  - Status: [PROVED_EXACT | PROVED_SYMBOLIC | NUMERICAL_EVIDENCE]
  - How used: [Briefly explain the logical role]
  
- **Exact constant C₁:** [Value with full precision]
  - Source: [Exact derivation or computation]
  - Artifact: [Path to rational or symbolic form]
  - Verification: [Verifier command to reproduce]

- **Stage-18 certificate:** [SHA256 or path]
  - Replay status: [PASS | BLOCKED | UNKNOWN]
```

**Why:** Establishes the proof's dependency graph. Every dependency must itself be verified or marked as OPEN. Circular dependencies are forbidden.

---

### 4. **Proof / Certificate**
```markdown
## Proof / Certificate Construction

**Route:** [SAT | Farkas | PB | Exhaustive | Symbolic/Algebraic | CRT | Other]

**Proof sketch:**
1. [High-level logical step]
2. [Next step]
3. ...

**Key lemmas / sub-certifications:**
- [Sub-result 1]: [Justification]
- [Sub-result 2]: [Justification]

**Certificate representation:**
- **Format:** [Python dict | JSON | .lp file | SymPy expression | Rational coefficients | Other]
- **Location:** [Workspace-relative path]
- **Size:** [# of variables, # of constraints, # of proof lines, etc.]
```

**Why:** Makes the proof inspectable. SAT/PB/Farkas certificates must be formatted for independent verification. Symbolic proofs must show the algebraic chain. No opaque "optimizer said yes" claims.

---

### 5. **Scope Limitations**
```markdown
## Scope and Limitations

- **Applies to:** [Exact set of objects: e.g., "all arbitrary-depth continuations of state 2275", "all 9-element subsets of {1..331}"]
- **Does NOT apply to:** [Any exclusions or boundary cases]
- **Precision requirements:** [e.g., "all coefficients exact rationals", "CRT reconstruction required for primes > 73"]
- **Known restrictions:** [Timeout limits, numerical thresholds, assumed lemmas not yet proved, etc.]
```

**Why:** Prevents silent scope creep. If a theorem has a boundary or a restriction, it must be explicit.

---

### 6. **Repeated-Power Audit**
```markdown
## Repeated-Power and Radical Treatment

- **Prime p^k handling:** [For each repeated power in use, e.g., "3^2, 5^2, 7^2, 11^2"]
  - **Claim:** [How repeated power is treated or why it matters]
  - **Justification:** [Theorem or computation that covers it]
  - **Counterexample search:** [Yes/No; if Yes, results]

- **Radical substitution:** [Did we replace p^k by p anywhere? If yes, why is it safe?]

- **Prime tower interactions:** [Are there any subtle interactions between repeated primes? If yes, documented where?]
```

**Why:** Repeated primes are a source of subtle bugs in tower and residue reasoning. This section enforces explicit handling.

---

### 7. **Verifier Command**
```markdown
## Independent Verification

**Optimizer-free verifier:**
```bash
cd /path/to/erdos7_codex_campaign
python src/verify_[theorem_name].py
```

**Expected output:**
```
[RESULT_NAME]=PASS
REASON=...
```

**Constraints:**
- No SciPy LP solver.
- No HiGHS / CPLEX / Gurobi status codes.
- Relies on: [SymPy | cddlib | VeriPB | exhaustive replay | rational arithmetic only]

**Verifier source:**
- Location: [Path to `.py` verifier script]
- Language: [Python 3.x, requires: ...]
- Runtime: [Typical duration, memory, timeout]

**Latest run:**
```
[Full output or stdout/stderr from last execution]
```
```

**Why:** The verifier must run independently. If it fails, the theorem fails. Status codes from optimizers are NOT verifiers.

---

### 8. **Artifact Hash**
```markdown
## Artifacts and Integrity

| Artifact | Path | SHA256 | Verified |
|----------|------|--------|----------|
| [Name] | `artifacts/exact/.../file.json` | `abc123...` | PASS / FAIL |
| [Certificate] | `artifacts/exact/.../cert.rational` | `def456...` | PASS / FAIL |
| [Verifier] | `src/verify_*.py` | `ghi789...` | PASS / FAIL |

**Verification command:**
```bash
sha256sum artifacts/exact/.../file.json
```

**All paths must be repository-relative and portable.** No absolute paths like `/mnt/data/...` or `C:\Users\...`.
```

**Why:** Ensures artifact integrity across machines and time. SHA256 binds the proof to exact data.

---

### 9. **Proof-Status Label**
```markdown
## Current Status

**Status:** PROVED_EXACT | PROVED_SYMBOLIC | NUMERICAL_EVIDENCE | COUNTEREXAMPLE | KILLED | OPEN | BLOCKED_DEPENDENCY

**Interpretation:**
- `PROVED_EXACT`: Finite, reproducible, optimizer-free verifier passes. All dependencies are PROVED_EXACT or PROVED_SYMBOLIC.
- `PROVED_SYMBOLIC`: Valid symbolic/algebraic proof with explicit hypotheses. All dependencies verified or stated. Counterexamples actively searched and none found.
- `NUMERICAL_EVIDENCE`: Optimizer output or numerical approximation only. NOT a theorem. Does not count toward QED gates.
- `COUNTEREXAMPLE`: A falsifying witness exists. Proof is wrong or incomplete.
- `KILLED`: Route was exhaustively explored and abandoned. Documented in `docs/DEAD_ENDS.md`.
- `OPEN`: Unresolved. State the blocker clearly.
- `BLOCKED_DEPENDENCY`: Depends on another theorem/artifact that is not yet PROVED_EXACT or PROVED_SYMBOLIC.

**If blocked or open:**
```markdown
**Blocker:** [Precise statement of what is missing]
**Next step:** [Exact theorem or computation needed to unblock]
**Alternate routes:** [Other approaches or pivot strategies]
```
```

**Why:** Enforces honest status tracking. The cascade to Gate-1 closure requires all steps to be PROVED_EXACT or PROVED_SYMBOLIC, not NUMERICAL_EVIDENCE.

---

## Checklist Before Submission

- [ ] Theorem statement is exact and unambiguous.
- [ ] All hypotheses are explicit and sources traced.
- [ ] All dependencies listed with their status.
- [ ] Proof/certificate is detailed enough to audit.
- [ ] Scope limitations are clearly stated.
- [ ] Repeated powers and radical substitutions are handled explicitly.
- [ ] Independent verifier exists and runs without optimizer output.
- [ ] All artifacts have SHA256 hashes; all paths are repository-relative.
- [ ] Status label is honest and justified.
- [ ] If PROVED_SYMBOLIC, counterexamples have been actively searched.
- [ ] If blocked, the exact blocker and next step are documented.
- [ ] File is ready for E_referee audit queue.

---

## Example: Stubs for Real Theorems

### Example 1: Exact Stage-18 Farkas Certificate
```markdown
## Theorem: Stage-18 Surplus Downset Contradictions

**Claim:** All 12 divisor-closed surplus downsets in the shallow low-four box have exact rational Farkas contradictions.

**Status:** PROVED_EXACT

...
[Full sections 1–9 as above]
...
```

### Example 2: Child-Pooled Model Domination (Currently OPEN)
```markdown
## Theorem: Arbitrary-Depth Child-Pooled Domination [GATE1_SAFE_RELAXATION_THEOREM.md]

**Claim:** For every legal arbitrary-depth continuation (Ω, s, d) of state 2275, the feasible set is strictly contained in the child-pooled relaxation.

**Status:** OPEN

**Blocker:** Exact coefficients for deep-3 pooling and tail unification not yet reconstructed from source.

**Next step:** Rebuild exact rational coefficients from CRT + prime-power descent; then prove domination symbolically.

...
```

---

## Coordination with E_referee

When a theorem reaches `PROVED_EXACT` or `PROVED_SYMBOLIC`, create a handoff record under `coordination/referee_queue/` (see `E_REFEREE_HANDOFF_PROTOCOL.md`). The referee must independently verify all sections before the theorem can be used to close a QED-gate edge.
