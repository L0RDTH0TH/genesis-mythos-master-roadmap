---
description: "Binds natural-language triggers and PARA-scoped notes to the autonomous-express pipeline. Applies to distilled or high-signal project, area, and resource content."
globs:
  - "1-Projects/**/*.md"
  - "2-Areas/**/*.md"
  - "3-Resources/**/*.md"
  - "!4-Archives/**"
  - "!Backups/**"
  - "!Templates/**"
  - "!**/Log*.md"
  - "!**/* Hub.md"
  - "!**/Versions/**"
alwaysApply: false
---

# Auto-express (context rule)

- **Pipeline**: autonomous-express — generates expressive output from distilled notes (related content blocks, mini-outlines, call-to-action callouts).
- **Reference**: See `[3-Resources/Cursor-Skill-Pipelines-Reference.md](3-Resources/Cursor-Skill-Pipelines-Reference.md)` for the canonical pipeline order, confidence gates, and snapshot triggers.
- **MCP safety**: Always obey `[.cursor/rules/always/mcp-obsidian-integration.mdc](.cursor/rules/always/mcp-obsidian-integration.mdc)` for backups, snapshot directories, and MCP fallbacks.

## How to activate this pipeline

Use any of these natural-language triggers (case-insensitive, partial match usually works):

- **EXPRESS MODE – safe batch autopilot** *(canonical mode trigger)*
- **express this note**
- **generate outline**
- **create publishable summary**
- **turn this into an outline/post**

Express is typically run on **single notes or very small batches** where you want to push a distilled note toward shareable output.

## Pipeline overview

High-level sequence, as defined in the pipelines reference:

1. **Backup**: Ensure `obsidian_create_backup` has been called for the note (handled by the always-applied MCP rule).
2. **`version-snapshot` (skill)** — create a dated snapshot (e.g. under `…/Versions/`) to preserve original content and colors before any major append (always).
3. **`related-content-pull` (skill)** or **MCP** **`obsidian_suggest_connections`** — pull similar notes via semantic + `project-id` search and append a Related section (≥85%). If using **`obsidian_suggest_connections`** with `auto_insert: true`, wrap the inserted Related section in a collapsible callout `[!related]` to keep notes visually clean.
4. **`research-scope` (skill)** — when note is a PMG (*Master*Goal* or is_master_goal: true): aggregate Resources by project-id/phases; propose-first callout with source citation; commit ## Scoped Resources only on second pass when approved.
5. **`express-mini-outline` (skill)** — generate a mini-outline or summary as a fenced block, using project colors for sections (≥85%).
6. **Optional for hub-like notes**: **`obsidian_append_to_moc`** or **`obsidian_generate_moc`** after outline generation.
7. **`call-to-action-append` (skill)** — append a CTA callout (e.g. `> [!tip] Share/Publish?`) at the end of the note (always).
8. **Logging**: Call `obsidian_log_action` and append entries to both `3-Resources/Express-Log.md` and `3-Resources/Backup-Log.md` when snapshots, version files, or backups are involved.

- **Graph view**: Optionally set graph-related frontmatter (e.g. `graph: { color: "#hex" }`) from project color after express so graph view can use it. Prefer reading project color from Highlightr-Color-Key or Second-Brain-Config.

**Important**: Confidence thresholds, snapshot points, and skill order must remain synchronized with the master table in `Cursor-Skill-Pipelines-Reference.md`. If conflict arises, the reference table takes precedence and this rule should be updated, not vice versa.

## Batch and isolation

- Express runs are generally **single-note**; when batching, keep batches very small (e.g. 2–3 notes).
- Process **one note fully** (including `version-snapshot`, appends, and `obsidian_log_action`) before starting the next.
- **On failure**:
  - If backup, version snapshot, per-change snapshot, or a critical append step fails for a note, log the failure with `#review-needed` in `3-Resources/Express-Log.md` (and `3-Resources/Backup-Log.md` when snapshots are involved).
  - Skip further appends for that note and continue with the next.

## Error handling

On failure of backup, version-snapshot, per-change snapshot, related-content-pull, express-mini-outline, or call-to-action-append:

- Follow the **Error Handling Protocol** in `mcp-obsidian-integration.mdc` (§ Error Handling Protocol). Pipeline: `autonomous-express`; stage as appropriate. Include **error_type** in the summary and in the Errors.md entry table.
- Log to `3-Resources/Errors.md` (standard entry format: heading, metadata table, #### Trace, #### Summary) and reference in `Express-Log.md` and `Backup-Log.md`.
- If backup or version-snapshot fails: abort expressive appends for that note, continue to next.

## Snapshots and checkpoints

All per-change snapshot triggers **must** follow the `Snapshot triggers (all pipelines)` table in `Cursor-Skill-Pipelines-Reference.md`. **Do not invent new trigger points.**

- **Version snapshots**:
  - Always run `version-snapshot` before any major append in this pipeline.
  - Use **timestamped version paths**: `Versions/<original-slug>--<timestamp>.md` (e.g. `Versions/2026-02-25-express-narrative--20260225-120530.md`) so each run creates a new file and history is preserved.
  - Ensure the `Versions/` folder exists under the note’s parent (create once per project/area or via `obsidian_ensure_structure`; optional `.gitkeep` in `Versions/` for visibility and backup inclusion).
  - Create version files using `obsidian_read_note` + `obsidian_update_note(path, content, mode: overwrite)`. For **new-file creates** (target path does not exist), the MCP backup gate should treat the write as a create (skip destination backup); the original note is already backed up at pipeline start, and per-change snapshots remain the in-vault safety net. If the server blocks the write because the target does not exist, log the skip with `#review-needed` and continue the pipeline without the version file for that note.
  - If parent `Versions/` does not exist, follow the MCP fallback guidance (e.g. `obsidian_ensure_structure` for the parent path; otherwise log and require manual folder creation).
- **Per-change snapshots (in-vault)**:
  - Before large appends in this pipeline — `related-content-pull`, `express-mini-outline`, `call-to-action-append` — call the `obsidian-snapshot` skill with `type: "per-change"` for the target note, when confidence for the change is **≥85%** (for outline) or aligned with thresholds in the reference table.
  - If confidence is below threshold, or snapshot creation fails:
    - Do **not** perform the append.
    - Log the situation with `#review-needed` and proceed to the next note.
- **Batch checkpoints (optional)**:
  - Express is usually single-note; batch checkpoints are **optional**.
  - When processing more than **5 notes** in one express session, consider creating a `type: "batch"` snapshot summarizing:
    - Pipeline context.
    - Count and paths of notes with new expressive content.
    - Links/paths to their per-change snapshots and version files.
  - Batch checkpoint notes (when created) live under `Backups/Batch/` (`BATCH_SNAPSHOT_DIR`) and should be logged in both:
    - `3-Resources/Express-Log.md`
    - `3-Resources/Backup-Log.md`

## Logging requirements

After **every note** processed by this pipeline (whether fully expressed, partially updated, or skipped), call `obsidian_log_action` and append a canonical log line:

- **Log fields** (mirror Ingest log format):
  - **timestamp**
  - **pipeline**: `autonomous-express`
  - **note path**
  - **confidence** (for `express-mini-outline` / main expressive decision)
  - **actions taken / actions skipped**
  - **backup path** (from `obsidian_create_backup` for this run)
  - **version-snapshot path** (if created)
  - **snapshot path(s)** (per-change and batch, if created)
  - **flag**: `#review-needed` (when applicable) plus a short reason
- **Where to log**:
  - Append a human-readable line to `3-Resources/Express-Log.md`.
  - Include backup, version, and snapshot paths in the `changes` string of `obsidian_log_action`.
  - For any step that created snapshots or version files, also append/reflect the same information in `3-Resources/Backup-Log.md`.

## Confidence bands & express soft loop

- **Primary express signal**: `express_conf` — expressive readiness based on `express-mini-outline` and related content.
- **Bands and behavior** (aligned with `Cursor-Skill-Pipelines-Reference.md` and `confidence-loops.mdc`):
  - **High (express_conf ≥85)**:
    - After version + per-change snapshots, run related-content-pull, full outline, and CTA.
  - **Mid (68 ≤ express_conf ≤ 84)**:
    - Run a **soft express loop**:
      - Generate a short **preview outline** and self-critique coherence/fidelity **without writing** to the note.
      - Compute `post_loop_conf`.
    - If `post_loop_conf ≥ 90`: commit full outline + CTA.
    - If `85 ≤ post_loop_conf ≤ 89`: commit a **shorter outline** + CTA.
    - Else or if `post_loop_conf ≤ pre_loop_conf`: skip outline/related blocks; optionally append a small CTA (“needs further distill before publish”) and log.
  - **Low (express_conf <68)**:
    - No express beyond optional minimal CTA; rely on prior/future distill or organize runs. **Create a Decision Wrapper** under `Ingest/Decisions/Low-Confidence/` with `wrapper_type: low-confidence`, `pipeline: express`, `original_path`, `clunk_severity: high`; fill options A–G with outline/view proposals and "Try distill lens", "Seed-enhance", "Mark orphan / review-pending", "Ignore". Use the option labels and meanings from [User-Questions-and-Options-Reference](3-Resources/Second-Brain/User-Questions-and-Options-Reference.md) §2 (Decision Wrappers: A–G, 0, R, re-wrap). Ensure `obsidian_ensure_structure`(folder_path: "Ingest/Decisions/Low-Confidence"); ensure CHECK_WRAPPERS entry exists; append Watcher-Result line `message: "created wrapper → Decisions/Low-Confidence/<basename>"`.
- **Mid-band → Refinements wrapper**: When post_loop_conf < 85% or post_loop_conf ≤ pre_loop_conf after the soft express loop, also create a Decision Wrapper under `Ingest/Decisions/Refinements/` with `wrapper_type: mid-band-refinement`, `pipeline: express`, `original_path`, `clunk_severity: medium`; fill options A–G with outline/view choices and "Re-queue with user_guidance", "Skip", "Ignore". Use the option labels and meanings from [User-Questions-and-Options-Reference](3-Resources/Second-Brain/User-Questions-and-Options-Reference.md) §2 (Decision Wrappers: A–G, 0, R, re-wrap). Ensure `obsidian_ensure_structure`(folder_path: "Ingest/Decisions/Refinements"); ensure CHECK_WRAPPERS entry exists; append Watcher-Result line `message: "created wrapper → Decisions/Refinements/<basename>"`.
- **Loop logging**:
  - Populate `loop_attempted`, `loop_band`, `pre_loop_conf`, `post_loop_conf`, `loop_outcome`, `loop_type: "express-soft"`, and `loop_reason` in `Express-Log.md` and the `obsidian_log_action` changes string.

## Exclusions

This rule:

- **Includes** only markdown notes under:
  - `1-Projects/**`
  - `2-Areas/**`
  - `3-Resources/**`
- **Excludes**:
  - `4-Archives/**` — archive notes are not expressed by this pipeline.
  - `Backups/**` (Per-Change, Batch, Versions, or other backup subtrees).
  - `Templates/**`.
  - Any `**/Log*.md` such as:
    - `3-Resources/Ingest-Log.md`
    - `3-Resources/Distill-Log.md`
    - `3-Resources/Archive-Log.md`
    - `3-Resources/Express-Log.md`
    - `3-Resources/Backup-Log.md`
  - Any `**/* Hub.md` (e.g. `Resources Hub.md`, project/area hubs) by default.
  - Any `**/Versions/**` subfolder to avoid recursively expressing version snapshots themselves.

These exclusions keep express operations focused on live, canonical notes rather than backups, versions, logs, or hub/index notes.

## Safety

- **Backups and versions first**:
  - If `obsidian_create_backup` or `version-snapshot` fails for a note, **abort** expressive appends for that note; log the failure with `#review-needed` and perform no destructive actions.
- **Per-change snapshots**:
  - Mandatory before large appends when confidence meets the thresholds in the snapshot triggers table.
  - Snapshot files under `Backups/Per-Change/` and batch notes under `Backups/Batch/` are **append-only** and must never be edited.
- **Critical invariant**:
  - No destructive action (rewrite, move, append, delete) may occur unless **both**:
    1. Confidence for the underlying expressive change is **≥85%** (or the relevant threshold from the pipeline reference), **and**
    2. A successful per-change snapshot was created and hashed for that note in the current run.
  - If either condition fails → **skip the destructive action**, log `#review-needed`, and continue to the next note.
- **Fallbacks for version paths**:
  - Follow the MCP fallback table when creating new version files; use `obsidian_ensure_structure` for missing parent directories where supported, otherwise log and require manual folder creation.
- **No shell file ops**:
  - Never use shell `cp/mv/rm` on the vault; all writes go through MCP tools and skills.
- **Restore is explicit**:
  - Restoring from version snapshots or backups is always user-driven via dedicated rules; autonomous-express never auto-restores or removes these files.

## Rollout guidance

- **Initial rollout recommendation**:
  - Start by running this rule only on a single, well-understood test project (e.g. `1-Projects/Test-Project/**`) containing already distilled notes.
  - Run several manual express sessions and confirm:
    - Version snapshots are created in the expected `Versions/` subfolder.
    - Per-change snapshots exist for notes with new related content, outlines, or CTAs.
    - Logs in `3-Resources/Express-Log.md` and `3-Resources/Backup-Log.md` contain complete information with no unexpected `#review-needed` spikes.
  - After stable behavior is observed, gradually widen usage to more projects and areas under the existing frontmatter globs.

