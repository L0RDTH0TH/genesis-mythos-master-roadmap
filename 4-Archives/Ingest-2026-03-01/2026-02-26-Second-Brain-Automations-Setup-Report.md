---
title: Second-Brain Automations Setup — Cursor + Obsidian
created: 2026-02-26
updated: 2026-02-26
tags: [pkm, automation, cursor, obsidian, pipelines, skills]
para-type: resource
status: active
links: ["[[Cursor Skill Pipelines Reference]]", "[[Second-Brain-Master-Goal-Audit-2026-02-26]]", "[[2026-02-26-Automation-Flows-MCP-Improvements]]"]
source: System-level automation overview for Thoth-AI + Obsidian MCP
---
### Purpose of this report

- **Goal**: Document how automations are currently configured across the vault: pipelines, skills, triggers, confidence gates, logging, and safety rails.
- **Scope**: Cursor-side skills, `.cursor/rules/**` pipeline rules, Obsidian MCP integration, snapshot/backup strategy, and how everything interacts with the PARA structure.

---

### 1. High-level architecture

- **Vault model**:
  - **PARA** roots: `1-Projects/`, `2-Areas/`, `3-Resources/`, `4-Archives/`.
  - **Ingest/** as the **only** entry point for new/unknown files (including non‑markdown).
- **Automation stack**:
  - **Cursor rules** (`.cursor/rules/always/**`, `.cursor/rules/context/**`) define:
    - Always-on constraints (backups, snapshots, no shell file ops, ingest bootstrap, MCP safety).
    - Context rules per pipeline (distill, archive, express, organize, ingest-processing, etc.).
  - **Cursor skills** (`.cursor/skills/<skill-name>/SKILL.md`) provide reusable operations plugged into pipelines:
    - E.g. `frontmatter-enrich`, `subfolder-organize`, `distill-highlight-color`, `version-snapshot`, etc.
  - **Obsidian MCP server** handles:
    - Note-level ops: `obsidian_read_note`, `obsidian_update_note`, `obsidian_move_note`, `obsidian_rename_note`, `obsidian_list_notes`, `obsidian_create_backup`, `obsidian_log_action`, `obsidian_ensure_structure`, plus snapshot/version helpers via skills.
- **Pipelines** (from `Cursor Skill Pipelines Reference`):
  - **full-autonomous-ingest** — capture → classify → organize → light distill → tasks → hub append → move.
  - **autonomous-distill** — periodic deepening of existing notes.
  - **autonomous-archive** — move completed/inactive items into `4-Archives/`.
  - **autonomous-express** — generate outlines/related content/CTAs from distilled notes.
  - **autonomous-organize** — re‑organize existing notes inside active PARA folders.

---

### 2. Trigger phrases → pipelines

From `Cursor Skill Pipelines Reference` and context rules:

- **full-autonomous-ingest**
  - **Triggers**: `"Ingest"`, `"process Ingest"`, `"run ingests"`, or any explicit reference to `Ingest/` / unprocessed captures.
  - **Rules**: `always-ingest-bootstrap` (always), `ingest-processing.mdc` (Ingest‑specific), Para‑Zettel Autopilot ingest logic.
- **autonomous-distill**
  - **Triggers**: `"DISTILL MODE – safe batch autopilot"`, `"distill this note"`, `"distill current file"`, `"refine this note"`, `"autonomous distill on folder X"`.
  - **Rule**: `.cursor/rules/context/auto-distill.mdc`.
- **autonomous-archive**
  - **Triggers**: `"ARCHIVE MODE – safe batch autopilot"`, `"archive this note"`, `"send to Archives"`, `"move completed to 4-Archives"`, or archive‑style language plus completion cues (`status: complete`, tags like `#eaten`).
  - **Rule**: `.cursor/rules/context/auto-archive.mdc`.
- **autonomous-express**
  - **Triggers**: `"EXPRESS MODE – safe batch autopilot"`, `"express this note"`, `"generate outline"`, `"create publishable summary"`, `"turn this into an outline/post"`.
  - **Rule**: `.cursor/rules/context/auto-express.mdc`.
- **autonomous-organize**
  - **Triggers**: `"ORGANIZE MODE – safe batch autopilot (on [folder])"`, `"re-organize this note"`, `"re-organize Projects and Resources"`, `"classify and move"`, `"put this note in the right folder"`.
  - **Rule**: `.cursor/rules/context/auto-organize.mdc`.
- **Global safety / MCP behavior**
  - **Rule**: `.cursor/rules/always/mcp-obsidian-integration.mdc` (backups, snapshot dirs, MCP fallbacks).
- **Garden review** (new flow; no dedicated context rule — interpret by agent)
  - **Triggers**: "GARDEN REVIEW", "run garden review", "orphans and distill candidates", "garden health", "vault orphans", "distill candidates sweep".
  - **Flow**: **`obsidian_garden_review`**(scope, focus: orphans | distill_candidates | weak_links | all, output_path optional, auto_apply). Suggest **`auto_apply: false`** by default during initial adoption. Downstream: feed autonomous-distill and autonomous-organize batches.
- **Curate cluster** (new flow; no dedicated context rule — interpret by agent)
  - **Triggers**: "CURATE CLUSTER #tag", "suggest gaps and merges for 3-Resources", "cluster curate #tag", "theme gaps #tag", "merge suggestions 3-Resources/…".
  - **Flow**: **`obsidian_curate_cluster`**(query: tag or folder, note_list optional, actions: suggest_gaps, suggest_merges, generate_synthesis). Suggest **`auto_apply: false`** by default during initial adoption. Client can call obsidian_split_atomic, obsidian_generate_moc, or merge proposals.

---

### 3. Safety model: backups, snapshots, and logging

#### 3.1 Backups

- **Backup root (`BACKUP_DIR`)**:
  - External‑style backups under a path like `/home/darth/Documents/Second-Brain-oops-Backups/`.
  - Created via `obsidian_create_backup` at the **start** of any pipeline that may change content, paths, or structure.
- **ensure_backup vs create_backup**:
  - Before long batches or after a gap (e.g. >15 minutes), call **`obsidian_ensure_backup`**(path, max_age_minutes) to confirm a recent backup exists; only call **`obsidian_create_backup`** when ensure_backup indicates one is needed or missing.
  - **Default value guidance**: Suggest `max_age_minutes: 1440` (24 hours) as a safe conservative default for most users/batches; allow tighter values (e.g. 60–180 min) for very active ingest runs. This prevents over-creation while still catching long-idle sessions.
- **Backup invariants**:
  - **No destructive action** (overwrite, append, move, rename, delete) is allowed until:
    - A backup exists for the note (via `obsidian_ensure_backup` check or `obsidian_create_backup` success in the current run), and
    - Confidence thresholds are met (see below) and per‑change snapshot succeeded if required.
  - If backup fails: pipeline for that note aborts; a `#review-needed` entry is logged.

#### 3.2 Snapshot directories

- **Per-change snapshots (`SNAPSHOT_DIR`)**:
  - Lives *inside* the vault under `Backups/Per-Change/`.
  - Holds hashed, flattened copies of notes **before** destructive actions per pipeline:
    - E.g. before `split_atomic`, `distill_note`, `append_to_hub`, `move_note`, `rename_note`, archive moves, or large expressive appends.
  - Append‑only; never edited.
- **Batch checkpoints (`BATCH_SNAPSHOT_DIR`)**:
  - Lives under `Backups/Batch/`.
  - Stores summary notes per batch/sweep (e.g. archive sweep, organize run, distill mini‑batch).
- **Version snapshots (content history)**:
  - Implemented by the `version-snapshot` skill:
    - Writes to `Versions/<original-slug>--<YYYYMMDD-HHMMSS>.md`.
    - Uses `obsidian_update_note(..., mode: "create")` so dest backup is skipped for brand‑new version files (source is already backed up).

#### 3.3 Confidence gates

(Aligned with `confidence-loops.mdc` and `Cursor-Skill-Pipelines-Reference.md`.)

- **≥85%**: safe to auto‑execute **destructive** steps (moves, renames, structural rewrites, archive decisions, large appends), *if* per‑change snapshot also succeeds.
- **72–84% (mid-band)**: triggers **at most one** non‑destructive refinement loop per note per run; after loop, if `post_loop_conf ≥ 85%` and snapshot succeeds, destructive steps may proceed. Some pipelines allow limited non‑destructive work (e.g. ingest: `frontmatter-enrich`, `append_to_hub`; subfolder-organize may allow move into **existing** folder at ≥78% where specified).
- **<72% (low)**: no loop; no destructive actions; propose‑only / log with `#review-needed`.

#### 3.4 Snapshot triggers (summary)

- **full-autonomous-ingest**:
  - Before `split_atomic`, before destructive `distill_note`, before `append_to_hub`, before `move_note`, before `rename_note`.
  - Batch checkpoint every ~5 notes.
- **autonomous-distill**:
  - Before first structural rewrite: distill layers / `layer-promote` / heavy `obsidian_update_note`.
  - Batch checkpoint every ~3 notes.
- **autonomous-archive**:
  - After `archive-check` recommends archive (≥85%), **before** `subfolder-organize`, `summary-preserve`, and `move_note`.
  - Batch checkpoint once per archive sweep.
- **autonomous-express**:
  - Alongside `version-snapshot`, before large appends: `related-content-pull`, `express-mini-outline`, `call-to-action-append` (when confidence ≥ thresholds).
  - Batch checkpoints optional for larger express runs.
- **autonomous-organize**:
  - Before `obsidian_rename_note` and before `obsidian_move_note` when confidence ≥85%.
  - Batch checkpoint roughly every 3 notes.

#### 3.5 Health check and observability

- Every N notes (e.g. 10) in a batch, or on first error in a run, call **`health_check`** and log result (status, metrics, serverIdentifier). Prefer a dedicated note **`3-Resources/MCP-Health-YYYY-MM.md`** (monthly rotation) instead of appending forever to Backup-Log.md; fallback to Backup-Log.md or **3-Resources/MCP-Observability.md** if preferred.
- When **`health_check`** returns non-OK status, automatically call **`obsidian_ensure_backup`** as a defensive measure before continuing the batch.

#### 3.6 Logging and log files

- **Log line convention** (from `Cursor Skill Pipelines Reference`):
  - `YYYY-MM-DD HH:MM | Excerpt: [snippet] | PARA: [type] | Changes: [list; include Backup: [path] when processing] | Confidence: X% | Proposed MV: [path or 'stay'] | Flag: [none or #review-needed + reason]`
- **`obsidian_log_action` usage**:
  - Called **after every note** processed by any pipeline (success, partial, or skip).
  - Backup/snapshot/version paths are included inside the `changes` string.
- **Dedicated log notes**:
  - `3-Resources/Ingest-Log.md`
  - `3-Resources/Distill-Log.md`
  - `3-Resources/Archive-Log.md`
  - `3-Resources/Express-Log.md`
  - `3-Resources/Organize-Log.md`
  - `3-Resources/Backup-Log.md`
- **Example current state (2026-02-26)**:
  - `Ingest-Log.md` shows:
    - Multiple **INGEST MODE** runs with `obsidian_create_backup` + classify + frontmatter‑enrich at ~70% confidence.
    - No automatic moves/splits because confidence <85% (safety respected).
    - Non‑markdown `Untitled Document 1/2` normalized via companion notes and logged as needing manual move.

---

### 4. Ingest folder behavior (`Ingest/**`)

Governed by `.cursor/rules/always/always-ingest-bootstrap.mdc` + `.cursor/rules/context/ingest-processing.mdc` + full‑autonomous‑ingest pipeline.

#### 4.1 When Ingest processing is triggered

- Any of the following:
  - User explicitly: **"INGEST MODE"**, **"Process Ingest"**, **"run ingests"**.
  - Any task/chat mentioning `Ingest/` or new/unprocessed files.
  - Opening Ingest notes in a context where automation is requested.

#### 4.2 Non-markdown handling

- **Listing**:
  - Use `obsidian_list_notes("Ingest")` for `.md` notes.
  - Separately list non‑`.md` entries via workspace glob (Cursor) because MCP only sees notes.
- **For each non‑markdown file** (PDF, image, audio, etc.):
  - **Do NOT** call `obsidian_move_note` on the binary.
  - Create a **companion `.md` note**:
    - Name pattern: `YYYY-MM-DD_OriginalName-Companion.md` (variants already seen in Resources).
    - Default PARA destination: `3-Resources/` (unless obviously a project/area — then 1/2/4 as appropriate).
  - In the companion:
    - Embed/link file as `![[5-Attachments/PDFs/original.pdf]]` or appropriate subtype (`Images/`, `Audio/`, `Documents/`, `Other/`).
    - Add a callout explaining manual move:
      - Manual action: move original binary from `Ingest/` to `5-Attachments/<subtype>/` in Obsidian’s file explorer.
      - After move: update embed path if needed and remove `#needs-manual-move`.
  - Tag companion with `#needs-manual-move` so a Dataview query can track pending manual moves.

#### 4.3 Embedded image normalization in Ingest `.md`

- Scan Ingest notes for image embeds:
  - `![[*.png]]`, `![[*.jpg]]`, `![[*.jpeg]]`, `![[*.gif]]`, `![[*.webp]]`, `![[*.svg]]`, `![[*.bmp]]`.
  - Includes common names like `"Pasted image ..."`, `"Screenshot ..."`.
- For each embed whose **file currently lives in `Ingest/` or vault root**:
  - Rewrite link to `![[5-Attachments/Images/original-filename.ext]]`.
  - Collect file names needing manual move.
- Insert standardized callout after frontmatter:
  - Explains that embeds were normalized to `5-Attachments/Images/`.
  - Lists each file to drag from `Ingest/` (or root) into `5-Attachments/Images/`.
  - Encourages better naming during move.
- Add `#needs-attachment-relocation` and `#attachment-relocation-pending` tags.
- **Important**: automation **never moves the image binaries**; user performs the drag‑and‑drop in Obsidian.

#### 4.4 Running full-autonomous-ingest on Ingest/*.md

- After steps above:
  - Run **full-autonomous-ingest** on all `Ingest/*.md` (including companions) via para‑zettel‑autopilot.
- **Bootstrap (before classify)**: After **`obsidian_list_notes("Ingest")`**, call **`obsidian_list_projects`** and **`bootstrap_project_batch`**(paths, existing_projects_json). If a project seed is detected (≥85%), either auto-apply or set requires_confirmation and ask user, then **`confirm_bootstrap`**. If multiple projects or low-confidence (<85%), default to requires_confirmation = true.
- **Pre-move chain (mid-band)**: **calibrate_confidence** → **verify_classification** → **obsidian_move_note**(..., `dry_run: true`) → if OK, **obsidian_move_note**(..., `dry_run: false`). On move failure or dry_run risks, use the canonical fallback in mcp-obsidian-integration.mdc.
- Effective pipeline (from the reference):
  - (optional bootstrap after list_notes + list_projects)
  - `obsidian_create_backup`
  - `obsidian_classify_para`
  - **`frontmatter-enrich` (skill)**:
    - Sets `status`, `confidence`, `para-type`, `created`, hub/related links, and optionally `project-id`, priority, deadline.
  - **`subfolder-organize` (skill)**:
    - Suggests or creates a subfolder path (≤4 levels) using PARA type + themes + `project-id`.
    - May move into **existing** folders at lower confidence (≥78%) or create new structure at ≥85%.
  - `split_atomic` (MCP op when appropriate).
  - **`split-link-preserve` (skill)**:
    - Ensures parent/child split linkage:
      - `split_from` on children.
      - `split_into` or "Splits" list on parent.
  - `distill_note` (first‑pass distill).
  - **`distill-highlight-color` (skill)**:
    - Applies highlight colors based on Highlightr master key + per‑project `highlight_key`.
  - **`next-action-extract` (skill)**:
    - Extracts tasks into checklists and populates `next-actions` frontmatter.
  - `manage_frontmatter` / `manage_tags` (housekeeping).
  - `append_to_hub` (MCP op to update hub notes).
  - **`obsidian_move_note`** (when confidence gates allow): always **dry_run first, then commit**; see §7 and MCP fallback table for move/dry_run fallback.
  - `obsidian_log_action` (log into `Ingest-Log` + `Backup-Log`).

---

### 5. Pipeline details

#### 5.1 full-autonomous-ingest (summary)

- **Purpose**: Transform raw captures in `Ingest/` into properly classified, atomic, lightly distilled, and placed PARA notes with hubs and tasks.
- **Main steps** (post non‑MD + image normalization):
  - (Optional **bootstrap_project_batch** after list_notes + list_projects, before classify) → backup → classify PARA → `frontmatter-enrich` → `subfolder-organize` → (mid-band: MCP `obsidian_subfolder_organize` candidates → **calibrate_confidence** → **verify_classification**) → optional split + `split-link-preserve` (or optional **`obsidian_refactor_to_zettel`** for literature/fleeting when note > ~800 words or multiple `##` headings) → first distill + `distill-highlight-color` → `next-action-extract` → (recommended when task-like: **task rerouting** via **`find_parent`** + **`obsidian_create_task_note`** / **`append_tasks`**) → hub updates → **move (dry_run first, then commit)** → log.
- **Skill usage**:
  - `frontmatter-enrich`, `subfolder-organize`, `split-link-preserve`, `distill-highlight-color`, `next-action-extract`. Optional: task rerouting (find_parent, create_task_note, append_tasks); optional **obsidian_refactor_to_zettel** for literature/fleeting when length/headings warrant.
- **Confidence behavior (current)**:
  - **≥85%**: full pipeline including splits, moves into new structures, hub appends; move always via dry_run then commit.
  - **72–84% (mid-band inclusive)**: single refinement loop with MCP path candidates + calibrate + verify; after loop, if `post_loop_conf ≥ 85%` then full pipeline (dry_run then commit); else metadata/hub and moves only to **existing** targets where allowed (e.g. ≥78% into existing per pipeline reference).
  - **<72%**: classify + frontmatter + proposals only; no move/split; log includes `#review-needed`.

#### 5.2 autonomous-distill

- **Purpose**: Periodic or on‑demand deepening of notes in active PARA folders.
- **Scope**: `1-Projects/**`, `2-Areas/**`, `3-Resources/**` (excluding `4-Archives/`, `Backups/**`, `Templates/**`, `*Log.md`, `* Hub.md`).
- **Pipeline**:
  - **Strongly recommended for batch mode (>5 notes)**: optional pre-step **`obsidian_garden_review`**(scope, focus: **distill_candidates**, output_path, auto_apply) to pre-select notes; then run distill on that set. Optional for single-note triggers.
  - Backup → optional `auto-layer-select` → distill layers → `distill-highlight-color` → `layer-promote` → `callout-tldr-wrap` → `readability-flag` → log.
- **Skill usage**:
  - `auto-layer-select` (optional).
  - `distill-highlight-color`.
  - `layer-promote`.
  - `callout-tldr-wrap`.
  - `readability-flag`.
- **Snapshots**:
  - Per‑change before first structural rewrite.
  - Batch snapshot every ~3 notes.

#### 5.3 autonomous-archive

- **Purpose**: Move completed/inactive material into `4-Archives/` while preserving summaries and resurfacing candidates.
- **Scope**: Markdown notes in `1-Projects/**`, `2-Areas/**`, `3-Resources/**` only.
- **Pipeline**:
  - Backup → `obsidian_classify_para` → `archive-check` → (if **mid-band 72–84%** post-check: **calibrate_confidence** → **verify_classification** → **obsidian_move_note**(..., `dry_run: true`) → then commit after snapshot) → `subfolder-organize` (archive path) → `resurface-candidate-mark` → `summary-preserve` → **obsidian_move_note (dry_run first, then commit)** → log. Reuse same fallback chain as §1.2 / mcp-obsidian-integration.mdc for move/dry_run failures.
- **Skill usage**:
  - `archive-check`: decides archive readiness (no open tasks, status complete, age threshold, cross‑checks).
  - `subfolder-organize`: builds archive path like `4-Archives/Project-Name-Archive/Subtheme/…`.
  - `resurface-candidate-mark`: marks high‑potential notes and optionally appends to a Resurface hub.
  - `summary-preserve`: ensures TL;DR / summary callout exists and preserves color links.
- **Snapshots**:
  - Per‑change after `archive-check` (confidence ≥85%) but before path computation/summary/move.
  - Batch snapshot once per archive sweep.

#### 5.4 autonomous-express

- **Purpose**: Turn already‑distilled notes into more expressive outputs (outlines, related‑content blocks, publishable summaries with CTAs).
- **Scope**: Same as distill (Projects/Areas/Resources), excluding Archives, Backups, Templates, Logs, Hubs, and `Versions/**`.
- **Pipeline**:
  - Backup → `version-snapshot` → **`related-content-pull`** or **`obsidian_suggest_connections`** (if `auto_insert: true`, wrap inserted Related section in collapsible callout `[!related]`) → `express-mini-outline` → (optional **`obsidian_append_to_moc`** / **`obsidian_generate_moc`** for hub-like notes) → `call-to-action-append` → log.
- **Skill usage**:
  - `version-snapshot`: creates dated snapshot in `Versions/`.
  - `related-content-pull` or **`obsidian_suggest_connections`**: appends a Related section via semantic + `project-id`; wrap in `[!related]` callout when using auto_insert.
  - `express-mini-outline`: writes a structured outline/summary block with project colors.
  - **`obsidian_append_to_moc`** / **`obsidian_generate_moc`**: optional for hub-like notes after outline.
  - `call-to-action-append`: appends CTA callout (e.g. Share/Publish?).
- **Snapshots**:
  - `version-snapshot` + per‑change snapshots before major appends.

#### 5.5 autonomous-organize

- **Purpose**: Re‑organize **existing** notes within active PARA (not ingest, not archive) by re‑classifying, enriching frontmatter, and moving/renaming them safely.
- **Scope**: `1-Projects/**`, `2-Areas/**`, `3-Resources/**`, excluding Archives, Backups, Templates, Logs, Hubs.
- **Pipeline**:
  - Backup → `obsidian_classify_para` → `frontmatter-enrich` → `subfolder-organize` or **MCP** **`obsidian_subfolder_organize`** (2–3 path candidates in mid-band) → (mid-band: **calibrate_confidence** → **verify_classification** → **obsidian_move_note**(..., `dry_run: true`) → commit) → optional `obsidian_rename_note` → **obsidian_move_note (dry_run first, then commit)** → log. Reuse same fallback chain as §1.2 / mcp-obsidian-integration.mdc for move/dry_run failures.
- **Skill usage**:
  - `frontmatter-enrich`.
  - `subfolder-organize` (re‑org mode: targets 1/2/3, not 4).
  - (Snapshots via `obsidian-snapshot` skill, not a dedicated organize skill.)
- **Snapshots**:
  - Per‑change before rename and before move (≥85%).
  - Batch snapshot about every 3 notes.

---

### 6. Skill catalog (current)

From `Cursor Skill Pipelines Reference` and skill list:

- **Classification & structure**
  - **`frontmatter-enrich`**: Sets/updates status, confidence, para-type, created, links, `project-id`, priority, deadline.
  - **`subfolder-organize`**: Computes target folder path (≤4 levels) from PARA type + `project-id` + semantic themes; separate modes for ingest, archive, and re‑org.
  - **`archive-check`**: Decides archive readiness (complete, no open tasks, age thresholds, folder checks).
  - **`split-link-preserve`**: Adds `split_from`/`split_into`-style metadata and Splits list for atomic splits.
- **Distillation & readability**
  - **`auto-layer-select`**: Suggests distillation depth (1/2/3 layers) from content complexity.
  - **`distill-highlight-color`**: Applies project‑aware highlight colors based on Highlightr keys.
  - **`layer-promote`**: Promotes bold → highlight → TL;DR; respects project colors.
  - **`callout-tldr-wrap`**: Wraps TL;DR in a `[!summary]` callout.
  - **`readability-flag`**: Marks notes as `needs-simplify` and inserts a readability warning callout.
- **Tasks & resurfacing**
  - **`next-action-extract`**: Extracts tasks / checklists, populates `next-actions` frontmatter.
  - **`resurface-candidate-mark`**: Flags high‑potential notes (links, highlights) and can append them to a Resurface hub.
- **Express / output**
  - **`related-content-pull`**: Finds and appends related notes based on semantics + `project-id`.
  - **`express-mini-outline`**: Generates a small outline/summary block with project color styling.
  - **`call-to-action-append`**: Appends a CTA callout (e.g. Share/Publish?).
  - **`version-snapshot`**: Writes dated snapshots into `Versions/` before major expressive appends.
- **Snapshots & safety**
  - **`obsidian-snapshot` (skill)**:
    - Creates per‑change and batch snapshots in `Backups/Per-Change/` and `Backups/Batch/`.
    - Required before a wide range of destructive actions across pipelines.

---

### 7. Operational notes and invariants

- **Dry-run before every move**:
  - For any **`obsidian_move_note`** at ≥85% confidence, the agent must first call **`obsidian_move_note`**(path, new_path, `dry_run: true`), review returned effects (path, new_path, backup status, risks e.g. dangling links), then call again with `dry_run: false` to commit. Move is always "`dry_run` first, then commit."
  - **Fallback**: If `dry_run` reports high-risk items (dangling links, overwrite conflicts, missing parents) or the actual move fails later: trigger **`propose_alternative_paths`** → feed top-1 or top-2 into **`calibrate_confidence`** (single retry) → **`verify_classification`** → `dry_run` again → commit; else append full `dry_run` output + error trace to log with `#review-needed` and pause that note. See MCP fallback table in `.cursor/rules/always/mcp-obsidian-integration.mdc`.
- **No shell file operations**:
  - Pipelines **never** use `mv/cp/rm` on vault files; all operations go through Obsidian MCP (`obsidian_move_note`, `obsidian_update_note`, `obsidian_ensure_structure`, etc.).
- **Folder creation semantics**:
  - `obsidian_move_note` does **not** create deep nested parents recursively; when moving to e.g. `4-Archives/Project-Archive/Subtheme/`, automation:
    - Calls `obsidian_ensure_structure(folder_path=<parent>)` first.
    - Retries `obsidian_move_note` only after parents exist.
- **Ingest as first stop**:
  - All new/unknown material is assumed to arrive under `Ingest/`.
  - For any task involving new files, the agent:
    - Checks `Ingest/` for outstanding items.
    - Normalizes non‑markdown + attachments.
    - Then runs (or at least proposes) full‑autonomous‑ingest per confidence rules.
- **Logs and review**:
  - Every pipeline writes human‑readable entries to its log note **and** to `Backup-Log.md` when snapshots/backups occur.
  - `#review-needed` flags any low‑confidence decision, backup/snapshot failure, or skipped destructive action.

---

### 8. How to extend or modify this setup

- **Add/adjust pipelines**:
  - Update `3-Resources/Cursor Skill Pipelines Reference` to keep canonical pipeline orders, confidence gates, and snapshot triggers.
  - Align or update context rules in `.cursor/rules/context/*.mdc` to match (triggers, globs, exclusions).
- **Add new skills**:
  - Place new skills under `.cursor/skills/<skill-name>/SKILL.md`.
  - Register them in the Pipelines Reference with:
    - Slot (where they run in the pipeline),
    - Behavior description,
    - Confidence gate.
- **Change safety thresholds**:
  - Adjust confidence tables in the Pipelines Reference first, then mirror special‑case details into context rules (distill/archive/express/organize/ingest-processing).
- **Documentation canon**:
  - This note is a human‑readable narrative overview.
  - **Companion**: [[2026-02-26-Automation-Flows-MCP-Improvements]] cross-references this report with the MCP server and proposes flow improvements using additional MCP tools (calibrate_confidence, verify_classification, dry_run, bootstrap, garden review, etc.).
  - **New flows** (Garden review, Curate cluster) are documented in §2 (triggers) and in the Pipelines Reference; they use **`obsidian_garden_review`** and **`obsidian_curate_cluster`** with optional auto_apply (suggest false during initial adoption).
  - **After each phase** of pipeline changes, re-run a small ingest batch (3–5 known notes) and verify in logs: `dry_run` usage, calibration/verification calls, backup existence, and `#review-needed` rate before/after.
  - The **source of truth** for behavior is:
    - `3-Resources/Cursor Skill Pipelines Reference.md` (pipelines + skills),
    - `.cursor/rules/always/*.mdc`, `.cursor/rules/context/*.mdc` (triggers, scopes, safety),
    - Individual `SKILL.md` files for low‑level behavior.

---

### 9. Changelog / updates tracked

| Date       | Change |
|-----------|--------|
| **2026-02-26** | Report created; initial snapshot of pipelines, skills, safety model, ingest behavior, and operational invariants. |
| **2026-02-26** | **Confidence bands** aligned with `confidence-loops.mdc` and Pipelines Reference: mid-band **72–84%** (single refinement loop); low **<72%** (propose-only, no destructive actions). Removed legacy 78–84% / 70–77% wording from §3.3 and §5.1. |
| **2026-02-26** | **MCP Pipelines Migration** (full plan): Phase 1 (ensure_backup, dry_run, health_check); Phase 2 (bootstrap, calibrate, verify, dry_run in ingest); Phase 3 (organize/archive verification chain + dry_run); Phase 4 (express suggest_connections + [!related] callout, MOC steps; distill garden_review pre-step); Phase 5 (Garden review and Curate cluster triggers/flows, task rerouting, refactor_to_zettel). Report §2, §3, §5, §7, §8 and Pipelines Reference updated. |
| **2026-02-26** | **MCP migration Phase 1**: ensure_backup vs create_backup (§3.1); health_check and MCP-Health-YYYY-MM.md (§3.5); dry-run before every move and canonical fallback (§7). See mcp-obsidian-integration.mdc and Pipelines Reference. |
| **2026-02-26** | **Loop logging** (all pipelines): document that logs and `obsidian_log_action` include `loop_attempted`, `loop_band`, `pre_loop_conf`, `post_loop_conf`, `loop_outcome`, `loop_type`, `loop_reason` per confidence-loops.mdc. |
| **2026-02-25** | **Version-snapshot create**: `obsidian_update_note(..., mode: "create")` for new version files under `Versions/` skips destination backup gate (source already backed up at pipeline start); path pattern `Versions/<slug>--<YYYYMMDD-HHMMSS>.md`. Documented in MCP rule and §3.2. |
| **2026-02-25** | **Deep-nested PARA moves**: Verified that `obsidian_move_note` does not create parent dirs recursively; flow is backup → (optional per-change snapshot) → `obsidian_ensure_structure`(folder_path: parent of new_path) → `obsidian_move_note`. Documented in MCP fallback table and §7. |

*When extending this report, append new rows above this table and keep the "Why resource?" section below.*

---

## Why resource?
Assigned based on content/frontmatter (confidence ~70%).

## Review Needed
Proposed para-type: resource. Assigned based on content/frontmatter (confidence ~70%). Do not move until reviewed.