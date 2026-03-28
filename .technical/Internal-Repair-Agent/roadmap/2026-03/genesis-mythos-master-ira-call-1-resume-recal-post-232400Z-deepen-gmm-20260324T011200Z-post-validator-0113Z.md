---
created: 2026-03-24
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: resume-recal-post-232400Z-deepen-gmm-20260324T011200Z
ira_call_index: 1
status: repair_plan
risk_summary: { low: 1, medium: 1, high: 0 }
validator_report_path: .technical/Validator/roadmap-auto-validation-genesis-mythos-master-20260324T011300Z-recal-post-yaml-2324-first.md
parent_run_id: queue-eat-20260323T224310Z-gmm-recal
---

# IRA — roadmap — genesis-mythos-master (post-validator 0113Z)

## Context

Validator-driven IRA after first-pass `roadmap_handoff_auto` (medium / `needs_work`, primary `contradictions_detected`, plus `missing_roll_up_gates`, `missing_task_decomposition`, `safety_unknown_gap`). The Roadmap subagent already reconciled `last_deepen_narrative_utc` and refreshed the **last_run vs deepen narrative** bullet for `last_recal_consistency_utc` and `last_run` vs **0112Z** / **232400Z** deepen. Live `roadmap-state.md` frontmatter shows `last_run: 2026-03-24-0112`, `last_recal_consistency_utc: "2026-03-24-0112"`, `last_deepen_narrative_utc: "2026-03-23-2324"`, `version: 78`. The validator’s cited prose-vs-YAML gap on **23:18 / 2322** is **no longer present** in the current Notes bullet.

## Structural discrepancies

1. **Residual `contradictions_detected` (minor):** In the same **last_run vs deepen narrative** bullet, prose still says **`version` 77** for the 01:12Z recal line, while frontmatter **`version` is 78** — forked truth for anyone reconciling Notes to YAML.
2. **`missing_roll_up_gates`:** Rollup authority table and phase summaries still show **HR 92 < 93** with **G-P*.*-REGISTRY-CI** HOLD — accurate reflection of vault state; clearing requires **repo / CI / D-020 / 2.2.3** execution evidence or a **decisions-log** policy exception (not a prose patch).
3. **`missing_task_decomposition`:** Phase **3.4.9** validator DoD mirror still has unchecked **`[ ]`** items (e.g. REGISTRY-CI clearance, drift-spec ladder) — intentional until evidence exists; checking boxes without repo work would be a false green.
4. **`safety_unknown_gap`:** `drift_metric_kind: qualitative_audit_v0` with numeric-looking `drift_score_last_recal` / `handoff_drift_last_recal` lacks **`drift_spec_version`** / **`drift_input_hash`** (validator `next_artifacts`). The Notes block already warns non-comparability; frontmatter could make the contract machine-visible.

## Proposed fixes (caller-applied)

| Order | Risk | Target | Action |
| --- | --- | --- | --- |
| 1 | low | `1-Projects/genesis-mythos-master/Roadmap/roadmap-state.md` | In **Notes** → **`last_run` vs deepen narrative**, change **`version` 77** → **`version` 78** to match frontmatter after the 0112Z recal. **Constraint:** apply only if frontmatter `version` remains `78`. |
| 2 | medium | same | **Optional:** add frontmatter `drift_spec_version` and `drift_input_hash` (e.g. spec id for `qualitative_audit_v0` and a real hash of the recal audit inputs, or an explicit sentinel like `pending_versioned_spec` documented in Notes) so hostile validation can retire `safety_unknown_gap` without pretending numerics are comparable. **Constraint:** snapshot `roadmap-state.md` before frontmatter edit per core guardrails. |

**Repo / execution gated (no IRA vault-only repair):** REGISTRY-CI HOLD → HR ≥ 93; closing DoD mirror checkboxes; overflow policy at ~98% context — track via operator queue / repo work, not IRA narrative edits alone.

## Notes for future tuning

- **Version drift in long Notes bullets:** When `version` increments on recal, the **last_run vs deepen** paragraph should be edited in the same commit as frontmatter or generated from frontmatter to avoid 77/78 skew.
- **Validator under-reporting:** Treat first-pass `needs_work` as a floor; residual one-field mismatches (version prose) are easy to miss after larger YAML fixes.

