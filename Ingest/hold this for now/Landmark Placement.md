---
confidence: 70%
decision_candidate: true
tags: guidance-aware
para-type: Area
created: 2026-03-02
status: ingest
guidance_conf_boost: 15
decision_priority: medium
proposal_path: Ingest/Decisions/Decision-for-landmark-placement--2026-03-04-0438.md
---
> [!warning] Decision needed (low confidence)
> This note needs guidance. Add `user_guidance: | ...` and `approved: true` to frontmatter, then run EAT-QUEUE.
>
> [!tip] Suggested user_guidance (copy-paste into frontmatter)
user_guidance: |
  Classify as Area. Prefer path: 2-Areas/Landmark Placement.md. Split if >500 words or multiple topics.

 The Landmark Placement system enhances the In-Game Tile-Based Map Editor by allowing DMs to add distinctive, interactive features to the world map. Landmarks serve as focal points for storytelling, exploration, and gameplay, integrating with the section and sub-tile framework for precise positioning. They can occupy one or more sub-tiles within a section (e.g., a small cave on a single 50 m × 50 m sub-tile or a sprawling ruin across 4–6 sub-tiles) and are designed to blend procedurally with surrounding biomes and terrain.

Landmarks are selected from a categorized palette and placed on the 10x10 sub-tile grid of a section, with support for finer adjustments at 5 m increments (e.g., offsetting a landmark within a sub-tile for exact placement). Each landmark type includes base models, procedural variations, and customizable properties to fit the DM's narrative. Upon placement, landmarks seed additional procedural generation, such as environmental effects (e.g., fog around ruins) or NPC spawns (e.g., guardians near ancient trees). They can also trigger events, like quests or encounters, and are optimized for LOD to maintain performance in large maps.

#### Key Features
- **Palette Integration**: Landmarks appear in a dedicated tab of the tile palette, searchable by category, with previews showing 3D renders and lore descriptions.
- **Placement Mechanics**: Drag-and-drop onto sub-tiles; multi-sub-tile landmarks auto-snap to available space. Supports rotation (in 45° increments), scaling (±20% for size variation), and layering (e.g., a river under a bridge landmark).
- **Biome Compatibility**: Landmarks suggest restricting placement based on sub-tile biomes (e.g., volcanic vents only on volcanic sub-tiles), with automatic adaptations (e.g., snowy variants in tundra).
- **Procedural Enhancements**:
  - **Terrain Integration**: Uses Godot's noise functions to modify local elevation or textures (e.g., craters around meteor impacts).
  - **Asset Spawning**: Scatter related props (e.g., debris near ruins) via MultiMesh, influenced by metadata sliders.
  - **Interactive Elements**: Optional scripting hooks for events (e.g., puzzle activation) or audio/visual cues (e.g., glowing runes).
- **Customization Tools**:
  - **Property Editor**: Post-placement panel with sliders and dropdowns (e.g., age: 0.0–1.0 for weathering effects, danger level: low/medium/high for enemy spawns).
  - **Variant Selection**: Choose from sub-types (e.g., dungeon: abandoned mine vs. haunted crypt).
  - **Linking**: Connect landmarks across sections (e.g., a river flowing through multiple sections) for cohesive features like trade routes.
- **Performance Optimizations**: LOD levels for landmark models (detailed up close, simplified at distance); culling for off-screen or void-adjacent landmarks.
- **Serialization**: Landmark data (type, position, properties) is saved in the map's JSON, including procedural seeds for reproducibility.

#### Landmark Categories
Landmarks are grouped into categories for easy navigation, each with 5–10 types. Procedural rules ensure diversity, such as randomizing orientations or adding wear based on biome metadata. Below are expanded details for key categories, with examples.

1. **Natural Formations**
   - **Aesthetic**: Organic features shaped by the environment, emphasizing exploration and resource gathering.
   - **Examples**:
     - **Ancient Tree**: A massive, gnarled tree (spans 1–3 sub-tiles). Variants: oak sentinel, glowing elderwood, withered curse-tree. Properties: height (10–50 m), branch density (0.0–1.0), magical aura (none/weak/strong—adds particle effects).
     - **River**: A flowing water body (linear, 1–2 sub-tiles wide, extendable across sections). Variants: calm stream, rushing rapids, polluted sludge. Properties: width (10–50 m), flow speed (slow/medium/fast), fordability (yes/no—adds crossing points).
     - **Cave Entrance**: Opening to underground areas (1 sub-tile). Variants: natural grotto, mined shaft, crystal cavern. Properties: depth hint (shallow/deep—seeds procedural interiors), lighting (dark/torchlit/bioluminescent).
   - **Procedural Details**: Rivers use Godot's water shaders with noise-driven currents; trees spawn procedural foliage and roots that interact with terrain (e.g., uplifting soil in plains).
   - **Customization Examples**: Link rivers to form networks; add hidden compartments to caves for loot.

