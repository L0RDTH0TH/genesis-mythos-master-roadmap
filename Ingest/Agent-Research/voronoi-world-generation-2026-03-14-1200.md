---
title: Voronoi World Generation — Research Synthesis
created: 2026-03-14
tags: [research, agent-research]
para-type: Resource
research_query: Voronoi world generation
linked_phase: standalone
project_id: research-standalone
research_tools_used: [web_search, mcp_web_fetch]
agent-generated: true
research_distilled: true
---

> [!summary] TL;DR
> **Voronoi world generation** uses sites → cells → dual graphs (Delaunay + Voronoi) for procedural maps: coastlines, elevation (distance-from-coast or tectonic uplift), rivers (steepest descent), moisture, and biomes. Use Lloyd relaxation or Poisson disc for even cells; noisy edges and libraries (d3-delaunay, PouletFrit, Delaunator) by platform.

---

# Voronoi World Generation — Research Synthesis

Synthesis of external sources on **Voronoi-based procedural world and terrain generation** for games and simulations, with focus on algorithms, implementations, and design patterns.

---

## What Are Voronoi Diagrams?

A <mark data-highlight-source="agent" style="background: #C1E1C1A6;">Voronoi diagram</mark> partitions space into regions (cells) around a set of points called **sites**. Each region contains all locations **closest** to its site compared to any other. The result looks organic: soap bubbles, cracked mud, giraffe spots.

