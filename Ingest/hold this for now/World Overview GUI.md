---
proposal_path: Ingest/Decisions/Decision-for-world-overview-gui--2026-03-04-0440.md
---
## TL;DR
The fractal wheel menu for the Session Preparation System in *Mythos Tabletop* is a radial, context-sensitive interface designed to streamline Dungeon Master (DM) interactions with the Session Prep mo...

---

The fractal wheel menu for the Session Preparation System in *Mythos Tabletop* is a radial, context-sensitive interface designed to streamline Dungeon Master (DM) interactions with the Session Prep mode. It integrates with the existing GUI elements (World Overview Panel, Element Selector, AI Chat Window, Timeline GUI, Map GUI, and Resource Browser) to provide quick access to quest planning, world editing, and AI collaboration tools. The menu appears when the DM right-clicks on a world element (e.g., a city, landmark, or NPC) in the 2D top-down or 3D free-cam view, offering a visually intuitive, hierarchical structure that mirrors the system’s collaborative and flexible design. Below, I’ll outline the design, functionality, implementation, and integration of the fractal wheel menu, tailored to the Session Preparation System described in the provided documents.

---

### Design Goals
- **Intuitive Navigation**: Provide a visually appealing, radial menu that organizes complex session prep tasks into clear, hierarchical options, reducing reliance on nested panels or toolbars.
- **Context-Sensitivity**: Dynamically adjust menu options based on the selected world element (e.g., city, landmark, NPC, or sub-tile) to minimize irrelevant choices.
- **Fractal Structure**: Use a multi-layered, zoomable wheel where each segment expands into sub-menus, resembling a fractal pattern, to handle the depth of options (e.g., quest creation, NPC editing, or timeline adjustments) without overwhelming the DM.
- **Integration with AI Assistant**: Embed AI-driven suggestions and prompts directly into the menu, enabling seamless collaboration (e.g., suggesting enemies for a landmark or quest hooks for an NPC).
- **Efficiency**: Minimize clicks and navigation time, allowing DMs to perform tasks (e.g., linking a quest to a landmark) within the wheel while maintaining access to the 3D/2D world view.
- **Aesthetic Consistency**: Align with *Mythos Tabletop*’s immersive, Skyrim-like aesthetic, using thematic visuals (e.g., runic or parchment textures) and smooth animations.

---

### Interface and Structure

The fractal wheel menu is a circular, radial interface that appears at the cursor’s position upon right-clicking a world element in Session Prep mode. It uses a layered design where each segment (or "wedge") represents a category of actions, and selecting a wedge zooms into a sub-wheel with detailed options. The menu is rendered as a Godot `Control` node with animated transitions, ensuring it feels responsive and integrated with the 3D world view.

#### Core Components
1. **Root Wheel**:
   - Appears on right-click, with 6–8 primary wedges, each representing a high-level category of session prep actions.
   - Categories are context-sensitive, based on the clicked element (e.g., city, landmark, NPC, or empty sub-tile).
   - Visuals: Semi-transparent, parchment-like background with glowing runic icons for each wedge, themed to match the world’s aesthetic (e.g., elven vine motifs for tree-cities).
   - Animation: Fades in with a slight scale-up effect; wedges pulse subtly when hovered.

2. **Sub-Wheels**:
   - Clicking a root wedge zooms the interface to a sub-wheel with 4–8 sub-options, arranged radially around the selected category.
   - Sub-wheels may branch further (e.g., Quest Creation → Hook → Specific Hook Types), creating a fractal hierarchy.
   - A "Back" wedge allows returning to the parent wheel without closing the menu.
   - Visuals: Sub-wheels inherit the root’s aesthetic but scale down opacity and size slightly to indicate depth.

3. **Context Labels**:
   - A small tooltip-like label above the wheel displays the selected element (e.g., “Elven Tree-City: Sylvara” or “Cave Entrance Landmark”).
   - AI-driven hints appear as subtle text prompts around the wheel’s edge (e.g., “Try adding a cursed relic to this cave quest?”).

