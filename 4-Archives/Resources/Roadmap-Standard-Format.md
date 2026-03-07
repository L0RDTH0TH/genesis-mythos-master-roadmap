---
title: Roadmap Standard Format
created: 2026-03-02
tags: [roadmap, tasks, dataview, second-brain, para]
para-type: Resource
status: active
links: ["[[Resources Hub]]", "[[Master Goal]]"]
---

# Roadmap Standard Format

Canonical structure for project roadmaps: **master hub (no tasks)** + **phase/sub-phase roadmap notes (tasks allowed)**. Normalized for Dataview, Tasks plugin, and EAT-QUEUE (TASK-ROADMAP, roadmap-ingest, add-roadmap-append, expand-road-assist). Enforced via roadmap-ingest and backbone-docs-sync.

---

## Folder layout (≤4 levels)

Keep depth ≤4 levels under the project. Example:

```
1-Projects/<Project>/Roadmap/
├── <Project>-Roadmap-YYYY-MM-DD-HHMM.md          ← master (no checkboxes/tasks)
├── Phase-1-<Name>/
│   ├── Phase-1-<Name>-Roadmap-YYYY-MM-DD-HHMM.md ← phase level (tasks + Dataview)
│   └── (optional) Subphase-X/                     ← sub-phase notes
├── Phase-2-<Name>/
│   └── …
└── …
```

**Example (Genesis-Mythos):**

```
1-Projects/Genesis-Mythos/Roadmap/
├── Genesis-Mythos-Roadmap-YYYY-MM-DD-HHMM.md     ← master
├── Phase-1-Maps/
│   ├── Phase-1-Maps-Roadmap-YYYY-MM-DD-HHMM.md
│   └── (optional) Subphase-X/
└── Phase-2-Terrain3D/
    └── …
```

---

## Master roadmap (high-level hub)

**MUST contain ZERO checkboxes or manual tasks.** It consists only of:

- **Standard frontmatter** with `roadmap-level: master` (see Frontmatter contract below).
- **Phase headings**: `## Phase N — <Name>` (e.g. `## Phase 1 — Maps`).
- **One Dataview TABLE or LIST per phase** that dynamically pulls sub-phase roadmap notes from that phase’s folder (see Dataview example below).
- **Related section or MOC links** at the bottom (e.g. `## Related` with `[[Project-Roadmap-MOC]]`, key docs, timeline).

No `- [ ]` or `- [x]` on the master note. All actionable tasks live in phase/sub-phase roadmap notes.

---

## Phase and sub-phase roadmaps

**Phase-level and sub-phase roadmap notes** (e.g. `Phase-1-Maps-Roadmap-….md`) **MAY** contain:

- A short **phase description paragraph** after each `## Phase N — <Name>` heading (goals, risks, scope).
- **Checkboxes/tasks** (`- [ ]`, `- [x]`) — this is the only place they are allowed in the hierarchy.
- **Further nested Dataview queries** (for deeper sub-sub-phases or task aggregation).
- **Or a mix** of tasks and Dataview blocks.

Phases can also link to dedicated **sub-roadmap notes** (e.g. `[[Phase-1-Maps-Sub-Roadmap]]`) that hold that phase’s detailed description, tasks, and their own Dataview blocks. Optional frontmatter `sub_roadmaps: ["Phase-1-Maps-Sub-Roadmap.md", ...]` allows Dataview aggregation across sub-roadmaps.

Use block-IDs (`^id`) and `(depends on: ^id)` for Task Complete validation. Optional: `📅 YYYY-MM-DD` or `⏳ date` for Tasks plugin.

---

## Frontmatter contract

Every roadmap note (master, phase, subphase) MUST include these fields. Pipelines and Dataview rely on them.

```yaml
roadmap-level: master | phase | subphase
phase-number: 1 | 2 | 3 | 4 | 5 | 6
status: active | blocked | done | deferred
priority: high | medium | low
dependencies: ["[[Other-Phase-Roadmap]]"]   # array or comma-separated links
progress: 0-100                             # integer or percentage string
highlight_perspective: geosynchronous-view   # or inherited from project
project-id: genesis-mythos                  # project slug
roadmap_generation_status: draft | complete # set to complete when roadmap-generate-from-outline has built the master + phases + MOC
```

