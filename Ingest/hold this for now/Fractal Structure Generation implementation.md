---
para-type: Project
confidence: 70%
created: 2026-03-02
status: ingest
decision_candidate: true
guidance_conf_boost: 15
tags: guidance-aware
proposal_path: Ingest/Decisions/Decision-for-fractal-structure-generation--2026-03-04-0439.md
---
> [!warning] Decision needed (low confidence)
> This note needs guidance. Add `user_guidance: | ...` and `approved: true` to frontmatter, then run EAT-QUEUE.
>
> [!tip] Suggested user_guidance (copy-paste into frontmatter)
> user_guidance: |
>   Classify as Project. Prefer path: 1-Projects/Genesis-Mythos/Fractal Structure Generation implementation.md. Split if >500 words or multiple topics.

### Best Approach to Generating Fractal Structures for Mythos Tabletop's GUI

Based on the provided framework for Mythos Tabletop's GUI, the "fractals" refer to the hierarchical, zoomable radial menu system (the "fractal wheel") that forms the core navigation element. This structure mimics fractal patterns by allowing menus to expand recursively into sub-levels, avoiding UI clutter while providing deep, context-sensitive options for features like world building, character customization, and session preparation. The goal is to generate these dynamically in Godot 4.x, ensuring modularity, performance, and integration with narrative prompts, AI suggestions, and real-time previews.

From analyzing the framework and cross-referencing best practices (e.g., Godot tutorials on radial menus, forum discussions on hierarchical UIs, and recipes for popup menus), the optimal method is a **procedural, script-driven generation using Godot's Control nodes and GDScript**. This approach leverages Godot's built-in UI tools for efficiency, avoids external dependencies, and supports the fractal-like expansion. Here's a breakdown of why this is the best way and how to implement it:

#### Why This Method?
- **Efficiency and Native Integration**: Godot's Control nodes (e.g., Container, TextureButton) are lightweight and GPU-accelerated, ideal for real-time UI. Procedural generation via script allows dynamic updates based on context (e.g., biome editing vs. NPC placement), aligning with the framework's emphasis on context-awareness.
- **Scalability for Fractals**: Hierarchical structures are handled via recursion or level-tracking, enabling infinite-depth menus without predefined scenes. This matches fractal principles: self-similar expansion.
- **Performance**: Limits wedges to 4–8 per level (as recommended in the framework) prevents overload. Use Tween/AnimationPlayer for smooth zooms, ensuring 60 FPS even on complex worlds.
- **Alternatives Considered**:
  - **Shader-Based Visuals**: Great for aesthetic fractals (e.g., Mandelbrot patterns on backgrounds), but overkill for structural menus. Reserve shaders for previews (e.g., terrain textures).
  - **Pre-Built Plugins**: Godot Asset Library has radial menu add-ons, but custom scripting is better for Mythos' narrative/AI integration.
  - **Tree Nodes**: Good for linear hierarchies, but radial positioning requires custom math (polar coordinates), making a scripted Control superior.
- **Drawbacks of Other Methods**: Static scenes lack dynamism; full procedural fractals (e.g., via math libraries like sympy) would be computationally heavy for UI.

This method builds directly on the provided `fractal_wheel.gd` script, enhancing it for better hierarchy, modularity, and error-handling.

#### Step-by-Step Implementation Guide
1. **Setup the Base Scene**:
   - Create a new scene (`FractalWheel.tscn`) with a root `Control` node.
   - Attach a script (`fractal_wheel.gd`) to it.
   - Add support nodes: A central `SubViewport` for previews, a `Panel` for AI chat overlays, and global buttons (e.g., Undo/Redo).

2. **Data Structure for Menu Hierarchy**:
   - Use a nested Dictionary to define the fractal structure. This allows easy loading from JSON (e.g., `world_data.json`) and AI-generated suggestions.
     ```gdscript
     var menu_data: Dictionary = {
         "root": [
             {"label": "Terrain", "icon": "res://icons/terrain.png", "sub": "terrain_options"},
             {"label": "Rulings", "icon": "res://icons/rulings.png", "sub": "rulings_options"},
             # Add more quadrants
         ],
         "terrain_options": [
             {"label": "Biomes", "action": "edit_biomes"},
             {"label": "Landmarks", "sub": "landmark_options"},  # Nested sub-level
             # Integrate from blocked docs if available (e.g., city generation)
         ],
         # Add more keys for deeper levels
     }
     ```

