---
created: 2026-03-19
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: resume-roadmap-genesis-mythos-master-2026-03-19-114230-next-next-next-next-next
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 4
  medium: 0
  high: 0
---

## Context

IRA call 1 for `RESUME_ROADMAP` (project `genesis-mythos-master`) after validator returned `needs_work` for missing flow, schema, and safety/handoff artifacts.

## Structural discrepancies

1. Missing worked end-to-end message flow with deterministic branch outputs.
2. Command/event schemas missing requiredness, constraints, and canonical reason-code enum contract.
3. No risk register linked to Q1-Q4 test labels in the active 1.1.6 note.
4. Decisions log lacks explicit entries linking this deepen step to concrete rationale.

## Proposed fixes

1. Add deterministic E2E message-flow example with concrete payloads and expected reason-code outcomes.
2. Expand command/event schema block with field constraints, required flags, and canonical reason-code semantics.
3. Add risk register v0 (3+ rows) with mitigations and Q1-Q4 mapping.
4. Add explicit decision-log entries for 1.1.6 and backlink to the phase note.

## Notes for future tuning

- Add a fixed "handoff package" section to roadmap-deepen output for tertiary depth: flow example, enum contract, risk matrix, and decision IDs.
