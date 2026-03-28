---
created: 2026-03-19
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: resume-roadmap-genesis-mythos-master-2026-03-19-114230-next-next-next
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 3
  medium: 0
  high: 0
---

## Context

IRA invoked from validator-driven branch after a `roadmap_handoff_auto` report returned `severity: medium`, `recommended_action: needs_work`, and reason codes `missing_message_flow_example`, `missing_command_event_schemas`, and `safety_unknown_gap`.

## Structural discrepancies

1. No explicit end-to-end rollback message flow example with success/failure branching.
2. No concrete command/event schema stubs for snapshot/anchor/restore/prune operations.
3. No explicit decision-log anchors in phase constraints mapped to concrete decision IDs.

## Proposed fixes

1. Add one insert-only section for rollback message flow (request -> validate -> anchor check -> lineage verify -> restore|prevent).
2. Add one insert-only section with schema stubs for command/event payloads and deterministic reason codes.
3. Add decision anchor mapping in the phase note and append missing decision IDs in decisions-log.

## Notes for future tuning

- Add a tertiary-level artifact completeness checklist (flow + schemas + decision anchors) to roadmap-deepen output templates.
