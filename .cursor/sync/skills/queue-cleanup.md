---
name: queue-cleanup
description: Sweep queue entries that failed validation or dispatch; auto-mark as queue_failed true and append summary to Errors.md for review. Slot after dedup in auto-eat-queue. Trigger via auto_cleanup_after_process config or "Clear queue" / "Queue cleanup" command.
---

# queue-cleanup

## When to use

- **Slot**: After dedup (and before or after sort) in [.cursor/rules/context/auto-eat-queue.mdc](.cursor/rules/context/auto-eat-queue.mdc).
- **Trigger**: When `auto_cleanup_after_process: true` in [3-Resources/Second-Brain-Config](3-Resources/Second-Brain-Config.md), run after each EAT-QUEUE run. When false, run only when user invokes "Clear queue" or "Queue cleanup".

## Instructions

1. **Input**: Use the list of entries that failed validation or dispatch in the current run (or, when run standalone, read the queue file and identify entries with `queue_failed: true` or that were skipped).

2. **Auto-mark**: For each failed/skipped entry not already marked, set **`queue_failed: true`** on the object. When rewriting the queue file, ensure these entries are written back with the flag so the next EAT-QUEUE run skips them.

3. **Append to Errors.md**: Append a short summary to **`3-Resources/Errors.md`** (create if missing), e.g.:
   - Heading: `### YYYY-MM-DD HH:MM — Queue cleanup`
   - One line: "Queue cleanup: N failed entries marked; see queue file." Optionally list requestIds or modes.

4. **Append analytics to Feedback-Log.md**: Append a line or short block to **`3-Resources/Feedback-Log.md`** (create if missing on first write). Include: timestamp, source: queue-cleanup, failed_count (or similar), optional refinement/merge stats (e.g. "N entries merged; overlap detection"). Enables MOC aggregation and evolution monitoring. See [Logs](3-Resources/Second-Brain/Logs.md) and [Feedback-Log](3-Resources/Feedback-Log.md).

5. **Log**: Optionally append to Watcher-Result or a single line to Backup-Log that cleanup ran and how many entries were marked.

## MCP tools

- `obsidian_read_note` — read queue file if needed
- `obsidian_update_note` / `obsidian_search_replace` — rewrite queue file with queue_failed set; append to Errors.md

## Config

- **auto_cleanup_after_process**: Read from [3-Resources/Second-Brain-Config](3-Resources/Second-Brain-Config.md). When true, auto-eat-queue invokes this skill after clearing passed entries (step 8). When false, skill runs only on explicit "Clear queue" or "Queue cleanup" user command.

## Reference

- [3-Resources/Second-Brain/Queue-Sources](3-Resources/Second-Brain/Queue-Sources.md) — Queue-cleanup section
- [3-Resources/Cursor-Skill-Pipelines-Reference](3-Resources/Cursor-Skill-Pipelines-Reference.md) — Queue processor flow
