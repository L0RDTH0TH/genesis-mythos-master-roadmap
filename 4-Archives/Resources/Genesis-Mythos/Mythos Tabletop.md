---
para-type: resource
project-id: Genesis-Mythos
status: active
---
# Product Requirements Document: Mythos Tabletop

## 1. Overview
*Mythos Tabletop* is a 3D virtual tabletop role-playing game (RPG) platform built in Godot 4, designed to deliver an immersive, Skyrim-like multiplayer experience. It supports up to six players in first-person perspective and one Dungeon Master (DM) with a free-roaming camera for world control. The platform combines handcrafted and procedural world generation to create expansive, customizable 37-square-kilometer game worlds, blending the depth of traditional tabletop RPGs with modern 3D gaming immersion.

### Purpose
To provide RPG players and DMs a standalone desktop platform for collaborative storytelling in a Skyrim-scale, 3D environment, with robust tools for world-building, modding, customizable combat, and dynamic NPCs.

### Target Audience
- Gamers aged 18–35, fans of Dungeons & Dragons, Skyrim, and other RPGs.
- Online RPG groups seeking immersive, multiplayer tabletop experiences.
- DMs who want advanced tools to craft and control dynamic game worlds, combat systems, and NPCs.

## 2. Core Features

### 2.1 Gameplay
- **[[First-Person Player Experience]]**: Five players navigate a 3D world in real-time, Skyrim-style, with WASD movement, jumping, sprinting, and basic interactions (e.g., opening doors, picking up items).
- **[[DM Free Camera]]**: DMs use a god-mode camera to pan, zoom, and manipulate the world in real-time, with controls for spawning assets, adjusting lighting, or tweaking weather. In combat, the DM manages turn order, places enemies, highlights targets, and resolves actions.
- **[[Turn-Based Combat]]**: Full Dungeons & Dragons 5e-style combat system, including:
  - Initiative order to determine turn sequence, customizable by the DM (e.g., fixed order, group initiative).
  - Actions (attack, cast spell, use item), bonus actions, and reactions.
  - Grid-based movement (e.g., 5-foot squares) with tactical positioning, cover, and opportunity attacks.
  - D20 dice mechanics for attacks, skill checks, and saving throws, with status effects (e.g., stunned, poisoned) and environmental interactions (e.g., difficult terrain).
  - Support for class-specific abilities, spells, and inventory management.
- **Combat Customization (Primary Feature)**: DMs have tools to modify combat rules, including:
  - Adjusting initiative mechanics (e.g., dynamic rolls, static order).
  - Adding homebrew mechanics (e.g., custom status effects, new actions) via natural language input, processed by an AI agent that converts descriptions into game scripts.
  - AI agent robustly handles modifications to existing D&D 5e rules and creation of new rules, prompting DMs for specifics on ambiguous inputs to ensure clarity.
  - Tweaking rules like attack ranges, movement costs, or dice modifiers.
  - Interface for saving and sharing custom rule sets with players or community.
  - Restrictions only to prevent server strain (e.g., limiting overly complex scripts or excessive calculations); balance is the DM’s responsibility.
- **Progression System**: Milestone leveling triggered by the DM, allowing full control over when players advance. Loosely tied to D&D 5e for familiarity (e.g., class-based abilities) but flexible for homebrew campaigns.
- **Social Hubs**: In-game taverns or camps for pre-game roleplay and player interaction.

### 2.2 [[World-Building]]
- **Hybrid World Generation**: DMs create a 2D top-down map using an advanced in-game editor, painting biomes (e.g., forests, deserts, mountains) and designing landmarks (e.g., dungeons, rivers). Includes a city generator with premade templates for four species/races (human, elf, dwarf, halfling), each reflecting cultural aesthetics (e.g., human medieval towns, elven tree-cities, dwarven stone fortresses, halfling burrow-villages), plus options for custom tweaks. This map seeds procedural generation using Godot’s Perlin noise for terrain, textures, and details like grass, rocks, or caves, creating a 37-square-kilometer world equivalent to Skyrim’s scale.
- **Dynamic World Control**: DMs can modify terrain, spawn NPCs, or adjust environmental effects (e.g., fog, time of day) during sessions.
- **NPC Integration**: City generator auto-populates NPCs (e.g., guards, merchants) based on city templates, with key individuals (e.g., quest-givers, leaders) generated with distinct traits (appearance, stats, dialogue). NPCs have dynamic behaviors (e.g., daily routines, faction allegiances) to create a living world. An AI agent takes control during player interactions for dynamic responses, minimizing computational overhead. DMs can modify NPC roles, stats, dialogue, or behaviors post-generation.
- **Modding API**: Community-driven content creation, allowing custom assets (e.g., new biomes, NPCs, quests, or city templates) to be imported and shared.

