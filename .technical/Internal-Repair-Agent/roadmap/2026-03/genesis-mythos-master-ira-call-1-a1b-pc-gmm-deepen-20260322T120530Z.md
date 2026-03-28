---
created: 2026-03-22
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: a1b-pc-gmm-deepen-20260322T120530Z
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 3
  medium: 3
  high: 1
validator_report: .technical/Validator/roadmap-auto-validation-genesis-mythos-master-20260322T121500Z-first.md
parent_run_id: l1-eatq-20260322-a1b-gmm
---

# IRA — roadmap (post–first-pass validator)

## Context

Nested `roadmap_handoff_auto` first pass returned **medium / needs_work** with `missing_task_decomposition` and `safety_unknown_gap`. `ira_after_first_pass: true`. Contaminated-report rule applied: treat cited gaps as a **weak minimum** — expand structure, traceability, and machine-safe semantics beyond the validator’s wording.

## Structural discrepancies

1. **`workflow_state.md` `## Log`:** Penultimate data row timestamp **2026-03-23 19:35** (Phase **3.4.4** / queue **253**) is **after** the final row **2026-03-22 12:05** (Phase **3.4.5** / queue **a1b**). Any consumer sorting by `Timestamp` infers the wrong “latest” event vs `current_subphase_index: "3.4.5"` and last-row convention.
2. **Secondary `phase-3-4-...-1210.md` `handoff_gaps`:** First bullet still reads as “**3.4.4** rollup opened — next: …” while machine cursor and `roadmap-state` identify **3.4.5** as live deepen context.
3. **Tertiary `phase-3-4-5-...-1205.md`:** Tasks are four unchecked bullets without **field-row tables**, **per-stub acceptance observables** (non-golden), or explicit **DEFERRED ledger** rows with owners; `ToolActionQueue_v0` is named but not bounded.
4. **Honesty / cross-links (expanded):** Validator mentioned D-044 / D-032 / D-043; under contaminated rule also verify **no task checkbox** or narrative implies presentation bridge “done” while preimage / header / regen lane story is still **HOLD** — including any implied closure in pseudo-code comments vs `handoff_gaps`.

## Proposed fixes

See structured `suggested_fixes` in the parent hand-off return (stable order: low risk group first, then medium, then high).

## Notes for future tuning

- **Timestamp vs causality:** When a “cursor” run predates a later rollup row in calendar time, either **enforce monotonic timestamps** via a reconcile row (with explicit semantics) or **standardize** `workflow_log_authority` in frontmatter across all projects.
- **Tertiary bridge pattern:** For notes with `handoff_readiness` below `min_handoff_conf`, require **field stub tables + acceptance observables** at first mint to avoid repeated `missing_task_decomposition` on otherwise honest openings.
