---
name: roadmap-generate-from-outline
description: Creates a full project roadmap tree (master + phase notes + MOC) from a high-level roadmap outline note. Triggered by ROADMAP MODE (or a dedicated queue mode), not from ingest apply-mode.
---

# roadmap-generate-from-outline

## When to use

- When the user runs **ROADMAP MODE – generate from outline** (or a dedicated queue mode) with a note path: the note may be in Ingest, in a PARA folder, or elsewhere. The skill creates project + Roadmap/ + master + phase notes + MOC from that note.
- **Preferred seed note:** Note whose filename contains `Master-Goal` or `MasterGoal` and resides directly under the project root folder (`1-Projects/<project-id>/…`). If multiple candidates, prefer the one with highest `created` timestamp or explicit `roadmap-seed: true` frontmatter.
- **Previously** this skill was invoked from ingest apply-mode when the user chose Option A on a roadmap Decision Wrapper; that path was removed so ingest only captures and places notes. Roadmap tree creation is now a separate concern.
- Inputs are provided by the trigger (e.g. queue entry or ROADMAP MODE): path to the outline note (`original_note` or `source_file`), optional `suggested_project_name`, optional `user_guidance` or Thoughts text.

This skill **does not** run from ingest. It:

1. Creates a project folder and `Roadmap/` subtree.
2. Creates a **master roadmap** note (no checkboxes).
3. Creates **phase roadmap** notes (tasks allowed).
4. Moves the original seed into `Roadmap/` as a source note.
5. Sets provenance and generation status on the master.

## Inputs

- `original_note`: vault-relative path of the seed note (from wrapper `original_path`).
- `suggested_project_name`: project slug or name (from wrapper or original frontmatter, e.g. `project-id`).
- `guidance_text` (optional): freeform text from the wrapper’s **Thoughts / corrections / why this location?** block or `user_guidance`.

## High-level behavior

1. **Backup & snapshot safety**
   - Ensure `obsidian_create_backup` has already been called for `original_note` in the ingest/apply pipeline (per `mcp-obsidian-integration` and `para-zettel-autopilot`). If not, run it before any structural writes.
   - Before **moving** the original seed note, create a **per-change snapshot** via the `obsidian-snapshot` skill (`type: "per-change"`) so the original state is recoverable.

2. **Read and parse the seed**
   - Use `obsidian_read_note(original_note)` to obtain:
     - Frontmatter (title, `project-id`, tags, `is_roadmap`, etc.).
     - Body headings and bullet structure.
   - Detect candidate phases from the outline:
     - Use top-level or second-level headings that enumerate systems/phases, e.g. `## 1. Paddle Controls`, `## 2. Ball Physics`, etc.
     - For each heading, extract:
       - A **phase display name** (e.g. `Paddle Controls`, `Ball Physics`).
       - A short **seed sentence** (the paragraph under that heading) describing the system.

3. **Intent / ambiguity check (lightweight)**
   - Using the guidance + parsed content, check for **conflicting or vague statements** about:
     - What the game / system is for (player outcome).
     - Whether a system is core vs optional.
   - If confidence in the **phase decomposition** or project name is **very low** (e.g. <75%) even after considering `guidance_text`, do **not** create a second wrapper here (that’s a future enhancement). Instead:
     - Prefer a conservative structure:
       - Use a single-phase roadmap or fewer phases.
       - Document uncertainty in the master’s provenance callout (see below).
     - Continue with generation; provenance makes the ambiguity visible instead of blocking the pipeline.

4. **Target folder layout**

Use the **Roadmap Standard Format** folder structure:

- Project root: `1-Projects/<ProjectName>/`
- Roadmap root: `1-Projects/<ProjectName>/Roadmap/`
- Phase folders (one per detected system/phase, depth ≤4):

  - `1-Projects/<ProjectName>/Roadmap/Phase-1-<Name>/`
  - `1-Projects/<ProjectName>/Roadmap/Phase-2-<Name>/`
  - …

