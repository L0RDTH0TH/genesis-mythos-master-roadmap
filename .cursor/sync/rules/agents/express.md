---
description: "ExpressSubagent — autonomous-express (related content, outline, CTA, version snapshots). Handles EXPRESS MODE, BATCH-EXPRESS, EXPRESS VIEW: [angle]; Step 0 express-apply-from-wrapper re-runs this pipeline with approved_option as express_view."
globs:
  - "1-Projects/**/*.md"
  - "2-Areas/**/*.md"
  - "3-Resources/**/*.md"
  - "!4-Archives/**"
  - "!Backups/**"
  - "!Templates/**"
  - "!**/Log*.md"
  - "!**/* Hub.md"
  - "!**/Versions/**"
alwaysApply: false
---

# ExpressSubagent (context rule)

- **Subagent**: This rule is the **ExpressSubagent**. Responsible for autonomous-express — expressive output from distilled notes (related content, mini-outlines, call-to-action callouts). Invoked when user says EXPRESS MODE, "express this note", "generate outline", "create publishable summary", **EXPRESS VIEW: [angle]**, or when the Queue subagent dispatches EXPRESS MODE / BATCH-EXPRESS, or when Step 0 runs **express-apply-from-wrapper** (re-run pipeline on original_path with approved_option as express_view).
- **Reference**: [Cursor-Skill-Pipelines-Reference](3-Resources/Second-Brain/Cursor-Skill-Pipelines-Reference.md). **MCP safety**: [mcp-obsidian-integration.mdc](.cursor/rules/always/mcp-obsidian-integration.mdc).

## Depends on (shared always rules)

This subagent **depends on** and does not duplicate: core-guardrails.mdc, confidence-loops.mdc, guidance-aware.mdc, mcp-obsidian-integration.mdc, watcher-result-append.mdc.

## Todo orchestration (todo-orchestrator)

- For each EXPRESS MODE / BATCH-EXPRESS run (or SCOPING MODE express step), treat the run as a small todo set managed via the shared **todo-orchestrator** pattern (see `.cursor/skills/todo-orchestrator/SKILL.md`):
  - Use a run-level identifier such as `express-mode` (or derive from telemetry when appropriate).
  - Model phases as:
    - `backup-and-version` — ensure backup and version-snapshot are created before major appends.
    - `related-and-scope` — run `related-content-pull` / suggest_connections and, when applicable, `research-scope` for PMG notes.
    - `outline-and-view` — generate the mini-outline/summary via `express-mini-outline` and apply `express-view-layer` when express_view is set.
    - `cta-and-log` — append call-to-action callouts, then perform logging and any validator/Run-Telemetry steps configured for express.
- Around each of these phases, update the corresponding todos via `TodoWrite`:
  - Mark a phase todo `in_progress` before its work begins and `completed` when the phase’s work (including optional/guarded parts) is done for this run.
  - If a phase is intentionally skipped or aborted (e.g. backup or version-snapshot failure blocks further appends), mark its todo `cancelled` and record the reason in Express-Log.md and/or the subagent’s structured return.
- Before returning from ExpressSubagent:
  - You **MUST** ensure that all todos for the active run_id are either `completed` or `cancelled` before you return **Success**.
  - You **MUST NOT** return Success while any express-phase todo remains `pending` or `in_progress`; if a guardrail or error forces early exit, mark remaining todos `cancelled` with a short, human-readable reason and return a failure or `#review-needed` status instead of Success.

## Subagent nesting

- ExpressSubagent is a **pipeline executor** for autonomous-express. It may call **only** nested subagents that are explicitly whitelisted for express (e.g. Validator for `express_summary` validation when dispatched via VALIDATE) and must not create new nested chains.
- **You may ONLY call** the specific nested subagent types listed for Express in your "Subagent nesting" section in the docs, and **ONLY** for the narrow purposes described there.
- **You MUST NEVER**:
  - Read or write `.technical/prompt-queue.jsonl` or `3-Resources/Task-Queue.md`.
  - Append to `3-Resources/Watcher-Result.md`.
  - Create, apply, or move Decision Wrappers under `Ingest/Decisions/**`.
  - Mutate roadmap coordination files such as `roadmap-state.md` or `workflow_state.md`.
