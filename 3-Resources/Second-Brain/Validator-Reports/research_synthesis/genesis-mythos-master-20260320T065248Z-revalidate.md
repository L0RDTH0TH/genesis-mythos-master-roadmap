---
title: Validator — research_synthesis (genesis-mythos-master / Phase-2-2 hardened pass)
created: 2026-03-20
tags: [validator, research_synthesis, genesis-mythos-master, phase-2-2]
validation_type: research_synthesis
project_id: genesis-mythos-master
linked_phase: Phase-2-2
queue_entry_id: resume-roadmap-genesis-mythos-master-phase2-deepen-20260320-0000-followup
parent_run_id: 7b8c2f1e-1d7d-4a3d-a2bb-9b7ac1e9c0c6
timestamp: 2026-03-20T06:52:48Z
synth_notes_validated:
  - Ingest/Agent-Research/phase-2-2-intent-parser-procedural-hooks-determinism-integration-research-2026-03-20-0233.md
compare_to_report_path: 3-Resources/Second-Brain/Validator-Reports/research_synthesis/genesis-mythos-master-20260320T064147Z.md
severity: medium
recommended_action: needs_work
ready_for_handoff: "conditional"
reason_codes:
  - safety_unknown_gap
potential_sycophancy_check: true
---

# research_synthesis — hostile hardened verdict

## One-paragraph summary
The synthesis now closes the earlier implementation-blocking holes around deterministic canonicalization, schema binding, and replay harness task decomposition (the note explicitly defines canonical bytes, versioned `IntentPlan`, command/event payload fields, and CI-grade replay tasks T1–T5). It still fails hostile determinism binding hardening because multiple hashing/encoding inputs remain underspecified for replay equality (generic `hash`/`H` usage, undefined `IntentPlan_without_transient_fields`, and unspecified canonical encodings for `policy_bytes` / constraint tag bytes / manifest row serialization). Net: closeable for implementation, but not yet safe to handoff without these remaining determinism binding gaps being made executable.

## Machine-readable verdict (return payload)

```yaml
severity: medium
recommended_action: needs_work
ready_for_handoff: conditional
reason_codes:
  - safety_unknown_gap
potential_sycophancy_check: true
gap_citations:
  safety_unknown_gap: >
    (a) `intent_stream_id := hash("intent" ‖ intent_schema_version ‖ intent_hash ‖ phase_context)` (hash function/encoding not explicitly fixed),
    (b) `annotated_intent_hash := SHA-256(canonical_json_bytes(IntentPlan_without_transient_fields))` (what counts as “transient” fields is undefined),
    (c) `policy_bundle_hash := H(policy_bytes ‖ canonical_constraint_tags_bytes ‖ intent_hash)` / `manifest_hash := H(lattice_hash ‖ policy_bundle_hash ‖ canonical_serialized_rows*)` (H + canonical encodings for inputs not fully specified).
```

## Strengths
- Canonicalization + canonical byte rules are spelled out: UTF-8 requirement, CRLF/LF normalization, Unicode NFC, whitespace canonicalization, and explicit `SHA-256(canonical_intent_bytes)` + lowercase-hex outputs.
- Binding surface is no longer hand-wavy: the note freezes `IntentPlan` with required fields (`intent_schema_version`, `intent_id`, `intent_hash`, `intent_stream_id`, `validation_status`, `reasons`, `hook_modifiers`, etc.) and provides an explicit Command/Event schema v0 payload mapping.
- Replay harness is decomposed into executable tasks: T1–T5 include persistables and concrete assertions for determinism, schema fail-closed behavior, golden replay stability, ledger idempotency, and isolation/optional stage skipping.

## Concerns (what remains blocking implementation safety)
1. **Deterministic hashing inputs are not fully pinned to a single executable encoding**: the spec uses generic `hash(...)` and `H(...)` without stating the algorithm (and/or byte-encoding semantics) for multiple derived identifiers/hashes.
2. **“Transient fields” is undefined**: the `annotated_intent_hash` depends on `IntentPlan_without_transient_fields`, but the note never defines which exact fields are considered transient vs persisted for hashing stability.
3. **Canonical serialization for key hash-chain inputs is incomplete**: `policy_bytes`, `canonical_constraint_tags_bytes`, `lattice_hash`, and `canonical_serialized_rows*` are referenced as if their encodings are known, but the note does not fully specify how to canonicalize those byte sequences across runtimes (beyond some earlier intent/canonical-json guidance).

## `reason_codes` x mandatory verbatim gap citations

| reason_code | Verbatim snippet (from validated synth note) |
|---|---|
| `safety_unknown_gap` | `intent_stream_id := hash("intent" ‖ intent_schema_version ‖ intent_hash ‖ phase_context)` / `annotated_intent_hash := SHA-256(canonical_json_bytes(IntentPlan_without_transient_fields))` / `policy_bundle_hash := H(policy_bytes ‖ canonical_constraint_tags_bytes ‖ intent_hash)` (hash function + transient-field definition + canonical encodings not fully specified). |

## `next_artifacts` (definition of done)
- [ ] **Fix hashing ambiguity (intent stream id + hash-chain):** Specify the exact hash function(s) for `hash(...)` and `H(...)` (e.g., SHA-256) and define the byte-encoding rules for concatenation/order separators so replay byte equality can be asserted.
- [ ] **Define `IntentPlan_without_transient_fields`:** Add an explicit list (or predicate) of which `IntentPlan` fields are excluded from `annotated_intent_hash`, and ensure the canonical JSON serialization rules apply to the filtered object.
- [ ] **Pin canonical encodings for hash-chain inputs:** Provide executable canonicalization rules for `policy_bytes`, `canonical_constraint_tags_bytes`, `lattice_hash`, and `canonical_serialized_rows*` (including how rows are serialized and how stable ordering is enforced).
- [ ] **Add one CI-level “hash equality” check:** Extend T3/T4 (or add a tiny sub-assert) that fails hard if computed `policy_bundle_hash`, `manifest_hash`, or `intent_stream_id` diverge across two replay runs built from the same `(seed_snapshot_id, stage_graph_version, intent_id, phase_context)`.

## Final-pass regression guard (vs `compare_to_report_path`)
Initial report reason_codes were:
- `safety_unknown_gap`
- `missing_command_event_schemas`
- `missing_task_decomposition`

This hardened pass keeps **`safety_unknown_gap`** and drops the other two because the synthesis now contains explicit closure text and the corresponding engineering artifacts:
- Resolved `missing_command_event_schemas`: the note states “There are no “fields like …” placeholders” and provides exact Command/Event payload fields for `submit_intent_command`, `intent_validated_event`, and `generation_stage_failed_event`.
- Resolved `missing_task_decomposition`: the note explicitly provides “Replay harness: engineering-grade tasks (closes `missing_task_decomposition`)” and enumerates T1–T5 with persistables + assertions.

No softening of the hostile bar: remaining handoff risk is still determinism binding executability (hash/encoding/transient-field definition), not prose coverage.

## `potential_sycophancy_check`
true. The note is very thorough and it is tempting to declare it “handoff-ready” immediately; I am not doing that because the remaining hashing/encoding/transient-field definitions are exactly where replay equality breaks in real engineering systems.

---
**Return token:** Success (validator completed; `severity: medium` / `recommended_action: needs_work` indicates remaining determinism binding gaps prevent safe implementation handoff).
