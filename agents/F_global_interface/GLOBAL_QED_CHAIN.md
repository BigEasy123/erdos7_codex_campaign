# Global QED dependency chain

## Node graph

least counterexample
-> consecutive odd prime support
-> low-prime canonical family
-> local state theorem
-> all-state lift
-> 13–73 stage
-> >73 termination
-> contradiction

## Edge classification

- least counterexample -> consecutive odd prime support : OPEN
  - The least-counterexample setup is conceptually sound, but the repository does not contain a closed proof that every valid odd distinct cover reduces to the exact prime support family used here.

- consecutive odd prime support -> low-prime canonical family : NUMERICAL_ONLY
  - The canonical state family is well-defined, but the exact reduction statements are not yet closed in the repo.

- low-prime canonical family -> local state theorem : OPEN
  - The local state-2275 obstruction is a strong finite target, but it still requires exact theorem proof rather than numerical evidence.

- local state theorem -> all-state lift : OPEN
  - This is explicitly treated as a separate gate in docs/QED_GATES.md. It remains open and unproved.

- all-state lift -> 13–73 stage : OPEN
  - No exact theorem in the repo settles the full canonical lift before the finite-prime interface.

- 13–73 stage -> >73 termination : OPEN
  - The handoff to published high-prime theory is not yet mapped with exact hypotheses and exact arithmetic verification.

- >73 termination -> contradiction : OPEN
  - The final contradiction is not established; it depends on a valid exact plug-in from the earlier stages.

## Current verdict

The chain is not closed. The repository contains exact local replays and strong numerical evidence, but the dependency edges needed to reach the final contradiction remain open or broken.

The project must not claim QED unless every edge is at least EXACT or PROVED_SYMBOLIC and independently audited.
