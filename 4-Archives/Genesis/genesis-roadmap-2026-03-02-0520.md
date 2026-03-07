---
title: Genesis Roadmap — Godot stack & phased plan
created: 2026-03-01
tags: [project, genesis, godot, vtt, roadmap]
para-type: Project
status: active
project-id: Genesis
links: ["[[Genesis]]", "[[master-goal-for-genesis-2026-03-02-0520]]"]
---

# Genesis Roadmap — Godot stack & phased plan

## TL;DR

Phased execution plan for Genesis VTT: Godot 4.3 + Terrain3D + Free5e/A5e, 2D SVG map maker → 3D Terrain3D, ~3–4 months to playable MVP. Week 1 core → Weeks 2–3 maps → Month 1 mechanics → Month 2 MP/DM → Month 3 polish.

## Stack fit & setup

| Component | Role | Install/Notes |
|-----------|------|---------------|
| **Godot 4.3+** | Engine core (FP nav, MP via High-Level Multiplayer) | Download editor. Enable GDExtensions. |
| **Terrain3D** | 3D maps/open world proc gen (noise/heightmaps, editable voxels, clipmaps) | Asset Lib: "Terrain3D". GDExtension—drop in `addons/`, enable plugin. |
| **Free5e (+A5E overlay)** | D&D mechanics (chars, combat, rules engine) | SRDs: wyrmworks/free5e, a5esrd.com. Parse JSON for sheets/rolls. |
| **SVG Maps** | 2D maker (zoomable editor, export to 3D) | Plugins: "godot-svg" or "Scalable Vector Shapes 2D". Paths→mesh for Terrain3D. |

**Gotchas:** Terrain3D GPU-heavy—test low-end. SVG: limit paths (<10k). SRDs: no official API—script parser.

## Integration flow

1. **2D Map Maker → 3D**: SVG editor → export paths → heightmap/colliders → Terrain3D import.
2. **Proc gen**: DM seeds → FastNoiseLite + Terrain3D textures; user-guided previews.
3. **FP open world**: CharacterBody3D + Terrain3D collision; seamless zones via clipmaps.
4. **Combat/chars**: Free5e JSON → dynamic sheets; turn queue (DM authoritative); RPC sync for rolls.
5. **MP (5p+DM)**: DM = dedicated server; sync transforms, RPCs, NetworkVars.
6. **DM tools**: Rule sliders (A5E), spawn on Terrain3D, fog, lore wiki.

```gdscript
extends Terrain3D
func _ready():
    var noise = FastNoiseLite.new()
    noise.seed = dm_seed
    texture_set(0, noise_texture_from_svg_export())
```

## Phased roadmap

| Phase | Milestones | Time |
|-------|------------|------|
| **Week 1: Core** | Godot proj + Terrain3D + basic FP cam. Proc hill demo. | 1w |
| **Weeks 2–3: Maps** | SVG plugin + 2D editor. Export→Terrain3D test. Presets (gothic tileset JSON). | 2w |
| **Month 1: Mechanics** | Free5e parser + char sheet UI. d20 combat loop + init queue. | 4w |
| **Month 2: MP/DM** | 6p sync (test LAN). Fog/rules editor. Guided proc (DM sliders). | 4w |
| **Month 3: Polish** | World saves (ResourceSaver), A5E toggles. Itch.io alpha. | 4w |

**Total: ~3–4 months to playable MVP.**

**Next moves:** Godot 4.3 → New Proj → Add Terrain3D + godot-svg; prototype SVG square → heightmap → walk on Terrain3D; GitHub repo for feedback.
