---
name: Genesis-Mythos Full Forward Roadmap
overview: Plan to produce a clean, Dataview-first Genesis-Mythos master roadmap and expanded phase roadmaps (5–15 prioritized subtasks per phase), enforce the desired vault pattern, add sample Dataview queries, propose Ingest/Decisions handling for 300+ files, and lock in the performance-first stance.
todos: []
isProject: false
---

# Genesis-Mythos Full Forward Roadmap – Plan

## 1. Current state vs desired end-state

**Existing assets (keep):**

- Master: [Genesis-Mythos-Roadmap-2026-03-02-1200.md](1-Projects/Genesis-Mythos/Roadmap/Genesis-Mythos-Roadmap-2026-03-02-1200.md) — already has zero checkboxes and one Dataview TABLE per phase.
- Phase roadmaps in `Phase-1-Maps/` … `Phase-6-Wizard/` with correct `roadmap-level: phase` and `phase-number`.
- [Genesis-Mythos-Roadmap-MOC.md](1-Projects/Genesis-Mythos/Genesis-Mythos-Roadmap-MOC.md) aggregates all roadmaps.

**Adjustments to enforce:**

- **Master frontmatter:** Remove `phase-number` from the master note (it applies only to phase/subphase). Add `decision_selected` to the documented contract; use only on phase/subphase when a decision note has approved an option.
- **Frontmatter contract** (document in master or in [Roadmap-Standard-Format.md](3-Resources/Roadmap-Standard-Format.md)): `roadmap-level`, `phase-number` (1–6, omit on master), `status`, `priority`, `dependencies`, `progress`, `decision_selected` (optional, **phase/subphase only — never on master**; when set via decision note).
- **Sub-phase depth:** Current structure is 3 levels under `Roadmap/` (e.g. `Roadmap/Phase-1-Maps/Phase-1-Maps-Roadmap-....md`). Allow optional 4th level for sub-phase notes (e.g. `Phase-1-Maps/Azgaar-Export/...`) if needed; no change required for the initial deliverable.

---

## 2. Folder structure (≤4 levels)

Keep and document:

```
1-Projects/Genesis-Mythos/Roadmap/
├── Genesis-Mythos-Roadmap-YYYY-MM-DD-HHMM.md   ← master (no tasks)
├── Phase-1-Maps/
│   └── Phase-1-Maps-Roadmap-YYYY-MM-DD-HHMM.md
├── Phase-2-Terrain3D/
│   └── Phase-2-Terrain3D-Roadmap-....
├── … Phase-3 through Phase-6 …
└── (optional) Phase-N-Name/Subphase-Folder/     ← 4th level if needed
```

**Refinement:** If a phase grows many sub-roadmaps, keep a single phase roadmap note per phase folder and use **nested Dataview** inside it to list any future sub-phase notes (e.g. `FROM "1-Projects/Genesis-Mythos/Roadmap/Phase-1-Maps" WHERE roadmap-level = "subphase"`). No new folders until you add real sub-phase files.

---

## 3. Expanded phases: 5–15 concrete subtasks each (prioritized)

Tasks are **high / medium / low**; store as inline tag or suffix (e.g. `[high]`) until task-level frontmatter exists. Sub-phase roadmaps hold the actual `- [ ]` lines; below is the content spec for each phase note.

### Phase 1 — Maps (Azgaar modular foundation)


| Priority | Subtask                                                                                   |
| -------- | ----------------------------------------------------------------------------------------- |
| high     | Stabilize Azgaar fork: clone, build, test generation pipeline locally                     |
| high     | Define and document Azgaar export schema (heightmaps, biomes, regions, political borders) |
| high     | Implement export pipeline: heightmap export from Azgaar state                             |
| high     | Implement export: region/biome and political-border export for Terrain3D                  |
| high     | In-game tile editor: 256×256 grid (500 m tiles), 37 km² total; save/load section state    |
| medium   | Tile editor: 10×10 sub-tiles per section (50 m); tileset and biome variants               |
| medium   | Shape templates (island, continent, ring); section counter; undo/redo                     |
| medium   | Void types (ocean, lava, void) and edge transition rules                                  |
| medium   | Landmark placement on sub-tile grid (dungeon, river, ruin)                                |
| medium   | City generator: templates (human, elf, dwarf, halfling); section-based cities             |
| low      | Serialize full map (sections, sub-tiles, biomes, voids) for 2D→3D handoff                 |
| low      | Editor UI: DM tooling hooks and validation (no invalid biomes at borders)                 |


