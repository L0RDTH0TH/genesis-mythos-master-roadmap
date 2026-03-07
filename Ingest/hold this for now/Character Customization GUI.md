---
confidence: 70%
created: 2026-03-02
status: ingest
proposal_path: Ingest/Decisions/Decision-for-character-customization-gui--2026-03-04-0424.md
decision_priority: high
---
## TL;DR
The **Character Customization** system in *Mythos Tabletop* enables players to craft 3D character models with deep personalization, integrating appearance, class-based visuals, narrative archetypes, a...

---

The **Character Customization** system in *Mythos Tabletop* enables players to craft 3D character models with deep personalization, integrating appearance, class-based visuals, narrative archetypes, and roleplay elements. Built in Godot 4.x, it uses a dynamic, fractal-based UI to guide players through a narrative-driven creation process, accessible pre-session or in social hubs (e.g., taverns, camps). The system ties into Dungeons & Dragons 5e-inspired mechanics, the procedural world, and multiplayer framework, with visuals updating dynamically (e.g., a paladin’s glowing aura, a rogue’s shadowed cloak) to enhance immersion.

## Key Features

### 1. Character Creator Interface
- **Access Points**: Available at game start (pre-session) or in social hubs via interactive objects (e.g., a mirror or tailor NPC). Hub changes support roleplay (e.g., donning ceremonial robes for a festival).
- **UI Design**: A 3D viewport previews the character model in real-time, surrounded by a circular fractal UI that “zooms in” with each selection, creating a layered, immersive experience. Tabs for Appearance, Class, Stats, and Roleplay are replaced by a narrative-driven question flow. A “Randomize” button offers a valid character for quick setup.
- **Fractal Color Wheel**: A circular interface divided into four quadrants, each tied to an archetype group (Identity and Self, Transformation and Balance, Guidance and Authority, Rebellion and Change). Selecting a quadrant zooms into sub-options (specific archetypes), with colors matching the archetype list (e.g., Gold for The Self, Red for The Hero). Animations use Godot’s Tween node for smooth transitions.
- **Navigation**: Questions guide the flow (“What story do you want to tell?”, “Who do you want to be?”, “Who were you?”, “Who are you?”), with selections narrowing options in the fractal wheel. Tooltips provide lore and gameplay impacts (e.g., “The Hero emphasizes bravery, suited for Fighter or Paladin”).
- **Performance**: Uses Godot’s SubViewport for the character preview, with LOD for hub NPCs to maintain 60 FPS. Changes save instantly to the player’s JSON profile.

### 2. Character Creation Workflow
The creation process is a step-by-step, narrative-driven sequence that integrates the archetype groups, class selections, and DM world rules. Each step uses the fractal color wheel to visually guide the player, with questions prompting introspection and tying choices to the game world.

- **Step 1: Launch and Connect to DM’s World**
  - **Action**: New player launches *Mythos Tabletop* and selects “New Character.”
  - **Prompt**: “Connect to your DM’s world for character creation rules.”
  - **Process**: Player inputs a world ID or joins via a server list (using Godot’s High-Level Multiplayer API). The system loads DM-defined rules (e.g., restricted classes, point-buy stat limits) from the world’s JSON configuration.
  - **UI**: A simple text input with a “Connect” button, followed by a confirmation popup showing the world’s name and DM’s rules summary.
  - **Edge Case**: If offline, a default ruleset (D&D 5e standard) is used, flagged for DM approval later.

- **Step 2: Choose the Story**
  - **Prompt**: “What story do you want to tell?”
  - **Action**: The fractal color wheel appears, divided into four quadrants, each representing an archetype group:
    - Identity and Self (Gold, Blue, Black)
    - Transformation and Balance (Purple, Pink, White)
    - Guidance and Authority (Silver, Green, Brown, Royal Blue, Grey)
    - Rebellion and Change (Red, Yellow, Orange, Crimson, Turquoise, Violet)
  - **Process**: Player clicks a quadrant, triggering a zoom-in animation to reveal sub-options (archetypes within the group). Each archetype displays its name, color, and a brief lore description (e.g., “The Hero: A brave soul destined for greatness, often a Fighter or Paladin”).
  - **UI**: The wheel uses a Godot CanvasLayer with a Control node for the circular layout. Sub-options are radial buttons with animated color gradients matching archetype colors. A 3D character preview updates with a placeholder model reflecting the archetype (e.g., a glowing aura for The Self).
  - **Example**: Selecting “Rebellion and Change” zooms into Hero, Child, Trickster, Rebel, Creator, Magician, with Red highlighting Hero.

