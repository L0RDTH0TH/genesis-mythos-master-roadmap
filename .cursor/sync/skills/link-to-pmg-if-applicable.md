---
name: link-to-pmg-if-applicable
description: When a note has project-id, appends a link to that project's Project Master Goal (PMG) note to the note's links array if a PMG exists. Use after append_to_hub in full-autonomous-ingest. Only appends to the current note; never inserts into the PMG.
---

# link-to-pmg-if-applicable

## When to use

- After **append_to_hub** in the full-autonomous-ingest pipeline (or in apply-mode ingest after the note has been moved and has project-id set).
- When the note has **project-id** frontmatter and you want bidirectional traceability so research notes link back to the project's goal.

## Instructions

1. **Read the note**: Use `obsidian_read_note(path)` to get frontmatter. If **project-id** is missing or empty, skip (no-op).

2. **Resolve project folder**: From `project-id`, build the project root path `1-Projects/<project-id>/`. Sanitize project-id for path (e.g. kebab-case, no invalid chars).

3. **Find PMG**: Use `obsidian_list_notes` on that project folder (or `obsidian_global_search` with path filter) to find a note whose filename contains `Master-Goal` or `MasterGoal` (e.g. `Project-Master-Goal.md`, `<project-slug>-Master-Goal.md`). If multiple candidates, prefer the one with highest `created` timestamp or frontmatter `roadmap-seed: true`. If none found, skip (no-op).

4. **Append to links**: If a PMG note was found, append its wikilink (e.g. `[[Project-Master-Goal]]` or full path as needed for uniqueness) to the **current note's** `links` frontmatter array via `obsidian_manage_frontmatter` (path, key: `links`, value: add the new link to existing array, action: set or merge per MCP contract). Alternatively add a short `## Related to Goal` callout with the link in the body via `obsidian_update_note` (mode: append); prefer links array when the MCP supports array merge to avoid duplicating links.

5. **Safety**: Only modify the **current (research) note**. Never insert into or edit the PMG note itself unless confidence ≥90% and `user_guidance` explicitly allows it; this skill does not do that.

6. **Log**: Optionally log to Ingest-Log that PMG link was added (note path, project-id, PMG path) for traceability.

## MCP tools

- `obsidian_read_note` — read current note frontmatter
- `obsidian_list_notes` — list project folder to find PMG
- `obsidian_manage_frontmatter` — append to links array (or `obsidian_update_note` for callout)

## Confidence gate

**≥78%** (or when ingest_conf allows safe cross-note/metadata writes): Apply link. **<78%**: Skip; no-op. No destructive action on PMG; only append to the research note.
