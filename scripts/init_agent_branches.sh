#!/usr/bin/env bash
set -euo pipefail
for b in agent-a-card9 agent-b-structure agent-c-commonu agent-d-hn-bbmst agent-e-referee agent-f-global-interface; do
  git show-ref --verify --quiet "refs/heads/$b" || git branch "$b" main
done
git branch --list 'agent-*'