- **Step 3: Define the Role**
  - **Prompt**: “Who do you want to be?”
  - **Action**: Player selects a specific archetype from the zoomed-in quadrant (e.g., The Hero). The system presents story-appropriate classes tied to the archetype (e.g., Hero: Fighter, Paladin, Barbarian, Ranger) and an “Other” option allowing any class.
  - **Process**: Class selection updates the 3D preview with class-specific visuals (e.g., Fighter’s battle-worn armor, Paladin’s glowing plate). A tooltip shows class mechanics (e.g., “Paladin: Oath-bound warrior with divine smites”). The “Other” option displays all classes (Monk, Bard, Rogue, etc.) with a warning if they deviate from DM rules.
  - **UI**: The fractal wheel zooms further, showing class icons in a radial layout around the archetype’s color. A “Confirm” button locks the choice, with an undo option.
  - **Example**: Choosing The Hero suggests Fighter, Paladin, Barbarian, Ranger. Selecting Paladin applies a radiant armor texture and faint glow effect.

- **Step 4: Craft the Backstory**
  - **Prompt**: “Who were you?”
  - **Action**: An AI assistant, integrated with the DM’s world, guides the player in creating a backstory that fits the world’s lore and the chosen archetype/class.
  - **Process**:
    - The AI parses the world’s JSON (biomes, cities, landmarks, factions) to suggest context-appropriate backstory elements (e.g., a Hero Paladin from a human medieval town might be a “knight exiled after defending a village from bandits”).
    - Players input preferences via text fields or dropdowns (e.g., “I want a tragic past” or “I’m a wanderer”). The AI generates 2–3 backstory options, each 50–100 words, with hooks for DM quests (e.g., “Seek the bandit leader for redemption”).
    - Backstories are flagged for DM approval, sent via the multiplayer server or saved for offline review. The DM can edit or reject, with feedback sent to the player.
  - **UI**: A dialogue window with a text area for player input and a “Generate” button. Backstory options appear as selectable cards with lore snippets and quest hooks. The 3D preview updates with subtle visual cues (e.g., scars for a tragic past).
  - **Example**: For a Hero Paladin in a mountain-based dwarven fortress world, the AI suggests: “You were a guard captain who failed to protect a sacred forge, now seeking atonement.” The player selects this, and it’s flagged for DM approval.

- **Step 5: Assign Stats**
  - **Prompt**: “Who are you?”
  - **Action**: Player assigns stats using the DM’s point-buy system (e.g., D&D 5e standard: 27 points across Strength, Dexterity, Constitution, Intelligence, Wisdom, Charisma).
  - **Process**:
    - The system presents a stat allocation interface with sliders or input fields, enforcing DM rules (e.g., max 15 in a stat before racial bonuses).
    - Archetype and class suggest optimal stats (e.g., Hero Paladin: high Strength and Charisma), but players can customize freely within limits.
    - Racial bonuses apply automatically (e.g., Dwarf: +2 Constitution). A tooltip shows stat impacts (e.g., “Strength boosts melee damage”).
  - **UI**: The fractal wheel zooms to a stat ring, with each stat as a node colored by the archetype (e.g., Red for Hero). Sliders adjust points, with a remaining-points counter. The 3D preview updates animations (e.g., stronger stance for high Strength).
  - **Example**: A Hero Paladin allocates 15 Strength, 14 Charisma, 12 Constitution, with 27 points. The preview shows a confident pose and glowing aura.

- **Step 6: Finalize Appearance**
  - **Prompt**: “How do you present yourself?”
  - **Action**: Player customizes appearance, equipment, and roleplay elements, building on the class and archetype visuals.
  - **Process**:
    - **Appearance**: Select race (Human, Elf, Dwarf, Halfling), adjusting body (height ±10%, build, age), face (jawline, eyes), hair (styles, colors), and skin (tone, scars, tattoos). Archetype influences defaults (e.g., Hero: muscular build, bold features).
    - **Equipment**: Choose armor (light, medium, heavy), weapons (melee, ranged, magical), and accessories (rings, cloaks). Archetype colors apply (e.g., Hero: Red-tinted armor). Material swaps (e.g., steel to mithril) and wear sliders add detail.
    - **Roleplay**: Select ceremonial outfits, emotes (e.g., heroic salute), and voice sets (e.g., commanding tone). Backstory choices add visual cues (e.g., exile’s worn cloak).
    - **Dynamic Updates**: Godot’s SkinnedMesh and shaders adjust the model in real-time (e.g., glowing Red aura for Hero Paladin’s plate armor).
  - **UI**: The fractal wheel zooms to a customization ring, with tabs for body, equipment, and roleplay. A color picker uses archetype colors (e.g., Red for Hero). The 3D viewport rotates for inspection.
  - **Example**: A Hero Paladin selects Dwarf, adds a scarred face, chooses heavy plate armor with Red accents, and picks a commanding voice set.

- **Step 7: Save and Submit**
  - **Action**: Player confirms the character, saving it to their JSON profile and submitting for DM approval.
  - **Process**: The system serializes all data (archetype, class, stats, appearance, backstory) and sends it to the DM via the multiplayer server or offline queue. The DM can approve, reject, or suggest changes (e.g., “Reduce Strength to 14 for balance”). Approved characters sync to the world for gameplay.
  - **UI**: A “Finalize” button triggers a confirmation popup with a character summary. The fractal wheel animates a closing spiral to signal completion.
  - **Example**: The Hero Paladin’s data (Dwarf, Paladin, Red-themed armor, exile backstory) is saved and flagged for DM review.

