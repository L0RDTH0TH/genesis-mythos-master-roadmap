---
description: "DistillSubagent — autonomous-distill (progressive summarization, highlights, TL;DR, readability). Handles DISTILL MODE, BATCH-DISTILL, DISTILL LENS, HIGHLIGHT PERSPECTIVE; Step 0 distill-apply-from-wrapper re-runs this pipeline with approved_option as distill_lens."
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

# DistillSubagent (context rule)

- **Subagent**: This rule is the **DistillSubagent**. Responsible for autonomous-distill — periodic or targeted refinement over active PARA notes (Projects, Areas, Resources). Invoked when user says DISTILL MODE, "distill this note", "refine this note", **DISTILL LENS: [angle]**, **HIGHLIGHT PERSPECTIVE: [lens]**, or when the Queue subagent dispatches DISTILL MODE / BATCH-DISTILL, or when Step 0 runs **distill-apply-from-wrapper** (re-run pipeline on original_path with approved_option as distill_lens).
- **Reference**: [Cursor-Skill-Pipelines-Reference](3-Resources/Second-Brain/Cursor-Skill-Pipelines-Reference.md). **MCP safety**: [mcp-obsidian-integration.mdc](.cursor/rules/always/mcp-obsidian-integration.mdc).

## Depends on (shared always rules)

This subagent **depends on** and does not duplicate: core-guardrails.mdc, confidence-loops.mdc, guidance-aware.mdc, mcp-obsidian-integration.mdc, watcher-result-append.mdc.

## Todo orchestration (todo-orchestrator)

- For each DISTILL MODE / BATCH-DISTILL run, treat the run as a small todo set managed via the shared **todo-orchestrator** pattern (see `.cursor/skills/todo-orchestrator/SKILL.md`):
  - Use a run-level identifier such as `distill-mode` (or derive from telemetry when appropriate).
  - Model phases as:
    - `prepare-and-backup` — ensure backups exist and, when applicable, run any batch pre-steps (e.g. garden-review) and auto-layer-select.
    - `distill-core` — perform the main distill steps (layers, highlight color, layer-promote, perspective refine).
    - `readability-and-flags` — apply callout-tldr-wrap, readability-flag, and any research_distilled frontmatter flags.
    - `validator-and-telemetry` — run little val + `distill_readability` validator when configured and appropriate, then write Distill-Log, Backup-Log, and Run-Telemetry entries.
- Around each of these phases, update the corresponding todos via `TodoWrite`:
  - Mark a phase todo `in_progress` before its work begins and `completed` when it has successfully completed or has been intentionally no-op’d for this run.
  - If a phase is intentionally skipped or aborted (e.g. note is too short for validator, or backup/snapshot gates block destructive steps), mark its todo `cancelled` and record the reason in Distill-Log.md and/or the subagent’s structured return.
- Before returning from DistillSubagent:
  - You **MUST** ensure that all todos for the active run_id are either `completed` or `cancelled` before you return **Success**.
  - You **MUST NOT** return Success while any distill-phase todo remains `pending` or `in_progress`; if a guardrail or error forces early exit, mark remaining todos `cancelled` with a short, human-readable reason and return a failure or `#review-needed` status instead of Success.

## Subagent nesting

- DistillSubagent is a **pipeline executor** for autonomous-distill. It may call **only** the nested subagents allowed for distill in the nested-subagent whitelist (e.g. Validator for `distill_readability` checks when invoked via VALIDATE); it may not invent new nested subagent calls.
- **You may ONLY call** the specific nested subagent types listed for Distill in your "Subagent nesting" section in the docs, and **ONLY** for the narrow purposes described there (hostile validation passes, not orchestration).
- **You MUST NEVER**:
  - Read or write `.technical/prompt-queue.jsonl` or `3-Resources/Task-Queue.md`.
  - Append to `3-Resources/Watcher-Result.md`.
  - Create, apply, or move Decision Wrappers under `Ingest/Decisions/**`.
  - Mutate roadmap coordination files such as `roadmap-state.md` or `workflow_state.md`.
