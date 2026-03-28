---
name: normalize-roadmap-mocs-and-templates
overview: Normalize roadmap Dataview MOC chains so each level scopes to its own children, fix existing genesis-mythos-master roadmap note formatting, and add reusable roadmap templates under Templates/Roadmap.
todos:
  - id: audit-current-roadmap-dataviews
    content: Audit existing genesis-mythos-master roadmap notes and their Dataview blocks (MOC, master, phase, secondary) against the intended hierarchy in Roadmap Structure.md.
    status: completed
  - id: define-normalized-dataview-patterns
    content: Define normalized Dataview patterns for each roadmap level (MOC, master, phase, secondary), limiting results to direct parents/children/grandchildren, with the master MOC as the only global table.
    status: completed
  - id: fix-genesis-roadmap-formatting
    content: Fix duplicated frontmatter/sections and normalize Dataview blocks in genesis-mythos-master roadmap notes, including adding a tertiary table to Phase-1-1-Core-Abstractions-Roadmap-2026-03-10-1210.md.
    status: completed
  - id: create-roadmap-templates
    content: Create standardized roadmap templates under Templates/Roadmap (master, phase, secondary, tertiary) using the normalized Dataview patterns.
    status: completed
  - id: docs-alignment-check
    content: Review Roadmap Structure.md and related docs to ensure they describe the updated MOC chain behavior and reference the new templates.
    status: completed
isProject: false
---

## Normalize roadmap MOC chain & templates

### 1. Audit existing roadmap notes and Dataview blocks

- **Scan current roadmap notes for `genesis-mythos-master`**:
  - Master roadmap: `[1-Projects/genesis-mythos-master/Roadmap/genesis-mythos-master-Roadmap-2026-03-10-1200.md](/home/darth/Documents/Second-Brain/1-Projects/genesis-mythos-master/Roadmap/genesis-mythos-master-Roadmap-2026-03-10-1200.md)`.
  - Phase 1 roadmap: `[1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-Core-Architecture/Phase-1-Conceptual-Foundation-Core-Architecture-Roadmap-2026-03-10-1200.md](/home/darth/Documents/Second-Brain/1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-Core-Architecture/Phase-1-Conceptual-Foundation-Core-Architecture-Roadmap-2026-03-10-1200.md)`.
  - Secondary 1.1 roadmap: `[1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-Core-Architecture/Phase-1-1-Core-Abstractions/Phase-1-1-Core-Abstractions-Roadmap-2026-03-10-1210.md](/home/darth/Documents/Second-Brain/1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-Core-Architecture/Phase-1-1-Core-Abstractions/Phase-1-1-Core-Abstractions-Roadmap-2026-03-10-1210.md)`.
  - Roadmap MOC: `[1-Projects/genesis-mythos-master/genesis-mythos-master-Roadmap-MOC.md](/home/darth/Documents/Second-Brain/1-Projects/genesis-mythos-master/genesis-mythos-master-Roadmap-MOC.md)`.
- **Compare them to the intended structure in** `[Roadmap Structure.md](/home/darth/Documents/Second-Brain/Roadmap Structure.md)`:
  - Confirm how each level is supposed to behave as a MOC (master → phases; phase → secondaries; secondary → tertiaries; tertiary → tasks only).
  - Identify mismatches, e.g. duplicated frontmatter/sections in the Phase 1 note and missing Dataview block in the secondary 1.1 note.

### 2. Define normalized Dataview patterns per level

- **Project Roadmap MOC** (`genesis-mythos-master-Roadmap-MOC.md`):
  - Keep the existing global table as the **only** exception that can see the entire project tree:
    - `FROM "1-Projects/genesis-mythos-master/Roadmap"`.
    - `WHERE roadmap-level IN ("master","primary","secondary","tertiary","task")`.
    - `TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Roadmap", subphase-index AS "Index", status, progress AS "%"`.
- **Master roadmap note** (`genesis-mythos-master-Roadmap-*.md`):
  - For each phase section, use a per-phase Dataview block:
    - `FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-N-<Name>"`.
    - `WHERE roadmap-level IN ("primary","secondary","tertiary")`.
    - Same standard TABLE columns and `SORT subphase-index ASC, file.name ASC`.
- **Phase roadmap notes** (`Phase-N-<Name>-Roadmap-*.md`):
  - Under `## Subphases & notes`, use a block scoped to that phase folder only:
    - `FROM "…/Roadmap/Phase-N-<Name>"`.
    - `WHERE roadmap-level IN ("primary","secondary","tertiary")`.
    - Standard TABLE + `SORT subphase-index ASC, file.name ASC`.
