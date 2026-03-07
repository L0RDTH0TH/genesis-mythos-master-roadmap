---
title: Genesis Mythos Roadmap
created: 2026-03-07
tags: [project, roadmap, genesis-mythos, vtt]
para-type: Project
project-id: genesis-mythos-master
status: active
roadmap-level: master
priority: medium
progress: 0
links: ["[[genesis-mythos-master MOC]]", "[[genesis-mythos-master-Roadmap-MOC]]", "[[Source-genesis-mythos-master-goal-2026-03-07-0033-2026-03-07-1200]]"]
---

# Genesis Mythos Roadmap

> [!tip] Full roadmap tree
> The canonical roadmap with **phase notes and Dataview** is under **Roadmap/**: [[genesis-mythos-master-Roadmap-2026-03-07-1200]]. MOC: [[genesis-mythos-master-Roadmap-MOC]]. This flat note is a legacy summary; use the full tree for sub-phases and task tracking.

Roadmap derived from [[Source-genesis-mythos-master-goal-2026-03-07-0033-2026-03-07-1200|Genesis Mythos Master Goal (source)]]. Phases align with the Master Goal v2.0 structure (perspective, world/systems, modularity, technical integration, prototype scope).

## Phase 1 — Perspective & control

Player first-person immersion; DM Sparky-style free-cam and orthographic tabletop view; smooth mode transitions.

- [ ] Lock player view to first-person only (no top-down/third-person escape) ^p1-player
- [ ] Implement DM free-flight camera (orbit, pan, zoom, tilt) ^p1-dm-cam
- [ ] Add orthographic/top-down toggle for tactical work (tokens, fog, measurements) ^p1-ortho
- [ ] Camera interpolator for mode switches (position, rotation, FOV easing) ^p1-interp

## Phase 2 — World & systems

Shared creation; player lore → systemic hooks; living simulation (weather, NPCs, persistence).

- [ ] Intent population pipeline: player/DM lore → reputation, events, environment state ^p2-intent
- [ ] Tick-based simulation layer decoupled from rendering (weather, NPC schedules, factions) ^p2-sim
- [ ] DM overwrites: live tweaks vs structural re-generation rules ^p2-overwrites
- [ ] Extensibility: swap simulation flavors, visual styles, rule behaviors ^p2-extend

## Phase 3 — Modularity & remixing

Open source; replaceable systems (gen pipeline, rule engine, simulation, input, visuals).

- [ ] World gen pipeline: stage-by-stage, each stage replaceable (noise → erosion → settlement → etc.) ^p3-gen
- [ ] Rule engine: core primitives only; rulesets as plugins (hooks & conflicts) ^p3-rules
- [ ] Simulation: event bus + state graph; new behaviors via script components ^p3-sim
- [ ] Input loop: intent parser + population resolver; extensible for voice, forms, chat ^p3-input
- [ ] Visuals & UI: overlay layers (grids, tokens, fog) as enable/disable modules ^p3-ui

## Phase 4 — Safety & iteration

Snapshots, dry-run, provenance; re-generation only on explicit structural change.

- [ ] Generation run: snapshot seed + overrides + intent state ^p4-snapshot
- [ ] Dry-run passes for performance & rule validity before commit ^p4-dryrun
- [ ] Provenance on elements (inputs, rulesets, modules) — in-game inspection or export ^p4-provenance

## Phase 5 — Prototype scope (Q3 2026)

Single-player playable world, one ruleset, full perspective split, one round-trip player intent loop, basic living sim, clear modding seams.

- [ ] Single-player playable world with one ruleset integrated ^p5-playable
- [ ] Full perspective split (player first-person, DM free-cam + orthographic) ^p5-perspective
- [ ] Live DM overwrites; one round-trip player intent loop ^p5-overwrites
- [ ] Basic living simulation (weather + simple NPC schedules) ^p5-sim
- [ ] Demonstrate modding seams (e.g. swap biome generator or add event type) ^p5-modding
