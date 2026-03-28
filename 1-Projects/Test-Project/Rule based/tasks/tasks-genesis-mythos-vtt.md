## Relevant Files

- `docs/prd-genesis-mythos-vtt.md` - Product Requirements Document describing the vertical slice scope and requirements.
- `engine/world/WorldGenerator.gd` - Godot world generation pipeline entrypoint (seed parsing, stage orchestration).
- `engine/world/stages/TerrainStage.gd` - Terrain layout generation stage (heightmap, collision meshes, navmesh).
- `engine/world/stages/BiomeStage.gd` - Biome placement and region tagging.
- `engine/world/stages/PoiStage.gd` - Placement of settlements, dungeons, and notable landmarks.
- `engine/world/stages/EntityStage.gd` - Initial placement of NPCs, creatures, and interactables.
- `engine/sim/SimulationLoop.gd` - Tick‑based simulation for time of day, weather, and basic NPC schedules.
- `engine/camera/PlayerFirstPersonController.gd` - First‑person player controller and camera rig.
- `engine/camera/DmFreeCamController.gd` - DM free‑cam controller and camera rig.
- `engine/camera/DmOrthographicController.gd` - DM orthographic tabletop camera and controls.
- `engine/camera/CameraRigManager.gd` - Camera abstraction and mode switching with interpolation.
- `engine/rules/free5e/Free5eRulesPlugin.gd` - Free 5e ruleset plugin (stats, actions, basic combat resolution).
- `engine/rules/free5e/EncounterManager.gd` - Encounter and turn‑based combat loop orchestration.
- `engine/session/SessionManager.gd` - Session lifecycle (world generation, session start, re‑generation triggers).
- `engine/world/ProvenanceStore.gd` - Captures and exposes generation seeds, parameters, and provenance metadata.
- `ui/PlayerHud.tscn` - Player HUD (basic prompts, simple stats, interaction cues).
- `ui/DmControlsPanel.tscn` - DM controls for view switching, weather toggles, and re‑generation actions.
- `tests/world/WorldGenerator.test.gd` - Tests for world generation pipeline behavior.
- `tests/rules/free5e/Free5eRulesPlugin.test.gd` - Tests for core Free 5e rules integration.
- `tests/camera/CameraRigManager.test.gd` - Tests for camera mode switching and interpolation behavior.

### Notes

- File paths are **proposed** and can be adapted to the actual project layout; keep implementation + tests co‑located where reasonable.
- Use the project’s test runner (e.g., `godot --headless --run-tests` or equivalent) to execute tests as they are added.

## Instructions for Completing Tasks

**IMPORTANT:** As you complete each task, you must check it off in this markdown file by changing `- [ ]` to `- [x]`. This helps track progress and ensures you don't skip any steps.

Example:
- `- [ ] 1.1 Read file` → `- [x] 1.1 Read file` (after completing)

Update the file after completing each sub‑task, not just after completing an entire parent task.

## Tasks

- [ ] 0.0 Create feature branch
  - [ ] 0.1 Create and checkout a new branch for this feature (e.g., `git checkout -b feature/genesis-mythos-vtt-vertical-slice`)

- [ ] 1.0 Establish project structure and PRD integration
  - [ ] 1.1 Confirm or create the core Godot project structure for `engine/`, `ui/`, and `tests/` folders.
  - [ ] 1.2 Move or link `prd-genesis-mythos-vtt.md` into an appropriate `docs/` location and ensure it is easily discoverable.
  - [ ] 1.3 Add a short `README` section that points contributors to the PRD and this tasks file as the source of truth for the vertical slice scope.

- [ ] 2.0 Implement the world generation pipeline skeleton
  - [ ] 2.1 Create `WorldGenerator.gd` as the main entrypoint for world generation with a clear interface (inputs: seeds + intents; outputs: populated world scene).
  - [ ] 2.2 Implement stubbed generation stages (`TerrainStage`, `BiomeStage`, `PoiStage`, `EntityStage`) with a shared interface and no‑op or minimal behavior.
  - [ ] 2.3 Wire the stages together in a simple, explicit pipeline within `WorldGenerator.gd` so stages execute in order and can be swapped.
  - [ ] 2.4 Add basic logging or debug output for each stage so generation runs are inspectable during development.
  - [ ] 2.5 Write initial tests in `WorldGenerator.test.gd` to verify that the pipeline executes all stages and produces a non‑empty world scene.

