---
created: 2026-03-19
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: roadmap-setup-2026-03-12
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 5
  medium: 0
  high: 0
---

## Context

IRA was invoked from ROADMAP_MODE setup after a validator `needs_work` verdict (`severity: medium`) with reason codes for state hygiene, missing decomposition, missing command/event schemas, and missing end-to-end message flow example. Current artifacts are structurally present, but implementation-facing evidence is mostly placeholders.

## Structural discrepancies

1. `workflow_state.md` still contains placeholder context metrics in the latest log row (`Ctx Util %`, `Leftover %`, `Threshold`, `Est. Tokens / Window` are `-`), and frontmatter `last_ctx_util_pct` / `last_conf` are empty.
2. `roadmap-state.md` records a duplicate-state warning but has no explicit closeout marker proving normalization was completed.
3. `decisions-log.md` has only a setup entry and lacks concrete architecture decision anchors with stable IDs.
4. No artifact in the roadmap folder defines the requested module decomposition and phase-1 done-criteria roll-up.
5. No artifact in the roadmap folder defines v0 command/event schemas or a worked end-to-end message flow with failure branch checks.

## Proposed fixes

1. **Create a state hygiene closeout memo**
   - **action_type:** `write_log_entry`
   - **target_path:** `1-Projects/genesis-mythos-master/Roadmap/state-hygiene-closeout-2026-03-19.md`
   - **risk_level:** `low`
   - **description:** Add a dated memo that records duplicate-artifact reconciliation status, file-by-file checks, and one explicit `resolved: true` marker.
   - **constraints:** Only factual reconciliation notes; do not rewrite canonical state files in this fix.

2. **Append a closeout link in roadmap-state notes section**
   - **action_type:** `write_log_entry`
   - **target_path:** `1-Projects/genesis-mythos-master/Roadmap/roadmap-state.md`
   - **risk_level:** `low`
   - **description:** Add one bullet in `## Notes` linking to the closeout memo so validators have an explicit closure anchor.
   - **constraints:** Append-only; do not alter frontmatter keys or phase summary rows.

3. **Create a primary decomposition sheet**
   - **action_type:** `write_log_entry`
   - **target_path:** `1-Projects/genesis-mythos-master/Roadmap/phase-1-decomposition-sheet-v0.md`
   - **risk_level:** `low`
   - **description:** Define module/workstream boundaries (`world state`, `generation graph`, `simulation`, `rendering`, `input`) with one owner/scope sentence each and a roll-up checklist tied to Phase 1 done-criteria.
   - **constraints:** New note only; avoid renames/moves.

4. **Create command/event schema v0**
   - **action_type:** `write_log_entry`
   - **target_path:** `1-Projects/genesis-mythos-master/Roadmap/command-event-schema-v0.md`
   - **risk_level:** `low`
   - **description:** Define minimum command/event names, payload fields, and validation constraints for intent injection and seed snapshot flow.
   - **constraints:** Keep as v0 spec note; no pipeline behavior changes in this step.

5. **Create end-to-end message flow example v0 and decision anchors**
   - **action_type:** `rewrite_log_entry`
   - **target_path:** `1-Projects/genesis-mythos-master/Roadmap/decisions-log.md`
   - **risk_level:** `low`
   - **description:** Add 3-5 concrete decision entries with IDs (for architecture boundaries and safety invariants), then add one linked sequence example note showing `input -> generation graph -> world state update -> simulation tick -> render/input reflection` with one failure branch.
   - **constraints:** Append decisions only; preserve existing setup entry.

## Notes for future tuning

- ROADMAP setup passes often leave placeholder context metrics that trigger repeated hygiene findings; setup templates should include a first non-placeholder log row shape.
- Validators benefit from explicit closeout links in `roadmap-state.md` even when normalization work happened elsewhere.
