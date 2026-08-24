# Launching the six Codex tracks

Open this repository as one Codex project. Run the six tasks in separate threads/worktrees so they can proceed independently. The root `AGENTS.md` supplies persistent proof-discipline rules; each prompt below delegates the mathematical mission to the corresponding `BRIEF.md`.

## Thread A — CARD9

```text
You are Track A. Read AGENTS.md, docs/CURRENT_FRONTIER.md, docs/QED_GATES.md, coordination/PROOF_STATUS.md, and agents/A_card9/BRIEF.md. Work only on the CARD9 exact finite-certificate mission. First make the active scripts repository-relative and validate/reconstruct any missing helper against saved checkpoint outputs. Then pursue the brief until you either obtain an exact closure certificate, a genuine phase-feasible 9-packet, a counterexample, or a clearly documented blocker. Do not stop at solver evidence. Write all conclusions to agents/A_card9/RESULT.md and status.json, with restartable artifacts and verifier scripts.
```

## Thread B — structural concentration

```text
You are Track B. Read AGENTS.md, docs/CURRENT_FRONTIER.md, docs/QED_GATES.md, coordination/PROOF_STATUS.md, and agents/B_structure/BRIEF.md. Independently attack the slab/concentration geometry of the near-extremal 9-parent packets. Do not merely extend Track A's Benders enumeration. Search for counterexamples before promoting a lemma. Produce a symbolic proof or exact finite structural reduction if possible. Record everything in agents/B_structure/RESULT.md and status.json.
```

## Thread C — common-U / blocker descent

```text
You are Track C. Read AGENTS.md, docs/CURRENT_FRONTIER.md, docs/QED_GATES.md, coordination/PROOF_STATUS.md, and agents/C_commonU/BRIEF.md. Audit the exact 284-case common-U theorem and attack the repeated-power triangle/blocker/pivot bridge, especially types 84–90 / radical mask 0x7f. Do not equate same radical with same modulus. Seek a rigorous arbitrary-depth descent, a small exact packet certificate, or a counterexample. Record results in agents/C_commonU/RESULT.md and status.json.
```

## Thread D — HN/BBMST bridge

```text
You are Track D. Read AGENTS.md, docs/CURRENT_FRONTIER.md, docs/DEAD_ENDS.md, docs/QED_GATES.md, coordination/PROOF_STATUS.md, and agents/D_HN_BBMST/BRIEF.md. Independently derive a correlated survivor-dispersion inequality or BBMST/HN dichotomy that handles repeated powers. Avoid the recorded independent-tower inflation and naive averaging failures. If you use literature, identify exact theorem hypotheses. Record all constants, proofs, counterexamples, and status in agents/D_HN_BBMST/RESULT.md and status.json.
```

## Thread E — referee

```text
You are Track E, the adversarial referee. Read AGENTS.md, docs/CURRENT_FRONTIER.md, docs/QED_GATES.md, docs/DEAD_ENDS.md, coordination/PROOF_STATUS.md, and agents/E_referee/BRIEF.md. First independently replay the immutable exact certificates and audit the 284 common-U semantics, CARD9 relaxation direction, and 42 symmetries. Then review outputs from A–D as they appear. Try to falsify every promoted lemma. Never upgrade status without independent evidence. Maintain agents/E_referee/RESULT.md and status.json.
```

## Thread F — global interface

```text
You are Track F. Read AGENTS.md, docs/CURRENT_FRONTIER.md, docs/QED_GATES.md, coordination/PROOF_STATUS.md, and agents/F_global_interface/BRIEF.md. Work ahead on the post-state-2275 proof: prove or sharply reduce the lift to all 7,637 canonical states and audit the 13–73 / >73 HN-BBMST interface with repeated powers. Do not assume state2275 tower extremality implies concentration extremality. Produce a dependency map and close any edges you can. Record results in agents/F_global_interface/RESULT.md and status.json.
```

## Coordinator merge rule

Do not merge a headline theorem just because two agents agree. A result should be promoted only after Track E reproduces/audits it and its status meets the evidence standard in `coordination/PROOF_STATUS.md`.
