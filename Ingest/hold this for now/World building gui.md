---
proposal_path: Ingest/Decisions/Decision-for-world-building-gui--2026-03-04-0440.md
---
## TL;DR
# Fractal Wheel World Building Menus

---

# Fractal Wheel World Building Menus

The **Fractal Wheel World Building Menus** in *Mythos Tabletop* integrate with the globe-centered GUI, providing a narrative-driven, layered interface for DMs to customize worlds. Inspired by the Character Customization system's fractal color wheel, this UI surrounds the central 3D globe mesh, acting as a dynamic "window" that zooms seamlessly into selected sections (500 m × 500 m) for detailed editing. The wheel starts with four initial quadrants, each representing a core aspect of world-building: **Terrain** (physical landscapes and features), **Rulings** (mechanical rules and systems), **Factions** (social and political entities), and **Narrative** (storytelling elements and lore—suggested as the fourth quadrant to complete the set, focusing on quests, events, and backstory integration).

The wheel uses Godot 4.x’s CanvasLayer for rendering, with Tween animations for zooming into sub-options. Colors are assigned thematically (e.g., Green for Terrain, Blue for Rulings, Red for Factions, Purple for Narrative) to aid navigation. Prompts guide the DM (e.g., "Shape the land," "Define the laws"), and selections update the globe in real-time with procedural previews. Submenus appear as further zooms, revealing radial buttons for options, sliders for metadata, and palettes for placement. The system ties into the spherical projection, ensuring edits (e.g., biome painting) conform to the globe's curvature via Godot’s projection mapping.

Below is the mapped structure of the fractal wheel, starting with the initial quadrants and breaking down into options and submenus where necessary. Each quadrant zooms to reveal 4–6 primary options, with deeper submenus for complex features (e.g., sliders or palettes). This allows hierarchical navigation while keeping the UI intuitive and non-overwhelming.

## Initial Fractal Wheel: Four Quadrants
- **Activation**: After selecting or customizing land placement defaults (e.g., "Continental Masses," "Archipelagos," "Pangaea-like Supercontinent," or custom via manual section placement), the DM zooms into a globe section using pinch-zoom or mouse wheel. The fractal wheel appears surrounding the zoomed view, divided into four colored quadrants. Clicking a quadrant triggers a zoom-in animation, revealing sub-options in a radial layout.
- **Global Controls**: A central "Back" button resets to the full wheel; tooltips provide lore/mechanic impacts (e.g., "Factions influence NPC behaviors and quests").
- **Real-Time Updates**: Selections apply to the current zoomed section (or globally if specified), with seamless globe refreshes using Godot’s procedural noise shaders.

