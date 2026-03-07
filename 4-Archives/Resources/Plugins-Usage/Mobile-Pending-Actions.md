---
title: Mobile Pending Actions
created: 2026-02-28
tags: [roadmap, mobile, queue]
para-type: Resource
status: active
---

# Mobile Pending Actions

Queue discoverability and post-process status. Updated by the Watcher plugin when a task/roadmap action is queued, and **always** updated by the EAT-QUEUE processor when each entry is processed (e.g. "TASK-COMPLETE: Success" or "Failed: Subtasks pending").

Use this note to see what was queued from mobile and what the last EAT-QUEUE run did.

## In-note pending banner (contract)

When an action is queued (e.g. Task Complete, Add Roadmap Item), the Watcher plugin or a Cursor-side rule can append a **temporary callout** to the **affected note** or to this file. Standard text:

`> [!note] Pending: <mode> queued — run **PROCESS TASK QUEUE** or **EAT-QUEUE** to apply.`

After a successful run, **banner cleanup** (auto-queue-processor) removes these callouts from affected notes when success count > failure count. See [[.cursor/rules/context/auto-queue-processor|auto-queue-processor]].

## Last processed

(Updated by Cursor when EAT-QUEUE runs.) **Shows both success and failure lines** — e.g. "TASK-COMPLETE: Success" or "Failed: Subtasks incomplete". Task/roadmap skills (e.g. task-complete-validate) always append failure reason to this section so mobile users see why an action did not apply.

- **standard-lock-final** (roadmap-ingest): Success — Canonical Roadmap-Standard-Format applied; Genesis-Mythos master + 6 phase roadmaps created under `1-Projects/Genesis-Mythos/Roadmap/`; [[Genesis-Mythos-Roadmap-MOC]] created. geosynchronous-view and links preserved.
