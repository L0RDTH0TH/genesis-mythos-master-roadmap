---
name: task-reroute
description: After next-action-extract, when note is task-like and confidence ≥78%, find or derive parent (Area/Project), then create a dedicated task note or append extracted tasks to an existing note. Use find_parent, obsidian_create_task_note, append_tasks. Snapshot target before append.
---

# task-reroute

## When to use

- **After next-action-extract** in the full-autonomous-ingest pipeline.
- Only when **next-action-extract confidence ≥78%** and the note is **task-like** (see trigger score below).
- Conditional: run only when task-like heuristics or classify_para (balancer) indicate tasks under an Area/Project; skip for non-task notes to avoid extra reads.

## Instructions

1. **Read note and frontmatter**: Use `obsidian_read_note` to get content and frontmatter: `next-actions` (or parsed checklists), `project-id`, `para-type`, and if available from classify_para: `tasks_extracted`, `suggested_parent`.

2. **Compute task-like score** (trigger):
   - **Base**: classify_para was run with `mode: "balancer"` and (tasks_extracted > 0 or suggested_parent exists): **+50**.
   - **Heuristics**: Multiple next-actions (>2): **+20**; para-type keywords (e.g. "Tasks", "Actions"): **+20**; deadlines/dates in content: **+10**.
   - **Trigger**: Run task-reroute only if **total ≥ 70** and **confidence ≥ 78%**. Otherwise skip and continue pipeline.

3. **Determine parent**:
   - If **suggested_parent** from classify_para exists and is a valid path (e.g. `2-Areas/Software Tools` or `1-Projects/MyProject`), use it as candidate parent.
   - Else if **project-id** in frontmatter: parent = `1-Projects/<ProjectName>` (slug from project-id); ensure folder exists via `obsidian_ensure_structure` if creating new task note.
   - Else: call **find_parent**(area_name, keywords) with area name and keywords derived from note title/content. If **find_parent** returns **no candidates or only low-score candidates**: **log and skip reroute** (do not create under ambiguous parent). Optionally default to vault-convention `Inbox/Tasks.md` if documented; otherwise skip.

4. **Create vs. append**:
   - If **parent note does not exist or is empty**: use **obsidian_create_task_note**(parent_path, title, content) with a sensible title (e.g. from note title or "Tasks") and content = note summary or list of tasks as markdown.
   - Else: use **append_tasks**(parent_path, tasks) where `tasks` is a JSON array of task strings (e.g. `["- [ ] Action one", "- [ ] Action two"]`) from the note's next-actions or extracted checklists.
   - Use **find_parent** score when available: high score (>90%) → prefer append to that parent; lower score → prefer creating a **new** task note under the parent folder.

5. **Backup and snapshot**: **append_tasks** requires backup before append (per MCP). Ingest already runs create_backup at pipeline start. Before **append_tasks** (and optionally before create_task_note if overwriting): create a **per-change snapshot of the target note** (the parent being appended to) via the obsidian-snapshot skill — not the source note. If backup for target fails, **abort** and notify via `obsidian_log_action` (e.g. "Backup failed for parent_path; skipping append"); do not append without backup.

6. **Optional source frontmatter**: After rerouting, optionally clear or archive the source note's `next-actions` frontmatter (e.g. move to `archived-actions` or a dedicated key) to avoid duplication, **unless** the note is intended to remain a standalone task hub. Document as optional; apply only when confident.

7. **Log**: Log task-reroute outcome in Ingest-Log (parent path, created vs appended, task count). Track **metrics** for tuning: reroute frequency, average confidence, task count per reroute (e.g. if ≥78% yields too many false positives, consider ≥82%).

## MCP tools

- `obsidian_read_note` — read source note and frontmatter
- `find_parent` — candidate parent path(s) with score (area_name, keywords)
- `obsidian_create_task_note` — create task note under parent_path (title, content)
- `append_tasks` — append tasks array to note at parent_path (requires backup before append)
- `obsidian_ensure_structure` — ensure parent folder exists when creating new task note
- `obsidian_manage_frontmatter` — optional: clear/archive source next-actions
- obsidian-snapshot skill — per-change snapshot of **target** note before append_tasks
- `obsidian_log_action` — log outcome and backup/snapshot paths

## Confidence gate

**≥78%** and **task-like score ≥ 70**: Execute reroute (create or append). **<78%** or score < 70: Skip; do not call find_parent or append/create. Log skip reason in Ingest-Log.

## Error handling and fallbacks

- **find_parent** returns no candidates or only low-score candidates: **log and skip reroute**; do not create under ambiguous parent. Optionally default to `Inbox/Tasks.md` if vault convention exists.
- **append_tasks**: If backup for target note fails, **abort** and notify via `obsidian_log_action`; do not append.
- On any failure: log to Ingest-Log with `#review-needed` if severity high; continue pipeline for next note (do not halt batch).

## Pipeline order

… → next-action-extract → **task-reroute** (when conditions above) → manage_frontmatter / manage_tags → append_to_hub → move_note → log_action.
