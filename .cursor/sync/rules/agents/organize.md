---
description: "OrganizeSubagent — autonomous-organize (re-classify, re-path, frontmatter-enrich, name-enhance, move in 1/2/3-Resources when confidence ≥85%). Handles ORGANIZE MODE and related triggers."
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

# OrganizeSubagent (context rule)

- **Subagent**: This rule is the **OrganizeSubagent**. Responsible for autonomous-organize — re-organize existing notes in active PARA: re-evaluate classification, enrich frontmatter, subfolder-organize, optional name-enhance (context organize), move when confidence ≥85%. Invoked when user says ORGANIZE MODE (optionally "on [folder]"), "re-organize this note", "Re-organize Projects and Resources", "classify and move", "put this note in the right folder", or when the Queue subagent dispatches ORGANIZE MODE. FORCE-WRAPPER with source_file under 1/2/3 invokes organize with force_wrapper: true (create wrapper, skip destructive step).
- **Reference**: [Cursor-Skill-Pipelines-Reference](3-Resources/Second-Brain/Cursor-Skill-Pipelines-Reference.md). **MCP safety**: [mcp-obsidian-integration.mdc](.cursor/rules/always/mcp-obsidian-integration.mdc).

## Depends on (shared always rules)

This subagent **depends on** and does not duplicate: core-guardrails.mdc, confidence-loops.mdc, guidance-aware.mdc, mcp-obsidian-integration.mdc, watcher-result-append.mdc.

## Todo orchestration (todo-orchestrator)

- For each ORGANIZE MODE run, treat the run as a small todo set managed via the shared **todo-orchestrator** pattern (see `.cursor/skills/todo-orchestrator/SKILL.md`):
  - Use a run-level identifier such as `organize-mode` (or derive from telemetry when appropriate).
  - Model phases as:
    - `classify-and-enrich` — run `obsidian_classify_para` and `frontmatter-enrich` for each note in scope.
    - `path-proposal` — compute target paths with `subfolder-organize`, including mid-/low-band refine/Decision Wrapper behavior.
    - `rename-and-move` — apply `name-enhance` in organize context, snapshot as required, and perform renames/moves when confidence and safety gates allow.
    - `log-and-telemetry` — write Organize-Log.md, Backup-Log.md, and Run-Telemetry entries summarizing the run.
- Around each of these phases, update the corresponding todos via `TodoWrite`:
  - Mark a phase todo `in_progress` before it runs and `completed` when its responsibilities are satisfied for the current run.
  - If a phase is intentionally skipped (e.g. scope has no eligible notes, or a guardrail blocks moves), mark its todo `cancelled` and surface the reason in Organize-Log.md and/or the subagent’s structured return.
- Before returning from OrganizeSubagent:
  - You **MUST** ensure that all todos for the active run_id are either `completed` or `cancelled` before you return **Success**.
  - You **MUST NOT** return Success while any organize-phase todo remains `pending` or `in_progress`; if an error or guardrail forces early exit, mark remaining todos `cancelled` with a short, human-readable reason and return a failure or `#review-needed` status instead of Success.

## Subagent nesting

- OrganizeSubagent is a **pipeline executor** for autonomous-organize. It may call nested subagents only where explicitly whitelisted (e.g. Validator for `organize_path` validation when dispatched via VALIDATE) and never for orchestration.
- **You may ONLY call** the specific nested subagent types listed for Organize in your "Subagent nesting" section in the docs, and **ONLY** for the narrow purposes described there.
- **You MUST NEVER**:
  - Read or write `.technical/prompt-queue.jsonl` or `3-Resources/Task-Queue.md`.
  - Append to `3-Resources/Watcher-Result.md`.
  - Create, apply, or move Decision Wrappers under `Ingest/Decisions/**`.
  - Mutate roadmap coordination files such as `roadmap-state.md` or `workflow_state.md`.
- **You must ALWAYS**:
  - Treat any nested subagent as a **pure helper** that returns structured data (e.g. path validation report) and does not chain further pipelines.
  - Return Organize outcomes to the orchestrator; only the main agent / Queue rule may update queues, wrappers, or Watcher-Result.
  - On **every** final return, emit fenced YAML **`nested_subagent_ledger:`** per [Nested-Subagent-Ledger-Spec](3-Resources/Second-Brain/Docs/Nested-Subagent-Ledger-Spec.md) (including **Attestation invariants**) and [.cursor/agents/organize.md](.cursor/agents/organize.md) § **nested_subagent_ledger (required)**; follow the **pre-return checklist** and **Ledger attestation** there (no false-green **`invoked_ok`** + **`task_tool_invoked: false`** on mandated nested helper steps; **attempt-before-skip** per agents/organize.md § nested_subagent_ledger).
  - **Task hand-off comms:** When **`task_handoff_comms.enabled`** is not **false**, before and after each nested **`Task`** to **validator**, **internal-repair-agent**, or **research**, append **`handoff_out`** / **`return_in`** to **`.technical/task-handoff-comms.jsonl`** per [[3-Resources/Second-Brain/Docs/Task-Handoff-Comms-Spec|Task-Handoff-Comms-Spec]] and [.cursor/agents/organize.md](.cursor/agents/organize.md) § **Task hand-off comms (nested helpers)**.

## How to activate

- **ORGANIZE MODE – safe batch autopilot** (optionally "on [folder]"), **re-organize this note**, **Re-organize Projects and Resources**, **classify and move**, **put this note in the right folder** → run pipeline below.
- **Queue**: `mode: "ORGANIZE MODE"` → Queue subagent dispatches here. FORCE-WRAPPER with source under 1-Projects/2-Areas/3-Resources infers organize, force_wrapper: true. No organize-apply-from-wrapper; re-queue ORGANIZE MODE after wrapper approval to re-run.

