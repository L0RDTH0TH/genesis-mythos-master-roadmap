---
created: 2026-03-24
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: operator-deepen-phase3-3-1-rollup-gmm-20260323T233237Z
ira_call_index: 1
status: repair_plan
risk_summary: { low: 1, medium: 4, high: 0 }
validator_report_path: .technical/Validator/roadmap-auto-validation-20260324T000530Z-gmm-operator-3317-first.md
parent_run_id: cc7122e6-5bd0-4aa7-b653-5eb610893651
---

# IRA call 1 — genesis-mythos-master — state hygiene (roadmap-state vs workflow_state)

## Context

Post–nested-validator cycle (`ira_after_first_pass: true`). Validator reported **high** / **block_destructive** with **primary_code** `state_hygiene_failure`: **`1-Projects/genesis-mythos-master/Roadmap/roadmap-state.md`** frontmatter and Phase summaries still describe **macro Phase 3 live / Phase 4 pending** (`current_phase: 3`, `completed_phases: [1, 2]`) while **`1-Projects/genesis-mythos-master/Roadmap/workflow_state.md`** declares **`current_phase: 4`**, **`current_subphase_index: "4"`**, and **`## Log`** rows **`advance-phase`** to **Phase-4-Perspective-Split-and-Control-Systems** (queues **`resume-advance-phase4-operator-gmm-20260323T232553Z`**, **D-062** in [[decisions-log]]). Rollup note **3.1.7** has **`roadmap-level: tertiary`** despite secondary-closure rollup semantics.

## Structural discrepancies

1. **Dual macro phase:** `roadmap-state` YAML vs `workflow_state` YAML.
2. **Narrative contradiction:** Phase summary bullets and Notes (e.g. “canonical macro phase is **3** per frontmatter” ~line 126) vs operator advance already logged in `workflow_state`.
3. **Altitude:** `phase-3-1-7-…-0122.md` `roadmap-level: tertiary` vs rollup / closure inventory role.

## Proposed fixes

See structured return in parent chat (`suggested_fixes` JSON-like list). Apply in **low → medium** order per RoadmapSubagent contract; **snapshot roadmap-state** (and rollup note) before edits. **Do not** add fabricated **D-044** / **D-059** rows; **D-062** already documents the Phase 3→4 advance trace — cite only.

## Notes for future tuning

- After **operator advance-phase**, a **recal** or other state write can **overwrite** a prior Layer-1 `roadmap-state` sync; add a **post-recal checklist** item: “If `workflow_state.current_phase` > `roadmap-state.current_phase`, reconcile YAML in the same run or next hygiene pass.”
- **Retroactive deepen** on a lower subphase while `current_subphase_index` reflects macro Phase 4 increases validator confusion; machine authority string is already `workflow_log_authority: last_table_row` — **roadmap-state** “Latest deepen” bullets should defer to **`last_auto_iteration`** when they disagree.
