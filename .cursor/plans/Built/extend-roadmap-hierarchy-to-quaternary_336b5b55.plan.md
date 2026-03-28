---
name: extend-roadmap-hierarchy-to-quaternary
overview: Extend the normalized roadmap MOC chain and templates to handle quaternary (and deeper) roadmap levels, treating tertiary as MOCs for quaternary and quaternary+ as leaf/task notes, and align docs accordingly.
todos: []
isProject: false
---

## Extend roadmap hierarchy to quaternary+

### 1. Generalize normalized Dataview patterns (building on existing step 2)

- **Keep existing levels intact**:
  - MOC: `[1-Projects/genesis-mythos-master/genesis-mythos-master-Roadmap-MOC.md](/home/darth/Documents/Second-Brain/1-Projects/genesis-mythos-master/genesis-mythos-master-Roadmap-MOC.md)` remains the **only** global view over `Roadmap/`.
  - Master and Phase notes keep their phase- and folder-scoped Dataview blocks using the canonical TABLE:

```dataview
    TABLE WITHOUT ID
      roadmap-level AS "Level",
      file.link AS "Roadmap",
      subphase-index AS "Index",
      status AS "Status",
      progress AS "% Progress"
    

```

- **Secondary notes (unchanged MOC role)**:
  - Continue to act as MOCs for **tertiary** notes and any task-level notes in the same folder:

```dataview
    TABLE WITHOUT ID
      roadmap-level AS "Level",
      file.link AS "Roadmap",
      subphase-index AS "Index",
      status AS "Status",
      progress AS "% Progress"
    FROM "…/Phase-N-M-<Secondary-Name>"
    WHERE roadmap-level IN ("secondary","tertiary","task")
    SORT subphase-index ASC, file.name ASC
    

```

- **Tertiary notes upgraded to mini-MOCs**:
  - Treat tertiary notes as MOCs for **quaternary** (and possibly deeper) children under a dedicated folder (`Phase-N-M-K-<Name>/`):
    - Add a `## Quaternary notes` section to tertiary templates and existing tertiary notes when you create children:

```dataview
      TABLE WITHOUT ID
        roadmap-level AS "Level",
        file.link AS "Roadmap",
        subphase-index AS "Index",
        status AS "Status",
        progress AS "% Progress"
      FROM "1-Projects/<project-id>/Roadmap/Phase-N-<Phase-Name>/Phase-N-M-<Secondary-Name>/Phase-N-M-K-<Tertiary-Name>"
      WHERE roadmap-level IN ("tertiary","quaternary","task")
      SORT subphase-index ASC, file.name ASC
      

```

- **Quaternary+ notes as leaves**:
  - Define **quaternary and deeper** roadmap notes as **leaf/task containers**:
    - `roadmap-level: quaternary` (or later `quinary`, etc., if you decide to enumerate them).
    - `subphase-index: "N.M.K.L"` for quaternary (extend dot notation for deeper levels as needed, e.g. `"1.1.3.2"`).
    - Body contains checklists and pseudo-code only; **no Dataview**.
  - Tertiary MOCs are responsible for listing these children; children do not list further descendants unless you explicitly push to 5+ depth by repeating the quaternary pattern.

### 2. Extend templates (building on existing step 4)

- **Add `Templates/Roadmap/Roadmap-Quaternary-Template.md`**:
  - Frontmatter (leaf-level):

```yaml
    ---
    title: "Phase N.M.K.L — <Quaternary Name>"
    roadmap-level: quaternary
    phase-number: N
    project-id: <project-id>
    status: active
    priority: high
    progress: 0
    created: {{date:YYYY-MM-DD}}
    tags: [roadmap, <project-id>, quaternary]
    para-type: Project
    links:
      - "[[Phase-N-M-K-<Tertiary-Name>-Roadmap-YYYY-MM-DD-HHMM]]"
    subphase-index: "N.M.K.L"
    ---
    

```

- Body skeleton:

```markdown
    ## Phase N.M.K.L — <Quaternary Name>

    <Short description of this quaternary subphase.>

    ### Tasks / pseudo-code

    - [ ] Task 1
    - [ ] Task 2
    - [ ] Task 3

    

```text
    // Optional pseudo-code / APIs / edge cases
    

```

```

  - For **deeper than quaternary (N>4)**, reuse this template, incrementing the dot-notation in `subphase-index` and adjusting `roadmap-level` if you decide to add more enums later.

- **Update `Templates/Roadmap/Roadmap-Tertiary-Template.md`**:
  - Keep it as a tertiary note but upgrade it to include a `## Quaternary notes` block (scoped to its own folder) using the canonical TABLE, as in the Dataview snippet above.
  - Clarify in comments that tertiary acts as MOC for quaternary+, while quaternary+ are leaves.

### 3. Align docs and aggressive-deepening behavior (building on existing step 5)

- **Update `Roadmap Structure.md`** to reflect the extended hierarchy:
  - **MOC chain**:
    - Project MOC → master (roadmap-level: master).
    - Master → phases (primary) via per-phase Dataview blocks.
    - Phase → secondaries via `Subphases & notes` scoped to each `Phase-N-<Name>/` folder.
    - Secondary → tertiaries via `Tertiary notes` in the secondary folder.
    - Tertiary → quaternary+ via `Quaternary notes` scoped to `Phase-N-M-K-<Name>/`.
    - Quaternary+ → **leaf** task/pseudo-code notes (no Dataview).
  - **Frontmatter `subphase-index`**:
    - Explicitly document dot-notation depth: `"1"` (phase), `"1.1"` (secondary), `"1.1.3"` (tertiary), `"1.1.3.2"` (quaternary), and note that further depths simply extend the chain.

- **Connect to aggressive deepening**:
  - In `Roadmap Structure.md` or `Roadmap-Upgrade-Plan.md`, add a short paragraph:
    - “When running RESUME-ROADMAP with aggressive parameters (see `Roadmap-Quality-Guide#Aggressive deepening`), the system may auto-create quaternary (and deeper) notes under tertiary parents when drift > 0.08 or the configured `tech_level` for a phase demands more detail. Tertiary notes should then act as MOCs for these deeper leaves via their `## Quaternary notes` Dataview block.”
  - Cross-link to `Roadmap-Quality-Guide#Aggressive deepening` so the levers (drift threshold, depth caps, etc.) are documented in one place while `Roadmap Structure.md` stays focused on hierarchy and MOC behavior.

This plan builds directly on your existing normalization work: it generalizes the Dataview/MOC chain past tertiary, introduces a dedicated quaternary template, and updates the structure docs so future deepen runs and manual note creation follow the same rules.
```

