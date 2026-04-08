---
created: 2026-04-08
pipeline: roadmap
project_id: sandbox-genesis-mythos-master
queue_entry_id: empty-bootstrap-sandbox-20260408T104041Z
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 5
  medium: 1
  high: 0
---

# IRA repair report - roadmap

## Context

Validator-first cycle returned `severity: medium`, `recommended_action: needs_work`, `primary_code: state_hygiene_failure`, `reason_codes: [state_hygiene_failure, contradictions_detected, safety_unknown_gap]`, with no validator report path provided. This plan keeps authority constrained to execution-track state surfaces and avoids any conceptual phase-note body edits, queue writes, or watcher writes.

## Structural discrepancies

1. Authority-surface drift risk: multiple roadmap state surfaces can re-state cursor/gate facts; if one diverges, validator flags state hygiene and contradictions.
2. Contradiction risk: stale "next action" prose can conflict with execution cursor (`current_subphase_index`) and tuple gate semantics.
3. Safety unknown gap risk: lingering broad uncertainty language may contradict the already-minted 1.2.2/1.2.3 execution chain and should be narrowed to attestation scope.
4. Provenance hygiene risk: some rows use synthetic/non-recorded correlation markers; this is acceptable only when explicitly bounded and non-claiming.

## Proposed fixes

1. **[low] Canonical tuple reassertion**
   - **action_type:** `set_context_metrics`
   - **target_path:** `1-Projects/sandbox-genesis-mythos-master/Roadmap/Execution/workflow_state-execution.md`
   - **description:** In frontmatter, keep and reassert only this Phase-1 closure tuple as canonical: `handoff_audit_status: closure_proof_attached_pending_compare`, `compare_validator_required: true`, and `current_subphase_index: "1.2.3"`.
   - **exact minimal action:** If any of these three fields drifted, patch only those field values back to the canonical tuple; do not modify other frontmatter keys.
   - **constraints:** Apply only if file exists and remains `roadmap_track: execution`.

2. **[low] Workflow log contradiction clamp**
   - **action_type:** `rewrite_log_entry`
   - **target_path:** `1-Projects/sandbox-genesis-mythos-master/Roadmap/Execution/workflow_state-execution.md`
   - **description:** Normalize the latest row for this queue family so "Status / Next" does not imply remint/deepen when cursor is already at `1.2.3`.
   - **exact minimal action:** In the most recent row referencing `followup-execution-deepen-empty-bootstrap-sandbox-20260408T164114Z` or this queue family, set `Next` text to: "execution handoff-audit compare closure pass" and keep "no remint/no flatten" language.
   - **constraints:** Edit only one row; do not reorder table rows.

3. **[low] Execution roadmap-state gate wording sync**
   - **action_type:** `rewrite_log_entry`
   - **target_path:** `1-Projects/sandbox-genesis-mythos-master/Roadmap/Execution/roadmap-state-execution.md`
   - **description:** Ensure all Phase 1 gate statements use one blocker tuple authority and avoid mixed blocker semantics.
   - **exact minimal action:** In `## Notes` and `Execution roll-up gate table`, keep `phase_1_rollup_closed: false` + `blocker_id: phase1_rollup_attestation_pending` wording as authoritative; remove any residual alternative blocker phrases if present.
   - **constraints:** No changes to phase summaries other than wording reconciliation.

4. **[medium] Conceptual advisory marker hardening**
   - **action_type:** `adjust_frontmatter`
   - **target_path:** `1-Projects/sandbox-genesis-mythos-master/Roadmap/workflow_state.md`
   - **description:** Prevent conceptual cursor text from being interpreted as live execution authority.
   - **exact minimal action:** Add or preserve a single explicit advisory sentence near execution references: conceptual cursor is non-authoritative while `roadmap_track: execution` is active; execution authority is `Execution/workflow_state-execution.md`.
   - **constraints:** Do not alter conceptual phase summaries or conceptual cursor values in this run.

5. **[low] Safety-unknown scope narrowing**
   - **action_type:** `write_log_entry`
   - **target_path:** `1-Projects/sandbox-genesis-mythos-master/Roadmap/Execution/roadmap-state-execution.md`
   - **description:** Convert broad safety ambiguity into bounded attestation-only uncertainty.
   - **exact minimal action:** Keep or add one sentence stating safety unknown is now bounded to roll-up attestation chronology/compare closure only (not missing execution node 1.2.2 or 1.2.3).
   - **constraints:** Must not claim closure success; keep gate open.

6. **[low] Provenance non-claiming annotation**
   - **action_type:** `write_log_entry`
   - **target_path:** `1-Projects/sandbox-genesis-mythos-master/Roadmap/Execution/workflow_state-execution.md`
   - **description:** Where correlation IDs are `not_recorded_from_host_task_handoff_comms`, make the row explicitly non-claiming about missing telemetry.
   - **exact minimal action:** Add a short qualifier in the latest affected row: "correlation id unavailable from host handoff; does not affect structural authority."
   - **constraints:** Do not backfill synthetic IDs in this run.

## Notes for future tuning

- Repeated `state_hygiene_failure` in this project is mostly authority-surface wording drift, not missing execution artifacts.
- Keep one canonical tuple and one canonical "next action" phrase per run family to reduce contradictions.
