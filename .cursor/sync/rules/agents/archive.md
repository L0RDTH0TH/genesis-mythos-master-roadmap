---
description: "ArchiveSubagent — autonomous-archive (move completed/inactive notes to 4-Archives/ with summary preservation, resurface markers, ghost-folder sweep). Handles ARCHIVE MODE and related triggers."
globs:
  - "1-Projects/**/*.md"
  - "2-Areas/**/*.md"
  - "3-Resources/**/*.md"
  - "!4-Archives/**"
  - "!Backups/**"
  - "!Templates/**"
  - "!**/Log*.md"
  - "!**/* Hub.md"
alwaysApply: false
---

# ArchiveSubagent (context rule)

- **Subagent**: This rule is the **ArchiveSubagent**. Responsible for autonomous-archive — move completed/inactive notes to `4-Archives/` with summary preservation and resurface markers. Invoked when user says ARCHIVE MODE, "archive this note", "send to Archives", "move completed to 4-Archives", or when the Queue subagent dispatches ARCHIVE MODE.
- **Reference**: [Cursor-Skill-Pipelines-Reference](3-Resources/Second-Brain/Cursor-Skill-Pipelines-Reference.md). **MCP safety**: [mcp-obsidian-integration.mdc](.cursor/rules/always/mcp-obsidian-integration.mdc).

## Depends on (shared always rules)

This subagent **depends on** and does not duplicate: core-guardrails.mdc, confidence-loops.mdc, guidance-aware.mdc, mcp-obsidian-integration.mdc, watcher-result-append.mdc.

## Todo orchestration (todo-orchestrator)

- For each ARCHIVE MODE run, treat the run as a small todo set managed via the shared **todo-orchestrator** pattern (see `.cursor/skills/todo-orchestrator/SKILL.md`):
  - Use a run-level identifier such as `archive-mode` (or derive from telemetry when appropriate).
  - Model phases as:
    - `select-candidates` — identify notes in scope for autonomous-archive and confirm they are eligible for processing in this run.
    - `archive-check-phase` — classify PARA and status, run `archive-check`, and handle mid-/low-band loops (Decision Wrappers) as specified.
    - `snapshot-and-move` — perform required per-change snapshots, compute target paths via `subfolder-organize`, run `summary-preserve` and `resurface-candidate-mark`, and move notes into `4-Archives/`.
    - `ghost-folder-sweep` — call `archive-ghost-folder-sweep` after moves when the moved_notes_list is non-empty.
    - `log-and-telemetry` — write Archive-Log, Backup-Log, and Run-Telemetry entries for this run.
- Around each of these phases, update the corresponding todos via `TodoWrite`:
  - Mark a phase todo `in_progress` before its work begins and `completed` after its responsibilities are fully discharged (including the “no candidates” case).
  - When a phase is intentionally skipped or aborted (e.g. snapshot failure, confidence below thresholds), mark its todo `cancelled` and record the reason in Archive-Log.md and/or the subagent’s structured return.
- Before returning from ArchiveSubagent:
  - You **MUST** ensure that all todos for the active run_id are either `completed` or `cancelled` before you return **Success**.
  - You **MUST NOT** return Success while any archive-phase todo remains `pending` or `in_progress`; if a guardrail or error forces early exit, mark remaining todos `cancelled` with a short, human-readable reason and return a failure or `#review-needed` status instead of Success.

## Subagent nesting

- ArchiveSubagent is a **pipeline executor** for autonomous-archive. It may only use nested subagents where explicitly whitelisted (e.g. Validator for `archive_candidate` validation when a VALIDATE entry has already been dispatched by the queue).
- **You may ONLY call** the specific nested subagent types listed for Archive in your "Subagent nesting" section in the docs, and **ONLY** for the narrow purposes described there.
- **You MUST NEVER**:
  - Read or write `.technical/prompt-queue.jsonl` or `3-Resources/Task-Queue.md`.
  - Append to `3-Resources/Watcher-Result.md`.
  - Create, apply, or move Decision Wrappers under `Ingest/Decisions/**`.
  - Mutate roadmap coordination files such as `roadmap-state.md` or `workflow_state.md`.
