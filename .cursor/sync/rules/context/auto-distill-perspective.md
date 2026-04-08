---
description: "Trigger distill run with a lens. When user says DISTILL LENS: [angle], set frontmatter distill_lens and/or pass to distill run; pipeline runs as usual with lens applied (e.g. beginner/simple vs expert/deep)."
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

# Auto-distill-perspective (context rule)

- **Purpose**: When the user triggers **DISTILL LENS: [angle]** (e.g. "DISTILL LENS: beginner", "DISTILL LENS: expert/deep"), set note frontmatter **`distill_lens: [angle]`** and/or pass the lens to the distill run. The autonomous-distill pipeline then runs as usual with the lens applied (e.g. auto-layer-select and distill-perspective-refine use it to shape layers and TL;DR depth indicators).
- **Reference**: [Cursor-Skill-Pipelines-Reference](3-Resources/Cursor-Skill-Pipelines-Reference.md), [auto-layer-select](.cursor/skills/auto-layer-select/SKILL.md), [distill-perspective-refine](.cursor/skills/distill-perspective-refine/SKILL.md). MCP safety: [mcp-obsidian-integration](.cursor/rules/always/mcp-obsidian-integration.mdc).

## How to activate

- **Trigger phrase**: **DISTILL LENS: [angle]** (e.g. "DISTILL LENS: beginner", "DISTILL LENS: expert/deep").
- **Async**: Queue **REFINE DISTILL: [feedback]** with previews (e.g. to Mobile-Pending-Actions or callout) for iterative refinement.

## Behavior

1. **Parse angle** from the phrase (text after "DISTILL LENS:").
2. **Set context**: Set note frontmatter **`distill_lens: [angle]`** for the current note (or note in queue), then run autonomous-distill (or queue a DISTILL MODE entry with payload including `distill_lens`).
3. **Pipeline**: autonomous-distill runs with lens applied; distill-perspective-refine and auto-layer-select read `distill_lens` to shape depth and TL;DR indicators.

## Observability

- When the run is executed, Distill-Log.md should include **lens** and **gradient stats** (e.g. distill_lens used, drift levels in TL;DR) for MOC aggregation.

## Exclusions

Same as auto-distill: exclude 4-Archives, Backups, Logs, Hub notes. Do not process notes with `watcher-protected: true`.
