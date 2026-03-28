---
name: express-mini-outline
description: Generates an outline or summary and appends it as a fenced block with project colors for sections. Use when running autonomous-express pipeline after read_note and optionally related-content-pull.
---

# express-mini-outline

## When to use

- After **obsidian_read_note** (and optionally **related-content-pull**) in the autonomous-express pipeline.
- Only when confidence is **≥85%** for appending; otherwise propose the outline only.

## Instructions

1. **Read the note**: Use `obsidian_read_note` to get structure and main ideas.

2. **Generate outline**: Use chain-of-thought to produce a concise outline or summary (headings, key points). Apply project color semantics for sections if the note has a `highlight_key` or project-id (e.g. analogous colors for related sub-ideas). When note frontmatter **`express_view`** is set (e.g. "stakeholder high-level" vs "dev technical"), shape the outline by view (e.g. stakeholder → higher-level bullets; dev → more technical detail).

3. **Format**: Append as a fenced block (e.g. markdown code block or a `## Outline` section) so it is clearly separated. Use **inline CSS only** per [Highlightr-Color-Key.md](3-Resources/Highlightr-Color-Key.md) Section 2 for any colored spans, and add `data-highlight-source="agent"` to every `<mark>` (e.g. `<mark data-highlight-source="agent" style="background: #A3D8FFA6;">Section A</mark>` for Blue). Never use `==text==` or `^{Color}` in outline output.

4. **Append**: Call `obsidian_update_note(path, content, mode: append)` with the outline block. **Backup before** any append if the pipeline has not already created a backup.

## MCP tools

- `obsidian_read_note` — read note
- `obsidian_update_note` — append outline (mode: append)

## Confidence gate

**≥85%**: Append outline. **<85%**: Propose outline in chat only.