**Standard frontmatter** (all roadmap notes): `title`, `created`, `tags`, `para-type`, `status`, `links`. Master and phase notes should link to the project roadmap MOC (e.g. `[[Genesis-Mythos-Roadmap-MOC]]`).

**Optional** (pipelines ignore if absent): `dataview_focus`, `min_conf`, `phase_desc_conf`, `sub_roadmaps`, `phase_index`, `resurface_after`, `archive_prep`, `depends-on` (task-ids). See [[3-Resources/Second-Brain/Parameters|Parameters]] for confidence bands.

---

## Dataview aggregation example

Use **precise** filters so custom tags or future fields do not cause false positives. Prefer explicit `roadmap-level` equality over `contains()`.

**Per-phase block in master roadmap** (adapt `FROM` path per phase folder):

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

**Why not `contains(roadmap-level, "phase")`:** Explicit `roadmap-level = "phase" OR roadmap-level = "subphase"` avoids false positives if someone adds custom tags or values later.

For other projects, replace the `FROM` path with `"1-Projects/<Project>/Roadmap/Phase-N-<Name>"`. If a query fails, check Obsidian Dataview docs for field names (e.g. `meta(section)`, `file.outlinks`).

---

## MOC behavior

- **Main (master) roadmap** always includes a link to the project roadmap MOC, e.g. `[[Genesis-Mythos-Roadmap-MOC]]`, in `links` or in a **Related** section at the bottom.
- **The MOC note** auto-aggregates all phase and sub-phase roadmaps via Dataview (e.g. TABLE/LIST over the project’s `Roadmap/` folder filtered by `roadmap-level`), similar to [[3-Resources/Vault-Change-Monitor|Vault-Change-Monitor]] style. One MOC per project; create it if missing when creating the master roadmap.

---

## When phases are added or removed

- Re-queue via **TASK-ROADMAP** (or ADD-ROADMAP-ITEM / EXPAND-ROAD); run **EAT-QUEUE** so roadmap-ingest (or the relevant skill) re-parses and updates the roadmap.
- For reorders: **REORDER-ROADMAP** uses **dry_run** first per [[.cursor/rules/always/mcp-obsidian-integration|mcp-obsidian-integration]].
- **All changes go through version-snapshot + dry_run before commit (per mcp-obsidian-integration).**
- Optional frontmatter `phase_index: true`: queue modes (e.g. REORDER-ROADMAP) may use this to refresh a phase index or Dataview-friendly structure when present.

---

## Future-proofing

- **Versioning:** Every substantive edit triggers version-snapshot (already in express pipeline); use for roadmap notes when appending or restructuring.
- **Re-ingest safety:** Feedback notes target specific phases without touching the master; keep master task-free so re-ingest does not add checkboxes there.
- **Graph/Dataview:** `project-id` and `phase-number` enable easy queries and graph traversal across roadmaps.
- **Scalability:** Pattern supports 6+ phase numbers and deeper nesting; tasks stay in leaf (phase/sub-phase) notes only.
- **Observability:** Optional `### Progress Log` section with Dataview from pipeline logs (see [[3-Resources/Second-Brain/Logs|Logs]]); optional `> [!feedback]` callout at end: "Add notes here; re-queue via EAT-QUEUE for refinement." ([[3-Resources/Second-Brain/Templates|Templates]])

---

## Quick-start

1. Create folder `1-Projects/<Project>/Roadmap/` and a master note: `<Project>-Roadmap-YYYY-MM-DD-HHMM.md` with `roadmap-level: master`, **no** checkboxes.
2. For each phase, create `Phase-N-<Name>/` and a phase roadmap note with `roadmap-level: phase`, tasks, and optional Dataview.
3. In the master, add `## Phase N — <Name>` and one Dataview block per phase (FROM that phase’s folder, WHERE `roadmap-level = "phase" OR roadmap-level = "subphase"`).
4. Add a **Related** section and link to `[[<Project>-Roadmap-MOC]]`; create the MOC if needed and add a Dataview that aggregates all phase/sub-phase roadmaps.
5. Queue from mobile (TASK-ROADMAP, Task Complete, Add Roadmap Item, etc.) and run **EAT-QUEUE** in Cursor to process.

See [[3-Resources/Mobile-Toolbar-Task-Commands]] for toolbar commands and [[Master Goal]] for philosophy. Example (legacy): [[1-Projects/Example/Roadmap/Example-Roadmap]].
