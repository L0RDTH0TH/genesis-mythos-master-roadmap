---
title: Phase 2.2.2 — Handoff readiness (fail-closed denial schema mapping)
created: 2026-03-20
tags: [research, agent-research, genesis-mythos-master, handoff-readiness, schema]
project-id: genesis-mythos-master
linked_phase: Phase-2-2-2
research_query: deterministic command/event schema mapping for fail-closed denials (stable reason_code + stable identifiers)
agent-generated: true
---

## Summary
This note freezes how fail-closed denials are represented in a deterministic command/event schema, so downstream stages can reliably stop consumption for a specific `intent_id` without hidden fallback behavior.

## Contract anchors (what must be stable)
The Phase 2.2.1 contract defines:

- Denial reason-code taxonomy (fixed strings)
- Deterministic denial event fields
- Stable identifiers derived from canonical bytes and raw boundary bytes

Key source references:
- [[1-Projects/genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building/phase-2-2-intent-parser-integration-generation-hooks-roadmap-2026-03-20-0624.md]]
- [[1-Projects/genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building/phase-2-2-1-intent-canonicalization-and-denial-taxonomy-roadmap-2026-03-20-0901.md]]
- [[Ingest/Agent-Research/phase-2-2-intent-parser-procedural-hooks-determinism-integration-research-2026-03-20-0233.md]]

## Deterministic denial reason codes (v0)
Exactly these stable strings must be used:

1. `INTENT_SCHEMA_MISMATCH`
2. `INTENT_CANONICALIZATION_ERROR`

No additional strings, no renamed variants, and no “stringly-typed” composition that depends on runtime error text.

## Denial mapping: stable identifiers and stable fields

### Case F1: `INTENT_SCHEMA_MISMATCH`
Trigger: validated intent schema field list mismatch against the frozen IntentPlan field list.

Denial event fields:
- `reason_code`: `INTENT_SCHEMA_MISMATCH`
- `intent_id`: `SHA256(domain_tag_v0 || len64(canonical_intent_bytes) || canonical_intent_bytes)`
  - note: canonicalization already succeeded
- `canonicalization_version`: `CanonicalizeIntentBytes_v1`
- `intent_schema_version`: `IntentPlan_v0`

### Case F2: `INTENT_CANONICALIZATION_ERROR`
Trigger: canonicalization fails due to disallowed characters or un-decodable bytes after applying `CanonicalizeIntentBytes_v1`.

Denial event fields:
- `reason_code`: `INTENT_CANONICALIZATION_ERROR`
- `error_fingerprint`: `SHA256(raw_input_bytes)`
  - precondition: raw bytes are the exact bytes at the player/DM input boundary
- `canonicalization_version`: `CanonicalizeIntentBytes_v1`

## Command/Event Schema v0 binding (fail-closed semantics)
The orchestration must bind intent lifecycle to the Command/Event Schema v0 so that failures are replay-assertable.

### Command
- `submit_intent_command`
  - `intent_id`
  - `actor_id`
  - `phase_context`
  - `intent_text`
  - `source_refs[]`

### Event
- `intent_validated_event`
  - `intent_id`
  - `validation_status`
  - `reasons[]`

Fail-closed rule:
- When `validation_status: fail`, downstream command execution must halt for that `intent_id`.
- There must be no silent default policy usage for denied intents.

### Stage execution failure event fields (for orchestration traces)
When a generation stage fails, the orchestration trace must use the same schema fields:
- `run_id`
- `stage_name`
- `error_code`
- `error_summary`
- `fallback_action`

## Typical failure modes (schema correctness)
1. Reason_code drift
   - any mismatch between actual strings and the fixed taxonomy breaks deterministic gating
2. Non-stable identifiers
   - `intent_id` computed from canonical bytes that were not produced by the frozen canonicalization rules
3. “Fail-open” behavior
   - downstream continues stage consumption despite denial, producing manifest_hash/spawn ordering changes
4. Inconsistent stage boundaries
   - denial publish occurs at a different boundary than the happy-path publish boundary

## Output expectations for handoff_readiness
This note supports handoff readiness by ensuring:

- Deterministic, fixed reason_code taxonomy
- Deterministic, replay-assertable identifiers (intent_id, error_fingerprint)
- Fail-closed stopping semantics per `intent_id`
- Stable command/event schema binding for denial paths

## Sources
- [[1-Projects/genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building/phase-2-2-1-intent-canonicalization-and-denial-taxonomy-roadmap-2026-03-20-0901.md]]
- [[Ingest/Agent-Research/phase-2-2-intent-parser-procedural-hooks-determinism-integration-research-2026-03-20-0233.md]]

