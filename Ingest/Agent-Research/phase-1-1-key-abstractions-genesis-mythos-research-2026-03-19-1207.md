---
title: Research — Phase 1.1 Key Abstractions (genesis-mythos-master)
created: 2026-03-19
tags: [research, agent-research, genesis-mythos-master, Phase-1-1]
para-type: Resource
project-id: genesis-mythos-master
linked_phase: Phase-1-1
research_query: world state single source of truth; tick-based simulation decoupled from rendering; scene graph camera rig
research_tools_used: [web_search, mcp_web_fetch]
agent-generated: true
origin: roadmap-deepen
research_focus: junior_handoff
decision_priority: high
ingest_queue_entry_id: ingest-research-phase-1-1-20260319-1207
ingest_hold_reason: safety_unknown_gap
decision_candidate: true
proposal_path: Ingest/Decisions/Ingest-Decisions/Decision-for-phase-1-1-key-abstractions-genesis-mythos-research-2026-03-19-1207--2026-03-19-0701.md
---
# Research — Phase 1.1 Key Abstractions

Synthesis for **Phase-1-1 (Key Abstractions)** of project genesis-mythos-master: world state, simulation logic, rendering, and input-handling interfaces. Target audience: junior devs who need copy-paste patterns and clear boundaries.

## World state — single source of truth and snapshot semantics

- **World as central hub:** In ECS-style architectures, a **World** object is the single source of truth: it holds all entities, their components, and queries. Each world is an isolated universe; no cross-world state. [Source: fennecs Worlds](https://fennecs.tech/docs/World.html)
- **Snapshot semantics:** Data-oriented layouts (tightly packed component arrays) give predictable, cache-friendly access and support deterministic simulation so that the same inputs produce the same outputs. [Source: ECS 2.0 and Data-Oriented Micro-Kernel Architectures](https://www.daydreamsoft.com/blog/ecs-2-0-data-oriented-micro-kernel-architectures-for-massive-persistent-game-worlds)
- **Terrain and entities:** Terrain can follow a data-provider / data-consumer pattern; consumers query terrain via components (e.g. gradient signals, surface data). [Source: O3DE Terrain Architecture](https://docs.o3de.org/docs/user-guide/visualization/environments/terrain/terrain-developer-guide/architecture)
- **Interfaces to outline (from phase):** Query, mutate, snapshot on world state; clear read/write boundaries so re-generation and rollback are well-defined.

## Simulation logic — tick-based and decoupled from rendering

- **Tick bus (O3DE):** The **tick bus** is the main way components receive **per–simulation-frame** events. Prefer event-driven behavior: connect to the tick bus only when needed and disconnect when done, instead of polling every frame. [Source: Tick Bus and Components — O3DE](https://development--o3deorg.netlify.app/docs/user-guide/programming/components/tick)
- **Tick order:** Use a defined order (e.g. input → game → physics → pre-render) so dependencies are explicit. O3DE exposes presets (TICK_INPUT, TICK_GAME, TICK_PHYSICS, TICK_PRE_RENDER, etc.). [Source: Tick Bus and Components — O3DE](https://development--o3deorg.netlify.app/docs/user-guide/programming/components/tick)
- **Decoupling from rendering:** Run simulation in discrete time steps independent of frame rate; headless simulation with deterministic execution. Event buses (e.g. tick bus, notification buses) let systems subscribe only when relevant. [Source: Headless game simulation; O3DE best practices]
- **Interfaces to outline:** Simulation tick hook (e.g. OnTick(deltaTime, time)); event bus for game events; pluggable behaviors via systems that operate on component data only.

## Rendering — scene graph and camera rigs

- **Scene graph:** A hierarchy of transforms: each node has local and world transform; world is derived from parent. Traditional scene graph = tree encoding spatial relationships and update order. [Source: Scene Graph Architectures in Modern Game Engines](https://levelup.gitconnected.com/scene-graph-architectures-in-modern-game-engines-572b09f95e13)
- **Component-based nodes:** Modern approach: nodes are containers (GameObjects) with components (Transform, MeshRenderer, Camera, etc.). Camera is a component; first-person vs editor/ortho is a matter of which camera component and projection mode (perspective vs orthographic). [Source: Scene Graph Architectures; Evergine / Ursina EditorCamera docs]
- **First-person vs free-cam/ortho (DM):** Editor/ortho cameras support toggle perspective/orthographic, pan/rotate/zoom, and smoothing. For player vs DM view, use separate camera rigs or components and switch active camera. [Source: Evergine Scene Editor; Ursina EditorCamera](https://ursinaengine.org/api_reference_v8_0_0/editor_camera.html)
- **Interfaces to outline:** Scene graph or ECS-friendly transform hierarchy; camera rig interface (player vs DM, ortho toggle); interpolation for mode switches.

## Input handling and intent pipeline

- **Not covered in this fetch:** External sources focused on world state, simulation, and rendering. Phase outline stands: intent parser, population resolver, seeds/overrides/lore injections, extensible for voice/forms/chat. Pipeline stages: seed parsing → terrain → biome → POI → entity → simulation bootstrap. Prefer event-driven and notification buses so components react to input changes instead of polling.

## Decisions / constraints (candidate)

- **World:** One World (or one per logical “universe”) as single source of truth; avoid scattered state.
- **Simulation:** Tick-based, with explicit tick order; prefer connect/disconnect to tick bus over always-on polling.
- **Rendering:** Scene graph or component-based hierarchy; separate camera rigs for player vs DM with ortho toggle.
- **Interfaces:** Define query/mutate/snapshot for world state; tick hook + event bus for simulation; camera rig interface; intent pipeline stages as discrete, testable steps.

## Raw sources (vault)

- Raw content for this run was fetched via web_search and mcp_web_fetch. No separate raw note was written for this run; URLs are listed in ## Sources below.

## Sources

- [fennecs.World — central hub for entities and components](https://fennecs.tech/docs/World.html)
- [Tick Bus and Components — Open 3D Engine](https://development--o3deorg.netlify.app/docs/user-guide/programming/components/tick)
- [Scene Graph Architectures in Modern Game Engines — Level Up Coding](https://levelup.gitconnected.com/scene-graph-architectures-in-modern-game-engines-572b09f95e13)
- [ECS 2.0 and Data-Oriented Micro-Kernel Architectures — Daydream Soft](https://www.daydreamsoft.com/blog/ecs-2-0-data-oriented-micro-kernel-architectures-for-massive-persistent-game-worlds)
- [O3DE Terrain Developer Guide — Architecture](https://docs.o3de.org/docs/user-guide/visualization/environments/terrain/terrain-developer-guide/architecture)
- [Ursina EditorCamera — orthographic and perspective](https://ursinaengine.org/api_reference_v8_0_0/editor_camera.html)

## Review Needed
Proposed para-type: resource. Assigned based on content/frontmatter (confidence ~70%). Do not move until reviewed.