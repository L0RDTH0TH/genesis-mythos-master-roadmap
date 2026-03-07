---
name: auto-layer-select
description: Optional. Uses content complexity to suggest 1 / 2 / 3 distillation layers; LLM confidence gates whether to auto-apply or propose. Manual override remains (e.g. "distill this note with 2 layers"). Use when autonomous-distill is run with layer-selection enabled.
---

# auto-layer-select

## When to use

- **Optional** step before "distill layers" in the autonomous-distill pipeline when layer-selection is enabled.
- When the user does not specify a layer count (e.g. "distill this note with 2 layers"), use this skill to suggest 1 / 2 / 3 layers from content complexity.

## Instructions

1. **Assess complexity**: Read the note with `obsidian_read_note`. Use simple heuristics: sentence length, heading density, jargon, and length. Map to 1 (light), 2 (medium), or 3 (full) distillation layers.

2. **Suggest or apply**: If confidence is **≥85%**, apply the chosen layer count for the subsequent distill steps. If **<85%**, propose the suggestion (e.g. "Recommend 2 layers") and let the pipeline use default or user override.

3. **Manual override**: The user can always say "distill this note with 2 layers" (or 1 / 3); in that case skip this skill and use the specified count.

## MCP tools

- `obsidian_read_note` — read note to assess complexity

## Confidence gate

**≥85%**: Use suggested layer count for this run. **<85%**: Propose only; pipeline uses default or manual override.

## Integration

Referenced in `.cursor/rules/context/auto-distill.mdc` and `3-Resources/Cursor-Skill-Pipelines-Reference.md` as optional step before "distill layers" when enabled.