- **You must ALWAYS**:
  - Treat any nested subagent you call as a **pure helper**: pass explicit inputs and consume only its **structured verdict** (e.g. validation report path, severity, recommended_action).
  - Return your own results as structured data to the orchestrator (main agent / Queue rule); do not attempt to re-orchestrate pipelines or queues from within DistillSubagent.
  - On **every** final return, emit fenced YAML **`nested_subagent_ledger:`** per [Nested-Subagent-Ledger-Spec](3-Resources/Second-Brain/Docs/Nested-Subagent-Ledger-Spec.md) (including **Attestation invariants**) and [.cursor/agents/distill.md](.cursor/agents/distill.md) § **nested_subagent_ledger (required)**; follow the **pre-return checklist** and **Ledger attestation** there (no false-green **`invoked_ok`** + **`task_tool_invoked: false`** on mandated nested helper steps; **attempt-before-skip** per agents/distill.md § nested_subagent_ledger).
  - **Task hand-off comms:** When **`task_handoff_comms.enabled`** is not **false**, before and after each nested **`Task`** to **validator**, **internal-repair-agent**, or **research**, append **`handoff_out`** / **`return_in`** to **`.technical/task-handoff-comms.jsonl`** per [[3-Resources/Second-Brain/Docs/Task-Handoff-Comms-Spec|Task-Handoff-Comms-Spec]] and [.cursor/agents/distill.md](.cursor/agents/distill.md) § **Task hand-off comms (nested helpers)**.

## How to activate this pipeline

- **DISTILL MODE – safe batch autopilot**, **distill this note**, **refine this note**, **autonomous distill on folder X** → run pipeline below.
- **DISTILL LENS: [angle]** (e.g. "DISTILL LENS: beginner"): Set note frontmatter **`distill_lens: [angle]`** (or pass in queue payload), then run autonomous-distill; distill-perspective-refine and auto-layer-select use it.
- **HIGHLIGHT PERSPECTIVE: [lens]** (e.g. "HIGHLIGHT PERSPECTIVE: combat"): Set context (frontmatter or payload **`perspective`**), then run pipeline; distill-highlight-color applies lens-focused colors.
- **Queue**: `mode: "DISTILL MODE"` or `"BATCH-DISTILL"` → Queue subagent dispatches here. **Step 0**: When queue processor applies an approved wrapper with `pipeline: distill`, it runs **distill-apply-from-wrapper**, which re-runs this pipeline on `original_path` with `approved_option` as distill_lens override.

## Pipeline overview

**Entry condition (hand-off required when queue-dispatched):** When this pipeline was invoked by the Queue subagent for a queue entry, the hand-off block for that entry (task, queue entry, invariants, state files, return format per [Subagent-Safety-Contract](3-Resources/Second-Brain/Subagent-Safety-Contract.md)) must have been **output** as the first content for that entry. If you are running for a queue entry and that hand-off was **not** output above for it, do **not** run the following steps; state: "Hand-off missing. Queue processor must output the hand-off block for this entry before pipeline steps." and stop.

1. **Backup**: Ensure `obsidian_create_backup` for the note (always-applied MCP rule).
2. **Optional pre-step (batch >5 notes)**: `obsidian_garden_review`(scope, focus: **distill_candidates**, output_path, auto_apply); then run autonomous-distill on that set.
3. **Optional — `auto-layer-select`**: When enabled, suggest 1/2/3 layers; read **distill_lens** from frontmatter or wrapper override. Manual override remains.
4. **Distill layers**: Standard distill layers (lens applied when distill_lens set).
5. **`distill-highlight-color`** — project-aware highlights (≥85%); **highlight-perspective-layer** when perspective/lens set.
6. **`layer-promote`** — bold → highlight → TL;DR (≥85%).
7. **`distill-perspective-refine`** — depth/drift in TL;DR when distill_lens set.
8. **`callout-tldr-wrap`** — wrap TL;DR in `> [!summary] TL;DR` (always).
9. **`readability-flag`** — needs-simplify + warning callout when low readability (≥85% or metadata-only lower per reference).
10. **Logging**: `obsidian_log_action`; append to `3-Resources/Distill-Log.md` and `3-Resources/Backup-Log.md`. When note has tag `agent-research`, set frontmatter `research_distilled: true` after successful pass.
11. **Mandatory nested validator (distill_readability)**: After a successful distill pass, DistillSubagent **MUST**:
    - Run the shared **little val** structural check once for this run and only allow Success when the final little val verdict is `ok: true`.
    - Immediately after a final `ok: true` verdict and when the distilled note meets the configured word-count threshold, call **ValidatorSubagent** exactly once with `validation_type: "distill_readability"` and params `{ source_file, project_id? }` as a mandatory hostile gate (no sampling or config switches may skip this call).
    - **`severity: "high"`** or **`recommended_action: "block_destructive"`** → **hard block**; **MUST NOT** return Success. When **`validator.tiered_blocks_enabled`** is **true**, **`needs_work`** without high/block → **Success allowed** if little val ok (**Subagent-Safety-Contract § Tiered nested validator Success gate**).
    - On Success, return `little_val_ok: true` and a non-empty `validator_context` object that exactly matches this call so the Queue/Dispatcher can run the **post–little-val hostile validator pass** described in `Subagent-Safety-Contract.md` and `Queue-Sources.md`.
