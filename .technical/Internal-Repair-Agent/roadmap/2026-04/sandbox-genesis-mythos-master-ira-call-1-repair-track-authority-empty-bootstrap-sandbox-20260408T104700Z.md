---
created: 2026-04-08
pipeline: roadmap
project_id: sandbox-genesis-mythos-master
queue_entry_id: repair-track-authority-empty-bootstrap-sandbox-20260408T104700Z
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 3
  medium: 1
  high: 0
---

## Context

Validator handoff reported `severity: medium`, `recommended_action: needs_work`, with primary `safety_unknown_gap` and secondary `state_hygiene_failure`. Scope is restricted to hygiene edits in `workflow_state.md`, `roadmap-state.md`, and `decisions-log.md`. No frozen conceptual phase-body edits are allowed.

## Structural discrepancies

1. `workflow_state.md` keeps `current_subphase_index: "6"` as an active scalar while authority is execution-only (`conceptual_cursor_authority: advisory_only`), which is parse-risky for consumers that ignore inline comments.
2. `workflow_state.md` lacks an explicit machine-safe hard gate flag that blocks conceptual deepen dispatch under execution authority.
3. `decisions-log.md` contains the repair row but only states `queue_mutation: none` without explicit stale-intent disposition semantics (consumed/invalidated/quarantined) for conceptual deepen lines.
4. `roadmap-state.md` already sets `roadmap_track: execution`, but there is no concise state-hygiene guard note in the state body cross-linking machine-safe conceptual-block semantics.

## Proposed fixes

1. **[low] Add hard conceptual-dispatch gate in workflow frontmatter**
   - `action_type`: `adjust_frontmatter`
   - `target_path`: `1-Projects/sandbox-genesis-mythos-master/Roadmap/workflow_state.md`
   - `description`: Add `conceptual_deepen_permitted: false` beside `conceptual_cursor_authority: advisory_only` so machine readers have a boolean gate independent of comments.
   - `constraints`: Only apply when `roadmap-state.md` still has `roadmap_track: execution`.

2. **[medium] Convert conceptual cursor to execution-safe sentinel**
   - `action_type`: `set_context_metrics`
   - `target_path`: `1-Projects/sandbox-genesis-mythos-master/Roadmap/workflow_state.md`
   - `description`: Replace active scalar `current_subphase_index: "6"` with a non-routable sentinel for conceptual track (for example `"EXECUTION_TRACK_ACTIVE"`), and move prior `"6"` into a namespaced archival key (for example `conceptual_cursor_last_seen: "6"`).
   - `constraints`: Preserve historical meaning in `## Log`; do not alter phase notes or execution state files.

3. **[low] Add explicit stale-intent disposition line in decisions log**
   - `action_type`: `write_log_entry`
   - `target_path`: `1-Projects/sandbox-genesis-mythos-master/Roadmap/decisions-log.md`
   - `description`: Append one repair follow-up bullet for `repair-track-authority-empty-bootstrap-sandbox-20260408T104700Z` with structured disposition fields such as `conceptual_deepen_stale_intents: quarantined_or_consumed`, `disposition_scope: conceptual_only`, and a cite to the validator report path.
   - `constraints`: Hygiene-only append; no queue file edits from IRA; no claim of queue mutation if not independently evidenced.

4. **[low] Add concise authority guard note in roadmap-state body**
   - `action_type`: `rewrite_log_entry`
   - `target_path`: `1-Projects/sandbox-genesis-mythos-master/Roadmap/roadmap-state.md`
   - `description`: Add a short note under consistency/status section that conceptual cursor fields are non-authoritative when `roadmap_track: execution`, and routing must use execution state files.
   - `constraints`: Body hygiene note only; do not edit frozen conceptual phase bodies.

## Notes for future tuning

- Prefer explicit booleans/sentinels over prose comments for dispatch gates.
- Keep conceptual cursor archival values separate from active routing keys to avoid parser ambiguity.
- Require stale-intent disposition metadata in decisions-log whenever validator reports `safety_unknown_gap` + `queue_mutation: none`.