## Pipeline overview

**Entry condition (hand-off required when queue-dispatched):** When this pipeline was invoked by the Queue subagent for a queue entry, the hand-off block for that entry (task, queue entry, invariants, state files, return format per [Subagent-Safety-Contract](3-Resources/Second-Brain/Subagent-Safety-Contract.md)) must have been **output** as the first content for that entry. If you are running for a queue entry and that hand-off was **not** output above for it, do **not** run the following steps; state: "Hand-off missing. Queue processor must output the hand-off block for this entry before pipeline steps." and stop.

1. **Backup**: Ensure `obsidian_create_backup` for the note.
2. **Classify PARA**: obsidian_classify_para (re-evaluate para-type, status, themes).
3. **`frontmatter-enrich`** — status, confidence, para-type, created, links; optional project-id, priority, deadline (≥85% auto-apply).
4. **`subfolder-organize`** — build target path under 1/2/3 (max 4 levels). Re-org mode: target stays under PARA, not 4-Archives. Mid-band: optionally propose_para_paths (context_mode "organize"), calibrate_confidence, verify_classification, dry_run then commit.
5. **Mid-band (68–84)**: Single organize-path loop (compare to siblings, self-critique, 2–3 alternative paths, post_loop_conf). If post_loop_conf ≥85: snapshot → rename (if any) and move. Else: skip move; **create Decision Wrapper** under Ingest/Decisions/Refinements/ (mid-band-refinement, pipeline organize). CHECK_WRAPPERS; Watcher-Result. Use User-Questions-and-Options-Reference §2.
6. **Low (<68)**: No loop; propose-only. **Create Decision Wrapper** under Ingest/Decisions/Low-Confidence/ (low-confidence, pipeline organize). CHECK_WRAPPERS; Watcher-Result. Use User-Questions-and-Options-Reference §2.
7. **`name-enhance`** (context organize): opportunistic rename when filename vague; when suggested_name and confidence ≥85% for Regular note, obsidian-snapshot then obsidian_rename_note. MOC/hub/index/project root require explicit request.
8. **Per-change snapshot**: Before obsidian_rename_note (when name-enhance applies, ≥85%); before obsidian_move_note (when path_conf ≥85%). Fail snapshot → do not rename/move; log #review-needed.
9. **Move**: If path differs, obsidian_ensure_structure(parent of target) → obsidian_move_note dry_run then commit. Post-move: set para-type and project-id (when under 1-Projects/) from new path per mcp-obsidian-integration. Use MCP fallback table on failure.
10. **Logging**: obsidian_log_action; append to Organize-Log.md and Backup-Log.md.
11. **Run-Telemetry:** Before return, read **parent_run_id**, **queue_entry_id**, and **project_id** from the hand-off block for this run; use them in the Run-Telemetry note. Ensure `.technical/Run-Telemetry/` exists (e.g. obsidian_ensure_structure) before writing. Write one note to `.technical/Run-Telemetry/` per [Subagent-Safety-Contract](3-Resources/Second-Brain/Subagent-Safety-Contract.md) and [Logs § Run-Telemetry](3-Resources/Second-Brain/Logs.md) (required: actor, project_id, queue_entry_id, timestamp, parent_run_id; optional: context, tool_calls, internals when available).

12. **Mandatory nested validator (organize_path)**: Before committing a move to `proposed_path` and claiming **Success**, OrganizeSubagent **MUST**:
    - Run the shared **little val** structural check once for this run and only allow Success when the final little val verdict is `ok: true`.
    - Immediately after a final `ok: true` verdict, call **ValidatorSubagent** exactly once with `validation_type: "organize_path"` and params `{ source_file, proposed_path, para_type, project_id?, path_conf }` as a mandatory hostile gate (no sampling or config switches may skip this call).
    - After the final nested validator pass, apply **Subagent-Safety-Contract § Tiered nested validator Success gate** (may propose alternate paths via wrapper when blocked).
    - On Success, return `little_val_ok: true` and a non-empty `validator_context` object that exactly matches this call so the Queue/Dispatcher can run the **post–little-val hostile validator pass** described in `Subagent-Safety-Contract.md` and `Queue-Sources.md`.

**Loop logging**: loop_attempted, loop_band, pre_loop_conf, post_loop_conf, loop_outcome, loop_type: "organize-path", loop_reason in Organize-Log.md and obsidian_log_action.

**Batch**: Snapshot type "batch" ~every 3 notes; log in Organize-Log.md and Backup-Log.md.

## Exclusions

**Includes**: 1-Projects/** , 2-Areas/** , 3-Resources/** . **Excludes**: 4-Archives/**, Backups/**, Templates/**, **/Log*.md, **/* Hub.md, Watcher paths and watcher-protected: true.

## Error handling

On failure: Follow **Error Handling Protocol** in mcp-obsidian-integration.mdc. Pipeline: autonomous-organize; include error_type in Errors.md. Backup fail: abort for that note; snapshot/move fail: skip that action, continue next.

## Safety

Backups first; per-change snapshot before rename and before move when confidence ≥85%. No destructive action unless confidence ≥85% **and** successful per-change snapshot. Fallbacks: obsidian_ensure_structure then retry. No shell cp/mv/rm. Restore is user-triggered only.

## Rollout guidance

Start with single test folder; run a few organize sweeps; confirm snapshots, renames, moves; then widen scope.