### 3. Integration with Archetypes
- **Archetype Influence**: Each archetype ties to specific classes and colors, guiding the player’s choices while allowing flexibility via the “Other” class option. Visuals reflect archetype themes (e.g., The Shadow’s Black cloak for a Rogue, The Magician’s Violet staff glow for a Wizard).
- **Color Wheel**: The fractal UI uses archetype colors for quadrants and sub-options, with Godot’s GradientTexture2D for smooth transitions. For example:
  - Identity and Self: Gold (Self), Blue (Persona), Black (Shadow).
  - Rebellion and Change: Red (Hero), Yellow (Child), Orange (Trickster).
- **Narrative Guidance**: The AI assistant reinforces archetypes in backstory generation (e.g., The Trickster’s backstory involves deception, like a Rogue swindling a merchant).

### 4. Technical Implementation in Godot 4.x
- **Core Nodes**:
  - **Fractal Wheel**: A CanvasLayer with a custom Control node for the circular UI. Uses Godot’s DrawCircle and AnimationPlayer for zoom animations.
  - **Character Preview**: A SubViewport with a Node3D for the character model, using SkinnedMesh for rigging and shaders for archetype colors.
  - **UI Elements**: Control nodes (e.g., OptionButton, Slider) for stats and customization, styled with archetype colors via Theme overrides.
- **Scripts**:
  - `render_fractal_wheel(quadrant: String)`: Draws the wheel, zooms to sub-options, and updates colors based on archetype.
  - `generate_backstory(world_data: Dictionary, archetype: String)`: AI-driven script parsing world JSON and player inputs to create backstory options.
  - `apply_character_visuals(data: Dictionary)`: Updates mesh, textures, and effects based on archetype, class, and customization choices.
  - `sync_character_to_server()`: Serializes data and sends to the DM via Godot’s multiplayer API.
- **Performance**:
  - **LOD**: Character models use LOD (high-detail in preview, low-poly in hubs). Wheel animations are GPU-accelerated.
  - **Optimization**: Batches shader updates for archetype colors. Unloads unused assets during creation.
  - **Networking**: Delta syncs for character changes (e.g., new armor) to minimize server load.
- **Edge Cases**: Handles DM rule conflicts (e.g., banned classes), archetype-class mismatches (e.g., Child Monk via “Other”), and offline mode (saves locally, syncs later).

### 5. Accessibility
- **Colorblind Modes**: Archetype colors use high-contrast gradients (e.g., Gold as bright yellow). UI labels support screen readers.
- **Customizable Controls**: Rebindable keys for wheel navigation (e.g., arrow keys for quadrant selection).
- **Scalable UI**: Adjustable font sizes and button scaling. Audio cues for wheel zooms and selection confirmations.

### 6. Example Workflow
1. Player launches *Mythos Tabletop*, selects “New Character,” and connects to a DM’s mountain-based world with standard D&D 5e rules.
2. Prompted “What story do you want to tell?”, they select the “Rebellion and Change” quadrant (Red/Yellow/Orange). The wheel zooms to show Hero, Child, Trickster, etc.
3. At “Who do you want to be?”, they pick The Hero (Red), selecting Paladin from suggested classes (Fighter, Paladin, Barbarian, Ranger). The preview shows radiant armor.
4. For “Who were you?”, the AI suggests a backstory: “A Dwarf Paladin exiled for defying a corrupt king, seeking to restore honor.” The player selects it, flagged for DM approval.
5. At “Who are you?”, they allocate 27 points (15 Strength, 14 Charisma, 12 Constitution). The preview updates with a strong stance.
6. For “How do you present yourself?”, they choose Dwarf, add a scarred face, Red-tinted plate armor, and a commanding voice set.
7. The character is saved and sent to the DM, who approves it. The player joins a session, their Paladin’s Red aura glowing in the dwarven fortress.

### 7. Future Expansions
- **Expanded Archetypes**: Add Jungian archetypes like The Explorer or The Caregiver with new class ties.
- **Dynamic Wheel Effects**: Particle effects on the fractal wheel (e.g., sparks for Rebellion quadrant).
- **Voice Integration**: Real-time voice modulation reflecting archetype (e.g., heroic tone for The Hero).
- **Community Archetypes**: Allow DMs to create custom archetypes via the modding API, shared in the marketplace.

This workflow creates an immersive, narrative-driven character creation process that ties archetypes to gameplay and visuals. If you’d like to refine specific steps, add more archetypes, or see GDScript snippets, let me know!

## Review Needed
Proposed para-type: area. Assigned based on content/frontmatter (confidence ~70%). Do not move until reviewed.