---
description: "Trigger express run with a view. When user says EXPRESS VIEW: [angle], set frontmatter express_view and run express pipeline (e.g. stakeholder high-level vs dev technical)."
globs:
  - "1-Projects/**/*.md"
  - "2-Areas/**/*.md"
  - "3-Resources/**/*.md"
  - "!4-Archives/**"
  - "!Backups/**"
  - "!**/Log*.md"
  - "!**/* Hub.md"
alwaysApply: false
---

# Auto-express-view (context rule)

- **Purpose**: When the user triggers **EXPRESS VIEW: [angle]** (e.g. "EXPRESS VIEW: stakeholder high-level", "EXPRESS VIEW: dev technical"), set note frontmatter **`express_view: [angle]`** and run the autonomous-express pipeline. related-content-pull and express-mini-outline (and express-view-layer) then shape the outline and Related section by view.
- **Reference**: [Cursor-Skill-Pipelines-Reference](3-Resources/Cursor-Skill-Pipelines-Reference.md), [express-mini-outline](.cursor/skills/express-mini-outline/SKILL.md), [related-content-pull](.cursor/skills/related-content-pull/SKILL.md), [express-view-layer](.cursor/skills/express-view-layer/SKILL.md). MCP safety: [mcp-obsidian-integration](.cursor/rules/always/mcp-obsidian-integration.mdc).

## How to activate

- **Trigger phrase**: **EXPRESS VIEW: [angle]** (e.g. "EXPRESS VIEW: stakeholder high-level", "EXPRESS VIEW: dev technical").
- **Queue mode or phrase**: **ITERATE EXPRESS: [feedback]** for feedback-driven re-runs with previews.

## Behavior

1. **Parse angle** from the phrase (text after "EXPRESS VIEW:").
2. **Set context**: Set note frontmatter **`express_view: [angle]`** for the current note (or note in queue), then run autonomous-express.
3. **Pipeline**: autonomous-express runs; related-content-pull and express-mini-outline use `express_view` to shape output; express-view-layer applies connection strength indicators when view is set.

## Mobile exports

- Document or add queue modes **EXPORT-HIGHLIGHTS** / **EXPORT-ROADMAP** for phone-friendly views (e.g. PDF with gradients). Implementation can be "append to Mobile-Pending-Actions with instructions" or link to export plugin until a concrete export step exists.

## Observability

- When the run is executed, Express-Log.md should include **view** and **relation stats** (e.g. express_view used, connection strength counts) for MOC aggregation.

## Exclusions

Same as auto-express: exclude 4-Archives, Backups, Logs, Hub notes. Do not process notes with `watcher-protected: true`.
