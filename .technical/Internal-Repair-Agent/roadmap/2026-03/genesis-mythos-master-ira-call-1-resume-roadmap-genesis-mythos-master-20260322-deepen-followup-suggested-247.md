---
created: 2026-03-23
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: resume-roadmap-genesis-mythos-master-20260322-deepen-followup-suggested-247
ira_call_index: 1
status: repair_plan
risk_summary: { low: 3, medium: 4, high: 0 }
validator_report_path: .technical/Validator/roadmap-auto-validation-genesis-mythos-master-20260323T001030Z-first.md
parent_run_id: l1-eatq-20260322-8c4e91a0
---

# IRA report — roadmap / RESUME_ROADMAP (validator-driven, call 1)

## Context

Host invoked IRA after **first-pass** `roadmap_handoff_auto` with **`state_hygiene_failure`** (primary), **`missing_task_decomposition`**, **`safety_unknown_gap`**, verdict **high / block_destructive**. The frozen validator report cites stale `workflow_state` frontmatter (**63 / 90**) vs last log row (**64 / 88**) for queue **`resume-roadmap-genesis-mythos-master-20260322-deepen-followup-suggested-247`**.

**Current vault read (post-caller note):** `workflow_state.md` frontmatter shows **`last_ctx_util_pct: 64`**, **`last_conf: 88`**, matching the **last** `## Log` data row for that queue id. The **migration_id** vault-table task on **3.3.3** is **checked**; a **G-NEG-*** binding subsection exists in-note. Treat the validator artifact as a **minimum** — some findings are **already partially cleared**, but **literal cross-artifact anchors** and **task hygiene** likely still fail a hostile re-pass until tightened.

## Structural discrepancies

1. **state_hygiene_failure — remediated in live files:** Frontmatter and last log row for **247** agree on util/conf. The validator markdown remains historically accurate as a **snapshot at 00:10Z**; no dual-truth remains **if** no newer log row was appended without FM sync (caller should re-verify after any further deepen).
2. **missing_task_decomposition — partial:** One of four **Tasks** on **3.3.3** is **done** (`[x]` migration registry stub). Three remain **open** without a **DEFERRED** ledger mirroring **3.3.1** discipline — automation may still score this as checklist debt.
3. **safety_unknown_gap — narrowed but not closed:** **G-NEG-*** IDs are bound to **vault wikilinks** in **3.3.3**, but **3.3.1** still has only **draft** resume reason bullets (no literal harness-ID column), and **3.3.2** has an open task to reconcile **reason_code** strings — **no explicit row** stating **`G-NEG-INCOMPAT` ↔ matrix INCOMPATIBLE branch** (machine-auditable).
4. **handoff_gaps stale phrasing:** **3.3.3** `handoff_gaps` still imply “draft binding” for **G-NEG-*** while the note now contains a binding **table** — creates false **unknown-gap** signal for validators.
5. **Secondary roll-up / EHR:** Validator **`safety_unknown_gap`** also flags **3.3** secondary **HR 0** and low **EHR**; that is **intentional stub** per prior reports — document as **non-contradiction** in consistency row if compare-final asks.

## Proposed fixes (for RoadmapSubagent apply order: low → medium → high)

| # | risk | target | action_type | summary |
|---|------|--------|-------------|---------|
| 1 | low | `workflow_state.md` | verify_alignment | Parse last `## Log` row for `last_auto_iteration`; confirm `last_ctx_util_pct`/`last_conf` numeric-equal row; **no write** if matched. |
| 2 | low | phase **3.3.3** note | adjust_frontmatter | Rewrite `handoff_gaps` bullets: state **G-NEG-*** vault binding **table present**; residual = **literal reason_code rows** in **3.3.1**/**3.3.2** + repo fixtures (**D-032**/**D-043**/**D-047**). |
| 3 | low | `roadmap-state.md` | write_log_entry | In **2026-03-23 00:10** consistency subsection, replace nested-validator placeholder with links to first / IRA / compare-final when available; one line noting **FM/log reconciled post-first-pass** if true. |
| 4 | medium | phase **3.3.1** note | recompute_phase_metadata | Add a small **Harness ID ↔ resume surface (draft)** table: e.g. **`G-NEG-TRACE`** → trace / `ordered_step_index` / hash linkage ↔ draft codes **`RESUME_LINEAGE_BREAK`**, **`RESUME_TICK_CURSOR_GAP`**, **`RESUME_PROFILE_MISMATCH`** (explicit mapping rows, not prose only). |
| 5 | medium | phase **3.3.2** note | recompute_phase_metadata | Under **INCOMPATIBLE** / fail-closed migrate path, add one **machine row**: **`G-NEG-INCOMPAT`** = harness parametrization of documented **INCOMPATIBLE** outcome + “no ordered migration steps” trace semantics (align with **3.3.3** binding table). |
| 6 | medium | phase **3.3.3** note | rewrite_log_entry | Add **### DEFERRED tasks (ledger)** for the three remaining checkboxes: each line = task + **D-049** + blocking **D-032**/**D-043**/**D-047**/**D-048** (same pattern as **3.3.1** deferred table). |
| 7 | medium | phase **3.3.3** note | write_log_entry | Add minimal **fixture case IDs** markdown table (stable IDs only, wikilinks to **3.3.3** binding table + **3.3.2** matrix) — satisfies decomposition evidence without claiming repo JSONL exists. |

**Constraints (global):** Apply only after **per-change snapshots** on each target note per roadmap rules; skip any fix if snapshot gate fails.

## Notes for future tuning

- **roadmap-deepen** should treat **frontmatter sync** as part of the same atomic write as the log append to prevent **state_hygiene_failure** regressions.
- Hostile **missing_task_decomposition** on tertiaries may require either **≥1 checked task with vault artifact** or an explicit **DEFERRED** block.
- **safety_unknown_gap** for **G-NEG-*** should be defined as **no row in partner phase notes**, not merely **no repo fixture**.
