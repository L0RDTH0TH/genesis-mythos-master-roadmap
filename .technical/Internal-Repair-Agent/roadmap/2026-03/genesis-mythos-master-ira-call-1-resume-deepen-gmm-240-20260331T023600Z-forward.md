---
created: 2026-03-30
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: resume-deepen-gmm-240-20260331T023600Z-forward
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 1
  medium: 2
  high: 1
---

## Context

IRA invoked for `RESUME_ROADMAP` (`action: deepen`) after nested validator reported `needs_work` with `missing_task_decomposition` and `safety_unknown_gap` on the Phase 2.4 secondary slice. The secondary note exists and cursor is at `2.4.1`, but no tertiary decomposition exists yet and decisions-log does not yet capture the 2.4 defer-expiry selection.

## Structural discrepancies

1. Missing tertiary decomposition artifact under `Phase-2-4-Post-Validation-Commit-Orchestration` for explicit `commit` / `deny_commit` / `defer` branch contracts and deterministic precedence.
2. Phase 2.4 secondary note has behavior-level ordering but lacks acceptance-criteria rows proving commit-block parity against Phase 2.3 diagnostics provenance.
3. `decisions-log.md` has no Phase 2.4-specific defer-expiry decision row with queue reference and consuming-slice backlinks.
4. Safety ambiguity remains because branch authority semantics are described narratively without explicit deterministic branch table plus acceptance checks.

## Proposed fixes

1. **[medium]** Create tertiary note `Phase-2-4-1-Commit-Deny-Defer-Branch-Decomposition-and-Deterministic-Precedence-Roadmap-2026-03-31-*.md` in the existing 2.4 folder.
   - Action type: `create_tertiary_decomposition_note`
   - Constraints: use `roadmap-level: tertiary`, `subphase-index: "2.4.1"`, include deterministic precedence matrix (`commit > deny_commit > defer` only when preconditions satisfy), explicit deny triggers, defer expiry contract.
   - Why: closes primary validator gap (`missing_task_decomposition`) and provides executable handoff shape.

2. **[medium]** Update `Phase-2-4-Post-Validation-Commit-Orchestration-Roadmap-2026-03-31-0236.md` with a new `## Acceptance criteria` block.
   - Action type: `add_acceptance_criteria_block`
   - Constraints: include at least 4 criteria mapping commit-block parity checks to 2.3 artifacts (`2.3.2` failure payload contract + `2.3.5` projection ordering provenance), and one negative criterion for stale projection ordering.
   - Why: removes safety ambiguity by converting narrative guarantees into checkable pass/fail criteria.

3. **[low]** Append one row under `## Decisions` in `decisions-log.md` for Phase 2.4 defer-expiry policy.
   - Action type: `append_decision_log_row`
   - Constraints: include decision id, selected defer expiry model, queue reference `resume-deepen-gmm-240-20260331T023600Z-forward`, backlinks to 2.4 secondary + 2.4.1 tertiary note.
   - Why: preserves operator-pick traceability continuity and aligns with existing decisions-log conventions.

4. **[high]** Re-run `roadmap_handoff_auto` compare pass against `.technical/Validator/roadmap-handoff-auto-genesis-mythos-master-20260331T023600Z-conceptual-v1-post-2-4.md` after applying fixes.
   - Action type: `rerun_validator_compare_pass`
   - Constraints: compare-to report path required; if `missing_task_decomposition` persists, block success and require follow-up tertiary refinement before next deepen.
   - Why: verifies repairs actually close the cited gaps and prevents false-green continuation.

## Notes for future tuning

- Recurrent pattern: secondary slices are being minted with strong behavior prose but validator expects tertiary decomposition before handoff-auto passes cleanly.
- Suggest adding an internal post-deepen checklist gate for secondary slices that enforces either immediate tertiary seed or explicit decomposition scaffold marker.
