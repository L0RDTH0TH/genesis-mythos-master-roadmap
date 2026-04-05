---
name: add-roadmap-append
description: Reads secondary note for title/summary; optional duplicate check in section; appends one line to primary roadmap under chosen section (or after task / as sub-task per insertType). Use when EAT-QUEUE processes mode ADD-ROADMAP-ITEM.
---

# add-roadmap-append

## When to use

- When **auto-queue-processor** dispatches a queue entry with **mode: ADD-ROADMAP-ITEM**.
- Payload: `primaryPath`, `secondaryPath`, `section`, `insertType` ("section-end" | "after-task" | "sub-task"), optional `taskLocator`.

## Instructions

1. **Read secondary**: Use `obsidian_read_note`(secondaryPath) to get title (or first heading). Build line: `- [[Title]]` or `- [[Title]] — one-line summary` (single line).

2. **Duplicate check**: Read primary (or the section) and check if a line with the same `[[...]]` link already exists in that section. If duplicate, log and skip; append to Watcher-Result and Mobile-Pending-Actions; do not append again.

3. **Snapshot primary**: Before any append, create per-change snapshot of the **primary** note (obsidian-snapshot skill). **append_conf ≥85%** for write; if below, propose only and log.

4. **Append**:
   - **insertType === "section-end"**: Call `obsidian_append_to_moc`(moc_path: primaryPath, section: section, line: built line). Or use equivalent MCP that appends under a heading.
   - **insertType === "after-task"**: Locate the task line (taskLocator); insert the new line **after** that line in the note (may require read + search_replace or an MCP that supports "insert after line").
   - **insertType === "sub-task"**: Locate the task line; append as nested list item (indented) under that task (read + search_replace to insert under the task line).

5. **Batch limit**: Process one ADD-ROADMAP-ITEM per EAT-QUEUE run or cap (e.g. max 5) to avoid large appends. Document in skill if cap is applied.

6. **Log**: Append result to Watcher-Result and Mobile-Pending-Actions.

## MCP tools

- `obsidian_read_note` — read secondary and primary
- `obsidian_append_to_moc` — append line under section (moc_path, section, line)
- `obsidian_search_replace` / `obsidian_update_note` — for after-task or sub-task insertion if needed
- obsidian-snapshot skill — snapshot primary before append

## Confidence gate

**append_conf ≥85%**: Execute append. **<85%**: Propose line only; do not write. Snapshot primary before append; log and update Mobile-Pending-Actions.
