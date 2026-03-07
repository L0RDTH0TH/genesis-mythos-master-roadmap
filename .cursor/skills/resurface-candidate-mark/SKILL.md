---
name: resurface-candidate-mark
description: Marks high-potential notes (links, highlights) with resurface-candidate frontmatter and optionally appends to a Resurface hub. Use before move in the autonomous-archive pipeline.
---

# resurface-candidate-mark

## When to use

- **Before** move in the autonomous-archive pipeline (after archive-check and subfolder-organize path is decided).
- When confidence is **≥75%** that the note has high resurface potential; otherwise skip.

## Instructions

1. **Assess potential**: Read the note with `obsidian_read_note`. High potential: many outgoing/incoming links, highlighted key ideas, or strong relevance to active projects. Use chain-of-thought to score.

2. **Mark**: If high potential, set frontmatter via `obsidian_manage_frontmatter`(path, key: "resurface-candidate", value: "true", action: set).

3. **Optional**: Append to a Resurface hub using `obsidian_append_to_hub`. Hub names: prefer [Second-Brain-Config.md](3-Resources/Second-Brain-Config.md) hub_names (e.g. resurface: "Resurface"); fallback to "Resurface", "Projects Hub", etc. if config is not available.

4. **Color theory**: When presenting in hub views, analogous colors can group related resurface candidates; document in pipeline or Highlightr key if needed.

## MCP tools

- `obsidian_read_note` — read note
- `obsidian_manage_frontmatter` — set resurface-candidate (path, key, value, action: set)
- `obsidian_append_to_hub` — optional append to Resurface hub

## Confidence gate

**≥75%**: Set flag and optionally append to hub. **<75%**: Skip.
