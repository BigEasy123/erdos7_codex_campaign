# Coordinator prompt

Use this in a seventh Codex thread if you want Codex itself to act as campaign coordinator while A–F work independently:

```text
Act as the coordinator for this repository, not as a seventh proof attacker. Read AGENTS.md, docs/QED_GATES.md, coordination/CAMPAIGN.md, and every agents/*/status.json and RESULT.md. Do not overwrite agent work. Maintain coordination/STATUS.json and a new coordination/INTEGRATION.md that records: (1) new claims from each track; (2) dependencies; (3) conflicts; (4) what Track E has independently verified; (5) the single best next task for each track. Never promote a theorem above the weakest dependency status. Never say QED unless every QED_GATES item is closed and referee-audited. If two tracks discover complementary lemmas, write an explicit integration lemma proposal but label it HEURISTIC until proved.
```