4. **Interaction**:
   - Input: Mouse hover to highlight wedges, left-click to select or expand, right-click to close or go back.
   - Optional: Keyboard shortcuts (e.g., 1–8 for root wedges) for power users.
   - Accessibility: Scalable UI, colorblind-friendly contrast, and screen reader support for wedge labels.

---

### Root Wheel Categories and Context-Sensitivity

The root wheel’s wedges adapt to the selected world element, pulling data from the world’s JSON serialization (e.g., section/sub-tile metadata, city templates, or NPC pools). Below are the primary categories and their behavior for different element types, with sub-wheel examples.

#### 1. Quest Creation
- **Available For**: Cities, landmarks, NPCs, sub-tiles.
- **Purpose**: Initiate or edit a quest tied to the selected element.
- **Root Wedge Icon**: A glowing scroll.
- **Sub-Wheel Options**:
  - **Hook**: Define the quest’s starting point (e.g., “Blacksmith seeks protection” for an NPC).
    - Sub-options: Fetch, Escort, Combat, Exploration, Moral Dilemma.
    - AI Prompt: “What’s the hook’s tone? Urgent, mysterious, or comedic?”
  - **Branching Paths**: Add “if” conditions (e.g., “If players fail stealth, spawn Kobolds”).
    - Sub-options: Add Condition, Edit Outcomes, Link to Timeline.
  - **Rewards**: Set rewards (e.g., enchanted weapon, lore snippet).
    - Sub-options: Item (from Resource Browser), XP, Custom.
  - **Link to Element**: Tie the quest to another world element (e.g., a cave landmark for a city NPC quest).
    - Sub-options: Search Landmarks, Search NPCs, Auto-Suggest (AI-driven).
- **Context Example** (Elven City):
  - DM right-clicks the city “Sylvara.” The Quest Creation wedge offers hooks like “Protect the sacred grove” (AI-suggested based on elven template).
  - Selecting “Hook” → “Combat” prompts the AI: “Enemies for a forest grove? Suggestions: Dire Wolves, Corrupted Treants.”

#### 2. Element Editing
- **Available For**: Cities, landmarks, NPCs, sub-tiles.
- **Purpose**: Modify properties of the selected element (e.g., city wealth, landmark size).
- **Root Wedge Icon**: A hammer and quill.
- **Sub-Wheel Options**:
  - **Properties**: Adjust metadata sliders (e.g., population density for cities, danger level for landmarks).
    - Sub-options: Biome-Specific (e.g., tree density for forests), Custom Fields.
  - **Structures/NPCs**: Add or edit sub-elements (e.g., add a tavern to a city, change an NPC’s role).
    - Sub-options: Add New, Edit Existing, Procedural Pool (e.g., “Blacksmith Pool”).
  - **Visuals**: Tweak aesthetics (e.g., weathering for ruins, bioluminescence for elven cities).
    - Sub-options: Texture Variants, Particle Effects, Lighting.
- **Context Example** (Cave Entrance):
  - DM right-clicks a cave landmark. The Element Editing wedge offers “Properties” → “Depth Hint” (shallow/deep) and “Visuals” → “Lighting” (torchlit/bioluminescent).
  - AI Prompt: “Deep caves might suit high-level threats like a Drider. Adjust danger level?”

#### 3. Timeline Management
- **Available For**: Cities, landmarks, NPCs, sub-tiles (quests must be initiated).
- **Purpose**: Build or edit the Timeline GUI for sequencing quest events or session arcs.
- **Root Wedge Icon**: A branching tree.
- **Sub-Wheel Options**:
  - **Add Event**: Create a new timeline node (e.g., “Ambush at cave entrance”).
    - Sub-options: Encounter, Roleplay, Decision Point.
  - **Branching**: Define player choice outcomes (e.g., “Find relic” vs. “Avoid relic”).
    - Sub-options: Add Branch, Link to Quest, AI-Suggested Paths.
  - **Time Estimation**: Adjust event duration or travel time (e.g., “30-minute forest trek”).
    - Sub-options: Manual Input, AI-Calculated (based on map data).
