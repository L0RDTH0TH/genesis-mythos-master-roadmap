---
name: express-view-layer
description: Applies gradient or strength indicators in Related section for connection strength. Uses project colors. Runs after related-content-pull when express_view is set.
---

# express-view-layer

## When to use

- After **related-content-pull** in the autonomous-express pipeline when **express_view** is set (frontmatter or param, e.g. "stakeholder high-level" vs "dev technical").
- Only when confidence is **≥85%**; for mid-band propose only (e.g. callout with proposed strength indicators).

## Parameters (optional)

- **express_view** (from note frontmatter or param): e.g. "stakeholder high-level", "dev technical". Shapes how connection strength is presented.

## Instructions

1. **Read the note**: Use `obsidian_read_note`. Locate the **Related** section. Check frontmatter for **`express_view`** if present.

2. **Apply connection strength**: For each related link or block, assign a strength level (e.g. strong / medium / weak). Add **data-connection-strength** attribute or class (e.g. `data-connection-strength="strong"`) so CSS can style. Use project colors from `highlight_key` where applicable.

3. **Edit**: Apply via `obsidian_search_replace` or `obsidian_update_note`. **Backup and per-change snapshot first** before appends.

4. **Observability**: Log **view** and **relation stats** (e.g. express_view, count of strong/medium/weak) in [Express-Log.md](3-Resources/Express-Log.md) for MOC aggregation.

## MCP tools

- `obsidian_read_note` — read note and Related section
- `obsidian_search_replace` / `obsidian_update_note` — add strength indicators (backup + snapshot first)

## Confidence gate

**≥85%**: Execute strength indicators. **68–84%**: Preview only. **<68%**: Propose only; no writes.

## Reference

- [related-content-pull](.cursor/skills/related-content-pull/SKILL.md) — builds the Related section.
- [express-mini-outline](.cursor/skills/express-mini-outline/SKILL.md) — outline with project colors; express_view shapes both outline and Related.
