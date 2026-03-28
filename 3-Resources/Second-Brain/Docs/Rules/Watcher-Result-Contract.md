# Watcher-Result Contract

**Version: 2026-03 – post-subagent migration**

Defines where and how agents append run results so the Obsidian Watcher plugin can detect completion. Path, line format, and when to append (Watcher-triggered, EAT-QUEUE, PROCESS TASK QUEUE, wrapper creation).

---

## Purpose

Single Docs reference for the Watcher-Result contract. Full behavior (inferring Watcher-triggered, queue vs task-queue, wrapper creation) is in the always rule; this file gives the contract at a glance and points to it.

---

## Path

- **File:** `3-Resources/Watcher-Result.md`
- Create the file (and `3-Resources` folder) if missing; **append** the new line; do not overwrite existing content.
- The plugin parses by `requestId` and `status`; keep the format below so the parser stays in sync.

---

## Line format

Append exactly one line per run or per processed entry in this form:

```
requestId: <id> | status: success|failure | message: "..." | trace: "..." | completed: <ISO8601>
```

| Field | Meaning |
|-------|---------|
| **requestId** | Same `requestId` from the Watcher signal that triggered the run, or the queue entry `id` for queue-based runs. Use a synthetic id (e.g. `wrapper-<timestamp>`) when no queue entry (e.g. wrapper creation). |
| **status** | `success` or `failure`. |
| **message** | Short human-readable summary; use quotes and escape internal double quotes as `\"`. |
| **trace** | For failures: full error stack or log excerpt (not a one-liner). For success: empty string or short note. Escape internal double quotes as `\"`. |
| **completed** | ISO 8601 timestamp when the run finished (e.g. `2026-02-27T12:34:56.789Z`). Enables lag estimation vs the trigger timestamp. |

---

## When to append

- **Watcher-triggered runs:** When the run was triggered by a Watcher request (mode phrases such as INGEST MODE, DISTILL MODE, EXPRESS MODE, ARCHIVE MODE, and/or instruction from the last line in `3-Resources/Watcher-Signal.md` with a `requestId`). Append one line on run finish.
- **EAT-QUEUE / Process queue / EAT-CACHE:** Append **one line per processed queue entry** to Watcher-Result; use each entry’s `id` as requestId. Queue and task-queue runs are laptop-originated.
- **PROCESS TASK QUEUE:** When the run processed the task queue (Task-Queue.md) and handled any of TASK-ROADMAP, TASK-COMPLETE, ADD-ROADMAP-ITEM, EXPAND-ROAD, REORDER-ROADMAP, DUPLICATE-ROADMAP, MERGE-ROADMAPS, EXPORT-ROADMAP, PROGRESS-REPORT; append one line per processed entry.
- **Wrapper creation:** Whenever any pipeline or the Error Handling Protocol **creates a Decision Wrapper** under `Ingest/Decisions/**`, append one line: `requestId: <id> | status: success | message: "created wrapper → Decisions/<subfolder>/<basename>" | trace: "" | completed: <ISO8601>`. Use the current queue entry’s `id` when queue-triggered; otherwise a synthetic id (e.g. `wrapper-<timestamp>`). Subfolder = relative path under Ingest/Decisions (e.g. Refinements, Low-Confidence, Errors, Ingest-Decisions).

If in doubt (e.g. user typed the phrase manually without the plugin), appending a result line is still safe; the plugin only reacts to the requestId it is polling for.

---

## References

- `.cursor/rules/always/watcher-result-append.mdc` — full behavior, “When to infer Watcher-triggered,” and path/format details.
- [User-Flows/EAT-QUEUE-Flow](../User-Flows/EAT-QUEUE-Flow.md) — queue run and one line per entry.
- [Pipelines/Queue-Pipeline](../Pipelines/Queue-Pipeline.md) — A.6 Log step.
