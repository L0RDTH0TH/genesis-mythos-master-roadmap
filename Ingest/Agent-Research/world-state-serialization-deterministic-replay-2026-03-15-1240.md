---
title: World State — Serialization, Tick Boundary, and Deterministic Replay (Research)
research_query: ECS world state serialization deterministic replay; tick-boundary state management
linked_phase: Phase-1-1-1
project-id: genesis-mythos-master
created: 2026-03-15
tags: [research, agent-research, genesis-mythos-master, world-state]
research_tools_used: [web_search, mcp_web_fetch]
agent-generated: true
---

## Summary

Research for **Phase-1-1-1 (World State)** of genesis-mythos-master: canonical world state, serialization for save/replay, and tick-boundary invariants. Prioritized handoff-oriented material: schema options, implementation patterns, and open-source references.

---

## Vault context (Phase-1-1-1)

- **World state** = single authoritative snapshot; all simulation reads/writes through it; no renderer/input mutates it directly.
- **Serialization contract**: export/import to stable format (JSON or binary) for save, rollback, headless replay; deterministic round-trip.
- **Tick/event boundary**: state transitions at discrete steps; presentation consumes state read-only per frame.
- **Algorithm**: Capture (normalized input, no render) → Update (systems in fixed order, mutate world only) → Expose (rendering reads state) → Persist (serialize full state + optional event log).

---

## 1. World state serialization (ECS and schema)

**Binary + delta encoding:** Colyseus Schema provides an incremental binary state serializer with delta encoding for games, reducing bandwidth by sending only state changes.

[Source: Colyseus Schema — incremental binary state serializer](https://github.com/colyseus/schema)

**Full state snapshots and round-trip:** Several ECS stacks support full world save/load for deterministic replay:

- **chromealex/ecs (Unity)**: automatic game state rollbacks and persistence.
- **IndigoECS**: built for rollback netcode and state save/load.
- **archetype_ecs (Rust)**: `save_world()` / `load_world()`, plus `Scene`, `EntityData`, and `SerializationRegistry` for serializable world snapshots.

[Source: archetype_ecs serialization](https://docs.rs/archetype_ecs/latest/archetype_ecs/serialization/index.html)

**Schema and formats:** Legion uses Serde-based `WorldSerializer` with component type mapping. Bevy Serde Lens adds stateful, structural serialization (JSON and binary). Rapier-style physics state export typically serializes RigidBodySet, ColliderSet, JointSet, etc., to string/file for exact world restore.

**Takeaway:** For a single WorldState snapshot, support both full serialization (save/replay) and, if needed later, delta encoding for sync. Prefer deterministic ordering of entities/components when serializing (e.g. stable sort by entity id) for round-trip consistency.

---

## 2. Tick-boundary and “no render in simulation”

**Problems with per-entity Tick():** Per-entity `Tick()`/`Update()` leads to undefined ordering, awkward multi-pass updates, and extra overhead. Dependencies between entities are hard to reason about when tick order is implicit.

[Source: Why you should avoid Tick()/Update() functions — Matt Gibson](https://mattgibson.dev/blog/tick-functions)

**Manager pattern:** Use a single manager (or system scheduler) that owns the update order: loop over entities/systems in an explicit sequence (e.g. physics → rules → intent), so dependencies and passes are visible in one place. Multiple passes per frame (e.g. first pass then second pass) are just multiple loops in that manager, with no frame delay.

**Fixed tick and render separation:** Run simulation at a fixed timestep; rendering runs after simulation and can interpolate. Phases such as `onPreTick` → `onTick` → `onPostTick` give a clear tick boundary. Presentation reads state only; it never mutates world state.

**Takeaway:** Aligns with Phase-1-1-1: “state transitions at discrete simulation steps”; “presentation layer consumes state as read-only per frame.” Implement a single update path (Capture → Update → Expose → Persist) with explicit system order and no render calls inside Update.

---

## 3. Deterministic replay and multiplayer sync

Deterministic replay and lockstep multiplayer both rely on:

- **Identical initial state** and **identical input sequence** (or event log).
- **Stable serialization**: same ordering and encoding so that the same bytes produce the same in-memory state.
- **No non-determinism in simulation**: avoid unseeded RNG, system-order dependence (beyond the chosen fixed order), and platform-specific float or time behavior in the sim.

Colyseus Schema and ECS world save/load (e.g. archetype_ecs, IndigoECS) are used in practice for state snapshots and replay; delta encoding helps for network sync without sending full state every tick.

---

## Tasks (from phase) — research-informed

- **Define WorldState schema**: Prefer entity/component or key-value layout that is serializable (e.g. Serde/reflection or schema registry). Document entity and component ordering for deterministic serialization.
- **Implement serialization/deserialization**: Use deterministic ordering (e.g. entity id, then component type order). Consider binary for size/speed and JSON for debugging; round-trip tests are essential.
- **Document tick-boundary and no-render invariant**: State transitions only in Update; rendering and input normalization never mutate world state; explicit system order in one place (manager or scheduler).

---

## Sources

- [Colyseus Schema — incremental binary state serializer with delta encoding](https://github.com/colyseus/schema)
- [Why you should avoid Tick()/Update() functions — Matt Gibson](https://mattgibson.dev/blog/tick-functions)
- [Rapier — export/import world state (Issue #111)](https://github.com/dimforge/rapier/issues/111)
- [archetype_ecs::serialization — Rust](https://docs.rs/archetype_ecs/latest/archetype_ecs/serialization/index.html)
- [Legion serialize](https://docs.rs/legion/latest/legion/serialize/index.html)
- [Bevy Serde Lens — stateful structural serialization](https://github.com/mintlu8/bevy_serde_lens)
- [Harmony-ECS World](https://3mcd.github.io/harmony-ecs/modules/World.html)
- [chromealex/ecs — Unity ECS with rollbacks](https://github.com/chromealex/ecs)
