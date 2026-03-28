---
title: Phase 2.2.2 — Handoff readiness (deterministic replay + ledger idempotency)
created: 2026-03-20
tags: [research, agent-research, genesis-mythos-master, handoff-readiness, determinism]
project-id: genesis-mythos-master
linked_phase: Phase-2-2-2
research_query: deterministic replay harness design for content-addressed/ledger-key idempotency
agent-generated: true
---

## Summary
This note provides an executable-grade checklist for building a deterministic replay harness around the Phase 2.2 intent integration path, with emphasis on content-addressed/ledger-key idempotency (no duplicate side effects on double-apply).

## Contract anchors (what the harness must match)
The harness must validate the invariants already frozen in Phase 2.2 / 2.2.1:

- Canonical intent identity anchors (canonicalization_version, intent_schema_version_as_ascii = `IntentPlan_v0`, domain_tag_v0 = `GENESIS_MYTHOS_INTENT_HASH_DOMAIN_V0`)
- Deterministic hash chain propagation (`intent_hash` -> policy/lattice/manifest -> spawn ordering)
- Fail-closed stage execution: invalid intent yields exactly one deterministic denial event and prevents downstream publish artifacts
- Replay-safe side effects: simulation/replay builds internal state/derived artifacts without external mutations

Key source references:
- [[1-Projects/genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building/phase-2-2-intent-parser-integration-generation-hooks-roadmap-2026-03-20-0624.md]]
- [[1-Projects/genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building/phase-2-2-1-intent-canonicalization-and-denial-taxonomy-roadmap-2026-03-20-0901.md]]
- [[Ingest/Agent-Research/phase-2-2-intent-parser-procedural-hooks-determinism-integration-research-2026-03-20-0233.md]]

## Deterministic replay identity (golden replay tuple)
Use a stable identity tuple so replay comparisons do not depend on runtime state:

- `seed_snapshot_id`
- `stage_graph_version`
- `intent_id` (derived deterministically from canonical bytes)
- `intent_hash` / `annotated_intent_hash` (hashes must be stable under replay)
- `phase_context`

If any component diverges, treat it as a harness failure; if inputs match, outputs must match bit-for-bit.

## Ledger-key idempotency: what to validate
Goal: replay-safe logic is idempotent and isolated; “double apply” should not produce new ledger mutations when event identity matches.

### Validation set
1. Parser/validation determinism (IR-layer)
   - `canonical_intent_bytes` is identical for semantically equivalent input variants
   - `IntentPlan` stable serialization bytes are stable (sorted keys, no insignificant whitespace rules)
2. Intent hash determinism (hash chain seam)
   - `intent_hash` recomputes to the same bytes across replay runs
   - any stable “intent -> manifest -> spawn ordering” chain seams are deterministic
3. Fail-closed isolation (denial path)
   - on denial, no downstream publish artifacts (PolicyBind/ManifestEmit/SpawnCommit) occur for that `intent_id`
4. Double-apply / ledger-hit idempotency
   - applying the same stage execution trace twice does not generate additional ledger side effects
   - if ledger events are persisted, they must be keyed by stable identifiers so duplicates are ignored

### Typical failure modes (what to catch early)
1. Canonicalization drift
   - whitespace/line-ending/unicode normalization differences cause `intent_hash` divergence
2. Serialization drift in stable_json
   - unordered keys, array reorder bugs, or “insignificant whitespace” changes break hash continuity
3. Transient-field leakage
   - timestamps/run ids/trace ids included in “stable subset” hashing by accident
4. Stage hook boundary confusion
   - IntentPlan is mutated in-place or consumed at different boundaries between runs
5. Replay-open side effects
   - replay triggers “live” side effects (emails, external DB writes, irreversible actions)
6. Ledger-key collisions or unstable event IDs
   - event ids derived from runtime (clock order, non-deterministic indexes) instead of content-addressed fields

## Harness tasks (implementation-friendly mapping)
Adapt Phase 2.2’s required harness tasks into CI-friendly stages:

### T1 — Parser determinism (IR-layer)
- Persistables: `canonical_intent_bytes` + `IntentPlan` canonical JSON bytes (or stable fields digest)
- Assertions: byte-identical canonical bytes; stable validation_status/reasons

### T2 — IntentPlan schema validation determinism
- Persistables: `intent_schema_version`, `validation_status`, `reasons[]`
- Assertions: wrong schema version always maps to the same denial reason_code; no partial success

### T3 — Golden replay on generation hooks
- Persistables: `stage_graph_version`, `seed_snapshot_id`, `intent_id`, `intent_hash`, `manifest_hash`, `spawn_event_id ordering`
- Assertions: repeated generation runs yield identical manifest_hash + spawn ordering sequence

### T4 — Double-apply / idempotency (ledger-hit)
- Persistables: command/event trace IDs + ledger mutation reference IDs
- Assertions: applying twice yields no additional ledger mutations for stable event IDs

### T5 — Stream isolation
- Persistables: feature flags (intent attach option) + produced outputs
- Assertions: if intent hook is disabled or attachments are skipped, deterministic outputs match baseline

## Output expectations for handoff_readiness
This note supports handoff readiness by ensuring the replay harness produces:

- Stable canonical inputs (canonical_intent_bytes)
- Stable identity hashes (intent_hash) and deterministic downstream outputs (manifest_hash, spawn ordering)
- Deterministic fail-closed semantics (one denial event; no partial downstream artifact leakage)
- Idempotent “double-apply” behavior (no additional ledger mutations)

## Sources
- [[Ingest/Agent-Research/phase-2-2-intent-parser-procedural-hooks-determinism-integration-research-2026-03-20-0233.md]]
- [[Ingest/Agent-Research/Raw/phase-2-1-5-event-sourcing-replay-idempotent-side-effects-raw-2026-03-20-2346.md]]
- https://docs.eventsourcingdb.io/best-practices/optimizing-event-replays/

