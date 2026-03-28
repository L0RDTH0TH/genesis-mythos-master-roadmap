---
name: subfolder-organize
description: Builds target path from para-type, project-id, and semantic themes (max 4 levels) and moves the note via MCP. Use when organizing after frontmatter-enrich in ingest or before move in autonomous-archive pipeline.
---

# Project Linking Priority (enforced 2026-02-26 fix)

- If classify_para returned a non-null **project_name** → ALWAYS place under `1-Projects/{sanitized-project_name}/{subfolder_hint or ''}/{kebab-slug-YYYY-MM-DD-HHMM.md}` (see Naming-Conventions; date and time at end)
- For **Audits**: force subfolder_hint `Audits` even if classify didn't return it
- For **Tasks**: force subfolder_hint `Tasks`
- Only create brand-new `1-Projects/` folder when classify_para explicitly sets **para_type: 'Project'** AND **project_name is null**
- Use `obsidian_ensure_structure` with the full **folder_path** built from above
- Never create a project whose name contains 'Audit', 'Review', 'Tasks', 'Actions' as the top-level project name

---

# subfolder-organize

## When to use

- After **frontmatter-enrich** in full-autonomous-ingest (build path from `para-type` + themes / `project-id`).
- Before **move** in autonomous-archive (build archive path e.g. `4-Archives/Project-X-Archive/Subtheme/`).
- In **autonomous-organize** (re-org mode): after frontmatter-enrich; build target path under **active PARA roots only** (`1-Projects/`, `2-Areas/`, `3-Resources/`), not `4-Archives/`. Same max 4 levels; use para-type + project-id + semantic themes. Requires backup and per-change snapshot before move.

**≥85%**: Execute move (including creating new project folder if para_type is Project). **≥78%**: Execute move **only if** target is under an existing project/area folder (no new top-level project); otherwise propose path only. **<78%**: Propose path only, do not call move_note.

## Instructions

1. **Read frontmatter**: Use `obsidian_read_note` to get `para-type`, `project-id` (if any), and content themes.

2. **Build path** (max 4 levels): Use **classify_para** result first: when `project_name` is non-null, use it as the project segment and `subfolder_hint` (Audits, Tasks, etc.) as the subfolder; only then fall back to thematic names. **Filename segment**: Follow [[3-Resources/Second-Brain/Naming-Conventions|Naming-Conventions]] — format `kebab-slug-YYYY-MM-DD-HHMM.md` (date and time at end). When **name-enhance** (ingest) provides optional `suggested_filename` and confidence ≥85% and not protected, use it for the path segment; else derive from current filename or content.
   - **Ingest**: `{para-root}/{ProjectOrAreaName?}/{subfolder_hint?}/{IdeaClusterOrSubtheme?}/{kebab-slug-YYYY-MM-DD-HHMM}.md`
     - Examples: `1-Projects/Project-X/Idea-Cluster/meeting-notes-2026-02-25-1430.md`, `3-Resources/reference-basb-2026-02-25-0915.md`.
   - **Archive**: `4-Archives/{Project-X-Archive?}/{Subtheme?}/{kebab-slug-YYYY-MM-DD-HHMM}.md`
   - **Re-org (autonomous-organize)**: Same pattern as Ingest but for notes already in vault; target stays under `1-Projects`, `2-Areas`, or `3-Resources` (never `4-Archives`).
   - Para roots: `1-Projects`, `2-Areas`, `3-Resources`, `4-Archives`. Do not exceed 4 path segments (including filename).

3. **Ensure structure**: For deep paths (3–4 levels), call `obsidian_ensure_structure` with **folder_path** set to the target parent (e.g. `4-Archives/Project-Archive/Subtheme`) before `obsidian_move_note`; the server creates that path recursively. Without this, move may fail if intermediate folders are missing.

4. **Move**: Call `obsidian_move_note(path, new_path)`. **Requires backup first** (obsidian_create_backup or ensure_backup).

## MCP tools

- `obsidian_read_note` — read current path and frontmatter
- `obsidian_ensure_structure` — ensure PARA folders exist (if needed)
- `obsidian_move_note` — move note to new_path (destructive; backup first)

## Confidence gate

**≥85%**: Execute move. **<85%**: Propose `new_path` only; do not call move_note.
