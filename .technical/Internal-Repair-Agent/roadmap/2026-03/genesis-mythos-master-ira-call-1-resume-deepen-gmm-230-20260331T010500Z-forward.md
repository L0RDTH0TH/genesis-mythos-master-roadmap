---
created: 2026-03-30
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: resume-deepen-gmm-230-20260331T010500Z-forward
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 1
  medium: 2
  high: 0
---

## Context

IRA invoked after nested validator first pass reported `severity: medium`, `recommended_action: needs_work`, and primary `missing_task_decomposition` for the conceptual Phase 2.3 slice. The repair scope is constrained to traceability and minimal prose alignment only, without minting a new `2.3.2` tertiary note in this cycle.

## Structural discrepancies

1. `decisions-log.md` has no `D-2.3.*` rows for two explicitly open policy questions already documented in `Phase 2.3` (`operator diagnostics granularity` and `warm-cache shortcut policy`).
2. `Phase 2.3` open-question bullets are not linked to stable decision IDs, so traceability from note prose to log entries is missing.
3. `Phase 2.3.1` "Downward" section references future split areas (`2.3.2+`) but does not anchor those split areas to decision IDs, leaving decomposition continuity implicit.

## Proposed fixes

1. **[low]** Add two new decision rows in `Roadmap/decisions-log.md` under `## Decisions`:
   - `D-2.3-diagnostics-granularity`
   - `D-2.3-warm-cache-shortcuts`
   Each row should include: date, explicit choice state (`execution-deferred` allowed), rationale, source note reference, and queue ref `resume-deepen-gmm-230-20260331T010500Z-forward`.
   - **Target:** `1-Projects/genesis-mythos-master/Roadmap/decisions-log.md`
   - **Constraints:** Keep existing ordering style and naming convention (`D-<subphase>-<slug>`). Do not rewrite unrelated historical rows.

2. **[medium]** Add minimal traceability clauses in Phase 2.3 open questions that point to the two new IDs:
   - diagnostics bullet ends with `(decision id: D-2.3-diagnostics-granularity)`
   - warm-cache bullet ends with `(decision id: D-2.3-warm-cache-shortcuts)`
   - **Target:** `1-Projects/genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building/Phase-2-3-Pipeline-Validation-and-Pre-Commit-Verification/Phase-2-3-Pipeline-Validation-and-Pre-Commit-Verification-Roadmap-2026-03-30-2140.md`
   - **Constraints:** Keep conceptual deferral language; no new implementation commitments; no section expansion beyond line-level alignment.

3. **[medium]** Add one short alignment sentence in Phase 2.3.1 "Downward" section to tie future split areas to the same two decision IDs (without minting 2.3.2):
   - Example intent: `Future 2.3.2 decomposition should consume D-2.3-diagnostics-granularity and D-2.3-warm-cache-shortcuts as policy anchors.`
   - **Target:** `1-Projects/genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building/Phase-2-3-Pipeline-Validation-and-Pre-Commit-Verification/Phase-2-3-1-Validation-Test-Plan-and-Acceptance-Criteria-Scaffold-Roadmap-2026-03-30-2140.md`
   - **Constraints:** No full tertiary decomposition/table rewrite; no new tasks beyond traceability mention.

## Notes for future tuning

- Recurrent pattern: conceptual slices are carrying open policy bullets without immediate `D-*` registration, causing predictable validator `safety_unknown_gap` findings.
- Suggest adding a roadmap-deepen post-step check: if an "Open questions" section contains policy forks, auto-propose matching `D-*` placeholders in `decisions-log.md` in the same run.