Implementation:

- Derive `<ProjectName>` from:
  - `suggested_project_name` (preferred), or
  - fallback from the seed note title (slugified).
- Use `obsidian_ensure_structure` for:
  - `1-Projects/<ProjectName>/Roadmap/`
  - Each `Phase-N-<Name>/` folder.

5. **Master roadmap note**

- Path:
  - `1-Projects/<ProjectName>/Roadmap/<ProjectName>-Roadmap-YYYY-MM-DD-HHMM.md`
  - Use current date/time in the filename to avoid collisions.

- Frontmatter (merge/adapt from Roadmap-Standard-Format):

  ```yaml
  title: <ProjectName> Roadmap
  roadmap-level: master
  phase-number: 0
  project-id: <ProjectName>
  status: active
  priority: high
  progress: 0
  created: YYYY-MM-DD
  tags: [roadmap, project, <project-slug>]
  para-type: Project
  links:
    - "[[<ProjectName>-Roadmap-MOC]]"
  roadmap_generation_status: complete
  ```

- Body sections:
  1. **Title**: `# <ProjectName> Roadmap`
  2. **Provenance callout** at the very top:

     > \[!info] Generation provenance  
     > Generated from `[[<SourceNote>]]` on `<ISO timestamp>`  
     > Wrapper: `[[<WrapperNote>]]` (`wrapper_type: roadmap`, option A)  
     > Guidance: short 1–2 sentence paraphrase of `guidance_text` (or “No additional guidance provided.”).  
     > Intent confidence: {high/medium/low} (based on how clear the seed + guidance are).

  3. **Source link** line:

     - `Source: [[<SourceNote>]]`

  4. **Per-phase headings and Dataview blocks**:

     For each detected phase `N`:

     - Heading:
       - `## Phase N — <PhaseName>`
     - Short **phase description**:
       - 1–3 sentences remixing the seed text into a small goal/risk/scope summary (not just copying the original line).
     - Dataview block following [Roadmap Standard Format]:

       ```dataview
       TABLE WITHOUT ID file.link AS "Sub-Phase", status, priority, progress AS "%"
       FROM "1-Projects/<ProjectName>/Roadmap/Phase-N-<PhaseNameSlug>"
       WHERE roadmap-level = "phase" OR roadmap-level = "subphase"
       SORT file.name ASC
       ```

  5. **Related section**:

     - `## Related`
     - Bullets for:
       - `[[<ProjectName>-Roadmap-MOC]]`
       - `[[<SourceNote>]]`

6. **Phase roadmap notes**

For each detected phase `N` with display name `<PhaseName>` and seed sentence:

- Path:
  - `1-Projects/<ProjectName>/Roadmap/Phase-N-<PhaseNameSlug>/Phase-N-<PhaseNameSlug>-Roadmap-YYYY-MM-DD-HHMM.md`

- Frontmatter:

  ```yaml
  title: Phase N — <PhaseName>
  roadmap-level: phase
  phase-number: N
  project-id: <ProjectName>
  status: active
  priority: high
  progress: 0
  created: YYYY-MM-DD
  tags: [roadmap, <project-slug>, phase]
  para-type: Project
  links:
    - "[[<ProjectName>-Roadmap-YYYY-MM-DD-HHMM]]"
  ```

- Body:
  - Heading: `## Phase N — <PhaseName>`
  - **Enriched description**: a short paragraph that:
    - Starts from the seed sentence.
    - Adds 1–2 clarifying phrases about intent, constraints, or player experience.
  - **Placeholder tasks** (minimal but structured), e.g.:

    ```markdown
    - [ ] Core implementation task 1
    - [ ] Core implementation task 2
    - [ ] Glue / integration task
    ```

  - Do **not** add dependencies/estimates yet; those will come later via TASK-ROADMAP / ADD-ROADMAP-ITEM / EXPAND-ROAD-ASSIST.

