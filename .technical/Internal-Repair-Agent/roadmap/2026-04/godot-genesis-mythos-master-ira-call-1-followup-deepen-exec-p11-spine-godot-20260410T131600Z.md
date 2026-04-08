---
created: 2026-04-07
pipeline: roadmap
project_id: godot-genesis-mythos-master
queue_entry_id: followup-deepen-exec-p11-spine-godot-20260410T131600Z
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 2
  medium: 2
  high: 1
---

## Context

IRA invoked after a high-severity `roadmap_handoff_auto` validator verdict (`block_destructive`) for execution-track `RESUME_ROADMAP` deepen. The blocker is coherent-state failure: execution tertiary `1.1.1` exists, but workflow cursor/lineage and roll-up closure evidence are not synchronized with that mint.

## Structural discrepancies

1. `workflow_state-execution.md` has `current_subphase_index: "1.1"` while execution tertiary `Phase-1-1-1-Execution-Layer-Boundary-and-Commit-Pipeline-Roadmap-2026-04-10-1316.md` is already minted.
2. `workflow_state-execution.md` latest deepen row says "Next: deepen 1.1.1" rather than recording the `1.1.1` mint closure row.
3. `workflow_state-execution.md` lineage in log rows uses `parent_run_id: eatq-godot-followup-deepenexec-20260407T120000Z`, while validator handoff facts expect `eatq-godot-20260407T120000Z`.
4. `roadmap-state-execution.md` Phase 1 summary claims tertiary mirror minted and roll-up target context, but the workflow chronology does not yet provide explicit closure row/evidence linkage for `1.1.1 -> 1.1`.
5. Roll-up gates remain open (`rollup_1_1_from_1_1_1`, `rollup_1_primary_from_1_1`) with no explicit promoted evidence links from tertiary gates into secondary and then primary.

## Proposed fixes

1. **Fix workflow chronology row for minted tertiary**
   - risk_level: low
   - action_type: rewrite_log_entry
   - target_path: `1-Projects/godot-genesis-mythos-master/Roadmap/Execution/workflow_state-execution.md`
   - apply steps:
     - Insert a dedicated `deepen` log row at mint timestamp (or immediately after existing 13:16 row) explicitly stating `target = .../Phase-1-1-1-Execution-...-2026-04-10-1316`.
     - Move current "Next: deepen 1.1.1" phrasing to "Next: 1.1 roll-up hardening from minted 1.1.1 evidence".
     - Include queue metadata fields in-row (`queue_entry_id`, `parent_run_id`, `ctx_token_strategy`) matching this queue entry.
   - constraints:
     - Preserve chronological order in table rows.
     - Do not mutate conceptual workflow file.

2. **Align workflow cursor to true active node post-mint**
   - risk_level: medium
   - action_type: set_context_metrics
   - target_path: `1-Projects/godot-genesis-mythos-master/Roadmap/Execution/workflow_state-execution.md`
   - apply steps:
     - Keep `current_phase: 1`.
     - Set `current_subphase_index` to the post-mint active node for roll-up (`"1.1"` if roll-up is next target) and ensure log "Status / Next" explicitly references roll-up, not tertiary mint.
     - Update `last_auto_iteration` and optional context metrics only if an actual row append occurs.
   - constraints:
     - Cursor value and latest log row target/next text must agree.
     - No phase promotion while roll-up gates remain open.

3. **Repair run lineage consistency for this deepen pass**
   - risk_level: medium
   - action_type: recompute_phase_metadata
   - target_path: `1-Projects/godot-genesis-mythos-master/Roadmap/Execution/workflow_state-execution.md`
   - apply steps:
     - Normalize `parent_run_id` references in the affected 13:15/13:16 deepen rows to one canonical id from the queue handoff (`eatq-godot-20260407T120000Z`).
     - Keep `queue_entry_id: followup-deepen-exec-p11-spine-godot-20260410T131600Z` on the row that represents this pass.
     - If preserving old lineage is required, append explicit `lineage_correction` note in row text instead of silent replacement.
   - constraints:
     - Never create mixed lineage ids for same queue entry in same table segment.

4. **Reconcile roadmap-state execution summary with verified workflow evidence**
   - risk_level: low
   - action_type: rewrite_log_entry
   - target_path: `1-Projects/godot-genesis-mythos-master/Roadmap/Execution/roadmap-state-execution.md`
   - apply steps:
     - Keep tertiary minted claim only if workflow row explicitly records 1.1.1 mint.
     - Add a compact lineage note in Phase 1 summary referencing corrected workflow row and active gate status.
     - Ensure "next structural target" mirrors workflow (`1.1 roll-up hardening`).
   - constraints:
     - Summary must be derivative of workflow evidence, not ahead of it.

