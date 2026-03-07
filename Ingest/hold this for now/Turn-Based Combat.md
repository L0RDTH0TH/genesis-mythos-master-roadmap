---
proposal_path: Ingest/Decisions/Decision-for-turn-based-combat--2026-03-04-0437.md
---
# Turn-Based Combat System for Mythos Tabletop

## Overview

The Turn-Based Combat System for _Mythos Tabletop_ is a robust, Dungeons & Dragons 5e-inspired framework designed to deliver tactical, engaging combat within a 3D virtual tabletop RPG built in Godot 4.x. It supports up to six players in first-person perspective and one Dungeon Master (DM) with a free-roaming camera, integrating seamlessly with the hybrid world generation and map editor systems. The system emphasizes flexibility, allowing DMs to customize rules, mechanics, and scenarios while maintaining performance for large-scale, 37-square-kilometer worlds. Combat is grid-based, tactical, and supports D&D 5e mechanics (initiative, actions, d20 dice rolls) alongside a powerful AI-driven customization tool that processes natural language inputs to create or modify rules.

## 1. Core Mechanics

The combat system is turn-based, operating on a 5-foot square grid overlaid on the 3D world, with seamless integration into the section (500 m × 500 m) and sub-tile (50 m × 50 m) framework of the world map. It balances D&D 5e fidelity with flexibility for homebrew campaigns.

### 1.1 Initiative and Turn Order

- **Initiative Mechanics**:
    
    - Default: Each participant (players, NPCs, enemies) rolls a d20 + Dexterity modifier to determine turn order, as per D&D 5e. DM can override with fixed order or group initiative (e.g., all enemies act together).
        
    - Customization: DMs adjust initiative via a UI panel:
        
        - Options: Dynamic rolls (re-rolled each round), static order (set manually), group initiative (players vs. enemies), or hybrid (e.g., players roll, enemies use fixed order).
            
        - Sliders for modifiers (e.g., +2 to initiative for specific classes or conditions).
            
    - UI: Displays a vertical initiative tracker on-screen, showing current turn, upcoming turns, and status effects (e.g., "stunned, skips turn"). DM can drag to reorder manually.
        
- **Surprise Rounds**: DM can initiate surprise rounds, granting free actions to specific participants based on narrative or stealth checks (e.g., d20 + Stealth vs. Perception).
    

### 1.2 Actions and Combat Flow

- **Action Types** (per D&D 5e):
    
    - **Standard Action**: Attack (melee/ranged), cast a spell, use an item, disengage, dodge, dash, or interact with objects (e.g., open door, pull lever).
        
    - **Bonus Action**: Class-specific abilities (e.g., Rogue’s Cunning Action), off-hand attacks, or quick spells (e.g., Healing Word).
        
    - **Reaction**: Opportunity attacks, counterspells, or triggered abilities (e.g., Shield spell).
        
    - **Movement**: Up to character’s speed (e.g., 30 feet/6 squares for humans), split before/after actions. Difficult terrain (e.g., swamp bog) doubles movement cost.
        
- **Turn Structure**:
    
    - Each participant’s turn includes movement, one standard action, one bonus action (if applicable), and unlimited free actions (e.g., dropping an item).
        
    - DM resolves reactions in real-time (e.g., opportunity attacks triggered by movement).
        
    - UI: Players see a highlighted grid overlay (5-foot squares) with range indicators for movement, attacks, and spells. DM’s free camera highlights active characters and valid targets.
        
- **Action Resolution**:
    
    - **Attacks**: Roll d20 + ability modifier + proficiency bonus vs. Armor Class (AC). Critical hits (natural 20) double damage dice; critical misses (natural 1) may trigger DM-defined mishaps.
        
    - **Spells**: Spell slots (per D&D 5e levels 1–9) with casting times (action, bonus, reaction). Spells use d20 for attack or force saving throws (e.g., Wisdom vs. Charm Person).
        
    - **Saving Throws**: d20 + ability modifier + proficiency (if applicable) vs. Difficulty Class (DC) set by spell, trap, or DM (default DC 10–20).
        
    - **Status Effects**: Applied via attacks, spells, or environmental hazards (e.g., poisoned, stunned, prone). UI displays icons with timers (e.g., “stunned for 1 round”).
        
    - **Environmental Interactions**: Terrain modifiers (e.g., +2 AC for cover behind ruins), hazards (e.g., lava vent deals 2d6 fire damage per round), or scripted objects (e.g., collapsing bridge).
        

### 1.3 Grid-Based Movement

