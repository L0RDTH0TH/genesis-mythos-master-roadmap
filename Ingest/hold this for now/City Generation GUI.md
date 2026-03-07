---
para-type: Resource
confidence: 70%
created: 2026-03-02
status: ingest
proposal_path: Ingest/Decisions/Decision-for-city-generation-gui--2026-03-04-0439.md
decision_candidate: true
decision_priority: high
---
## TL;DR
Based on the general Fractal GUI Framework for *Mythos Tabletop* and the City Generator subsystem, I've synthesized a specialized framework for the City GUI. This extends the core fractal wheel-based ...

---

Based on the general Fractal GUI Framework for *Mythos Tabletop* and the City Generator subsystem, I've synthesized a specialized framework for the City GUI. This extends the core fractal wheel-based radial menu to focus on city creation, placement, and customization within the in-game tile-based map editor. It integrates procedural generation, race-specific templates, and user-driven edits while maintaining narrative prompts, context-sensitivity, AI collaboration, and real-time previews. Built on Godot 4.x, this framework emphasizes modularity for seamless integration with world-building tools (e.g., biomes, landmarks).

The City GUI is activated from the main world-building menu (e.g., via a "Cities" quadrant in the root fractal wheel) and adapts the fractal structure for hierarchical city editing. It balances ease-of-use for DMs with depth for customization, ensuring cities blend with the hybrid world generation pipeline.

#### 1. **High-Level Architecture**
The City GUI inherits the layered system from the general framework:
- **Root Layer**: A 2D/3D viewport previewing the selected section(s) (e.g., a top-down map view with zoomable sub-tiles, showing procedural elements like buildings and roads).
- **Menu Layer**: Fractal wheel for city-specific navigation, with wedges adapting to race templates and procedural options.
- **Support Layers**: Overlays for AI suggestions (e.g., "Generate elf tree-city lore"), tooltips with lore snippets, metadata sliders, and global controls (e.g., generate/regenerate, undo/redo).
- **Data Flow**: Interactions update a city JSON object (e.g., city_data.json) nested within the world map's JSON for serialization, sharing, and multiplayer sync.

Key Principles:
- **Context-Awareness**: Menus adapt based on selected elements (e.g., section type: core vs. edge) or race template, using metadata dictionaries.
- **Animation-Driven UX**: Tween animations for wheel zooms, procedural generation fades (e.g., buildings "growing" in preview), and sub-tile swaps.
- **Narrative Flow**: Prompts guide steps (e.g., "Choose a race to found your city" → template options), with AI enhancing procedural outputs.
- **Scalability**: 4–6 wedges per level; deeper fractals for advanced customizations like NPC behaviors.
- **Integration with City Generator**: Directly calls procedural scripts (e.g., `generate_city()`) from wheel actions.

#### 2. **Core Components in Godot 4.x**
Extends the general framework's nodes and scripts, with city-specific additions. Base scene: `CityGUI.tscn` (extends `MainGUI.tscn`).

- **Viewport for Previews**:
  - Use `SubViewport` for real-time rendering of sections (e.g., TileMap for sub-tiles, with procedural overlays like MultiMeshInstance3D for props).
  - Script: Dynamically updates based on template (e.g., apply tree shaders for elf cities) and blends with biome metadata (e.g., elevate structures on mountains).
  - Features: Zoom/pan controls; highlight sub-tiles for editing; LOD for performance.

- **Fractal Wheel Control**:
  - Node: Extends `FractalWheel.gd` with city overrides (e.g., `CityFractalWheel.gd`).
  - Structure:
    - Root wheel: Quadrants like Template, Layout, Population, Customize.
    - Sub-wheels: Nested for details (e.g., Population → Structures, Roads, NPCs).
  - Visuals: Themed backgrounds (e.g., stone texture for dwarves); icons from race lore (e.g., tree icon for elves).
  - Animations: `AnimationPlayer` for procedural reveals (e.g., roads pathfinding in real-time); `Tween` for multi-section expansions.
  - Input: Right-click on map sections to open context wheel; hover for previews/tooltips.

- **Prompt and Tooltip System**:
  - Node: `RichTextLabel` for narrative prompts (e.g., "Build a thriving human town or a hidden elf enclave?").
  - Integration: Tooltips show impacts (e.g., "Higher density increases NPC count but risks overcrowding"); lore snippets from templates.

- **AI Assistant Integration**:
  - Node: `AIChatWindow` for city-specific queries (e.g., "Suggest quests for a dwarven forge district").
  - Functionality: Generates variants (e.g., 2–3 building layouts) based on template and metadata; integrates with procedural seeds.

- **Sliders, Palettes, and Tools**:
  - Nodes: `Slider` for metadata (e.g., density 0.0–1.0, wealth level); `OptionButton` for template selection.
  - Tools: Drag-and-drop sub-tile palette (e.g., swap house for shop); brush for road/path editing; scatter tool for props.
  - Procedural Buttons: "Generate" triggers noise-based placement; "Adapt to Biome" blends elements.

- **Global Controls**:
  - "Apply to Sections" for multi-section support; Randomize seed; Export/Share city JSON.
  - Performance: Toggle LOD/occlusion; unload distant NPC AI.

