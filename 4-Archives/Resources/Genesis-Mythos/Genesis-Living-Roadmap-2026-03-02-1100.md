---
title: Genesis Mythos Living Roadmap
created: 2026-03-02
tags: [genesis-mythos, roadmap, implementation]
para-type: Resource
project-id: genesis-mythos
highlight_key: Genesis-Mythos-Key
highlight_perspective: geosynchronous-view
links: ["[[Genesis-Docs-Timeline]]", "[[Genesis-Mythos-README]]", "[[Terrain3D-Integration-Guide-2026-03-02-1059]]", "[[World-Building]]", "[[Mythos Tabletop]]"]
status: active
---

## TL;DR
Single forward-living roadmap for Genesis Mythos: clean 2D Azgaar → Terrain3D pipeline plus lore, combat/equipment, politics, and world-builder wizard. Synthesized from [[Genesis-Docs-Timeline]], [[World-Building]], [[Mythos Tabletop]], and existing mythos docs. Geosynchronous flow: **Maps → Terrain3D → Lore → Combat & Equipment → Politics → Wizard & Rendering**. MVP: Phases 1–2 (maps + terrain) with DM editor and first-playable 3D slice.

---

# Genesis Mythos — Forward-Living Roadmap

Backbone: **[[Genesis-Docs-Timeline]]**. This note is the **single canonical** implementation plan: 2D-Azgaar → Terrain3D + lore, combat/equipment, politics, world-builder wizard, and rendering. Primary references: [[World-Building]] (tile-based editor, 37 km², biomes, city generator), [[Mythos Tabletop]] (PRD: first-person, DM cam, D&D 5e combat, NPCs).

## Flow (geosynchronous)

1. **Phase 1 — Maps (Azgaar / tile-based)** — 2D procedural maps, Azgaar fork + in-game tile editor
2. **Phase 2 — Terrain3D** — Open-world pipeline, heightmaps, regions, 2D→3D seed
3. **Phase 3 — Lore** — Data-driven lore, world state, narrative hooks
4. **Phase 4 — Combat & equipment** — Slots, progression, D&D 5e–style combat, homebrew support
5. **Phase 5 — Politics & factions** — Faction simulation, economy
6. **Phase 6 — World-builder wizard & rendering** — Wizard UI, rendering approach, performance

---

## Phase 1 — Maps (Azgaar modular + tile-based editor)

*Sources: [[Genesis-Mythos-README]], [[World-Building]], timeline `azgaar`, `map`, `world_builder`*

### 1.1 Azgaar pipeline
- [ ] Stabilize Azgaar modular map pipeline (timeline: `docs--api--AZGAAR_FORK_API`, audit reports)
- [ ] Map generation → export for Terrain3D (heightmaps, region parameters)

### 1.2 In-game tile-based map editor (from [[World-Building]])
- [ ] Freeform canvas for 256 grid sections (500 m × 500 m each, 37 km² max)
- [ ] 10×10 sub-tiles per section (50 m) for biome placement; tileset with biome variants
- [ ] Shape templates (island, continent, ring), section counter, undo/redo
- [ ] Void types for unplaced sections (ocean, lava, void); transition rules at edges
- [ ] [[Landmark Placement]]: landmarks on sub-tile grid (dungeon, river, ruin)
- [ ] [[City Generator]]: templates (human, elf, dwarf, halfling); section-based cities

### 1.3 Export & handoff to Terrain3D
- [ ] Serialize map (section positions, sub-tile biomes, void types) for 2D→3D pipeline

---

## Phase 2 — Terrain3D integration

*Sources: [[Terrain3D-Integration-Guide-2026-03-02-1059]], timeline `docs--terrain3d--*`*

### 2.1 Data and regions
- [ ] Data directory, region size, mesh size (see integration guide)
- [ ] 2D→3D pipeline: pass generated map data (heightmaps, biomes) into Terrain3D

### 2.2 Procedural generation (from [[World-Building]])
- [ ] Seed-based generation from 2D tilemap; Perlin noise for terrain, textures, details
- [ ] LOD: terrain LOD, asset LOD, tilemap LOD; culling for voids
- [ ] Runtime-modifiable parameters, UI hooks for DM

---

## Phase 3 — Lore support systems

*Sources: Timeline data schemas, [[docs--SYSTEM_IMPLEMENTATIONS]]*

- [ ] Lore data schema and loading
- [ ] World state / narrative hooks for sessions

---

## Phase 4 — Combat & equipment

*Sources: [[Mythos Tabletop]], timeline testing/character coverage, data schemas*

### 4.1 Core combat
- [ ] D&D 5e–style turn-based combat: initiative, actions/bonus/reactions, grid movement, d20
- [ ] Status effects, environmental interactions, class abilities, spells, inventory

### 4.2 DM tools and homebrew
- [ ] [[DM Free Camera]]: spawn assets, lighting, weather; turn order, target highlighting
- [ ] Combat customization: initiative rules, homebrew mechanics via AI-parsed natural language
- [ ] Equipment slots, progression loops; save/share custom rule sets

### 4.3 Player experience
- [ ] [[First-Person Player Experience]]: WASD, jump, sprint, interactions ([[Mythos Tabletop]])

---

## Phase 5 — Politics & factions

*Sources: [[Genesis-Mythos-README]] (singletons), timeline architecture*

- [ ] Faction simulation (EntitySim, FactionEconomy)
- [ ] Politics/faction dynamics; NPC allegiances and world state

---

## Phase 6 — World-builder wizard & rendering

*Sources: Timeline `docs--WORLD_BUILDER*`, `docs--technical--RENDERING*`, GUI specs*

- [ ] Wizard flow consolidation (WORLD_BUILDER_WIZARD_GUIDE, WORLD_BUILDER_API_REFERENCE)
- [ ] Rendering approach comparison (RENDERING_APPROACH_COMPARISON)
- [ ] Performance vs visual fidelity; 60 FPS baseline ([[Mythos Tabletop]])
- [ ] NPC integration: city templates → NPCs; AI agent for dialogue; routines, factions

---

## Related

- [[Genesis-Docs-Timeline]] — Chronological backbone
- [[Genesis-Mythos-README]] — Project rules, singletons
- [[Terrain3D-Integration-Guide-2026-03-02-1059]] — Terrain3D setup
- [[World-Building]] — Tile-based editor, biomes, city generator, 37 km²
- [[Mythos Tabletop]] — PRD: first-person, DM cam, combat, NPCs, modding

## Next steps

- [ ] Expand Phase 1–2 subphases from timeline + [[World-Building]] for MVP
- [ ] Run related-content-pull per phase for cross-links
- [ ] Lock MVP scope: Phases 1–2 + minimal Phase 4 (first-playable 3D + basic combat)

> [!tip] **CTA — MVP implementation**
> Prioritize **Phase 1 (Maps)** and **Phase 2 (Terrain3D)** for a first-playable 3D slice: tile-based editor → export → Terrain3D with LOD. Then add Phase 4 combat (initiative, grid, one combat flow). Share this roadmap from the project MOC for implementation tracking.