### 1. Terrain Quadrant (Green: Physical World Shaping)
   - **Prompt**: "Shape the land. What biomes and features define this realm?"
   - **Overview**: Focuses on geographical and environmental elements, integrating with sub-tiles (50 m × 50 m) for fine-grained placement on the globe's surface.
   - **Primary Options (Radial Buttons on Zoom)**:
     - **Biomes**: Paint and customize ecosystem types.
     - **Landmarks**: Add interactive natural or man-made features.
     - **Voids**: Define unplaced or edge areas on the globe (e.g., oceans wrapping around poles).
     - **Elevation & Textures**: Adjust terrain height and surfaces globally or locally.
     - **Procedural Seeds**: Tweak noise parameters for organic generation.
   - **Submenus**:
     - **Biomes**:
       - Variants: Forests (pine, oak, jungle), Deserts (dunes, oasis), Mountains, Plains, Swamps, Tundra, Coastal, Volcanic.
       - Tools: Brush (single sub-tile), Fill (region), Variants Palette (searchable with previews).
       - Metadata Sliders: Elevation (0.0–1.0), Vegetation Density (0.0–1.0), Water Presence (0.0–1.0).
       - Submenu: Transition Rules (auto-blend edges; toggle for manual overrides).
     - **Landmarks**:
       - Categories: Natural Formations (ancient tree, river, cave), Ruins & Structures (ruin, dungeon entrance, monolith), Mystical & Anomalous (portal, floating island, meteor crater), Environmental Hazards (volcanic vent, swamp bog, cliff edge).
       - Tools: Drag-and-Drop (5 m precision), Rotation (45° increments), Scaling (±20%).
       - Metadata Sliders: Age (0.0–1.0 for weathering), Danger Level (low/high for spawns).
       - Submenu: Linking (connect across sections, e.g., river networks wrapping globe longitudes).
     - **Voids**:
       - Types: Ocean (waves, reefs), Lava (flows, ash), Void Space (fog, stars).
       - Metadata Sliders: Intensity (e.g., wave height 0.0–1.0), Particle Effects (density).
       - Submenu: Transitions (beaches for ocean, scorched edges for lava; global equator/pole overrides).
     - **Elevation & Textures**:
       - Tools: Raise/Lower Brush, Texture Palette (sand, grass, rock).
       - Submenu: LOD Settings (high-detail near zoom, low at distance).
     - **Procedural Seeds**:
       - Sliders: Noise Frequency, Amplitude, Seed Value (randomize button).
       - Submenu: Preview Modes (wireframe, textured, full 3D orbit).

### 2. Rulings Quadrant (Blue: Mechanical Rules and Systems)
   - **Prompt**: "Define the laws. How will mechanics govern this world?"
   - **Overview**: Customizes game rules, integrating with D&D 5e base and AI-parsed homebrew for combat, progression, and world interactions. Applies globally or to specific globe regions (e.g., magic-suppressed zones).
   - **Primary Options (Radial Buttons on Zoom)**:
     - **Combat Rules**: Modify turn-based systems.
     - **Progression System**: Control leveling and abilities.
     - **Homebrew Mechanics**: Add custom rules via natural language.
     - **Environmental Interactions**: Rules for terrain effects (e.g., difficult terrain in swamps).
     - **Restrictions**: Set limits (e.g., banned classes in certain factions).
   - **Submenus**:
     - **Combat Rules**:
       - Options: Initiative (dynamic rolls, group), Actions (attacks, spells), Status Effects (stunned, poisoned).
       - Sliders: Dice Modifiers (e.g., +1 attack in mountains), Range Costs.
       - Submenu: AI Parser (text input for homebrew, e.g., "Add fatigue in deserts"; prompts for clarification).
     - **Progression System**:
       - Options: Milestone Leveling (DM-triggered), Class Abilities (tie to archetypes).
       - Submenu: Point-Buy Limits (e.g., 27 points; region-specific bonuses, like +1 Strength in volcanic areas).
     - **Homebrew Mechanics**:
       - Tools: Natural Language Input (AI converts to scripts), Save/Share Rule Sets.
       - Submenu: Test Mode (simulate combats on globe preview).
     - **Environmental Interactions**:
       - Options: Cover (from landmarks), Opportunity Attacks (near cliffs).
       - Submenu: Biome Ties (link to Terrain, e.g., auto-apply fog concealment in swamps).
     - **Restrictions**:
       - Options: Class/Race Bans, Magic Levels (high/low in regions).
       - Submenu: Global vs. Local (apply to whole globe or zoomed section).

