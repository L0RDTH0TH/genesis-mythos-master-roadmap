---
title: Phase 1.1 Key Abstractions — research synthesis
research_query: game engine decoupled simulation rendering world state; headless deterministic serialization replay
linked_phase: Phase-1-1
project_id: genesis-mythos-master
created: 2026-03-17 04:58
tags:
  - research
  - agent-research
  - genesis-mythos-master
  - phase-1
  - ingest
  - raw-capture
  - no-template
research_tools_used:
  - web_search
  - mcp_web_fetch
agent-generated: true
para-type: Ingest
status: ingest
---

## Summary

Research for **Phase 1.1 — Key Abstractions** (world state, simulation, rendering, input as decoupled layers). Findings support: (1) world state as serializable canonical source of truth, (2) simulation layer with no direct rendering, (3) presentation/rendering consuming state and running at a different rate, (4) headless deterministic replay and input normalization.

## World state and simulation–rendering separation

Modern engines decouple simulation and rendering via **Entity-Component-System (ECS)** and explicit **simulation vs presentation** phases. Simulation advances gameplay state; presentation consumes that state for meshes, shaders, FX, and sound and can run once per rendered frame while simulation may run zero or multiple times per frame (e.g. for networking or fixed tick rate).

[Source: Simulation vs. Presentation | SnapNet](https://snapnet.dev/docs/core-concepts/simulation-vs-presentation/)

Data-oriented world state uses **cache-friendly, tightly-packed data** and deterministic updates, which are important for serialization, multiplayer sync, rollback, and replay. ECS 2.0–style designs support hierarchical world segmentation and predictable state for replay systems.

[Source: ECS 2.0 and Data-Oriented Micro-Kernel Architectures — Daydreamsoft](https://www.daydreamsoft.com/blog/ecs-2-0-data-oriented-micro-kernel-architectures-for-massive-persistent-game-worlds)

## Headless, deterministic simulation

A **headless** simulation runs without UI/rendering dependencies. Core ideas:

- **Tick-based**: discrete time steps independent of real time.
- **Deterministic execution**: pure functions, immutable state transitions, deterministic RNG (e.g. seeded LCG).
- **Event-driven**: process scheduled events and player inputs in a fixed order.
- **Full state serialization**: entire game state to JSON/binary for save, replay, and network sync.
- **Event recording**: all gameplay events recorded so identical inputs yield identical replay.

[Source: Headless game simulation concepts — search synthesis](https://github.com/Fadilix/headless-game-simulation)

Rendering can be **swappable** (2D preview, 3D, headless) because it only reads state produced by the simulation and does not feed back into it; cosmetic systems (e.g. cloth) can run once per render frame while simulation stays lightweight.

## Input and camera

Input and camera should be **normalized** into events (and optionally camera info) that the simulation accepts in a renderer-agnostic way, so the same simulation can drive different presentation layers and headless runs.

## Sources

- [Simulation vs. Presentation | SnapNet](https://snapnet.dev/docs/core-concepts/simulation-vs-presentation/)
- [ECS 2.0 and Data-Oriented Micro-Kernel Architectures for Large, Persistent Worlds | Daydreamsoft](https://www.daydreamsoft.com/blog/ecs-2-0-data-oriented-micro-kernel-architectures-for-massive-persistent-game-worlds)
- [An Extensible, Data-Oriented Architecture for High-Performance, Many-World Simulation | Erik Wijmans (Madrona)](https://wijmans.xyz/publication/madrona/)
- [Headless game simulation (determinism, serialization, replay) — GitHub / search synthesis](https://github.com/Fadilix/headless-game-simulation)

# No template selected

Paste your raw capture here. You can refactor or re-template this later.

