---
title: Azgaar Fantasy Map Generator — Research Synthesis
created: 2026-03-14
tags: [research, agent-research]
para-type: Resource
research_query: Azgaar Fantasy map generator
linked_phase: standalone
project_id: research-standalone
research_tools_used: [web_search, mcp_web_fetch]
agent-generated: true
research_distilled: true
---

> [!summary] TL;DR
> **Azgaar's Fantasy Map Generator** is a free web app that builds procedural fantasy maps from a **Voronoi diagram** (jittered square grid + repacking). Data lives in **grid** (pre-repack) and **pack** (post-repack); layers include political, biomes, heightmap, 2D/3D/globe. Customize via heightmap editor, styles, and markers; export or extend with custom JS.

---

# Azgaar Fantasy Map Generator — Research Synthesis

Synthesis of external sources on **Azgaar's Fantasy Map Generator**: a free web-based tool for procedurally generating interactive, highly customizable fantasy maps.

[Source: Azgaar's Fantasy Map Generator](https://azgaar.github.io/Fantasy-Map-Generator)  
[Source: GitHub — Azgaar/Fantasy-Map-Generator](https://github.com/Azgaar/Fantasy-Map-Generator)

---

## Overview

Azgaar's Fantasy Map Generator (FMG) is a **web application** that generates **interactive and highly customizable** fantasy maps. It supports exploration of random maps, parameter tuning, full customization, controlled generation from heightmaps, image conversion, and manual drawing. The project has substantial community adoption (e.g. 5.5k+ GitHub stars) and is actively maintained.

---

## How It Works — Core Technology

The generator uses a **Voronoi diagram** as its foundation, based on a **jittered square grid** of points. A **repacking** process then optimizes this initial diagram for the current landmass, converting the square grid into more natural-looking terrain.

[Source: Data model — Azgaar/Fantasy-Map-Generator Wiki](https://github.com/Azgaar/Fantasy-Map-Generator/wiki/Data-model)

**Data model (simplified):**

- **`grid`** — Map data *before* repacking (initial jittered square grid; used for grid-optimized data).
- **`pack`** — Map data *after* repacking; used for most operations (display, editing, export).

Voronoi data (cells, vertices, adjacencies) is computed in memory and not stored in the .map file; it is recalculated on load.

---

## Features and Capabilities

**Map layers and display:** <mark data-highlight-source="agent" style="background: #B8DAFFA6;">Political, cultural, religious, and province maps</mark>; biomes, heightmap, physical map; military positions, emblems, places of interest; environmental data (precipitation, temperature, wind, ice). Multiple view options: **2D**, **3D scene**, and **globe view**.

**Customization:** Heightmap editor (paint brushes, template editor, image converter); extensive style options (colors, textures, fonts, opacity, effects); element-level styling (borders, labels, icons, grid types). Grid types include **hex**, **square**, and **triangle**.

**Workflows:** Exploration (random maps + layer presets); tuning (template, number of states/cultures/religions, burgs); controlled generation (custom heightmaps then generate); conversion (existing map images → heightmaps); manual drawing from scratch.

**Special elements:** Markers (points of interest with notes; integration with Watabou's one-page dungeon generator). Active community (Discord, Reddit).

---

## Technical Notes (from Data Model)

- FMG exposes data in the **global namespace** (simplifies debugging and custom JS in dev console; may conflict with third-party extensions).
- **Features** represent locked areas: islands, lakes, oceans (with types: ocean, island, lake; subtypes for lakes: freshwater, salt, dry, sinkhole, lava).
- **Cells** hold elevation, precipitation, temperature, distance-from-water, feature index, and (in pack) population, area, religion, province, state, culture, burg, biome, rivers, routes, etc.
- Default **cellsDesired** is 10,000 (min 1,000, max 100,000). Typed arrays (Uint8Array, Uint16Array, Float32Array, etc.) are used for performance.

---

## Sources

- [Azgaar's Fantasy Map Generator](https://azgaar.github.io/Fantasy-Map-Generator) — main app
- [GitHub — Azgaar/Fantasy-Map-Generator](https://github.com/Azgaar/Fantasy-Map-Generator) — repo
- [Data model · Azgaar/Fantasy-Map-Generator Wiki](https://github.com/Azgaar/Fantasy-Map-Generator/wiki/Data-model) — data structures, grid vs pack, Voronoi
- [Home · Azgaar/Fantasy-Map-Generator Wiki](https://github.com/Azgaar/Fantasy-Map-Generator/wiki) — wiki index
- [Heightmap customization](https://github.com/Azgaar/Fantasy-Map-Generator/wiki/Heightmap-customization) — heightmap editing
- [Markers](https://github.com/Azgaar/Fantasy-Map-Generator/wiki/Markers) — points of interest
