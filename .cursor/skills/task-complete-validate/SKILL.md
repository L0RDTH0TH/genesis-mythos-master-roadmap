---
name: task-complete-validate
description: Given filePath and task locator (block-id or lineIndex), reads note, locates task, detects subtasks (block-links ^id / depends on; fallback nested list). If desiredState is incomplete, unmarks without validation; if complete, marks [x] only when all subtasks complete. Use when EAT-QUEUE processes mode TASK-COMPLETE.
---

# task-complete-validate

## When to use

- When **auto-queue-processor** dispatches a queue entry with **mode: TASK-COMPLETE**.
- Payload: `filePath`, `taskLocator` (^block-id or lineIndex), `desiredState` ("complete" | "incomplete").

## Instructions

1. **Read note**: Use `obsidian_read_note`(filePath) to get full content.

2. **Locate task**: Find the task line by `taskLocator`: if it is a block-id (e.g. `^abc123`), find the line containing that id; if it is a lineIndex, use that line. If not found, log failure and append to Watcher-Result and Mobile-Pending-Actions; skip.

3. **If desiredState === "incomplete"**: Always unmark without validation. Use `obsidian_search_replace` to change `- [x]` to `- [ ]` on that line. Log success to Watcher-Result and Mobile-Pending-Actions. Done.

4. **If desiredState === "complete"**: **Validate subtasks** first:
   - **Preferred**: Use Tasks block-links: tasks that reference `depends on: ^<this-task-id>` or are nested under this task (same heading, indented list). Check each such subtask: if any is `- [ ]`, do **not** mark the parent; log "Task not completed: subtasks incomplete" and optionally list which ones; append to Watcher-Result and Mobile-Pending-Actions. If all subtasks are `- [x]`, proceed.
   - **Fallback**: Nested list under the task line until next same-level task or heading = subtasks. Same check: all must be [x] before marking parent.
   - If no subtasks found, treat as leaf task; allow mark.

5. **Mark complete**: Use `obsidian_search_replace` to change `- [ ]` to `- [x]` on the task line. Append success to Watcher-Result and Mobile-Pending-Actions.

## MCP tools

- `obsidian_read_note` — read note at filePath
- `obsidian_search_replace` — replace `- [ ]` with `- [x]` or vice versa on the target line

## Confidence gate

Deterministic (subtask check). No confidence band; log outcome (success or reason for skip) to Watcher-Result and Mobile-Pending-Actions.
