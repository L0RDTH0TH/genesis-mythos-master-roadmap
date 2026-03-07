---
description: "Process the task/roadmap queue (Task-Queue.md): read queue, dispatch by mode (TASK-ROADMAP, TASK-COMPLETE, ADD-ROADMAP-ITEM, EXPAND-ROAD, REORDER-ROADMAP, DUPLICATE-ROADMAP, MERGE-ROADMAPS, EXPORT-ROADMAP, PROGRESS-REPORT), run corresponding skill/handler, log to Watcher-Result, always update Mobile-Pending-Actions with post-process status."
globs: []
alwaysApply: false
---

# Auto queue processor (task/roadmap queue)

- **Queue**: Read **`3-Resources/Task-Queue.md`** (canonical task/roadmap queue). One JSON-like line per entry. Single entry point for all roadmap/task queue processing.
- **Reference**: See [3-Resources/Cursor-Skill-Pipelines-Reference](3-Resources/Cursor-Skill-Pipelines-Reference.md) and the Task-Roadmap Master Goal Migration plan. Roadmaps are manual-first; AI assists only.
- **MCP safety**: Obey [.cursor/rules/always/mcp-obsidian-integration.mdc](.cursor/rules/always/mcp-obsidian-integration.mdc) for backups, snapshots, and fallbacks.

## How to activate

Use any of these triggers (case-insensitive):

- **EAT-QUEUE** *(when intent is task/roadmap queue)*
- **PROCESS TASK QUEUE** *(canonical for this queue)*

When the instruction contains one of these, run the flow below. Read **Task-Queue.md**; if the file is missing or has no queue entries (no JSON lines in the body), treat as empty: optionally append to Watcher-Result and Mobile-Pending-Actions that nothing was processed; exit.

## Queue format

Each line in Task-Queue.md (below the frontmatter/content) is one JSON object: `{"mode": "TASK-ROADMAP", "filePath": "...", "requestId": "...", "timestamp": "..."}`. Modes: TASK-ROADMAP, TASK-COMPLETE, ADD-ROADMAP-ITEM, EXPAND-ROAD, REORDER-ROADMAP, DUPLICATE-ROADMAP, MERGE-ROADMAPS, EXPORT-ROADMAP, PROGRESS-REPORT.

## Flow

### 1. Read queue

- Read `3-Resources/Task-Queue.md`. Parse line-by-line; skip non-JSON lines (e.g. markdown headers). For each line, try to parse as JSON. Require `mode` (string). If no valid entries, exit and optionally log "Task queue empty".
- **Fast-path for single entry**: If **exactly one valid queue line**, skip any batch ordering and dispatch that entry immediately (go to step 2).

### 2. Dispatch by mode (switch on mode)

Per-mode logic is **folded into this rule** (implement as switch/cases). For each entry:

- **TASK-ROADMAP**: Run **roadmap-ingest** skill — read `filePath` from queue, parse roadmap, standardize (no heavy distillation unless `#needs-process`), place in `1-Projects/<Project>/Roadmap/`, link MOC; backup and per-change snapshot before writes. Append result to Watcher-Result. **Always** update Mobile-Pending-Actions.md with post-process status (e.g. "TASK-ROADMAP: Success" or "Failed: …").
- **TASK-COMPLETE**: Run **task-complete-validate** skill — locate task by block-id or line; if `desiredState === "incomplete"` unmark without validation; if `desiredState === "complete"` validate subtasks (block-links ^id / depends on); if all complete → search_replace [x]; else log reason. Append to Watcher-Result and Mobile-Pending-Actions.
- **ADD-ROADMAP-ITEM**: Parse primaryPath, secondaryPath, section, insertType; duplicate check; call obsidian_append_to_moc (or equivalent) with insertType; append_conf ≥85%; snapshot primary before append. Log and update Mobile-Pending-Actions.
- **EXPAND-ROAD**: Run **expand-road-assist** skill — user text or suggest breakdown; append under target; snapshot before write; propose-only if confidence <85%. **Post-step:** After success, if the primary roadmap note has frontmatter **phase_forks** (array) or expand-road-assist reported direction choices (e.g. phase_direction_choices), create a Phase Direction Wrapper under `Ingest/Decisions/Roadmap-Decisions/` using `Templates/Decision-Wrapper-Phase-Direction.md` (ensure structure via obsidian_ensure_structure; fill phase_path, direction_question, options A–G with **conceptual end-state** descriptions — one sentence per option, no tech terms — and store technical resolution in wrapper frontmatter for provenance; see Cursor-Skill-Pipelines-Reference § Phase-direction wrapper creation). Low-confidence (<68%): propose-only, do not write wrapper. Log and update Mobile-Pending-Actions.
- **REORDER-ROADMAP**: Run **reorder-roadmap-validate** — validate order, rewrite sections, dry-run option, snapshot. Log and update Mobile-Pending-Actions.
- **DUPLICATE-ROADMAP**: Copy note to new path; update frontmatter/links; optional duplicate-roadmap-customize; snapshot. Log and update Mobile-Pending-Actions.
- **MERGE-ROADMAPS**: Read both; merge per strategy; conflict proposal if low confidence; snapshot primary. Log and update Mobile-Pending-Actions.
- **EXPORT-ROADMAP**: Generate export; save to 5-Attachments/Exports/. Log and update Mobile-Pending-Actions.
- **PROGRESS-REPORT**: Compute completed/total per phase; append report note or callouts (progress bars, fallback text). Log and update Mobile-Pending-Actions.

Unknown mode → skip entry; append failure to Watcher-Result and Mobile-Pending-Actions.

### 3. Log and update

- Append **one line per processed entry** to `3-Resources/Watcher-Result.md`: `requestId: <id> | status: success|failure | message: "..." | trace: "..." | completed: <ISO8601>`.
- **Always** update `3-Resources/Mobile-Pending-Actions.md` with post-process status for each entry (e.g. "TASK-COMPLETE: Success" or "Failed: Subtasks pending"). Append a short line so mobile users see what was processed.

### 4. Banner cleanup (post-process)

- **Only if** success count **>** failure count for this run: for each **affected note** (from processed queue entries, e.g. `filePath` or `source_file`), use MCP **`obsidian_search_replace`** to **remove** pending callouts matching the standard pattern: `> [!note] Pending: … queued — run **PROCESS TASK QUEUE** or **EAT-QUEUE** to apply.` (or equivalent). This prevents clutter when users forget to process; when failures dominate, do **not** remove banners so users still see pending state on failed items.

### 5. Clear processed entries (optional)

- After successful processing, remove processed lines from Task-Queue.md or mark them (implementation choice). If keeping a simple append-only queue, document that processed entries remain and a separate "clear" step or manual edit can trim the file.

## Watcher-Result contract

When run was triggered by EAT-QUEUE or PROCESS TASK QUEUE for the task queue, append the one-line format per requestId. See [.cursor/rules/always/watcher-result-append.mdc](.cursor/rules/always/watcher-result-append.mdc).

## Exclusions

Do not touch Watcher-protected paths (Watcher-Signal.md, Watcher-Result.md, watched-file.md). Do not process queue entries whose filePath is under those or Backups/.
