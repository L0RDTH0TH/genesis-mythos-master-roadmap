---
created: 2026-03-20
pipeline: research
mode: RESUME_ROADMAP
project_id: genesis-mythos-master
queue_entry_id: resume-roadmap-genesis-mythos-master-phase2-deepen-20260320-0000-followup
parent_run_id: 7b8c2f1e-1d7d-4a3d-a2bb-9b7ac1e9c0c6
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 0
  medium: 6
  high: 0
initial_validator_verdict:
  severity: medium
  recommended_action: needs_work
reason_codes:
  - safety_unknown_gap
  - missing_command_event_schemas
  - missing_task_decomposition
validator_report_path: 3-Resources/Second-Brain/Validator-Reports/research_synthesis/genesis-mythos-master-20260320T064147Z.md
---

## Context
Validator→IRA (apply-repair proposal) for `pipeline: research` under `mode: RESUME_ROADMAP`. The validator marked the Phase-2.2 intent-parser procedural-hooks determinism synthesis as `severity: medium` / `recommended_action: needs_work` because it lacks concrete determinism canonicalization, exact schema binding to the stage hook contracts and command/event schema v0, and executable replay harness decomposition.

## Structural discrepancies detected
1. **Determinism safety is asserted, not engineered**: the synthesis refers to canonical bytes/hashes and replay stability, but does not define canonicalization rules (normalization, deterministic AST serialization) or hash inputs/encoding.
2. **Binding surface is underspecified**: the note uses “fields like …” for `IntentPlan`/`AnnotatedIntent`, and does not provide a fixed field list + a deterministic mapping into Phase-2.1 stage publish metadata/ledger chain (`policy_bundle_hash` → `manifest_hash` → spawn ledger `spawn_event_id` sequence).
3. **Missing command/event schema binding**: the note does not bind intent publication to the canonical command/event flow in `Roadmap/command-event-schema-v0.md` (notably `submit_intent_command` and `intent_validated_event`), nor does it specify fail-closed semantics and error-code mapping.
4. **Replay harness needs executable task decomposition**: the note lists test categories but does not break them into concrete engineering tasks with explicit persistables, assertions (double-apply/idempotency, ordering tuple checks), and deterministic failure-mode diffs.
5. **Evidence upgrade is incomplete**: lacks a “how it’s verified” checklist tied to the existing contracts (Phase-2.1.1/2.1.2) and schema docs, leaving engineers without a CI-ready verification trail.

## Proposed fixes (repair plan)
1. Add a **Canonicalization + Hashing Spec** section to the synthesis note: define `canonical_intent_bytes` deterministic construction and `intent_hash` computation + output format, including a short pseudocode/state machine.
2. Freeze an **Exact `IntentPlan` / `AnnotatedIntent` Field List** (no “fields like …”) and include versioning semantics (`intent_schema_version`) + deterministic namespace derivation for intent RNG stream isolation.
3. Add an **Exact Stage Hook Binding + Ledger Chain Mapping**: map `IntentPlan` into Phase-2.1 stage IO/publish metadata using concrete names (`PolicyBind` publish `policy_bundle_hash`, `ManifestEmit` publish `manifest_hash`, and terminal `SpawnCommit` consumption + `spawn_event_id` ordering).
4. Bind intent publication to **Command/Event Schema v0**: explicitly reference `submit_intent_command` and `intent_validated_event`, include payload field names, idempotency/ordering implications, and fail-closed halting semantics for invalid intent.
5. Decompose replay validation into **Executable Harness Tasks**: specify what to persist (seed, stage_graph_version, `canonical_intent_bytes` or hash, command/event trace fields), what assertions to run (double-apply, ordering invariants, stream-isolation skip safety), and the deterministic failure modes/reason codes.
6. Add an **Evidence Upgrade Checklist + Traceability Matrix**: link each safety-critical claim to the relevant contract docs and to the exact verification steps the harness must implement.

## Notes for future tuning
This IRA run intentionally treats the hostile validator findings as a weak minimum. The fastest handoff path is to replace prose with fixed field lists + deterministic pseudocode + CI-ready golden vector/assertion checklists anchored to `command-event-schema-v0.md` and Phase-2.1.1/2.1.2 contracts.

