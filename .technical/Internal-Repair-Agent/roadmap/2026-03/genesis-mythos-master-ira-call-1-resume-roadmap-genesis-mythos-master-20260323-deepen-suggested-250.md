---
created: 2026-03-23
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: resume-roadmap-genesis-mythos-master-20260323-deepen-suggested-250
ira_call_index: 1
status: repair_plan
risk_summary: { low: 2, medium: 3, high: 0 }
---

# IRA call 1 — RESUME_ROADMAP deepen 250 (Validator first pass → IRA)

## Context

Nested **roadmap_handoff_auto** first pass reported **high** / **block_destructive** with **primary_code** `state_hygiene_failure`, plus `missing_task_decomposition` and `safety_unknown_gap`. The validator snapshot claimed `workflow_state.md` frontmatter still reflected the **prior** deepen row (**67% / 86**) while the authoritative last **`## Log`** row for queue **250** was **68% / 85**.

**Re-read of current vault state (2026-03-23):** `1-Projects/genesis-mythos-master/Roadmap/workflow_state.md` frontmatter already has `last_ctx_util_pct: 68` and `last_conf: 85`, matching the last table row (`2026-03-23 16:20`, `queue_entry_id: resume-roadmap-genesis-mythos-master-20260323-deepen-suggested-250`). **`state_hygiene_failure` is therefore already remediated on disk** (likely applied by the parent between validator write and this IRA read). Remaining work targets **residual** `missing_task_decomposition` / `safety_unknown_gap` at honest tertiary draft altitude — treat validator wording as a **weak minimum** and expand coverage.

## Structural discrepancies

1. **Stale validator premise vs live files:** First-pass report is **obsolete** for frontmatter mismatch; do not re-apply duplicate `68/85` writes.
2. **Phase 3.4.1** (`phase-3-4-1-ambient-slice-taxonomy-and-schedule-binding-roadmap-2026-03-23-1620.md`): Open **Tasks** and **Acceptance sketch** checkboxes without an explicit DEFER/BLOCKED ledger — supports `missing_task_decomposition`.
3. **Safety / unknown gaps:** `handoff_gaps` and research synthesis correctly cite **D-032**, **D-044**, **D-045**, **D-047**, **D-048**; automation consumers still benefit from **one** consolidated “provisional until …” ledger in-note (reduces false “delegatable” reads).

## Proposed fixes (for parent Roadmap subagent — apply under gates)

See structured return `suggested_fixes[]` in parent hand-off. Apply order: low → medium; snapshot `workflow_state` / `roadmap-state` / phase note per roadmap rules before structural edits.

## Notes for future tuning

- **roadmap-deepen post-append:** Ensure the skill **always** updates `last_ctx_util_pct` / `last_conf` in the **same** edit as the new log row (or immediately after) so first-pass validators never see a race where the log row is newer than frontmatter.
- **Tiered policy:** When `state_hygiene_failure` is cleared, expect compare-final to downgrade to **needs_work** for tertiary drafts with open Tasks — that is **not** a regression; document in Run-Telemetry.
