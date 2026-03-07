---
title: Prompt-Components Error-Handling-Template
created: 2026-03-06
tags: [second-brain, prompt-crafter, templates]
para-type: Resource
status: active
---

# If invalid: Log to Errors.md with trace per mcp-obsidian-integration.mdc

Validation failures (invalid params, unknown keys, enum mismatch) must be logged to [[3-Resources/Errors|Errors.md]] following the Error Handling Protocol in [[.cursor/rules/always/mcp-obsidian-integration|mcp-obsidian-integration]]. Include pipeline, stage, affected path(s), and suggested fix (e.g. "rationale_style not in [concise, detailed, bullet, technical]").
