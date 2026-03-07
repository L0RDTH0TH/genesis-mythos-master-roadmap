---
title: Feedback Log
created: 2026-03-01
tags: [pkm, second-brain, logs, feedback, observability]
para-type: Resource
status: active
links: ["[[Resources Hub]]", "[[3-Resources/Second-Brain/Logs]]"]
---

# Feedback Log

Aggregated user-refinement stats, loop outcomes, and queue analytics. Used for MOC aggregation (e.g. [Vault-Change-Monitor](3-Resources/Vault-Change-Monitor.md)) and evolution monitoring.

## Purpose

- **Loop outcomes**: Log when mid-band loops run (pre_loop_conf, post_loop_conf, loop_outcome, loop_type).
- **User refinements**: e.g. "40% of previews refined — consider increasing default depth"; aggregate from pipeline runs and queue-cleanup.
- **Queue analytics**: Batch merge counts (overlap detection), preview caps, commander_macro stats (e.g. "Most used: Queue Perspective (15x this week)").
- **Dataview-friendly fields**: drift_avg, loop_refinements_count, and other numeric/categorical fields for queries.

## Format (per entry)

One line or short block per run; no PII. Example fields:

- timestamp (ISO 8601 or YYYY-MM-DD HH:MM)
- pipeline or source (e.g. queue-cleanup, async-loop, distill)
- loop_attempted, pre_loop_conf, post_loop_conf, loop_outcome, loop_reason
- drift_avg (when applicable)
- loop_refinements_count (when applicable)
- commander_macro (when Commander-triggered)
- summary (one-line, e.g. "User refines 40% of previews")

## Rotation

- Rotate with [log-rotate](.cursor/skills/log-rotate/SKILL.md) (e.g. monthly or with other pipeline logs). See [Logs.md](3-Resources/Second-Brain/Logs.md) for rotation spec.

## See also

- [Logs](3-Resources/Second-Brain/Logs.md) — all log destinations and rotation
- [Parameters](3-Resources/Second-Brain/Parameters.md) — Async-Loop Flow, confidence bands
- [Queue-Sources](3-Resources/Second-Brain/Queue-Sources.md) — queue modes and Commander-Sourced
