---
name: distill-perspective-refine
description: Adds emojis or gradient indicators in TL;DR callout for depth/drift (core vs fading relevance). Runs after layer-promote in autonomous-distill. Use distill_lens from frontmatter when set.
---

# distill-perspective-refine

## When to use

- After **layer-promote** in the autonomous-distill pipeline.
- Only when confidence is **≥85%**; for mid-band (68–84%), produce preview-only (e.g. proposed indicators in a callout) and do not write back. Per mcp-obsidian-integration, snapshot before any destructive step if rewriting note content.

## Parameters (optional)

- **distill_lens** (from note frontmatter or param): e.g. "beginner/simple" vs "expert/deep". When set, shape depth indicators toward that lens (e.g. simpler lens → fewer levels; expert → more granular drift).

## Instructions

1. **Read the note**: Use `obsidian_read_note`. Locate the TL;DR callout (e.g. `> [!summary] TL;DR` or existing callout-tldr-wrap output). Check frontmatter for **`distill_lens`** if present.

2. **Add depth/drift indicators**: Within the TL;DR block, add emojis or gradient indicators for depth/drift (e.g. core vs fading relevance). Use existing callout format; avoid breaking Reading mode. Examples: 🔵 core point, 🟢 supporting, ⚪ fading; or inline markers that CSS can style from `data-drift-level` if the note already has highlight-perspective-layer output.

3. **Edit**: Apply via `obsidian_search_replace` or `obsidian_update_note`. **Backup and per-change snapshot first** before in-place edits.

4. **Observability**: Log **lens** used and **gradient stats** (e.g. distill_lens, count of levels in TL;DR) in [Distill-Log.md](3-Resources/Distill-Log.md) for MOC aggregation.

## MCP tools

- `obsidian_read_note` — read note and TL;DR callout
- `obsidian_search_replace` / `obsidian_update_note` — add indicators in TL;DR (destructive; backup + snapshot first)

## Confidence gate

**≥85%**: Execute TL;DR refinement. **68–84%**: Preview only (callout with proposed indicators). **<68%**: Propose only; no writes.

## Reference

- [layer-promote](.cursor/skills/layer-promote/SKILL.md) — produces the TL;DR that this skill refines.
- [callout-tldr-wrap](.cursor/skills/callout-tldr-wrap/SKILL.md) — wraps TL;DR in summary callout.
- [auto-layer-select](.cursor/skills/auto-layer-select/SKILL.md) — layer count; when distill_lens is set, shape toward that lens.