5. **Close roll-up evidence chain `1.1.1 -> 1.1` before any destructive advancement**
   - risk_level: high
   - action_type: mark_snapshot_link
   - target_path: `1-Projects/godot-genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layering-and-Interface-Contracts/Phase-1-1-Execution-Layering-and-Interface-Contracts-Roadmap-2026-04-10-1316.md` (plus workflow gate tracker)
   - apply steps:
     - In 1.1 secondary note, add explicit roll-up section linking tertiary evidence rows (`rollup_1_1_from_1_1_1`, `G-1.1-Commit-Seam`, `G-1.1-Boundary-Isolation`) with pass/fail rationale.
     - Update workflow gate tracker `rollup_1_1_from_1_1_1` from `open` to `closed` only after links resolve to concrete rows.
     - Propagate closure readiness to `rollup_1_primary_from_1_1` as `in-progress` (not closed) until phase-1 primary absorbs the roll-up.
   - constraints:
     - Requires per-change snapshots on touched roadmap execution notes before structural edits.
     - If evidence cannot be substantiated, keep gate `open` and return `#review-needed` (no phase advance).

## Notes for future tuning

- Recurrent pattern: state summary gets ahead of workflow chronology when same-minute mints occur.
- Add a roadmap-deepen postcondition check: if tertiary file minted, require same-run workflow row with matching target path and lineage tuple before updating roadmap-state summary.
- Consider a lineage canonicalization helper to prevent parent_run_id drift across follow-up entries.
---
created: 2026-04-07
pipeline: roadmap
project_id: godot-genesis-mythos-master
queue_entry_id: followup-deepen-exec-p11-spine-godot-20260410T131600Z
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 2
  medium: 1
  high: 0
---

## Context

Single-cycle IRA plan for `RESUME_ROADMAP` execution-track handoff repair on Phase 1.1 secondary. Triggered by validator verdict `severity: medium`, `recommended_action: needs_work`, with primary blocker `missing_roll_up_gates` and additional gaps `missing_risk_register_v0`, `missing_interface_spec_detail`.

## Structural discrepancies

1. Roll-up/gate closure is explicitly deferred in the target note, so the execution handoff has no gate closure criteria.
2. No risk register section exists for this execution slice; risk ownership and fallback logic are absent.
3. Interfaces are listed as stubs only; no signature-level contracts, failure enums, or invariants are documented.

## Proposed fixes

1. **R1 (low)**  
   - **Target**: `1-Projects/godot-genesis-mythos-master/Roadmap/Execution/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layering-and-Interface-Contracts/Phase-1-1-Execution-Layering-and-Interface-Contracts-Roadmap-2026-04-10-1316.md`  
   - **Action type**: `add_rollup_gates_block`  
   - **Patch intent**: Insert a `## Roll-up gates (execution_v1)` section with 3-5 concrete gates, each including pass criteria, required evidence artifact path(s), owner, and status placeholder. Replace "CI and HR rollup gates deferred" language with explicit gated criteria for this secondary.  
   - **Why**: Directly resolves `missing_roll_up_gates` by converting deferral into auditable gate closure metadata required by execution handoff.

2. **R2 (low)**  
   - **Target**: same target note as R1  
   - **Action type**: `add_risk_register_v0`  
   - **Patch intent**: Add `## Risk register v0 (Phase 1.1)` with at least three rows: risk, trigger signal, mitigation owner, fallback/rollback, and gate impact. Include one risk each for commit authority seam, interface drift, and failure propagation mismatch.  
   - **Why**: Resolves `missing_risk_register_v0` by adding first-pass execution risk governance tied to ownership and fallback paths.

3. **R3 (medium)**  
   - **Target**: same target note as R1  
   - **Action type**: `upgrade_interface_spec_detail`  
   - **Patch intent**: Replace `## Interface stubs (execution-shaped)` bullets with signature-level contract blocks for `IWorldCommitGateway` plus adjacent interfaces (`IWorldReadModel`, `ISimulationStepper`, `IRenderViewAdapter`, `IIntentIngress`): method signatures, typed inputs/outputs, failure enums, and non-negotiable invariants. Add cross-reference from pseudocode error paths to named failure enums.  
   - **Why**: Resolves `missing_interface_spec_detail` by promoting stubs to implementation-ready contract detail and explicit failure semantics.

## Notes for future tuning

- Execution secondaries repeatedly pass structural checks but fail handoff on closure artifacts; add a pre-validator checklist in roadmap-deepen for roll-up gates + risk register + interface contract granularity.
- Keep `handoff_readiness` pinned below 85 until all three artifacts are present and cross-linked.