[Source: Game Genius Lab — Voronoi in Game Dev](https://www.gamegeniuslab.com/tutorial-post/voronoi-diagrams-in-game-development-procedural-maps-ai-territories-stylish-effects/)

Formally, you drop “seeds” and each seed grows until it meets its neighbors — that’s the Voronoi partition.

---

## Why Use Voronoi for World Generation?

Voronoi diagrams are used in game dev for:

- **Procedural maps** — Natural-looking biomes, continents, island shapes, city districts.
- **Level design** — Irregular dungeon rooms, organic caves.
- **AI territories** — Divide the map into zones of control for factions or bases.
- **Resource distribution** — Cluster ores, plants, or loot in believable ways.
- **Stylized visuals** — Organic textures, magic shields, sci-fi overlays.

[Source: Game Genius Lab — Voronoi in Game Dev](https://www.gamegeniuslab.com/tutorial-post/voronoi-diagrams-in-game-development-procedural-maps-ai-territories-stylish-effects/)

Unlike pure noise (Perlin, simplex, diamond-square), Voronoi gives a **graph structure**: polygons with adjacency. That supports gameplay constraints (elevation, rivers, roads, quest locations) while still using noise for variety (coastlines, vegetation).

[Source: Amit Patel — Polygonal Map Generation for Games](http://www-cs-students.stanford.edu/~amitp/game-programming/polygon-map-generation/)

---

## Core Algorithms

<mark data-highlight-source="agent" style="background: #FFF3A3A6;">Fortune’s algorithm</mark> — O(n log n) exact construction; event-driven with a “beachline”; often implemented with a doubly connected edge list (DCEL).

**Jump Flooding Algorithm (JFA)** — GPU-friendly approximate Voronoi in logarithmic passes over a texture; good for real-time or image-space effects.

**Delaunay triangulation** — Mathematically dual to Voronoi. Many implementations (e.g. d3-delaunay, PouletFrit’s C# port, Delaunator) build Voronoi via Delaunay.

[Source: Game Genius Lab — Voronoi in Game Dev](https://www.gamegeniuslab.com/tutorial-post/voronoi-diagrams-in-game-development-procedural-maps-ai-territories-stylish-effects/)

---

## Design Patterns for Voronoi Maps

### 1. Polygons from random points

Generate random points (sites), then build Voronoi polygons. Raw random points look “clumpy”; <mark data-highlight-source="agent" style="background: #A3D8FFA6;">Lloyd relaxation</mark> (move each site to the centroid of its cell, repeat) gives more even cell sizes. Alternatively use **Poisson disc** or **jittered grid** for better distribution without iteration.

[Source: Amit Patel — Polygonal Map Generation for Games](http://www-cs-students.stanford.edu/~amitp/game-programming/polygon-map-generation/)

### 2. Two graphs: Delaunay + Voronoi

- **Delaunay graph**: nodes = polygon centers; edges = adjacency. Good for pathfinding and “which polygon is next to which.”
- **Voronoi shape graph**: nodes = polygon corners; edges = corners. Good for rendering borders and geometry.

Every Delaunay triangle corresponds to a Voronoi corner; the two are duals. Storing a combined representation (e.g. Delaunator-style) keeps both in sync.

[Source: Amit Patel — Polygonal Map Generation for Games](http://www-cs-students.stanford.edu/~amitp/game-programming/polygon-map-generation/)

### 3. Coastlines and land/water

Assign land/water to polygons (or corners) by any rule: radial blob, noise, hand-drawn shape. Coastline = edges where land meets water. Flood-fill from map border to separate ocean vs lakes.

[Source: Amit Patel — Polygonal Map Generation for Games](http://www-cs-students.stanford.edu/~amitp/game-programming/polygon-map-generation/)

### 4. Elevation

- **Distance-from-coast** — Elevation = distance from coast (mountains = far from coast). Simple and guarantees “uphill to summit, downhill to ocean” for rivers.
- **Tectonic uplift** — Define “plates,” compute boundary stress (convergent/divergent/shear), propagate uplift from boundaries inward with decay or perturbation. Add plate “density” (e.g. oceanic vs continental) to control how far uplift spreads.

[Source: Procedural Map Generation With Voronoi Diagrams (squeakyspacebar)](https://squeakyspacebar.github.io/2017/07/12/Procedural-Map-Generation-With-Voronoi-Diagrams.html)

### 5. Rivers

Pick corners (or centers) in high elevation, then follow <mark data-highlight-source="agent" style="background: #A3D8FFA6;">steepest descent</mark> corner-to-corner to the ocean. Lakes can be kept flat so rivers flow in/out naturally. River width can scale with cumulative flow (e.g. sqrt(flow)).

[Source: Amit Patel — Polygonal Map Generation for Games](http://www-cs-students.stanford.edu/~amitp/game-programming/polygon-map-generation/)

### 6. Moisture and biomes

Moisture often = distance from fresh water (rivers/lakes). Redistribute moisture (and elevation) to match desired distributions. Biomes from elevation × moisture (e.g. Whittaker-style: snow, tundra, taiga, grassland, desert, rainforest, etc.).

[Source: Amit Patel — Polygonal Map Generation for Games](http://www-cs-students.stanford.edu/~amitp/game-programming/polygon-map-generation/)

### 7. Noisy edges

Replace straight polygon edges with **noisy lines** constrained so they don’t cross. Keeps the graph for logic/pathfinding but makes the map look less obviously polygonal. Constrain noise to per-edge quads so segments don’t cross.

[Source: Amit Patel — Polygonal Map Generation for Games](http://www-cs-students.stanford.edu/~amitp/game-programming/polygon-map-generation/)

---

## Implementation Notes (Unity / code)

- **Libraries**: PouletFrit’s C# Delaunay/Voronoi port, d3-delaunay (JS), Delaunator, Wollnashorn/Voronoi (Fortune in C++). Unity projects often use PouletFrit for sections/cells, then add tectonics, elevation, and rendering (Bresenham lines, polygon fill, or LineRenderers).
- **Tectonics**: A second Voronoi for “plates” can be too regular; flood-fill from random plate sites or stress-based boundaries often gives more natural plate sizes. Store boundary edges and stress (convergent/divergent/shear) per edge; propagate uplift with decay or “vibrating” perturbation (e.g. ±10% gain to 20% loss) for less grid-like mountains.
- **Rendering**: Draw edges to texture (Bresenham + polygon fill) or use LineRenderers per edge; optionally bake to tile map for gameplay.

[Source: Procedural Map Generation With Voronoi Diagrams (squeakyspacebar)](https://squeakyspacebar.github.io/2017/07/12/Procedural-Map-Generation-With-Voronoi-Diagrams.html)

---

## Notable Projects and Demos

- **Amit Patel (Red Blob Games)** — [Polygonal Map Generation](http://www-cs-students.stanford.edu/~amitp/game-programming/polygon-map-generation/), [HTML5 demo](https://www.redblobgames.com/maps/mapgen2/), [mapgen4](https://www.redblobgames.com/maps/mapgen4/) (faster, 25k–1M polygons). Tutorial: [Voronoi maps step-by-step](https://www.redblobgames.com/x/2022-voronoi-maps-tutorial/).
- **squeakyspacebar (Andy Lo)** — [Unity Voronoi map generator](https://squeakyspacebar.github.io/2017/07/12/Procedural-Map-Generation-With-Voronoi-Diagrams.html), [Novatellus repo](https://github.com/squeakyspacebar/novatellus): tectonics, uplift, density, elevation propagation.
- **Terasology PolyWorld** — [GitHub](https://github.com/Terasology/PolyWorld): world generator based on Voronoi diagrams.
- **Game Genius Lab** — [Tutorial](https://www.gamegeniuslab.com/tutorial-post/voronoi-diagrams-in-game-development-procedural-maps-ai-territories-stylish-effects/) with d3-delaunay and step-by-step JS examples for cells, territories, and stylized effects.

---

## Summary

Voronoi world generation uses **sites → cells → dual graphs (Delaunay + Voronoi)** to get recognizable, gameplay-friendly regions (towns, quests, territories). Combine with coastlines, elevation (distance-from-coast or tectonic uplift), rivers (steepest descent), moisture, and biomes. Use noisy edges and optional noise overlays to hide the polygon grid. Choose libraries by platform (JS: d3-delaunay/Delaunator; C#/Unity: PouletFrit; C++: Fortune-style); then layer on tectonics, rivers, and biome logic per project needs.

---

## Sources

- [Game Genius Lab — Voronoi Diagrams in Game Development](https://www.gamegeniuslab.com/tutorial-post/voronoi-diagrams-in-game-development-procedural-maps-ai-territories-stylish-effects/)
- [Amit Patel — Polygonal Map Generation for Games](http://www-cs-students.stanford.edu/~amitp/game-programming/polygon-map-generation/)
- [Procedural Terrain Generation With Voronoi Diagrams (squeakyspacebar)](https://squeakyspacebar.github.io/2017/07/12/Procedural-Map-Generation-With-Voronoi-Diagrams.html)
- [Terasology PolyWorld (GitHub)](https://github.com/Terasology/PolyWorld)
- [Unity Terrain Procedural Generation — Voronoi + biomes (GitHub)](https://github.com/aurorerakoto/terrain-procedural-generation)
