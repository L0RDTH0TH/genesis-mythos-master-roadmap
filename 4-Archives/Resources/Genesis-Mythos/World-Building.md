---
para-type: resource
project-id: Genesis-Mythos
status: active
---
## Overview
The updated World-Building System enables Dungeon Masters (DMs) to create a 37-square-kilometer game world with customizable, non-square shapes by arranging modular grid sections (tiles) on a freeform canvas. Each section contains sub-tiles for fine-grained biome control, allowing detailed placement within the broader map shape. DMs can use all 256 sections or a subset for unique layouts (e.g., irregular continents, archipelagos, narrow strips). The system includes pre-defined shape templates, a section counter, and customizable void types (e.g., ocean, lava) for unplaced sections. Built in Godot 4.x, it leverages the tilemap system, Perlin noise, and LOD for flexibility and performance.

## 1. Hybrid World Generation
The Hybrid World Generation system allows DMs to construct a 2D map by arranging grid sections to define the overall shape, with sub-tiles for detailed biome placement. This seeds procedural generation for a 3D world with terrain, textures, and assets.

### 1.1 In-Game Tile-Based Map Editor
- **[[World building gui]]**: A 2D editor in DM mode with a freeform canvas for arranging grid sections and a sub-tile editor for biome placement within sections. The dynamic tilemap system supports non-contiguous, pmnon-square layouts and intuitive UI features.
- **Tile-Based Section Placement**:
  - **Grid Sections**: The world is divided into a pool of 256 sequential grid sections, each approximately 500 m × 500 m (calculated as √(37 km² / 256) ≈ 380 m, rounded for simplicity). Each section represents a modular piece of the map.
  - **Sub-Tiles**: Each section contains a 10x10 grid of sub-tiles (50 m × 50 m each), allowing fine-grained biome placement within the section’s boundaries.
  - **Available Biomes**: Forests, deserts, mountains, plains, swamps, tundra, coastal regions, volcanic areas.
  - **Tileset**: Each biome has sub-tile variants (e.g., forest: pine, oak, jungle, clearing; desert: dunes, oasis, rocky outcrop; plains, river) for visual diversity.
  - **Section Arrangement**:
    - DMs select sections from a pool of 256 tiles and place them on a freeform canvas (no fixed grid boundaries).
    - Sections can be placed adjacent to others, rotated (0°, 90°, 180°, 270°), scaled (±10% for variation), or left unplaced to create gaps.
    - Example shapes: Crescent-shaped archipelago, cross-shaped continent, or narrow peninsula.
    - Sections snap to a virtual grid (500 m increments) for alignment.
    - DMs can use all 256 sections (37 km²) or fewer for smaller maps (e.g., 100 sections ≈ 14.5 km²).
  - **Sub-Tile Biome Placement**:
    - Within each section, DMs place biomes on the 10x10 sub-tile grid (50 m resolution) for detailed control.
    - Example: A section could have 60 forest sub-tiles (dense trees), 30 plains sub-tiles, and 10 swamp sub-tiles, creating a mixed-biome area.
  - **Placement Tools**:
    - **Single-Section Placement**: Select and left-click canvas in desired position.
    - **Multi-Section Placement**: Arrange multiple sections in patterns (e.g., line, cluster, circle) for quick layout, left-click to place.
    - **Shape Templates**: Pre-defined map shapes (e.g., “island,” “continent,” “ring”) auto-arrange sections to approximate the shape, adjustable by the DM.
    - **Section Counter**: Displays “X/256 sections used” in the UI, with a progress bar showing the map’s area (e.g., “14.5/37 km²”).
    - **Sub-Tile Placement**: Single sub-tile placement or fill tool to apply biomes across sub-tile regions within a section.
    - **Transition Rules**: Automatically blend sub-tile edges (e.g., desert dunes to plains grass) and section boundaries for seamless visuals.
    - **Undo/Redo**: Tracks section and sub-tile placements for easy editing.
    - **Tile Palette**: Searchable palette of biome sub-tiles and variants, with sliders for metadata (e.g., tree density, tree age, dune height, oasis rate).
  - **[[Biome Properties]]**: Each sub-tile has metadata (e.g., elevation: 0.0–1.0, vegetation density: 0.0–1.0, water presence: 0.0–1.0) adjustable via sliders, influencing procedural generation.
- **[[Landmark Placement]]**:
  - DMs place landmark sub-tiles (e.g., dungeon entrance, river, ruin, ancient tree) within a section’s 10x10 sub-tile grid (5 m increments for precision).
  - Landmarks have customizable properties (e.g., dungeon type: crypt, fortress; river width) and support rotation/scaling.
