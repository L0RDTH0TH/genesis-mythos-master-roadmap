---
title: Prompt-Components Guidance-Default
created: 2026-03-06
tags: [second-brain, prompt-crafter, templates]
para-type: Resource
status: active
---

# Guidance-aware default (fixed string)

Include this in every assembled prompt so the agent consistently loads guidance and applies boost when set.

**Text**: Use note `user_guidance` when present; else queue `prompt`. Apply `guidance_conf_boost` if set (per [[.cursor/rules/always/guidance-aware|guidance-aware]]). Do not override user_guidance; inject defaults only where missing.
