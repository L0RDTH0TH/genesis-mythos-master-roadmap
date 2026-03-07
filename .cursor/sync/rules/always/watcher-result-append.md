---
description: Watcher bridge — append run result to Watcher-Result.md for plugin completion detection
globs: "*"
alwaysApply: true
---

# Watcher-Result append (Cursor-side contract)

When the current run was **triggered by a Watcher request** (prompt contains a Watcher mode trigger such as INGEST MODE, DISTILL MODE, EXPRESS MODE, or ARCHIVE MODE, and/or the instruction originated from the last line in `3-Resources/Watcher-Signal.md` with a `requestId`), the agent must report completion so the Obsidian Watcher plugin can show a detailed popup.

**EAT-QUEUE / queue-based runs**: When the run was triggered by **EAT-QUEUE** or **Process queue** (or by pasted EAT-CACHE payload), the trigger is the queue (`3-Resources/prompt-queue.jsonl`) or the pasted payload, not Watcher-Signal. The agent must still append **one line per processed queue entry** to `3-Resources/Watcher-Result.md` in the same format (requestId, status, message, trace, completed). Each queue entry has an `id` field that serves as the requestId. See `.cursor/rules/context/auto-eat-queue.mdc` for the full queue processor flow.

## On run finish

**On run finish** (success or failure), append **one line** to `3-Resources/Watcher-Result.md`:

```
requestId: <id> | status: success|failure | message: "..." | trace: "..." | completed: <ISO8601>
```

- **requestId**: The same `requestId` from the Watcher signal line that triggered this run (read from the prompt or from the last line of `Watcher-Signal.md` if present).
- **status**: `success` or `failure`.
- **message**: Short human-readable summary; use quotes and escape internal double quotes as `\"`.
- **trace**: For failures, the **full error stack or log excerpt** (not a one-liner). For success, empty string or short note. Escape internal double quotes as `\"`.
- **completed**: ISO 8601 timestamp when the run finished (e.g. `2026-02-27T12:34:56.789Z`). Enables lag estimation: compare with the timestamp on the matching line in `Watcher-Signal.md` (triggered at) to compute end-to-end delay.

## Path and format

- **Path**: `3-Resources/Watcher-Result.md`. Create the file (and `3-Resources` folder) if missing; append the new line; do not overwrite existing content.
- The plugin parses by `requestId` and `status`; keep the format above so the parser stays in sync.

## When to infer Watcher-triggered

Treat the run as Watcher-triggered when the user instruction or system context includes:

- The exact or canonical mode phrases (e.g. "INGEST MODE – process captures", "DISTILL MODE – safe batch autopilot", "EXPRESS MODE – safe batch autopilot", "ARCHIVE MODE – safe batch autopilot"), or
- A reference to having been invoked from the Watcher plugin / signal file, or
- **EAT-QUEUE**, **Process queue**, or a pasted **EAT-CACHE** payload (queue-based run; append one line per processed queue entry, using each entry's `id` as requestId), or
- **Task/roadmap queue** runs: when the run was triggered by EAT-QUEUE or PROCESS TASK QUEUE for the task queue (Task-Queue.md), and processed any of TASK-ROADMAP, TASK-COMPLETE, ADD-ROADMAP-ITEM, EXPAND-ROAD, REORDER-ROADMAP, DUPLICATE-ROADMAP, MERGE-ROADMAPS, EXPORT-ROADMAP, PROGRESS-REPORT; append one line per processed entry to Watcher-Result.md.

If in doubt (e.g. user typed the phrase manually without the plugin), appending a result line is still safe; the plugin only reacts to the `requestId` it is polling for.
