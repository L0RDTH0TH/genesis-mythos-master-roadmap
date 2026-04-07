---
created: 2026-04-09
pipeline: roadmap
project_id: sandbox-genesis-mythos-master
queue_entry_id: followup-deepen-exec-phase1-2-1-tertiary-sandbox-gmm-20260409T152100Z
ira_call_index: 1
status: repair_plan
risk_summary: { low: 3, medium: 2, high: 1 }
validator_report_path: .technical/Validator/roadmap-handoff-auto-sandbox-gmm-exec-1-2-1-tertiary-20260409T160500Z.md
---

# IRA — roadmap (post–nested-validator pass 1)

## Context

Validator **`roadmap_handoff_auto`** returned **`needs_work`** (medium) with **`missing_roll_up_gates`**, **`safety_unknown_gap`**, **`missing_task_decomposition`**. Execution tertiary **1.2.1** mint is structurally present; gaps are **evidence hygiene** on **GWT-1-2-1-Exec-A** vs **`current_subphase_index: "1.2"`**, **`progress: 35`** vs an all-checked NL checklist, missing **decisions-log** anchor for this **`queue_entry_id`**, and **rollup / WBS** debt called out for the execution track.

## Structural discrepancies

1. **GWT-A evidence:** Row cites “`current_subphase_index` post-mint” without quoting the **actual** frontmatter value **`"1.2"`** or the **## Log** justification (2026-04-09 15:25 row: cursor remains **`1.2`** for rollup scope after **1.2.1** mint).
2. **`progress: 35`** on **1.2.1** conflicts with **all `[x]`** items in **## NL checklist (1.2.1)** unless **`progress`** is explicitly defined as a non-checklist metric.
3. **`decisions-log.md`** has **no** line containing **`followup-deepen-exec-phase1-2-1-tertiary-sandbox-gmm-20260409T152100Z`** — traceability is **workflow_state ## Log** only.
4. **Roll-up gate (primary code):** **`roadmap-state-execution`** Phase 1 summary still advertises “next **secondary 1.2 rollup**” without a completed **NL + GWT** reconciliation section on **1.2** (or dedicated rollup note).
5. **Task decomposition:** Tertiary note is **stub-tier**; validator still flags absence of **delegatable** hooks — needs either minimal **## Verification / ownership** rows or an explicit **stub / defer** label.

## Proposed fixes

See parent agent return **`suggested_fixes[]`** (ordered **low → medium → high**).

## Notes for future tuning

- When minting execution tertiaries under a secondary whose **workflow cursor** stays at **parent index** (rollup scope), **GWT evidence** should **always** quote **`workflow_state-execution` frontmatter** verbatim + **one Log row** — template this in roadmap-deepen / handoff-audit.
- Consider a **progress** convention for roadmap notes: either **`progress` tracks checklist completion** (0–100 aligned to boxes) or **`progress_is_stub: true`** + human **`progress_note`**.