**Total:** 12 tasks. Phase 1 roadmap note gets these as `- [ ]` with `[high]`/`[medium]`/`[low]` in the line or in a short table above.

### Phase 2 — Terrain3D integration & runtime


| Priority | Subtask                                                                               |
| -------- | ------------------------------------------------------------------------------------- |
| high     | Data layout: data directory, region size, mesh size (per integration guide)           |
| high     | 2D→3D pipeline: consume Azgaar exports (heightmaps, biomes) into Terrain3D            |
| high     | Runtime: seamless open-world stitching for full 37 km² (256×256 tiles)                |
| high     | LOD system: terrain LOD levels; culling for void tiles                                |
| high     | Performance baseline: profile and tune for 60 FPS target (see opinionated note below) |
| medium   | Seed-based procedural generation from 2D tilemap; Perlin for terrain/textures         |
| medium   | Asset LOD and tilemap LOD; runtime-modifiable parameters                              |
| medium   | UI hooks for DM: runtime parameter tweaks (e.g. time of day, weather)                 |
| low      | Save/load world state (terrain + runtime edits) for sessions                          |


**Total:** 9 tasks.

### Phase 3 — Lore support systems


| Priority | Subtask                                                                            |
| -------- | ---------------------------------------------------------------------------------- |
| high     | Lore data schema: entities, regions, events, relationships (queryable)             |
| high     | World lore database: load and query by region, faction, character                  |
| high     | Dynamic events: define event types and bind to map regions                         |
| high     | Lore → NPC dialogue hooks: data-driven dialogue keys from lore DB                  |
| medium   | Timeline / chronology tables for events and history                                |
| medium   | Integration with combat/faction systems: lore flags that affect combat or politics |
| medium   | DM tools: spawn/trigger events from lore; preview dialogue hooks                   |
| low      | Export/import lore packs for modding                                               |
| low      | Localization placeholder structure for dialogue and lore text                      |


**Total:** 9 tasks.

### Phase 4 — Combat & equipment progression


| Priority | Subtask                                                                             |
| -------- | ----------------------------------------------------------------------------------- |
| high     | Turn-based combat loop: initiative, round, actions/bonus/reactions, d20 resolution  |
| high     | Grid movement and facing; line-of-sight and range rules                             |
| high     | Equipment slots and inventory; equip/unequip and stat application                   |
| high     | D&D 5e–style core: AC, HP, conditions, death saves; balance baseline from 5e SRD    |
| high     | First-person player: WASD, jump, sprint, interact (doors, NPCs, objects)            |
| medium   | Status effects and environmental interactions (difficult terrain, cover)            |
| medium   | Class abilities and spells: data-driven definitions and execution                   |
| medium   | DM free camera: spawn assets, lighting, weather; turn order UI, target highlighting |
| medium   | Combat customization: initiative rules, homebrew mechanics (AI-parsed or scripted)  |
| medium   | Progression loops: XP, level-up, unlock abilities; save/share custom rule sets      |
| low      | Real-time hybrid option: optional real-time mode for exploration-only segments      |


**Total:** 11 tasks.

### Phase 5 — Politics & factions


| Priority | Subtask                                                                           |
| -------- | --------------------------------------------------------------------------------- |
| high     | Faction data model: factions, allegiance, influence, economy flags                |
| high     | Faction simulation: economy and influence tick; conflict/war state                |
| high     | NPC routines: schedule and location by faction and role                           |
| high     | World-state reactivity: NPC dialogue and behavior depend on faction state         |
| medium   | Player impact: alliances, declarations, quest outcomes affecting faction standing |
| medium   | Politics UI: faction standings, conflict map, key figures                         |
| medium   | Integration with lore: faction history and events from lore DB                    |
| low      | Modding: scriptable faction rules and new faction types                           |


**Total:** 8 tasks.

### Phase 6 — World-builder wizard & rendering


| Priority | Subtask                                                                                          |
| -------- | ------------------------------------------------------------------------------------------------ |
| high     | Wizard flow: guided steps map → terrain → lore → factions → polish (single linear flow)          |
| high     | Rendering comparison: document and decide engine/render path (e.g. forward vs deferred; shadows) |
| high     | Lock 60 FPS as non-negotiable; tune LOD, draw distance, shadow quality to meet it (see below)    |
| high     | Main menu and session create/load; character creation flow                                       |
| high     | DM camera: free fly, spawn, time control, visibility toggles                                     |
| medium   | World overview map (2D or 3D) for DM and optional player                                         |
| medium   | Wizard persistence: save wizard state and resume; export “world package”                         |
| medium   | NPC integration: city templates → NPCs; AI agent or scripted dialogue; routines                  |
| low      | Modding: scriptable events, custom archetypes, asset packs                                       |
| low      | Mobile considerations: decision workflow and toolbar macros for mobile review                    |


