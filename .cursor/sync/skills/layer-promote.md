---
name: layer-promote
description: Promotes progressive summarization layers (bold → highlight → TL;DR) with project color overrides and contrast colors for conflicting ideas. Use when running autonomous-distill pipeline after distill-highlight-color.
---

# layer-promote

## When to use

- After **distill-highlight-color** in the autonomous-distill pipeline.
- Only when confidence is **≥85%**; otherwise propose promotions only.

## Instructions

1. **Read the note**: Use `obsidian_read_note` to see current layers (bold, highlight, TL;DR). Check frontmatter for `highlight_key` or project-id for color overrides.

2. **Promote layers**: Use chain-of-thought to decide what to promote:
   - Bold key phrases that are not yet highlighted → add highlight with appropriate color. Any new `<mark>` you add **must** include `data-highlight-source="agent"` (see Highlightr-Color-Key Section 3).
   - Highlighted content that deserves TL;DR → add or refine the TL;DR sentence.
   - For **conflicting or opposing ideas**, use complementary colors (e.g. orange for tension, blue for main idea) so relations are clear.

3. **Edit**: Apply changes via `obsidian_search_replace` for each promotion. **Backup first** (obsidian_create_backup) before in-place edits.

4. **Preserve structure**: Keep user sections (e.g. "What am I thinking?", "What does this seem to mean?") intact; only refine the summarization layers.

## MCP tools

- `obsidian_read_note` — read note and frontmatter
- `obsidian_search_replace` — promote bold → highlight → TL;DR (destructive; backup first)

## Confidence gate

**≥85%**: Execute promotions. **<85%**: Propose changes only.
