---
title: Phase 1 — Maps (Azgaar + tile-based editor)
created: 2026-03-02
tags: [genesis-mythos, roadmap, phase1, maps]
para-type: Project
status: active
roadmap-level: phase
phase-number: 1
priority: high
dependencies: []
progress: 0
highlight_perspective: geosynchronous-view
project-id: genesis-mythos
links: ["[[Genesis-Mythos-Roadmap-2026-03-02-1200]]", "[[Genesis-Mythos-README]]", "[[World-Building]]"]
---

# Phase 1 — Maps (Azgaar modular + tile-based editor)

Sources: [[Genesis-Mythos-README]], [[World-Building]], timeline `azgaar`, `map`, `world_builder`. 2D procedural maps, Azgaar fork + in-game tile editor; export for Terrain3D.

## 1.1 Azgaar pipeline

- [ ] Stabilize Azgaar modular map pipeline (timeline: `docs--api--AZGAAR_FORK_API`, audit reports)
- [ ] Map generation → export for Terrain3D (heightmaps, region parameters)

## 1.2 In-game tile-based map editor (from [[World-Building]])

- [ ] Freeform canvas for 256 grid sections (500 m × 500 m each, 37 km² max)
- [ ] 10×10 sub-tiles per section (50 m) for biome placement; tileset with biome variants
- [ ] Shape templates (island, continent, ring), section counter, undo/redo
- [ ] Void types for unplaced sections (ocean, lava, void); transition rules at edges
- [ ] [[Landmark Placement]]: landmarks on sub-tile grid (dungeon, river, ruin)
- [ ] [[City Generator]]: templates (human, elf, dwarf, halfling); section-based cities

## 1.3 Export & handoff to Terrain3D

- [ ] Serialize map (section positions, sub-tile biomes, void types) for 2D→3D pipeline
