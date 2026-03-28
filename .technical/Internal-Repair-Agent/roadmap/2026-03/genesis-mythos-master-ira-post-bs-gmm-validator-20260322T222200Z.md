---
created: 2026-03-22
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: bs-gmm-deepen-20260322T201945Z-m4n8p2q6
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 4
  medium: 0
  high: 0
validator_report_path: .technical/Validator/roadmap-auto-validation-genesis-mythos-master-20260322T222200Z-post-bs-gmm-deepen.md
---

# IRA — genesis-mythos-master (post–bs-gmm deepen validator)

## Context

Nested **`roadmap_handoff_auto`** after **RESUME_ROADMAP** deepen **`bs-gmm-deepen-20260322T201945Z-m4n8p2q6`** returned **medium / `needs_work`** with **`missing_roll_up_gates`**, **`missing_task_decomposition`**, **`safety_unknown_gap`**. **`ira_after_first_pass: true`**. Authoritative **`workflow_state.md`** frontmatter matches the physical last **`## Log`** row: **`last_ctx_util_pct: 92`**, **`last_auto_iteration`** = that queue id, **Ctx Util %** **92** on the **2026-03-22 20:19** deepen row. **`distilled-core.md`** frontmatter **`core_decisions`** Phase **3.4.9** bullet and the body duplicate still say **ctx 87%**, i.e. stale vs the live cursor (**`safety_unknown_gap`** / secondary-index drift). Contaminated-report rule: rollup **HOLD**s and unchecked **GMM-** tasks are treated as **at least** what the validator stated; fixing distilled-core alone does **not** clear **`missing_roll_up_gates`** or **`missing_task_decomposition`**.

## Structural discrepancies

1. **`distilled-core.md`** Phase **3.4.9** summary cites **ctx 87%** while **`workflow_state`** cites **92%** and **`queue_entry_id` `bs-gmm-deepen-20260322T201945Z-m4n8p2q6`** for the last deepen.
2. Same **87%** sentence duplicated in **`distilled-core.md`** body **Core decisions** section (~line 98).
3. **Macro rollup** rows on **3.2.4 / 3.3.4 / 3.4.4** remain **HR 92 < 93** with **HOLD** ids — **not** caused by ctx drift; should stay **explicitly documented** so operators do not misread **bs-gmm** deepen as rollup closure.
4. **`decisions-log.md`** **D-044** / **D-059** already use **stub / template** language without fabricated **A/B** or **ARCH-FORK** picks — **no repair** unless a future edit removes placeholders.

## Proposed fixes

See structured return **`suggested_fixes`** (caller applies under snapshot + roadmap gates). Order: low-risk hygiene first.

## Notes for future tuning

- After **high-context** deepens, **`roadmap-deepen`** or a post-step should refresh **`distilled-core`** `core_decisions` **ctx** / **`queue_entry_id`** when **`workflow_state`** frontmatter updates, or emit a machine checklist item so **Validator→IRA** does not repeat the same drift.
- **`missing_roll_up_gates`** will remain **`needs_work`** until operator/repo evidence clears **HOLD**s — document as **orthogonal** to **3.4.9** WBS literacy.