2. **Ruins and Structures**
   - **Aesthetic**: Man-made remnants from ancient civilizations, ideal for lore and puzzles.
   - **Examples**:
     - **Ruin**: Overgrown remnants (2–4 sub-tiles). Variants: temple ruins, fortress walls, buried pyramid. Properties: decay level (0.0–1.0—adds cracks/vines), trap density (low/high—procedural pitfalls).
     - **Dungeon Entrance**: Portal to instanced areas (1–2 sub-tiles). Variants: crypt door, fortress gate, labyrinth arch. Properties: type (undead/beast/mechanical—influences interior generation), lock mechanism (key/puzzle/open).
     - **Monolith**: Standing stone or obelisk (1 sub-tile). Variants: rune-carved, weathered pillar, sacrificial altar. Properties: inscription (custom text), energy field (none/repel/attract— affects nearby NPCs).
   - **Procedural Details**: Ruins use scatter for debris and ivy; dungeons seed procedural layouts (e.g., using Godot's Dungeon Generator addon) based on type.
   - **Customization Examples**: Scale ruins for larger complexes; embed quests like "decipher monolith runes."

3. **Mystical and Anomalous**
   - **Aesthetic**: Supernatural or otherworldly elements, fostering mystery and magic.
   - **Examples**:
     - **Portal**: Shimmering gateway (1 sub-tile). Variants: stable rift, unstable vortex, elemental gate. Properties: destination (linked landmark/void/random), activation (always/timed/triggered).
     - **Floating Island**: Suspended landmass (2–3 sub-tiles, elevated). Variants: verdant isle, crystalline shard, shadowed rock. Properties: height (20–100 m), stability (stable/wobbling—adds sway animation).
     - **Meteor Crater**: Impact site (1–2 sub-tiles). Variants: fresh crater, overgrown pit, radioactive glow. Properties: size (small/large), resource yield (ore/gems/none—spawns collectibles).
   - **Procedural Details**: Portals use particle shaders for effects; floating islands generate underside meshes and drop shadows on terrain below.
   - **Customization Examples**: Chain portals for teleport networks; add hazards like radiation to craters.

4. **Environmental Hazards**
   - **Aesthetic**: Dangerous features that add risk and strategy to traversal.
   - **Examples**:
     - **Volcanic Vent**: Lava-spewing fissure (1 sub-tile). Variants: dormant geyser, active flow, ash vent. Properties: eruption frequency (rare/frequent), heat radius (10–50 m—affects nearby vegetation).
     - **Swamp Bog**: Quicksand or mire (1–2 sub-tiles). Variants: toxic pool, foggy marsh, insect-infested. Properties: sink speed (slow/fast), visibility (clear/hidden—adds fog particles).
     - **Cliff Edge**: Sheer drop (linear, along sub-tile edges). Variants: rocky precipice, iced ledge, vine-draped. Properties: height (20–200 m), climbability (yes/no—adds handholds).
   - **Procedural Details**: Vents use dynamic lava simulations; bogs spawn procedural bubbles and sounds.
   - **Customization Examples**: Extend cliffs to form canyons across sections; integrate with voids (e.g., cliff to ocean drop).

#### Implementation Notes in Godot 4.x
- **Core Nodes**: Each landmark is a Scene instance (e.g., PackedScene for reusability) parented to the section's TileMap, with child nodes for procedural elements (e.g., GPUParticles3D for effects).
- **Procedural Scripts**: GDScript functions for placement and generation:
  - `place_landmark(type: String, sub_tiles: Array[Vector2i], properties: Dictionary)`: Instantiates the landmark, applies properties, and runs noise-based enhancements.
  - `integrate_with_terrain(landmark: Node)`: Adjusts position/effects based on sub-tile elevation and biome.
- **UI Integration**: Extends the sub-tile editor with a landmark overlay mode; property editor uses Godot's Inspector for intuitive tweaks. Undo/redo supports landmark actions.
- **Edge Cases**: Handles overlaps (e.g., priority layering for river under ruin); optimizes for non-contiguous maps by culling landmarks near voids.

This landmark system adds depth and interactivity to the world, encouraging player engagement. If you'd like to expand on specific categories, add more types (e.g., underwater landmarks for ocean voids), or integrate with city templates (e.g., urban landmarks like fountains), just say the word!

## Review Needed
Proposed para-type: area. Assigned based on content/frontmatter (confidence ~70%). Do not move until reviewed.