---
title: Phase 1.1.1 - Deterministic Runtime and Replay Boundary
roadmap-level: tertiary
phase-number: 1
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-19
tags: [roadmap, genesis-mythos-master, phase]
para-type: Project
subphase-index: "1.1.1"
links:
  - "[[phase-1-1-core-architecture-contracts-roadmap-2026-03-19-0001]]"
  - "[[phase-1-conceptual-foundation-and-core-architecture-roadmap-2026-03-19-1101]]"
---

## Phase 1.1.1 - Deterministic Runtime and Replay Boundary

Lock the runtime seam that makes simulation replayable and verifiable before adding deeper gameplay complexity. This tertiary note narrows 1.1 into a concrete contract for step order, fixed timestep policy, deterministic randomness, and replay verification.

### Objectives

- [ ] Freeze fixed/semi-fixed tick policy and backlog guard behavior.
- [ ] Define deterministic ordering and event/intent sort key requirements.
- [ ] Standardize replay envelope fields and checksum checkpoints.
- [ ] Isolate side effects from authoritative simulation replay.

## Runtime boundary contract (v1)

```text
interface IDeterministicRuntimeBoundary {
  begin_frame(frame_id: int, seed: string, prior_checksum: string) -> FrameContext;
  run_simulation_steps(ctx: FrameContext, intents_hash: string) -> SimulationResult;
  finalize_frame(result: SimulationResult) -> ReplayFrameRecord;
}

Invariant:
- frame_id monotonically increasing.
- dt policy remains fixed for all simulation steps in frame.
- deterministic ordering key required for every consumed intent/event.
- replay checksum emitted at end of frame.
```

### Replay envelope fields

- `frame_id`
- `dt_fixed_ms`
- `seed_root`
- `seed_derived`
- `intent_order_hash`
- `system_order_hash`
- `state_checksum_post`
- `module_versions`

## Implementation notes for deepen

- Use a stable sort key for intents: `(tick, actor_id, intent_id)`.
- For semi-fixed mode, clamp max sim steps per render frame and emit backlog warnings.
- Keep rendering and audio outside authoritative state mutation path.
- Persist checksum deltas for divergence debugging in later phases.

## Research integration

### Key takeaways

- Determinism should be treated as bit-level reproducibility from identical inputs, not as "close enough" behavior.
- Fixed or semi-fixed timestep discipline must be enforced before deeper simulation expansion.
- Floating-point and ordering footguns should be bounded by explicit policy at the runtime seam.
- Replay-safe architecture requires side-effect isolation and stable event/intent ordering.
- End-of-frame checksum validation provides a practical divergence detector for future phases.

### Decisions / constraints

- Require deterministic order hash and state checksum in every replay frame record.
- Keep authoritative simulation updates pure; presentation systems consume read-only projections.
- Bind seed derivation to replay-stable inputs to avoid hidden randomness drift.

### Links

- [[Ingest/Agent-Research/phase-1-1-1-core-abstractions-boundaries-research-2026-03-18-1622]]

## Compliance links

- [[command-event-schema-v0]]
- [[command-event-schema-v0#Message flow example (with failure branch)]]
- [[command-event-schema-v0#Failure branch assertions]]

### Sources

- [Source: Gaffer On Games - Deterministic Lockstep](https://gafferongames.com/post/deterministic_lockstep/)
- [Source: Gaffer On Games - Fix Your Timestep!](https://gafferongames.com/post/fix_your_timestep/)
- [Source: Gaffer On Games - Floating Point Determinism](https://gafferongames.com/post/floating_point_determinism/)
- [Source: EventSourcingDB - Optimizing Event Replays](https://docs.eventsourcingdb.io/best-practices/optimizing-event-replays/)
