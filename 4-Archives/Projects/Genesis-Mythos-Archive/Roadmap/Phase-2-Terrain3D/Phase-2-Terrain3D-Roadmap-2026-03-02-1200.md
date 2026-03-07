---
title: Phase 2 — Terrain3D integration
created: 2026-03-02
tags: [genesis-mythos, roadmap, phase2, terrain3d]
para-type: Project
status: active
roadmap-level: phase
phase-number: 2
priority: high
dependencies: ["[[Phase-1-Maps-Roadmap-2026-03-02-1200]]"]
progress: 0
highlight_perspective: geosynchronous-view
project-id: genesis-mythos
links: ["[[Genesis-Mythos-Roadmap-2026-03-02-1200]]", "[[Terrain3D-Integration-Guide-2026-03-02-1059]]"]
---

# Phase 2 — Terrain3D integration

Sources: [[Terrain3D-Integration-Guide-2026-03-02-1059]], timeline `docs--terrain3d--*`. Open-world pipeline, heightmaps, regions, 2D→3D seed.

## 2.1 Data and regions

- [ ] Data directory, region size, mesh size (see integration guide)
- [ ] 2D→3D pipeline: pass generated map data (heightmaps, biomes) into Terrain3D

## 2.2 Procedural generation (from [[World-Building]])

- [ ] Seed-based generation from 2D tilemap; Perlin noise for terrain, textures, details
- [ ] LOD: terrain LOD, asset LOD, tilemap LOD; culling for voids
- [ ] Runtime-modifiable parameters, UI hooks for DM
