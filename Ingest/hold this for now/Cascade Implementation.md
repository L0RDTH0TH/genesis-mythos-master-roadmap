---
confidence: 70%
status: ingest
decision_candidate: true
guidance_conf_boost: 15
decision_priority: high
tags: guidance-aware
proposal_path: Ingest/Decisions/Decision-for-cascade-implementation--2026-03-04-1022.md
---
> [!warning] Decision needed (confidence 70%)
> This note needs guidance. Add `user_guidance: | ...` and `approved: true` to frontmatter, then run EAT-QUEUE.
> Proposed path: 1-Projects/Genesis-Mythos-Cascade-GUI/Notes/Cascade Implementation.md
>
> [!tip] Suggested user_guidance (copy-paste into frontmatter)
> user_guidance: |
>   Classify as Project. Prefer path: 1-Projects/Genesis-Mythos-Cascade-GUI/Notes/Cascade Implementation.md. Split if >500 words or multiple topics.

### Overall Foundation Principles
- **Modularity**: Treat the GUI as a self-contained module that communicates via signals and data structures (e.g., dictionaries or resources). This way, it can plug into core game systems without tight coupling. Use Godot's scenes for composability—e.g., a "CascadeMenu" scene that can be instanced anywhere.
- **Robustness**: Leverage Godot's signal system for events (e.g., branch selected, portal update). Use Resources or ScriptableObjects-like classes for menu data (e.g., a MenuBranchResource with properties like title, sub-branches, associated 2D/3D content). Always back up your project before big changes—integrate Git directly in Godot's VCS menu for versioned saves.
- **Performance**: Since it's FPV 3D, keep the GUI lightweight. Use CanvasLayer for overlay, and optimize draws/animations to avoid frame drops in the main 3D viewport.
- **Extensibility**: Design for your VTTRPG needs—e.g., branches could load procedural content from your city generator or landmark placement logic. Start simple, then add multiplayer sync (via Godot's High-Level Multiplayer API) for shared tabletop sessions.

### Implementing the Cascade GUI in Godot
I'll break this down by your described components. Assume Godot 4.x for better UI tools (e.g., shaders, SubViewports). You can prototype this in a new scene like `CascadeGUI.tscn` extending Control, set as a fullscreen CanvasLayer.

#### 1. [[Cascade Tree]] (Blue Arched Wedges: Max 7 wedges per tree)
- **Visuals**: This is the root structure—left and right groups of wedges forming a bow-tie or fan shape around the central portal.
  - Use a Control node as the base container.
  - For each wedge: Create a custom Control subclass (e.g., `WedgeButton.gd`) that overrides `_draw()` to render blue arched outlines (use `draw_arc()` for curves, `draw_line()` for edges). Fill with semi-transparent blue for the base tree.
  - Position wedges symmetrically: Left group in a VBoxContainer rotated -45 degrees, right in another at +45 degrees. Anchor to center.
  - Example code snippet for `_draw()` in WedgeButton:
    ```
    func _draw():
        var center = size / 2
        var radius = min(size.x, size.y) / 2
        draw_arc(center, radius, deg_to_rad(-45), deg_to_rad(45), 32, Color.BLUE, 2.0)  # Outer arch
        draw_line(Vector2(0, center.y), center, Color.BLUE, 2.0)  # Left radial
        draw_line(Vector2(size.x, center.y), center, Color.BLUE, 2.0)  # Right radial
    ```
  - Add a Label child for text (e.g., "Player").
- **Behavior**: On ready, populate with initial wedges (e.g., from a data array: ["Main", "Player", "World", "Settings"]).

#### 2. [[Cascade Branches]] (Yellow on Hover/Click, Max 7)
- **Visuals**: Branches appear as smaller yellow wedges fanning out from the hovered tree wedge.
  - Each branch is another `WedgeButton` instance, but colored yellow via a modulate or style override.
  - Dynamically instance and position them in a fan: Calculate angles evenly (e.g., for 7 branches, spread 90 degrees total, 12.857 degrees each).
  - Hide them by default; use a Tween for smooth fan-out animation (scale from 0 to 1, rotate slightly).
- **Interaction**:
  - Connect `mouse_entered` on a tree wedge to show its branches (e.g., `func on_hover(): branches_container.visible = true; tween.play()`).
  - On `mouse_exited`, hide after a delay (to allow hovering directly to branches).
  - Clicking a branch: Emit a signal like `branch_selected(branch_data)`, add to breadcrumbs, repopulate the tree with the new branch's sub-options, and update the portal.
  - For quick progression: If hovering a branch shows sub-branches, chain the hover logic recursively. Limit depth to avoid clutter—use max 7 rule by scaling branch size dynamically (`branch_size = full_width / branch_count`).
  - Example: Player wedge branches to ["New", "Edit", "Join Game"]. Hover "New" shows ["Character", "Campaign"] without clicking, but click advances.

#### 3. [[Cascade Breadcrumb]] (Navigation History)
- **Visuals**: A horizontal bar (HBoxContainer) at the top, with Button or Label children for each level (e.g., "Main > Player > New Character > Archetypes > Family").
  - Style as subtle text, perhaps with purple arrows between (from your sketch).
- **Behavior**:
  - Maintain an array `breadcrumb_history: Array[Dict]` (each dict: {title: "Player", branch_data: {...}}).
  - On branch click, append to array, update HBox by clearing children and re-adding Labels/Buttons.
  - Clicking a breadcrumb item: Slice the array to that index, repopulate the tree with the selected level's branches, and refresh the portal.
  - Hover on breadcrumb: Temporarily show branches for that level (like a preview), allowing quick jumps.

#### 4. [[Cascade Portal]] (Green Elliptical Center)
- **Visuals**: An elliptical viewer in the dead center, outlined in green.
  - Use a SubViewport node (for mixing 2D/3D content) inside a ViewportContainer.
  - To make it elliptical: Apply a custom shader to clip/mask to an oval (e.g., discard pixels outside an ellipse equation in fragment shader).
    - Simple shader example:
      ```
      shader_type canvas_item;
      void fragment() {
          vec2 uv = UV - 0.5;
          if (length(uv * vec2(ASPECT, 1.0)) > 0.5) discard;
          COLOR = texture(TEXTURE, UV);
      }
      ```
  - Size it to ~50% of horizontal and 100% vertical screen ratio, anchor center.
- **Behavior**:
  - On branch hover/selection: Update the portal's content dynamically.
    - For 2D: Add a TextureRect or RichTextLabel as a child (e.g., show character stats text).
    - For 3D: Instance a 3D scene (e.g., Spatial with a MeshInstance for a character model or city preview), set as SubViewport's child. Rotate/zoom via input signals.
  - Tie to your VTTRPG: For "New Character > Archetype", load a 3D model preview; for "World > City", render a procedural city from your generator.

### Integration with Your VTTRPG Systems
- **From Attachments**: Based on filenames, assume "Mythos Tabletop.md" has core rules (e.g., archetypes, classes), "World-Building.md" for lore, "Landmark Placement.md" for procedural placement, "City Generator.md" for urban gen. Make the cascade data-driven—load menu branches from JSON/Resources parsed from these (e.g., archetypes as branches under "New Character").
- **Modular Tie-Ins**:
  - World Gen: Branch like "World > Generate City" calls a procedural script (e.g., using NoiseTexture for terrain, place landmarks via algorithm), previews in portal.
  - Character Creation: Branches lead to forms; save as a CharacterResource, load into 3D FPV scene.
  - FPV 3D Core: The GUI overlays the main 3D world (Camera3D for player view). Toggle GUI with input, or make it contextual (e.g., open on interact with in-world terminal).
  - Robustness: Use Autoload singleton (e.g., GameManager) for state (current menu, player data). For multiplayer VTTRPG, sync breadcrumb/portal state via RPCs.

### Next Steps & Tips
- **Prototype**: Start with a minimal tree (2-3 wedges), add hover branching, then breadcrumbs/portal. Test in a blank scene.
- **Tools**: Use Godot's AnimationPlayer for smooth transitions. For complex shapes, consider SVG imports or pre-made textures.
- **Edge Cases**: Handle overflow (e.g., >5 branches? Paginate or scroll). Mobile touch support: Replace hover with long-press.
- **Expansion**: Once GUI is solid, hook into 3D—e.g., portal previews feed into the main world scene for seamless transitions.

This should give a strong, refactor-resistant base. If you share more details (e.g., specific Mythos mechanics or Godot version), I can refine with code examples or debug ideas.

## Review Needed
Proposed para-type: project. Assigned based on content/frontmatter (confidence ~70%). Do not move until reviewed.