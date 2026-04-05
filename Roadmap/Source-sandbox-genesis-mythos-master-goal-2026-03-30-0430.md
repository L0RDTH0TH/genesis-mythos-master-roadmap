---
title: Genesis Mythos Master Goal
created: 2026-03-07
updated: 2026-03-30
tags:
  - project
  - genesis-mythos
  - master-goal
  - restored-from-unaltered-capture
para-type: Project
project-id: sandbox-genesis-mythos-master
status: active
is_master_goal: true
source:
  - - Backups/Per-Change/Source-sandbox-genesis-mythos-master-goal-unaltered-capture-2026-03-07-0033-2026-03-08-0900-2026-03-11-0533-2026-03-14-1200--a8815e27--20260314-120000.md.bak
links:
  - "[[sandbox-genesis-mythos-master-Roadmap-MOC]]"
---

# Genesis Mythos Master Goal

## One-line

Build an open-source, aggressively modular first-person 3D VTT generator that procedurally creates living, collaborative open worlds from shared DM + player intents, where players experience pure immersive first-person exploration, DMs command with fluid Sparky-style free-cam + orthographic tabletop control, player lore loops into systemic depth, major changes require intentional re-generation, and every layer is built for endless community remixing.

## Vision

**Building a first-person open-world 3D virtual tabletop (VTT) generator that supports multiple RPG rule systems.**

**Perspective split:** Players stay in first-person immersion; the DM uses Sparky-inspired free-cam plus an orthographic tabletop mode for tactical work, with smooth camera interpolation between modes.

**Shared creation:** Player lore intents feed systemic hooks (reputation, events, environment). Lore stays emergent; the **systems** that enable emergence (intent pipelines, graphs, triggers) are the product focus.

**Life, agency, modularity:** Layered simulation, DM overwrites that respect live tweak vs structural re-generation, and replaceable modules across generation, simulation, cameras, and rules.

**Open source:** Interfaces-first so the community can remix stages, rulesets, sim behaviors, and UI overlays.

## Phases

### Phase 1 — Conceptual Foundation and Core Architecture

Establish the high-level blueprint and modular skeleton to align with the master goal's vision of immersion, collaboration, and extensibility.

- Define key abstractions: Separate world state, simulation logic, rendering, and input handling into decoupled layers.
- Outline the procedural generation graph and intent population pipeline, focusing on interfaces for seeds, overrides, and lore injections.
- Identify modularity seams (e.g., generation stages, rule hooks, event bus) to ensure replaceability from the start.
- Prototype basic safety invariants, like seed snapshots and dry-run validation, to embed iteration-friendly practices.

### Phase 2 — Procedural Generation and World Building

Develop the collaborative forge for creating emergent worlds, emphasizing shared intents without hardcoded narratives.

- Implement the generation pipeline: From seed parsing to terrain, biomes, POIs, entities, and simulation bootstrap.
- Integrate player/DM intent loops: Parse backstories and quests into systemic hooks (e.g., reputation graphs, event triggers).
- Enable basic collaborative dialogue: System proposes scaffolds, users refine via choices, resulting in co-authored procedural depth.
- Test initial world emergence: Ensure player agency ripples into environment and events subtly over simulated sessions.

### Phase 3 — Living Simulation and Dynamic Agency

Bring the world to life with persistent, balanced elements that reward long-term play and respect DM authority.

- Build the tick-based simulation layer: Weather cycles, NPC agendas, faction interactions, and persistent state changes.
- Incorporate DM overwrites: Real-time tweaks (e.g., token movement, event triggers) vs. deliberate re-generation for major changes.
- Layer in vitality features: Ambient surprises, consequence graphs, and evolution mechanics for meaningful campaign progression.
- Decouple simulation from visuals: Allow lightweight previews while maintaining fluidity for full sessions.

### Phase 4 — Perspective Split and Control Systems

Create immersive views tailored to roles, with seamless transitions for unbroken flow.

- Develop player perspective: Locked first-person immersion with interaction mechanics (e.g., raycasts, sensory feedback).
- Build DM controls: Free-cam god-view (flight, orbiting) and orthographic tabletop toggle for tactical precision.
- Implement camera abstraction and interpolator: Unified scene graph with smooth mode switches and easing.
- Ensure role-based agency: Players experience the world personally, DMs command with effortless dominion.

### Phase 5 — Rule System Integration and Extensibility

Incorporate RPG mechanics while prioritizing open-source remixing and communal growth.

- Integrate a core rule engine with primitives; add one initial ruleset as a plugin, declaring hooks and resolving conflicts.
- Demonstrate modularity: Swap components (e.g., biome generators, event types) without breaking cohesion.
- Enable customization: Visual styles, simulation flavors, and input types (e.g., chat-based intents) via clear interfaces.
- Foster ecosystem potential: Document seams for community contributions, turning the tool into a remixable platform.

### Phase 6 — Prototype Assembly, Testing, and Iteration

Assemble a minimal viable prototype aligned with the Q3 2026 target, focusing on playability and validation.

- Combine phases into a single-player world: One ruleset, perspective split, basic simulation (weather + NPC schedules), one intent loop, and DM overwrites.
- Conduct high-level testing: Emergent lore integration, performance dry-runs, and user flow (generation to session play).
- Embed provenance and traceability: In-game inspection of inputs and modules for debugging and export.
- Iterate conceptually: Gather feedback on immersion, agency, and modularity to refine toward full open-world VTT.

## Technical Integration

(How the conceptual vision maps to concrete architecture — without prescribing implementation details.)

**Stack policy:** Contracts and patterns are **engine- and language-agnostic** until explicitly decided; **no game engine or primary stack is selected in this vault artifact.** Roadmap links to specific engines or languages are **examples only** (see archived decisions for D-027 when needed).

- **Procedural core + intent population pipeline** — Modular generation graph (seed parsing → terrain → biome → POI → entity → simulation bootstrap) with an intent resolver that turns narrative seeds into mechanical hooks.
- **Living simulation decoupled from rendering** — Tick-based sim (weather, NPCs, factions, persistence) independent of the visual engine; structural re-generation only on explicit requests.
- **Perspective and control abstraction** — Unified scene graph; player first-person rig; DM free-flight + orthographic toggle with a swappable camera interpolator.
- **Modularity boundaries** — Staged world gen, rules-as-plugins, event bus + state graph, intent parser loop, overlay/fog/token layers as modules.
- **Safety and iteration** — Snapshot seeds/overrides/intent state; dry-run estimates before commit; provenance on generated elements.
- **Target prototype scope (Q3 2026 horizon)** — Single-player world, one ruleset, perspective split, live DM overwrites, one intent loop, basic sim, demonstrated mod seams.

## TL;DR

Open-source, modular first-person 3D VTT generator: collaborative procedural worlds, strict perspective split, emergent lore via systems, deliberate re-generation for big changes, built to remix. Normalized to Master-Goal template on 2026-03-30 for ROADMAP_MODE.

## Related

- [[sandbox-genesis-mythos-master-Roadmap-MOC]]
- Prior capture and snapshots preserved under `Backups/Per-Change/` and external backup from pipeline runs.