- **You must ALWAYS**:
  - Treat any nested subagent you call as a **pure helper** that returns structured data (e.g. validation verdict) and does not orchestrate or chain pipelines.
  - Return Archive results to the orchestrator; all queue writes, wrapper creation, and watcher logging stay in the main agent / Queue rule.
  - On **every** final return, emit fenced YAML **`nested_subagent_ledger:`** per [Nested-Subagent-Ledger-Spec](3-Resources/Second-Brain/Docs/Nested-Subagent-Ledger-Spec.md) (including **Attestation invariants**) and [.cursor/agents/archive.md](.cursor/agents/archive.md) § **nested_subagent_ledger (required)**; follow the **pre-return checklist** and **Ledger attestation** there (no false-green **`invoked_ok`** + **`task_tool_invoked: false`** on mandated nested helper steps; **attempt-before-skip** per agents/archive.md § nested_subagent_ledger).
  - **Task hand-off comms:** When **`task_handoff_comms.enabled`** is not **false**, before and after each nested **`Task`** to **validator**, **internal-repair-agent**, or **research**, append **`handoff_out`** / **`return_in`** to **`.technical/task-handoff-comms.jsonl`** per [[3-Resources/Second-Brain/Docs/Task-Handoff-Comms-Spec|Task-Handoff-Comms-Spec]] and [.cursor/agents/archive.md](.cursor/agents/archive.md) § **Task hand-off comms (nested helpers)**.

## How to activate

- **ARCHIVE MODE – safe batch autopilot**, **archive this note**, **send to Archives**, **move completed to 4-Archives** → run pipeline below.
- **Queue**: `mode: "ARCHIVE MODE"` → Queue subagent dispatches here (optional scope/source_file). No archive-apply-from-wrapper; re-queue ARCHIVE MODE after wrapper approval to re-run.

## Pipeline overview

**Entry condition (hand-off required when queue-dispatched):** When this pipeline was invoked by the Queue subagent for a queue entry, the hand-off block for that entry (task, queue entry, invariants, state files, return format per [Subagent-Safety-Contract](3-Resources/Second-Brain/Subagent-Safety-Contract.md)) must have been **output** as the first content for that entry. If you are running for a queue entry and that hand-off was **not** output above for it, do **not** run the following steps; state: "Hand-off missing. Queue processor must output the hand-off block for this entry before pipeline steps." and stop.

1. **Backup**: Ensure `obsidian_create_backup` for the note.
2. **Classify PARA**: Confirm para-type and status.
3. **`archive-check`** — verify archive readiness (no open tasks, status complete, age threshold, subfolder checks). Primary signal: `archive_conf` (≥85% for move).
3b. **Mandatory nested validator (archive_candidate)**: After archive-check has produced `archive_conf` and archive moves/logging for this run are complete, ArchiveSubagent **MUST**:
    - Run the shared **little val** structural check once for this run and only allow Success when the final little val verdict is `ok: true`.
    - Immediately after a final `ok: true` verdict, call **ValidatorSubagent** exactly once with `validation_type: "archive_candidate"` and params `{ source_file, archive_conf, project_id? }` as a mandatory hostile gate (no sampling or config switches may skip this call).
    - **`severity: "high"`** or **`recommended_action: "block_destructive"`** → **hard block**: **MUST NOT** return Success; return **#review-needed** or **failure**. When **`validator.tiered_blocks_enabled`** is **true**, **`needs_work`** without high/block → **Success allowed** if little val ok (**Subagent-Safety-Contract § Tiered nested validator Success gate**).
    - On Success, return `little_val_ok: true` and a non-empty `validator_context` object that exactly matches this call so the Queue/Dispatcher can run the **post–little-val hostile validator pass** described in `Subagent-Safety-Contract.md` and `Queue-Sources.md`.
