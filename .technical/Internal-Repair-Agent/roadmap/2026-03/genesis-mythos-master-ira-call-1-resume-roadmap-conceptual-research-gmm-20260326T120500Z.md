---
created: 2026-03-27
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: resume-roadmap-conceptual-research-gmm-20260326T120500Z
ira_call_index: 1
status: repair_plan
risk_summary: {low: 3, medium: 0, high: 0}
validator_report_path: .technical/Validator/roadmap-handoff-auto-genesis-mythos-master-20260327T121500Z-conceptual-v1-post-415-research-deepen.md
---

# IRA report — genesis-mythos-master (post–first-pass `roadmap_handoff_auto`)

## Context

Post–nested-validator IRA after **`roadmap_handoff_auto`** for conceptual gate catalog **`conceptual_v1`**, cursor **4.1.5**, queue **`resume-roadmap-conceptual-research-gmm-20260326T120500Z`**. First-pass report: **`severity: medium`**, **`recommended_action: needs_work`**, **`primary_code: missing_roll_up_gates`**, **`reason_codes`**: `missing_roll_up_gates`, `safety_unknown_gap`. Coherence checks in that report **passed** (workflow_state / roadmap-state / top deepen row alignment). The “gaps” are **policy-honest** on the conceptual track: rollup **HR 92 < 93**, **G-P*.*-REGISTRY-CI HOLD**, and qualitative drift comparability — **not** skimmer/YAML contradictions. **No vault edit should falsely clear** those advisories without repo/CI evidence.

## Structural discrepancies

1. **`missing_roll_up_gates` (validator-facing)** — Macro rollup/registry execution debt remains **open by design** until **G-P*.*-REGISTRY-CI** clears and HR meets **`min_handoff_conf` 93**; phase **4.1.5** note + **distilled-core** correctly echo **HOLD** / **HR 92 < 93**. This is **not** a missing workflow row or stale cursor; it is **unresolved gate evidence** outside vault prose.
2. **`safety_unknown_gap`** — [[roadmap-state]] already documents **non-numeric** comparability for **`drift_metric_kind: qualitative_audit_v0`** and points at [[drift-spec-qualitative-audit-v0]]. No additional structural inconsistency detected beyond the **documented** uncertainty until a versioned drift spec + input hash exists.

## Proposed fixes (apply order)

See structured return **`suggested_fixes`** in the parent pipeline hand-off (stable-ordered). All are **compatible** with **Vault-honest** / **no PASS inflation** invariants.

## Notes for future tuning

- **Recurrent pattern:** `missing_roll_up_gates` will keep appearing on **`roadmap_handoff_auto`** while conceptual vault stays honest and execution remains deferred — treat **`needs_work`** as **expected** unless tiered policy changes.
- **Ctx 76%** after 4.1.5 deepen already triggers **D-060** preference for **`recal`** over heavy **`deepen`**; automations should **enqueue recal** and log ids rather than chasing deepen loops for the same gate codes.