- **Grid System**: 5-foot (1.5 m) squares overlaid on the 3D world, aligned with sub-tiles (50 m × 50 m, or 10x10 grid squares per section). Grid is toggleable for immersion.
    
- **Tactical Positioning**:
    
    - **Cover**: Half cover (+2 AC, +2 Dexterity saves), three-quarters cover (+5 AC, +5 Dexterity saves), or full cover (cannot be targeted).
        
    - **Flanking**: Optional rule (toggleable by DM) grants +2 to attack rolls when two allies are on opposite sides of an enemy.
        
    - **Opportunity Attacks**: Triggered when moving out of an enemy’s reach (5 feet for most weapons), resolved with a reaction.
        
- **Movement Costs**:
    
    - Normal terrain: 1 square = 5 feet.
        
    - Difficult terrain (e.g., swamp, rubble): 1 square = 10 feet.
        
    - Climb/swim: 1 square = 10 feet (or 15 feet in harsh conditions, e.g., icy cliff).
        
    - DM can define custom terrain costs via sliders (e.g., quicksand = 20 feet per square).
        
- **Visualization**: Grid highlights valid movement squares in blue, out-of-range in red, and difficult terrain in yellow. Pathfinding (A* algorithm) suggests optimal routes, respecting obstacles and cover.
    

### 1.4 Dice Mechanics

- **Core Rolls**:
    
    - **Attack Rolls**: d20 + ability modifier (e.g., Strength for melee, Dexterity for ranged) + proficiency (if proficient) vs. AC.
        
    - **Skill Checks**: d20 + ability modifier + proficiency (if applicable) vs. DM-set DC (e.g., Athletics for climbing, Stealth for sneaking).
        
    - **Saving Throws**: d20 + ability modifier + proficiency (if applicable) vs. DC (e.g., Constitution vs. poison).
        
- **Advantage/Disadvantage**: Roll 2d20, take highest (advantage) or lowest (disadvantage), triggered by conditions (e.g., advantage on attack from invisibility).
    
- **Randomization**: Godot’s RandomNumberGenerator for dice rolls, seeded for reproducibility in saved sessions. UI shows animated dice rolls for immersion.
    
- **DM Overrides**: DM can manually set roll outcomes or modifiers (e.g., +5 for narrative reasons) via a dice control panel.
    

## 2. Customization Tools

The combat system is highly customizable, allowing DMs to modify D&D 5e rules or create new mechanics using an AI-driven interface that processes natural language inputs. Customization is accessible via a dedicated “Combat Rules Editor” in the DM’s UI.

### 2.1 Combat Rules Editor

- **Interface**: A dockable panel in the DM’s free camera mode, with tabs for Initiative, Actions, Status Effects, and Environmental Rules.
    
- **Natural Language Input**:
    
    - DMs describe custom rules in text (e.g., “Add a ‘Burning’ status effect that deals 1d4 fire damage per round for 3 rounds”).
        
    - AI Agent: Parses input using a natural language processing model, converting descriptions into GDScript logic. Prompts DM for clarification on ambiguous inputs (e.g., “Does ‘Burning’ stack with multiple applications?”).
        
    - Examples:
        
        - Input: “Create a new action: ‘Whirlwind Strike’ lets fighters hit all enemies within 10 feet for 2d6 damage.”
            
            - Output: Script defining a new action with range check, damage roll, and animation trigger.
                
        - Input: “Change movement to cost 1.5x in forests.”
            
            - Output: Updates terrain cost multiplier for forest sub-tiles.
                
    - Restrictions: Limits complex scripts (e.g., recursive calculations) to prevent server strain. AI flags potential performance issues and suggests simplifications.
        
- **Predefined Templates**:
    
    - Modifiable D&D 5e rules (e.g., adjust attack range, spell slot recovery).
        
    - Common homebrew templates (e.g., “gritty realism” with longer rests, “fast combat” with doubled damage).
        
- **Rule Storage**:
    
    - Custom rules saved as JSON in the campaign file, including AI-generated scripts and metadata (e.g., rule name, author).
        
    - Shareable via in-game marketplace, with version control to track updates.
        

### 2.2 Dynamic Adjustments

- **Real-Time Tweaks**:
    
    - DMs adjust rules during combat via sliders/dropdowns (e.g., increase AC by 2 for a specific enemy, reduce spell DC by 1).
        
    - Quick-add status effects or actions (e.g., “Add ‘Frozen’ effect: halves movement, lasts 2 rounds”).
        
