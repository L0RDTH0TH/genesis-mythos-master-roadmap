---
created: 2026-03-21
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: resume-roadmap-genesis-mythos-master-20260321-followup-deepen-next-followup-next
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 3
  medium: 0
  high: 0
validator_report_path: .technical/Validator/roadmap-auto-validation-genesis-mythos-master-20260321T221800Z.md
parent_run_id: queue-eat-20260321-gmm-deepen-1
---

# IRA — roadmap / RESUME_ROADMAP deepen (genesis-mythos-master)

## Context

Post–nested-validator IRA after `roadmap_handoff_auto` reported `medium` / `needs_work`, primary `safety_unknown_gap`, secondary `missing_task_decomposition`. Operator states **vault-follow** on Phase **2.3.4** is already fixed: Tasks show `[x]` with lineage to `distilled-core` + `roadmap-state` (`version: 14`), matching live wikilinks in those files. **Scope here:** doc hygiene only — no execution/VCS checklist edits. `missing_task_decomposition` remains legitimately open until PR evidence exists; do not treat as vault-doc repair.

## Structural discrepancies (doc layer)

1. **Stale validator snapshot:** Report `roadmap-auto-validation-genesis-mythos-master-20260321T221800Z.md` still describes vault-follow as unchecked vs sibling files; creates confusion when reconciling automation vs vault truth after the checkbox fix.
2. **Weak upstream navigation:** `phase-2-3-4-…2339.md` `links` frontmatter lists siblings and `decisions-log` but not the **Phase 2 primary** parent note, unlike typical breadcrumb expectations and validator “primary MOC / hub” guidance.
3. **Consistency report gap:** `roadmap-state.md` § Consistency reports (2026-03-21 23:39) does not record that vault-follow reconcile post-dates the 221800Z validator read, so humans comparing report + state lack a single anchor.

## Proposed fixes (caller applies under snapshot/backup rules)

See structured `suggested_fixes[]` in parent return.

## Notes for future tuning

- Consider having `roadmap_handoff_auto` compare checkbox text to `distilled-core`/`roadmap-state` wikilink presence when scoring `safety_unknown_gap`, or require validator `compare_to_report_path` runs to refresh “verbatim gap” citations after IRA-applied hygiene.
- Tertiary notes could standardize a `links` entry for the owning **primary** phase container to reduce graph orphaning.
