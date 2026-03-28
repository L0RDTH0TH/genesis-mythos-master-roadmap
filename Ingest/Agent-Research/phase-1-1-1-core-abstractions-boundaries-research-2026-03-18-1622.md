---
created: 2026-03-18
tags: [research, agent-research, genesis-mythos-master, roadmap]
project-id: genesis-mythos-master
linked_phase: "Phase-1-1-1"
research_query:
  - "Deterministic simulation loop contracts (dt, RNG, stable ordering, checksums)"
  - "Floating point determinism constraints and replay-safe design"
  - "Event replay and side-effect isolation patterns (event sourcing)"
research_tools_used: [web_search, web_fetch]
agent-generated: true
title: "Phase-1-1-1 — deterministic replay + boundaries research"
---

## Summary
Reference notes to support Phase-1-1-1 “hard seams” decisions: (1) keep ECS boundaries explicit between world-state, simulation, rendering, input, and rules; (2) make the simulation loop replayable with deterministic ordering, fixed/semi-fixed timestep discipline, and RNG discipline; (3) design provenance + replay/checkpoint workflows so you can compare runs via checksums/diffs without hidden side effects.

## ECS boundaries that enable independent evolution
- Prefer “small components, composed features” so the world-state schema stays stable while systems evolve independently.  
  [Source: Meta Horizon — ECS Patterns](https://developers.meta.com/horizon/documentation/web/iwsdk-concept-ecs-patterns/)
- Qualify/disqualify expensive setup using queries/events rather than re-running work every frame; this keeps the render adapter and simulation step “read-only-ish” and reduces hidden coupling.  
  [Source: Meta Horizon — ECS Patterns](https://developers.meta.com/horizon/documentation/web/iwsdk-concept-ecs-patterns/)
- Ensure your event and intent streams carry stable IDs and allow deterministic sorting; otherwise replay will depend on incidental iteration order. (This is the “data contract” that backs deterministic replay.)

## Deterministic simulation loop: what to lock down
### 1) Determinism = bit-for-bit given same inputs
- Define determinism as “exactly the same result—bit-level identical—given the same initial state and the same inputs,” and enable verification via checksums of the simulated state at the end of each frame/tick.  
  [Source: Gaffer On Games — Deterministic Lockstep](https://gafferongames.com/post/deterministic_lockstep/)

### 2) Fixed or semi-fixed timestep discipline
- Use a fixed `dt` for simulation steps (or semi-fixed clamping with accumulator) so the behavior doesn’t depend on variable render framerate. Variable delta time changes the physics behavior.  
  [Source: Gaffer On Games — Fix Your Timestep!](https://gafferongames.com/post/fix_your_timestep/)
- Keep the simulation and renderer decoupled: simulation advances in discrete `dt` steps; rendering may interpolate between the last and next simulation states.  
  [Source: Gaffer On Games — Fix Your Timestep!](https://gafferongames.com/post/fix_your_timestep/)

### 3) Floating point determinism constraints (the usual footguns)
- Floating point determinism is not “automatic”; you must control compiler/architecture differences and floating-point environment settings if you want cross-run reproducibility at the bit level.  
  [Source: Gaffer On Games — Floating Point Determinism](https://gafferongames.com/post/floating_point_determinism/)

Practical implications for Phase-1.1 hard seams:
- Treat float-heavy transforms inside simulation steps as “needs determinism policy” items: either constrain your FP settings/model or route those transforms behind a “determinism boundary” (so rendering can vary without breaking replay).
- Avoid relying on map/set iteration order or unordered collections inside the simulation step; stable ordering must be part of your event/intent pipeline contract.

### 4) RNG discipline and seed derivation
- Make RNG outputs deterministic by deriving seeds from replay-stable inputs (e.g., global seed + linked phase + stage index + `from_snapshot_id` + `intents_hash`) so that “same inputs => same randomness.”
- Verify determinism by comparing end-of-frame checksums across replays; divergence is your trigger to investigate hidden nondeterminism (solver ordering, float env changes, data races, etc.).  
  [Source: Gaffer On Games — Deterministic Lockstep](https://gafferongames.com/post/deterministic_lockstep/)

## Replay / provenance / checkpoint patterns (event sourcing lessons)
- Treat replayability as first-class: design replay-safe logic (idempotent, side-effect isolated) so reconstructing state doesn’t accidentally send emails, write databases, or mutate external systems.  
  [Source: EventSourcingDB — Optimizing Event Replays](https://docs.eventsourcingdb.io/best-practices/optimizing-event-replays/)
- Use snapshots/checkpoints for restartability when history is long, and apply early filtering to avoid processing unrelated events during replay.  
  [Source: EventSourcingDB — Optimizing Event Replays](https://docs.eventsourcingdb.io/best-practices/optimizing-event-replays/)

## Concrete integration guidance for Genesis Mythos
### Minimal “replay envelope” per simulation stage
Use the vault’s existing provenance intent (software + parameters + environment) but add two replay-specific requirements:
- **Reproducibility controls**: lock the floating-point policy and timestep policy so the simulation step’s output is stable under replay.  
  [Source: Gaffer On Games — Floating Point Determinism](https://gafferongames.com/post/floating_point_determinism/)
- **Verification anchors**: compute and record (a) the end-of-stage state checksum and (b) a deterministic ordering key for intents/events so you can attribute divergence to either ordering or nondeterminism.  
  [Source: Gaffer On Games — Deterministic Lockstep](https://gafferongames.com/post/deterministic_lockstep/)

### Boundary checklist (tie-back to your Definition of Done)
- World-state schema is data-only and versioned; simulation emits deltas/events + provenance (no render writes).
- Rendering consumes a read-only world projection + events (no side effects that would break replay).
- Input produces intents only; intent publication order is stable and replayable.
- Rules engine has a dry-run validate gate; apply only after deterministic verification succeeds.

## Raw sources (vault)
- ![[Ingest/Agent-Research/Raw/phase-1-1-1-core-abstractions-boundaries-raw-2026-03-18-1622.md]]

## Sources
- [Meta Horizon — ECS Patterns](https://developers.meta.com/horizon/documentation/web/iwsdk-concept-ecs-patterns/)
- [Gaffer On Games — Deterministic Lockstep](https://gafferongames.com/post/deterministic_lockstep/)
- [Gaffer On Games — Fix Your Timestep!](https://gafferongames.com/post/fix_your_timestep/)
- [Gaffer On Games — Floating Point Determinism](https://gafferongames.com/post/floating_point_determinism/)
- [EventSourcingDB — Optimizing Event Replays](https://docs.eventsourcingdb.io/best-practices/optimizing-event-replays/)