- **[[City Generator]]**
  - **Templates**: Premade city sub-tile sets for four species/races:
    - Human: Medieval towns with cobblestone roads, taverns, market squares.
    - Elf: Tree-cities with organic platforms, vine-covered structures.
    - Dwarf: Stone fortresses with carved halls, defensive walls.
    - Halfling: Burrow-villages with hobbit-like homes, winding paths.
  - **Customization**: DMs swap sub-tiles within a section (e.g., tavern to temple) or add unique structures (e.g., wizard’s tower).
  - **Section-Based Cities**: Cities can span multiple sections (e.g., 4 sections for a large city), with procedural streets and props (e.g., lanterns, carts) based on template rules.
  - **Procedural Details**: Sections with city sub-tiles are auto-populated with procedural elements tailored to the race’s aesthetic.
- **Void Customization**:
  - Unplaced sections are treated as voids, with DM-selectable types:
    - **Ocean**: Procedural water with waves, shallow reefs, or deep trenches.
    - **Lava**: Molten flows, volcanic ash, or glowing fissures.
    - **Void Space**: Empty or ethereal space, with optional particle effects (e.g., fog, stars).
  - DMs can adjust void properties (e.g., wave height for ocean, glow intensity for lava) via sliders.
  - Procedural transitions (e.g., beaches for ocean-adjacent coastal sections, scorched edges for lava-adjacent sections) enhance immersion.

### 1.2 Procedural Generation
- **Seed-Based Generation**: The arranged sections and their sub-tiles (dynamic 2D tilemap) seed Godot’s Perlin noise algorithm for 3D terrain, textures, and details.
  - **Terrain**: Elevation maps derived from sub-tile metadata (e.g., high elevation for mountain sub-tiles).
  - **Textures**: Biome-specific textures (e.g., sand for desert sub-tiles) with blending at sub-tile and section boundaries.
  - **Details**: Procedural asset placement (e.g., trees, rocks, caves) using noise, respecting sub-tile properties (e.g., dense forest sub-tiles have more trees).
  - **Non-Contiguous Maps**: Unplaced sections generate as the selected void type (e.g., ocean with waves), with procedural transitions at map edges (e.g., cliffs for coastal sections near lava voids).
- **Scale**: Maximum world size is 37 km² (256 sections, each 500 m × 500 m). Smaller maps use fewer sections (e.g., 100 sections ≈ 14.5 km²). Sub-tiles (50 m × 50 m) provide fine granularity within sections.
- **Level of Detail (LOD) System**:
  - **Terrain LOD**: Multiple LOD levels for terrain meshes (high-detail near players, low-detail at distance).
  - **Asset LOD**: Environmental assets use simplified models or impostors at greater distances.
  - **Tilemap LOD**: Distant sections/sub-tiles use lower-resolution textures or merged geometry.
  - **Implementation**: Godot’s LOD system with custom shaders for seamless transitions.
  - **Non-Square Optimization**: Prioritizes sections in the player’s view frustum, culling unplaced sections (voids) for performance.

### Example Workflow
1. DM opens the tile-based editor and selects the “crescent” shape template, which auto-arranges 100/256 sections (500 m × 500 m each) into a crescent-shaped map (~14.5 km²).
2. DM refines the layout by moving sections and leaving gaps for an ocean void, setting void type to “ocean” with high wave intensity.
3. Within sections:
   - Places forest sub-tiles (10x10 grid, 50 m each) in the northern arc, adjusting tree density to 0.9.
   - Places desert sub-tiles in the southern arc, setting dune height to 0.4.
   - Places mountain sub-tiles in the center, setting elevation to 0.8.
4. DM places a human town section near the forest, customizing it with a castle sub-tile, and a dwarven fortress section in the mountains.
5. The system generates a 3D world with detailed terrain (e.g., rolling hills in forests, jagged peaks in mountains), procedural streets/NPCs in cities, and ocean waves in voids with beach transitions.
6. LOD ensures distant mountain sections use low-poly models, while nearby town sub-tiles remain high-resolution.

---

### Technical Considerations
- **Tilemap System**: Each section is a Godot TileMap node with a 10x10 sub-tile grid. The freeform canvas is a parent node managing section positions/rotations.
- **Performance**: Sub-tiles increase data complexity, but LOD and culling (especially for voids) mitigate performance impacts. Sections are loaded/unloaded based on player proximity.
- **Serialization**: Map data (section positions, sub-tile biomes, void types) is saved as JSON, including metadata and void properties.
- **Godot Integration**: Uses Godot’s TileMap for sub-tiles, MultiMesh for procedural assets, and shaders for LOD/void transitions.

## Why resource?
Assigned based on content/frontmatter (confidence ~85%).