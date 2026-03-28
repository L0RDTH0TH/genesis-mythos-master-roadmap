---
created: 2026-03-23
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: resume-recal-post-pc349-followup-deepen-gmm-20260323T121530Z
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 3
  medium: 3
  high: 1
validator_report_path: .technical/Validator/roadmap-auto-validation-genesis-mythos-master-20260323T121545Z-gmm-followup-recal-d060-first.md
parent_run_id: edacd85e-e25d-4e9b-b77a-45e6c859a16b
primary_code: missing_roll_up_gates
reason_codes:
  - missing_roll_up_gates
  - missing_task_decomposition
  - safety_unknown_gap
---

# IRA report — roadmap / RESUME_ROADMAP `recal` (validator-driven, `ira_after_first_pass`)

## Context

RoadmapSubagent completed a **post-first-pass** nested `roadmap_handoff_auto` cycle for queue entry **`resume-recal-post-pc349-followup-deepen-gmm-20260323T121530Z`** (`parent_run_id` `edacd85e-e25d-4e9b-b77a-45e6c859a16b`). The hostile validator report (**first** pass, compare vs compare-final **121000Z**) returns **`needs_work`**, **`severity: medium`**, with **`missing_roll_up_gates`** as **`primary_code`**, plus **`missing_task_decomposition`** and **`safety_unknown_gap`**. Regression guard vs compare-final: **no dulling**; clock skew between `last_run` and `last_recal_consistency_utc` was cleared (hygiene only). This IRA call does **not** re-litigate material rollup debt: **rollup `handoff_readiness` 92 < `min_handoff_conf` 93** with **G-P*.*-REGISTRY-CI** **HOLD** remains the honest advance wall under strict **`handoff_gate`**.

## Structural discrepancies

1. **Rollup / CI (material, not doc-fixable):** Rollup authority index and Phase 3 summary on [[1-Projects/genesis-mythos-master/Roadmap/roadmap-state.md|roadmap-state]] still show **92 < 93** and **REGISTRY-CI HOLD** per **D-046** / **D-050** / **D-055** on [[1-Projects/genesis-mythos-master/Roadmap/decisions-log.md|decisions-log]]. No **recal** prose can substitute for **2.2.3** / **D-020** execution evidence.
2. **Task decomposition signal:** [[1-Projects/genesis-mythos-master/Roadmap/distilled-core.md|distilled-core]] **`core_decisions`** Phase **3.4.9** line keeps **GMM-PC-349** **mirror DoD `[ ]`** — validator maps this to **`missing_task_decomposition`** (junior WBS / checkable leaves still open vs strict handoff bar).
3. **Traceability / phantom deepen id:** [[1-Projects/genesis-mythos-master/Roadmap/roadmap-state.md|roadmap-state]] nested validation bullet and [[1-Projects/genesis-mythos-master/Roadmap/workflow_state.md|workflow_state]] **12:15** `recal` row cite a follow-up deepen id **`resume-deepen-post-recal-pc349-gmm-20260323T121500Z`** as context (“D-060 after …”) while **`last_auto_iteration`** / authoritative deepen cursor remain **`resume-deepen-post-layer1-recal-gmm-20260323T022200Z`** and no matching **`## Log`** **deepen** row exists for the **pc349** id — parsers can misread “after deepen” as executed work.
4. **Drift methodology (`safety_unknown_gap`):** **`drift_metric_kind: qualitative_audit_v0`** implies **`drift_score_last_recal`** / **`handoff_drift_last_recal`** are not numerically comparable run-to-run without a **versioned drift spec + input hash**; roadmap-state already documents this — gap persists until spec exists or metrics are retired/replaced.

## Proposed fixes (for RoadmapSubagent / operator; IRA does not apply)

