---
title: Phase 1.1.2 - Command Stream Validation and Fault Recovery
roadmap-level: tertiary
phase-number: 1
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-19
tags: [roadmap, genesis-mythos-master, phase]
para-type: Project
subphase-index: "1.1.2"
links:
  - "[[phase-1-1-core-architecture-contracts-roadmap-2026-03-19-0001]]"
  - "[[phase-1-1-1-deterministic-runtime-and-replay-boundary-roadmap-2026-03-19-1132]]"
---

## Phase 1.1.2 - Command Stream Validation and Fault Recovery

Define the validation and failure branch for command ingestion so deterministic replay survives malformed input, stale intents, and partial system faults. This deepens Phase 1.1 by turning the command/event contract into a concrete guardrail layer.

### Objectives

- [ ] Define pre-simulation command validation stages and rejection semantics.
- [ ] Standardize failure event payloads for deterministic replay traces.
- [ ] Lock idempotency and duplicate-command handling rules.
- [ ] Add recovery paths for subsystem timeouts without corrupting authoritative state.

## Command validation contract (v1)

```text
interface ICommandValidationPipeline {
  validate_schema(cmd: CommandEnvelope) -> ValidationResult;
  validate_authority(cmd: CommandEnvelope, actor: ActorState) -> ValidationResult;
  validate_temporal_window(cmd: CommandEnvelope, frame_id: int) -> ValidationResult;
  commit_or_reject(cmd: CommandEnvelope, result: ValidationResult) -> CommandDisposition;
}

CommandDisposition:
- accepted: command enters deterministic queue for this frame.
- rejected: emit deterministic rejection event with reason_code.
- deferred: emit retry-window event with deterministic backoff key.
```

### Failure event fields

- `frame_id`
- `command_id`
- `actor_id`
- `reason_code`
- `reason_detail_hash`
- `recovery_policy`
- `checksum_post_validation`

## Implementation notes for deepen

- Keep validation pure and deterministic before any mutable world-state transition.
- Classify failures into stable reason codes (`schema`, `authority`, `temporal`, `rate-limit`, `dependency-timeout`).
- Emit rejection/defer events into the replay stream using the same ordering key as accepted commands.
- Record recovery policy in-line so replay and diagnostics remain equivalent.

## Research integration

### Key takeaways

- Command validation must be a first-class deterministic stage, not an application-side afterthought.
- Reliable replay depends on recording rejected/deferred command outcomes as explicit events.
- Idempotency keys and stable reason-code taxonomies make fault handling reproducible and debuggable.
- Timeout/dependency failures should map to deterministic recovery policies instead of ad hoc retries.
- Event-stream systems benefit from explicit validation envelopes and immutable failure metadata.

### Decisions / constraints

- Rejections and deferrals are replay-visible events with checksum impact.
- Duplicate command IDs are deterministic no-ops with explicit reason code.
- Temporal window violations never mutate authoritative state; recovery policy defaults to defer.
- Validation pipeline executes before simulation mutation and before presentation side effects.

### Links

- [[Ingest/Agent-Research/phase-1-1-1-core-abstractions-boundaries-research-2026-03-18-1622]]
- [[command-event-schema-v0]]

### Sources

- [Source: Martin Fowler - Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html)
- [Source: Greg Young - Versioning in an Event Sourced System](https://leanpub.com/esversioning/read)
- [Source: EventSourcingDB - Event Validation and Idempotency](https://docs.eventsourcingdb.io/best-practices/common-issues/)