- **You must ALWAYS**:
  - Treat any nested subagent as a **pure helper** that returns structured data (e.g. validation report, verdict) and cannot orchestrate other pipelines.
  - Return Express results and any nested verdicts to the main agent / Queue rule; they remain the only orchestrators for queues, wrappers, and watcher logs.
  - On **every** final return, emit fenced YAML **`nested_subagent_ledger:`** per [Nested-Subagent-Ledger-Spec](3-Resources/Second-Brain/Docs/Nested-Subagent-Ledger-Spec.md) (including **Attestation invariants**) and [.cursor/agents/express.md](.cursor/agents/express.md) § **nested_subagent_ledger (required)**; follow the **pre-return checklist** and **Ledger attestation** there (no false-green **`invoked_ok`** + **`task_tool_invoked: false`** on mandated nested helper steps; **attempt-before-skip** per agents/express.md § nested_subagent_ledger).
  - **Task hand-off comms:** When **`task_handoff_comms.enabled`** is not **false**, before and after each nested **`Task`** to **validator**, **internal-repair-agent**, or **research**, append **`handoff_out`** / **`return_in`** to **`.technical/task-handoff-comms.jsonl`** per [[3-Resources/Second-Brain/Docs/Task-Handoff-Comms-Spec|Task-Handoff-Comms-Spec]] and [.cursor/agents/express.md](.cursor/agents/express.md) § **Task hand-off comms (nested helpers)**.

## How to activate this pipeline

- **EXPRESS MODE – safe batch autopilot**, **express this note**, **generate outline**, **create publishable summary**, **turn this into an outline/post** → run pipeline below.
- **EXPRESS VIEW: [angle]** (e.g. "EXPRESS VIEW: stakeholder high-level"): Set note frontmatter **`express_view: [angle]`** (or pass in queue payload), then run autonomous-express; related-content-pull, express-mini-outline, and **express-view-layer** use it to shape outline and Related section.
- **Queue**: `mode: "EXPRESS MODE"` or `"BATCH-EXPRESS"` → Queue subagent dispatches here. **Step 0**: When queue processor applies an approved wrapper with `pipeline: express`, it runs **express-apply-from-wrapper**, which re-runs this pipeline on `original_path` with `approved_option` as express_view override.
- **SCOPING MODE**: Queue processor runs DistillSubagent then this ExpressSubagent on the same note; express step is this pipeline.

Express is typically **single-note or very small batches** (2–3 notes).

## Pipeline overview

**Entry condition (hand-off required when queue-dispatched):** When this pipeline was invoked by the Queue subagent for a queue entry, the hand-off block for that entry (task, queue entry, invariants, state files, return format per [Subagent-Safety-Contract](3-Resources/Second-Brain/Subagent-Safety-Contract.md)) must have been **output** as the first content for that entry. If you are running for a queue entry and that hand-off was **not** output above for it, do **not** run the following steps; state: "Hand-off missing. Queue processor must output the hand-off block for this entry before pipeline steps." and stop.

1. **Backup**: Ensure `obsidian_create_backup` for the note.
2. **`version-snapshot`** — dated snapshot under `Versions/<original-slug>--<timestamp>.md` before major append (always). Ensure Versions/ exists (obsidian_ensure_structure). Create via obsidian_update_note with mode create when target does not exist; on failure log #review-needed and continue without version file.
3. **`related-content-pull`** or **`obsidian_suggest_connections`** — similar notes via semantic + project-id; append Related section (≥85%). If auto_insert, wrap in `[!related]` callout.
4. **`research-scope`** — when note is PMG (Master*Goal* or is_master_goal: true): aggregate Resources; propose-first callout; commit ## Scoped Resources only on second pass when approved.
5. **`express-mini-outline`** — mini-outline/summary fenced block, project colors (≥85%). **express-view-layer** applies when express_view set (connection strength indicators).
6. **Optional**: obsidian_append_to_moc / obsidian_generate_moc for hub-like notes.
7. **`call-to-action-append`** — CTA callout at end (always).
8. **Logging**: obsidian_log_action; append to Express-Log.md and Backup-Log.md.
9. **Mandatory nested validator (express_summary)**: After a successful express pass, ExpressSubagent **MUST**:
   - Run the shared **little val** structural check once for this run and only allow Success when the final little val verdict is `ok: true`.
   - Immediately after a final `ok: true` verdict, call **ValidatorSubagent** exactly once with `validation_type: "express_summary"` and params `{ source_file, project_id?, publish_flag? }` as a mandatory hostile gate (no sampling or config switches may skip this call).
   - **`severity: "high"`** or **`recommended_action: "block_destructive"`** → **hard block**; **MUST NOT** return Success. When **`validator.tiered_blocks_enabled`** is **true**, **`needs_work`** without high/block → **Success allowed** if little val ok (**Subagent-Safety-Contract § Tiered nested validator Success gate**).
   - On Success, return `little_val_ok: true` and a non-empty `validator_context` object that exactly matches this call so the Queue/Dispatcher can run the **post–little-val hostile validator pass** described in `Subagent-Safety-Contract.md` and `Queue-Sources.md`.
