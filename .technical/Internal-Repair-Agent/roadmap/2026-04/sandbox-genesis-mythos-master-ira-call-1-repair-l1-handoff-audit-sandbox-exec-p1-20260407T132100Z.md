---
created: 2026-04-07
pipeline: roadmap
project_id: sandbox-genesis-mythos-master
queue_entry_id: repair-l1-handoff-audit-sandbox-exec-p1-20260407T132100Z
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 2
  medium: 2
  high: 0
---

## Context

Roadmap execution track invoked IRA after validator `roadmap_handoff_auto` returned `severity: medium`, `recommended_action: needs_work`, `primary_code: missing_roll_up_gates`, and `reason_codes: [missing_roll_up_gates, safety_unknown_gap]`. Current artifacts show Phase 1 primary exists, but roll-up closure remains open because 1.1 and 1.2 execution mirrors are not minted and closure evidence cells are still placeholders.

## Structural discrepancies

1. `roadmap-state-execution.md` roll-up table marks **1.1**, **1.2**, and **Primary rollup** as `Open` with no evidence links.
2. `workflow_state-execution.md` latest log row confirms next target is 1.1 and does not include closure evidence for Phase 1 roll-up gates.
3. Phase 1 execution note defines deferrals, but there is no explicit handoff-audit closure criterion tying deferred IDs to roll-up gating state updates.
4. Safety evidence is ambiguous: execution state claims progress while gate table remains unresolved, producing `safety_unknown_gap`.

## Proposed fixes

1. **[low]** Add explicit "gate-owner + expected evidence" metadata row in execution roll-up table to remove ambiguity for who closes each gate and with which artifact.
   - file: `1-Projects/sandbox-genesis-mythos-master/Roadmap/Execution/roadmap-state-execution.md`
   - constraints: only append rows/columns in the existing roll-up table; do not rewrite historical phase summaries.
2. **[medium]** Mint missing Phase 1.1 execution mirror at the declared parallel-spine path and add a stable wiki-link evidence reference in the roll-up table.
   - file: `1-Projects/sandbox-genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layering-and-Interface-Contracts/Phase-1-1-Layering-and-Interface-Contracts-Roadmap-2026-03-30-0500.md`
   - constraints: preserve execution-track frontmatter contract (`roadmap_track: execution`, `subphase-index: "1.1"`), and keep deferral IDs if still unresolved.
3. **[medium]** Mint missing Phase 1.2 execution mirror and add a stable wiki-link evidence reference in the roll-up table.
   - file: `1-Projects/sandbox-genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Schema-and-Data-Pipeline-Foundations/Phase-1-2-Schema-and-Data-Pipeline-Foundations-Roadmap-2026-03-30-0600.md`
   - constraints: use the same execution parallel-spine naming pattern as 1.1; avoid flattening under `Roadmap/Execution/`.
4. **[low]** After 1.1/1.2 mints, update workflow log with one explicit roll-up checkpoint row that states whether "Primary rollup" is now closed or still open with exact blocker IDs.
   - file: `1-Projects/sandbox-genesis-mythos-master/Roadmap/Execution/workflow_state-execution.md`
   - constraints: append-only in `## Log`; no retrospective edits of prior rows.

## Notes for future tuning

- Recurrent pattern: primary execution mirrors are minted before secondary gate rows are provisioned with closure owners, causing repeated `missing_roll_up_gates`.
- Suggested policy hardening: require a non-placeholder roll-up metadata row at first primary mint, even if secondary notes are still pending.
