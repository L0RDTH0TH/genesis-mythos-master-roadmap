---
created: 2026-03-22
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: resume-roadmap-genesis-mythos-master-20260322-deepen-followup-suggested-245
ira_call_index: 1
status: repair_plan
risk_summary: { low: 4, medium: 2, high: 1 }
validator_report_path: .technical/Validator/roadmap-auto-validation-genesis-mythos-master-20260322T234200Z.md
parent_run_id: pr-queue-20260322-genesis-resume-245
---

# IRA call 1 — roadmap / RESUME_ROADMAP deepen 3.3.1 (queue 245)

## Context

Nested `roadmap_handoff_auto` first pass (`.technical/Validator/roadmap-auto-validation-genesis-mythos-master-20260322T234200Z.md`) returned **high** / **block_destructive** with **primary_code** `state_hygiene_failure`, plus `missing_task_decomposition` and `safety_unknown_gap`. The Roadmap subagent then applied **post-validator edits** (roadmap-state Notes hygiene, 3.3.1 deferral table + checked spine task, 3.3 secondary stub banner). Re-read of live `roadmap-state.md` shows the **dual-truth Notes bullet** is already rewritten as **historical** (line 57: past-tense macro phase 2 at 2026-03-20 vs canonical phase 3 today). Little val for this deepen was not the invocation driver; this IRA cycle is **validator branch B** with `ira_after_first_pass: true`.

## Structural discrepancies (expanded beyond validator minimum)

1. **Primary code (validator time):** Notes bullet asserted present-tense macro `current_phase` 2 vs frontmatter `current_phase: 3` — **likely cleared** in vault v29 + 23:45 consistency block; still run a **whole-file grep** for stray "remains **2**" / present-tense macro pointers in Notes.
2. **missing_task_decomposition:** Hostile pass treats **unchecked Tasks** as insufficient even when a deferral table exists; **duplicate representation** (Tasks checkboxes + deferral table) can still read as "undecomposed" to automation.
3. **safety_unknown_gap:** Tertiary honestly holds **`execution_handoff_readiness: 58`** and TBD literals until **D-032** / **D-043**; **D-047** names TBD **stream_id** + reason codes — validator-softened risk is **implying** junior-ready handoff when checkboxes + gaps coexist without a single **authoritative blocked-on surface** in frontmatter/body.

## Proposed fixes (for Roadmap subagent to apply)

See structured `suggested_fixes` in parent return payload; summary by risk:

- **Low:** Consistency-block trace line (validator → IRA → compare-final pending); grep verification on `roadmap-state.md` Notes; `distilled-core` one-line pointer to deferral ledger + D-047 as authoritative open-work surface; optional frontmatter `blocked_on_decisions` on 3.3.1.
- **Medium:** Deduplicate or explicitly cross-link Tasks vs deferral table on 3.3.1; append **D-047** fork (labeled stream_id options, operator pick required).
- **High (conditional):** Header-only placeholder table for ResumeCheckpoint fields — **only** if compare-final still demands a literal scaffold; **never** invent field types before D-032/D-043.

## Notes for future tuning

- Repeated **state_hygiene_failure** from Notes bullets that lag `workflow_state` / frontmatter; consider a roadmap-deepen post-step lint: "no present-tense `current_phase` in Notes unless tagged `(current — …)`."
- Hostile validator should treat **deferral table + honest EHR** as satisfying decomposition when Tasks checkboxes are explicitly mapped to deferral rows (avoid double signal).
