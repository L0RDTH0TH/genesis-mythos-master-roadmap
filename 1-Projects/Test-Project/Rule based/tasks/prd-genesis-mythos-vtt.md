# Product Requirements Document (PRD)

## 1. Introduction / Overview

### 1.1 Project Name

**Genesis Mythos VTT Generator (Prototype Vertical Slice)**

### 1.2 One‑Line Summary

Build an open‑source, aggressively modular **first‑person 3D virtual tabletop (VTT) generator** that procedurally creates living, collaborative open worlds from shared DM + player intents, with **pure first‑person immersion for players**, **Sparky‑style free‑cam + orthographic tabletop control for DMs**, and architecture designed for **endless community remixing**.

### 1.3 Scope for This PRD

This PRD defines a **vertical slice prototype** (6–9 month horizon) that:

- Targets **desktop PC** (Windows/Linux) as the primary platform.
- Assumes a **Godot‑based 3D implementation** (Godot 4+), but keeps most seams engine‑agnostic where reasonable.
- Integrates a **“Free 5e”‑style ruleset** as the first rulesystem plugin.
- Prioritizes **immersive first‑person feel and perspective split polish** over simulation depth or content volume.

The goal is to ship a **playable, end‑to‑end loop**: generate a small world from intents → explore in first person as a player → command as DM with free‑cam + orthographic tabletop → iterate via re‑generation of regions, with basic rules and combat hooks.

## 2. Goals

1. **Vertical Slice, Not Full Platform**
   - Deliver a constrained, but end‑to‑end experience: world generation, first‑person exploration, DM control, and one integrated ruleset.
2. **First‑Person Immersion for Players**
   - Players experience the world **only** in first‑person, with responsive movement, interaction, and audiovisual feedback that feels like “being there,” not watching a board.
3. **DM Command Mastery via Perspective Split**
   - DMs can seamlessly switch between a **Sparky‑style free‑flight god‑view** and a **precise orthographic tabletop view** for tactical control.
4. **Intent‑Driven Procedural Worldgen**
   - DM + player “intent inputs” (seeds, lore snippets, preferences) feed a modular generation pipeline to produce small, but **meaningfully reactive** worlds.
5. **Modularity and Open‑Source Extensibility**
   - Architect clear seams (generation stages, rules plugins, simulation modules) so community contributors can swap or extend behavior without forking the whole engine.
6. **Free 5e Ruleset Integration**
   - Integrate an open, SRD‑compatible, “Free 5e” ruleset as a plugin that drives basic combat, checks, and encounters within the world.
7. **Traceable, Regenerable Worlds**
   - Every generated world (or region) is reproducible from seeds + intents, with explicit re‑generation for major structural changes.

## 3. User Stories

### 3.1 DMs

1. **World Generation from Intents**
   - As a **DM**, I want to input a seed, a few lore hooks, and ruleset preferences so that the system generates a small, coherent world region I can use for a campaign session.
2. **God‑View Exploration**
   - As a **DM**, I want to fly around the world in a free‑cam god‑view so that I can quickly inspect locations, NPCs, and encounters before and during play.
3. **Tabletop Tactical Mode**
   - As a **DM**, I want to switch to a top‑down orthographic tabletop view so that I can precisely position tokens, measure movement, and run tactical combat.
4. **Live Session Tweaks**
   - As a **DM**, I want to make small, in‑session adjustments (move tokens, tweak weather, spawn an encounter) without triggering full re‑generation so that I can react to players fluidly.
5. **Deliberate Re‑Generation**
   - As a **DM**, I want to explicitly choose when to re‑generate a region or world with different parameters so that major structural changes are intentional and explainable.

### 3.2 Players

6. **Immersive First‑Person Exploration**
   - As a **player**, I want to explore the world exclusively in first‑person so that I feel like I inhabit my character, not a token on a board.
7. **Smooth Movement and Interaction**
   - As a **player**, I want responsive movement (WASD + mouse look) and clear interaction prompts so that exploration and interaction feel intuitive and satisfying.
8. **Rules‑Aware Encounters**
   - As a **player**, I want combat and checks to follow a recognizable 5e‑style ruleset so that I understand what my character can do and how risk/reward works.

### 3.3 Modders / Contributors

9. **Replaceable Generation Stages**
   - As a **modder**, I want to plug in alternate biome or settlement generators so that I can create custom flavors of worlds without rewriting the core engine.
10. **Rules Plugins**
    - As a **modder**, I want to define new rules plugins (beyond Free 5e) so that I can run different RPG systems on the same worldgen and perspective split.

## 4. Functional Requirements

### 4.1 World Generation & Intent Pipeline

1. The system must accept a **world seed** and a set of **DM/player intents** (e.g., text fields describing key themes, factions, or hooks).
2. The system must run a **modular generation pipeline** with at least these stages:
   - Seed parsing
   - Terrain layout (heightmap / navmesh‑friendly geometry)
   - Biome placement (e.g., forest, plains, mountains)
   - Points of Interest (POIs) placement (settlements, dungeons, landmarks)
   - Entity placement (NPCs, creatures, interactable objects)
3. The pipeline must allow each stage to be implemented as a **swappable module** (e.g., Godot scripts implementing a shared interface).
4. The system must associate generated content with the inputs that shaped it (e.g., which intent, which rules plugin) for later inspection.

### 4.2 Simulation Skeleton (Vertical Slice)