- **Balance Control**: DMs are responsible for balance; system provides warnings (e.g., “High damage output may unbalance encounter”) but does not enforce restrictions.
    
- **UI Feedback**: Visual indicators show modified rules (e.g., red outline on affected characters, tooltips explaining custom effects).
    

### 2.3 Integration with World-Building

- **Biome and Landmark Effects**:
    
    - Sub-tile metadata influences combat (e.g., forest sub-tiles grant +1 AC due to cover, volcanic vents apply “Burning” effect within 10 feet).
        
    - Landmarks trigger unique mechanics (e.g., fighting near a portal grants +1 to spell damage, cliffs impose fall damage risks).
        
- **City-Based Combat**:
    
    - City templates add tactical elements (e.g., human town alleys provide cover, dwarven fortress walls block line of sight).
        
    - NPCs in cities have combat roles (e.g., guards with +2 AC, merchants with low HP but high Charisma for negotiation).
        
- **Void Interactions**: Voids (e.g., ocean, lava) impose environmental hazards (e.g., lava deals 4d6 damage per round if entered).
    

## 3. Implementation in Godot 4.x

The combat system leverages Godot’s node-based architecture, networking, and scripting for seamless integration with the game world.

### 3.1 Core Nodes

- **CombatManager (Node)**:
    
    - Manages turn order, dice rolls, and action resolution.
        
    - Signals: turn_started(character: Node), action_resolved(action: Dictionary), status_effect_applied(character: Node, effect: String).
        
- **GridOverlay (TileMap)**:
    
    - Renders 5-foot square grid, aligned with sub-tiles (10 squares per 50 m sub-tile).
        
    - Dynamically updates to highlight movement ranges, cover, and hazards.
        
- **Character (Node3D)**:
    
    - Represents players, NPCs, and enemies, with properties for stats (HP, AC, ability scores), position (grid coordinates), and status effects.
        
    - Child nodes: AnimationPlayer (for attacks/spells), CollisionShape3D (for hit detection).
        
- **DMControl (Camera3D)**:
    
    - Free-roaming camera with UI overlays for selecting characters, placing enemies, and editing rules.
        
    - Contextual menus for quick actions (e.g., “Spawn goblin at grid [x,y]”).
        

### 3.2 Procedural Scripts

- **GDScript Functions**:
    
    - resolve_action(character: Node, action: Dictionary, target: Node): Calculates attack rolls, damage, or spell effects, applying status effects and environmental modifiers.
        
    - calculate_movement(character: Node, destination: Vector2i): Uses A* pathfinding to validate movement, accounting for terrain costs and obstacles.
        
    - apply_custom_rule(rule: Dictionary): Executes AI-generated scripts for homebrew mechanics, with safety checks for performance.
        
- **AI Integration**:
    
    - parse_rule_input(input: String) -> Dictionary: Converts natural language to GDScript, storing parameters (e.g., damage type, duration) in a rule dictionary.
        
    - Prompts DM for clarification via pop-up UI (e.g., “Specify range for ‘Whirlwind Strike’”).
        
- **Serialization**:
    
    - Combat state (turn order, character stats, active effects) saved in JSON, linked to the campaign’s map data.
        
    - Custom rules stored as separate JSON objects, referenced by CombatManager.
        

### 3.3 Networking

- **Multiplayer**:
    
    - Dedicated servers synchronize combat state (turn order, grid positions, dice rolls) for six players + DM.
        
    - Latency mitigation: Predictive movement for real-time positioning, server-authoritative resolution for actions.
        
    - Turn-based sync: Clients wait for server confirmation before advancing turns.
        
- **Offline Mode**:
    
    - Full combat functionality available without internet, using local CombatManager instance.
        
    - AI-driven NPCs handle enemy turns, with DM override options.
        

### 3.4 Performance Optimizations

- **LOD and Culling**:
    
    - GridOverlay uses low-resolution textures for distant areas, high-resolution near active characters.
        
    - Enemies outside player view frustum are culled, with simplified AI for off-screen NPCs.
        
- **Batch Processing**:
    
    - Dice rolls and status effect calculations batched to minimize frame drops.
        
    - Custom rule scripts optimized to avoid excessive loops or recursion.
        
- **Hardware Target**: Maintains 60 FPS on mid-range PCs (e.g., GTX 1660, 16GB RAM), with dynamic LOD adjustments based on world complexity.
    

## 4. UI and Accessibility

