---
confidence: 70%
created: 2026-03-02
status: ingest
para-type: Resource
proposal_path: Ingest/Decisions/Decision-for-city-generator--2026-03-04-0439.md
decision_priority: high
---
The City Generator is a modular subsystem within the In-Game Tile-Based Map Editor, designed to streamline the creation of populated settlements that integrate seamlessly with the hybrid world generation pipeline. It builds on the section and sub-tile framework, allowing DMs to place and customize cities that span one or more sections (e.g., a small village in a single 500 m × 500 m section or a sprawling metropolis across 4–9 sections). Cities are generated using race-specific templates as a foundation, which define aesthetic, structural, and procedural rules. These templates ensure thematic consistency while offering extensive customization options.

The generator uses a combination of predefined sub-tile sets, procedural algorithms (leveraging Godot's noise functions and pathfinding), and user-editable metadata to populate sections with buildings, roads, NPCs, and interactive elements. Cities can be placed on compatible biomes (e.g., human towns on plains or forests, dwarven fortresses on mountains), with automatic adaptations for terrain (e.g., elevating structures on uneven ground). Procedural details are seeded from the section's sub-tile biomes and metadata, ensuring harmony with the surrounding environment.

#### Key Features
- **Template Selection**: DMs choose a race template from a dropdown in the tile palette, which applies a default sub-tile layout to the selected section(s). Templates include visual previews and lore snippets for inspiration.
- **Multi-Section Support**: For larger cities, DMs select a cluster of adjacent sections (e.g., 2x2 grid) and apply the template across them. The system auto-generates connecting elements like roads or walls between sections.
- **Procedural Population**:
  - **Structures**: Placed via a density map derived from Perlin noise, modulated by sub-tile metadata (e.g., higher building density in urban cores).
  - **Roads and Paths**: Uses A* pathfinding to create networks connecting key landmarks, with width and material varying by race (e.g., wide cobblestone for humans, narrow vines for elves).
  - **Props and Details**: Scatter systems place race-specific items (e.g., market stalls, lanterns) using MultiMeshInstance for efficiency.
  - **NPCs**: Procedural NPC spawns (e.g., 10–50 per section) with basic AI behaviors, tied to city type. Quests assigned from a session prep pool (e.g., "tavern owners share quest pools, blacksmiths share quest pools").
- **Customization Tools**:
  - **Sub-Tile Swapping**: Drag-and-drop to replace default sub-tiles (e.g., swap a house for a shop).
  - **Metadata Sliders**: Adjust city-wide properties like population density (0.0–1.0), wealth level (influencing building quality), or defense rating (adding walls/towers).
  - **Unique Additions**: Place custom landmarks (e.g., a dragon statue) from a shared palette, with support for scripting interactions.
  - **Blending with Biomes**: Automatic overrides for sub-tiles (e.g., a forest city replaces some ground with tree platforms).
- **Performance Optimizations**: Cities use LOD for buildings (e.g., detailed facades up close, simplified meshes at distance) and occlusion culling. Non-visible sections unload NPC AI.
- **Serialization**: City data (template ID, custom sub-tiles, metadata) is stored in the map's JSON, allowing easy loading and sharing.

#### Race-Specific Templates
Each template defines a 10x10 sub-tile layout pattern per section, with variants for core (dense urban), edge (suburban), and extension (outskirts) sections in multi-section cities. Sub-tiles are categorized as structural (buildings), connective (roads), open (plazas), or decorative (gardens). Procedural rules ensure variety, such as randomizing building orientations or adding wear effects.

1. **Human: Medieval Towns**
   - **Aesthetic**: Rustic, practical architecture with timber-framed houses, thatched roofs, and stone accents. Inspired by European medieval villages, emphasizing community hubs like markets and inns.
   - **Default Sub-Tile Layout (Per Section)**:
     - 40% Residential: Cottages, multi-story homes (variants: small hut, family house).
     - 20% Commercial: Taverns, blacksmiths, markets (variants: open stall, enclosed shop).
     - 15% Civic: Town hall, temple, guard tower.
     - 15% Open Space: Cobblestone plazas, fountains, parks.
     - 10% Connective: Winding roads (2–4 sub-tiles wide), alleys.
   - **Procedural Details**:
     - Roads: Cobblestone with procedural cracks and puddles; connect to biome edges (e.g., dirt paths in adjacent forests).
     - Props: Carts, barrels, hanging signs; weather effects like smoke from chimneys.
     - NPCs: Farmers, merchants, guards; behaviors include patrolling or bartering.
     - Customization Examples: Add a castle (replaces 4–6 sub-tiles with fortified walls and keep); increase wealth for gilded roofs.
     - Multi-Section Example: Core section as market square, edges as residential districts, extensions as farms blending into plains biomes.

2. **Elf: Tree-Cities**
   - **Aesthetic**: Organic, nature-integrated designs with elevated platforms on ancient trees, vine bridges, and bioluminescent elements. Emphasizes harmony with the environment, suitable for forest or swamp biomes.
   - **Default Sub-Tile Layout (Per Section)**:
     - 35% Residential: Treehouses, woven pods (variants: single canopy dwelling, communal hall).
     - 25% Natural Integration: Giant trees, glowing fungi groves.
     - 15% Civic: Elder council platforms, shrines to nature spirits.
     - 15% Open Space: Suspended gardens, waterfalls.
     - 10% Connective: Vine bridges, spiral staircases around trunks.
   - **Procedural Details**:
     - Roads: Elevated walkways with procedural sway animations; adapt to tree density from sub-tile metadata.
     - Props: Crystal lanterns, enchanted runes, hanging vines; particle effects for fireflies.
     - NPCs: Rangers, druids, artisans; behaviors include meditating or crafting.
     - Customization Examples: Add an ancient tree landmark (central sub-tile with glowing core); scale platforms for denser forests.
     - Multi-Section Example: Core as sacred grove, edges as living quarters, extensions as hunting grounds with seamless tree transitions.

3. **Dwarf: Stone Fortresses**
   - **Aesthetic**: Sturdy, underground-inspired carvings with rune-etched stone walls, forges, and defensive ramparts. Geared toward mountain or volcanic biomes, focusing on craftsmanship and fortification.
   - **Default Sub-Tile Layout (Per Section)**:
     - 40% Residential: Carved halls, clan dwellings (variants: simple barracks, ornate chambers).
     - 20% Industrial: Forges, mineshafts, workshops.
     - 15% Civic: Throne room, armory, grand hall.
     - 15% Defensive: Walls, towers, gates.
     - 10% Connective: Tunnels, stone bridges.
   - **Procedural Details**:
     - Roads: Chiseled stone paths with rail tracks for carts; integrate with elevation metadata for multi-level designs.
     - Props: Anvils, gem veins, statues; lighting from lava lamps or torches.
     - NPCs: Miners, warriors, smiths; behaviors include forging or mining.
     - Customization Examples: Add a deep mine (sub-tiles with procedural cave extensions); reinforce defenses for higher threat levels.
     - Multi-Section Example: Core as great hall, edges as living quarters, extensions as outer walls blending into rocky terrain.

4. **Halfling: Burrow-Villages**
   - **Aesthetic**: Cozy, earthy homes dug into hillsides with rounded doors, gardens, and communal gathering spots. Inspired by hobbit lore, ideal for plains or coastal biomes, emphasizing comfort and community.
   - **Default Sub-Tile Layout (Per Section)**:
     - 45% Residential: Hobbit holes, burrow clusters (variants: single family, extended warren).
     - 20% Agricultural: Gardens, orchards, bakeries.
     - 15% Civic: Meeting hall, inn, festival grounds.
     - 15% Open Space: Rolling lawns, ponds.
     - 5% Connective: Winding dirt paths, hedgerows.
   - **Procedural Details**:
     - Roads: Soft dirt trails with procedural flower borders; curve naturally around terrain contours.
     - Props: Picnic tables, pipe-weed plants, colorful doors; ambient sounds like laughter or baking.
     - NPCs: Farmers, storytellers, cooks; behaviors include gardening or feasting.
     - Customization Examples: Add a grand burrow (larger sub-tile with multiple rooms); incorporate water features for pond-side homes.
     - Multi-Section Example: Core as village green, edges as family burrows, extensions as farmlands transitioning to surrounding biomes.

#### Implementation Notes in Godot 4.x
- **Core Nodes**: Each city section uses a TileMap for base layout, with child nodes for procedural elements (e.g., NavigationRegion2D for paths, MultiMeshInstance3D for props).
- **Procedural Scripts**: GDScript functions for generation:
  - `generate_city(template_id: String, sections: Array[Node])`: Applies template, runs noise-based placement, and connects sections.
  - `blend_with_biome(sub_tile: TileData)`: Adjusts assets (e.g., add snow to tundra halfling burrows).
- **UI Integration**: Extends the tile palette with a "Cities" tab, including template previews and sliders. Undo/redo hooks into the editor's history.
- **Edge Cases**: Handles non-square shapes (e.g., cities on peninsula sections) by clipping invalid sub-tiles to voids. Ensures performance by batching procedural calls.

This expansion provides a robust foundation for city templates, balancing ease-of-use with depth. If you'd like to add more races (e.g., orc warcamps), refine specific procedural algorithms, or dive into sample GDScript code, let me know!

## Review Needed
Proposed para-type: resource. Assigned based on content/frontmatter (confidence ~70%). Do not move until reviewed.