7. **Project roadmap MOC**

- Path:
  - `1-Projects/<ProjectName>/<ProjectName>-Roadmap-MOC.md`
- If the MOC already exists, **append or merge** the roadmap section instead of overwriting.
- Minimal structure:

  ```markdown
  ---
  title: <ProjectName> Roadmap MOC
  created: YYYY-MM-DD
  tags: [roadmap, moc, <project-slug>]
  para-type: Project
  status: active
  project-id: <ProjectName>
  links: ["[[<ProjectName>-Roadmap-YYYY-MM-DD-HHMM]]"]
  ---

  # <ProjectName> — Roadmap MOC

  ## Master roadmap

  - [[<ProjectName>-Roadmap-YYYY-MM-DD-HHMM]]

  ## All phase roadmaps

  ```dataview
  TABLE WITHOUT ID file.link AS "Roadmap", roadmap-level, status, progress AS "%"
  FROM "1-Projects/<ProjectName>/Roadmap"
  WHERE roadmap-level = "phase" OR roadmap-level = "subphase" OR roadmap-level = "master"
  SORT phase-number ASC, file.name ASC
  ```
  ```

8. **Move the original seed note**

- After master + phases + MOC are written successfully:
  - Move `original_note` from `Ingest/...` to:
    - `1-Projects/<ProjectName>/Roadmap/Source-<OriginalSlug>-YYYY-MM-DD-HHMM.md`
  - Use:
    - `obsidian_ensure_structure` for the `Roadmap/` folder (already ensured above).
    - `obsidian_move_note` with `dry_run: true` then `dry_run: false`.
  - Do **not** alter the original seed content (beyond what ingest may already have done); treat it as a historical source.

9. **Optional polish (future-safe hooks)**

These steps are **optional** but recommended when confidence is high and performance allows:

- Run **autonomous-express** (EXPRESS MODE) on the **master roadmap** to:
  - Create a TL;DR / mini-outline header via `express-mini-outline`.
  - Append a call-to-action block if appropriate.
- Optionally run **autonomous-distill** on individual phase notes later to apply `distill-highlight-color` and progressive summarization.

Current implementation may skip these in the first version; the important part is that the master structure, provenance, and phase notes exist and are consistent with `Roadmap-Standard-Format`.

10. **Logging and wrapper cleanup**

- Log a `CHECK_WRAPPERS` entry in `3-Resources/Ingest-Log.md`, e.g.:
  - `CHECK_WRAPPERS: <timestamp> | Roadmap created for <ProjectName> (Option A) | Project | created master + N phases + MOC; moved original to Roadmap/Source; wrapper archived | 85% | 1-Projects/<ProjectName>/Roadmap/ | `
- After success:
  - Set `used_at` and/or `processed: true` on the wrapper.
  - Move the wrapper to `4-Archives/Ingest-Decisions/` (per auto-eat-queue and para-zettel-autopilot).

## MCP tools

- `obsidian_read_note` — read the seed roadmap outline.
- `obsidian_ensure_structure` — ensure project root, `Roadmap/`, and phase folders exist.
- `obsidian_update_note` — create/update master roadmap, phase notes, and MOC.
- `obsidian_create_backup` — ensure backup exists before structural operations (if ingest did not already run it in this apply-mode cycle).
- `obsidian_move_note` — move the original seed from `Ingest/` to the project `Roadmap/Source-...` path (dry_run then commit).
- `obsidian-snapshot` skill — per-change snapshot before moving the original or performing other destructive changes.

## Confidence gate

- Use the ingest/apply-mode **`ingest_conf`** (and any `guidance_conf_boost`) as the primary signal.
- **≥85%**: Create project + roadmap tree as described.
- **<85%**: Do **not** make structural changes; leave the wrapper and seed note as-is and log a low-confidence proposal (e.g. suggested project name and phases) into Ingest-Log.md with `#review-needed`.

