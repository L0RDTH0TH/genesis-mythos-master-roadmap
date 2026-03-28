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
- **`resume_from`** (optional): When set (e.g. `resume_from: 2`), skip phases 1..N-1; read existing master and phase notes from `Roadmap/`; generate only from phase N onward. Append/update master and MOC as needed. Output of each phase must end with a **"## Next Phase Hand-Off"** section: short summary + open TBDs + link to `[[roadmap-state]]` and `[[decisions-log]]`. Used by **roadmap-resume** when continuing a multi-run roadmap.

## High-level behavior

1. **Backup & snapshot safety**
   - Ensure `obsidian_create_backup` has already been called for `original_note` in the ingest/apply pipeline (per `mcp-obsidian-integration` and `para-zettel-autopilot`). If not, run it before any structural writes.
   - Before **moving** the original seed note, create a **per-change snapshot** via the `obsidian-snapshot` skill (`type: "per-change"`) so the original state is recoverable.

2. **Normalize seed if master goal**
   - After backup/snapshot, read the seed note once. If it is a **Project Master Goal** (`is_master_goal: true` in frontmatter **or** filename/path matches `*Master*Goal*` / `*MasterGoal*`), run the **normalize-master-goal** skill on `original_note` so the body follows [[Templates/Master-Goal]] (One-line, Vision, Phases, Technical Integration, TL;DR, Related). Then re-read the note for parsing. This ensures phase detection (step 3) sees a consistent structure; phases are expected under `## Phases` as `### Phase N — <Name>` or as top-level `## Phase N — <Name>`.

3. **Read and parse the seed**
   - Use `obsidian_read_note(original_note)` to obtain:
     - Frontmatter (title, `project-id`, tags, `is_roadmap`, etc.).
     - Body headings and bullet structure.
   - Detect candidate phases from the outline:
     - **If the seed follows the Master-Goal template**: Look for `## Phases` and parse `### Phase N — <Name>` (and any paragraph under each) for phase display name and seed sentence.
     - **Else**: Use top-level or second-level headings that enumerate systems/phases, e.g. `## 1. Paddle Controls`, `## 2. Ball Physics`, or `## Phase 1 — Name`.
     - For each heading, extract:
       - A **phase display name** (e.g. `Paddle Controls`, `Ball Physics`).
       - A short **seed sentence** (the paragraph under that heading) describing the system.

4. **Intent / ambiguity check (lightweight)**
   - Using the guidance + parsed content, check for **conflicting or vague statements** about:
     - What the game / system is for (player outcome).
     - Whether a system is core vs optional.
   - If confidence in the **phase decomposition** or project name is **very low** (e.g. <75%) even after considering `guidance_text`, do **not** create a second wrapper here (that’s a future enhancement). Instead:
     - Prefer a conservative structure:
       - Use a single-phase roadmap or fewer phases.
       - Document uncertainty in the master’s provenance callout (see below).
     - Continue with generation; provenance makes the ambiguity visible instead of blocking the pipeline.

5. **Target folder layout**

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

5b. **Create workflow_state.md if missing**