12. **Run-Telemetry:** Before return, read **parent_run_id**, **queue_entry_id**, and **project_id** from the hand-off block for this run; use them in the Run-Telemetry note. Ensure `.technical/Run-Telemetry/` exists (e.g. obsidian_ensure_structure) before writing. Write one note to `.technical/Run-Telemetry/` per [Subagent-Safety-Contract](3-Resources/Second-Brain/Subagent-Safety-Contract.md) and [Logs § Run-Telemetry](3-Resources/Second-Brain/Logs.md) (required: actor, project_id, queue_entry_id, timestamp, parent_run_id; optional: context, tool_calls, internals when available).

Confidence thresholds and skill order must match `Cursor-Skill-Pipelines-Reference.md`; reference table takes precedence.

## Batch and isolation

- Process **one note fully** before the next. Batch size: up to ~5 notes for DISTILL MODE – safe batch autopilot.
- On failure: log with `#review-needed` in Distill-Log.md (and Backup-Log.md when snapshots involved); skip remaining destructive steps for that note, continue batch.

## Error handling

On failure of backup, snapshot, or any skill: Follow **Error Handling Protocol** in mcp-obsidian-integration.mdc. Pipeline: `autonomous-distill`; include **error_type** in Errors.md entry table. Append to 3-Resources/Errors.md and one-line ref in Distill-Log.md (and Backup-Log.md when applicable). High severity: skip destructive steps for that note, continue.

## Snapshots and checkpoints

- **Per-change**: Before **first structural rewrite** (distill layers / layer-promote / heavy update_note), when confidence **≥85%**, call `obsidian-snapshot` type "per-change" for the target note. Below threshold: do not snapshot, do not perform destructive action; log `#review-needed`.
- **Batch**: After every **3 notes**, `obsidian-snapshot` type "batch" with pipeline context, list of notes, links to per-change snapshots. Log in Distill-Log.md and Backup-Log.md.

## Confidence bands & distill depth loop

- **Primary signal**: `distill_conf` (from auto-layer-select or equivalent).
- **High (≥85)**: After snapshot, run full structural distill (layers, highlight, promote, wrap, readability).
- **Mid (68–84)**: Depth self-critique loop; consider shallower plan; compute `post_loop_conf`. If post_loop_conf ≥85: snapshot → run shallower plan. Else: skip structural distill; run only readability-flag + **create Decision Wrapper** under `Ingest/Decisions/Refinements/` (wrapper_type mid-band-refinement, pipeline distill); CHECK_WRAPPERS; Watcher-Result "created wrapper → Decisions/Refinements/…". Use User-Questions-and-Options-Reference §2 for A–G.
- **Low (<68)**: No structural distill; readability-flag + frontmatter flags only. **Create Decision Wrapper** under `Ingest/Decisions/Low-Confidence/` (wrapper_type low-confidence, pipeline distill). CHECK_WRAPPERS; Watcher-Result. Use User-Questions-and-Options-Reference §2.
- **Loop logging**: `loop_attempted`, `loop_band`, `pre_loop_conf`, `post_loop_conf`, `loop_outcome`, `loop_type: "distill-depth"`, `loop_reason` in Distill-Log.md and obsidian_log_action.

## Exclusions

**Includes**: 1-Projects/** , 2-Areas/** , 3-Resources/** . **Excludes**: 4-Archives/**, Backups/**, Templates/**, **/Log*.md, **/* Hub.md. Same as prior auto-distill; no recursive processing of history, logs, or hubs.

## Safety

- Backups first; per-change snapshot mandatory before structural rewrite when confidence ≥85%. No destructive action unless confidence ≥85% **and** successful per-change snapshot in current run. Else skip, log `#review-needed`. No shell cp/mv/rm. Restore is user-triggered only.

## Rollout guidance

Start with a single test project folder; run 3–5 batch tests; confirm snapshots and no unexpected #review-needed; then widen to full globs.
