---
name: highlight-perspective-layer
description: Applies drift level via data-drift-level attribute and stores highlight_angles in frontmatter. Runs after distill-highlight-color in autonomous-distill (and optionally after highlight in ingest). CSS renders gradients (solid → fade); this skill only sets the attribute.
---

# highlight-perspective-layer

## When to use

- After **distill-highlight-color** in the autonomous-distill pipeline (and optionally after highlight in ingest).
- Only when confidence is **≥85%**; for mid-band (68–84%), produce **preview-only** (e.g. append a small callout with proposed drift/angles) and do not write back. Per mcp-obsidian-integration, snapshot before any destructive step.

## Instructions

1. **Read the note**: Use `obsidian_read_note`. Identify existing `<mark>` spans (agent or user). Decide **drift level** per span: 0 = core (solid), 1–3 = fading relevance. Use content semantics (e.g. main thesis = 0, supporting = 1, tangential = 2–3).

2. **Apply drift level**: Add or update **`data-drift-level="0"`** … **`data-drift-level="3"`** on each `<mark>` or wrapper. The skill **only sets the attribute**; vault CSS (snippet or Highlightr-compatible) renders gradients (e.g. solid → fade) from `data-drift-level`. Document in skill docs that CSS does the visual.

3. **Angles**: Update frontmatter **`highlight_angles: [list]`** (e.g. `["combat", "performance"]`) when applying a layer run so that "SWITCH HIGHLIGHT ANGLE" or multi-angle runs have a clear list. Add or merge angles used in this run.

4. **Edit**: Apply via `obsidian_search_replace` or `obsidian_update_note`. **Backup and per-change snapshot first** (see mcp-obsidian-integration) before in-place edits.

5. **Observability**: Log **drift levels** applied and **angles** (e.g. count of spans per level, highlight_angles list) in [Distill-Log.md](3-Resources/Distill-Log.md) for MOC aggregation.

6. **Mobile sync**: When a run produces layered output (e.g. multiple angles), append a short bulleted summary by angle to [Mobile-Pending-Actions](3-Resources/Mobile-Pending-Actions.md) (e.g. "Angle X: 3 highlights; Angle Y: 5 highlights") so mobile users see what was shaped.

## Triggers (context / queue)

- **SWITCH HIGHLIGHT ANGLE: [angle]** — Set current angle (e.g. frontmatter `highlight_active_angle`) and optionally re-run highlight step for that angle only; or document that switching is CSS/Dataview-driven (e.g. CSS hides/shows by angle class).
- **HIGHLIGHT MULTI-ANGLE: [list]** — Queue multiple runs (one per angle) or a single batch run that applies multiple angles and writes `highlight_angles`; document in Queue-Sources as new mode or variant of DISTILL MODE with payload.

## MCP tools

- `obsidian_read_note` — read note and existing marks
- `obsidian_search_replace` / `obsidian_update_note` — add data-drift-level, update highlight_angles (destructive; backup + snapshot first)
- `obsidian_manage_frontmatter` — set highlight_angles, highlight_active_angle

## Confidence gate

**≥85%**: Execute drift/angle edits. **68–84%**: Preview only (callout with proposed drift/angles; do not write back). **<68%**: Propose only; no writes.

## Reference

- [Color-Coded-Highlighting](3-Resources/Second-Brain/Color-Coded-Highlighting.md) — perspective guidelines; fallback to emojis for drift on mobile if CSS lags.
- [Highlightr-Color-Key](3-Resources/Highlightr-Color-Key.md) — storage format; use same `<mark>` format when adding attributes.
