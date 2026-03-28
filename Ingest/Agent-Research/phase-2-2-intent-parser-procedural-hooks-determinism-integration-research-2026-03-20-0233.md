---
title: Research — Phase 2.2 Intent Parser Hooks Integration (genesis-mythos-master)
created: 2026-03-20
tags: [research, agent-research, genesis-mythos-master]
linked_phase: Phase-2-2
project-id: genesis-mythos-master
research_query: intent parser integration into procedural generation hooks; deterministic intent->generation mapping; replay/golden determinism tests
research_tools_used: [web_search, mcp_web_fetch]
raw_sources:
  - Ingest/Agent-Research/Raw/phase-2-2-intent-parser-procedural-hooks-determinism-integration-research-raw-2026-03-20-0233.md
agent-generated: true
origin: roadmap-deepen
research_escalations_used: 0
---

# Research — Phase 2.2 Intent Parser Hooks Integration

## Summary
Phase 2.2 should integrate the intent parser into procedural generation as a **deterministic front-end**:
`DM/Player intent text` -> deterministic `IntentPlan` (schema-validated, canonical bytes) -> **explicit generation hook contract** -> deterministic ledger artifacts (`IntentPlan`/hash -> `BoundPolicyContext` -> `EntityManifest` -> `SpawnCommit`).

This addresses three engineering needs: (1) stable replay keys (`seed + canonical_intent_bytes`), (2) fail-closed orchestration when validation fails, and (3) auditably deterministic hook insertion points that can be verified with golden replay + idempotency/double-apply tests.

## Canonicalization + Hashing Spec (closes `safety_unknown_gap`)
### Canonical input bytes (`canonical_intent_bytes`)
Canonicalization must be fully deterministic and independent of locale/runtime quirks:

1. **Encoding:** require UTF-8 input; if `intent_text` is not valid UTF-8, treat as `validation_status: fail` with reason code `INTENT_SCHEMA_MISMATCH` (fails closed).
2. **Line endings:** normalize CRLF/CR to LF.
3. **Unicode normalization:** apply Unicode NFC to the full text.
4. **Whitespace canonicalization:**
   - trim leading/trailing whitespace
   - replace any run of ASCII whitespace (`[ \t\n\r\f\v]`) with a single space
5. **Case policy:** apply parser’s keyword policy (e.g. case-sensitive vs case-insensitive) during parsing; canonicalization itself must not “guess” semantics.
6. **Output:** `canonical_intent_bytes` is the exact UTF-8 byte sequence after steps 1–5.

## Deterministic parse + IR serialization
Phase 2.2 should define the parser as a deterministic grammar:

- PEG parsing expression grammars are deterministic/unambiguous under ordered choice semantics (first match wins), which gives stable parse outputs for a given canonical input.  
  [Source: Parsing Expression Grammar (PEG) determinism](https://en.wikipedia.org/wiki/Parsing_expression_grammar)

Deterministic IR serialization rules for hashing:
1. The parser produces an AST/IR.
2. The validator produces an `IntentPlan` view.
3. `IntentPlan` is serialized to canonical JSON with:
   - lexicographically sorted object keys
   - arrays serialized in their semantic order (preserve order; never sort unless explicitly defined by a rule)
   - numbers serialized as JSON numbers (no stringified floats)

## Hash functions and outputs
All hash outputs must be explicit and unambiguous:
1. `intent_hash := SHA-256(canonical_intent_bytes)`, encoded as **lowercase hex** (no `0x` prefix).
2. `annotated_intent_hash := SHA-256(canonical_json_bytes(IntentPlan_without_transient_fields))`, encoded as lowercase hex.

## Deterministic intent stream id (`intent_stream_id`)
`intent_stream_id` must be derived only from stable identifiers so replay identity is preserved:

`intent_stream_id := hash("intent" ‖ intent_schema_version ‖ intent_hash ‖ phase_context)`

If any future “intent RNG” is required for procedurally interpreting intent, it must use a dedicated intent RNG namespace so intent sampling cannot desynchronize lattice/policy streams.

PCG-style designs explicitly rely on multiple independent streams to prevent correlated consumption across concerns.  
[Source: PCG — multiple streams](https://www.pcg-random.org/useful-features.html)

## Canonicalization state machine (pseudocode)
The hook contract should implement this deterministic state machine:

```text
State S0: Receive submit_intent_command(intent_id, actor_id, phase_context, intent_text, source_refs[])
  -> canonicalize(intent_text) -> canonical_intent_bytes
  -> parse(canonical_intent_bytes) -> AST (or parse failure)
  -> validate(AST, intent_schema_version) -> IntentPlan(view)
  -> compute intent_hash and annotated_intent_hash
  -> if validation_status == pass: publish IntentPlan immutably
  -> emit intent_validated_event(intent_id, validation_status, reasons[])
State S1: Fail-closed
  -> do not publish IntentPlan
  -> emit intent_validated_event(validation_status: fail, reasons[])
  -> downstream stage execution is halted for this intent_id
```

## Exact IntentPlan / AnnotatedIntent schema (closes `missing_command_event_schemas`)
This section freezes a precise contract. There are no “fields like …” placeholders.

### `IntentPlan` (schema-validated view; versioned)
`IntentPlan` version is explicit:
- `intent_schema_version` (string, required): e.g. `"v0"`
- `intent_id` (string, required): must match the command payload `intent_id`
- `actor_id` (string, required): must match `submit_intent_command.actor_id`
- `phase_context` (string, required): must match `submit_intent_command.phase_context`

Stable identity artifacts:
- `canonical_intent_bytes` (string, required): lowercase hex of `canonical_intent_bytes` (for debugging + replay keying)
- `intent_hash` (string, required): lowercase hex SHA-256(canonical_intent_bytes)
- `intent_stream_id` (string, required): derived per the spec above

Validation outcome artifacts:
- `validation_status` (string, required): one of `"pass"` or `"fail"`
- `reasons` (array of string, required): empty array when `pass`, non-empty when `fail`

Intent-conditioned procedural modifiers (deterministic, ordered):
- `hook_modifiers` (object, required):
  - `attach_option` (string, required): one of `"A" | "B" | "C"` (matches the v0 DAG attachment decision space)
  - `priority` (integer, required): deterministic ordering for applying multiple intent constraints (higher wins)
  - `constraint_tags` (array of string, required): normalized tags derived from the intent grammar; array order is deterministic

Hash audit artifact:
- `annotated_intent_hash` (string, required): lowercase hex SHA-256(canonical_json_bytes(IntentPlan_without_transient_fields))

### `IntentAnnotate` view (if implemented as a separate stage)
If Phase 2.2 separates parsing and annotation, then `IntentAnnotate` publishes an immutable `AnnotatedIntent` view that must contain:
- `intent_id`
- `intent_schema_version`
- `annotated_intent_hash`
- `intent_stream_id`

and may additionally carry `hook_modifiers` in the same deterministic normalized form as `IntentPlan`.

### JSON Schema contract tie-in
JSON Schema supports explicit, versioned contracts for evolving structured data while keeping validation behavior defined.  
[Source: JSON Schema Draft 2020-12 specification](https://json-schema.org/draft/2020-12)

## Stage Hook Contract Mapping (closes `missing_task_decomposition` gaps by binding replay assertions)
Phase 2.1.1 defines the stage spine and publish-once artifacts:
`SeedParse -> LatticeSynthesis -> PolicyBind -> ManifestEmit -> SpawnCommit`.

Phase 2.2 integrates intent by specifying how `IntentPlan` participates in those immutable publish records.

### Hook placement for Phase 2.2 (deterministic, fail-closed)
For determinism and isolation, Phase 2.2 should choose one hook insertion path:

Recommended deterministic pattern:
1. `PolicyBind` publishes `BoundPolicyContext` from:
   - `DensityLattice`
   - `SpawnPolicySet`
   - **`IntentPlan.hook_modifiers`** (the only allowed intent influence input to PolicyBind)
2. `ManifestEmit` publishes `EntityManifest` from:
   - `BoundPolicyContext`
   - traversal order token
3. `SpawnCommit` consumes only terminal `EntityManifest` publish records.

### Required publish metadata (ties to Phase 2.1.1 publish-once contracts)
For replay harnessing, each stage publish record must include the following fields:
- `PolicyBind` publish: `stage_version_id` and `policy_bundle_hash` (and it must be derived using `intent_hash`, per the hash chain below).
- `ManifestEmit` publish: `stage_version_id` and `manifest_hash` computed from `lattice_hash`, `policy_bundle_hash`, and canonical serialized `EntityManifest` rows.
- `SpawnCommit` publish/ledger emissions: deterministic `spawn_event_id` sequence (stable under replay) and an explicit reference that ties the emitted events back to the terminal `EntityManifest` (so the harness can assert no “shadow manifest” usage).

### Exact ledger/hash chain mapping
Define the hash chain inputs explicitly so replay can compare like-for-like:
1. `policy_bundle_hash := H(policy_bytes ‖ canonical_constraint_tags_bytes ‖ intent_hash)`
   - where `canonical_constraint_tags_bytes` is a deterministic encoding of `IntentPlan.hook_modifiers.constraint_tags` (array order preserved exactly as produced)
2. `manifest_hash := H(lattice_hash ‖ policy_bundle_hash ‖ canonical_serialized_rows*)`
   - where canonical serialized rows are the post-intent-conditioned row bytes from `EntityManifest` after stable sort.

### Failure surfaces (deterministic, reason-code driven)
Intent-related deterministic fail-closed events must use Phase 2.1.2 reason codes:
- `INTENT_SCHEMA_MISMATCH`: schema version mismatch or invalid payload shape
- `INTENT_HASH_CHAIN_BREAK`: any mismatch between expected intent hash inputs and recomputed canonical bytes/hash
- `INTENT_STREAM_COLLISION`: intent-derived `intent_stream_id` collision (should be treated as fatal)

When validation fails:
- do not publish downstream artifacts (`BoundPolicyContext`, `EntityManifest`, or `SpawnCommit`)
- emit deterministic failure into orchestration trace (see command/event binding below)

## Command/Event Schema v0 Binding (closes `missing_command_event_schemas`)
The intent lifecycle must be wired exactly to the Command/Event Schema v0.

### Command: `submit_intent_command`
Payload fields (exact):
- `intent_id`
- `actor_id`
- `phase_context`
- `intent_text`
- `source_refs[]`
The command payload constraints are:
- `intent_id` unique
- `intent_text` non-empty
- `actor_id` required

### Event: `intent_validated_event`
Event payload fields (exact):
- `intent_id`
- `validation_status`
- `reasons[]`
Failure semantics:
- On `validation_status: fail`, downstream command execution must halt for the intent_id (fail-closed).

### Failure event for stage execution (`generation_stage_failed_event`)
When a generation stage fails, the orchestration trace must use the Command/Event Schema v0 payload fields (exact) to support deterministic failure-mode assertions:
- `run_id`
- `stage_name`
- `error_code`
- `error_summary`
- `fallback_action`

### Deterministic replay identity
For golden replay, the orchestration identity tuple must be:
`(seed_snapshot_id, stage_graph_version, intent_id, canonical_intent_bytes_hash/intent_hash, phase_context)`.

## Replay harness: engineering-grade tasks (closes `missing_task_decomposition`)
Implement the Phase 2.2 replay harness as executable tasks with explicit persistables and assertions.

Deterministic replay is typically built by recording stable inputs (seed + player inputs/intent) and relying on deterministic simulation code, rather than snapshotting full state every frame.  
[Source: Developing your own replay system (seed+inputs replay concept)](https://www.gamedeveloper.com/programming/developing-your-own-replay-system)

Even when determinism is expected, hardware/runtime differences (e.g. floating-point precision and scheduling/order) can diverge execution unless you keep nondeterministic borders isolated and set seeds during setup.  
[Source: Isaac Lab — Reproducibility and Determinism](https://isaac-sim.github.io/IsaacLab/main/source/features/reproducibility.html)

### Task T1 — Parser determinism (IR-layer)
Persistables:
- canonicalized intent input bytes (hex) per test case
- resulting `IntentPlan` fields (or serialized canonical JSON bytes)
Assertions:
1. `canonical_intent_bytes` is identical for whitespace/case/punctuation variations that the grammar defines as equivalent
2. `intent_hash` is identical across repeated parse runs in the same binary
3. `IntentPlan.validation_status` and `reasons[]` are stable across runs

### Task T2 — IntentPlan schema validation determinism
Persistables:
- `intent_schema_version`
- `validation_status`
- `reasons[]`
Assertions:
1. schema changes version deterministically: wrong version always fails with `INTENT_SCHEMA_MISMATCH`
2. no “partial success”: when validation fails, downstream publish does not occur

Property-based testing can be used to fuzz intent inputs while keeping failures replayable via a deterministic examples database.  
[Source: Hypothesis — Replaying failed tests](https://hypothesis.readthedocs.io/en/latest/tutorial/replaying-failures.html)

### Task T3 — Golden replay on generation hooks
Persistables:
- `stage_graph_version`
- `seed_snapshot_id`
- `intent_id`
- `intent_hash` / `annotated_intent_hash`
- terminal `EntityManifest.manifest_hash`
- `SpawnCommit` deterministic event sequence (`spawn_event_id` ordering)
Assertions:
1. repeated generation runs yield identical `manifest_hash` and identical spawn_event_id sequence
2. swapping unrelated runtime parameters (that are supposed to be out of deterministic border) does not affect deterministic outputs

### Task T4 — Double-apply / idempotency (ledger-hit)
Persistables:
- command/event trace for stage execution (`generation_stage_completed_event` and/or failure events)
Assertions:
1. second apply produces no additional ledger mutations (idempotency via stable event ids and ledger references)
2. if intent differs only by rejected changes (validation_status fail), no generation-stage commands should run

### Task T5 — Stream isolation + optional stage skip safety
Persistables:
- enable/disable intent feature flag or attach option
- produced `manifest_hash` and spawn_event_id sequence
Assertions:
1. when intent is disabled, deterministic outputs match the baseline (intent hook must be isolated)
2. when optional stages are skipped, mandatory stage publish artifacts remain unchanged

### Expected failure diffs (what to assert when hashes diverge)
- If `manifest_hash` diverges while `(seed_snapshot_id, stage_graph_version, intent_id)` match:
  - treat as `INTENT_HASH_CHAIN_BREAK` candidate (canonicalization/serialization drift or policy_bundle_hash wiring error)
- If `intent_stream_id` is equal for two distinct intents that should be distinct:
  - treat as `INTENT_STREAM_COLLISION` candidate

## Evidence upgrade + traceability matrix
This note’s safety claims must be “proven by CI”, not by narrative.

Traceability matrix:
| Safety claim (what we must guarantee) | Proof artifact (what to compare) | Harness task(s) |
|---|---|---|
| Intent text -> stable canonical bytes | `canonical_intent_bytes` equality | T1 |
| Stable deterministic parsing | `IntentPlan` canonical JSON bytes equality | T1 |
| Schema validation is fail-closed | `validation_status: fail` and `reasons[]` stability | T2 |
| Replay stability of generation hook outputs | `EntityManifest.manifest_hash` + spawn event ordering equality | T3 |
| Idempotency/no duplicate side effects | command trace shows no additional ledger mutations | T4 |
| Intent RNG isolation from lattice/policy RNG | identical outputs when intent optional pieces are skipped/flagged | T5 |

## Decisions / constraints (candidate for Phase 2.2)
- Choose hook input mapping precisely: only `IntentPlan.hook_modifiers` is allowed to flow into `PolicyBind` for v0 intent integration.
- Require explicit hash chain wiring: `policy_bundle_hash` must include `intent_hash`, and `manifest_hash` must include `policy_bundle_hash` to make intent influence auditable.
- Keep deterministic replay “in-bounds”: parser and schema validation run before any stage touches RNG streams.
- If intent procedural interpretation is later introduced, it must use a dedicated intent RNG namespace derived from `(intent_hash, intent_schema_version, phase_context)` (never lattice/policy RNG).

## Raw sources (vault)
External sources used in this synthesis were captured into:
- [[Ingest/Agent-Research/Raw/phase-2-2-intent-parser-procedural-hooks-determinism-integration-research-raw-2026-03-20-0233.md]]

## Sources
- [Source: Isaac Lab — Reproducibility and Determinism](https://isaac-sim.github.io/IsaacLab/main/source/features/reproducibility.html)
- [Source: Developing your own replay system — GameDeveloper](https://www.gamedeveloper.com/programming/developing-your-own-replay-system)
- [Source: JSON Schema Draft 2020-12 specification](https://json-schema.org/draft/2020-12)
- [Source: Hypothesis — Replaying failed tests](https://hypothesis.readthedocs.io/en/latest/tutorial/replaying-failures.html)
- [Source: Parsing Expression Grammar (PEG) determinism](https://en.wikipedia.org/wiki/Parsing_expression_grammar)
- [Source: PCG — multiple streams](https://www.pcg-random.org/useful-features.html)