**Total:** 10 tasks.

---

## 4. Sample Dataview queries for the master roadmap

**Keep existing:** One TABLE per phase (sub-phase links, status, priority, progress, deadline). Paths already use `FROM "1-Projects/Genesis-Mythos/Roadmap/Phase-N-..."`.

**Add (optional) rollup block** at top or bottom of master for a single “at a glance” view:

```dataview
TABLE WITHOUT ID
    file.link AS "Phase",
    phase-number AS "#",
    status,
    priority,
    progress AS "%",
    length(filter(file.tasks, (t) => !t.completed)) AS "Open"
FROM "1-Projects/Genesis-Mythos/Roadmap"
WHERE roadmap-level = "phase"
SORT phase-number ASC
```

**Optional + fallback:** The rollup is optional. If the Tasks plugin is not installed or `file.tasks` is unavailable, remove the "Open" column entirely (or use a Tasks-plugin–specific fallback in a separate block). Document in Roadmap-Standard-Format that this is environment-dependent.

**Per-phase block** (already in place; ensure FROM path and WHERE are exact):

```dataview
TABLE WITHOUT ID
    file.link AS "Sub-Phase",
    status,
    priority,
    progress AS "%",
    deadline
FROM "1-Projects/Genesis-Mythos/Roadmap/Phase-1-Maps"
WHERE roadmap-level = "phase" OR roadmap-level = "subphase"
SORT priority DESC, file.name ASC
```

Repeat for Phase-2-Terrain3D through Phase-6-Wizard with the correct FROM path.

---

## 5. Ingest mess: 300+ files (genesis-mythos mirror, roadmaps, D&D, random)

**Strategy:**

1. **Backup first**
  Run `obsidian_create_backup` (or ensure recent backup) before any bulk move. No destructive moves without backup (per MCP rule).
