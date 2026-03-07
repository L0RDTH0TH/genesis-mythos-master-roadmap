---
title: Genesis Week 1 — Core sub-roadmap
created: 2026-03-02
tags: [project, genesis, godot, vtt, week1]
para-type: Project
status: active
project-id: Genesis
links: ["[[Genesis]]", "[[genesis-roadmap-2026-03-02-0520]]"]
---

# Genesis Week 1 — Core sub-roadmap

## TL;DR

Week 1 Genesis VTT: Godot project + Terrain3D + basic FP cam + proc hill demo. Four phases over 5–7 days — project setup, terrain integration, first-person camera, integration & polish. Deliverable: playable walk on procedural hills.

**Principles:** Modularity, completeness, robustness, future-proofing (version control, configurable scripts, signal-based events).

**Estimated:** 5–7 days (4–6 h/day). **Prereqs:** Godot 4.3+, basic GDScript, Git.

---

### Phase 1: Project setup (Day 1)

| Task | Description | Dependencies | Validation | Notes |
|------|-------------|--------------|------------|-------|
| 1.1 Create New Project | Godot 4.3+ → new project "GenesisVTT", enable GDExtensions | None | Run empty project; no console errors | .gitignore; `git init` + first commit |
| 1.2 Configure Version Control | Git init, remote, commit empty project | 1.1 | `git status` clean; push succeeds | README with goals; branches e.g. `feature/week1-core` |
| 1.3 Install Dependencies | Asset Lib: Terrain3D (GDExtension), enable in Plugins | 1.1 | Restart editor; Terrain3D in Addons, no errors | Pin version in `dependencies.txt` |

### Phase 2: Basic terrain integration (Days 2–3)

| Task | Description | Dependencies | Validation | Notes |
|------|-------------|--------------|------------|-------|
| 2.1 Add Terrain3D Node | Scene `world.tscn`, Terrain3D root; heightmap 1024×1024, clipmap levels | Phase 1 | Scene plays; terrain renders; test on low-end | `@export heightmap_size`; signals for `terrain_generated` |
| 2.2 Procedural Hill Demo | FastNoiseLite (Perlin, seed=0) → heightmap; grass/rock textures | 2.1 | Hills visible; zoom seamless; FPS >30; unit test noise range | `ProcGen.gd` singleton; fallback flat on noise fail |
| 2.3 Collision Setup | Terrain3D collision; StaticBody3D test drop | 2.2 | Object collides on hills; no steep-slope clip | Optimized colliders; signals for voxel edits |

### Phase 3: First-person camera (Days 4–5)

| Task | Description | Dependencies | Validation | Notes |
|------|-------------|--------------|------------|-------|
| 3.1 Basic FP Camera | `player.tscn`: CharacterBody3D + Camera3D; WASD + mouse look; Terrain3D collision | Phase 2 | Walk hills, no fall-through; keyboard/mouse vs gamepad | `Movement.gd`, `CameraControl.gd`; `player_moved` signal |
| 3.2 Terrain Interaction | Raycast ground snap; jump/climb on hills | 3.1 | Navigate hills; no stuck; perf OK at speed | Raycast fail → warning + fallback; `TerrainInteractor` for DM tools |
| 3.3 Debug HUD | CanvasLayer: FPS, position, terrain height at feet | 3.2 | HUD real-time | Toggle (e.g. F3); singleton |

### Phase 4: Integration & polish (Days 6–7)

| Task | Description | Dependencies | Validation | Notes |
|------|-------------|--------------|------------|-------|
| 4.1 Full Demo Integration | `world.tscn` main; player on terrain; proc hills on `_ready()` | Phases 1–3 | Full playtest; 1-min video demo | Scene inheritance `base_world.tscn` |
| 4.2 Robustness Checks | Error handling (e.g. Terrain3D fail → error scene); memory/CPU profile | 4.1 | Simulate fail; no crash; run on low-end | Global error handler; baseline benchmark |
| 4.3 Unit/Scene Tests | GDScript tests: noise, camera bounds, collision; Godot tester or GDUnit | 4.1 | 100% pass | `tests/`; GitHub Actions CI |
| 4.4 Documentation & Commit | README Week 1 guide; commit; tag `week1-mvp` | All prior | History + docs readable | Architecture notes; merge after tests pass |

**Deliverable:** Playable demo — walk procedural hills in first-person. Share repo or Itch.io prototype.

**Risks:** Terrain3D issues → fallback HeightMapShape3D. Budget time for GDScript learning.

**Next:** Week 2 = SVG maps → Terrain3D; ProcGen singleton can overlay SVG data.
