---
title: Vault Change Monitor
created: 2026-03-01
tags: [pkm, second-brain, observability, moc, dashboard]
para-type: Resource
status: active
links: ["[[Resources Hub]]", "[[3-Resources/Second-Brain/Logs]]"]
---

# Vault Change Monitor (MOC)

Unified observability dashboard for pipeline activity, errors, and Commander-triggered events. Use this note as the single place to see recent changes and system health.

## Purpose

- **Last N entries**: Dataview queries over pipeline logs (Ingest-Log, Distill-Log, Archive-Log, Express-Log, Organize-Log) for the last 50 (or N) entries, filterable by pipeline and error.
- **Timelines**: Dataview tables for recent changes (timestamp, note_path, pipeline, confidence, actions).
- **Commander Dashboard**: Section for Commander-triggered events — Dataview table for macros used, entries with `commander_source: true` (e.g. "Macros used this week").
- **System Health**: Integrate **health_check** output; link or embed from [MCP-Health-YYYY-MM](3-Resources/MCP-Health-YYYY-MM.md) (e.g. monthly rotation) into a "System Health" section.
- **Links**: Links to full logs (Ingest-Log, Distill-Log, Archive-Log, Express-Log, Organize-Log), [Errors](3-Resources/Errors.md), [Feedback-Log](3-Resources/Feedback-Log.md), [Watcher-Result](3-Resources/Watcher-Result.md).

## Log sources

| Log | Path | Role |
|-----|------|------|
| Ingest-Log | 3-Resources/Ingest-Log.md | Ingest pipeline entries |
| Distill-Log | 3-Resources/Distill-Log.md | Distill pipeline; coverage, lens, drift |
| Archive-Log | 3-Resources/Archive-Log.md | Archive pipeline |
| Express-Log | 3-Resources/Express-Log.md | Express pipeline; view, relation stats |
| Organize-Log | 3-Resources/Organize-Log.md | Organize pipeline |
| Feedback-Log | 3-Resources/Feedback-Log.md | Loop outcomes, queue analytics, commander_macro |
| Backup-Log | 3-Resources/Backup-Log.md | Snapshots, backup paths |
| Errors | 3-Resources/Errors.md | Error entries (pipeline, severity, commander_macro) |
| Watcher-Result | 3-Resources/Watcher-Result.md | Request results (requestId, status, completed) |

## Commander Dashboard

Dataview query (example): list entries from pipeline logs or Feedback-Log where `commander_source = true` or `commander_macro` is set; group by commander_macro for "Macros used this week" or similar. Adjust query to your log format (e.g. inline table rows or frontmatter).

## Consistent fields (for Dataview)

All pipeline logs should expose at minimum: **timestamp**, **note_path**, **pipeline**, **confidence**, **actions** (and backup/snapshot paths, flag). For loop runs: **loop_attempted**, **loop_band**, **pre_loop_conf**, **post_loop_conf**, **loop_outcome**, **loop_type**, **loop_reason**. Errors: **pipeline**, **severity**, **approval**, **timestamp**, **error_type**, **commander_macro** (when applicable). See [Logs](3-Resources/Second-Brain/Logs.md) and [Cursor-Skill-Pipelines-Reference](3-Resources/Cursor-Skill-Pipelines-Reference.md) Log format.

## MOC Refresh

Commander macro **"MOC Refresh"** (optional): run health_check + aggregate or link latest log summaries into this note. Document in [Commander-Plugin-Usage](3-Resources/Commander-Plugin-Usage.md).

## See also

- [Logs](3-Resources/Second-Brain/Logs.md) — Unified Dashboard; log → MOC flow
- [Backbone](3-Resources/Second-Brain/Backbone.md) — Unified Observability, Evolution Monitoring
- [Vault-Layout](3-Resources/Second-Brain/Vault-Layout.md) — folder tree; MOC and flow
