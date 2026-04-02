---
created: 2026-03-30
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: empty-bootstrap-20260330T130315Z
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 2
  medium: 0
  high: 0
---

## Context

IRA invoked after nested validator reported advisory conceptual-track gaps (`missing_roll_up_gates`, `safety_unknown_gap`) for `RESUME_ROADMAP` on `2.4.5`. This plan is execution-deferred only and avoids changing conceptual authority or forcing execution-track closure.

## Structural discrepancies

1. `decisions-log.md` has many deferred decision rows, but no explicit `2.4.5` decision-anchor row tying this slice to concrete downstream execution deferment IDs with ownership boundaries.
2. The `2.4.5` phase note includes execution-deferred open questions, but lacks a concrete handoff appendix enumerating required execution artifacts with owner lane and completion signal.

## Proposed fixes

1. **id:** `fix-01-245-decision-anchor-row`
   - **target_path:** `1-Projects/genesis-mythos-master/Roadmap/decisions-log.md`
   - **change_summary:** Add one grep-stable decision-anchor row for `2.4.5` that references queue entry `empty-bootstrap-20260330T130315Z`, introduces explicit execution deferment IDs, and records replay/audit ownership boundaries.
   - **risk_level:** `low`
   - **patch_hint:** Add under `## Decisions` a single bullet like `D-2.4.5-execution-deferred-handoff-anchor` with fields: `deferment_ids`, `owner_lane`, `carry_forward_targets`, `queue_ref`.
   - **constraints:** Keep wording advisory; do not claim execution closure; do not alter conceptual-track waiver semantics.

2. **id:** `fix-02-245-exec-deferred-appendix`
   - **target_path:** `1-Projects/genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building/Phase-2-4-Post-Validation-Commit-Orchestration/Phase-2-4-5-Commit-Decision-Finalization-Replay-Safety-and-Audit-Handoff-Roadmap-2026-03-31-0345.md`
   - **change_summary:** Add an `Execution-deferred handoff appendix` section listing exact required artifacts (`finalization schema`, `retention policy`, `validator compare payload table`) with owner lane and completion signal per item.
   - **risk_level:** `low`
   - **patch_hint:** Append a compact table with columns: `artifact_name | owner_lane | completion_signal | linked_deferment_id`; reference IDs from fix-01.
   - **constraints:** Additive only; keep current conceptual NL contracts unchanged; avoid implementation details or execution commitments.

## Notes for future tuning

- Validator next-artifact requests are recurring for conceptual slices near closure; consider a reusable "execution-deferred appendix" template for tertiary `2.x.5` finalization notes.
- Decision-anchor consistency could be auto-checked by little val for `reason_code: missing_roll_up_gates` on conceptual track to reduce repeat medium advisories.
