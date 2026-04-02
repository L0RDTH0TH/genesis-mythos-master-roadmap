---
title: Phase 2.2.2 — IntentPlan consumption boundary + deterministic verification harness
roadmap-level: tertiary
phase-number: 2
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-20
tags: [roadmap, genesis-mythos-master, phase, intent-parser, determinism, handoff-readiness]
para-type: Project
subphase-index: "2.2.2"
handoff_readiness: 94
links:
  - "[[phase-2-2-intent-parser-integration-generation-hooks-roadmap-2026-03-20-0624]]"
  - "[[phase-2-2-1-intent-canonicalization-and-denial-taxonomy-roadmap-2026-03-20-0901]]"
  - "[[decisions-log]]"
---

## Phase 2.2.2 — IntentPlan consumption boundary + deterministic verification harness

This tertiary note makes the Phase 2.2 handoff *verifiable*: it defines the deterministic replay harness assertions (happy path + fail-closed denials) and the idempotent ledger invariants that guarantee double-apply cannot create duplicate side effects.

### Pinned consumption boundary (happy path + denial path)

Chosen boundary: **IntentPlan is consumed at the manifest-emission boundary**, after deterministic policy derivation and immediately before `ManifestEmit` draft emission.

- Happy path: `IntentPlan` is validated, then its `intent_hash` deterministically wires into `policy_hash`, `lattice_hash`, `manifest_hash`, and `spawn_event_id` ordering.
- Denial path: invalid intent emits exactly one deterministic denial event for the denied `intent_id`, and downstream stage hooks must stop consuming the intent for that `intent_id` with no silent fallbacks.

### Deterministic replay harness (v1) — executable-grade assertions

```pseudo
constants:
  canonicalization_version := "CanonicalizeIntentBytes_v1"
  intent_schema_version_as_ascii := "IntentPlan_v0"
  domain_tag_v0 := "GENESIS_MYTHOS_INTENT_HASH_DOMAIN_V0"
  deterministic_gate_version_id := "DETERMINISTIC_GATE_V1"

types:
  ReplayInputs := {
    raw_intent_text_bytes,            // exact bytes at input boundary
    intent_schema_version_as_ascii,
    canonicalization_version,
    stable_run_context,              // stage-graph semver + boundary-id + replay slice (no wall-clock)
    ordered_identity_sequence         // stable ordering tuple
  }

functions:
  canonicalize(raw_intent_bytes) -> (canonical_intent_bytes, intent_id) or denial
  compute_intent_hash(canonical_intent_bytes, validated_intent_view) -> intent_hash
  wire_hash_chain(intent_hash) -> (policy_hash, lattice_hash, manifest_hash, spawn_event_id_ordering)
  emit_manifest_at_boundary(manifest_hash, spawn_event_id_ordering) -> (manifest_hash_emitted, spawn_order_emitted)
  emit_denial_event_at_boundary(reason_code, intent_id, error_fingerprint) -> denial_event_payload

procedure ReplayAndVerify(replay_inputs: ReplayInputs, golden_vectors):
  // Step 1: canonicalization -> canonical bytes + deterministic identity
  result := canonicalize(replay_inputs.raw_intent_text_bytes)
  if result is denial:
    // Step 2a: fail-closed denial assertions
    assert result.reason_code in { INTENT_SCHEMA_MISMATCH, INTENT_CANONICALIZATION_ERROR }
    assert denial_event_payload.reason_code == result.reason_code
    assert denial_event_payload.intent_id == result.intent_id
    assert exactly_one_denial_event_emitted_for(intent_id=result.intent_id)
    assert downstream_stage_hooks_stop_consuming(intent_id=result.intent_id)
    assert no manifest emission occurs for denied intent_id
    return

  // Step 2b: validation + hashing on happy path
  validated_intent_view := ValidateFrozenIntentPlanSchema(result.canonical_intent_bytes)
  intent_hash := compute_intent_hash(result.canonical_intent_bytes, validated_intent_view)
  (policy_hash, lattice_hash, manifest_hash, spawn_event_id_ordering) := wire_hash_chain(intent_hash)

  // Step 3: stage-hook consumption at pinned boundary
  (manifest_hash_emitted, spawn_order_emitted) := emit_manifest_at_boundary(
    manifest_hash=manifest_hash,
    spawn_event_id_ordering=spawn_event_id_ordering
  )

  // Step 4: golden-vector assertions (happy-path)
  assert manifest_hash_emitted == golden_vectors.manifest_hash_hex
  assert spawn_order_emitted == golden_vectors.spawn_event_id_ordering

  // Step 5: double-apply / idempotency assertions (ledger)
  ledger_key := (stable_run_context.stage_graph_version, stable_run_context.boundary_id, replay_inputs.intent_id, deterministic_gate_version_id)
  ledger_result_1 := TryApplyToLedger(ledger_key, payload_hash=Hash(manifest_hash || spawn_order_emitted))
  ledger_result_2 := TryApplyToLedger(ledger_key, payload_hash=Hash(manifest_hash || spawn_order_emitted))
  assert ledger_result_1 == "applied"
  assert ledger_result_2 == "ledger-hit"
  assert no additional state mutations on second apply
```