5. The system must provide a **basic simulation loop** that updates:
   - Time of day / lighting
   - Simple weather states (clear, rain, fog) that affect visuals
   - Minimal NPC schedules (e.g., idle, walk between a few waypoints)
6. The simulation must be **decoupled from rendering**, so that stepping the simulation is not tied to frame rate.

### 4.3 First‑Person Player Perspective

7. The system must provide a **first‑person player controller** with:
   - WASD movement, mouse look, and configurable sensitivity.
   - Jump and basic collision with the environment.
8. The player camera must **always remain in first‑person** during normal play (no third‑person or overhead view for players).
9. The system must support **basic interaction** via raycast (e.g., look at interactive object + key press).

### 4.4 DM Free‑Cam & Orthographic Tabletop View

10. The system must provide a **DM free‑cam controller** allowing:
    - Flight (up/down/left/right/forward/back)
    - Orbiting and smooth panning/tilting
11. The system must provide a **DM orthographic tabletop view** that:
    - Shows the relevant combat area from above with a fixed orthographic camera.
    - Allows grid overlay and precise token positioning.
12. The system must implement a **camera rig abstraction** that:
    - Shares a unified world/scene graph.
    - Supports multiple camera modes (player first‑person, DM free‑cam, DM orthographic) as interchangeable rigs.
13. The system must provide **smooth camera transitions** (interpolation of position, rotation, FOV) when switching between DM views.

### 4.5 Free 5e Ruleset Integration

14. The system must load and expose a **Free 5e ruleset plugin** that defines:
    - Core stats (abilities, HP, AC, etc.).
    - Basic actions (attack, move, dash, cast simple spells).
    - Simple encounter resolution (attack roll, damage, save, success/fail outcomes).
15. The rules plugin must operate on **abstract entities** (characters, NPCs, monsters) that are mapped to world entities.
16. The system must provide a minimal **combat loop**:
    - Initiative order
    - Turn taking
    - Movement + action resolution in the orthographic view.

### 4.6 Session Controls and Re‑Generation

17. The DM must be able to trigger:
    - **Minor live tweens** (e.g., reposition a token, toggle weather state).
    - **Explicit region/world re‑generation**, which re‑runs part or all of the generation pipeline with updated seeds/intents.
18. The system must capture **snapshots** of parameters for each generation run so that a world or region can be reproduced later.

### 4.7 Modularity & Extensibility

19. The system must expose **clear extension points** for:
    - New world generation stages.
    - New rules plugins.
    - New simulation behaviors.
20. Extension points must be documented with **interfaces/contracts** (e.g., Godot script interfaces, signals) rather than requiring invasive core edits.

## 5. Non‑Goals (Out of Scope for This Vertical Slice)

1. Full‑scale MMO‑style networking or persistent multi‑server architecture.
2. Rich narrative authoring tools (quest graph editors, dialogue trees) beyond basic hooks.
3. Rich content libraries (hundreds of monsters/biomes); vertical slice will use a **small, curated set**.
4. VR/AR support in the prototype (designs may keep this possible, but it is not required).
5. Cross‑platform mobile deployment (Android/iOS).
6. Comprehensive ruleset coverage for all 5e content; focus is on a **minimal, Free‑5e‑aligned subset**.

## 6. Design Considerations

1. **Visual Style**
   - Prioritize clarity and performance over fidelity (e.g., stylized low‑poly or mid‑poly art).
   - Ensure that the orthographic view remains readable at typical zoom levels.
2. **UX for Role Separation**
   - Provide clear affordances for which role is active (Player vs DM).
   - Guard rails to avoid players accidentally entering DM‑only views.
3. **Godot‑Friendly Architecture**
   - Use Godot scenes/nodes for world entities, but keep simulation and rules logic in separate modules/classes where possible.
   - Use signals to decouple events (combat start, world regenerated, etc.).

## 7. Technical Considerations

1. **Engine & Language**
   - Primary assumption: **Godot 4+** with GDScript or C# for gameplay and systems.
2. **Scene Graph & Cameras**
   - Single world scene graph with:
     - Player camera + controller.
     - DM free‑cam camera + controller.
     - DM orthographic camera.
3. **Data & Seeds**
   - Configurable JSON/YAML for generation parameters and Free 5e rules data (e.g., SRD stat blocks).
4. **Performance**
   - The vertical slice should run smoothly on a **mid‑range gaming PC** at 1080p with modest graphics settings.

## 8. Success Metrics

1. A DM can, within 10–15 minutes:
   - Provide a seed + a few text intents.
   - Generate a small world region.
   - Inspect it in free‑cam.
   - Run at least one short encounter in orthographic tabletop mode using the Free 5e rules.
2. A player can:
   - Join a session.
   - Explore a portion of the world in first‑person.
   - Participate in at least one basic combat encounter.
3. A contributor can:
   - Swap a biome/terrain generator or add a simple rules plugin with **no changes to core engine files**, using documented seams.

## 9. Open Questions

1. How much of the Free 5e ruleset should be included in the first pass (e.g., only basic combat vs. spells, conditions, etc.)?
2. What minimum viable set of biomes and POIs are required for the slice to feel “alive” but still achievable?
3. What, if any, session persistence (saving/loading) is needed for the prototype versus ephemeral sessions?
4. How far should we go with AI‑assisted intent parsing (pure text vs. structured form inputs) in this first slice?

