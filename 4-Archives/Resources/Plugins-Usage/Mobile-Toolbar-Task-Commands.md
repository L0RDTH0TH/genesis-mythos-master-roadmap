---
title: Mobile Toolbar Task Commands
created: 2026-02-28
tags: [roadmap, tasks, mobile, watcher, eat-queue]
para-type: Resource
status: active
links: ["[[Resources Hub]]", "[[Master Goal]]", "[[3-Resources/Roadmap-Standard-Format]]"]
---

# Mobile Toolbar Task Commands

Roadmap and task actions from the mobile toolbar are **queued** only; they are processed when you run **EAT-QUEUE** or **PROCESS TASK QUEUE** in Cursor. Roadmaps are manual-first: you trigger the action, Cursor assists (validation, formatting, snapshots).

## Quick-start

1. Add a roadmap note under `1-Projects/<Project>/Roadmap/` or ingest one via **TASK-ROADMAP** (see [[3-Resources/Roadmap-Standard-Format]]).
2. From mobile (or desktop), use the Watcher toolbar: **TASK-ROADMAP**, **Task Complete**, or **Add Roadmap Item**.
3. In Cursor, say **EAT-QUEUE** or **PROCESS TASK QUEUE** to process all queued entries.
4. Check [[3-Resources/Mobile-Pending-Actions]] and [[3-Resources/Watcher-Result]] for status.

## Toolbar entries (Watcher)

| Command | Icon | Behavior |
|--------|------|----------|
| **TASK-ROADMAP** | list-checks | Queues current (or chosen) file for roadmap ingest. Run EAT-QUEUE to standardize and place in `1-Projects/…/Roadmap/`. |
| **Task Complete** | check-circle | Opens popup: toggle Complete / Incomplete. Queues with file path and cursor line. EAT-QUEUE validates subtasks (block-IDs preferred); marks [x] only if all subtasks done. |
| **Add Roadmap Item** | link | Modal: secondary path (default current file), primary roadmap path, section dropdown, insert type (section-end / after-task / sub-task). Queues for EAT-QUEUE to append. |
| **Clear queue** | trash-2 | Clears the prompt queue (prompt-queue.jsonl). Optional archive to done file before clear. |

## In-note pending banner

After queuing an action, a temporary callout can appear on the **affected note** (or in [[3-Resources/Mobile-Pending-Actions]]): `> [!note] Pending: <mode> queued — run **PROCESS TASK QUEUE** or **EAT-QUEUE** to apply.` Watcher or a Cursor rule writes it; banner cleanup removes it after a successful process run (when success > failure). See [[3-Resources/Mobile-Pending-Actions#In-note pending banner (contract)|Mobile-Pending-Actions]] contract.

## One-tap Process Queue

Add a **persistent** "Process Queue" (or "EAT-QUEUE") icon to the mobile toolbar (e.g. gear or sync arrow) via **Commander** (recommended; see [[3-Resources/Commander-Plugin-Usage]]) or Advanced Toolbar. On tap, run the command that triggers processing (e.g. opens Cursor with "Process queue" or invokes local script). Implementation is plugin/settings; this describes the UX contract so the queue can be processed without leaving the note.

## EAT-QUEUE

- **Trigger**: In Cursor, say **EAT-QUEUE** or **PROCESS TASK QUEUE** (or use the one-tap toolbar icon above).
- **Queue file**: [[3-Resources/Task-Queue]] (one JSON-like line per entry).
- **Result**: Each entry is dispatched by `mode`; results are appended to Watcher-Result.md and Mobile-Pending-Actions.md.

## Merge strategies (future)

When **Merge Roadmaps** is added: **Append phases** (secondary phases after primary); **Interleave by priority** (frontmatter `priority: N` on phases). Documented here for reference.

## Progress report (future)

**Roadmap Progress** will use **callouts** for progress bars (e.g. `> [!progress] Phase 1: 3/5 ■■■□□`); fallback to plain text. Optional: Mermaid plugin for charts — see Obsidian Mermaid plugin.

## Toolbar overcrowding

Commander is installed; use it to place and group commands. With multiple roadmap commands, consider grouping under a **"Roadmap Tools"** sub-menu if Commander supports it (see [[3-Resources/Commander-Plugin-Usage]] for setup). **Prioritize Task Complete and Process Queue (EAT-QUEUE) on the main bar**; group TASK-ROADMAP, Add Roadmap Item, Expand Road, Reorder, Duplicate, Merge, Export, Progress under one "Roadmap Tools" icon. Power users: use command palette or mobile voice (e.g. Siri shortcut) to run "Process queue" or "Task Complete" to reduce toolbar reliance.