- [ ] 3.0 Add intent input and provenance tracking
  - [ ] 3.1 Define a simple data model for DM/player intents (seed, themes, factions, hooks) that can be passed into the generator.
  - [ ] 3.2 Implement a lightweight `ProvenanceStore.gd` that records seeds, intents, and stage parameters for each generation run.
  - [ ] 3.3 Attach provenance metadata to key generated entities (e.g., POIs, factions) for later inspection.
  - [ ] 3.4 Expose a simple in‑engine debug view or log output that surfaces provenance for selected entities.
  - [ ] 3.5 Add tests to ensure that provenance data is created and accessible after generation.

- [ ] 4.0 Implement basic simulation loop
  - [ ] 4.1 Create `SimulationLoop.gd` that advances a tick counter and updates simple world state (time of day, weather).
  - [ ] 4.2 Implement at least two weather states (e.g., clear, rain) that affect lighting or simple visual parameters.
  - [ ] 4.3 Add minimal NPC schedule behavior (e.g., idle + walk along a few waypoints) driven by the simulation loop.
  - [ ] 4.4 Ensure the simulation is decoupled from rendering frame rate (e.g., uses fixed timestep or delta‑time with caps).
  - [ ] 4.5 Add tests to exercise the simulation loop and validate deterministic behavior for a given seed.

- [ ] 5.0 Build first‑person player controller and HUD
  - [ ] 5.1 Implement `PlayerFirstPersonController.gd` with WASD movement, mouse look, and collision handling appropriate for the prototype.
  - [ ] 5.2 Add an interaction raycast and simple interaction system (e.g., highlight/tooltip when looking at usable objects).
  - [ ] 5.3 Create `PlayerHud.tscn` with minimal UI for health, simple stats, and interaction prompts.
  - [ ] 5.4 Integrate the player controller and HUD into a playable scene, starting in first‑person view by default.
  - [ ] 5.5 Add tests (where feasible) or automated checks for controller configuration and basic interaction wiring.

- [ ] 6.0 Implement DM free‑cam and orthographic tabletop view
  - [ ] 6.1 Implement `DmFreeCamController.gd` with flight controls (move, orbit, tilt, zoom) over the world.
  - [ ] 6.2 Implement `DmOrthographicController.gd` to provide a top‑down orthographic view of a configurable region.
  - [ ] 6.3 Create `CameraRigManager.gd` that manages camera mode switching (player, DM free‑cam, DM ortho) using a unified world scene graph.
  - [ ] 6.4 Implement smooth interpolation for camera transitions (position, rotation, FOV) between DM modes.
  - [ ] 6.5 Create `DmControlsPanel.tscn` with buttons or hotkeys to switch views and expose key DM actions.
  - [ ] 6.6 Add tests for `CameraRigManager.gd` to validate correct mode switching and basic interpolation behavior.

- [ ] 7.0 Integrate Free 5e ruleset as a plugin
  - [ ] 7.1 Design a rules plugin interface that exposes core hooks (stat blocks, actions, checks, damage resolution).
  - [ ] 7.2 Implement `Free5eRulesPlugin.gd` with a minimal, SRD‑compatible subset (basic stats, attack rolls, damage, saving throws).
  - [ ] 7.3 Implement `EncounterManager.gd` to orchestrate turn order, actions, and outcomes using the Free 5e rules plugin.
  - [ ] 7.4 Connect encounter state to the orthographic tabletop view (token positions, selected targets, etc.).
  - [ ] 7.5 Add tests in `Free5eRulesPlugin.test.gd` to validate attack/defense resolution and a simple combat scenario.

- [ ] 8.0 Session management and re‑generation controls
  - [ ] 8.1 Implement `SessionManager.gd` to coordinate world generation, entering a session, and ending or resetting sessions.
  - [ ] 8.2 Add DM UI controls to trigger minor live tweaks (e.g., reposition a token, toggle weather) without full re‑generation.
  - [ ] 8.3 Add DM UI controls to intentionally re‑generate a region or the entire world, using updated seeds or intents.
  - [ ] 8.4 Ensure each generation run records a snapshot (seed, intents, rules plugin versions) via `ProvenanceStore.gd`.
  - [ ] 8.5 Add tests to verify that session transitions and re‑generation calls work as expected.

- [ ] 9.0 Polish, UX, and documentation for the vertical slice
  - [ ] 9.1 Tighten basic visuals (lighting presets, simple materials) so the world is readable and appealing in both first‑person and orthographic views.
  - [ ] 9.2 Refine movement and camera feel (sensitivity, acceleration, easing) to support the “immersive first‑person” and “Sparky‑style” goals.
  - [ ] 9.3 Add a short in‑engine tutorial or help overlay summarizing key controls for players and DMs.
  - [ ] 9.4 Document extension points (worldgen stages, rules plugins, simulation hooks) in `docs/` for future contributors.
  - [ ] 9.5 Run an end‑to‑end playtest (generation → exploration → one combat encounter → re‑generation) and capture notes for the next iteration.