| # | Risk | Action type | Target | Summary |
|---|------|-------------|--------|---------|
| 1 | low | `adjust_frontmatter` / narrative patch | `1-Projects/genesis-mythos-master/Roadmap/roadmap-state.md` | In the **nested validation** bullet for `resume-recal-post-pc349-followup-deepen-gmm-20260323T121530Z`, replace “after **`resume-deepen-post-recal-pc349-gmm-20260323T121500Z`**” framing with **explicit queued / idempotency** language (e.g. “per queue `user_guidance` / idempotency_key **`…121500Z-followup-deepen`** — **no matching deepen `## Log` row yet**”) so recal is not read as proof deepen landed. |
| 2 | low | `rewrite_log_entry` | `1-Projects/genesis-mythos-master/Roadmap/workflow_state.md` | Same disambiguation in the **2026-03-23 12:15** `recal` row **Status / Next** cell: distinguish **planned** vs **completed** deepen id; keep **`last_auto_iteration`** unchanged until a real deepen row is appended. |
| 3 | medium | `write_log_entry` | `1-Projects/genesis-mythos-master/Roadmap/workflow_state.md` | **When** (and only when) the pipeline runs the deepen for **`resume-deepen-post-recal-pc349-gmm-20260323T121500Z`**, append the standard **`## Log`** **deepen** row and then align **`last_auto_iteration`**, **`iterations_per_phase.3`**, **`last_ctx_util_pct`**, **`current_subphase_index`** per **`workflow_log_authority: last_table_row`**. **Constraint:** do not bump cursor on recal-only rows. |
| 4 | medium | `adjust_frontmatter` / section edit | `1-Projects/genesis-mythos-master/Roadmap/distilled-core.md` | On the **3.4.9** `core_decisions` string: add an inline qualifier that **`[ ]`** is the **validator DoD mirror** (pending checkable closure / second-pass validator), **not** absence of the GMM-PC-349 trace artifact — or split into two bullets (trace done vs DoD closed). **Constraint:** do not change rollup HR or imply REGISTRY-CI clearance. |
| 5 | medium | `recompute_phase_metadata` / in-note checklist | Phase **3.4.9** roadmap note under `1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/` (post-recal junior handoff bundle slug) | Add **checkable** sub-leaves under **GMM-PC-349** (or explicit “deferred until …” rows) so **`missing_task_decomposition`** can narrow to concrete unchecked items with wiki anchors — without claiming rollup or CI closure. |
| 6 | high | policy / execution path | `1-Projects/genesis-mythos-master/Roadmap/decisions-log.md` + repo / **2.2.3** | **Clear REGISTRY-CI HOLD** via **checked-in** registry/fixture evidence per **D-020** / **2.2.3**, **or** add a **signed policy exception** row that explicitly lowers **`min_handoff_conf`** or exempts advance — **operator + eng**, not vault-only HR edits. **Constraint:** no silent bump of rollup **HR** from **92** to **≥93** without evidence. |
| 7 | low | `set_context_metrics` / frontmatter stub | `1-Projects/genesis-mythos-master/Roadmap/roadmap-state.md` | When the vault adopts a **versioned drift spec**, add **`drift_spec_version`** + **`drift_input_hash`** (or equivalent) beside **`drift_metric_kind`**; until then, keep the existing **qualitative** disclaimer block (no removal). |

## Notes for future tuning

- **Recal-after-compare-final** runs should default to **one of two** deepen id states in state files: **(A)** id only in **queue / idempotency** fields, or **(B)** id mirrored in **`## Log`** after deepen — avoid **(C)** id cited in recal narrative as if **(B)** without the row.
- **`ira_after_first_pass: true`** should continue to allow **empty `suggested_fixes`** when the only gaps are **honest material blockers**; this project state still benefits from **low/medium traceability** patches before the second validator pass.
- Consider a **lint** (little val or roadmap skill) for **`queue_entry_id` cited in roadmap-state / workflow_state** → must match a **`## Log`** row or be labeled **pending**.

## Machine return stub

- **`status`:** `repair_plan`
- **`suggested_fix_count`:** 7 (3 low, 3 medium, 1 high)
