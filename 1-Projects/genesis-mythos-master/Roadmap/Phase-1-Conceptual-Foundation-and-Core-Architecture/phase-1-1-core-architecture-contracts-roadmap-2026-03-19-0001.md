---
title: Phase 1.1 - Core Architecture Contracts
roadmap-level: secondary
phase-number: 1
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-19
tags: [roadmap, genesis-mythos-master, phase]
para-type: Project
subphase-index: "1.1"
links:
  - "[[phase-1-conceptual-foundation-and-core-architecture-roadmap-2026-03-19-1101]]"
  - "[[genesis-mythos-master-roadmap-2026-03-19-1101]]"
---

## Phase 1.1 - Core Architecture Contracts

Define architecture contracts between simulation, generation, rendering, input, and state snapshot flows so downstream phases can deepen safely without redesigning core seams.

### Objectives

- [ ] Publish fixed-timestep simulation contract and accumulator policy.
- [ ] Define immutable frame publish boundary for rendering and tooling.
- [ ] Specify deterministic ordering and seeded RNG policy for simulation systems.
- [ ] Define snapshot/restore contract for rollback, replay, and test harnesses.

## Contract signatures (v0)

```text
interface ISimulationRuntime {
  tick(frame_id: int, dt_fixed_ms: int, deterministic_seed: string) -> SimulationFrame;
}
Invariant: dt_fixed_ms constant per run; system execution order is stable and hashed per build.
```

```text
interface IGenerationPipeline {
  run_stage(run_id: string, stage_name: string, snapshot_id: string, overrides: map) -> StageResult;
}
Invariant: stage_name is enum-constrained; snapshot_id must resolve to immutable seed snapshot metadata.
```

```text
interface IRenderFramePublisher {
  publish(frame_id: int, sim_state_ref: string, interp_alpha: float) -> RenderFrame;
}
Invariant: sim_state_ref is immutable for frame_id; interp_alpha in [0,1], render cannot mutate sim state.
```

```text
interface IInputIntentIngest {
  submit_intent(intent_id: string, actor_id: string, phase_context: string, intent_text: string) -> ValidationResult;
}
Invariant: intent_id globally unique; empty intent_text rejected; validation status emitted as event.
```

```text
interface ISnapshotStore {
  create_snapshot(snapshot_id: string, seed_hash: string, module_versions: map) -> SnapshotMeta;
  restore_snapshot(snapshot_id: string) -> AuthoritativeState;
}
Invariant: seed_hash and module_versions required; restore is deterministic for identical module versions.
```

## Research integration

### Key takeaways
- Use a fixed-timestep simulation core with an accumulator; avoid variable-dt gameplay logic to preserve stability and reproducibility.
- Separate simulation tick from render frame rate; render interpolation should consume leftover accumulator time rather than changing simulation dt.
- Prefer composition-first modularity (Component pattern): isolate gameplay domains (simulation, input, rendering, audio, networking) behind clean interfaces.
- If future multiplayer/rollback is plausible, enforce deterministic constraints now: fixed tick, deterministic update ordering, seeded randomness, and platform-consistent math policy.
- Treat state serialization as a first-class architecture requirement (snapshot/restore for rollback, testing, replay, and debugging).
- Define a strict frame pipeline contract early: input sample -> simulate N ticks -> publish immutable frame state -> render.
- Add guardrails against simulation backlog (max simulation steps/frame + degrade mode) to prevent spiral-of-death behavior under load.
- Keep VFX/audio side effects decoupled from authoritative gameplay state; gameplay remains deterministic while presentation can be reconciled.

### Decisions / constraints
- **Decision candidate:** Standardize on a fixed simulation rate (e.g., 60 Hz) with render interpolation.
- **Decision candidate:** Adopt ECS-lite or component-based entity composition for Phase 1 foundation before full data-oriented migration.
- **Decision candidate:** Add a deterministic execution checklist in CI (system order hash, replay checksum, RNG seed audit).
- **Constraint:** Any subsystem requiring wall-clock time in gameplay path must be refactored behind deterministic tick-time.
- **Constraint:** Architecture must support save/load of full authoritative sim state at frame granularity.

### Sources
- [Source: Fix Your Timestep! (Gaffer on Games)](https://gafferongames.com/post/fix_your_timestep/)
- [Source: Component Pattern (Game Programming Patterns)](http://gameprogrammingpatterns.com/component.html)
- [Source: Rollback Netcode Architecture (SnapNet)](https://www.snapnet.dev/blog/netcode-architectures-part-2-rollback/)

## Tertiary notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-and-Core-Architecture"
WHERE roadmap-level = "secondary" OR roadmap-level = "tertiary" OR roadmap-level = "task"
SORT subphase-index ASC, file.name ASC
```