### 3. Factions Quadrant (Red: Social and Political Entities)
   - **Prompt**: "Forge alliances and rivalries. Who claims dominion over these lands?"
   - **Overview**: Builds societal elements, including races, NPCs, and cities, with procedural population tied to globe sections. Factions can span hemispheres or be localized.
   - **Primary Options (Radial Buttons on Zoom)**:
     - **Races & Cities**: Template-based settlements.
     - **NPCs**: Generate and customize individuals/groups.
     - **Alliances & Conflicts**: Define relationships.
     - **Quests & Hooks**: Tie factions to story elements.
     - **Economy & Resources**: Set trade and spawns.
   - **Submenus**:
     - **Races & Cities**:
       - Templates: Human (medieval towns), Elf (tree-cities), Dwarf (stone fortresses), Halfling (burrow-villages).
       - Tools: Multi-Section Placement, Sub-Tile Swapping (e.g., tavern to temple).
       - Metadata Sliders: Population Density (0.0–1.0), Wealth Level.
       - Submenu: Blending (adapt to biomes, e.g., elevated dwarf cities on globe poles).
     - **NPCs**:
       - Options: Guards, Merchants, Quest-Givers; Behaviors (patrols, routines).
       - Submenu: AI Control (dynamic responses; tie to rulings for stats).
     - **Alliances & Conflicts**:
       - Tools: Faction Map Overlay (visualize on globe), Relationship Sliders (ally/neutral/hostile).
       - Submenu: Events (e.g., wars triggering procedural battles).
     - **Quests & Hooks**:
       - Options: Fetch, Escort, Diplomacy; Auto-Generate from Factions.
       - Submenu: Integration (link to Narrative quadrant).
     - **Economy & Resources**:
       - Options: Resource Nodes (ore in mountains), Trade Routes (globe-spanning paths).
       - Submenu: Procedural Spawns (influenced by terrain seeds).

### 4. Narrative Quadrant (Purple: Storytelling Elements and Lore)
   - **Prompt**: "Weave the tales. What histories and destinies await in this world?"
   - **Overview**: Focuses on lore, events, and immersive storytelling, seeding quests and backstories that interact with the globe's features (e.g., ancient ruins with tied legends).
   - **Primary Options (Radial Buttons on Zoom)**:
     - **Backstory & Lore**: Generate world history.
     - **Quests & Events**: Create dynamic storylines.
     - **Artifacts & Secrets**: Place hidden elements.
     - **Weather & Cycles**: Add time-based narratives (e.g., seasonal events).
     - **Mod Integration**: Incorporate community content for lore.
   - **Submenus**:
     - **Backstory & Lore**:
       - Tools: AI Generator (input prompts like "Ancient war between elves and dwarves"; outputs 100–200 word summaries).
       - Submenu: Globe Ties (assign lore to sections, e.g., "Cursed equator").
     - **Quests & Events**:
       - Options: Main Quests, Side Quests, Random Encounters.
       - Submenu: Triggers (link to landmarks, e.g., portal activation).
     - **Artifacts & Secrets**:
       - Options: Magical Items, Hidden Dungeons.
       - Tools: Placement Palette (drag to sub-tiles), Rarity Sliders.
       - Submenu: Reveals (DM-triggered or player-discovered).
     - **Weather & Cycles**:
       - Options: Day/Night, Seasons, Storms.
       - Sliders: Frequency, Intensity; Globe-Specific (e.g., polar auroras).
       - Submenu: Narrative Impacts (e.g., storms tie to faction conflicts).
     - **Mod Integration**:
       - Tools: Import Marketplace Mods (custom lore packs).
       - Submenu: Compatibility Check (ensure fit with rulings).

## Technical Implementation Notes
- **Fractal Zoom**: Each level uses Godot’s AnimationPlayer for radial expansions; submenus load dynamically to optimize performance.
- **Globe Integration**: Edits project onto the spherical mesh using UV mapping; zoom transitions use Camera3D interpolation for seamlessness.
- **Accessibility**: Color contrasts, screen reader labels for options; keyboard navigation for quadrants (e.g., arrow keys).
- **Edge Cases**: Handles globe wrapping (e.g., trans-oceanic factions); undo/redo spans fractal levels.

This mapping provides a balanced, expandable structure. If you'd like to adjust the fourth quadrant (e.g., to "Mechanics" or "Hazards"), add more submenus, or integrate specific GDScript examples, let me know!

## Review Needed
Proposed para-type: project. Assigned based on content/frontmatter (confidence ~70%). Do not move until reviewed.