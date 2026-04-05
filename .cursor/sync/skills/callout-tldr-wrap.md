---
name: callout-tldr-wrap
description: Wraps the TL;DR section in an Obsidian summary callout for glanceable emphasis. Use when running autonomous-distill pipeline after layer-promote.
---

# callout-tldr-wrap

## When to use

- After **layer-promote** in the autonomous-distill pipeline.
- **Always** run when the note has a TL;DR section (no confidence gate).

## Instructions

1. **Locate TL;DR**: Read the note with `obsidian_read_note`. Find the existing `## TL;DR` (or similar) block and its content.

2. **Wrap in callout**: Replace the raw TL;DR block with:
   ```markdown
   > [!summary] TL;DR
   > {existing TL;DR content}
   ```
   Use `obsidian_search_replace`(path, old_text, new_text) to wrap the section. Preserve the existing content; only add the callout wrapper. **Backup first** before edits.

3. **Optional**: Color-callout border via a CSS snippet tied to a color key can be documented in [Highlightr-Color-Key.md](3-Resources/Highlightr-Color-Key.md); this skill does not inject CSS.

## MCP tools

- `obsidian_read_note` — read note
- `obsidian_search_replace` — wrap TL;DR in callout (destructive; backup first)

## Confidence gate

**Always** — apply whenever a TL;DR block exists.
