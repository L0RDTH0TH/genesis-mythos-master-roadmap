---
proposal_path: Ingest/Decisions/Decision-for-task-test--2026-03-04-0440.md
---
## TL;DR
{

---

{

"metadata": {

"version": "2.0",

"description": "Mythos Tabletop Task Dependency Graph - Organized by category and hierarchy",

"last_updated": "2025-10-22"

},

"nodes": [

{

"id": "player_systems",

"label": "Player Systems",

"type": "category",

"level": 0

},

{

"id": "char_creation",

"label": "Character Creation",

"type": "task",

"parent": "player_systems",

"level": 1,

"description": "Design and implement character customization system with appearance, class, equipment, and roleplay elements"

},

{

"id": "char_appearance",

"label": "Character Appearance Customization",

"type": "subtask",

"parent": "char_creation",

"level": 2,

"description": "Implement race selection (Human, Elf, Dwarf, Halfling), body customization (height, build, age), face details, hair styles, skin tones, and procedural textures"

},

{

"id": "char_class",

"label": "Character Class System",

"type": "subtask",

"parent": "char_creation",

"level": 2,

"description": "Implement D&D 5e-inspired classes (Fighter, Wizard, Rogue, Cleric, Paladin, Ranger, Druid) with visual themes, stat seeding, and ability pools"

},

{

"id": "char_equipment",

"label": "Equipment Customization",

"type": "subtask",

"parent": "char_creation",

"level": 2,

"description": "Implement equipment slots (head, torso, legs, hands, feet, weapon, shield, accessories) with armor types, weapons, material swaps, and dynamic updates"

},

{

"id": "char_roleplay",

"label": "Roleplay Customization",

"type": "subtask",

"parent": "char_creation",

"level": 2,

"description": "Implement ceremonial outfits, emotes, animations, voice sets, and backstory hooks for character personality"

},

{

"id": "fp_gameplay",

"label": "First-Person Player Experience",

"type": "task",

"parent": "player_systems",

"level": 1,

"description": "Implement first-person exploration, interaction, and immersion mechanics for 3D world navigation"

},

{

"id": "fp_movement",

"label": "First-Person Movement & Controls",

"type": "subtask",

"parent": "fp_gameplay",

"level": 2,

"description": "Implement WASD movement, mouse camera control, jumping, sprinting, crouching, and biome-based movement modifiers"

},

{

"id": "fp_interaction",

"label": "World Interaction System",

"type": "subtask",

"parent": "fp_gameplay",

"level": 2,

"description": "Implement landmark engagement, NPC dialogue, resource gathering, inventory interaction, and environmental feedback"

},

{

"id": "fp_cities",

"label": "City Exploration & NPCs",

"type": "subtask",

"parent": "fp_gameplay",

"level": 2,

"description": "Implement city navigation, NPC behaviors, dialogue trees, quest generation, and dynamic NPC engagement"

},

{

"id": "fp_social",

"label": "Social Hubs & Roleplay",

"type": "subtask",

"parent": "fp_gameplay",

"level": 2,

"description": "Implement social hub areas, emotes, voice/text chat, roleplay prompts, and party dynamics visualization"

},

{

"id": "combat_system",

"label": "Turn-Based Combat",

"type": "task",

"parent": "player_systems",

"level": 1,

"description": "Implement D&D 5e-inspired turn-based combat with grid-based movement, actions, and tactical positioning"

},

{

"id": "combat_initiative",

"label": "Initiative & Turn Order",

"type": "subtask",

"parent": "combat_system",

"level": 2,

"description": "Implement d20 + Dexterity initiative rolls, turn order tracking, surprise rounds, and DM customization options"

},

{

"id": "combat_actions",

"label": "Actions & Combat Flow",

"type": "subtask",

"parent": "combat_system",

"level": 2,

"description": "Implement standard actions, bonus actions, reactions, movement mechanics, and action resolution (attacks, spells, saves)"

},

{

"id": "combat_grid",

"label": "Grid-Based Movement & Positioning",

"type": "subtask",

"parent": "combat_system",

"level": 2,

"description": "Implement 5-foot grid overlay, cover mechanics, flanking, opportunity attacks, and A* pathfinding for movement"

},

{

"id": "combat_dice",

"label": "Dice Mechanics & Rolls",

"type": "subtask",

"parent": "combat_system",

"level": 2,

"description": "Implement d20 rolls for attacks/skills/saves, advantage/disadvantage, critical hits/misses, and DM overrides"

},

{

"id": "dm_systems",

"label": "DM Systems",

"type": "category",

"level": 0

},

{

"id": "dm_camera",

"label": "DM Free Camera",

"type": "task",

"parent": "dm_systems",

"level": 1,

"description": "Implement god-mode camera system for DM world oversight and real-time manipulation"

},

{

"id": "dm_camera_nav",

"label": "Camera Navigation & Flight",

"type": "subtask",

"parent": "dm_camera",

"level": 2,

"description": "Implement Halo-inspired hover flight (WASD, space/shift for vertical), boost mechanic, teleportation, and speed modifiers"

},

{

"id": "dm_camera_tools",

"label": "World Manipulation Tools",

"type": "subtask",

"parent": "dm_camera",

"level": 2,

"description": "Implement asset spawning, environmental adjustments (lighting, weather, terrain), scripted events, and undo/redo support"

},

{

"id": "dm_camera_visibility",

"label": "Visibility & Overlay Options",

"type": "subtask",

"parent": "dm_camera",

"level": 2,

"description": "Implement layer toggles, annotations, multi-view support, and colorblind-friendly overlays"

},

{

"id": "dm_camera_combat",

"label": "Combat Mode Integration",

"type": "subtask",

"parent": "dm_camera",

"level": 2,

"description": "Implement turn management, enemy placement, action resolution tools, range/AoE visualization, and status tracking"

},

{

"id": "session_prep",

"label": "Session Preparation",

"type": "task",

"parent": "dm_systems",

"level": 1,

"description": "Implement AI-assisted pre-game planning system for quests, encounters, and narrative alignment"

},

{

"id": "session_prep_interface",

"label": "Session Prep Interface & GUI",

"type": "subtask",

"parent": "session_prep",

"level": 2,

"description": "Implement world overview, element selector, AI chat window, timeline GUI, map GUI, and resource browser"

},

{

"id": "session_prep_quest",

"label": "Quest Planning & Design",

"type": "subtask",

"parent": "session_prep",

"level": 2,

"description": "Implement quest creation, arc branching, encounter scaling, and unique quest customization"

},

{

"id": "session_prep_timeline",

"label": "Timeline & Event Sequencing",

"type": "subtask",

"parent": "session_prep",

"level": 2,

"description": "Implement draggable timeline nodes, branching paths, bullet-point editing, and event visualization"

},

{

"id": "session_prep_ai",

"label": "AI Assistant Integration",

"type": "subtask",

"parent": "session_prep",

"level": 2,

"description": "Implement NLP for suggestions, clarification prompts, balance checks, and homebrew support"

},

{

"id": "session_prep_path",

"label": "Path Visualization & Travel Estimation",

"type": "subtask",

"parent": "session_prep",

"level": 2,

"description": "Implement path overlays, travel time calculations, encounter simulation, and map-based planning"

},

{

"id": "gui",

"label": "GUI",

"type": "category",

"level": 0

},

{

"id": "fractal_framework",

"label": "Fractal GUI Framework",

"type": "task",

"parent": "gui",

"level": 1,

"description": "Implement core fractal wheel-based radial menu system with context-sensitivity and animations"

},

{

"id": "fractal_wheel",

"label": "Fractal Wheel Control",

"type": "subtask",

"parent": "fractal_framework",

"level": 2,

"description": "Implement circular radial menu with wedges, zoom animations, and hierarchical navigation"

},

{

"id": "fractal_viewport",

"label": "Viewport & Preview System",

"type": "subtask",

"parent": "fractal_framework",

"level": 2,

"description": "Implement real-time 3D/2D previews with LOD and dynamic updates"

},

{

"id": "fractal_prompts",

"label": "Prompts & Tooltips",

"type": "subtask",

"parent": "fractal_framework",

"level": 2,

"description": "Implement narrative prompts, tooltips with lore/mechanics, and context-sensitive hints"

},

{

"id": "fractal_ai",

"label": "AI Assistant Integration",

"type": "subtask",

"parent": "fractal_framework",

"level": 2,

"description": "Implement NLP parsing, suggestions, and AI-driven content generation"

},

{

"id": "char_custom_gui",

"label": "Character Customization GUI",

"type": "task",

"parent": "gui",

"level": 1,

"description": "Implement character creation interface with archetype-driven fractal wheel"

},

{

"id": "char_gui_workflow",

"label": "Character Creation Workflow",

"type": "subtask",

"parent": "char_custom_gui",

"level": 2,

"description": "Implement step-by-step narrative flow (story, role, backstory, stats, appearance)"

},

{

"id": "char_gui_archetype",

"label": "Archetype Color Wheel",

"type": "subtask",

"parent": "char_custom_gui",

"level": 2,

"description": "Implement archetype quadrants with color-coded navigation and class suggestions"

},

{

"id": "char_gui_customization",

"label": "Appearance & Equipment UI",

"type": "subtask",

"parent": "char_custom_gui",

"level": 2,

"description": "Implement sliders, color pickers, equipment palette, and real-time model updates"

},

{

"id": "city_gen_gui",

"label": "City Generation GUI",

"type": "task",

"parent": "gui",

"level": 1,

"description": "Implement city creation interface with race templates and procedural generation controls"

},

{

"id": "city_gui_wheel",

"label": "City Fractal Wheel",

"type": "subtask",

"parent": "city_gen_gui",

"level": 2,

"description": "Implement city-specific wheel with Template, Layout, Population, and Customize quadrants"

},

{

"id": "city_gui_preview",

"label": "City Preview & Viewport",

"type": "subtask",

"parent": "city_gen_gui",

"level": 2,

"description": "Implement real-time city rendering with procedural generation visualization"

},

{

"id": "city_gui_tools",

"label": "City Editing Tools",

"type": "subtask",

"parent": "city_gen_gui",

"level": 2,

"description": "Implement metadata sliders, sub-tile palette, brush tools, and procedural generation buttons"

},

{

"id": "world_overview_gui",

"label": "World Overview GUI",

"type": "task",

"parent": "gui",

"level": 1,

"description": "Implement session prep fractal wheel menu for quest planning and world editing"

},

{

"id": "world_overview_wheel",

"label": "Session Prep Fractal Wheel",

"type": "subtask",

"parent": "world_overview_gui",

"level": 2,

"description": "Implement context-sensitive wheel with Quest Creation, Element Editing, Timeline, Map Visualization, AI Collaboration, and Resource Browser"

},

{

"id": "world_overview_context",

"label": "Context-Sensitive Menus",

"type": "subtask",

"parent": "world_overview_gui",

"level": 2,

"description": "Implement dynamic menu adaptation based on selected world elements (cities, landmarks, NPCs)"

},

{

"id": "world_building_gui",

"label": "World Building GUI",

"type": "task",

"parent": "gui",

"level": 1,

"description": "Implement world-building fractal wheel with Terrain, Rulings, Factions, and Narrative quadrants"

},

{

"id": "world_build_terrain",

"label": "Terrain Quadrant",

"type": "subtask",

"parent": "world_building_gui",

"level": 2,

"description": "Implement biome painting, landmark placement, void editing, elevation/texture tools, and procedural seeds"

},

{

"id": "world_build_rulings",

"label": "Rulings Quadrant",

"type": "subtask",

"parent": "world_building_gui",

"level": 2,

"description": "Implement combat rules, progression system, homebrew mechanics, environmental interactions, and restrictions"

},

{

"id": "world_build_factions",

"label": "Factions Quadrant",

"type": "subtask",

"parent": "world_building_gui",

"level": 2,

"description": "Implement race/city templates, NPC generation, alliances/conflicts, quest hooks, and economy/resources"

},

{

"id": "world_build_narrative",

"label": "Narrative Quadrant",

"type": "subtask",

"parent": "world_building_gui",

"level": 2,

"description": "Implement backstory/lore generation, quests/events, artifacts/secrets, weather/cycles, and mod integration"

},

{

"id": "backend_systems",

"label": "Backend Systems",

"type": "category",

"level": 0

},

{

"id": "char_data_backend",

"label": "Character Data Management",

"type": "task",

"parent": "backend_systems",

"level": 1,

"description": "Implement character profile persistence, validation, and multiplayer synchronization"

},

{

"id": "char_profile",

"label": "Character Profile Management",

"type": "subtask",

"parent": "char_data_backend",

"level": 2,

"description": "Implement JSON serialization for character profiles, save/load functionality, and profile versioning"

},

{

"id": "char_networking",

"label": "Character Networking Sync",

"type": "subtask",

"parent": "char_data_backend",

"level": 2,

"description": "Implement multiplayer sync for character customization changes, DM approval workflows, and delta updates"

},

{

"id": "char_validation",

"label": "Character Validation & Rules",

"type": "subtask",

"parent": "char_data_backend",

"level": 2,

"description": "Implement race-class compatibility checks, DM-enforced restrictions, and homebrew approval system"

},

{

"id": "world_data_backend",

"label": "World Data Management",

"type": "task",

"parent": "backend_systems",

"level": 1,

"description": "Implement world map serialization, biome/landmark data persistence, and procedural generation seeding"

},

{

"id": "world_serialization",

"label": "World Map Serialization",

"type": "subtask",

"parent": "world_data_backend",

"level": 2,

"description": "Implement JSON serialization for section placement, sub-tile biomes, landmarks, and void types"

},

{

"id": "biome_data",

"label": "Biome & Terrain Data",

"type": "subtask",

"parent": "world_data_backend",

"level": 2,

"description": "Implement biome metadata (elevation, vegetation density, water presence), texture mapping, and procedural generation parameters"

},

{

"id": "landmark_data",

"label": "Landmark Data Management",

"type": "subtask",

"parent": "world_data_backend",

"level": 2,

"description": "Implement landmark placement, properties, customization, and linking across sections"

},

{

"id": "npc_backend",

"label": "NPC & Entity Management",

"type": "task",

"parent": "backend_systems",

"level": 1,

"description": "Implement NPC generation, behavior systems, dialogue state, and dynamic interaction tracking"

},

{

"id": "npc_generation",

"label": "NPC Generation & Pooling",

"type": "subtask",

"parent": "npc_backend",

"level": 2,

"description": "Implement procedural NPC creation from templates, stat generation, trait assignment, and NPC pool management"

},

{

"id": "npc_behaviors",

"label": "NPC Behavior & Routines",

"type": "subtask",

"parent": "npc_backend",

"level": 2,

"description": "Implement daily routines, movement patterns, faction relationships, and dynamic state tracking"

},

{

"id": "npc_dialogue",

"label": "NPC Dialogue & Interaction",

"type": "subtask",

"parent": "npc_backend",

"level": 2,

"description": "Implement dialogue state management, interaction history, quest tracking, and player relationship tracking"

},

{

"id": "combat_backend",

"label": "Combat System Backend",

"type": "task",

"parent": "backend_systems",

"level": 1,

"description": "Implement combat state management, rule execution, dice mechanics, and status effect tracking"

},

{

"id": "combat_state",

"label": "Combat State Management",

"type": "subtask",

"parent": "combat_backend",

"level": 2,

"description": "Implement turn order tracking, initiative calculations, combat phase management, and round sequencing"

},

{

"id": "combat_rules_engine",

"label": "Combat Rules Engine",

"type": "subtask",

"parent": "combat_backend",

"level": 2,

"description": "Implement D&D 5e rule execution, action resolution, damage calculations, and saving throw mechanics"

},

{

"id": "status_effects",

"label": "Status Effects & Conditions",

"type": "subtask",

"parent": "combat_backend",

"level": 2,

"description": "Implement status effect creation, duration tracking, stacking logic, and mechanical application"

},

{

"id": "dice_system",

"label": "Dice Rolling & RNG",

"type": "subtask",

"parent": "combat_backend",

"level": 2,

"description": "Implement d20 rolls, advantage/disadvantage, critical hits/misses, and seeded randomization for reproducibility"

},

{

"id": "ai_backend",

"label": "AI Integration Backend",

"type": "task",

"parent": "backend_systems",

"level": 1,

"description": "Implement AI interpreter, NLP parsing, content generation, and MCP server integration"

},

{

"id": "ai_interpreter",

"label": "Natural Language Interpreter",

"type": "subtask",

"parent": "ai_backend",

"level": 2,

"description": "Implement NLP parsing for DM input, intent extraction, and structured data conversion for combat rules and world modifications"

},

{

"id": "ai_content_gen",

"label": "AI Content Generation",

"type": "subtask",

"parent": "ai_backend",

"level": 2,

"description": "Implement NPC dialogue generation, quest narrative creation, backstory generation, and environmental storytelling"

},

{

"id": "mcp_integration",

"label": "MCP Server Integration",

"type": "subtask",

"parent": "ai_backend",

"level": 2,

"description": "Implement MCP bridges for combat rules, world building, and session management; handle structured data routing"

},

{

"id": "session_backend",

"label": "Session & Game State Management",

"type": "task",

"parent": "backend_systems",

"level": 1,

"description": "Implement session persistence, game state tracking, save/load functionality, and multiplayer synchronization"

},

{

"id": "session_persistence",

"label": "Session Save/Load System",

"type": "subtask",

"parent": "session_backend",

"level": 2,

"description": "Implement JSON serialization for session state, checkpoint creation, and session recovery"

},

{

"id": "game_state",

"label": "Game State Tracking",

"type": "subtask",

"parent": "session_backend",

"level": 2,

"description": "Implement player positions, inventory state, quest progress, NPC states, and world modifications tracking"

},

{

"id": "multiplayer_sync",

"label": "Multiplayer Synchronization",

"type": "subtask",

"parent": "session_backend",

"level": 2,

"description": "Implement server-authoritative state updates, delta syncing, conflict resolution, and latency compensation"

},

{

"id": "procedural_backend",

"label": "Procedural Generation Backend",

"type": "task",

"parent": "backend_systems",

"level": 1,

"description": "Implement Perlin noise seeding, terrain generation, asset placement, and LOD management"

},

{

"id": "perlin_noise",

"label": "Perlin Noise & Seeding",

"type": "subtask",

"parent": "procedural_backend",

"level": 2,

"description": "Implement noise parameter seeding from map data, frequency/amplitude control, and reproducible generation"

},

{

"id": "terrain_generation",

"label": "Terrain & Texture Generation",

"type": "subtask",

"parent": "procedural_backend",

"level": 2,

"description": "Implement elevation maps, biome-specific textures, blending at boundaries, and detail layer generation"

},

{

"id": "asset_placement",

"label": "Procedural Asset Placement",

"type": "subtask",

"parent": "procedural_backend",

"level": 2,

"description": "Implement tree/rock/cave placement, density control, biome-specific variations, and collision generation"

},

{

"id": "lod_system",

"label": "Level of Detail Management",

"type": "subtask",

"parent": "procedural_backend",

"level": 2,

"description": "Implement LOD transitions, terrain mesh simplification, asset culling, and streaming optimization"

},

{

"id": "networking_backend",

"label": "Networking & Server Infrastructure",

"type": "task",

"parent": "backend_systems",

"level": 1,

"description": "Implement multiplayer networking, server management, offline mode support, and connection handling"

},

{

"id": "multiplayer_network",

"label": "Multiplayer Networking",

"type": "subtask",

"parent": "networking_backend",

"level": 2,

"description": "Implement Godot's High-Level Multiplayer API, RPC systems, player synchronization, and latency handling"

},

{

"id": "server_management",

"label": "Server Management & Hosting",

"type": "subtask",

"parent": "networking_backend",

"level": 2,

"description": "Implement server instance creation, player lobby management, session hosting, and connection validation"

},

{

"id": "offline_mode",

"label": "Offline Mode Support",

"type": "subtask",

"parent": "networking_backend",

"level": 2,

"description": "Implement local game state management, single-player session handling, and offline-to-online sync"

}

],

"edges": [

{

"source": "char_appearance",

"target": "char_creation",

"label": "part_of"

},

{

"source": "char_class",

"target": "char_creation",

"label": "part_of"

},

{

"source": "char_equipment",

"target": "char_creation",

"label": "part_of"

},

{

"source": "char_roleplay",

"target": "char_creation",

"label": "part_of"

},

{

"source": "char_creation",

"target": "char_data_backend",

"label": "depends_on"

},

{

"source": "char_profile",

"target": "char_data_backend",

"label": "part_of"

},

{

"source": "char_networking",

"target": "char_data_backend",

"label": "part_of"

},

{

"source": "char_validation",

"target": "char_data_backend",

"label": "part_of"

},

{

"source": "fp_movement",

"target": "fp_gameplay",

"label": "part_of"

},

{

"source": "fp_interaction",

"target": "fp_gameplay",

"label": "part_of"

},

{

"source": "fp_cities",

"target": "fp_gameplay",

"label": "part_of"

},

{

"source": "fp_social",

"target": "fp_gameplay",

"label": "part_of"

},

{

"source": "combat_initiative",

"target": "combat_system",

"label": "part_of"

},

{

"source": "combat_actions",

"target": "combat_system",

"label": "part_of"

},

{

"source": "combat_grid",

"target": "combat_system",

"label": "part_of"

},

{

"source": "combat_dice",

"target": "combat_system",

"label": "part_of"

},

{

"source": "fp_gameplay",

"target": "combat_system",

"label": "transitions_to"

},

{

"source": "dm_camera_nav",

"target": "dm_camera",

"label": "part_of"

},

{

"source": "dm_camera_tools",

"target": "dm_camera",

"label": "part_of"

},

{

"source": "dm_camera_visibility",

"target": "dm_camera",

"label": "part_of"

},

{

"source": "dm_camera_combat",

"target": "dm_camera",

"label": "part_of"

},

{

"source": "session_prep_interface",

"target": "session_prep",

"label": "part_of"

},

{

"source": "session_prep_quest",

"target": "session_prep",

"label": "part_of"

},

{

"source": "session_prep_timeline",

"target": "session_prep",

"label": "part_of"

},

{

"source": "session_prep_ai",

"target": "session_prep",

"label": "part_of"

},

{

"source": "session_prep_path",

"target": "session_prep",

"label": "part_of"

},

{

"source": "session_prep",

"target": "dm_camera",

"label": "informs"

},

{

"source": "fractal_wheel",

"target": "fractal_framework",

"label": "part_of"

},

{

"source": "fractal_viewport",

"target": "fractal_framework",

"label": "part_of"

},

{

"source": "fractal_prompts",

"target": "fractal_framework",

"label": "part_of"

},

{

"source": "fractal_ai",

"target": "fractal_framework",

"label": "part_of"

},

{

"source": "char_gui_workflow",

"target": "char_custom_gui",

"label": "part_of"

},

{

"source": "char_gui_archetype",

"target": "char_custom_gui",

"label": "part_of"

},

{

"source": "char_gui_customization",

"target": "char_custom_gui",

"label": "part_of"

},

{

"source": "char_custom_gui",

"target": "fractal_framework",

"label": "extends"

},

{

"source": "city_gui_wheel",

"target": "city_gen_gui",

"label": "part_of"

},

{

"source": "city_gui_preview",

"target": "city_gen_gui",

"label": "part_of"

},

{

"source": "city_gui_tools",

"target": "city_gen_gui",

"label": "part_of"

},

{

"source": "city_gen_gui",

"target": "fractal_framework",

"label": "extends"

},

{

"source": "world_overview_wheel",

"target": "world_overview_gui",

"label": "part_of"

},

{

"source": "world_overview_context",

"target": "world_overview_gui",

"label": "part_of"

},

{

"source": "world_overview_gui",

"target": "fractal_framework",

"label": "extends"

},

{

"source": "world_build_terrain",

"target": "world_building_gui",

"label": "part_of"

},

{

"source": "world_build_rulings",

"target": "world_building_gui",

"label": "part_of"

},

{

"source": "world_build_factions",

"target": "world_building_gui",

"label": "part_of"

},

{

"source": "world_build_narrative",

"target": "world_building_gui",

"label": "part_of"

},

{

"source": "world_building_gui",

"target": "fractal_framework",

"label": "extends"

},

{

"source": "world_serialization",

"target": "world_data_backend",

"label": "part_of"

},

{

"source": "biome_data",

"target": "world_data_backend",

"label": "part_of"

},

{

"source": "landmark_data",

"target": "world_data_backend",

"label": "part_of"

},

{

"source": "npc_generation",

"target": "npc_backend",

"label": "part_of"

},

{

"source": "npc_behaviors",

"target": "npc_backend",

"label": "part_of"

},

{

"source": "npc_dialogue",

"target": "npc_backend",

"label": "part_of"

},

{

"source": "combat_state",

"target": "combat_backend",

"label": "part_of"

},

{

"source": "combat_rules_engine",

"target": "combat_backend",

"label": "part_of"

},

{

"source": "status_effects",

"target": "combat_backend",

"label": "part_of"

},

{

"source": "dice_system",

"target": "combat_backend",

"label": "part_of"

},

{

"source": "ai_interpreter",

"target": "ai_backend",

"label": "part_of"

},

{

"source": "ai_content_gen",

"target": "ai_backend",

"label": "part_of"

},

{

"source": "mcp_integration",

"target": "ai_backend",

"label": "part_of"

},

{

"source": "session_persistence",

"target": "session_backend",

"label": "part_of"

},

{

"source": "game_state",

"target": "session_backend",

"label": "part_of"

},

{

"source": "multiplayer_sync",

"target": "session_backend",

"label": "part_of"

},

{

"source": "perlin_noise",

"target": "procedural_backend",

"label": "part_of"

},

{

"source": "terrain_generation",

"target": "procedural_backend",

"label": "part_of"

},

{

"source": "asset_placement",

"target": "procedural_backend",

"label": "part_of"

},

{

"source": "lod_system",

"target": "procedural_backend",

"label": "part_of"

},

{

"source": "multiplayer_network",

"target": "networking_backend",

"label": "part_of"

},

{

"source": "server_management",

"target": "networking_backend",

"label": "part_of"

},

{

"source": "offline_mode",

"target": "networking_backend",

"label": "part_of"

},

{

"source": "world_data_backend",

"target": "procedural_backend",

"label": "feeds_into"

},

{

"source": "combat_backend",

"target": "ai_backend",

"label": "uses"

},

{

"source": "npc_backend",

"target": "ai_backend",

"label": "uses"

},

{

"source": "session_backend",

"target": "multiplayer_sync",

"label": "depends_on"

}

]

}

## Review Needed
Proposed para-type: area. Assigned based on content/frontmatter (confidence ~70%). Do not move until reviewed.