---
created: 2026-03-22
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: resume-roadmap-genesis-mythos-master-20260322-deepen-followup-235
ira_call_index: 1
status: repair_plan
risk_summary: { low: 2, medium: 2, high: 1 }
parent_run_id: l1-eatq-20260322-gmm-0015-a7f3c2
validator_report_path: .technical/Validator/roadmap-auto-validation-genesis-mythos-master-20260322T001600Z.md
---

# IRA report — roadmap (validator first pass)

## Context

RoadmapSubagent invoked IRA after nested `roadmap_handoff_auto` first pass (`severity: medium`, `recommended_action: needs_work`, `primary_code: safety_unknown_gap`). Validator cites multiple incompatible **"Latest deepen"** bullets in `roadmap-state.md` **Notes**. Workflow truth is `current_subphase_index: "3.1.2"` and last log row `queue_entry_id …-235` on `workflow_state.md`. Contaminated-report rule: treat the validator gap as a **floor** — also fix navigation order (deepen bullets before **Active phase**) and surface authority so future appends do not reintroduce duplicate "Latest".

## Structural discrepancies

1. **Eight** lines in `## Notes` begin with `- Latest deepen (` — only one subphase can be "latest" for operators and grep.
2. **Phase 3.1.2** is the live cursor (matches `workflow_state`); labels should say **3.1.2**, not vague "Phase 3.1 tertiary" alone, to match `current_subphase_index`.
3. **Ordering**: `Latest deepen (Phase 1.1 closure)` appears **above** **Active phase (primary)** and **Prior macro phase**, which invites reading stale work as current.
4. Validator secondary: research note filename time `2205` vs run `00:16` is unexplained in Notes — weak trust signal; document as TZ/synthetic suffix in Notes only (optional in medium fix).

## Proposed fixes

See parent return `suggested_fixes[]` (stable low → medium → high). Apply only under roadmap snapshot + backup gates.

## Notes for future tuning

- **roadmap-deepen** (or append templates): when writing Notes bullets, use **Prior deepen (historical)** for any subphase that is not the new current `current_subphase_index`, or stop appending per-spine "Latest" lines and only maintain one canonical row updated in-place.
- Consider a single **machine-updated** field in frontmatter for `last_deepen_note` to reduce human-section drift (backlog; not part of this Notes-only repair).
