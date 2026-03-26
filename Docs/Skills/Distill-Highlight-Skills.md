# Distill and Highlight Skills Overview

**Version: 2026-03 – post-subagent migration**

Overview of skills used by the Distill subagent: distill layers, highlight color, perspective layer, layer-promote, callout-tldr-wrap, readability, and related.

---

## Purpose

Single reference for which skills the Distill pipeline calls and when. Skill definitions live in `.cursor/skills/<skill-name>/SKILL.md`.

---

## Core distill skills

| Skill | When used |
|-------|-----------|
| **auto-layer-select** | Optional: suggest 1/2/3 layers; read distill_lens from frontmatter or wrapper override. |
| **distill-highlight-color** | After distill layers: project-aware highlights (≥85%); uses master key + project highlight_key; color theory (analogous/complementary). |
| **highlight-perspective-layer** | When perspective/lens set: apply drift level via data-drift-level attribute; store highlight_angles in frontmatter; CSS renders gradients (solid → fade). |
| **layer-promote** | After distill-highlight-color: bold → highlight → TL;DR; project color overrides; contrast colors for conflicting ideas. |
| **distill-perspective-refine** | When distill_lens set: add emojis or gradient indicators in TL;DR callout for depth/drift (core vs fading relevance). |
| **callout-tldr-wrap** | After layer-promote: wrap TL;DR in `> [!summary] TL;DR`. |
| **readability-flag** | End of pipeline: set needs-simplify frontmatter and insert warning callout when note readability is low. |

---

## Apply-from-wrapper

| Skill | When used |
|-------|-----------|
| **distill-apply-from-wrapper** | EAT-QUEUE Step 0: when an approved Decision Wrapper has pipeline distill, re-run autonomous-distill on original_path with approved_option as distill_lens override. Invoked by Queue rule, not by the Distill subagent directly; the Queue applies the wrapper then dispatches to Distill with the override. |

---

## Related (ingest / express)

| Skill | When used |
|-------|-----------|
| **highlight-seed-enhance** | SEEDED-ENHANCE queue mode or mobile-seed-detect: detect user `<mark>` (no data-highlight-source); treat as cores; extend with AI using analogous color and optional drift gradient. |