- **Path**: `1-Projects/<ProjectName>/Roadmap/workflow_state.md`
- When the Roadmap/ folder exists (after step 5), check if **workflow_state.md** exists there. If it does **not** exist, create it with the following schema (per [Vault-Layout § Roadmap state artifacts](3-Resources/Second-Brain/Vault-Layout.md) and **workflow_state ## Log table format**):
  - **Frontmatter**: `current_phase` (int; seed with 1 so first RESUME-ROADMAP has a clear target), `current_subphase_index` (null), `status` (in-progress), `automation_level` (semi), `last_auto_iteration` (empty or ISO timestamp), `iterations_per_phase` (e.g. `{}`), optional `max_iterations_per_phase` (from Config if set; else omit or use as optional hard ceiling), optional `max_iterations_total`, optional **`iteration_guidance_ranges`** (copy from Config `prompt_defaults.roadmap.iteration_guidance_ranges` when present: depth_1, depth_2, depth_3, depth_4_plus).
  - **Body**: `## Log` with an append-only table. The table **must** consist of exactly: **(1) header row** (12 columns: `Timestamp | Action | Target | Iter Obj | Iter Phase | Ctx Util % | Leftover % | Threshold | Est. Tokens / Window | Util Delta % | Confidence | Status / Next`), **(2) mandatory separator row** with 12 cells: `| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |`, **(3) optional seed row**. No table without the separator row — without it the table will not render as Markdown. See Vault-Layout § workflow_state ## Log table format (Markdown).
- Use `obsidian_update_note` (or equivalent) to create the file when missing. Snapshot **roadmap-state.md** before and after any state write (per mcp-obsidian-integration). When creating workflow_state for the first time, snapshot roadmap-state after creation so the "Phase 0 complete" state is captured.

6. **Master roadmap note**

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
       TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
       FROM "1-Projects/<ProjectName>/Roadmap/Phase-N-<PhaseNameSlug>"
       WHERE roadmap-level = "primary" OR roadmap-level = "secondary" OR roadmap-level = "tertiary"
       SORT subphase-index ASC, file.name ASC
       ```

  5. **Related section**:

     - `## Related`
     - Bullets for:
       - `[[<ProjectName>-Roadmap-MOC]]`
       - `[[<SourceNote>]]`

7. **Phase roadmap notes**

For each detected phase `N` with display name `<PhaseName>` and seed sentence:

- Path:
  - `1-Projects/<ProjectName>/Roadmap/Phase-N-<PhaseNameSlug>/Phase-N-<PhaseNameSlug>-Roadmap-YYYY-MM-DD-HHMM.md`

- Frontmatter:

  ```yaml
  title: Phase N — <PhaseName>
  roadmap-level: primary
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

  - **Subphases & notes (MOC block):** Add a section **"## Subphases & notes"** and a Dataview block so the phase note is a MOC from creation (per Roadmap Structure and MOC migration plan). Use canonical columns with Level: `TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"` with `FROM "1-Projects/<ProjectName>/Roadmap/Phase-N-<PhaseNameSlug>"`, `WHERE roadmap-level = "primary" OR roadmap-level = "secondary" OR roadmap-level = "tertiary"`, `SORT subphase-index ASC, file.name ASC`.
  - Do **not** add dependencies/estimates yet; those will come later via TASK-ROADMAP / ADD-ROADMAP-ITEM / EXPAND-ROAD-ASSIST.

8. **Project roadmap MOC**

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
  TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Roadmap", subphase-index AS "Index", status, progress AS "%"
  FROM "1-Projects/<ProjectName>/Roadmap"
  WHERE roadmap-level = "master" OR roadmap-level = "primary" OR roadmap-level = "secondary" OR roadmap-level = "tertiary" OR roadmap-level = "task"
  SORT phase-number ASC, subphase-index ASC, file.name ASC
  ```
  ```

9. **Move the original seed note**

- After master + phases + MOC are written successfully:
  - Move `original_note` from `Ingest/...` to:
    - `1-Projects/<ProjectName>/Roadmap/Source-<OriginalSlug>-YYYY-MM-DD-HHMM.md`
  - Use:
    - `obsidian_ensure_structure` for the `Roadmap/` folder (already ensured above).
    - `obsidian_move_note` with `dry_run: true` then `dry_run: false`.
  - Do **not** alter the original seed content (beyond what ingest may already have done); treat it as a historical source.

10. **Optional polish (future-safe hooks)**

These steps are **optional** but recommended when confidence is high and performance allows:

- Run **autonomous-express** (EXPRESS MODE) on the **master roadmap** to:
  - Create a TL;DR / mini-outline header via `express-mini-outline`.
  - Append a call-to-action block if appropriate.
- Optionally run **autonomous-distill** on individual phase notes later to apply `distill-highlight-color` and progressive summarization.

Current implementation may skip these in the first version; the important part is that the master structure, provenance, and phase notes exist and are consistent with `Roadmap-Standard-Format`.

11. **Logging and wrapper cleanup**

- Log a `CHECK_WRAPPERS` entry in `3-Resources/Ingest-Log.md`, e.g.:
  - `CHECK_WRAPPERS: <timestamp> | Roadmap created for <ProjectName> (Option A) | Project | created master + N phases + MOC; moved original to Roadmap/Source; wrapper archived | 85% | 1-Projects/<ProjectName>/Roadmap/ | `
- After success:
  - Set `used_at` and/or `processed: true` on the wrapper.
  - Move the wrapper to `4-Archives/Ingest-Decisions/` (per auto-eat-queue and para-zettel-autopilot).

12. **Mandatory post-processing (multi-run)**

When not in one-shot mode (i.e. when auto-roadmap runs the default multi-run path), after generating phase notes:

- **For each phase roadmap note** (or phase-output.md when phase-output sync is used):
  - Run **distill-highlight-color** with lens `roadmap-accuracy` (bias toward factual consistency, cross-references).
  - Derive or receive **per-phase confidence** (e.g. from distill or a lightweight scoring step).
  - **If phase conf < 85%:**
    - Do **not** mark the phase complete.
    - Create a Decision Wrapper in `Ingest/Decisions/Roadmap-Decisions/` (ensure structure via obsidian_ensure_structure) with options:
      - A: Accept anyway (risky)
      - B: Refine with guidance "Increase factual consistency and cross-check prior phases"
      - C: Revert this phase and regenerate from previous
      - D: Abort roadmap
  - **Else:**
    - Append to decisions-log: `- Phase {{n}}: [summary] [[phase-n-output or phase note]] (conf {{conf}}%)`
    - Append 🔵 core-decision highlights to distilled-core.md (frontmatter core_decisions and/or body).
- **Hand-off gate (when `handoff_gate_enabled` or payload `handoff_gate: true`):** For each phase, run **hand-off-audit** (see [hand-off-audit](.cursor/skills/hand-off-audit/SKILL.md)). Resolve high threshold from config (default 85) or **handoff_thresholds_by_tech** by phase tech_level. If **handoff_readiness < high threshold**: do **not** add phase to completed_phases; do **not** set phase status to ready-for-impl; create Decision Wrapper `wrapper_type: handoff-readiness` under `Ingest/Decisions/Roadmap-Decisions/` (use phase-direction template from Templates § Roadmap), pre-populate A–G with gap-filling options, add option R (re-try with auto-stub gen); link phase note and decisions-log; add `#review-needed`; optionally append to Mobile-Pending-Actions. If handoff_readiness ≥ high threshold, proceed with existing logic (append to decisions-log, update state, snapshot).
- **If recal was triggered and drift > drift_score_threshold** (from Parameters, default 0.08):
  - Force a Decision Wrapper with **"A: Revert to last safe phase"** as the default/first option (revert prioritized).
- **Update roadmap-state.md**: Set current_phase, last_run (YYYY-MM-DD-HHMM), and increment version. See roadmap-state schema in Vault-Layout.

Use **drift_score_threshold** and **conf_phase_complete_threshold** (85) from Parameters or Second-Brain-Config roadmap block. Snapshot roadmap-state before and after every state update (per mcp-obsidian-integration).

## MCP tools

- `obsidian_read_note` — read the seed roadmap outline.
- `obsidian_ensure_structure` — ensure project root, `Roadmap/`, and phase folders exist.
- `obsidian_update_note` — create/update master roadmap, phase notes, and MOC.
- `obsidian_create_backup` — ensure backup exists before structural operations (if ingest did not already run it in this apply-mode cycle).
- `obsidian_move_note` — move the original seed from `Ingest/` to the project `Roadmap/Source-...` path (dry_run then commit).
- `obsidian-snapshot` skill — per-change snapshot before moving the original or performing other destructive changes.

## Confidence gate

Entry-point split: behavior depends on how the skill was invoked.

- **ROADMAP MODE / queue entry (no ingest context)**  
  When the skill is invoked from ROADMAP MODE (or a queue entry with `mode: "ROADMAP MODE"`) or ROADMAP-ONE-SHOT, **do not use `ingest_conf`**. No ingest pipeline has run; that signal is undefined.
  - **Proceed** with generation when:
    - `original_note` / `source_file` exists and is readable, and
    - Project name is resolved (`suggested_project_name` from params or from seed frontmatter/title).
  - The only confidence guardrail for this path is the existing **step 4 (Intent / ambiguity check)**: if confidence in phase decomposition or project name is very low (e.g. <75%) after considering `guidance_text`, prefer conservative structure (e.g. single-phase or fewer phases) and document uncertainty in the master's provenance callout — but **do not block** structural creation (no "leave wrapper and seed as-is").
  - Backup and snapshot requirements (step 1) unchanged.

- **Ingest apply-mode (future)**  
  If the skill is ever invoked from a path that **supplies** `ingest_conf` (e.g. an approved roadmap Decision Wrapper that runs apply-mode and then calls this skill with the same run context), use **ingest_conf** (and any `guidance_conf_boost`) as the primary signal:
  - **≥85%:** Create project + roadmap tree as described.
  - **<85%:** Do not make structural changes; leave the wrapper and seed note as-is and log a low-confidence proposal (suggested project name and phases) into `3-Resources/Ingest-Log.md` with `#review-needed`.

*Current entry point is ROADMAP MODE only; ingest apply-mode path is reserved for a possible future re-introduction.*

