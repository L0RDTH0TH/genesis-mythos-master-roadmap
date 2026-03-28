---
created: 2026-03-19
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: resume-roadmap-genesis-mythos-master-2026-03-19-114230-next-next
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 6
  medium: 0
  high: 0
---

## Context

Validator-driven IRA call for `RESUME_ROADMAP` with `recommended_action: needs_work` and reason codes `missing_task_decomposition` and `missing_test_plan`. Target artifact is coherent but lacks executable decomposition and test harness detail for delegatable handoff.

## Structural discrepancies

1. Objectives are present, but there are no task IDs, owner surfaces, I/O contracts, or done conditions.
2. Determinism gate contract exists, but no concrete implementation sequence mapped to tasks.
3. No executable test plan for determinism, idempotency conflicts, and rollback-window breaches.
4. Acceptance criteria are not measurable and not linked to specific tests.

## Proposed fixes

1. Add `## Task decomposition (v1)` with 8 tasks (`T1`-`T8`), each including `owner_surface`, `inputs`, `outputs`, and `done_condition`.
   - action_type: `write_log_entry`
   - target_path: `1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-and-Core-Architecture/phase-1-1-3-replay-determinism-gate-and-compensation-orchestrator-roadmap-2026-03-19-1200.md`
   - risk_level: `low`
2. Add `## Determinism gate execution plan` with sequence `S1`-`S6` mapped directly to task IDs (`S1 -> T1`, etc.) for ledger checks, checkpoint verify, and recovery transitions.
   - action_type: `write_log_entry`
   - target_path: same as above
   - risk_level: `low`
3. Add `## Executable test plan (v0)` with test IDs (`R1`-`R8`) covering replay determinism positive/negative, idempotency same-key/same-hash vs same-key/different-hash, rollback-window breach, and expected reason code per test.
   - action_type: `write_log_entry`
   - target_path: same as above
   - risk_level: `low`
4. Add `## Acceptance criteria (gated)` with measurable criteria (`A1`-`A4`) each linked to one or more `R*` tests and objectives.
   - action_type: `recompute_phase_metadata`
   - target_path: same as above
   - risk_level: `low`
5. Add reason-code mapping table: `reason_code -> trigger -> expected terminal_state` using only baseline codes unless explicitly versioned.
   - action_type: `rewrite_log_entry`
   - target_path: same as above
   - risk_level: `low`
6. Add `## Handoff pack` checklist that references decomposition, execution sequence, test matrix, and acceptance links.
   - action_type: `mark_snapshot_link`
   - target_path: same as above
   - risk_level: `low`

## Rationale

These changes are additive and local to one phase note, so risk is low while directly resolving both validator gaps.

## Notes for future tuning

- Recurring issue: tertiary roadmap notes can be architecture-strong but execution-light.
- Candidate template improvement for roadmap-deepen at depth >= 3: auto-seed decomposition + test-plan + acceptance sections.
