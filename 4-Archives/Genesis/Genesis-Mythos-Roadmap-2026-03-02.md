---
title: Genesis Mythos Roadmap
created: 2026-03-02
tags: [genesis-mythos, roadmap, implementation]
para-type: Resource
project-id: genesis-mythos
highlight_key: Genesis-Mythos-Key
highlight_perspective: geosynchronous-view
links: ["[[Genesis-Docs-Timeline]]", "[[Genesis-Mythos-README]]", "[[Genesis-Living-Roadmap-2026-03-02-1100]]", "[[World-Building]]", "[[Mythos Tabletop]]"]
status: active
source: "[[3-Resources/Genesis-Mythos/Genesis-Living-Roadmap-2026-03-02-1100]]"
---

# Genesis Mythos — Canonical Roadmap (standardized)

Phases: 1-Maps → 2-Terrain3D → 3-Lore → 4-Combat & Equipment → 5-Politics & Factions → 6-World-Builder & Rendering. Tasks and links preserved; `highlight_perspective: geosynchronous-view`.

---

## Phase 1 — Maps (Azgaar modular + tile-based editor)

*Sources: [[Genesis-Mythos-README]], [[World-Building]]*

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

*Sources: [[Terrain3D-Integration-Guide-2026-03-02-1059]]*

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

*Sources: [[Mythos Tabletop]], timeline testing/character coverage*

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
- [[Genesis-Living-Roadmap-2026-03-02-1100]] — Living roadmap (Resources)
- [[Terrain3D-Integration-Guide-2026-03-02-1059]] — Terrain3D setup
- [[World-Building]] — Tile-based editor, biomes, city generator, 37 km²
- [[Mythos Tabletop]] — PRD: first-person, DM cam, combat, NPCs, modding
