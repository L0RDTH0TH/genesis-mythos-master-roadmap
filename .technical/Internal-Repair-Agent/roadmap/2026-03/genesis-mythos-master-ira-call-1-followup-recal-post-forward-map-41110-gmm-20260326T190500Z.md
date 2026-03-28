---
created: 2026-03-26
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: followup-recal-post-forward-map-41110-gmm-20260326T190500Z
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 1
  medium: 2
  high: 1
---

## Context

Called after roadmap handoff validator reported `severity: high`, `recommended_action: block_destructive`, and `primary_code: state_hygiene_failure` for conceptual-track `RESUME_ROADMAP` (`action: recal`). The blocking issue is mirror divergence: `distilled-core` and phase notes claim stale machine cursor authority that contradicts `workflow_state`.

## Structural discrepancies

1. `workflow_state.md` is currently authoritative (`last_auto_iteration: resume-forward-map-phase-41110-gmm-20260326T180000Z`, `current_subphase_index: 4.1.1.10`), but mirror artifacts present stale/contradictory cursor IDs.
2. `distilled-core.md` still advertises prior iteration as live authority.
3. Phase 4 primary roadmap note still advertises a mismatched older cursor line.
4. Phase 4.1.1.10 task note contains stale "Canonical machine cursor" text.
5. Mirror notes do not carry a standardized "single-source authority" clause pointing to `workflow_state` as canonical.

## Proposed fixes

1) **Low risk**  
- **action_type:** `add_authority_clause`  
- **target_path:** `1-Projects/genesis-mythos-master/Roadmap/distilled-core.md`  
- **description:** Add one explicit sentence: `workflow_state` frontmatter plus first physical deepen row is the only authoritative machine cursor source.  
- **constraints:** Add as a short clause without rewriting unrelated sections.

2) **Medium risk**  
- **action_type:** `rewrite_cursor_mirror`  
- **target_path:** `1-Projects/genesis-mythos-master/Roadmap/distilled-core.md`  
- **description:** Replace stale live-cursor claim with current values from `workflow_state` and move prior IDs into a clearly labeled historical line.  
- **constraints:** Preserve existing chronology and do not delete old IDs; demote them to history only.

3) **Medium risk**  
- **action_type:** `rewrite_cursor_mirror`  
- **target_path:** `1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems/phase-4-perspective-split-and-control-systems-roadmap-2026-03-19-1101.md`  
- **description:** Update the "current machine cursor" statement to match `workflow_state` (`resume-forward-map-phase-41110-gmm-20260326T180000Z`, `4.1.1.10`) and historicalize old cursor references.  
- **constraints:** Touch only authority/header block and keep roadmap content unchanged.

4) **High risk**  
- **action_type:** `synchronize_task_note_authority_block`  
- **target_path:** `1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems/phase-4-1-1-10-auditable-path-check-contract-and-example-witness-appendix-roadmap-2026-03-25-0003.md`  
- **description:** Normalize "Canonical machine cursor" block to canonical values and introduce explicit "history vs active" split so downstream readers cannot mistake stale IDs as active authority.  
- **constraints:** If this note has downstream references to old phrasing, keep compatibility by retaining prior IDs under a `Historical cursor IDs` subsection.

## Notes for future tuning

- Recurrent issue pattern: cursor mirror text is manually duplicated across roadmap surfaces and drifts from `workflow_state`.
- Suggested hardening: generate mirror authority blocks from one template function and include an automated parity check before handoff validation.
