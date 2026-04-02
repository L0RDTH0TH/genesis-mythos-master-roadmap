---
created: 2026-03-30
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: resume-gmm-deepen-glue-primary-20260330T201500Z
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 4
  medium: 2
  high: 0
validator_report_path: 3-Resources/Second-Brain/Validator-Reports/roadmap_handoff_auto/genesis-mythos-master-20260330T213500Z-conceptual-v1-glue-primary.md
---

# IRA report — genesis-mythos-master (call 1)

## Context

Post–first-pass `roadmap_handoff_auto` (`conceptual_v1`) returned **`needs_work` / medium** with **`missing_roll_up_gates`** (primary) and **`safety_unknown_gap`**. State alignment (roadmap-state, workflow_state last row, decisions-log for glue deepen) is **good**. The open issues are: (1) absence of execution-track rollup/CI/registry proof — **expected and already labeled execution-deferred** in the Phase 1 primary note, but not echoed in rollup surfaces; (2) **ambiguous `progress: 44`** in the Phase 1 primary note versus prose saying “primary checklist **complete**”; (3) **two open TBDs** (DM merge policy, DAG vs cycles) still floating without stable IDs or a single deferred-decision locus. **Invoked with `ira_after_first_pass: true` (validator branch B).** Per operator guidance: treat execution rollup/CI gaps as **advisory** on conceptual track — prefer **prose labeling** and **execution-deferred** pointers, **not** RECAL loops or fake CI artifacts.

## Structural discrepancies

1. **`missing_roll_up_gates`:** Validator correctly flags missing HR/rollup/registry/CI rows; the Phase 1 primary note already defers these in prose, but **roadmap-state** / **distilled-core** do not state that conceptual design authority **does not** claim those closures.
2. **`safety_unknown_gap`:** `progress: 44` + “complete” in the same note trips hostile consistency checks; Progress semantics paragraph also admits a **scale tension** (44 vs “50+ = secondaries substantially drafted”).
3. **Floating TBDs:** Edge cases / Open questions list unresolved policies without **stable IDs** or a single “execution-track” anchor (even a placeholder path).

## Proposed fixes (for RoadmapSubagent to apply)

See structured `suggested_fixes` in the parent return payload; apply in **low → medium → high** order after snapshots and track gates.

## Notes for future tuning

- When a phase note uses a **custom `progress` scale**, pair it with an explicit **`progress_scale_id`** or **`primary_checklist_status`** in frontmatter so automated validators and Dataview do not infer “complete” from grep alone.
- On **conceptual_v1**, consider treating `missing_roll_up_gates` as **silent** when `effective_track: conceptual` **and** at least one rollup surface (roadmap-state or distilled-core) **explicitly waives** execution rollup for design authority.
