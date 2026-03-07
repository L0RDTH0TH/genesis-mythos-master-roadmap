---
proposal_path: Ingest/Decisions/Decision-for-session-preparation--2026-03-04-0440.md
---
## TL;DR
# Session Preparation System

---

# Session Preparation System

The Session Preparation System is an AI-assisted pre-game module integrated into the DM's toolkit within *Mythos Tabletop*, accessible via a dedicated "Session Prep" mode in the main menu. This system allows Dungeon Masters (DMs) to collaborate with an embedded AI assistant to refine world elements, plan quests, anticipate player actions, and establish narrative guidelines before players join the session. Built on Godot 4.x with AI integration (leveraging natural language processing for dynamic collaboration), it ensures that the generative AI used during gameplay (e.g., for NPC responses, environmental events, or quest adaptations) is aligned with the DM's vision. This prevents inconsistencies and enhances immersion by providing a structured "rehearsal" phase.

Session Prep is offline-capable, supporting solo DM planning, and syncs seamlessly to multiplayer sessions. It uses the existing world map (from the Hybrid World Generation system) as a foundation, allowing interactive modifications via GUI elements like pop-ups, timelines, and path visualizers. The AI assistant acts as a collaborative partner, suggesting ideas, searching internal databases (e.g., for enemies, lore), and prompting for clarifications to refine ambiguous inputs—mirroring the robust AI handling in combat customization.

### Key Objectives
- **Narrative Alignment**: Guide the in-game AI to adhere to DM-defined arcs, reducing the need for mid-session corrections.
- **Efficiency**: Streamline quest design with tools for visualization, estimation, and iteration.
- **Flexibility**: Support homebrew elements, scaling from simple side quests to multi-session campaigns.
- **Integration**: Builds on existing features like the City Generator, Landmark Placement, and NPC Integration, pulling data from the world's JSON serialization for context-aware suggestions.

### Interface and Workflow
The Session Prep GUI overlays the 3D world view (toggleable between 2D top-down and 3D free-cam modes) with interactive panels:
- **[[World Overview GUI]]**: Displays the loaded map (e.g., Roostworth) with zoomable navigation, highlighting placed sections, cities, landmarks, and voids.
- **Element Selector**: Left-click on any world element (e.g., a city, landmark, or biome sub-tile) to open a context-sensitive pop-up menu.
- **AI Chat Window**: A persistent underbar for natural language interaction with the AI assistant, supporting text input, voice-to-text, and response history.
- **Timeline GUI**: A draggable timeline panel for sequencing events, with bullet-point editing and branching paths for player choices in a tech tree like prezi appearance. 
- **Map GUI**: An enhance overlay that visualizes paths, estimates travel times, and simulates encounters in a city skyline like appearance.
- **Resource Browser**: Quick access to internal databases (e.g., enemy compendiums, item pools, lore snippets) for AI-suggested integrations.

#### Example Workflow: Quest Planning in an Elven City
1. **Initiate Session Prep**:
   - DM loads the world (e.g., Roostworth, a 20 km² map with mixed biomes, including an elven tree-city in a forest section) droping into a 2d plane camerafor the 3d world.
   - Players' characters are not yet created, so the AI assistant at the bottom of the screen prompts: "Since characters are pending, I'll suggest balanced challenges. Want to assume level 1–3 adventurers?"

2. **Select and Configure World Element**:
   - DM switches to 3D view and left-clicks the elven city (generated via the Elf: Tree-Cities template in the City Generator).
   - A pop-up appears with tabs: Overview (city stats like population density), Structures (edit sub-tiles), NPCs (manage inhabitants), Quests (add/edit arcs), and Custom (homebrew additions).
   - DM navigates to NPCs tab, which lists procedural pools (e.g., "Blacksmith Pool": 3–5 smiths with default traits like "Elven artisan specializing in enchanted blades").
   - DM adds a new quest to a blacksmith NPC: "Protection quest—guard the quest giver from predators in the nearby mine."
   - Checkbox options appear: "Make Unique" (expands for detailed planning), "Auto-Generate" (AI fills basics), "Link to Landmark" (e.g., attach to a Cave Entrance landmark).

