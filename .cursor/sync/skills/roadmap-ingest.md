name: roadmap-ingest
description: Reads roadmap file from queue path; parses structure; standardizes to phases/subphases/tasks (no heavy distillation unless #needs-process); ensures project PARA root folder; creates/updates roadmap MOC note at 1-Projects/<Project>/ (no Roadmap/ subfolder for the primary roadmap); links to project MOC. Use when EAT-QUEUE processes mode TASK-ROADMAP.
---

# roadmap-ingest

## When to use

- When **auto-queue-processor** dispatches a queue entry with **mode: TASK-ROADMAP** (user triggered TASK-ROADMAP toolbar, then EAT-QUEUE).
- Read `filePath` from the queue entry; parse and standardize the roadmap; place in `1-Projects/<Project>/` (project PARA root; no `Roadmap/` subfolder for the primary roadmap MOC); link to project MOC if applicable.

## Instructions

1. **Read roadmap**: Use `obsidian_read_note`(filePath) to get full content. If the note is in Ingest or elsewhere, use that path.

2. **Parse structure**: Identify phases (`## Phase` or `##` headings), subphases (`###`), and tasks (`- [ ]` or `- [x]`). If format is non-standard (e.g. flat list), convert to standard: phases → subphases → tasks. **No heavy auto-splitting or distillation** unless the note has `#needs-process`; otherwise light normalization only.

3. **Target path**: Determine project from content or frontmatter (e.g. `project-id`) or from queue payload. Target **project PARA root** folder: `1-Projects/<Project>/`. Use `obsidian_ensure_structure` with **folder_path** set to that project folder (if needed) so it exists. **Do not** create or use a `Roadmap/` subfolder for the primary roadmap MOC; reserve subfolders (e.g. `Roadmap/`, `Phases/`, `Tasks/`) for related execution notes like feature specs, sub-phase roadmaps, task lists, etc.

4. **Write**: Create or update the roadmap MOC note at `1-Projects/<Project>/<slug>.md` (at the project PARA root, not in a subfolder) with standardized structure (heading hierarchy, `- [ ]` tasks, optional block-IDs and `depends on` per [Roadmap-Standard-Format](3-Resources/Roadmap-Standard-Format.md)). Use `obsidian_update_note` (create or overwrite as appropriate). **Backup and per-change snapshot before write** per mcp-obsidian-integration.

5. **Link MOC**: If project has a MOC (e.g. `[[ProjectName MOC]]`), ensure the new roadmap is linked from that MOC or add a link in the roadmap frontmatter `links` array.

6. **Log**: Append result to Watcher-Result.md and update Mobile-Pending-Actions.md with status (Success or failure reason).

## MCP tools

- `obsidian_read_note` — read roadmap at filePath
- `obsidian_ensure_structure` — ensure 1-Projects/<Project>/ (project PARA root) exists
- `obsidian_update_note` — write standardized roadmap (backup + snapshot first)
- `obsidian_create_backup` / obsidian-snapshot skill — before any destructive write

## Confidence gate

**≥85%**: Create/move and write. **<85%**: Propose path and structure only; do not write. Log and update Mobile-Pending-Actions with "propose-only" or failure.
