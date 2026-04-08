---
name: summary-preserve
description: Ensures a minimal TL;DR or summary and callout exist before archiving; preserves project color links. Use before move in the autonomous-archive pipeline.
---

# summary-preserve

## When to use

- **Before** move in the autonomous-archive pipeline (after resurface-candidate-mark).
- Only when confidence is **≥80%**; otherwise propose summary only.

## Instructions

1. **Read the note**: Use `obsidian_read_note` to check for an existing TL;DR or summary section.

2. **If no TL;DR**: Run a light distill (e.g. `obsidian_distill_note` with add_tldr: true if the tool supports a "light" mode, or a single CoT pass to add one short summary sentence). Then wrap the new TL;DR in a callout: `> [!summary] TL;DR\n> {content}` via `obsidian_search_replace`. **Backup first** before edits.

3. **Preserve highlights**: Do not strip or change existing Highlightr markup; preserve project color links so archived notes remain relationally clear.

4. **If TL;DR already exists**: Optionally ensure it is in a callout (see callout-tldr-wrap); otherwise leave as-is.

## MCP tools

- `obsidian_read_note` — read note
- `obsidian_distill_note` — light distill if no TL;DR (path, add_tldr: true)
- `obsidian_search_replace` — add or wrap TL;DR callout (destructive; backup first)

## Confidence gate

**≥80%**: Execute light distill + callout if needed. **<80%**: Propose summary only.