4. **Mid-band (68–84)**: Single archive-refine loop (re-scan tasks, optional TL;DR preview, self-critique, compute post_loop_conf). If post_loop_conf ≥85: snapshot → proceed. Else: skip move; **create Decision Wrapper** under Ingest/Decisions/Refinements/ (mid-band-refinement, pipeline archive). CHECK_WRAPPERS; Watcher-Result. Use User-Questions-and-Options-Reference §2.
5. **Low (<68)**: No loop; archive candidate only. **Create Decision Wrapper** under Ingest/Decisions/Low-Confidence/ (low-confidence, pipeline archive). CHECK_WRAPPERS; Watcher-Result. Use User-Questions-and-Options-Reference §2.
6. **Per-change snapshot**: After archive-check ≥85%, **before** subfolder-organize, summary-preserve, move — call obsidian-snapshot type "per-change". Below threshold or snapshot fail: do not move; log #review-needed.
7. **`subfolder-organize`** — compute target path under 4-Archives/ (≥85%). Optionally propose_para_paths (context_mode organize/archive) for advisory candidates.
8. **`resurface-candidate-mark`** — mark high-potential notes (≥85% for hub append; metadata-only ≥75%).
9. **`summary-preserve`** — minimal TL;DR/summary callout, project color links (≥85%).
10. **Move**: obsidian_ensure_structure(parent of target) → obsidian_move_note dry_run then commit. Post-move: set para-type Archive, **status: archived** on note at new path per mcp-obsidian-integration. On failure use MCP fallback table.
11. **Logging**: obsidian_log_action; append to Archive-Log.md and Backup-Log.md.
11b. **Run-Telemetry:** Before return, read **parent_run_id**, **queue_entry_id**, and **project_id** from the hand-off block for this run; use them in the Run-Telemetry note. Ensure `.technical/Run-Telemetry/` exists (e.g. obsidian_ensure_structure) before writing. Write one note to `.technical/Run-Telemetry/` per [Subagent-Safety-Contract](3-Resources/Second-Brain/Subagent-Safety-Contract.md) and [Logs § Run-Telemetry](3-Resources/Second-Brain/Logs.md) (required: actor, project_id, queue_entry_id, timestamp, parent_run_id; optional: context, tool_calls, internals when available).
12. **Ghost-folder sweep**: After all moves, if moved_notes_list non-empty, invoke **archive-ghost-folder-sweep** with that list (obsidian_remove_empty_folder; no shell rmdir). Log #ghost-sweep in Archive-Log.

**Loop logging**: loop_attempted, loop_band, pre_loop_conf, post_loop_conf, loop_outcome, loop_type: "archive-refine", loop_reason in Archive-Log.md and obsidian_log_action.

**Batch**: One batch snapshot per sweep; log in Archive-Log.md and Backup-Log.md.

## Exclusions

**Includes**: 1-Projects/** , 2-Areas/** , 3-Resources/** . **Excludes**: 4-Archives/**, Backups/**, Templates/**, **/Log*.md, **/* Hub.md, Watcher paths and watcher-protected: true.

## Error handling

On failure: Follow **Error Handling Protocol** in mcp-obsidian-integration.mdc. Pipeline: autonomous-archive; include error_type in Errors.md. Log to Errors.md, reference in Archive-Log.md and Backup-Log.md. Backup/snapshot fail: abort for that note, continue next.

## Safety

Backups first; per-change snapshot mandatory before move when archive_conf ≥85%. No destructive action unless confidence ≥85% **and** successful per-change snapshot. Fallbacks: obsidian_ensure_structure then retry move; else log and propose manual parent. No shell cp/mv/rm. Restore is user-triggered only.

## Rollout guidance

Start with single test project folder; run 3–5 archive sweeps; confirm only complete/inactive notes moved, snapshots created; then widen scope.
