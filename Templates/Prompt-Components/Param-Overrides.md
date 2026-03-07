---
title: Prompt-Components Param-Overrides
created: 2026-03-06
tags: [second-brain, prompt-crafter, templates]
para-type: Resource
status: active
---

# Param overrides (user-selectable)

References [[3-Resources/Second-Brain-Config|Second-Brain-Config]] `prompt_defaults.profiles`. Selectable via Commander macro; fallback to pipeline default.

**Example profiles** (from Config):
- **default**: use pipeline block (ingest / organize)
- **project-priority**: `context_mode: project-strict`, `max_candidates: 5`

When assembling: if user chose a profile, merge its keys over the pipeline default; otherwise use pipeline block only.