2. **Batch classify and triage**
  - Use `obsidian_classify_para` (or equivalent) in batches on Ingest/*.md.  
  - Tag or log: `project-id: genesis-mythos` vs other (reference, archive).  
  - **Genesis-Mythos project notes** → move to `1-Projects/Genesis-Mythos/` subfolders (e.g. Docs, Design, Ingest-Processed) by theme, not back into Ingest.  
  - **Reference (D&D, system docs)** → `3-Resources/` with a clear subfolder (e.g. `3-Resources/Genesis-Mythos/D&D-5e-Ref/` or `3-Resources/RPG-Systems/`).  
  - **Obsolete/duplicate/junk** → `4-Archives/Genesis-Mythos-Old-Ingest-YYYY-MM/` or similar; optionally add `resurface-candidate` for high-value items before archiving.
3. **Low-confidence and decision workflow**
  - **Ingest/Decisions/ (or Ingest/Decisions):** When classification confidence < 72% (or below your mid-band min), do **not** auto-move. Instead:  
    - Write a **proposal note** (or leave note in Ingest with a `#needs-decision` tag and a short proposal callout).  
    - Option A: Move the note to `Ingest/Decisions/` and add frontmatter: `proposal_path: "1-Projects/Genesis-Mythos/..."`, `approved: false`.  
    - **One-tap approve:** User sets `approved: true` in frontmatter (or adds a single approval tag). On next EAT-QUEUE or “Process Decisions” run, agent moves the note to `proposal_path` (after snapshot + dry_run move) and logs.
  - **Approval flow tie-in:** When a decision note in `Ingest/Decisions/` is approved (`approved: true` + `decision_selected`), the next EAT-QUEUE run will automatically move the original file to the chosen path and set the decision note `status: resolved`.
  - **Hidden:** If “hidden” means “excluded from main Ingest sweep,” add `Ingest/Decisions/` to the list of paths that are not auto-processed by full ingest (only by a dedicated “Process Decisions” or “Approve & next” queue mode).
4. **Non-markdown in Ingest**
  Per existing rules: create companion .md; attempt move of original to `5-Attachments/` by type; on failure leave in Ingest with `#needs-manual-move` and log.
5. **Order of operations**
  - Backup → classify batch → move high-confidence to PARA → archive junk → leave low-confidence in Ingest or move to Ingest/Decisions/ with proposal → document “Approve & next” in Queue-Sources or pipeline reference.

---

## 6. Opinionated: performance vs fidelity, and broken paths

**Performance vs fidelity (Phase 6):**  
The current line “Performance vs visual fidelity; 60 FPS baseline” is ambiguous and can lead to fidelity creep. **Recommendation:** Treat **60 FPS as fixed**. Then:  

- Set a performance budget (e.g. 16.6 ms frame time); profile and keep LOD, draw distance, shadow resolution, and post-processing under that budget.  
- Add an explicit task: “Lock 60 FPS as non-negotiable; tune LOD, draw distance, shadow quality to meet it” and avoid “balance” wording that implies trading FPS for fidelity.  
- Document in the phase or in a short “Performance contract” note: we reduce fidelity (e.g. shadow distance, LOD tiers) until 60 FPS is stable, not the reverse.

**Other risks:**  

- **Phase 3 and 5:** “Lore → NPC dialogue” and “faction simulation” can become scope creep. Keep data schemas and one clear integration point per system (lore DB, faction state) and defer “AI agent for dialogue” to a later sub-phase or separate phase so the wizard and first-playable slice stay shippable.  
- **Modding:** Call out as “low” priority and post-MVP; scriptable events and custom archetypes are stretch goals so core loop (map → terrain → first-person + DM cam) is not delayed.

---

## 7. Deliverable: structured markdown for the new master file

The **new master roadmap note** (e.g. `Genesis-Mythos-Roadmap-2026-03-02-1430.md` or next timestamp per [Naming-Conventions](3-Resources/Second-Brain/Naming-Conventions.md)) will:

1. **Frontmatter**
  `title`, `created`, `tags`, `para-type`, `status`, `roadmap-level: master`, `project-id: genesis-mythos`, `highlight_perspective: geosynchronous-view`, `links` (MOC, key docs). **No** `phase-number`. Optional: `decision_selected` only if a master-level decision exists.
2. **Body**
  - Short **vision paragraph** (geosynchronous flow: Maps → Terrain3D → Lore → Combat → Politics → Wizard; 37 km², 60 FPS, moddable, first-person + DM cam).  
  - **## Phase 1 — Maps** (no checkboxes) + one Dataview TABLE from `Phase-1-Maps`.  
  - Same for Phases 2–6.  
  - **## Related** with links to [[Genesis-Mythos-Roadmap-MOC]], [[Genesis-Mythos-README]], [[Terrain3D-Integration-Guide-...]], [[World-Building]], [[Mythos Tabletop]].  
  - Optional: one rollup Dataview (all phases, open task count if available).
3. **No tasks**
  All `- [ ]` live only in the phase roadmap notes under `Phase-X-Name/`.

**Phase roadmap notes** (existing six files):  

- Update each with the **expanded task list** from §3 (5–15 tasks per phase, with [high]/[medium]/[low] in the task line or in a small table).  
- Ensure frontmatter includes `dependencies` (e.g. Phase 2 → `[[Phase-1-Maps-Roadmap-...]]`).  
- Add optional `decision_selected` when a decision note has approved an option.

---

## 8. Implementation order

1. **Document** the full frontmatter contract (including `decision_selected`; phase/subphase only for `decision_selected`) in [Roadmap-Standard-Format.md](3-Resources/Roadmap-Standard-Format.md) and optionally in the master note.
2. **Create** [Genesis-Mythos-Roadmap-MOC.md](1-Projects/Genesis-Mythos/Genesis-Mythos-Roadmap-MOC.md) (if it doesn't exist) with a single Dataview block that lists every phase and sub-phase note sorted by `phase-number`.
3. **Create** the new master roadmap file with the structure in §7 (vision, phase headings, Dataview only; no checkboxes).
4. **Update** each of the six phase roadmap notes with the expanded 5–15 prioritized subtasks from §3.
5. **Add** the optional rollup Dataview to the master if your environment supports `file.tasks` or Tasks plugin (or omit the Open column per §4 fallback).
6. **Implement** Ingest/Decisions/ and “Approve & next” (including approval → move + `status: resolved`) in queue/pipeline docs and, if desired, in a small context rule or skill.
7. **Run** Ingest triage in batches (backup → classify → move high-confidence → archive junk → low-confidence to Decisions or proposal).

No edits to the codebase or vault are made in plan mode; the above is the specification for you or a follow-up run to execute.