### Golden vectors (G1/G2/G3) — fixture table

| Vector | raw intent text | canonical_intent_bytes_hex | intent_hash_hex | manifest_hash_hex | spawn_event_id_ordering |
| --- | --- | --- | --- | --- | --- |
| G1 | `Move to Sector A` | `4d6f766520746f20536563746f7220410a496e74656e74506c616e5f7630` | `5b2f6d3fd7c64a7525222fbd7583b11cd6ba71326c9b6b9c314368ba01d4e3a6` | `b5755f84fbfe43a67b8c8b0af6d378f2a529278cbe1388e26b4447f2e2f7a19a` | `[1b4c2abb8961c17ea5ad331578495cd49fc9c33e3e31ffacd11940fe58844b99]` |
| G2 | `  Move   to   Sector   A  ` | `4d6f766520746f20536563746f7220410a496e74656e74506c616e5f7630` | `5b2f6d3fd7c64a7525222fbd7583b11cd6ba71326c9b6b9c314368ba01d4e3a6` | `b5755f84fbfe43a67b8c8b0af6d378f2a529278cbe1388e26b4447f2e2f7a19a` | `[1b4c2abb8961c17ea5ad331578495cd49fc9c33e3e31ffacd11940fe58844b99]` |
| G3 | `Rest at Sector A` | `5265737420617420536563746f7220410a496e74656e74506c616e5f7630` | `933778468e12f75dacae727638f1edff8eb8a6216d2b7a89cee1312eeec30360` | `fe980e32ed7c84197b9567d2bccc7746194a667a720d8ccdc0e72ad477b73471` | `[313f06099e5c205731afa9e3d7074f4e6a27371f3638f0c5efbec6d7d7cd3a38]` |

Expected double-apply / idempotency outcomes (ledger):

- G1: `ledger_result_1=applied`, `ledger_result_2=ledger-hit`
- G2: `ledger_result_1=applied`, `ledger_result_2=ledger-hit`
- G3: `ledger_result_1=applied`, `ledger_result_2=ledger-hit`

### Fail-closed denial fixtures (F1/F2) — expected denial payloads + stop-consumption

- F1 (`INTENT_SCHEMA_MISMATCH`):
  - raw intent text: `Move to Sector` (canonicalization succeeds; schema validation fails)
  - expected `intent_id`: `4754625a0be8e38fbec7adc5297a4ad622a0f5fd8397d0d143d7546176413388`
  - expected behavior:
    - exactly one deterministic denial event emitted for that `intent_id`
    - downstream stage hooks stop consuming for that `intent_id`
    - no manifest emission occurs for the denied `intent_id`
  - expected idempotency: `ledger_result_1=applied`, `ledger_result_2=ledger-hit`

- F2 (`INTENT_CANONICALIZATION_ERROR`):
  - raw_input_bytes_hex: `fffeff` (UTF-8 decode fails -> canonicalization error)
  - expected `error_fingerprint`: `b88c193009c22360a2a1e815905a7ea5f0b091647e5eaaff56a0cd90e22598b7`
  - expected behavior:
    - exactly one deterministic denial event emitted for the canonicalization-error identity
    - downstream stage hooks stop consuming for that denial identity
    - no manifest emission occurs for the denied identity
  - expected idempotency: `ledger_result_1=applied`, `ledger_result_2=ledger-hit`

### Minimal test matrix (handoff verification)

- Happy-path drift checks: validate G1/G2/G3 fixture table matches emitted `manifest_hash` and `spawn_event_id_ordering` at the pinned consumption boundary.
- Fail-closed denial checks: validate F1/F2 each emit exactly one denial event and prevent any manifest emission for the denied identifier.

### Handoff readiness evidence inventory

The note is considered handoff-ready when all of the following evidence is linked and satisfied:

1. Pinned consumption boundary for both happy and denial paths (no fail-open).
2. Deterministic replay harness that asserts golden vectors and enforces double-apply/idempotency via ledger-hit outcomes.
3. Closed reason_code taxonomy for denials with stable identifiers (`intent_id`, and when relevant `error_fingerprint`).
4. Explicit hash-chain wiring from `intent_hash` into `manifest_hash` and `spawn_event_id` ordering.
5. A named deterministic gate version (`DETERMINISTIC_GATE_V1`) used for drift detection.