- **Secondary roadmap notes** (like `Phase-1-1-Core-Abstractions-Roadmap-2026-03-10-1210.md`):
  - Add `## Tertiary notes` with a Dataview block scoped to the secondary folder:
    - `FROM "…/Phase-1-1-Core-Abstractions"`.
    - `WHERE roadmap-level IN ("secondary","tertiary","task")`.
    - Same standard TABLE + `SORT subphase-index ASC, file.name ASC`.
  - This makes the secondary a proper MOC for its direct tertiaries and any future task-level notes.
- **Tertiary notes** (e.g. `Phase-1-1-3-Rendering-Input.md`):
  - Do **not** add Dataview MOC tables; keep them as task containers (checklists / pseudo-code) with proper `roadmap-level: tertiary` and `subphase-index: "N.M.K"`.

### 3. Clean up formatting and duplicates in existing genesis-mythos-master roadmap notes

- **Phase 1 roadmap** (`Phase-1-Conceptual-Foundation-Core-Architecture-Roadmap-2026-03-10-1200.md`):
  - Remove duplicated frontmatter and repeated `## Phase 1`/`## Subphases & notes` sections, leaving a single frontmatter block and one `## Subphases & notes` section with the normalized Dataview described above.
- **Master roadmap** (`genesis-mythos-master-Roadmap-2026-03-10-1200.md`):
  - Verify each phase section’s Dataview matches the per-phase pattern (scoped `FROM` path, standard columns, and filters) and adjust if any section diverges.
- **Secondary 1.1 roadmap**:
  - Append the `## Tertiary notes` Dataview block scoped to its folder.
  - Ensure frontmatter has `roadmap-level: secondary`, `phase-number: 1`, `subphase-index: "1.1"`, and `project-id: genesis-mythos-master`.
- **Other phase roadmaps** (Phases 2–6):
  - Apply the same phase-level Dataview normalization (scoped folders, standard TABLE) and fix any duplicated sections or inconsistent filters.

### 4. Introduce standard roadmap templates under Templates/Roadmap

- **Create a new `Templates/Roadmap/` subfolder** (name exactly `Roadmap` under `Templates`) and add:
  - `**Templates/Roadmap/Roadmap-Master-Template.md`**:
    - Frontmatter stub: `roadmap-level: master`, `phase-number: 0`, `project-id`, etc.
    - Body sections: provenance, per-phase sections with placeholder Dataview blocks following the per-phase pattern, and `## Related`.
  - `**Templates/Roadmap/Roadmap-Phase-Template.md`**:
    - Frontmatter for `roadmap-level: primary`, `phase-number: N`.
    - `## Phase N — <Name>` narrative and checklist placeholders.
    - `## Subphases & notes` with a Dataview block scoped to the phase folder.
  - `**Templates/Roadmap/Roadmap-Secondary-Template.md**`:
    - Frontmatter for `roadmap-level: secondary`, `phase-number: N`, `subphase-index: "N.M"`.
    - Narrative / responsibility sections.
    - `## Tertiary notes` Dataview scoped to the secondary folder.
  - `**Templates/Roadmap/Roadmap-Tertiary-Template.md**`:
    - Frontmatter for `roadmap-level: tertiary`, `subphase-index: "N.M.K"`.
    - Heading and a structured checklist / pseudo-code section for tasks; **no** Dataview.
- Ensure each template uses the **same standard Dataview TABLE signature** (Level, Note, Index, status, progress) and consistent `FROM`/`WHERE` clauses so future roadmap generations are uniform.

### 5. Align docs and future runs

- **Update docs if needed** in `Roadmap Structure.md` or `Roadmap-Upgrade-Plan.md` only to:
  - Confirm that the MOC chain convention (master → phase → secondary → tertiary) now explicitly includes the Dataview scoping patterns above.
  - Mention the new `Templates/Roadmap/`* files as the canonical source for future roadmap note creation.
- **After implementation**, plan a quick manual audit:
  - Open the MOC, master roadmap, Phase 1 roadmap, and the Core Abstractions secondary roadmap; confirm that:
    - Each Dataview shows only parents/children/grandchildren as intended.
    - There are no duplicated sections or mismatched frontmatter.
  - Optionally, run a small RESUME-ROADMAP deepen on Phase 1 and verify that newly created secondaries/tertiaries match the templates and appear correctly in the local MOC tables.