- **Context Example** (NPC: Blacksmith):
  - DM right-clicks a blacksmith NPC with a protection quest. The Timeline Management wedge offers “Add Event” → “Climax” (e.g., “Defend against Drider”).
  - AI Prompt: “This encounter seems deadly. Add a rest point before the climax?”

#### 4. Map Visualization
- **Available For**: Cities, landmarks, sub-tiles.
- **Purpose**: Access the Map GUI to visualize paths, encounters, or travel times.
- **Root Wedge Icon**: A compass and map.
- **Sub-Wheel Options**:
  - **Path Planning**: Draw a path from the element to another (e.g., city to landmark).
    - Sub-options: Auto-Generate Path, Manual Draw, Add Stops (e.g., campsite).
  - **Encounter Simulation**: Test encounters along a path (e.g., drag a player token to trigger spider ambush).
    - Sub-options: Add Encounter, Adjust Difficulty, AI-Suggested Enemies.
  - **Travel Estimations**: View or edit travel times (e.g., “20 minutes through forest”).
    - Sub-options: Terrain Modifiers (e.g., swamp delays), Weather Effects.
- **Context Example** (Sub-Tile: Forest Path):
  - DM right-clicks a forest sub-tile. The Map Visualization wedge offers “Path Planning” → “Auto-Generate” to a nearby cave.
  - AI Prompt: “Swamp terrain may slow travel by 5 minutes. Include weather effects like rain?”

#### 5. AI Collaboration
- **Available For**: All elements.
- **Purpose**: Directly interact with the AI assistant for suggestions or refinements.
- **Root Wedge Icon**: A glowing crystal (symbolizing AI intelligence).
- **Sub-Wheel Options**:
  - **Suggest Content**: Request AI-generated ideas (e.g., enemies, lore, quest hooks).
    - Sub-options: Enemies, Items, Story Arcs.
  - **Refine Input**: Clarify vague DM inputs (e.g., “Add a monster” → “What level or biome?”).
    - Sub-options: Prompt for Details, Auto-Fill Basics.
  - **Balance Check**: AI evaluates quest or encounter difficulty (e.g., “Too deadly for level 1?”).
    - Sub-options: Adjust Stats, Scale Challenge, Add Mitigations.
- **Context Example** (Landmark: Ruin):
  - DM right-clicks a ruin. The AI Collaboration wedge offers “Suggest Content” → “Enemies” (e.g., “Skeletons or Wraiths for a haunted ruin?”).
  - AI Prompt: “A cursed relic could tie to the ruin’s lore. Want to add a related quest?”

#### 6. Resource Browser
- **Available For**: All elements.
- **Purpose**: Access internal databases (e.g., enemies, items, lore) for quick integration.
- **Root Wedge Icon**: A book and magnifying glass.
- **Sub-Wheel Options**:
  - **Search Database**: Browse compendiums (e.g., D&D 5e-inspired enemies).
    - Sub-options: Filter by Type (Enemy, Item, Lore), Keyword Search.
  - **Add to Element**: Attach a resource to the element (e.g., add a “Longsword +1” to an NPC).
    - Sub-options: Direct Add, Customize First.
  - **Homebrew Entry**: Create custom content via natural language input.
    - Sub-options: Enemy, Item, Lore Snippet.
- **Context Example** (City: Human Town):
  - DM right-clicks a tavern. The Resource Browser wedge offers “Search Database” → “NPCs” (e.g., “Add a Bard from the Tavern Pool”).
  - AI Prompt: “Bards could offer a quest hook. Want to generate a performance-based quest?”

---

