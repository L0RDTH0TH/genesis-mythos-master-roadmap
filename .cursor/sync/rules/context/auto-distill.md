---
description: "Binds natural-language triggers and PARA-scoped notes to the autonomous-distill pipeline. Applies to active project, area, and resource content."
globs:
  - "1-Projects/**/*.md"
  - "2-Areas/**/*.md"
  - "3-Resources/**/*.md"
  - "!4-Archives/**"
  - "!Backups/**"
  - "!Templates/**"
  - "!**/Log*.md"
  - "!**/* Hub.md"
alwaysApply: false
---

# Auto-distill (context rule)

- **Pipeline**: autonomous-distill — periodic or targeted refinement pass over active PARA notes (Projects, Areas, Resources).
- **Reference**: See `[3-Resources/Cursor-Skill-Pipelines-Reference.md](3-Resources/Cursor-Skill-Pipelines-Reference.md)` for the canonical pipeline order, confidence gates, and snapshot triggers.
- **MCP safety**: Always obey `[.cursor/rules/always/mcp-obsidian-integration.mdc](.cursor/rules/always/mcp-obsidian-integration.mdc)` for backups, snapshot directories, and MCP fallbacks.

## How to activate this pipeline

Use any of these natural-language triggers (case-insensitive, partial match usually works):

- **DISTILL MODE – safe batch autopilot** *(canonical mode trigger)*
- **distill this note** / **distill current file**
- **refine this note** / **refine [[Note Title]]**
- **autonomous distill on folder X**

When these phrases appear in the instruction (and the current note or selection matches the `globs` above), prefer this rule to drive the **autonomous-distill** pipeline.

## Pipeline overview

High-level sequence, as defined in the pipelines reference:

1. **Backup**: Ensure `obsidian_create_backup` has been called for the note (handled by the always-applied MCP rule).
2. **Optional pre-step (strongly recommended for batch mode, >5 notes)**: Use **`obsidian_garden_review`**(scope/folder, focus: **distill_candidates**, output_path, auto_apply) to pre-select notes that need distill; then run autonomous-distill on that set. Optional for single-note triggers. See Pipelines Reference.
3. **Optional — `auto-layer-select` (skill)**: When layer-selection is enabled, use content complexity to suggest 1 / 2 / 3 distillation layers; manual override remains (e.g. "distill this note with 2 layers"). See `.cursor/skills/auto-layer-select/SKILL.md`.
4. **Distill layers**: Run standard distill layers appropriate to the note.
5. **`distill-highlight-color` (skill)** — apply project-aware highlight colors based on Highlightr keys (≥85% confidence).
6. **`layer-promote` (skill)** — promote bold → highlight → TL;DR with project color overrides and contrast for conflicting ideas (≥85%).
7. **`callout-tldr-wrap` (skill)** — wrap TL;DR in a `> [!summary] TL;DR` callout (always).
8. **`readability-flag` (skill)** — set `needs-simplify` and insert a warning callout when readability is low (≥85%; non-destructive metadata-only may use lower threshold per pipeline reference).
9. **Logging**: Call `obsidian_log_action` and append entries to both `3-Resources/Distill-Log.md` and `3-Resources/Backup-Log.md` when snapshots or backups are involved.

**Important**: Confidence thresholds, snapshot points, and skill order must remain synchronized with the master table in `Cursor-Skill-Pipelines-Reference.md`. If conflict arises, the reference table takes precedence and this rule should be updated, not vice versa.

## Batch and isolation

- Process **one note fully** (including `obsidian_log_action`) before starting the next.
- **Batch size**: Use small, intentional batches (e.g. up to ~5 notes) when running `DISTILL MODE – safe batch autopilot`.
- **On failure**:
  - If backup, snapshot, or a critical skill fails for a note, log the failure with `#review-needed` in `3-Resources/Distill-Log.md` (and `3-Resources/Backup-Log.md` when snapshots are involved).
  - Skip remaining destructive steps for that note and continue with the next note in the batch.

## Error handling

On failure of backup, snapshot, auto-layer-select, distill layers, distill-highlight-color, layer-promote, callout-tldr-wrap, or readability-flag:

- Follow the **Error Handling Protocol** in `mcp-obsidian-integration.mdc` (§ Error Handling Protocol). Pipeline: `autonomous-distill`; stage: e.g. `distill-highlight-color`, `layer-promote`. Include **error_type** in the summary and in the Errors.md entry table.
- Append to `3-Resources/Errors.md` (standard entry format: heading, metadata table, #### Trace, #### Summary) and a one-line reference in `Distill-Log.md` (and `Backup-Log.md` when snapshots involved).
- If severity high: skip remaining destructive steps for that note, continue to next.

## Snapshots and checkpoints

All per-change snapshot triggers **must** follow the `Snapshot triggers (all pipelines)` table in `Cursor-Skill-Pipelines-Reference.md`. **Do not invent new trigger points.**

- **Per-change snapshots (in-vault)**:
  - Before the **first structural rewrite** in this pipeline (distill layers / `layer-promote` / heavy `obsidian_update_note`), when confidence for the underlying change is **≥85%**, call the `obsidian-snapshot` skill with `type: "per-change"` for the target note.
  - If confidence is below threshold:
    - Do **not** snapshot.
    - Do **not** perform the destructive action; instead log and flag `#review-needed`.
- **Batch checkpoints**:
  - Maintain a counter of notes processed in the current distill session.
  - After every **3 notes**, call `obsidian-snapshot` with `type: "batch"` and include:
    - Pipeline context (e.g. `"DISTILL MODE – safe batch autopilot"`).
    - The list of notes processed in that mini-batch.
    - Links/paths to their per-change snapshots (when available).
  - Batch checkpoint notes live under `Backups/Batch/` (`BATCH_SNAPSHOT_DIR`) and must also be logged in both:
    - `3-Resources/Distill-Log.md`
    - `3-Resources/Backup-Log.md`

## Logging requirements

After **every note** (whether processed successfully, skipped, or failed), call `obsidian_log_action` and append a canonical log line:

- **Log fields** (mirror Ingest log format):
  - **timestamp**
  - **pipeline**: `autonomous-distill`
  - **note path**
  - **confidence** (for the main structural decision)
  - **actions taken / actions skipped**
  - **backup path** (if `obsidian_create_backup` was called for this run)
  - **snapshot path(s)** (per-change and batch, if created)
  - **flag**: `#review-needed` (when applicable) plus a short reason
- **Where to log**:
  - Append a human-readable line to `3-Resources/Distill-Log.md`.
  - Include backup and snapshot paths in the `changes` string of `obsidian_log_action`.
  - For any step that created snapshots or relied on existing backups, also append/reflect the same information in `3-Resources/Backup-Log.md` so cross-pipeline history stays consistent.
  - When the note has `tags` including `agent-research` (Agent-Research notes created by `research-agent-run`), set a lightweight frontmatter marker such as `research_distilled: true` after a successful autonomous-distill pass so future RESEARCH-AGENT runs and BATCH-DISTILL can treat it as already distilled.

## Confidence bands & distill depth loop

- **Primary distill signal**: `distill_conf` — depth signal from `auto-layer-select` or equivalent evaluation.
- **Bands and behavior** (aligned with `Cursor-Skill-Pipelines-Reference.md` and `confidence-loops.mdc`):
  - **High (distill_conf ≥85)**:
    - After snapshot, run full planned structural distill (layers, highlight, promote, wrap, readability).
  - **Mid (68 ≤ distill_conf ≤ 84)**:
    - Run a **depth self-critique loop**:
      - Evaluate risk of nuance loss; consider a shallower plan (e.g. fewer layers).
      - Compute `post_loop_conf` for the shallower plan.
    - If `post_loop_conf ≥ 85`: snapshot → run the **shallower** structural distill plan.
    - Else or if `post_loop_conf ≤ pre_loop_conf`: skip structural distill; run only `readability-flag` (and safe metadata tweaks) and log. **Also create a Decision Wrapper** under `Ingest/Decisions/Refinements/` with `wrapper_type: mid-band-refinement`, `pipeline: distill`, `original_path`, `clunk_severity: medium`; fill options A–G with depth/layer choices and "Re-queue with user_guidance", "Skip", "Ignore". Use the option labels and meanings from [User-Questions-and-Options-Reference](3-Resources/Second-Brain/User-Questions-and-Options-Reference.md) §2 (Decision Wrappers: A–G, 0, R, re-wrap). Ensure `obsidian_ensure_structure`(folder_path: "Ingest/Decisions/Refinements"); ensure CHECK_WRAPPERS entry exists; append Watcher-Result line `message: "created wrapper → Decisions/Refinements/<basename>"`.
  - **Low (distill_conf <68)**:
    - No structural distill; only `readability-flag` and frontmatter flags. **Create a Decision Wrapper** under `Ingest/Decisions/Low-Confidence/` with `wrapper_type: low-confidence`, `pipeline: distill`, `original_path`, `clunk_severity: high`; fill options A–G with depth/layer proposals and "Try distill lens", "Seed-enhance", "Mark orphan / review-pending", "Ignore". Use the option labels and meanings from [User-Questions-and-Options-Reference](3-Resources/Second-Brain/User-Questions-and-Options-Reference.md) §2 (Decision Wrappers: A–G, 0, R, re-wrap). Ensure `obsidian_ensure_structure`(folder_path: "Ingest/Decisions/Low-Confidence"); ensure CHECK_WRAPPERS entry exists; append Watcher-Result line `message: "created wrapper → Decisions/Low-Confidence/<basename>"`.
- **Loop logging**:
  - Populate `loop_attempted`, `loop_band`, `pre_loop_conf`, `post_loop_conf`, `loop_outcome`, `loop_type: "distill-depth"`, and `loop_reason` in `Distill-Log.md` and the `obsidian_log_action` changes string.

## Exclusions

This rule:

- **Includes** only markdown notes under:
  - `1-Projects/**`
  - `2-Areas/**`
  - `3-Resources/**`
- **Excludes**:
  - `4-Archives/**` — archive notes are not refined by this pipeline.
  - `Backups/**` (Per-Change, Batch, Versions, or any other backup subtree).
  - `Templates/**`.
  - Any `**/Log*.md` such as:
    - `3-Resources/Ingest-Log.md`
    - `3-Resources/Distill-Log.md`
    - `3-Resources/Archive-Log.md`
    - `3-Resources/Express-Log.md`
    - `3-Resources/Backup-Log.md`
  - Any `**/* Hub.md` (e.g. `Resources Hub.md`, project/area hubs) by default.

These exclusions prevent recursive processing of history, configuration, and hub/index notes. Hubs or logs may be handled by dedicated rules if needed, but not by autonomous-distill.

## Safety

- **Backups first**: Rely on the always-applied MCP rule to ensure `obsidian_create_backup` is called before any destructive distill run.
- **Per-change snapshots**:
  - Mandatory before structural rewrites when confidence ≥85%, as per the snapshot triggers table.
  - Snapshot files under `Backups/Per-Change/` and batch notes under `Backups/Batch/` are **append-only** and must never be edited.
- **Critical invariant**:
  - No destructive action (rewrite, move, append, delete) may occur unless **both**:
    1. Confidence for the underlying action is **≥85%**, **and**
    2. A successful per-change snapshot was created and hashed for that note in the current run.
  - If either condition fails → **skip the destructive action**, log `#review-needed`, and continue to the next note.
- **No shell file ops**:
  - Never use shell `cp/mv/rm` on the vault. All operations must go through Obsidian MCP tools and skills.
- **Restore is explicit**:
  - Snapshot and backup **restore** is always user-triggered via dedicated restore/sweep rules; autonomous-distill never auto-restores or auto-deletes snapshots.

## Rollout guidance

- **Initial rollout recommendation**:
  - Start with `globs` effectively restricted to a single test project folder, e.g. `1-Projects/Test-Project/**`, by running this rule only on that folder and inspecting results and logs.
  - Run 3–5 manual batch tests (2–5 notes each) and confirm:
    - Snapshots and batch checkpoints are created as expected.
    - No new, unexpected `#review-needed` flags appear.
  - Only after stable behavior is observed should you widen usage to all `1-Projects/**`, `2-Areas/**`, and `3-Resources/**` under the existing frontmatter globs.