## Research integration

### Key takeaways
- Deterministic replay harness + assertions (parser determinism, schema validation determinism, golden hook replay, double-apply/idempotency, stream isolation) provide CI-grade proof for handoff safety.
- Ledger idempotency should be driven by content-addressed/stable event identity keyed to replay invariants (seed snapshot, stage graph version, intent_id, intent_hash, phase_context) so “apply twice” cannot create duplicate ledger mutations.
- Fail-closed denials must use a fixed, stable reason_code taxonomy (`INTENT_SCHEMA_MISMATCH`, `INTENT_CANONICALIZATION_ERROR`) and emit exactly one deterministic denial event per denied `intent_id`.
- Command/event schema v0 binding makes denial paths replay-assertable: downstream must stop consuming the intent for that `intent_id` with no silent fallback policy.
- Canonicalization is a frozen contract (CanonicalizeIntentBytes_v1): whitespace/punctuation/unicode normalization must converge to identical `canonical_intent_bytes`.
- Hash-chain integration must deterministically wire `intent_hash` into `policy_hash`, `lattice_hash`, `manifest_hash`, and `spawn_event_id` ordering.
- Golden vectors (G1/G2/G3) plus fail-closed vectors (F1/F2) form the minimal drift test matrix for canonicalization + hashing + denial semantics.
- `handoff_readiness` should be computed as evidence-backed checklist completeness (contract freeze + deterministic replay + vectors + fail-closed behavior + linked proof inventory), not narrative confidence.

### Decisions / constraints
- Pin the stage-hook consumption boundary consistently (happy-path and denial-path) to prevent boundary drift across pipeline stages.
- Freeze canonicalization_version, intent_schema_version_as_ascii (`IntentPlan_v0`), and domain_tag_v0; exclude transient/non-semantic fields from hashed stable subsets.
- Denial mapping is closed over the two fixed reason_codes only; no extra reason_code strings, no reason_code composition from runtime text.
- Stable identifiers must be computed exactly: `intent_id` from canonical bytes and `error_fingerprint` from raw input bytes.
- Hash concatenation must be unambiguous (length-prefixed fields via `len64`) and stable_json must be strictly defined (sorted keys, no insignificant whitespace).
- The test matrix must include golden vectors G1/G2/G3 and fail-closed assertions F1/F2, plus double-apply/idempotency checks.

### Stable-subset hashing filter (allowlist/denylist, v1)

Transient-field denylist (excluded from deterministic hashing / stable subsets):

- `intent_processing_time_utc`
- `generation_run_id` / `ui_request_id`
- free-form diagnostic strings
- non-deterministic model outputs / sampling metadata

Stable-subset allowlist (hashed semantic fields used for `stable_field_digest`):

- `intent_kind`
- `canonical_target`
- `intent_constraints` (sorted lexicographically)
- `intent_schema_version` fixed to `IntentPlan_v0`

Stable serialization + digest:

- `stable_json` = UTF-8 JSON with keys sorted lexicographically and no insignificant whitespace.
- `stable_field_digest := SHA-256(stable_json_bytes)`
- `len64(x) = 8-byte big-endian byte-length` (the harness’s identifier preimage must use this exact length encoding).

Because `intent_hash` preimage uses only `domain_tag_v0` + length-prefixed canonical bytes + `stable_field_digest(validated_intent_view)`, transient field drift cannot change the deterministic hashes.

### Synthesized research notes (paste targets)
- [[Ingest/Agent-Research/phase-2-2-2-handoff-readiness-deterministic-replay-ledger-idempotency-2026-03-20-0613.md]]
- [[Ingest/Agent-Research/phase-2-2-2-handoff-readiness-fail-closed-denial-schema-mapping-2026-03-20-0613.md]]
- [[Ingest/Agent-Research/phase-2-2-2-handoff-readiness-hash-chain-vectors-and-validation-checklist-2026-03-20-0613.md]]

### Sources
- [[1-Projects/genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building/phase-2-2-intent-parser-integration-generation-hooks-roadmap-2026-03-20-0624.md]]
- [[1-Projects/genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building/phase-2-2-1-intent-canonicalization-and-denial-taxonomy-roadmap-2026-03-20-0901.md]]
- [[Ingest/Agent-Research/phase-2-2-intent-parser-procedural-hooks-determinism-integration-research-2026-03-20-0233.md]]
- https://json-schema.org/draft/2020-12
- https://docs.eventsourcingdb.io/best-practices/optimizing-event-replays/

