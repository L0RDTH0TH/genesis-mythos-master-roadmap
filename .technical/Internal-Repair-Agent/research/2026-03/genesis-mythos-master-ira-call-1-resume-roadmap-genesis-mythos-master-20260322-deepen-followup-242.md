---
created: 2026-03-22
pipeline: research
project_id: genesis-mythos-master
queue_entry_id: resume-roadmap-genesis-mythos-master-20260322-deepen-followup-242
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 3
  medium: 4
  high: 1
validator_report_path: .technical/Validator/research-synthesis-phase-3-2-3-gmm-20260322T183600Z-first.md
parent_run_id: prq-20260322-1748-genesis-deepen
---

# IRA call 1 — research synthesis (Phase 3.2.3)

## Context

Validator-driven invocation after first hostile pass on `research_synthesis` for genesis-mythos-master. Verdict: `needs_work`, primary `missing_task_decomposition`, secondary `safety_unknown_gap`. The synthesis note is narrative scaffolding: it defers preimage decisions to a checklist, leaves multi-regen ordering unpinned, uses optional-row language without decision criteria, and cites blog/forum sources for normative idempotency claims. Crash/replay boundary for `ledger-hit` is absent. IRA treats the validator gaps as a **minimum**; the repair plan closes spec holes **inside** the allowed edit surface: `Ingest/Agent-Research/phase-3-2-3-replay-regen-ledger-tickcommit-serialization-research-2026-03-22-1830.md` only.

## Structural discrepancies

1. **missing_task_decomposition:** Section 4 checklist says "document later" instead of in-note mapping of digests to `TickCommitRecord_v0` preimage fields.
2. **missing_task_decomposition:** No worked example with two regens, explicit order, and hash placeholders tying sequence to merge to commit.
3. **safety_unknown_gap:** Section 3 step 2 references "StableMergeKey-style" without a named tuple, endianness, or collision-avoidance contract versus player/DM lane.
4. **missing_task_decomposition:** `regen_subgraph_outcome_row` "optional split" lacks a test-golden rule (when required versus folded).
5. **safety_unknown_gap:** Section 2 idempotency backed partly by Stack Overflow / Medium for semantics that must be fail-closed in spec.
6. **safety_unknown_gap:** No statement on **when** the regen ledger is durable relative to tick commit, or how replay reproduces `ledger-hit` after crash or truncation without double-apply.

## Proposed fixes

See structured `suggested_fixes` returned to the Research pipeline caller; each targets only the synthesis path above.

## Notes for future tuning

- Research synthesis validator repeatedly flags **deferred deliverables** masquerading as complete notes; enforce "no checklist hand-off" in research agent template for tertiary serialization phases.
- **Web source tiering** in research skill: auto-tag SO/Medium as reading-list unless paired with primary spec or vault norm.
- Multi-regen ordering should default to **explicit tuple in note** or **single-regen invariant** — avoid "-style" phrasing without a vault link to the actual type.