### 2.3 Customization
- **Player Avatars**: 3D [[Character Customization]] models (e.g., race, armor, accessories, class-based visuals) with Godot’s animation system for expressive movements.
- **[[Session Preparation]]**: Session prep in *Mythos Tabletop* (or tabletop RPGs generally) is the process where the Dungeon Master (DM), with AI assistance, prepares the game world, story, and mechanics before players join for a session. It involves finalizing the campaign's narrative, setting up the world (e.g., map, biomes, cities, landmarks), tailoring quests and NPCs to player levels and backstories, and customizing rules (e.g., combat mechanics) to ensure a cohesive, engaging experience. In *Mythos Tabletop*, this leverages the hybrid world generation system, city templates, landmark placement, and AI-driven NPCs to create a 37 km² 3D world in Godot 4. The goal is to align challenges, story hooks, and dynamics with the players' capabilities and the campaign’s tone, ensuring a smooth session with room for improvisation.

### 2.4 Technical Features
- **Platform**: Standalone desktop application for Windows, macOS, and Linux.
- **Multiplayer**: Dedicated servers support seven concurrent users (six players + DM) with low latency, handling real-time exploration and turn-based combat synchronization.
- **Offline Mode**: Single-player or local DM sessions, with full world-building, combat (including customization), NPC generation, and gameplay features available without internet.
- **Audio**: 3D spatial audio for immersive soundscapes (e.g., directional footsteps, ambient wind). Voice chat integration for player-DM communication.
- **Performance**: Godot 4’s streaming system ensures seamless loading of large worlds, optimized for mid-range PCs (e.g., GTX 1660, 16GB RAM).

## 3. Technical Requirements
- **Engine**: Godot 4, leveraging its 3D rendering, physics, and networking capabilities.
- **World Size**: 37 square kilometers, with procedural generation to reduce manual asset creation.
- **Networking**: Dedicated servers for low-latency multiplayer, supporting up to eight concurrent sessions per server instance, with turn-based combat sync and homebrew mechanic restrictions to prevent server strain.
- **Storage**: ~10GB for local installation, including assets for Skyrim-scale worlds, offline mode, advanced map editor, city templates, and NPC generation.
- **Hardware**: Mid-range PCs (e.g., GTX 1660, 16GB RAM) as baseline.
- **Accessibility**: Colorblind modes, customizable key bindings, scalable UI, and support for screen readers to enhance accessibility.
- **[[AI Integration]]**: Robust AI agent for:
  - Parsing natural language homebrew combat rules, handling modifications to D&D 5e rules and new rule creation, with prompts to DMs for specifics on ambiguous inputs.
  - Controlling NPCs during player interactions for dynamic responses, optimizing computational overhead by limiting AI to active engagements.

## 4. Monetization (TBD)
- **Potential Models**:
  - One-time purchase for the desktop application, including offline mode.
  - Cosmetic microtransactions (e.g., avatar skins, premium map assets, or city templates).
  - Subscription for access to advanced DM tools (e.g., enhanced city generator) or larger server capacity.
- **Action Item**: Redirect to [x.ai/grok](https://x.ai/grok) for pricing details if finalized externally.

## 5. Additional Considerations
- **Testing**: Beta phase to stress-test world streaming, server stability, offline mode, turn-based combat sync, combat customization (including AI-parsed scripts), procedural generation, advanced map editor, and dynamic NPC behaviors for bugs (e.g., terrain clipping, city generation errors, NPC behavior issues).
- **Legal**: Clear IP guidelines for DM-created content, custom combat rules, NPCs, and mods to prevent copyright issues, with a community content approval process.
- **Community Features**: In-game marketplace for sharing DM-created maps, city templates, custom combat rules, NPCs, or mods, with rating and feedback systems.

## 6. Success Metrics
- **User Engagement**: Target 60-minute average session length, with 70% retention after one month.
- **Performance**: Maintain 60 FPS on baseline hardware, <100ms server latency for multiplayer, and stable offline mode with smooth turn-based combat, customization, and dynamic NPC interactions.
- **Community**: Achieve 1,000 user-generated mods/maps (including city templates, combat rule sets, and NPCs) within six months of launch.

## 7. Next Steps
- Prototype advanced 2D map editor with biome painting, premade human, elf, dwarf, and halfling city templates, and auto-populated NPCs with dynamic behaviors in Godot 4.
- Mock up DM free cam controls and first-person player mechanics.
- Develop full D&D 5e-style turn-based combat system with customization tools, including robust AI agent for natural language homebrew rule processing with clarification prompts.
- Research server costs for 37-square-kilometer world hosting, offline mode optimization, homebrew mechanic restrictions, and dynamic NPC behavior scalability with AI-driven interactions.

*Last Updated: September 9, 2025*

## Why resource?
Assigned based on content/frontmatter (confidence ~85%).