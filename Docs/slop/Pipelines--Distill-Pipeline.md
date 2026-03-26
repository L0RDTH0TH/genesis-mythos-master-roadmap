# Distill Pipeline

**Version: 2026-03 – post-subagent migration**

Documents the autonomous-distill pipeline: progressive summarization, highlights, TL;DR, readability; distill-apply-from-wrapper when an approved wrapper applies.

---

## Purpose

Single reference for distill steps, confidence bands, and return format. Implementation in `.cursor/agents/distill.md` and legacy-agents/distill.mdc.

---

## Pipeline steps

1. **Backup** — obsidian_create_backup for the note.
2. **Optional** — batch >5: garden_review (distill_candidates); then run on that set.
3. **Optional auto-layer-select** — suggest 1/2/3 layers; read distill_lens from frontmatter or wrapper override.
4. **Distill layers** — standard layers (lens when distill_lens set).
5. **distill-highlight-color** — project-aware highlights (≥85%); highlight-perspective-layer when perspective/lens set.
6. **layer-promote** — bold → highlight → TL;DR (≥85%).
7. **distill-perspective-refine** — depth/drift in TL;DR when distill_lens set.
8. **callout-tldr-wrap** — wrap TL;DR in `> [!summary] TL;DR`.
9. **readability-flag** — needs-simplify + warning when low readability.
10. **Logging** — obsidian_log_action; Distill-Log.md, Backup-Log.md. If tag agent-research, set research_distilled: true after pass.

---

## Confidence

- **High (≥85):** Snapshot then full structural distill.
- **Mid (68–84):** Self-critique loop; if post_loop_conf ≥85 snapshot and run; else Decision Wrapper under Ingest/Decisions/Refinements/ (mid-band-refinement, pipeline distill).
- **Low (<68):** Decision Wrapper under Ingest/Decisions/Low-Confidence/.
- **Loop logging:** loop_attempted, loop_band, pre/post_loop_conf, loop_outcome, loop_type "distill-depth", loop_reason.

**Exclusions:** 4-Archives/, Backups/, Templates/, **/Log*.md, **/* Hub.md.

**Return:** One-paragraph summary; any wrapper created; Success / #review-needed / failure. Watcher-Result when requestId provided.
