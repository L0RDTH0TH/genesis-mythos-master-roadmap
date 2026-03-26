---
name: next-action-extract
description: Extracts tasks from note content into checklists and next-actions frontmatter for Dataview. Use when running full-autonomous-ingest pipeline after distill-highlight-color.
---

# next-action-extract

## When to use

- After **distill-highlight-color** in the full-autonomous-ingest pipeline.
- Only when confidence is **≥85%**; otherwise propose extractions only.

## Instructions

1. **Parse content**: Read the note with `obsidian_read_note`. Identify task-like phrases (TODOs, "should", deadlines, checklists, action items).

2. **Checklist in body**: Convert task lines to Obsidian/Tasks format (e.g. `- [ ] task text`). Apply via `obsidian_search_replace` for each conversion or a single `obsidian_update_note` if doing many edits. **Backup first** before destructive edits.

3. **next-actions in frontmatter**: `obsidian_manage_frontmatter` accepts `value` as a **string**. Store the list in one of these formats:
   - **JSON array string**: `value: "[\"Action one\", \"Action two\"]"` so Dataview can parse (e.g. `flat(next-actions)` if the theme supports it).
   - **Comma-separated**: `value: "Action one, Action two"` for simple display.
   - Document the chosen format in the vault (e.g. "next-actions is a JSON array string in frontmatter for Dataview queries").

4. **Project color (required when project-id set)**: When `project-id` (or project frontmatter) exists, use project-specific highlight color for action blocks from the note's `highlight_key` or [Highlightr-Color-Key.md](3-Resources/Highlightr-Color-Key.md) project guidelines. Use inline CSS only. This step is required when project-id is set, not optional.

## MCP tools

- `obsidian_read_note` — read content
- `obsidian_search_replace` — convert task lines to `- [ ]` (destructive; backup first)
- `obsidian_manage_frontmatter` — set `next-actions` key with string value (path, key, value, action: set)

## Confidence gate

**≥85%**: Execute checklist and frontmatter updates. **<85%**: Propose list only.

## next-actions frontmatter format

Use a **string** value. Recommended: JSON array string for Dataview, e.g. `next-actions: "[\"Review draft\", \"Send to client\"]"`. Alternative: comma-separated `"Review draft, Send to client"`. Keep consistent across the vault.
