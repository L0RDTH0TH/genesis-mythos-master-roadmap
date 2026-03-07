---
name: version-snapshot
description: Creates a dated snapshot of the note in a Versions subfolder before major appends, preserving original content and colors. Use before any major append in the autonomous-express pipeline.
---

# version-snapshot

## When to use

- **Before** any major append in the autonomous-express pipeline (e.g. before related-content-pull, express-mini-outline, or call-to-action-append that will change the note).
- **Always** run when the pipeline performs express output (no confidence gate).

> **Note**: `version-snapshot` is focused on **narrative versions** in the express pipeline (e.g. different drafts or output states for a single note). It complements, but does not replace, the system-level `obsidian-snapshot` safety net used across all pipelines for per-change protection.

## Create the version file reliably (mode: "create")

Version files are **new-file creates** (target path does not exist yet). The MCP server supports **`mode: "create"`** in `obsidian_update_note` (2026-02-25): it **skips the destination backup gate** (no backup required for the new path) and **fails if the path already exists**, so we use a **timestamped filename** to guarantee a new path every time. The **original note** is already backed up by `obsidian_create_backup` at pipeline start; a **per-change snapshot** of the original (via `obsidian-snapshot` skill) remains the safety net before appends. This skill only adds a narrative copy under `Versions/`.

- **Standardized filename**: `Versions/<original_slug>--<YYYYMMDD-HHMMSS>.md` using the **current** timestamp (e.g. `2026-02-25-express-narrative--20260225-120530.md`). Slug = note filename without extension; keep depth ≤4 levels.
- **Ensure `Versions/` exists**: Create the folder once per project/area; optional `.gitkeep` in `Versions/` so the folder appears in Obsidian and is included by backup tools.
- **Why mode "create" works**: No destination backup is needed for a file that does not exist; the server treats the write as a create and returns e.g. "✅ Note created (new path, no destination backup required)." Using a unique timestamp in the path ensures the call always targets a non-existent file, so the create succeeds.

## Instructions

1. **Read the note**: Use `obsidian_read_note` (path) to get full content (including highlights and structure).

2. **Ensure Versions folder**: Ensure `Versions/` exists under the note’s parent (e.g. `1-Projects/Project-X/Versions/`). Use `obsidian_ensure_structure` for the parent path if supported; otherwise the pipeline assumes the folder was created once.

3. **Build version path**: From the note path and **current** time:
   - **slug**: safe filename without extension (e.g. `2026-02-25-express-narrative`).
   - **timestamp**: `YYYYMMDD-HHMMSS` (e.g. `20260225-120530`).
   - **version_path**: `<note_parent>/Versions/<original_slug>--<YYYYMMDD-HHMMSS>.md` (vault-relative).

4. **Confidence gate**: Only write the version file if confidence for this step is **≥85%**. If <85%, skip the version write, log the skip in `Express-Log.md`, and continue the pipeline (related-content-pull, outline, CTA still run).

5. **Create version file**: Use `obsidian_update_note(path: version_path, content: full_note_content, mode: "create")`. Preserve the exact note body and frontmatter. The server skips destination backup for `mode: "create"` and fails if the path already exists (timestamped names avoid that). On success, expect response like "✅ Note created (new path, no destination backup required)."

6. **Log**: On success, include the version path in `obsidian_log_action` and in `Backup-Log.md`. On skip (confidence <85% or create failed), log with the reason; if create failed because path existed, use a fresh timestamp and retry once or log `#review-needed`.

## MCP tools

- `obsidian_read_note` — read full note
- `obsidian_update_note` — write to version path with **`mode: "create"`** (path: `Versions/<original_slug>--<YYYYMMDD-HHMMSS>.md`, content, mode: create). Skips dest backup; fails if path exists.
- `obsidian_ensure_structure` — ensure parent path exists when the server does not create parent dirs automatically

## Confidence gate

**≥85%** for the version write. If below threshold, skip the version file creation and continue the rest of the express pipeline. System-level destructive actions (appends to the **source** note) still use the ≥85% rule and `obsidian-snapshot` per the pipeline reference.

