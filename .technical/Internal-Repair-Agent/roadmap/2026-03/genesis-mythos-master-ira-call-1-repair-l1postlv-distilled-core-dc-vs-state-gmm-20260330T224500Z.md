---
created: 2026-03-30
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: repair-l1postlv-distilled-core-dc-vs-state-gmm-20260330T224500Z
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 0
  medium: 0
  high: 0
parent_run_id: pr-eat-20260330-gmm-pass3-repair-dc
---

# IRA — roadmap (post-first validator)

## Context

Post–nested-validator IRA for **RESUME_ROADMAP** `recal` after report `.technical/Validator/roadmap-handoff-auto-post-recal-rollup-2026-04-01T010000Z-genesis-mythos-master.md`. Verdict: **medium**, **needs_work**, **`safety_unknown_gap`**. RoadmapSubagent reported it already applied: (1) **workflow_state** `2026-04-01 00:45` recal row column alignment, (2) **distilled-core** `core_decisions` monotonic reorder (2.5.3 before 2.6 / 2.6.1). On-disk verification confirms both **validator next_artifacts** items are satisfied; no further structural edits are required for this pass.

## Structural discrepancies

1. **Resolved (was Gap A):** The `2026-04-01 00:45` **recal** row now has **five** `-` placeholders between **Current subphase** (`2.6.2`) and **Confidence** (`90`), matching the canonical 12-column **## Log** schema and the reference row `2026-04-01 00:10`.
2. **Resolved (was Gap B):** `distilled-core.md` frontmatter `core_decisions` lists **Phase 2.5.3** before **Phase 2.6** and **Phase 2.6.1** (monotonic phase-id order for rollup scanners).

## Proposed fixes

**None** — `suggested_fixes` returned empty to the caller; prior RoadmapSubagent edits already satisfy the validator’s **next_artifacts** checklist.

## Notes for future tuning

- After **compare_to_report_path** second validator pass, expect **`reason_codes`** to clear **`safety_unknown_gap`** if the report was stale relative to applied fixes.
- **Pattern:** recal rollup rows that append long **Status** prose should still be validated with a **pipe-count** or **column-index** sanity check before little val / validator to avoid repeated `-` drift.