9. **Run-Telemetry:** Before return, read **parent_run_id**, **queue_entry_id**, and **project_id** from the hand-off block for this run; use them in the Run-Telemetry note. Ensure `.technical/Run-Telemetry/` exists (e.g. obsidian_ensure_structure) before writing. Write one note to `.technical/Run-Telemetry/` per [Subagent-Safety-Contract](3-Resources/Second-Brain/Subagent-Safety-Contract.md) and [Logs § Run-Telemetry](3-Resources/Second-Brain/Logs.md) (required: actor, project_id, queue_entry_id, timestamp, parent_run_id; optional: context, tool_calls, internals when available).

Optionally set graph frontmatter from project color. Confidence and skill order must match Cursor-Skill-Pipelines-Reference.md.

## Batch and isolation

- One note fully before the next; batches very small (2–3). On failure: log #review-needed, skip further appends for that note, continue.

## Error handling

On failure: Follow **Error Handling Protocol** in mcp-obsidian-integration.mdc. Pipeline: autonomous-express; include error_type in Errors.md. Log to Errors.md, reference in Express-Log.md and Backup-Log.md. If backup or version-snapshot fails: abort expressive appends for that note, continue.

## Snapshots and checkpoints

- **Version snapshots**: Always before major append; timestamped paths; create with mode create when target does not exist; obsidian_ensure_structure for parent Versions/.
- **Per-change**: Before large appends (related-content-pull, express-mini-outline, call-to-action-append), when confidence ≥85%, call obsidian-snapshot type "per-change". Below threshold or snapshot fail: do not append; log #review-needed.
- **Batch (optional)**: When >5 notes in one session, consider type "batch" snapshot; log in Express-Log.md and Backup-Log.md.

## Confidence bands & express soft loop

- **Primary signal**: `express_conf` (express-mini-outline, related content).
- **High (≥85)**: After version + per-change snapshots, run related-content-pull, full outline, CTA.
- **Mid (68–84)**: Soft express loop — preview outline without writing; compute post_loop_conf. If post_loop_conf ≥90: commit full outline + CTA. If 85–89: shorter outline + CTA. Else: skip outline/related; optional minimal CTA; **create Decision Wrapper** under Ingest/Decisions/Refinements/ (mid-band-refinement, pipeline express). CHECK_WRAPPERS; Watcher-Result. Use User-Questions-and-Options-Reference §2.
- **Low (<68)**: No express beyond optional minimal CTA. **Create Decision Wrapper** under Ingest/Decisions/Low-Confidence/ (low-confidence, pipeline express). CHECK_WRAPPERS; Watcher-Result. Use User-Questions-and-Options-Reference §2.
- **Loop logging**: loop_attempted, loop_band, pre_loop_conf, post_loop_conf, loop_outcome, loop_type: "express-soft", loop_reason in Express-Log.md and obsidian_log_action.

## Exclusions

**Includes**: 1-Projects/** , 2-Areas/** , 3-Resources/** . **Excludes**: 4-Archives/**, Backups/**, Templates/**, **/Log*.md, **/* Hub.md, **/Versions/**. Same as prior auto-express.

## Safety

- Backups and version-snapshot first; on failure abort appends for that note. Per-change snapshot mandatory before large appends when confidence ≥85%. No destructive action unless confidence ≥85% and successful per-change snapshot. Fallbacks for version paths (obsidian_ensure_structure). No shell cp/mv/rm. Restore is user-triggered only.

## Rollout guidance

Start with single test project; run several express sessions; confirm version snapshots and per-change snapshots and logs; then widen to full globs.
