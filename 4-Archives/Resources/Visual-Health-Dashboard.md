---
title: Visual Health Dashboard
created: 2026-02-25
tags: [pkm, second-brain, dataview, dashboard]
para-type: Resource
status: active
---

# Visual Health Dashboard

**Last refreshed:** `$= dv.current().file.mtime`

> Quick glance at distillation quality, highlight discipline, actionability, and highlight consistency across active PARA notes.

## Core scope

Active notes in **1-Projects**, **2-Areas**, **3-Resources** (excludes Archives, Backups, Templates, Ingest, *Log*.md, *Hub.md).

```dataviewjs
await dv.view("3-Resources/_dv-visual-health-dashboard", { dv });
```

## 3. Actionable / review candidates (list)

Notes flagged for attention (needs-simplify, resurface-candidate, or non-empty next-actions). Summary counts are in the script output above.

```dataview
LIST WITHOUT ID file.link
FROM "1-Projects" OR "2-Areas" OR "3-Resources"
WHERE (needs-simplify = true OR resurface-candidate = true OR next-actions)
AND !contains(file.path, "Backups")
AND !contains(file.path, "Log")
SORT file.mtime DESC
LIMIT 20
```
