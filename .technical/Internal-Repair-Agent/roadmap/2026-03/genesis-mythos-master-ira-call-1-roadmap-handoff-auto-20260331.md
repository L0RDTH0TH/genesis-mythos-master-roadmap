---
created: 2026-03-31
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: roadmap-handoff-auto-20260331
ira_call_index: 1
status: repair_plan
risk_summary: { low: 3, medium: 0, high: 0 }
validator_report: .technical/Validator/roadmap-handoff-auto-genesis-mythos-master-20260331T120000Z-conceptual-v1.md
---

# IRA — roadmap_handoff_auto (first pass), genesis-mythos-master

## Context

Post–nested-validator **IRA** after **`roadmap_handoff_auto`** first pass (`severity: medium`, **`recommended_action: needs_work`**, **`primary_code: missing_roll_up_gates`**, **`reason_codes`:** `missing_roll_up_gates`, `safety_unknown_gap`). **Effective track:** conceptual (`gate_catalog_id: conceptual_v1`). The validator treats **GMM-2.4.5-*** execution compare-table / registry closure as **execution-deferred** on conceptual; the remaining gaps are **traceability / hygiene** (dual clock fields in **`workflow_state`** ## Log; **`progress: 85`** vs **`handoff_readiness: 86`** on Phase 4 primary).

## Structural discrepancies

1. **`missing_roll_up_gates`:** Execution artifacts for **`GMM-2.4.5-SCHEMA` / `RETENTION` / `VALIDATOR-COMPARE-TABLE`** are not closed — already anchored in **`decisions-log`** (**D-2.4.5-execution-deferred-handoff-anchor**) and **`distilled-core`** (conceptual waiver + `GMM-2.4.5-*` reference-only). Residual risk is **cross-reader clarity** that the validator reason code is **advisory** on conceptual, not a design contradiction.

2. **`safety_unknown_gap` (A — clocks):** **`workflow_state`** last ## Log row pairs **`telemetry_utc`** (e.g. handoff correlation / repair run) with **`monotonic_log_timestamp`** and human **Timestamp** — automation can misread which field is authoritative without an explicit contract in **rollup** surfaces.

3. **`safety_unknown_gap` (B — progress):** Phase 4 primary shows **`progress: 85`** alongside **`handoff_readiness: 86`** and narrative claiming primary rollup complete — semantics are ambiguous unless reconciled in a **non-body** advisory line (avoid rewriting frozen phase narrative).

## Proposed fixes (caller-applied; IRA does not edit PARA notes)

All items below are **`risk_level: low`** — **append-only** lines to **`decisions-log.md`** and **`distilled-core.md`**; no overwrite of frozen conceptual phase bodies, no structural rewrite of **`workflow_state`** or Phase 4 frontmatter in this pass.

| # | Description | action_type | target_path |
|---|-------------|-------------|-------------|
| 1 | Append a dated bullet under **`## Decisions`** citing validator report path, **`primary_code` / `reason_codes`**, and explicit statement: **`GMM-2.4.5-*` closure** is **execution-track** obligation (per **D-2.4.5**); conceptual **`needs_work`** here is **advisory** and satisfied by existing deferrals + distilled-core waiver — second-pass validator should not treat as sole hard-fail on conceptual. | append_section_line | `1-Projects/genesis-mythos-master/Roadmap/decisions-log.md` |
| 2 | Append a short **advisory** paragraph (after **Conceptual track waiver** block or under **Phase 0 anchors**) in **`distilled-core.md`**: **Authoritative clock fields** for **`workflow_state` ## Log** — for sorting/trace, treat **`Timestamp`** + **`monotonic_log_timestamp`** as the row’s sequence anchor; **`telemetry_utc`** is **handoff/validator correlation** and may differ when **`clock_corrected`** is present (not a duplicate error by itself). | append_section_line | `1-Projects/genesis-mythos-master/Roadmap/distilled-core.md` |
| 3 | Append one bullet under **`## Conceptual autopilot`** (or **`## Decisions`**) reconciling **Phase 4 primary** **`progress`** vs **`handoff_readiness`**: e.g. **`progress`** = slice checklist completion; **`handoff_readiness`** = rollup gate score — both can coexist without forcing a frontmatter edit on the primary note. | append_section_line | `1-Projects/genesis-mythos-master/Roadmap/decisions-log.md` |

## Notes for future tuning

- Prefer **append-only rollup hygiene** in **`decisions-log` / `distilled-core`** before touching **`workflow_state`** log rows or frozen phase frontmatter when the validator codes are **`safety_unknown_gap`** + conceptual **`needs_work`**.
- Consider a single **workflow_state** header line (**medium** risk) in a later run if second validator still flags clock ambiguity after advisory text.

## Patterns

- **`missing_roll_up_gates`** on conceptual often resolves with **explicit execution-deferral pointers** already in **D-2.4.5** + distilled-core — residual value is **verbatim validator report citation** in decisions-log for grep-stable audits.
