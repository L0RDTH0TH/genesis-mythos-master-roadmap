---
created: 2026-04-09
pipeline: roadmap
project_id: godot-genesis-mythos-master
queue_entry_id: followup-deepen-exec-phase1-3-instrumentation-harness-stub-godot-gmm-20260409T010000Z
ira_call_index: 1
parent_run_id: eatq-godot-layer1-20260409T120000Z
pipeline_task_correlation_id: f4e8a2c1-9b3d-4e7f-a1c2-0d6e9b8a7f5e
status: repair_plan
risk_summary:
  low: 2
  medium: 2
  high: 0
validator_report_path: .technical/Validator/roadmap-auto-validation-godot-exec-orch-pass1-f4e8-20260409.md
---

# IRA report — roadmap / RESUME_ROADMAP (validator pass 1 → IRA)

## Context

RoadmapSubagent invoked IRA after nested **`roadmap_handoff_auto`** pass 1 with **`recommended_action: needs_work`**, **`primary_code: safety_unknown_gap`**, and **`reason_codes: safety_unknown_gap, state_hygiene_failure`**. Material cursor alignment (frontmatter **`current_subphase_index: "1.4"`**, repair row **2026-04-09 20:05**) is consistent; remaining gaps are **audit-field hygiene** on the **2026-04-09 18:30** deepen row, **spine prose** for parent **`progress`** rollup vs **1.4** child, and **nested Task ledger** closure (**`nested_Task_host: not_exposed_ledger_task_error`**).

## Structural discrepancies

1. **`state_hygiene_failure`:** ## Log row **2026-04-09 18:30** embeds **`parent_run_id: eatq-godot-layer1-20260407T012000Z`**, which does not match the **2026-04-09** Layer 1 family (**`eatq-godot-layer1-20260409T120000Z`**) documented on the **2026-04-09 20:05** repair row and this hand-off. Idempotent **`queue_entry_id`** reuse is fine; **`parent_run_id`** must be single-clock auditable unless explicitly superseded.

2. **`safety_unknown_gap` (spine):** § **Execution progress semantics** narrows child slices to **`1.1`–`1.3`** while § **Execution child slices** lists **1.4** as a first-class child — hostile readers cannot tell if **`max(progress)`** on the parent includes **1.4**.

3. **`safety_unknown_gap` (nested Task):** The **18:30** row ends with **`nested_Task_host: not_exposed_ledger_task_error`** without a matching **repair/supersession** row proving nested Validator **`Task`** outcome for correlation **`5357d6c4-7edb-4439-89f6-36f0ca1e8d6e`** (per decisions-log cite) or verbatim **`task_error` / `host_error_raw`** per Nested-Subagent-Ledger-Spec.

## Proposed fixes

See structured **`suggested_fixes`** in the caller return payload (same content as below).

## Notes for future tuning

- **Idempotent re-dispatch:** When the same **`queue_entry_id`** spans multiple calendar days, template log rows should default **`parent_run_id`** from the **current** Layer 1 hand-off unless a deliberate **`ledger_only: true`** / historical stamp is documented.
- **Spine templates:** Prefer **“child slices listed under § Execution child slices”** over hard-coded numeric ranges to avoid ellipsis drift when **`1.x`** grows.
- **Strict micro_workflow:** Any **`not_exposed_ledger_task_error`** should be paired in the **same run** or the next **repair** row with either success attestation or explicit **`task_error`** text — avoid “failure-class token only.”
