---
title: Phase 1.1.5 - Idempotent State Rehydration Contract and Cold-Start Consistency
roadmap-level: tertiary
phase-number: 1
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-19
tags: [roadmap, genesis-mythos-master, phase]
para-type: Project
subphase-index: "1.1.5"
links:
  - "[[phase-1-1-core-architecture-contracts-roadmap-2026-03-19-0001]]"
  - "[[phase-1-1-4-state-snapshot-lineage-and-authoritative-rollback-ledger-roadmap-2026-03-19-1201]]"
---

## Phase 1.1.5 - Idempotent State Rehydration Contract and Cold-Start Consistency

Define the deterministic rehydration contract that restores authoritative world state from snapshot and event lineage without divergence. This phase hardens cold-start behavior so junior implementation can replay, verify, and resume from the same contract each time.

### Objectives

- [ ] Define rehydration input schema and strict preflight checks.
- [ ] Formalize idempotent restore behavior for repeated boot attempts.
- [ ] Add deterministic ordering and conflict handling for replay slices.
- [ ] Prove cold-start parity against warm-path execution checkpoints.

## Rehydration contract (v1)

```text
interface StateRehydrationContract {
  load_snapshot(snapshot_id: string, stream_id: string) -> SnapshotPayload;
  load_replay_slice(stream_id: string, from_tick: int, to_tick: int) -> EventSlice;
  preflight_verify(snapshot: SnapshotPayload, slice: EventSlice, expected_hash: string) -> PreflightResult;
  rehydrate(snapshot: SnapshotPayload, slice: EventSlice, options: RehydrateOptions) -> RehydrateResult;
  publish_resume_checkpoint(stream_id: string, checkpoint_hash: string, resumed_at_tick: int) -> ResumeCheckpoint;
}

PreflightResult:
- schema_valid
- lineage_valid
- hash_compatible
- deterministic_order_ready
- blocker_reason_code
```

## Event/application ordering rules (v1)

```yaml
rehydrate.begin.command:
  command_id: string
  stream_id: string
  snapshot_id: string
  replay_from_tick: integer
  replay_to_tick: integer
  expected_state_hash: string
  idempotency_key: string
  requested_at: string

rehydrate.verify.event:
  event_id: string
  correlation_id: string
  causation_id: string
  schema_valid: boolean
  lineage_valid: boolean
  hash_compatible: boolean
  deterministic_payload_hash: string

rehydrate.committed.event:
  event_id: string
  correlation_id: string
  causation_id: string
  resumed_at_tick: integer
  checkpoint_hash: string
  deterministic_payload_hash: string

rehydrate.blocked.event:
  event_id: string
  correlation_id: string
  causation_id: string
  blocker_reason_code: string
  deterministic_payload_hash: string
```

### Invariants

- Rehydration consumes one canonical snapshot source and one ordered replay slice.
- Replay ordering is stable and stream-scoped for every restore attempt.
- Repeated rehydration requests with same idempotency key yield same observable outcome.
- Resume checkpoint hash must match preflight-compatible expected hash family.
- Any incompatibility emits deterministic blocker reason code and no partial commit.

## Research integration

### Key takeaways

- Model rehydration as deterministic replay from a trusted snapshot baseline plus ordered event/log tail.
- Enforce idempotent application using durable operation IDs and "already applied" indexes.
- Validate snapshot compatibility (schema/config/version/watermark/checksum) before replay.
- Isolate side effects from rebuild; only emit writes after replay commit boundaries are confirmed.
- Instrument startup with drift checks (expected vs reconstructed counters/hashes) and recovery SLO metrics.

### Decisions / constraints

- **Constraint:** Startup must be safe to rerun any number of times without duplicating writes.
- **Decision candidate:** Keep per-entity monotonic sequence + dedupe index as minimum idempotency surface.
- **Constraint:** On version mismatch or checksum failure, block normal writes and trigger controlled recovery path.
- **Decision candidate:** Use periodic snapshots to cap replay time, with snapshot metadata required for trust.
- **Constraint:** Recovery path must expose observability (replay lag, skipped/duplicate events, mismatch counters).

### Sources

- Foundational reference: Event sourcing recovery and deterministic replay patterns (Fowler; CQRS/event-store literature).
- Foundational reference: Idempotent consumer and exactly-once-effect patterns in distributed systems.
- Foundational reference: Kafka-style offset/watermark checkpointing and replay safety guidance.
- Foundational reference: AWS Well-Architected reliability patterns for restart/recovery and failure isolation.
- Foundational reference: Database WAL/checkpoint principles (ARIES-style recovery concepts) adapted to application state rehydration.

## Task decomposition (v1)

- [ ] **T1 - Rehydration preflight module**
  - owner_surface: restore orchestration package
  - inputs: snapshot payload, replay slice, expected hash
  - outputs: preflight verdict with blocker reason
  - done_condition: any failed invariant blocks restore path before mutation
- [ ] **T2 - Deterministic replay applier**
  - owner_surface: replay engine
  - inputs: ordered event slice + snapshot base
  - outputs: deterministic state projection
  - done_condition: replay run yields identical hash for identical inputs
- [ ] **T3 - Restore idempotency ledger**
  - owner_surface: rehydration gateway
  - inputs: idempotency tuple and restore outcome hash
  - outputs: deduplicated restore outcomes
  - done_condition: duplicate requests return prior canonical result without side effects
- [ ] **T4 - Resume checkpoint publisher**
  - owner_surface: checkpoint service
  - inputs: stream_id, resumed tick, checkpoint hash
  - outputs: resume checkpoint event and anchor record
  - done_condition: live command stream references the published checkpoint
- [ ] **T5 - Rehydration observability map**
  - owner_surface: telemetry + audit
  - inputs: preflight/commit/block events
  - outputs: deterministic trace set for incident replay
  - done_condition: operators can reconstruct restore lifecycle from emitted events

## Executable test plan (v0)

- [ ] **R1 - Stable replay hash:** same snapshot + replay slice produces same final hash.
- [ ] **R2 - Idempotent rehydrate retry:** repeated `rehydrate.begin` with same key returns same committed outcome.
- [ ] **R3 - Ordering mismatch block:** unsorted replay slice emits `rehydrate.blocked`.
- [ ] **R4 - Hash incompatibility block:** incompatible expected hash emits deterministic blocker reason.
- [ ] **R5 - Resume checkpoint continuity:** successful rehydrate publishes checkpoint consumed by live path.
- [ ] **R6 - No partial commit on failure:** preflight failure leaves authoritative state untouched.

## Acceptance criteria (gated)

- [ ] **A1:** Preflight + deterministic replay applier implemented and verified (T1/T2, R1/R3/R4).
- [ ] **A2:** Restore idempotency and checkpoint continuity guaranteed (T3/T4, R2/R5).
- [ ] **A3:** Rehydration observability provides complete incident traceability (T5, R6).
