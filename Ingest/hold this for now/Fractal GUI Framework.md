---
para-type: Archive
confidence: 70%
created: 2026-03-02
status: ingest
decision_candidate: true
guidance_conf_boost: 15
tags: guidance-aware
decision_priority: medium
proposal_path: Ingest/Decisions/Decision-for-fractal-gui-framework--2026-03-04-0439.md
---
> [!warning] Decision needed (low confidence)
> This note needs guidance. Add `user_guidance: | ...` and `approved: true` to frontmatter, then run EAT-QUEUE.
>
> [!tip] Suggested user_guidance (copy-paste into frontmatter)
> user_guidance: |
>   Classify as Archive. Prefer path: 4-Archives/Genesis/Fractal GUI Framework.md. Split if >500 words or multiple topics.

### General GUI Framework for Mythos Tabletop

Based on the provided documents ("World building gui.md", "Character Customization GUI.md", and "World Overview GUI.md"), I've synthesized a general framework for the GUI system in *Mythos Tabletop*. This framework emphasizes a **fractal wheel-based radial menu** as the core navigation element, integrated with Godot 4.x for performance, narrative-driven prompts, context-sensitivity, AI collaboration, and real-time previews. It draws from the recurring patterns across world building, character customization, and session preparation GUIs:

- **Fractal Structure**: Hierarchical, zoomable radial menus that expand like fractals to avoid overwhelming the user.
- **Narrative Integration**: Prompts and questions guide users (e.g., DMs or players), tying choices to lore and mechanics.
- **Modularity**: Reusable components for different contexts (e.g., world editing, character creation, session prep).
- **Technical Foundation**: Built on Godot's CanvasLayer, Control nodes, Tween/AnimationPlayer for smooth interactions, and JSON serialization for data persistence.
- **Enhancements**: AI-assisted suggestions, accessibility features, and performance optimizations like LOD (Level of Detail).

This framework is extensible—e.g., it could incorporate elements from the inaccessible documents (like landmark placement or city generation) by adapting the wheel to specific tools (e.g., procedural generation sliders).

#### 1. **High-Level Architecture**
The GUI is structured as a layered system:
- **Root Layer**: A central 3D/2D viewport (e.g., globe for world building, character model for customization) surrounded by the fractal wheel.
- **Menu Layer**: Fractal wheel for navigation, with context-sensitive wedges (segments).
- **Support Layers**: Overlays for AI chat, tooltips, previews, and global controls (e.g., back button, undo/redo).
- **Data Flow**: All interactions update a central JSON object (e.g., world_data.json or character_profile.json) for serialization and multiplayer sync.

Key Principles:
- **Context-Awareness**: Menus adapt based on selected elements (e.g., biome vs. NPC) using a Dictionary of metadata.
- **Animation-Driven UX**: Use Tween for zooms and fades to make navigation feel immersive and "fractal-like."
- **Narrative Flow**: Sequence steps with prompts (e.g., "Shape the land" → sub-options), optionally guided by AI.
- **Scalability**: Limit wedges to 4–8 per level to prevent clutter; deeper levels for complexity.

#### 2. **Core Components in Godot 4.x**
Implement the framework using these Godot nodes and scripts. Assume a base scene (e.g., `MainGUI.tscn`) with a CanvasLayer as the parent.

- **Viewport for Previews**:
  - Use `SubViewport` or `Viewport` for real-time 3D previews (e.g., character model or globe mesh).
  - Script: Update visuals dynamically (e.g., apply shaders for archetype colors or terrain textures).
  - Example from Docs: In character customization, the viewport rotates for inspection and updates with class-specific effects (e.g., glowing aura).

- **Fractal Wheel Control**:
  - Node: Custom `Control` node (e.g., `FractalWheel.gd`) with child `TextureButton`s for wedges.
  - Structure:
    - Root wheel: 4–6 quadrants (e.g., Terrain, Rulings, Factions, Narrative).
    - Sub-wheels: Nested Controls that appear on zoom, inheriting aesthetics.
  - Visuals: Circular layout with `DrawCircle` or pre-made textures (e.g., parchment background, runic icons). Use `GradientTexture2D` for color themes (e.g., Green for Terrain).
  - Animations: `AnimationPlayer` for open/close (scale from 0.5 to 1.0 over 0.3s); `Tween` for sub-wheel transitions (fade parent to 50% opacity).
  - Input: Right-click to open at cursor; hover to highlight; left-click to expand/execute.

- **Prompt and Tooltip System**:
  - Node: `Label` or `RichTextLabel` for narrative prompts (e.g., "What story do you want to tell?").
  - Integration: Tooltips as popups with lore/mechanic impacts; AI hints as edge labels.

- **AI Assistant Integration**:
  - Node: Dedicated `Control` (e.g., `AIChatWindow`) linked to an AI agent script.
  - Functionality: Parse natural language inputs (e.g., "Generate backstory for Hero Paladin") and suggest options. Outputs update JSON or wheel suggestions.
  - Example from Docs: In backstory crafting, AI generates 2–3 options based on world JSON.

- **Sliders, Palettes, and Tools**:
  - Nodes: `Slider`, `OptionButton`, `ColorPicker` for metadata (e.g., elevation 0.0–1.0).
  - Tools: Brush/Fill for painting (e.g., biomes); Drag-and-Drop for placement.

- **Global Controls**:
  - Central "Back" button, Undo/Redo stack, Randomize button.
  - Multiplayer Sync: Use Godot's High-Level Multiplayer API to send updates (e.g., character approval to DM).

