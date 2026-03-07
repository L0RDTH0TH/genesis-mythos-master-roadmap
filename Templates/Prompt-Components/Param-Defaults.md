---
title: Prompt-Components Param-Defaults
created: 2026-03-06
tags: [second-brain, prompt-crafter, templates]
para-type: Resource
status: active
---

# Param defaults (Templater-enabled)

Values from [[3-Resources/Second-Brain-Config|Second-Brain-Config]] `prompt_defaults`. Replace placeholders when assembling.

- **ingest**: `context_mode: {{prompt_defaults.ingest.context_mode}}`, `max_candidates: {{prompt_defaults.ingest.max_candidates}}`, `rationale_style: {{prompt_defaults.ingest.rationale_style}}`
- **organize**: `context_mode: {{prompt_defaults.organize.context_mode}}`, `max_candidates: {{prompt_defaults.organize.max_candidates}}`

Optional dynamic (if Templater hooked): `{{tp.file.content | yaml_load | get('prompt_defaults.ingest.context_mode')}}`

## Validation snippet

Validate against: **max_candidates ≤ 10** (MCP limit per [[3-Resources/Second-Brain/MCP-Tools|MCP-Tools]]). Invalid params → log to Errors.md per mcp-obsidian-integration Error Handling Protocol.