3. **Expand with "Make Unique" Option**:
   - Selecting "Make Unique" opens a sub-panel for quest refinement.
   - AI assistant activates in the chat window: "Great choice! For a subterranean mine quest, I'll search our compendium for appropriate enemies. Suggestions: Giant Spiders (ambush predators), Kobolds (trap-setters), or Gelatinous Cubes (slow-moving hazards). Which fit your theme?"
   - AI cross-references the world's data: Mine landmark (from Landmark Placement) is in a mountain section adjacent to the elven city, with volcanic sub-tiles influencing suggestions (e.g., adding fire-based creatures like Magma Mephits).
   - AI prompts for uniqueness: "What's special about this quest? Could the players stumble across a lost artifact, uncover a hidden conspiracy, or face a moral dilemma (e.g., the predators are displaced by mining)?"
   - DM responds (e.g., via text): "They stumble across an ancient elven relic that's cursed."
   - AI refines: "Understood—adding a cursed relic branch. I'll ensure the in-game AI escalates tension if players investigate." 

4. **Plan Quest Arc with Timeline GUI**:
   - Timeline GUI pops up as a horizontal bar with draggable nodes for key events.
   - DM and AI collaborate to build a bullet-point arc:
     - **Hook (City Start)**: Blacksmith NPC approaches players in the tree-city tavern: "My mining expedition is plagued by beasts—protect me for a reward!"
     - **Travel to Mine (Path Visualization)**: AI estimates time based on map data (e.g., 30-minute forest trek at walking speed, factoring sub-tile terrain like swamps adding delays).
     - **Entry Encounter**: Ambush by 2–4 Giant Spiders (AI-suggested, scaled to assumed player levels).
     - **Exploration Branch**: Bullet points for paths—main tunnel (resource gathering), side chamber (stumble on relic).
     - **Climax**: Protect blacksmith from a boss predator (e.g., Drider); if relic found, trigger curse event (e.g., hallucinations).
     - **Resolution**: Return to city; rewards (enchanted weapon) and hooks for future quests (e.g., cure the curse).
   - Branching: DM adds "if" conditions (e.g., "If players fail stealth check: Additional Kobold reinforcements").
   - AI suggests balances: "This arc estimates 1–2 hours playtime. Add rest points to avoid fatigue?"

5. **Visualize with Map GUI**:
   - Map GUI overlays the path: A glowing line from elven city to mine landmark, with icons for encounters (e.g., spider webs at chokepoints).
   - Travel Estimations: "Forest leg: 20 minutes (easy terrain); Mountain ascent: 10 minutes (difficult, +5 minutes if raining)."
   - Simulation Mode: DM can "playtest" by dragging a player token along the path; AI seeds the story factoring in "stops" (e.g., campsite for roleplay), "attractions" (hidden groves), and "hazards" (monsters, weather).

6. **Finalize and Guide In-Game AI**:
   - DM saves the prep: Quest data serializes to JSON (e.g., arc bullets, enemy lists, uniqueness flags), linking to the NPC and landmark.
   - AI assistant confirms: "This prep will direct my responses during play—e.g., if players deviate, I'll suggest how to guide them back to the arc."
   - Integration with Gameplay: During sessions, the in-game AI references this prep for NPC dialogue (e.g., blacksmith mentions the mine predators), dynamic events (e.g., spawning suggested enemies), and adaptations (e.g., escalating if players find the relic).

### AI Assistant Behaviors
- **Proactive Suggestions**: Draws from internal compendiums (D&D 5e-inspired, expandable via mods) for enemies, items, and lore, tailored to world context (e.g., subterranean focus pulls underground creatures).
- **Clarification Prompts**: If DM input is vague (e.g., "add monsters"), AI asks: "What level of challenge? Environmental ties?"
- **Balance Checks**: Warns on potential issues (e.g., "This quest may be too deadly for new characters—adjust enemy stats?").
- **Homebrew Support**: Parses natural language for custom elements (e.g., "Add a flying predator"), integrating with combat customization tools.
- **Optimization**: Limits to low-compute tasks; complex simulations run offline.

### Technical Implementation
- **Godot Nodes**: Uses CanvasLayer for GUI overlays; Timeline as a custom Control node with GraphEdit for branching.
- **AI Backend**: Leverages the existing AI agent (from PRD) for NLP, with prep data stored as a Dictionary in the world's save file.
- **Performance**: Path visualizations use Line2D nodes; estimations via A* on the tilemap grid.
- **Edge Cases**: Handles uncreated characters by assuming defaults; supports multi-quest layering (e.g., overlapping arcs in the same city).

This system empowers DMs to craft cohesive experiences, blending creativity with AI efficiency. If you'd like to expand on specific GUI mockups, add more examples (e.g., for a dungeon crawl), integrate with player character creation, or refine AI prompts, just let me know!

## Review Needed
Proposed para-type: resource. Assigned based on content/frontmatter (confidence ~70%). Do not move until reviewed.