### Example Workflow: Quest Planning in an Elven City
1. **Initiate Menu**:
   - DM right-clicks the elven tree-city “Sylvara” in 3D view. The fractal wheel appears, displaying wedges: Quest Creation, Element Editing, Timeline Management, Map Visualization, AI Collaboration, Resource Browser.
   - Context Label: “Elven Tree-City: Sylvara.”

2. **Quest Creation**:
   - DM selects the Quest Creation wedge, zooming to a sub-wheel with Hook, Branching Paths, Rewards, and Link to Element.
   - DM chooses “Hook” → “Combat.” The AI prompts: “Protect the sacred grove from predators? Suggested enemies: Dire Wolves, Corrupted Treants.”
   - DM confirms “Dire Wolves” and adds a hook: “Elder Druid seeks defenders for the grove.”

3. **Timeline Management**:
   - DM navigates back to the root wheel and selects Timeline Management, zooming to Add Event, Branching, and Time Estimation.
   - DM picks “Add Event” → “Entry Encounter” (Dire Wolf ambush). The AI suggests: “2–4 Dire Wolves for level 1–3 players.”
   - DM adds a branching path: “If players investigate grove, find a relic.”

4. **Map Visualization**:
   - DM selects Map Visualization from the root wheel, choosing “Path Planning” → “Auto-Generate” to a nearby grove landmark.
   - The Map GUI overlays a glowing path, estimating “15-minute trek through forest.”
   - AI Prompt: “Add a campsite stop for roleplay?”

5. **AI Collaboration**:
   - DM selects AI Collaboration → “Suggest Content” → “Story Arcs.”
   - AI suggests: “The relic is cursed, tied to an ancient elven betrayal. Want to expand this lore?”
   - DM confirms, and the AI integrates the curse into the quest’s JSON data.

6. **Finalize**:
   - DM uses the Resource Browser wedge to add a “Glowing Amulet” (the cursed relic) from the item compendium.
   - The menu closes with a right-click, and the quest serializes to the world’s JSON, guiding in-game AI responses.

---

### Technical Implementation in Godot 4.x
- **Node Structure**:
  - **Root Node**: A `Control` node (e.g., `FractalWheelMenu`) parented to the Session Prep `CanvasLayer`.
  - **Wedge Nodes**: Each wedge is a `TextureButton` with a custom `StyleBox` for the parchment/runic aesthetic. Sub-wheels are nested `Control` nodes, toggled via visibility.
  - **Animation**: Uses `AnimationPlayer` for fade-in, scale-up, and pulse effects. Transitions between wheels use `Tween` for smooth zooming.
  - **Context Data**: A `Dictionary` stores the selected element’s metadata (e.g., `{"type": "city", "id": "Sylvara", "biome": "forest"}`), pulled from the world’s JSON.

- **Scripts**:
  - **Main Script** (`fractal_wheel_menu.gd`):
    ```gdscript
    extends Control

    var context: Dictionary
    var current_wheel: Node
    var ai_assistant: Node  # Reference to AI agent

    func _ready():
        visible = false
        # Connect right-click signal from world view
        get_parent().connect("right_clicked", self, "_on_world_right_click")

    func _on_world_right_click(element_data: Dictionary, position: Vector2):
        context = element_data
        position = position
        update_root_wheel()
        visible = true
        animate_open()

    func update_root_wheel():
        # Clear existing wedges
        for child in current_wheel.get_children():
            child.queue_free()
        # Add wedges based on context (e.g., city vs. NPC)
        var wedges = generate_wedges(context["type"])
        for wedge_data in wedges:
            var wedge = create_wedge(wedge_data)
            current_wheel.add_child(wedge)

    func create_wedge(data: Dictionary) -> TextureButton:
        var wedge = TextureButton.new()
        wedge.texture_normal = load(data["icon"])
        wedge.connect("pressed", self, "_on_wedge_pressed", [data["action"]])
        return wedge

    func _on_wedge_pressed(action: String):
        if action.begins_with("subwheel_"):
            show_subwheel(action)
        else:
            execute_action(action)
    ```
  - **AI Integration**: The AI assistant node (from the existing PRD) processes natural language inputs via the `ai_assistant.parse_input()` function, returning suggestions or prompts displayed as labels.
  - **Serialization**: Menu actions (e.g., quest creation, timeline edits) update the world’s JSON via `world_data.update_quest()` or similar functions, ensuring persistence.

