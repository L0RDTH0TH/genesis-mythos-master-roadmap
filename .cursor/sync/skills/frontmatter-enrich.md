---
name: frontmatter-enrich
description: Sets status, confidence, para-type, created, links (hub + related), and optional project-id, priority, deadline on a note after PARA classification. Use when running full-autonomous-ingest pipeline after obsidian_classify_para.
---

# frontmatter-enrich

## When to use

- Immediately after **obsidian_classify_para** in the full-autonomous-ingest pipeline.
- After **obsidian_classify_para** in the **autonomous-organize** pipeline (re-evaluate and update frontmatter for existing notes in active PARA).
- When confidence is **≥85%**: apply all enrichments. When confidence is **≥75%** and classify_para returned **project_name**: still apply project-id, MOC link, and lift stored confidence to ≥82% so downstream steps can proceed (see Project fallback logic below). Below 75%: propose only or set only safe fields.

## Instructions

1. **Use classification result**: From classify_para you have `para-type` (and optionally confidence). Read the note with `obsidian_read_note` to get current frontmatter and content.

2. **Set required and optional fields** via multiple `obsidian_manage_frontmatter` calls (path, key, value, action: set):
   - **Required**: `status`, `confidence` (e.g. "85%"), `para-type`, `created` (YYYY-MM-DD), `links` (hub + related projects/notes; **array format** — see step 3).
   - **Optional** (if detected by CoT): `project-id`, `priority`, `deadline`, `resurface-date`.
   - **Project MOC**: When `project-id` is set, ensure `links` includes a link to that project's MOC. Convention: `[[ProjectName MOC]]` (e.g. project-id "Test-Project" → add `[[Test-Project MOC]]`). If **classify_para.project_name** exists → set project-id and append `[[{{project_name}} MOC]]` to links array. Project MOC notes may be created manually once per project or by the pipeline as a minimal note under the project folder; see `[Second-Brain-Config](3-Resources/Second-Brain-Config.md)` and pipeline reference.
   - **Audit notes**: If note title contains "Audit" and project-id is set → add `highlight_key: "project-audit"` (for special yellow/orange relational color).

## Project fallback logic (2026-02-26 safety lift)

- If **classify_para** returned **project_name** (not null) AND confidence **≥75**:
  - Set frontmatter `project-id` to the slugified project name (e.g. from `classify_para.project_name`).
  - Append to `links` array: `[[{{classify_para.project_name}} MOC]]`.
  - Set stored confidence to **max(current confidence, 82)** so later pipeline steps (subfolder-organize, move) see a higher value — e.g. write `confidence: "82%"` or the higher of classify confidence and 82.
- If no **project_name** but title/content strongly implies an existing project (e.g. "Second Brain", "audit", "Cursor MCP"), set project-id to the closest match from `obsidian_list_notes("1-Projects")` and note reasoning in the log.

3. **Value format**: Output `links` as a **YAML array** (e.g. `["[[Resources Hub]]", "[[Project X]]"]`). If the MCP only accepts a string value, use a JSON array string and document that Dataview parses it. Always output array format; never comma-separated only. For Dataview queries, use `contains(links, "[[HubName]]")` or array membership; see `[Cursor-Skill-Pipelines-Reference](3-Resources/Cursor-Skill-Pipelines-Reference.md)` or `[Second-Brain-Config](3-Resources/Second-Brain-Config.md)`.

4. **Do not overwrite** user-critical fields unless the pipeline explicitly allows it; prefer adding or updating only the keys listed above.

## MCP tools

- `obsidian_read_note` — read note and frontmatter
- `obsidian_manage_frontmatter` — set key/value (path, key, value, action: set)

## Confidence gate

**≥85%**: Apply all enrichments. **≥75%** with project_name: apply project-id, MOC link, and set confidence to max(classified, 82%) so move/organize can run. **<75%**: Propose only or set only safe fields.

