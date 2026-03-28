---
created: 2026-03-23
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: resume-recal-post-layer1-deepen-gmm-20260323T021530Z
ira_call_index: 1
parent_run_id: a2e8bc50-0270-4c51-a0cc-9ac1bc18666e
validator_report_path: .technical/Validator/roadmap-auto-validation-genesis-mythos-master-20260323T021530Z-layer2-recal-first.md
status: repair_plan
risk_summary: { low: 3, medium: 2, high: 1 }
tags: [internal-repair-agent, roadmap, genesis-mythos-master, validator-driven]
---

# IRA report — genesis-mythos-master — call 1 (validator-driven)

## Context

RoadmapSubagent invoked IRA after **Layer-2** nested `roadmap_handoff_auto` **first pass** (`ira_after_first_pass: true`) for queue **`resume-recal-post-layer1-deepen-gmm-20260323T021530Z`**. Validator verdict: **`severity: medium`**, **`recommended_action: needs_work`**, **`primary_code: missing_roll_up_gates`**, plus **`missing_task_decomposition`** and **`safety_unknown_gap`**. Artifacts reviewed: validator report, [[roadmap-state]], [[workflow_state]], [[decisions-log]], [[distilled-core]]. **Little val** is not the driver here; nested validator gaps define the repair surface.

**Contaminated-report rule applied:** Treat validator findings as a **weak minimum**. Vault state already reflects **D-044 Option A** and **D-059 ARCH-FORK-02** on [[decisions-log]] (2026-03-23); rollup **HR 92 < min_handoff_conf 93** and **G-P*.*-REGISTRY-CI HOLD** remain honestly documented. No IRA recommendation fabricates operator picks.

## Structural discrepancies

1. **Rollup / advance semantics (`missing_roll_up_gates`):** Secondary closure rollups for **3.2.4**, **3.3.4**, **3.4.4** remain at **HR 92** with **REGISTRY-CI HOLD** — consistent with Layer-1 compare-final; **not** fixable by narrative alone.
2. **Execution ladder vs decomposition (`missing_task_decomposition`):** Phase **3.4.9** shows **`execution_handoff_readiness: 33`** in validator cite; **3.4.8** ladder **row 1** PASS is evidenced; rows **2+** remain gated on **D-032 / D-043 / D-045** (and repo paths) per validator **next_artifacts**.
3. **Ambiguous junior-facing history (`safety_unknown_gap`):** Older **Consistency reports** blocks still say "**D-044 / D-059** remain **open**" while [[decisions-log]] now logs **Option A** / **ARCH-FORK-02** — "open" mixes *pick missing* vs *execution / literal-field debt*. [[roadmap-state]] section **Operator decision visibility (2026-03-23)** mitigates but is easy to miss when scanning older callouts.
4. **Drift comparability:** `drift_metric_kind: qualitative_audit_v0` + unchanged scalars **0.04 / 0.15** — methodology not versioned; validator correctly flags **safety_unknown_gap** until spec + input hash or explicit labeling everywhere scalars appear (partially done in newer notes).

## Proposed fixes (for RoadmapSubagent / operator; IRA does not edit PARA)

| # | risk_level | action_type | target_path | description |
|---|------------|-------------|-------------|-------------|
| 1 | low | append_consistency_citation | `1-Projects/genesis-mythos-master/Roadmap/roadmap-state.md` | In **2026-03-23 02:15 UTC** RECAL consistency block, append a **Layer-2 nested validation** line citing `.technical/Validator/roadmap-auto-validation-genesis-mythos-master-20260323T021530Z-layer2-recal-first.md` with **`primary_code`** + **`reason_codes`** (mirror the existing Layer-1 compare-final cite pattern). |
| 2 | low | append_workflow_note | `1-Projects/genesis-mythos-master/Roadmap/workflow_state.md` | Add a **Notes** bullet (2026-03-23) recording **Layer-2** first-pass validator path, **`queue_entry_id`**, **`parent_run_id`**, and **`pipeline_task_correlation_id`** for parity with the **02:15** `recal` row. |
| 3 | low | add_validator_dod_mirror | `1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/phase-3-4-9-post-recal-task-decomposition-junior-handoff-bundle-roadmap-2026-03-22-1225.md` | Add a short section **Validator definition of done (mirror — not closure)** listing the four **next_artifacts** bullets from the Layer-2 report as **explicit unchecked** execution items (REGISTRY-CI / D-032–D-045 evidence / drift spec or label discipline / optional stale-block banners). |
| 4 | medium | add_archived_block_gloss | `1-Projects/genesis-mythos-master/Roadmap/roadmap-state.md` | Under **Consistency reports (RECAL-ROAD)** or **Notes**, add a single **Archived RECAL wording gloss** paragraph: any pre-2026-03-23 "D-044 / D-059 remain open" line means **checklist / execution debt**, not "operator pick absent" after **2026-03-23** [[decisions-log]] rows; point to section **Operator decision visibility (2026-03-23)**. **Constraint:** Do not mass-rewrite every historical block in one run unless snapshots are taken per block (prefer one gloss + optional incremental banners). |
| 5 | medium | incremental_stale_banner | `1-Projects/genesis-mythos-master/Roadmap/roadmap-state.md` | Optionally prefix **1–2** highest-traffic older consistency callouts with `> [!warning] Archived narrative` one-liner pointing to Operator decision visibility — **only** after per-change snapshot of `roadmap-state.md`. |
| 6 | high | clear_registry_ci_hold | *(repository / CI)* | **Out of vault automation scope:** clearing **G-P*.*-REGISTRY-CI** requires checked-in fixtures, green **ReplayAndVerify**, and/or an **explicit operator policy exception** documented in [[decisions-log]] — do **not** simulate closure in vault prose. **Constraint:** Apply only with real VCS evidence; skip if unavailable. |

## Notes for future tuning

- **Validator to IRA after first pass:** Even when verdict is **`needs_work`** without contradiction, IRA should still emit **traceability** fixes so Layer-2 reports are **symmetrically cited** next to Layer-1 compare-final in [[roadmap-state]].
- **Word "open" on D-044/D-059:** Standardize in templates: **open (execution)** vs **logged (operator)** to reduce **`safety_unknown_gap`** false signals.
- **Drift:** A one-page **versioned drift spec** (inputs + hash) would retire **`qualitative_audit_v0`** ambiguity; until then, every scalar cite should repeat **`drift_metric_kind`**.

## IRA outcome

**`status: repair_plan`** — Fixes 1–3 are **low-risk documentation/traceability**; 4–5 **medium** (scope control + snapshots); 6 **high** and **external**. **None** assert rollup **HR >= 93** or ladder closure without repo evidence.