- **Accessibility and Performance Nodes**:
  - High-contrast modes for sliders; voice prompts for templates.
  - Optimizations: Batch procedural calls; use NavigationRegion2D for efficient pathfinding.

#### 3. **Fractal Wheel Implementation Guide**
Extends the base `fractal_wheel.gd` with city logic. Here's an updated GDScript snippet.

```gdscript
extends FractalWheel  # From general framework

# City-specific exports
@export var race_templates: Array[String] = ["Human", "Elf", "Dwarf", "Halfling"]
@export var section_cluster: Array[Node] = []  # Selected map sections

var city_context: Dictionary = {"template": "", "sections": [], "metadata": {"density": 0.5, "wealth": 0.5}}

func _on_element_selected(element_data: Dictionary, position: Vector2):
    city_context = element_data  # e.g., {"type": "section", "biome": "forest"}
    section_cluster = get_selected_sections()  # Custom func to grab adjacent sections
    super._on_element_selected(element_data, position)

func update_wheel():
    super.update_wheel()  # Clear and regenerate
    var wedge_data = generate_city_wedges(city_context, current_level)
    for i in wedge_data.size():
        var wedge = create_wedge(wedge_data[i], i)
        add_child(wedge)

func generate_city_wedges(ctx: Dictionary, level: int) -> Array:
    if level == 0:  # Root
        return [
            {"label": "Template", "icon": "res://icons/template.png", "action": "subwheel_template"},
            {"label": "Layout", "icon": "res://icons/layout.png", "action": "subwheel_layout"},
            {"label": "Population", "icon": "res://icons/population.png", "action": "subwheel_population"},
            {"label": "Customize", "icon": "res://icons/customize.png", "action": "subwheel_customize"},
            {"label": "Generate", "icon": "res://icons/generate.png", "action": "generate_city"}
        ]
    elif level == 1 and ctx["quadrant"] == "Template":
        var wedges = []
        for template in race_templates:
            wedges.append({"label": template, "action": "select_template_" + template.to_lower()})
        return wedges
    elif level == 1 and ctx["quadrant"] == "Layout":
        return [
            {"label": "Multi-Section", "action": "toggle_multi_section"},
            {"label": "Blend Biomes", "action": "blend_with_biome"},
            {"label": "Sub-Tile Swap", "action": "open_subtile_palette"}
        ]
    elif level == 1 and ctx["quadrant"] == "Population":
        return [
            {"label": "Structures", "action": "proc_structures"},
            {"label": "Roads", "action": "proc_roads"},
            {"label": "Props", "action": "proc_props"},
            {"label": "NPCs", "action": "proc_npcs"}
        ]
    elif level == 1 and ctx["quadrant"] == "Customize":
        return [
            {"label": "Metadata Sliders", "action": "open_sliders"},
            {"label": "Unique Landmarks", "action": "place_landmark"},
            {"label": "AI Suggestions", "action": "ai_generate"}
        ]
    return []  # Fallback

func _on_wedge_pressed(action: String):
    if action.begins_with("select_template_"):
        city_context["template"] = action.substr(16).capitalize()
        apply_template(city_context["template"])
        animate_close()
    elif action == "generate_city":
        generate_city(city_context["template"], section_cluster)
    elif action.begins_with("proc_"):
        run_procedural(action.substr(5), city_context)
    # ... Handle other actions like open_sliders()
    super._on_wedge_pressed(action)

# City Generator integrations
func apply_template(template_id: String):
    # Load race-specific layout (e.g., 40% residential for Human)
    update_preview()  # Refresh viewport

func generate_city(template_id: String, sections: Array[Node]):
    # Call procedural script from City Generator
    # e.g., Use Perlin noise for density, A* for roads
    for section in sections:
        section.get_node("TileMap").apply_city_layout(template_id, city_context["metadata"])
    save_to_json()

func run_procedural(type: String, ctx: Dictionary):
    # e.g., If type == "roads", use NavigationRegion2D with A*
    update_preview()

# ... Additional funcs like blend_with_biome(sub_tile: TileData)
```

#### 4. **Usage Guidelines**
- **Workflow Example**:
  1. Select map section(s) → Open wheel with prompt ("Found a new settlement?").
  2. Choose Template quadrant → Zoom to races → Select "Elf" → Apply tree-city layout.
  3. Population quadrant → Generate structures/roads → Preview updates procedurally.
  4. Customize → Adjust sliders (e.g., density) → AI suggests NPC quests.
  5. Generate → Serialize and blend with biomes.

- **Customization**:
  - Add new races (e.g., orc templates) via mods; extend wedges for landmark integration.
  - Edge Cases: Handle incompatible biomes (e.g., warn for dwarf city on swamp); clip non-square sections.

- **Testing and Optimization**:
  - Ensure smooth procedural generation (<1s per section); test multiplayer city sharing.
  - Accessibility: Sliders with keyboard nav; color-coded templates for visual distinction.

This City GUI Framework provides an intuitive, extensible interface for the City Generator. It can be further refined with details from related docs (e.g., landmark integration) or expanded for more races. Let me know if you'd like GDScript samples, UI mockups, or iterations!

## Review Needed
Proposed para-type: resource. Assigned based on content/frontmatter (confidence ~70%). Do not move until reviewed.