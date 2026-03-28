---
title: Phase 1.4.2 — Dry-Run Validation
roadmap-level: tertiary
phase-number: 1
subphase-index: "1.4.2"
project-id: genesis-mythos-master
status: archived
priority: high
progress: 0
created: 2026-03-09
tags: [roadmap, genesis-mythos-master, phase, subphase]
para-type: Archive
links:
  - "[[Phase-1-4-Safety-Invariants-Roadmap-2026-03-09-0110]]"
---

## Phase 1.4.2 — Dry-Run Validation

Define dry-run validation before commit: estimate performance and rule validity; no world write until pass (per master goal: "Dry-run passes estimate performance & rule validity before commit").

### Interface sketch

- **Input**: Seed + overrides + intent graph snapshot; pipeline stage checkpoint; optional rule-set id.
- **Output**: Pass/fail; estimated metrics (e.g. tick budget, memory hint); list of rule violations or warnings.
- **Contract**: No persistent world/region write until dry-run returns pass for that scope.

### Tasks

- [ ] Define **when to run dry-run**: before first world write for a run; before region re-generation; optionally on explicit user "validate" action.
- [ ] Define **performance estimate**: lightweight tick or step budget; memory/entity count caps; report as structured payload (no side effects).
- [ ] Define **rule validity check**: run rule engine in read-only mode over proposed state; return violations and severity (block vs warn).
- [ ] Document **rollback semantics**: if dry-run fails, no commit; state remains at last snapshot; user/agent can fix inputs and re-run.
