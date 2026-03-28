---
title: Telemetry Dashboard
created: 2026-03-15
tags: [pkm, second-brain, observability, telemetry, run-telemetry]
para-type: Resource
status: active
links: ["[[Resources Hub]]", "[[3-Resources/Second-Brain/Logs#Run-Telemetry]]", "[[3-Resources/Vault-Change-Monitor]]"]
---

# Telemetry Dashboard

Run telemetry for **primary** and **subagents** (roadmap, research, ingest, distill, express, archive, organize). One note per run in `.technical/Run-Telemetry/` with YAML frontmatter; this dashboard queries them via Dataview. **Optional-first:** columns show data when present; missing optional fields are intentional during phased rollout. See [Logs § Run-Telemetry](3-Resources/Second-Brain/Logs.md) and [Vault-Layout § .technical/Run-Telemetry](3-Resources/Second-Brain/Vault-Layout.md).

## Runs (last 30 days)

```dataview
TABLE
  actor,
  model,
  project_id,
  success,
  util_pct,
  total_tokens,
  cost_estimate_usd,
  internals.duration_sec AS duration_sec,
  error_category
FROM ".technical/Run-Telemetry"
WHERE timestamp >= date(today) - dur(30 days)
SORT file.mtime DESC
```

When `cost_estimate_usd` exists it appears in the table; when `success != "success"`, `error_category` (and optionally `error_message`) help with root-cause. Use columns that exist; omit or show "-" for missing optional fields.

## Failed or partial runs

When `success` is not `"success"`, show error details:

```dataview
TABLE
  file.mtime AS time,
  actor,
  project_id,
  success,
  error_category,
  error_message
FROM ".technical/Run-Telemetry"
WHERE timestamp >= date(today) - dur(30 days) AND success != "success"
SORT file.mtime DESC
```

## Last 7 days by actor

```dataview
TABLE length(rows) AS runs
FROM ".technical/Run-Telemetry"
WHERE timestamp >= date(today) - dur(7 days)
GROUP BY actor
SORT runs DESC
```

## Links

- [Logs § Run-Telemetry](3-Resources/Second-Brain/Logs.md) — required/optional fields, sources
- [Parameters § Run-Telemetry](3-Resources/Second-Brain/Parameters.md) — rollout order
- [Vault-Change-Monitor](3-Resources/Vault-Change-Monitor.md) — unified observability MOC
