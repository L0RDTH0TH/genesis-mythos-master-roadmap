---
title: Second Brain Config
created: 2026-03-02
tags: [pkm, second-brain, config]
para-type: Resource
status: active
---

hub_names:
  projects: "Genesis Mythos Hub"
  resources: "Genesis Resources Hub"
  areas: "Genesis Areas Hub"

highlight:
  default_key: "3-Resources/Highlightr-Color-Key.md"  # create this stub next if missing
  # Post-process stabilizer (distill): short-note core bias and emoji fallback
  short_note_word_threshold: 300
  default_core_bias: true       # whether short notes bias toward core (drift 0)
  mobile_emoji_fallback: true   # force emojis when mobile context detected; else CSS gradients

archive:
  age_days: 180
  no_activity_days: 60          # used with #stale/#review-later for confidence-floor boost (post-process stabilizer)

depths:
  async_preview_threshold: 75
  batch_size_for_snapshot: 8

# Prompt-crafter defaults (laptop-only). Consumed by prompt-crafter and rules (e.g. para-zettel-autopilot) for MCP pass-through; queue payload overrides take precedence. Non-destructive defaults only—params influence proposals but require approved: true for any move/rename per Pipelines § Phase 2. No auto-approval injection.
prompt_defaults:
  ingest:
    context_mode: strict-para  # For ingest/wrapper; fallback to organize for re-org
    max_candidates: 7          # Wrapper must pad to exactly 7 per Pipelines.md
    rationale_style: concise   # Per MCP-Tools.md optional
  organize:
    context_mode: organize
    max_candidates: 5
  profiles:  # Named overrides; selectable via Commander macro; fallback to pipeline default
    project-priority:
      context_mode: project-strict
      max_candidates: 5