- **Accessibility and Performance Nodes**:
  - Theme overrides for color contrasts and font scaling.
  - LODGroup for 3D models; GPU-accelerated shaders.
  - Screen reader labels on wedges; rebindable keys (e.g., arrows for navigation).

#### 3. **Fractal Wheel Implementation Guide**
The fractal wheel is the framework's centerpiece. Here's a step-by-step to build it in GDScript.

1. **Base Script (`fractal_wheel.gd`)**:
   ```gdscript:disable-run
   extends Control

   # Exported vars for customization
   @export var wedge_count: int = 4
   @export var radius: float = 200.0
   @export var colors: Array[Color] = [Color.GREEN, Color.BLUE, Color.RED, Color.PURPLE]

   var context: Dictionary = {}  # e.g., {"type": "biome", "id": "forest"}
   var current_level: int = 0
   var sub_wheels: Array[Control] = []

   func _ready():
       visible = false
       # Connect to input events (e.g., right-click from parent scene)
       get_parent().connect("element_selected", self, "_on_element_selected")

   func _on_element_selected(element_data: Dictionary, position: Vector2):
       context = element_data
       global_position = position
       update_wheel()
       animate_open()
       visible = true

   func update_wheel():
       # Clear children
       for child in get_children():
           child.queue_free()
       
       # Generate wedges based on context and level
       var wedge_data = generate_wedges(context, current_level)
       for i in wedge_data.size():
           var wedge = create_wedge(wedge_data[i], i)
           add_child(wedge)

   func generate_wedges(ctx: Dictionary, level: int) -> Array:
       # Context-sensitive logic (expand based on docs)
       if level == 0:  # Root
           return [
               {"label": "Terrain", "icon": "res://icons/terrain.png", "action": "subwheel_terrain"},
               {"label": "Rulings", "icon": "res://icons/rulings.png", "action": "subwheel_rulings"},
               # ... Add more from docs
           ]
       elif level == 1 and ctx["quadrant"] == "Terrain":
           return [
               {"label": "Biomes", "action": "edit_biomes"},
               # ... Sub-options like Landmarks, Voids
           ]
       return []  # Fallback

   func create_wedge(data: Dictionary, index: int) -> TextureButton:
       var wedge = TextureButton.new()
       wedge.texture_normal = load(data["icon"])
       wedge.modulate = colors[index % colors.size()]  # Thematic colors
       # Position radially: Use polar coordinates
       var angle = (2 * PI / wedge_count) * index
       wedge.position = Vector2(cos(angle), sin(angle)) * radius
       wedge.connect("pressed", self, "_on_wedge_pressed", [data["action"]])
       # Add label/tooltip
       var label = Label.new()
       label.text = data["label"]
       wedge.add_child(label)
       return wedge

   func _on_wedge_pressed(action: String):
       if action.begins_with("subwheel_"):
           current_level += 1
           context["quadrant"] = action.substr(9)  # e.g., "terrain"
           update_wheel()  # Zoom to sub-wheel
           animate_zoom()
       else:
           execute_action(action)  # e.g., open slider panel

   func execute_action(action: String):
       # Trigger specific logic, e.g., open sliders or call AI
       if action == "edit_biomes":
           # Show palette, update preview
           get_parent().update_preview(context)
       # Close wheel if terminal action
       animate_close()

   # Animation helpers
   func animate_open():
       var tween = Tween.new()
       add_child(tween)
       tween.interpolate_property(self, "scale", Vector2(0.5, 0.5), Vector2(1, 1), 0.3)
       tween.start()

   func animate_zoom():
       # Fade parent, show sub-wheel (implement as needed)
       pass

   func animate_close():
       visible = false
       current_level = 0
   ```

2. **Extending for Specific GUIs**:
   - **World Building**: Override `generate_wedges` for quadrants like Terrain (biomes, landmarks).
   - **Character Customization**: Tie to archetype groups (e.g., Identity and Self quadrant zooms to classes).
   - **Session Prep**: Make wedges context-sensitive to elements (e.g., Quest Creation for NPCs).

3. **Integration with Other Systems**:
   - **AI**: Call `ai_assistant.parse_input(prompt)` in `execute_action` for suggestions.
   - **Previews**: Emit signals to update the viewport (e.g., apply Red aura for Hero archetype).
   - **Data Persistence**: On action, update `world_data: Dictionary` and save to JSON.

#### 4. **Usage Guidelines**
- **Workflow Example** (From Character Doc):
  1. Connect to world (load JSON rules).
  2. Open wheel with prompt ("What story?").
  3. Select quadrant → Zoom to archetypes → Choose class → Update preview.
  4. AI generates backstory → Submit for approval.

- **Customization**:
  - Add mods via marketplace (e.g., new wedges for city generation).
  - Handle Edge Cases: Invalid contexts show minimal wheel; multiplayer conflicts flag for DM review.

- **Testing and Optimization**:
  - Ensure 60 FPS: Batch updates, use culling.
  - Accessibility: Test with colorblind modes; add audio cues.

This framework provides a cohesive, reusable base for *Mythos Tabletop*'s GUIs. If you provide more details from the blocked docs (e.g., via summaries or URLs I can browse), I can refine it further—e.g., adding procedural city tools. Let me know how you'd like to proceed!

## Review Needed
Proposed para-type: archive. Assigned based on content/frontmatter (confidence ~70%). Do not move until reviewed.