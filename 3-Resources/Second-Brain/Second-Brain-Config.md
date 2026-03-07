---
title: Second Brain Config
created: 2026-02-25
tags: [pkm, second-brain, config]
para-type: Resource
status: active
links: [[Resources Hub]]
---

# Second Brain Config

Single source of truth for pipeline and skill configuration. Skills and rules that need hub names or thresholds should read this note (e.g. via context or Templater/Dataview).

## hub_names

- projects: "Projects Hub"
- areas: "Areas Hub"
- resources: "Resources Hub"
- resurface: "Resurface"

## archive

- age_days: 90
- no_activity_days: 60

## highlight

- default_key: "3-Resources/Highlightr-Color-Key.md"
- **short_note_word_threshold**: 300 — post-process stabilizer: notes below this word count bias toward core (drift 0).
- **default_core_bias**: true — whether short notes get core bias.
- **mobile_emoji_fallback**: true — when mobile context detected, use emoji indicators instead of/in addition to CSS gradients.

## graph

- moc_strength: 3

## queue

- **queue_nudge_after_seconds** (optional): e.g. 30 — after this inactivity, Watcher or cron can append a reminder to Watcher-Signal.md to run Process Queue. Omit or 0 to disable.
- **queue_nudge_enabled**: true | false — when true, nudge is allowed when queue has pending entries.
- **auto_cleanup_after_process**: true | false — when true, run queue-cleanup skill after each EAT-QUEUE run (auto-mark failed entries, append to Errors.md). When false, cleanup only when user runs "Clear queue" or "Queue cleanup".
- **re_try_max_loops**: 3 — cap on re-try spins per thread (e.g. same section/phase_path). When exceeded, abort re-try and create cap-hit wrapper (A: Force approve, B: Prune branch, 0: Re-wrap full phase). Document in Parameters.md.

## snapshot

- **batch_size_for_snapshot**: 5 — when queue length (or batch size) > this value, use BATCH_SNAPSHOT_DIR for the run; when ≤ this value, use per-change snapshots per note. Fine-tunes overhead for mobile single-item vs batch.

## roadmap (optional)

- **phase_fork_heuristic**: "strict" | "off" — when "strict", expand-road-assist post-step scans expanded output for choice indicators ("or", "vs", "options:") and, if found, sets phase_forks frontmatter and auto-queues Phase Direction Wrapper creation. When "off", only explicit phase_forks frontmatter triggers wrapper creation. Document in Skills.md and expand-road-assist SKILL.

## code_comments (optional)

- **density**: medium — high | medium | minimal (default medium to avoid over-commenting).
- **required_sections**: ["why", "provenance_link"] — mandatory in plan output; optional_sections: ["assumptions", "limitations"].
- **provenance_format**: "> See [[{wrapper_link}]] for decision context" — merged into TASK-TO-PLAN-PROMPT template by prompt-crafter/task-to-prompt handler. Document in Parameters.md.

## depths (optional)

User-tunable depth-enhancement parameters. Read by depth skills and pipeline rules; enables personalization post-rollout.

- **highlight_coverage_min**: 50 — minimum % of meaningful spans to target for highlighting (distill-highlight-color). Range typically 50–70%; skill may adapt within range from content length/complexity.
- **async_loop_max_hours**: 24 — max age (hours) for async preview/refinement context when considering loop outcomes.
- **commander_macro_limits**: 5 — cap on chained commands in a single Commander macro to avoid runaway chains.
- **async_preview_threshold** (optional, in depths or top-level): e.g. 68 or 85 — below this confidence, always emit async preview and do not commit; document in Configs.md and Parameters.md.

## confidence_bands (optional)

Override default bands when present. Pipelines and skills read these; fallback to 68–84% mid, 85% high if omitted.

- **mid**: [80, 90] — mid-band range (min, max %).
- **high_threshold**: 90 — minimum % to proceed with destructive actions after snapshot.
- **non_destructive_lower** (optional): e.g. 75 — minimum % for metadata-only or preview-only steps (no destructive write). Safety unchanged for destructive (still ≥85% + snapshot). Document pros/cons in Parameters.md.

**Project MOCs**: In each project MOC note, include a "Graph Focus" callout with a Dataview query that lists notes in that project, e.g. `WHERE project-id = "Test-Project"` for quick graph context.

---

**links frontmatter:** Always an array (e.g. `links: ["[[Resources Hub]]", "[[Related]]"]`). For Dataview, use `contains(links, "[[HubName]]")` or array membership.

**Tags vs frontmatter:** Tags are convenience only (e.g. #dev-task, #bug for QuickAdd and task filters). Pipelines and core filtering use frontmatter. Do not rely on tags for ingest/distill/archive logic.

Pipelines pass this note as context or read it when resolving hub names and archive thresholds. See [Cursor-Skill-Pipelines-Reference](Cursor-Skill-Pipelines-Reference.md) for pipeline order.
