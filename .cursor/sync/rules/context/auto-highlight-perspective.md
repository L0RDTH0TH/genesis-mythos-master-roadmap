---
description: "Trigger highlight pass with a perspective lens. When user says HIGHLIGHT PERSPECTIVE: [lens], invoke distill pipeline or dedicated highlight step with perspective set from the phrase; scope to current note or batch from queue/signal."
globs:
  - "1-Projects/**/*.md"
  - "2-Areas/**/*.md"
  - "3-Resources/**/*.md"
  - "!4-Archives/**"
  - "!Backups/**"
  - "!Templates/**"
  - "!**/Log*.md"
  - "!**/* Hub.md"
alwaysApply: false
---

# Auto-highlight-perspective (context rule)

- **Purpose**: When the user triggers **HIGHLIGHT PERSPECTIVE: [lens]** (e.g. "HIGHLIGHT PERSPECTIVE: combat systems"), invoke a highlight pass on the current note or batch with `perspective` set from the phrase. This rule **sets context** (frontmatter or queue payload); it defers to auto-distill or full-autonomous-ingest for actual pipeline steps.
- **Reference**: See [Cursor-Skill-Pipelines-Reference](3-Resources/Cursor-Skill-Pipelines-Reference.md) and [distill-highlight-color](.cursor/skills/distill-highlight-color/SKILL.md). MCP safety: obey [mcp-obsidian-integration](.cursor/rules/always/mcp-obsidian-integration.mdc).

## How to activate

- **Trigger phrase**: **HIGHLIGHT PERSPECTIVE: [lens]** (e.g. "HIGHLIGHT PERSPECTIVE: combat systems", "HIGHLIGHT PERSPECTIVE: performance").
- **Commander**: This trigger can be surfaced via Commander (e.g. "Queue Highlight: Combat" macro that prompts for lens and appends to queue); see Commander deepening §2.3.

## Behavior

1. **Parse lens** from the phrase (text after "HIGHLIGHT PERSPECTIVE:").
2. **Set context**: Either set note frontmatter **`highlight_perspective: [lens]`** for the current note, or append a queue entry (e.g. to prompt-queue.jsonl) with `mode` appropriate for a highlight pass and payload including `perspective: [lens]`.
3. **Invoke pipeline**: Run autonomous-distill (or a dedicated highlight step) on the current note or batch, with `perspective` passed so distill-highlight-color applies lens-focused analogous colors.
4. **Scope**: Current note when triggered in-editor; batch when triggered with a list or from queue.

## Observability

- When the run is executed, pipeline log (e.g. Distill-Log.md) should include **coverage %** and **perspective** (and **coverage_adapted** when adaptive coverage is used) for MOC aggregation.

## Exclusions

Same as auto-distill: exclude 4-Archives, Backups, Templates, Logs, Hub notes. Do not process notes with `watcher-protected: true`.
