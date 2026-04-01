---
title: Phase 1.1 — Layering and Interface Contracts
roadmap-level: secondary
phase-number: 1
subphase-index: "1.1"
project-id: genesis-mythos-master
status: active
priority: high
progress: 40
handoff_readiness: 82
created: 2026-03-30
tags:
  - roadmap
  - genesis-mythos-master
  - phase-1
para-type: Project
links:
  - "[[Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-03-30-0430]]"
---

## Phase 1.1 — Layering and interface contracts

This secondary slice names the **four-layer stack** (world state, simulation, rendering, input), the **direction of data flow** between them, and the **interface contracts** each layer exposes to its neighbors. It turns the Phase 1 primary promise into something implementers can sketch without choosing a specific engine.

## Scope

**In scope:** Layer identities; which subsystem owns persistence vs ephemeral buffers; one-way vs two-way dependencies; contract surfaces (what each layer may call or observe on another); ordering guarantees for tick/frame/input; where procedural generation **injects** into the stack (typically before or beside live simulation, not inside the render loop).

**Out of scope:** Concrete class names, threading models, GPU APIs, network sync, plugin ABI, file formats, and execution-track test/CI obligations. **Execution-deferred:** rollup/registry/HR closure artifacts and CI gates are advisory for conceptual completion.

## Behavior (natural language)

- **World state** holds authoritative entities, components, and narrative facts that must survive saves and reloads. It is the **only** layer that may commit durable changes to the “truth” of the campaign world.
- **Simulation** advances time: applies rules, resolves intents, schedules deferred effects, and emits **proposed mutations** to world state (or applies them through a single commit API so rendering never sees half-applied state).
- **Rendering** reads a **snapshot** or **view model** derived from world state + simulation outputs; it never pushes authoritative state backward except through explicit UI/edit channels that still route through input → simulation → world state.
- **Input** collects DM/player/device events, normalizes them into **intents**, and delivers them to simulation (or to a dedicated tool mode that may bypass play simulation but still respects world-state commit rules).
- **Ordering:** On each frame/tick: **input dispatch → simulation step → world state commit (if any) → render read**. Generation pipelines run **outside** this loop or in explicit “offline” stages that complete before play resumes.

## Interfaces

- **World state → simulation:** Query API for current entities; simulation requests mutations via **transactional** or **staged** commits; no direct field writes across the boundary without going through the commit path.
- **Simulation → rendering:** Emits **render model** or **diff** (what changed for views); render does not call simulation except through scheduled queries (e.g. prediction), which remain read-only on authoritative state.
- **Input → simulation:** Intent objects with source, target, and timestamp; simulation validates and may reject or queue; conflicts resolve per policy (see Edge cases).
- **Generation → world state / simulation:** Injects seeds, graphs, or overrides through **named injection points** (stages) so later phases can replace generators without rewriting the spine.
- **Adjacent slices:** Primary Phase 1 note defines modularity seams; Phase 2 deepens **generation graph**; Phase 4 **perspective/control** consumes render/input boundaries documented here.

## Edge cases

- **Frame-rate vs simulation rate:** If decoupled, define which clock owns “authoritative time” and how render interpolation relates to committed state (TBD execution detail; conceptual default: single authoritative sim clock).
- **Destructive regeneration:** Any replace of large world regions must go through **snapshot + dry-run** before commit (invariant from PMG); this slice names the **hook** only.
- **Concurrent intents:** DM override vs player lore on the same entity — defer to execution-track merge policy; here: **single committer** rule (one pipeline owns merges per entity per tick).

## Open questions

- Whether **replay** requires deterministic simulation from intents alone, or may snapshot world state at checkpoints (affects how much history simulation must retain).
- Minimum **contract** for mod plugins: event-bus topics only vs shared types (left open until execution plugin spec).

## Pseudo-code readiness

Readers can sketch **interface sketches** (function-shaped bullets) without a real codebase: e.g. `commit(WorldDelta)`, `render(ViewModel)`, `dispatch(Intent)`. Full pseudo-code and API signatures belong to **tertiary** notes (**1.1.1+**) or execution track; this secondary stops at **contract clarity**, not implementation.

## Research integration

> [!note] External grounding
> No `Ingest/Agent-Research/` notes were bound this run; alignment is **pattern-only** from established layered-game architecture practice.

## Tertiary notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layering-and-Interface-Contracts"
WHERE roadmap-level = "tertiary" OR roadmap-level = "task"
SORT subphase-index ASC, file.name ASC
```
