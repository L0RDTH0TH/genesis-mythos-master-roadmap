---
name: related-content-pull
description: Pulls similar notes via semantic and project-id search and appends a Related section with color-theory emphasis. Use when running autonomous-express pipeline before express-mini-outline.
---

# related-content-pull

## When to use

- **Before** express-mini-outline in the autonomous-express pipeline.
- When confidence is **≥80%**; otherwise skip or propose the Related block only.

## Instructions

1. **Read the note**: Use `obsidian_read_note` to get title, main ideas, and frontmatter `project-id` (if any).

2. **Search**: Call `obsidian_global_search` with a query derived from the note (keywords, themes) and optionally project-id or project name to find related notes. When note frontmatter **`express_view`** is set (e.g. "stakeholder high-level" vs "dev technical"), shape the Related section by view (e.g. stakeholder → fewer, higher-level links; dev → more granular links).

3. **Build Related section**: Format as a markdown block (e.g. `## Related\n\n- [[Note A]] — brief reason\n- [[Note B]] — brief reason`). Use color theory for relation emphasis if appending highlighted links (e.g. complementary for contrasts, analogous for same theme).

4. **Append**: Use `obsidian_update_note(path, content, mode: append)` to add the Related section. Prefer append to avoid overwriting.

## MCP tools

- `obsidian_read_note` — read current note
- `obsidian_global_search` — find similar notes
- `obsidian_update_note` — append block (mode: append)

## Confidence gate

**≥80%**: Execute search and append. **<80%**: Propose related links only.
