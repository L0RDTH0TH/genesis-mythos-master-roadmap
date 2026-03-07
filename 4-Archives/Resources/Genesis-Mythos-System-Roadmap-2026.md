---
title: Genesis Mythos System Roadmap 2026
created: 2026-03-02
tags: [roadmap, genesis-mythos, project, synthesis]
para-type: Resource
status: active
highlight_key: genesis-chaos
---

# Genesis Mythos System Roadmap 2026

Consolidated from Ingest genesis-mythos docs, audits, and rules. Use highlight_perspective: genesis-chaos.

---

## Phase 1: Primordial Chaos & Origins

- **Chaos origin**: Raw development artifacts (docs/, audit/, .cursor/rules, flame_graph, forensic scripts) captured from [L0RDTH0TH/genesis-mythos](https://github.com/L0RDTH0TH/genesis-mythos) and [Genesis-Azgaar](https://github.com/L0RDTH0TH/Genesis-Azgaar).
- **Genesis Mythos**: Godot 4.5.1 project — 3D first-person open world for tabletop RPG; data-driven, GDScript-only, Lordthoth.
- **Azgaar fork**: Modularity refactor for Godot integration; Fantasy Map Generator lineage.
- **Bootstrap**: Config stub (Second-Brain-Config), Genesis Mythos Hub + Genesis Resources Hub, highlight_key genesis-chaos.

---

## Phase 2: Core Features & Components

### Core (implemented)
- **Core singletons**: Eryndor, Logger, WorldStreamer, EntitySim, FactionEconomy (autoload).
- **World generation**: MapGenerator (FastNoiseLite), MapRenderer, MapEditor, MarkerManager.
- **World Builder UI**: 8-step wizard (Seed & Size → 2D Map Maker → Terrain → Climate → Biomes → Structures & Civilizations → Environment → Resources & Magic → Export).
- **Terrain3D integration**: Heightmap import, sculpting, LOD, biomes (32 textures).
- **Procedural World Map addon**: 2D map display.
- **Data management**: JSON/Resources for items, abilities, races, UI text.

### Support
- **Fantasy archetypes**: Preset configurations (high/low fantasy, grimdark, sword-and-sorcery, etc.) for procedural world generation.
- **GUI spec**: BG3-inspired; GameGUI scripts on base nodes; single theme `bg3_theme.tres`; UIConstants, no magic numbers.
- **Audits**: World builder, Azgaar integration, performance overlay, flamegraph, race/class UI, layout fixes.
- **Forensic/debug**: FORENSIC_DEBUG_SCRIPT, debug overlays, migration/status reports.

---

## Phase 3: Development Tasks & Milestones

- [ ] **Ingest completion**: Run full-autonomous-ingest on remaining Ingest/genesis-mythos (≈252 .md) and Ingest/Genesis-Azgaar (9); approve mid-band proposals (e.g. README → 1-Projects/Genesis-Mythos) via `approved: true` and re-run.
- [ ] **Distill pass**: BATCH-DISTILL on all Genesis Mythos–related notes (chaos origin, core features, phases, actionable tasks; 60–80% coverage; highlight_perspective genesis-chaos; log coverage_adapted).
- [ ] **Map-maker / 2D→3D**: Parchment painter → Terrain3D seed; MapEditor.tscn + height/biome layers; Azgaar PNG import.
- [ ] **Character creation**: Wizard flow, HSplit (options left, 3D preview right), AbilityScoreRow prefab, races.json.
- [ ] **Migration/prep**: Azgaar fork to Terrain3D plan v2; parameter integration audits; rendering disconnect fixes.
- [ ] **Testing**: GUT setup, world generation coverage, character creation coverage, fantasy style presets.
- [ ] **Performance**: Idle FPS, create-world lag, grey screen investigations; performance overlay purge/migration.

---

## Phase 4: Evolution & Open Questions

- **Open**: Genesis / TheDiem repos (404); capture when available.
- **Open**: Remaining audits (azgaar SVG hang, serverless, transparency) → fold into task list or archive.
- **Resurface**: High-potential notes (links, highlights) mark resurface-candidate; optional Resurface hub.
- **Express**: Related-content-pull + mini-outline + CTA on key roadmap notes; append to hub.

---

## Related / Connections

- [[3-Resources/Genesis Mythos Hub]]
- [[3-Resources/Genesis Resources Hub]]
- [[3-Resources/Second-Brain-Config]]
- Ingest: `Ingest/genesis-mythos/` (README, docs--SYSTEM_IMPLEMENTATIONS, docs--WORLD_BUILDER_WIZARD_GUIDE, audit--*, flame_graph_freeze_audit) — run INGEST MODE to classify and move.
