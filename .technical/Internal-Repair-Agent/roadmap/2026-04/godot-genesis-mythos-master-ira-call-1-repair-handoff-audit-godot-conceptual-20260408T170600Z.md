---
created: 2026-04-08
pipeline: roadmap
project_id: godot-genesis-mythos-master
queue_entry_id: repair-handoff-audit-godot-conceptual-20260408T170600Z
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 2
  medium: 3
  high: 1
---

## Context

Validator `roadmap_handoff_auto` reported `severity: high` with `state_hygiene_failure`, `contradictions_detected`, and `safety_unknown_gap`. The four target artifacts disagree on the canonical conceptual cursor and lifecycle state (notably `workflow_state.current_subphase_index: "6.2.3"` vs Phase 6 frontmatter `subphase-index: "1"`), and the primary Phase 6 note mixes closure-complete flags with active/incomplete lifecycle fields.

## Structural discrepancies

1. **Cursor mismatch across authoritative surfaces**
   - `workflow_state.md` frontmatter: `current_subphase_index: "6.2.3"`.
   - Phase 6 primary note frontmatter: `subphase-index: "1"`.
2. **Lifecycle contradiction in Phase 6 note**
   - `phase6_primary_checklist: complete` and `phase6_primary_rollup_nl_gwt: complete` coexist with `status: active` and `progress: 80`.
3. **Stale decision-log hygiene anchor**
   - Decisions log contradiction-closure hygiene line still cites `workflow_state.current_subphase_index: "6.2.1"` for lineage now at `6.2.3`.
4. **Ambiguous routing after completion claims**
   - `roadmap-state.md` remains `status: generating` while closure language and rollup completion claims imply a post-rollup decision point.
5. **Missing explicit immediate-next-action sentence parity**
   - Validator asks for one explicit conceptual next-action sentence in both `roadmap-state.md` and `workflow_state.md`; current language is distributed but not single-sentence normalized.

## Proposed fixes

1. **Normalize Phase 6 cursor index to canonical conceptual cursor**
   - `action_type`: adjust_frontmatter
   - `target_path`: `1-Projects/godot-genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-Prototype-Assembly-Testing-and-Iteration-Roadmap-2026-03-30-0430.md`
   - `target_fields`:
     - `subphase-index`
   - `from_to`:
     - `subphase-index: "1" -> "6.2.3"`
   - `risk_level`: low
   - `constraints`:
     - Do not alter body sections; frontmatter-only correction.
     - Keep `roadmap-level: primary` and existing links unchanged.

2. **Reconcile Phase 6 lifecycle semantics with completion flags**
   - `action_type`: adjust_frontmatter
   - `target_path`: `1-Projects/godot-genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-Prototype-Assembly-Testing-and-Iteration-Roadmap-2026-03-30-0430.md`
   - `target_fields`:
     - `status`
     - `progress`
   - `from_to`:
     - `status: active -> complete`
     - `progress: 80 -> 100`
   - `risk_level`: medium
   - `constraints`:
     - Apply only if `phase6_primary_checklist: complete` and `phase6_primary_rollup_nl_gwt: complete` remain true.
     - If caller wants non-terminal semantics, set explicit non-terminal marker in a separate field (do not keep implicit contradiction).

3. **Refresh contradiction-closure hygiene anchor in decisions-log**
   - `action_type`: rewrite_log_entry
   - `target_path`: `1-Projects/godot-genesis-mythos-master/Roadmap/decisions-log.md`
   - `target_fields`:
     - `## Conceptual autopilot` entry: `Contradiction-closure hygiene (empty-bootstrap-godot-20260408T103834Z, 2026-04-08)`
   - `from_to`:
     - `workflow_state.current_subphase_index: "6.2.1" -> "6.2.3"`
   - `risk_level`: medium
   - `constraints`:
     - Preserve historical queue id and reason-code mapping.
     - Append clarification if strict append-only policy is required by caller.

4. **Resolve roadmap-state safety ambiguity with explicit conceptual routing sentence**
   - `action_type`: write_log_entry
   - `target_path`: `1-Projects/godot-genesis-mythos-master/Roadmap/roadmap-state.md`
   - `target_fields`:
     - `status`
     - `## Consistency reports (RECAL-ROAD)` new dated bullet
   - `from_to`:
     - `status: generating -> in-progress` (or `complete` if caller treats 6.2.3 as terminal conceptual closure)
     - Add explicit sentence: `Immediate conceptual next action: deepen tertiary 6.2.3 under workflow_state current_subphase_index 6.2.3 (unless operator selects handoff-audit/recal).`
   - `risk_level`: high
   - `constraints`:
     - Caller must choose terminal vs non-terminal intent before applying.
     - Keep `roadmap_track: execution` untouched; this is lane default, not cursor authority.

5. **Add matching immediate-next-action sentence in workflow_state**
   - `action_type`: write_log_entry
   - `target_path`: `1-Projects/godot-genesis-mythos-master/Roadmap/workflow_state.md`
   - `target_fields`:
     - frontmatter-adjacent authority narrative block (or nearest explicit authority section)
   - `from_to`:
     - Add explicit sentence: `Immediate conceptual next action for this lineage is tertiary 6.2.3 (cursor authority: workflow_state.current_subphase_index).`
   - `risk_level`: medium
   - `constraints`:
     - Keep existing `cursor_authority_model` and `cursor_authority_queue_lock` values.
     - Ensure wording matches roadmap-state sentence verbatim on action and index.

6. **Optional hygiene: add one reconciliation note in Phase 6 body to avoid future stale frontmatter drift**
   - `action_type`: write_log_entry
   - `target_path`: `1-Projects/godot-genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-Prototype-Assembly-Testing-and-Iteration-Roadmap-2026-03-30-0430.md`
   - `target_fields`:
     - `### Progress semantics (frontmatter)` section
   - `from_to`:
     - Add one line that primary note frontmatter index/lifecycle mirrors workflow cursor authority for conceptual lineage.
   - `risk_level`: low
   - `constraints`:
     - Single-line additive note; no section restructuring.

## Notes for future tuning

- This failure pattern is recurring: stale contradiction-hygiene entry pins an old cursor while new conceptual deepens progress the line.
- A lightweight guard could validate that any decisions-log entry mentioning `workflow_state.current_subphase_index` matches frontmatter at write time.
- Lifecycle consistency checks should assert `(checklist complete + rollup complete) => status/progress closure` unless explicit non-terminal override is present.
