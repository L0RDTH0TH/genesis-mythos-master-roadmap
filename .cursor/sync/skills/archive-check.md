---
name: archive-check
description: Evaluates whether a note is a candidate for archiving (no open tasks, status complete, age past threshold) and cross-checks project subfolders. Use after classify_para in the autonomous-archive pipeline.
---

# archive-check

## When to use

- After **obsidian_classify_para** in the autonomous-archive pipeline.
- Only when confidence is **≥85%** to recommend move; otherwise flag for review or skip move.

## Instructions

1. **Read note**: Use `obsidian_read_note` to get frontmatter (`status`, `para-type`, dates, tasks) and body (open checklists, `- [ ]`).

2. **Heuristic**:
   - No open tasks (all `- [x]` or no task list).
   - `status: complete` (or equivalent).
   - Age beyond threshold: read from [Second-Brain-Config.md](3-Resources/Second-Brain-Config.md) (archive.age_days / no_activity_days) if available; else default 90 / 60 days (no activity or last-modified older than configured days).
   - Cross-check: use `obsidian_list_notes` or `obsidian_global_search` for linked notes in the same project subfolder; if they are still active, consider delaying archive or note the relation.

3. **Output**: Set an internal recommendation (archive / do not archive) and, if archiving, pass the result to **subfolder-organize** for archive path. Do not move here; move is done by the pipeline after subfolder-organize, resurface-candidate-mark, summary-preserve.

4. **If anomalies are detected** (e.g. open tasks but `status: complete`, conflicting dates, or linked notes still active in the same project):
   - Recommend **not archiving** automatically.
   - Flag the note for review and suggest consulting recent snapshots for context:
     - Use `Restore Hub.md` to inspect per-change snapshots for this note (and related notes) before deciding whether to archive, revise, or keep active.

## MCP tools

- `obsidian_read_note` — read note and frontmatter
- `obsidian_list_notes` — list folder for project subfolder context
- `obsidian_global_search` — find linked notes if needed

## Confidence gate

**≥85%**: Recommend move to archive and proceed in pipeline. **<85%**: Do not move; flag for review or skip.
