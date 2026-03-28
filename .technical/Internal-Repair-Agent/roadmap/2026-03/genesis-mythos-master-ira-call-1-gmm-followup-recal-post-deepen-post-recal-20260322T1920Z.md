---
created: 2026-03-22
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: gmm-followup-recal-post-deepen-post-recal-20260322T1920Z
parent_run_id: l1-eat-20260322-gmm-recal-7f3a
ira_call_index: 1
status: repair_plan
risk_summary: { low: 3, medium: 5, high: 1 }
validator_report_path: .technical/Validator/roadmap-auto-validation-20260322T194530Z-gmm-recal-followup.md
reason_codes: [missing_roll_up_gates, safety_unknown_gap]
---

# IRA report — genesis-mythos-master (validator first pass)

## Context

Post–RESUME_ROADMAP recal for queue entry gmm-followup-recal-post-deepen-post-recal-20260322T1920Z (parent_run_id l1-eat-20260322-gmm-recal-7f3a): nested roadmap_handoff_auto returned medium / needs_work with primary_code missing_roll_up_gates and safety_unknown_gap. Validator text is treated as a weak minimum (likely under-reporting): cross-phase HOLD rows, HR 92 vs 93 gating, D-044/D-059 openness, and qualitative drift scalars are all material until operator + vault evidence close them.

## Structural discrepancies (expanded)

1. Roll-up advance gates: Authoritative secondaries 3.2.4, 3.3.4, 3.4.4 carry rollup handoff_readiness 92 with explicit HOLD rows tied to D-044 (RegenLaneTotalOrder_v0 A/B) and registry/CI materialization — strict min_handoff_conf 93 blocks advance-phase claims for those macro slices until HOLD clears, HR rises with traceable evidence, or a written policy exception exists.
2. Operator-open decisions: D-044 and D-059 still lack dated Option A/B and ARCH-FORK-01/02 sub-bullets per the decisions-log templates.
3. Drift scalars: drift_score_last_recal / handoff_drift_last_recal are qualitative roadmap-audit judgments; 0.04 vs 0.15 divergence is a methodology/scope signal, not a reproducible statistic without a machine spec.
4. Cross-artifact sync risk: If rollup HR or HOLD status changes, distilled-core core_decisions, D-046/D-050/D-055 rows, and workflow_state trace rows can drift unless updated in one pass.
5. Execution vs normative: Low rollup HR coexists with execution_handoff_readiness debt; coherent validator language must not be read as repo-executable handoff.

## Proposed fixes

See parent return suggested_fixes (stable order: risk low then medium then high; ties broken by target_path lexicographic).

## Notes for future tuning

- Prefer single bundle edits: operator picks (D-044, D-059) then handoff-audit / rollup row recompute so HR and HOLD columns move together.
- Add optional automation hook in roadmap-audit skill: emit drift_metric_version + inputs hash whenever scalars are written.
- When ira_after_first_pass is true, treat empty validator gap lists as still requiring explicit no-op confirmation in second pass compare mode.