- **Player UI**:
    
    - HUD displays HP, AC, spell slots, and available actions. Clickable buttons for standard/bonus actions, with tooltips for rules.
        
    - Dice roll animations with results (e.g., “d20 = 17 + 3 = 20, hit!”).
        
    - Grid overlay toggleable via hotkey, with colorblind-friendly modes (e.g., high-contrast blue/yellow).
        
- **DM UI**:
    
    - Combat Rules Editor with text input, sliders, and template dropdowns.
        
    - Initiative tracker with drag-and-drop reordering and status effect icons.
        
    - Contextual menus for spawning enemies, applying effects, or overriding rolls.
        
- **Accessibility**:
    
    - Customizable key bindings for movement and actions.
        
    - Screen reader support for UI elements (e.g., “Player 1’s turn, 30 HP, stunned”).
        
    - Scalable UI for different resolutions, with font size adjustments.
        

## 5. Integration with World-Building

- **Map Editor Synergy**:
    
    - Sub-tile biomes influence combat (e.g., swamp sub-tiles apply “muddy” effect, reducing speed by 10%).
        
    - Landmarks trigger unique mechanics (e.g., fighting in a ruin grants +1 AC due to debris, meteor crater applies “radiation” effect dealing 1d4 damage per round).
        
- **City Integration**:
    
    - City templates define combat zones (e.g., human town plaza as open terrain, dwarven tunnels as confined with cover).
        
    - NPCs in cities have combat stats (e.g., guard: AC 16, longsword +5 to hit, 2d8 damage).
        
- **Void Effects**:
    
    - Voids (e.g., ocean, lava) act as impassable terrain or hazards (e.g., falling into lava deals 10d10 fire damage).
        
    - Procedural transitions (e.g., beach sub-tiles near ocean voids) add tactical elements like slippery surfaces (+1 DC to Dexterity saves).
        

## 6. Example Workflow

1. **Setup**: DM places a combat encounter in a forest section with a ruin landmark, spawning 4 goblins (AC 15, 7 HP each) and 1 ogre (AC 11, 59 HP).
    
2. **Initiative**: Players roll d20 + Dexterity (e.g., Fighter rolls 17, Wizard 12), DM sets goblin group initiative to 10, ogre to 5.
    
3. **Turn 1**:
    
    - Fighter moves 6 squares (30 feet), attacks goblin with longsword (d20 + 5 = 18, hits, deals 1d8 + 3 = 7 damage, kills goblin).
        
    - Wizard casts Fireball (8d6 damage, Dexterity save DC 15), targeting 3 goblins. Two fail, take 28 damage (dead); one saves, takes 14 (survives).
        
    - DM uses free camera to highlight ogre, applies custom “Rage” effect (+2 damage, lasts 2 rounds) via Combat Rules Editor.
        
4. **Environment**: Forest sub-tiles grant +1 AC for cover. Ruin landmark spawns debris, providing half cover (+2 AC) to one goblin.
    
5. **Resolution**: Combat continues with synchronized turns, DM adjusts rules (e.g., “Ogre’s club now has 10-foot reach”) mid-session via AI input.
    

## 7. Edge Cases and Testing

- **Edge Cases**:
    
    - Non-square maps: Grid aligns to section boundaries, voids treated as impassable.
        
    - Overlapping effects: Status effects stack with clear priorities (e.g., “stunned” overrides “burning”).
        
    - AI parsing errors: Fallback to default D&D 5e rules if custom script fails; logs issue for DM review.
        
- **Testing Needs**:
    
    - Stress-test AI rule parsing for complex inputs (e.g., multi-step abilities).
        
    - Verify grid alignment in non-contiguous maps (e.g., archipelago layouts).
        
    - Ensure server sync for 7 concurrent users with custom rules active.
        
    - Test offline mode for combat with 50+ NPCs and dynamic effects.
        

## 8. Future Enhancements

- Add advanced AI behaviors for enemies (e.g., pack tactics, morale-based retreats).
    
- Expand environmental interactions (e.g., destructible terrain, weather effects like rain reducing visibility).
    
- Integrate modding API for community-created abilities, spells, or combat templates.
    
- Support larger battles (e.g., 20+ participants) with optimized culling and AI.
    

This Turn-Based Combat System delivers a flexible, immersive experience that blends D&D 5e’s tactical depth with _Mythos Tabletop_’s dynamic world. It empowers DMs to craft unique encounters while ensuring performance and accessibility.

## Review Needed
Proposed para-type: area. Assigned based on content/frontmatter (confidence ~70%). Do not move until reviewed.