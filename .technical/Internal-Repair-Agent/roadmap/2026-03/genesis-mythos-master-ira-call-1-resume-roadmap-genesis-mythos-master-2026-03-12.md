---
created: 2026-03-19
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: resume-roadmap-genesis-mythos-master-2026-03-12
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 4
  medium: 0
  high: 0
---

## Context

IRA invoked from validator-driven branch for a `RESUME_ROADMAP` deepen cycle after hostile validation returned `recommended_action: needs_work` with reason codes: missing port signatures, command/event schema incompleteness, missing executable decomposition, and unresolved state-hygiene lineage context.

## Structural discrepancies

1. `phase-1-1-core-architecture-contracts-roadmap-2026-03-19-0001.md` contains intent-level objectives but no concrete seam signatures (input/output types and invariants) required for handoff-grade contracts.
2. `command-event-schema-v0.md` has list-style payloads but lacks tabular v0 contract fields for versioning, ordering/idempotency keys, and explicit producer/consumer ownership mappings.
3. `phase-1-decomposition-sheet-v0.md` defines boundaries and gates but does not provide an ordered, executable task list with acceptance checks for subphase `1.1`, including deterministic replay harness work.
4. `workflow_state.md` lineage is stale (`last_auto_iteration` still points to older queue id), while `roadmap-state.md` still carries a warning callout without an explicit closure linkage to the state-hygiene closeout note.

## Proposed fixes

1. **Add interface-signature contracts section for Phase 1.1 seams**
   - `action_type`: `adjust_frontmatter`
   - `target_path`: `1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-and-Core-Architecture/phase-1-1-core-architecture-contracts-roadmap-2026-03-19-0001.md`
   - `risk_level`: `low`
   - `description`: Add a `## Contract signatures (v0)` section with one concrete signature per seam (`simulation`, `generation`, `render publish`, `input ingest`, `snapshot/restore`), each with deterministic invariants (ordering, immutability boundaries, seed/stability guarantees).
   - `constraints`: Apply as additive markdown section only; do not alter existing frontmatter keys or remove current objective bullets.

2. **Normalize command/event schema into explicit v0 payload tables**
   - `action_type`: `recompute_phase_metadata`
   - `target_path`: `1-Projects/genesis-mythos-master/Roadmap/command-event-schema-v0.md`
   - `risk_level`: `low`
   - `description`: Replace bullet payload blocks with two markdown tables (`Commands v0`, `Events v0`) containing required fields: `message_name`, `version`, `payload_fields`, `ordering_key`, `idempotency_key`, `producer`, `consumer`, `failure_semantics`.
   - `constraints`: Preserve existing message names; additive/transformational content edit only, no file move/rename.

3. **Add executable subphase 1.1 task decomposition**
   - `action_type`: `write_log_entry`
   - `target_path`: `1-Projects/genesis-mythos-master/Roadmap/phase-1-decomposition-sheet-v0.md`
   - `risk_level`: `low`
   - `description`: Append `## Subphase 1.1 executable task plan (v0)` with at least 6 ordered tasks; each task includes owner boundary, deliverable artifact path, and acceptance check. Include one dedicated deterministic replay harness task with checksum validation criterion.
   - `constraints`: Keep existing boundaries and roll-up gates intact; new section should not invalidate current links in `decisions-log.md`.

4. **Reconcile workflow lineage and close duplicate-state warning context**
   - `action_type`: `mark_snapshot_link`
   - `target_path`: `1-Projects/genesis-mythos-master/Roadmap/workflow_state.md`
   - `risk_level`: `low`
   - `description`: Update `last_auto_iteration` to the current deepen queue lineage id for this run and append one new log row noting state-hygiene reconciliation event.
   - `constraints`: Edit only frontmatter lineage fields plus a single append row in the canonical first `## Log` table; preserve existing rows.
   - `secondary_target_path`: `1-Projects/genesis-mythos-master/Roadmap/roadmap-state.md`
   - `secondary_description`: Under `## Consistency reports (RECAL-ROAD)`, add a closeout bullet that links `[[state-hygiene-closeout-2026-03-19]]` and marks the duplicate-state warning as resolved (or explicitly still-open with owner + next check date).

## Notes for future tuning

- Recurrent pattern: roadmap deepen outputs at secondary level are often conceptually rich but lack machine-checkable interface/schema artifacts.
- Add a pre-handoff checklist hook that auto-prompts for v0 signatures + schema tables before confidence can exceed 85 for Phase 1 subphases.
