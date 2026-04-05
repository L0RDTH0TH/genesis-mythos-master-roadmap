---
name: readability-flag
description: Sets needs-simplify frontmatter and inserts a warning callout when note readability is low. Use at the end of the autonomous-distill pipeline.
---

# readability-flag

## When to use

- At the **end** of the autonomous-distill pipeline.
- When confidence in the heuristic is **≥70%**; otherwise skip or only propose.

## Instructions

1. **Assess readability**: Read the note with `obsidian_read_note`. Use a simple heuristic: long sentences, dense paragraphs, few headings, complex jargon without context. Optionally flag related project ideas that have similar issues (e.g. same color/section type).

2. **If low readability**:
   - Set frontmatter: `obsidian_manage_frontmatter`(path, key: "needs-simplify", value: "true", action: set).
   - Insert a warning callout near the top (after first heading or in a consistent place): e.g. `> [!warning] Needs simplification — low readability.` via `obsidian_search_replace`. **Backup first** before edits.

3. **If readability is acceptable**: Do nothing; do not set `needs-simplify`.

## MCP tools

- `obsidian_read_note` — read note
- `obsidian_manage_frontmatter` — set needs-simplify (path, key, value, action: set)
- `obsidian_search_replace` — insert warning callout (destructive; backup first)

## Confidence gate

**≥70%**: Apply flag and callout. **<70%**: Skip or propose only.
