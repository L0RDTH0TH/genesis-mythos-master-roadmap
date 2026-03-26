---
name: highlight-seed-enhance
description: Detects user <mark> (no data-highlight-source), treats them as cores (solid color), extends with AI using analogous color and optional drift gradient. Use when running SEEDED-ENHANCE queue mode or when mobile-seed-detect rule triggers.
---

# highlight-seed-enhance

## When to use

- When a note has **user highlights** (plain `<mark>` without `data-highlight-source`), e.g. from Highlightr UI or mobile capture.
- Triggered by **SEEDED-ENHANCE** queue mode or by rule **mobile-seed-detect** (glob/queue for notes with user highlights).
- Only when confidence is **≥85%**; else propose extensions in a callout only.

## Instructions

1. **Detect seeds**: Read the note with `obsidian_read_note`. Find every `<mark>` that has **no** `data-highlight-source` attribute (i.e. user/Highlightr UI highlights). Treat these as "cores" (solid color; keep or assign from semantic key).

2. **Optional tagging**: When extending from a seed, add `data-highlight-source="user-seed"` to **agent-added** spans so they remain distinguishable from the original user mark. Do not overwrite the user's `<mark>` with agent attribute unless you are extending in-place; when extending, new spans get `data-highlight-source="agent"` and can reference the seed.

3. **Extend from seeds**: For each user seed, consider the same paragraph or list: extend to **related phrases** with analogous color (same theme = same hue family). Optionally add light gradient (drift) from seed to extended span (e.g. seed = drift 0, extended = drift 1). Use the same storage format as [Highlightr-Color-Key](3-Resources/Highlightr-Color-Key.md) (Section 2).

4. **Edit**: Apply via `obsidian_search_replace` or `obsidian_update_note`. **Backup and per-change snapshot first** (see mcp-obsidian-integration) before in-place edits.

5. **Observability**: Log **seed count** (and optionally spans added) in [Organize-Log](3-Resources/Organize-Log.md) or [Feedback-Log](3-Resources/Feedback-Log.md) for MOC/analytics.

## MCP tools

- `obsidian_read_note` — find user `<mark>` (no data-highlight-source)
- `obsidian_search_replace` / `obsidian_update_note` — add extended spans, optional data-highlight-source on new marks (destructive; backup + snapshot first)

## Confidence gate

**≥85%**: Execute seed extension edits. **<85%**: Propose extensions in a callout only; do not write back.

## Reference

- [Highlightr-Color-Key](3-Resources/Highlightr-Color-Key.md) — storage format; agent vs user (Section 3).
- [Color-Coded-Highlighting](3-Resources/Second-Brain/Color-Coded-Highlighting.md) — analogous colors for related ideas.
- [mobile-seed-detect](.cursor/rules/context/mobile-seed-detect.mdc) — rule that queues SEEDED-ENHANCE for notes with user highlights.
