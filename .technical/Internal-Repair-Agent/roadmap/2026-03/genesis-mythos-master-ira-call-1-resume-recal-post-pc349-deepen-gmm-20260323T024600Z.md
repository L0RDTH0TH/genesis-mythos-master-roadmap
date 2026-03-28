---
created: 2026-03-23
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: resume-recal-post-pc349-deepen-gmm-20260323T024600Z
ira_call_index: 1
status: repair_plan
risk_summary: { low: 1, medium: 0, high: 0 }
parent_run_id: pr-eatq-20260323-gmm-recal
validator_report_path: .technical/Validator/roadmap-auto-validation-genesis-mythos-master-20260323T120500Z-gmm-pc349-recal-d060-first.md
---

# IRA call 1 — genesis-mythos-master — post–PC349 recal D-060 (validator→IRA)

## Context

RoadmapSubagent invoked IRA after the **first** nested roadmap_handoff_auto pass (ira_after_first_pass: true). Validator verdict: **medium** / **needs_work**, **primary_code** missing_roll_up_gates, plus missing_task_decomposition, safety_unknown_gap. Regression guard vs compare-final preserved codes and severity. workflow_state was already coherent per validator body (12:05 recal row above 02:22 deepen; frontmatter matches resume-deepen-post-layer1-recal-gmm-20260323T022200Z). Material rollup / execution debt is real and unchanged; this IRA pass does **not** propose clearing REGISTRY-CI HOLD, inventing operator picks, or closing HR 92 < 93 via prose.

## Structural discrepancies

1. **roadmap-state.md Notes — last_run vs deepen narrative bullet (line ~61):** Still describes "12:00 RECAL consistency block vs 12:05 deepen report below." That is **stale** after the **2026-03-23 12:05 UTC** RECAL block for resume-recal-post-pc349-deepen-gmm-20260323T024600Z and contradicts the validator safety_unknown_gap / stale_gloss_flag finding. Live **deepen** authority is workflow_state **2026-03-23 02:22** / resume-deepen-post-layer1-recal-gmm-20260323T022200Z, not a "12:05 deepen" pairing with 12:00 recal.
2. **Frontmatter last_deepen_narrative_utc: "2026-03-23-0026"** may be a separate hygiene item (0026 vs log 02:22); not in scope for this call per operator request for one low-risk Note fix only.

## Proposed fixes

| Order | Risk | Target | Action |
| --- | --- | --- | --- |
| 1 | **low** | 1-Projects/genesis-mythos-master/Roadmap/roadmap-state.md | Replace the **last_run vs deepen narrative** list item so it states: last_recal_consistency_utc / last_run track the **2026-03-23 12:05 UTC** RECAL consistency block (resume-recal-post-pc349-deepen-gmm-20260323T024600Z); **authoritative deepen** is workflow_state last ## Log deepen at **2026-03-23 02:22 UTC** with last_auto_iteration resume-deepen-post-layer1-recal-gmm-20260323T022200Z; remove the incorrect **12:00 vs 12:05** gloss. |

**Constraints:** Apply only after per-change snapshot + backup gates per Roadmap pipeline; single-section edit; do not touch rollup tables, REGISTRY-CI rows, or decisions-log picks.

## Notes for future tuning

- After multi-step recal/deepen chains, scan roadmap-state Notes for time labels that reference prior consistency headings (e.g. 2026-03-22 12:00) when a newer block exists (2026-03-23 12:05).
- Validator stale_gloss_flag: true in delta is a useful machine hook for doc-only IRA when structural YAML is already clean.
