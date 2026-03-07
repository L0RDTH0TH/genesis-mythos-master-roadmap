---
title: Task Queue
created: 2026-02-28
tags: [roadmap, queue, eat-queue]
para-type: Resource
status: active
---

# Task Queue

Canonical queue file for roadmap/task actions. **Do not edit by hand** except for debugging; the Watcher plugin appends one JSON-like line per queued action. Process by running **EAT-QUEUE** or **PROCESS TASK QUEUE** in Cursor.

## Queue format

One line per entry. Each line is a JSON object (single line, no newlines inside). Example:

```json
{"mode": "TASK-ROADMAP", "filePath": "Ingest/My-Roadmap.md", "requestId": "abc123", "timestamp": "2026-02-28T12:00:00Z"}
```

Modes: `TASK-ROADMAP`, `TASK-COMPLETE`, `ADD-ROADMAP-ITEM`, `EXPAND-ROAD`, `REORDER-ROADMAP`, `DUPLICATE-ROADMAP`, `MERGE-ROADMAPS`, `EXPORT-ROADMAP`, `PROGRESS-REPORT`.

## Entries (appended by Watcher)

Entries appear below when the user triggers a toolbar command (TASK-ROADMAP, Task Complete, Add Roadmap Item, etc.). Run **EAT-QUEUE** to process them; results are logged to Watcher-Result.md and Mobile-Pending-Actions.md.
