---
created: 2026-03-23
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: resume-recal-post-2136-followup-deepen-gmm-20260323T231800Z
ira_call_index: 1
status: repair_plan
risk_summary: { low: 4, medium: 2, high: 0 }
validator_report_path: .technical/Validator/roadmap-auto-validation-genesis-mythos-master-20260323T231800Z-recal-2136-layer2-first.md
parent_run_id: pr-8c507e1a-4a88-45a0-8a30-f1088ef076e6
tags: [internal-repair-agent, roadmap, genesis-mythos-master, validator-driven, recal-2136, layer2-first]
---

# IRA — genesis-mythos-master — call 1 (post–nested-validator first pass)

## Context

RoadmapSubagent invoked IRA after **nested** `roadmap_handoff_auto` **first pass** for queue **`resume-recal-post-2136-followup-deepen-gmm-20260323T231800Z`** (`ira_after_first_pass: true`). Validator report: **medium** / **`needs_work`** / **`missing_roll_up_gates`** (primary), plus **`missing_task_decomposition`**, **`safety_unknown_gap`**. **Contaminated-report rule:** treat machine gaps as a **floor** — vault truth is **rollup HR 92 < min_handoff_conf 93**, **G-P*.*-REGISTRY-CI HOLD**, **D-044/D-059 operator picks already on decisions-log (2026-03-23)** — **do not fabricate** picks or imply CI/registry clearance from prose. **RECAL** remains **drift refresh / audit**, not handoff.

## Structural discrepancies (expanded minimum)

1. **Rollup / advance semantics:** Validator **`missing_roll_up_gates`** matches vault: secondary rollups stay **HR 92** with **REGISTRY-CI HOLD**; no advance-eligible narrative should appear without repo evidence or a dated policy exception on [[decisions-log]].
2. **Task decomposition mirror:** Phase **3.4.9** Validator **definition-of-done mirror** can remain **unchecked** while **GMM-HYG-01** hygiene is reconciled — the mirror tracks **repo/registry** closure, not checkbox cosmetics alone.
3. **Drift comparability:** [[roadmap-state]] **`drift_metric_kind: qualitative_audit_v0`** + narrative already warn comparability; **`drift_spec_version`** / **`drift_input_hash`** are still **unpublished** — **`safety_unknown_gap`** stays honest until those exist or scalars are explicitly non-comparable in UI tables.
4. **Trace gap:** [[roadmap-state]] **Notes** cite **231500Z** second pass and **221000Z** baseline but do not yet cite this run's **231800Z layer2-first** path as the **first** nested pass that feeds the second-pass anchor — weak cross-audit for Layer-2 ordering.

## Proposed fixes (for Roadmap subagent / operator; apply under snapshots + guardrails)

See structured **`suggested_fixes`** in the parent return payload (stable order).

## Notes for future tuning

- Repeated **`missing_roll_up_gates`** on **honest** **92 < 93** + **REGISTRY-CI HOLD** is expected until VCS; validators should not be trained to downgrade to **`log_only`** when the vault explicitly documents HOLD.
- Publish a **minimal drift spec stub** (version + hash algorithm + inputs list) when you want numeric drift fields to be machine-auditable; until then, keep **qualitative** labeling visible wherever scalars appear.