- **Performance**:
  - **Optimization**: Limit wedge count to 8 per wheel to avoid clutter. Use `CanvasItem` culling for off-screen rendering.
  - **LOD Integration**: Menu visuals scale with the world’s LOD system (e.g., lower texture resolution in distant 3D views).
  - **Edge Cases**: Handle invalid contexts (e.g., clicking a void) by showing a minimal wheel with only AI Collaboration and Resource Browser.

- **UI Integration**:
  - The menu overlays the World Overview Panel, temporarily disabling other GUI inputs (e.g., Timeline GUI) to prevent conflicts.
  - Links to existing panels: Selecting “Add Event” opens the Timeline GUI; “Search Database” toggles the Resource Browser.

---

### Visual and Aesthetic Details
- **Theme**: Parchment background with runic or biome-specific borders (e.g., vines for elven contexts, stone carvings for dwarven). Wedges use glowing icons (e.g., scroll for Quest Creation, compass for Map Visualization).
- **Animations**:
  - Open: Wheel scales from 0.5 to 1.0 over 0.3 seconds with a slight rotation.
  - Sub-Wheel Transition: Parent wheel fades to 50% opacity, sub-wheel zooms in from the selected wedge’s position.
  - Hover: Wedges glow brighter and scale up by 10%.
- **Feedback**: Subtle audio cues (e.g., parchment rustle on open, click on selection) using Godot’s 3D spatial audio for immersion.

---

### Edge Cases and Accessibility
- **Edge Cases**:
  - **No Valid Element**: If the DM clicks an unplaced section (void), the wheel offers only AI Collaboration and Resource Browser to suggest new elements (e.g., “Place a landmark here?”).
  - **Overlapping Actions**: If a quest is already tied to an element, the Quest Creation wedge shows “Edit Quest” instead of “New Quest.”
  - **Multi-Selection**: If multiple elements are selected (e.g., via drag-select), the wheel prioritizes common actions (e.g., Map Visualization for paths between elements).
- **Accessibility**:
  - Colorblind mode: High-contrast wedge icons and text labels.
  - Screen reader: Reads wedge names and AI prompts aloud.
  - Scalable UI: Adjusts wheel size via settings (e.g., 80–120% scaling).
  - Keyboard navigation: Number keys (1–8) select wedges; arrow keys navigate sub-wheels.

---

### Future Enhancements
- **Voice Input**: Integrate with the AI Chat Window’s voice-to-text for hands-free menu navigation (e.g., “Open Quest Creation”).
- **Custom Wedges**: Allow DMs to add homebrew wedges via the Modding API (e.g., a custom “Faction Editor”).
- **Visual Previews**: Sub-wheels show 3D thumbnails (e.g., a Dire Wolf model when selecting enemies).
- **Multiplayer Sync**: Share the wheel’s state with co-DMs in real-time for collaborative prep.

---

### Sample Mockup
Here’s a conceptual layout of the root wheel for an elven city:

```
[Fractal Wheel Menu: Elven Tree-City: Sylvara]
  (Scroll) Quest Creation → [Hook, Branching Paths, Rewards, Link to Element]
  (Hammer) Element Editing → [Properties, Structures/NPCs, Visuals]
  (Tree) Timeline Management → [Add Event, Branching, Time Estimation]
  (Compass) Map Visualization → [Path Planning, Encounter Simulation, Travel Estimations]
  (Crystal) AI Collaboration → [Suggest Content, Refine Input, Balance Check]
  (Book) Resource Browser → [Search Database, Add to Element, Homebrew Entry]

## Review Needed
Proposed para-type: project. Assigned based on content/frontmatter (confidence ~70%). Do not move until reviewed.