3. **Enhanced GDScript for Generation**:
   - The script procedurally generates wedges using polar math. Improvements: Recursive sub-wheel creation, prefab instantiation for wedges, better animation chaining, and signal emission for previews/AI.
     ```gdscript
     extends Control

     # Exports for customization
     @export var wedge_prefab: PackedScene  # A pre-made TextureButton scene with Label child
     @export var radius: float = 200.0
     @export var max_wedges: int = 8
     @export var colors: Array[Color] = [Color.GREEN, Color.BLUE, Color.RED, Color.PURPLE]

     var current_path: Array[String] = ["root"]  # Tracks hierarchy, e.g., ["root", "terrain_options"]
     var context: Dictionary = {}  # e.g., {"type": "biome"}
     var sub_wheels: Array[Control] = []  # For managing nested wheels

     signal update_preview(data: Dictionary)  # Emit to parent for viewport updates
     signal request_ai_suggestion(prompt: String)  # For AI integration

     func _ready():
         visible = false

     func open_at(position: Vector2, initial_context: Dictionary):
         context = initial_context
         global_position = position
         current_path = ["root"]
         generate_wheel()
         animate_open()

     func generate_wheel():
         # Clear existing children
         for child in get_children():
             child.queue_free()

         # Get data for current level
         var current_data = menu_data.get(current_path.back(), [])
         if current_data.size() > max_wedges:
             print_warning("Too many wedges; truncating to " + str(max_wedges))
             current_data = current_data.slice(0, max_wedges)

         # Generate wedges
         for i in current_data.size():
             var data = current_data[i]
             var wedge = wedge_prefab.instantiate() as TextureButton
             wedge.texture_normal = load(data["icon"])
             wedge.modulate = colors[i % colors.size()]
             # Position radially
             var angle_step = 2 * PI / current_data.size()
             var angle = angle_step * i - PI / 2  # Start at top
             wedge.position = Vector2(cos(angle), sin(angle)) * radius
             # Set label/tooltip
             wedge.get_child(0).text = data["label"]  # Assuming Label as child 0
             wedge.tooltip_text = data.get("tooltip", "")
             wedge.connect("pressed", _on_wedge_pressed.bind(data))
             add_child(wedge)

     func _on_wedge_pressed(data: Dictionary):
         if data.has("sub"):
             # Enter sub-level (fractal expansion)
             current_path.append(data["sub"])
             animate_zoom_to_sub()
             generate_wheel()
         elif data.has("action"):
             # Terminal action: Execute and close
             execute_action(data["action"])
             animate_close()
         else:
             print_error("Invalid wedge data")

     func execute_action(action: String):
         # Context-specific logic
         match action:
             "edit_biomes":
                 update_preview.emit({"type": "biome", "context": context})
             # Add more, e.g., "generate_city" from city generator doc
         # Optional AI call
         if context.get("use_ai", false):
             request_ai_suggestion.emit("Suggest options for " + action)

     # Back navigation
     func go_back():
         if current_path.size() > 1:
             current_path.pop_back()
             animate_zoom_back()
             generate_wheel()

     # Animation helpers
     func animate_open():
         var tween = create_tween()
         tween.tween_property(self, "scale", Vector2(1, 1), 0.3).from(Vector2(0.5, 0.5))

     func animate_zoom_to_sub():
         var tween = create_tween()
         tween.tween_property(self, "modulate:a", 0.5, 0.2)  # Fade parent slightly

     func animate_zoom_back():
         var tween = create_tween()
         tween.tween_property(self, "modulate:a", 1.0, 0.2)

     func animate_close():
         var tween = create_tween()
         tween.tween_property(self, "scale", Vector2(0.5, 0.5), 0.3)
         tween.tween_callback(queue_free)  # Or set visible=false for reuse
     ```

4. **Integration with Mythos Features**:
   - **Context-Sensitivity**: Update `menu_data` dynamically (e.g., filter options based on selected element like "forest" biome).
   - **Narrative/AI**: On generation, display prompts (e.g., "Shape the land?") via a central Label. Connect AI signals to populate sub-options.
   - **Previews**: Emit signals to update the central Viewport (e.g., apply textures/shaders).
   - **Extensions for Blocked Docs**: For landmark placement or city generation, add sub-keys like "landmark_options" with actions for drag-and-drop or procedural sliders. If those involve fractal terrain (e.g., recursive voids), integrate Godot's NoiseTexture for procedural visuals.

5. **Testing and Optimization**:
   - **Accessibility**: Add keyboard navigation (e.g., arrows to cycle wedges) and screen reader support.
   - **Performance**: Use object pooling for wedges if menus change frequently. Test on low-end hardware.
   - **Edge Cases**: Handle empty levels, invalid contexts, or multiplayer sync (update JSON on actions).

This generates the fractal menus procedurally, ensuring they're extensible for Mythos Tabletop's lore-driven gameplay. If you provide more specifics (e.g., from blocked docs), I can refine the script further!

## Review Needed
Proposed para-type: project. Assigned based on content/frontmatter (confidence ~70%). Do not move until reviewed.