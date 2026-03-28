---
description: "IngestSubagent — Ingest/ processing: non-MD handling, embedded image normalization, Phase 1 full-autonomous-ingest (propose + Decision Wrapper), Phase 2 apply-mode. INGEST MODE and apply-mode routed here by Queue subagent."
globs:
  - "Ingest/**"
alwaysApply: false
---

# IngestSubagent (context rule)

- **Subagent**: This rule is the **IngestSubagent**. Responsible for Ingest/ processing: (1) non-MD handling (companion .md, attempt move to 5-Attachments), (2) embedded image normalization for .md, (3) Phase 1 full-autonomous-ingest (propose-only + Decision Wrapper, no moves/renames except Cursor-agent direct move when conditions hold), (4) Phase 2 apply-mode (approved wrapper → move/rename, post-move frontmatter). Invoked when user says INGEST MODE / Process Ingest / run ingests, or when the Queue subagent dispatches INGEST MODE or apply-mode ingest (Step 0 approved wrapper).
- **Reference**: [Cursor-Skill-Pipelines-Reference](3-Resources/Second-Brain/Cursor-Skill-Pipelines-Reference.md), [Queue-Sources](3-Resources/Second-Brain/Queue-Sources.md). **MCP safety**: [mcp-obsidian-integration.mdc](.cursor/rules/always/mcp-obsidian-integration.mdc) — backup before destructive steps, per-change snapshot, dry_run before move.

## Depends on (shared always rules)

This subagent **depends on** and does not duplicate: core-guardrails.mdc, confidence-loops.mdc, guidance-aware.mdc, mcp-obsidian-integration.mdc, watcher-result-append.mdc. Safety (Error Handling Protocol, confidence bands, exclusions) is inherited; no new safety logic here.

## Todo orchestration (todo-orchestrator)

- For each INGEST MODE run, treat the run as a small todo set managed via the shared **todo-orchestrator** pattern (see `.cursor/skills/todo-orchestrator/SKILL.md`):
  - Use a run-level identifier such as `ingest-phase-1` (or derive from telemetry when applicable).
  - Model phases as:
    - `scan-ingest` — list Ingest contents (markdown and non-markdown) and determine which notes/files are in scope for this run.
    - `handle-non-md` — apply **Non-markdown handling** for every non-.md file in the chosen scope (companion .md, subtype, embed, backup, move attempt to 5-Attachments).
    - `normalize-embeds` — run embedded image normalization for `.md` files in Ingest (rewrite embeds, add relocation callouts/tags).
    - `ingest-phase-1` — run Phase 1 full-autonomous-ingest over `.md` notes (classify PARA, frontmatter-enrich, name-enhance propose, subfolder-organize, split/distill/hub/task-reroute) up to but not including moves/renames that are reserved for apply-mode or Cursor-agent direct move.
    - `wrapper-or-direct-move` — for eligible notes, either create Decision Wrappers or perform Cursor-agent direct move when the strict conditions for that path are met.
  - When the run is a **pure apply-mode ingest** (triggered from an approved Decision Wrapper), you may instead model a smaller todo set focused on:
    - `resolve-wrapper` — resolve hard_target_path and guidance via feedback-incorporate.
    - `apply-move` — re-run classification/enrich/path with hard_target_path, snapshot, and move/rename.
    - `log-and-mark-wrapper` — update wrapper (used_at, processed) and log to Ingest-Log.
- Around each of these phases, update the corresponding todos via `TodoWrite`:
  - Mark a phase todo `in_progress` before its work begins and `completed` when its responsibilities have been satisfied (including the “nothing to do” case).
  - If a phase is intentionally skipped (e.g. no non-MD files present, or only apply-mode ingest is running), mark its todo `cancelled` and surface the reason in Ingest-Log.md or the subagent’s structured return.
- Before returning from IngestSubagent for any run:
  - You **MUST** ensure that all todos for the active run_id are either `completed` or `cancelled` before you return **Success**.
  - You **MUST NOT** return Success while any ingest-phase todo remains `pending` or `in_progress`; if an error or guardrail forces early exit, mark remaining todos `cancelled` with a short, human-readable reason and record it in the ingest logs, and return a failure or `#review-needed` status instead of Success.
## Subagent nesting

- IngestSubagent is primarily a **top-level pipeline executor**. It may call **nested subagents only where explicitly documented** in the global nested-subagent whitelist (see `3-Resources/Second-Brain/Docs/Subagent-List.md`).
- **You may ONLY call** the specific nested subagent types listed in your own "Subagent nesting" section in the docs, and **ONLY** for the narrow purposes described there (e.g. Validator for ingest_classification checks when the queue has already dispatched VALIDATE).
- **You MUST NEVER**:
  - Read or write `.technical/prompt-queue.jsonl` or `3-Resources/Task-Queue.md`.
  - Append to `3-Resources/Watcher-Result.md`.
  - Create, apply, or move Decision Wrappers under `Ingest/Decisions/**`.
  - Mutate roadmap coordination files such as `roadmap-state.md` or `workflow_state.md`.
- **You must ALWAYS**:
  - Treat any nested subagent you call as a **pure helper**: pass in explicit inputs, and consume only its **structured result** (e.g. validation verdict); do not let it orchestrate or chain further pipelines.
  - Return your own results as structured data to the **main agent / Queue rule**, which remains the only orchestrator for queues, wrappers, and Watcher-Result.
  - On **every** final return, emit fenced YAML **`nested_subagent_ledger:`** per [Nested-Subagent-Ledger-Spec](3-Resources/Second-Brain/Docs/Nested-Subagent-Ledger-Spec.md) (including **Attestation invariants**) and [.cursor/agents/ingest.md](.cursor/agents/ingest.md) § **nested_subagent_ledger (required)**; follow the **pre-return checklist** and **Ledger attestation** there (no Success with **`little_val_ok: true`** without **`validator_context`** + ledger when applicable; no false-green **`invoked_ok`** + **`task_tool_invoked: false`** on mandated nested helper steps).
  - **Task hand-off comms:** When **`task_handoff_comms.enabled`** is not **false**, before and after each nested **`Task`** to **validator**, **internal-repair-agent**, or **research**, append **`handoff_out`** / **`return_in`** to **`.technical/task-handoff-comms.jsonl`** per [[3-Resources/Second-Brain/Docs/Task-Handoff-Comms-Spec|Task-Handoff-Comms-Spec]] and [.cursor/agents/ingest.md](.cursor/agents/ingest.md) § **Task hand-off comms (nested helpers)**.

## Safety

- IngestSubagent obeys Error Handling Protocol, confidence bands, guidance-aware, and Watcher exclusions via shared always rules. Destructive operations (move, rename, split, distill, append_to_hub) occur only in downstream steps with backup + snapshot gates as in Cursor-Skill-Pipelines-Reference.

---

## How to activate

- **User**: "INGEST MODE", "Process Ingest", "run ingests" → run full flow below (ingest-processing then Phase 1 on .md; apply-mode only when triggered by approved wrapper via queue).
- **Queue**: Entry `mode: "INGEST MODE"` → Queue subagent dispatches here; run same flow. Apply-mode: when Queue subagent Step 0 processes an approved Decision Wrapper under `Ingest/Decisions/`, it invokes apply-mode ingest (behavior defined in "Apply-mode ingest" below).

---

## Flow (entry)

**Entry condition (hand-off required when queue-dispatched):** When this pipeline was invoked by the Queue subagent for a queue entry, the hand-off block for that entry (task, queue entry, invariants, state files, return format per [Subagent-Safety-Contract](3-Resources/Second-Brain/Subagent-Safety-Contract.md)) must have been **output** as the first content for that entry. If you are running for a queue entry and that hand-off was **not** output above for it, do **not** run the following steps; state: "Hand-off missing. Queue processor must output the hand-off block for this entry before pipeline steps." and stop.

1. **List Ingest**: `obsidian_list_notes("Ingest")` for .md; also list non-.md in Ingest (workspace glob/list).
2. **Non-.md**: For each non-.md file, follow **Non-markdown handling** (subsection below): companion .md, subtype, embed, backup, attempt move to 5-Attachments/[subtype]; on failure leave in Ingest/ with #needs-manual-move.
3. **Embedded image normalization** (for .md in Ingest): Scan note content for image embeds (`![[...png]]`, etc.). Rewrite links to `![[5-Attachments/Images/original-filename.ext]]`; add callout "Manual image relocation needed" and tags #needs-attachment-relocation, #attachment-relocation-pending. Never move image files via MCP; user drag-drops.
4. **.md**: After non-MD and embedded normalization, run **Phase 1 full-autonomous-ingest** on all `Ingest/**/*.md` (excluding `Ingest/Decisions/**` and watcher/control notes), or **Phase 2 apply-mode** when this run was triggered by an approved wrapper (Step 0 path-apply).

**Exclusions**: Do not process `Ingest/Decisions/**`, `Ingest/watched-file.md`, or notes with `watcher-protected: true`. Do not process Backups/.

---

## Non-markdown handling

When processing any non-.md file in Ingest/:

- **Classify → Create companion .md** (title, created, aliases, tags, source embed). Use [Attachment-Subtype-Mapping](3-Resources/Attachment-Subtype-Mapping.md) or table: Images → 5-Attachments/Images/, PDFs → PDFs/, Documents → Documents/, Audio/Video → Audio/, Other → Other/.
- **Embed**: `source: "![[5-Attachments/<subtype>/<filename>]]"` (or final path after move).
- **Attempt automatic move**: If companion or original has **#skip-auto-move**, skip move. Else: validate source under Ingest/; resolve destination conflicts (timestamp suffix if exists). **obsidian_ensure_structure**("5-Attachments/<subtype>"). **obsidian_create_backup**([Ingest/<filename>]). Only if backup succeeds: **obsidian_move_note**(Ingest/<filename>, 5-Attachments/<subtype>/<final-filename>). On success: companion source = moved path; success callout; no #needs-manual-move. On failure: leave in Ingest/, add #needs-manual-move, failure callout, log.
- **MCP**: No shell mv/cp/rm except move-attachment-to-99 when user explicitly invokes. Follow Error Handling Protocol on failure.

---

## Phase 1 — full-autonomous-ingest (propose + Decision Wrapper)

**PARA**: 1-Projects/, 2-Areas/, 3-Resources/, 4-Archives/. **Zettel**: Atomic notes, CODE = Capture → Organize → Distill → Express; append to hubs.

**Confidence bands** (ingest_conf from classify_para + frontmatter-enrich + subfolder-organize path proposal):

- **≥85%**: Execute in-note destructive steps (split, distill, append_to_hub, task-reroute) after required snapshots; **no move/rename in Phase 1** except Cursor-agent direct move (see below).
- **≥78%**: Non-destructive + cross-note safe writes (frontmatter, append_to_hub, task-reroute per skill gates); no move/rename.
- **70–77%**: Propose only, #review-needed; apply frontmatter/links if project_name present.
- **<70%**: Backup + log; no destructive actions.

**Pipeline order**: Read → Classify PARA (CoT + %) → Split if multi-idea (high conf only) → Distill (TL;DR, bold, next actions) → Append to hub / task-reroute (per skill gates) → **Propose move/rename via Decision Wrapper only** (unless Cursor-agent direct move) → Log. **Skills**: classify_para → frontmatter-enrich → **name-enhance** (propose only in Phase 1) → subfolder-organize; after split_atomic → split-link-preserve; after distill → distill-highlight-color, next-action-extract, task-reroute (task-like and conf ≥78%); after append_to_hub → **link-to-pmg-if-applicable**. **In ingest, name-enhance proposes; subfolder-organize commits the name via move in apply-mode.**

**Mandatory nested validator (ingest_classification)**: For every ingest run that mutates notes/state and intends to return **Success**, IngestSubagent **MUST**:
- Run the shared **little val** structural check once for this run and only allow Success when the final little val verdict is `ok: true`.
- Immediately after a final `ok: true` verdict, call **ValidatorSubagent** exactly once with `validation_type: "ingest_classification"` and params `{ source_file, proposed_path, para_type, ingest_conf, project_id? }` as a mandatory hostile gate (no sampling or config switches may skip this call).
- For normal ingest and wrapper/apply-mode paths, apply **Subagent-Safety-Contract § Tiered nested validator Success gate** after the final nested validator pass. **`severity: "high"`** or **`recommended_action: "block_destructive"`** → **no Success**. When **`validator.tiered_blocks_enabled`** is **true**, **`needs_work`** without high/block → **Success allowed** if little val ok. See [[3-Resources/Second-Brain/Docs/Validator-Tiered-Blocks-Spec|Validator-Tiered-Blocks-Spec]] for roadmap-aligned codes; `ingest_classification` uses the same Success rule pattern.
- **Exception (auto-apply policy branch):** For eligible agent-generated direct-move notes (`Ingest/Agent-Output/` or `Ingest/Agent-Research/`, or `agent-generated: true`) when `prompt_defaults.ingest.auto_apply_agent_generated_without_wrapper: true` and `prompt_defaults.ingest.validator_block_agent_generated_without_wrapper: false`, validator results are **advisory-only** for that branch. Log validator output, but do not block direct move solely from validator severity.
- On Success, return `little_val_ok: true` and a non-empty `validator_context` object that exactly matches this call so the Queue/Dispatcher can run the **post–little-val hostile validator pass** described in `Subagent-Safety-Contract.md` and `Queue-Sources.md`.

**Lowered-threshold runs**: When confidence overwrite relaxes gates, still run frontmatter-enrich and at least minimal distill (TL;DR, strip raw Ingest template) before creating wrapper. No note may be moved into PARA while still raw (e.g. title: Untitled, template intact); moves only in apply-mode after user approval.

### Cursor-agent direct move (Phase 1 — skip wrapper)

**When**: Note under `Ingest/Agent-Output/`, under `Ingest/Agent-Research/` (research synthesis notes), or `agent-generated: true`; run is **not** FORCE-WRAPPER; **ingest_conf ≥ 85%** or `confidence_override: high`; subfolder-organize has single clear target. When **tech_level > 1** and confidence mid-band (68–84%), do **not** direct-move; fall through to Decision Wrapper.

**Policy boundary**: This path is an **auto-apply ingest policy** for eligible agent-generated notes. It does **not** change Decision Wrapper semantics: `approved: true` remains wrapper-only state under `Ingest/Decisions/**`.

**Behavior**: Do not create wrapper. obsidian-snapshot (per-change) → obsidian_ensure_structure(parent of target) → obsidian_move_note dry_run then commit → post-move frontmatter sync (para-type, project-id, status). Provenance callout. Log Ingest-Log.md with #cursor-agent-direct and note path + target path (+ tech_level if present).

### Decision Wrapper creation (Phase 1)

After frontmatter-enrich + name-enhance (propose) + subfolder-organize:

- **FORCE-WRAPPER**: When queue mode FORCE-WRAPPER or `force_wrapper: true`, **always** create wrapper, never move/rename. wrapper_type force-wrapper (or ingest-decision), clunk_severity low.
- Else: Call **propose_para_paths**(path, para_type, max_candidates "7", context_mode "wrapper", rationale_style "concise"). Use candidates to fill options A–G; pad to **exactly 7** (fallbacks: classified PARA root+basename, other PARA roots+basename, 3-Resources/Unfiled/, 4-Archives/Ingest-YYYY-MM-DD/). Use [User-Questions-and-Options-Reference](3-Resources/Second-Brain/User-Questions-and-Options-Reference.md) §2 for labels. Display confidence: conf_display = max(40, min(98, round(score))).
- **Template**: Read `Templates/Decisions/Decision-Wrapper.md`. Fill {{candidate_a_path}}…G, {{original_path}}, {{original_filename}}, {{original_slug}}, {{proposal_path}}, {{date}}, {{time}}, {{priority}}.
- **Write** to `Ingest/Decisions/Ingest-Decisions/Decision-for-{{original_slug}}--{{YYYY-MM-DD-HHMM}}.md`. **obsidian_ensure_structure**("Ingest/Decisions/Ingest-Decisions").
- Set on original note: `decision_candidate: true`, `proposal_path: "{{wrapper_path}}"`, `decision_priority: high|medium`.
- **CHECK_WRAPPERS**: After wrapper creation, ensure queue has an entry with mode "INGEST MODE" and prompt "CHECK_WRAPPERS"; if none, append `{"mode":"INGEST MODE","prompt":"CHECK_WRAPPERS","source_file":"Ingest/Decisions/","id":"check-wrappers-<timestamp>"}`.
- Log Ingest-Log.md: "… | Flag: #decision-wrapper-created | Decision Wrapper created — up to 7 candidates … | Wrapper: Ingest/Decisions/…"
- **STOP** move/rename for this note this run. Wait for EAT-QUEUE with approved wrapper to trigger apply-mode.

### Apply-mode ingest (Phase 2 — from approved Decision Wrapper)

When queue entry is for a wrapper under `Ingest/Decisions/` with `approved: true`:

- feedback-incorporate resolves **hard_target_path** (from approved_path or candidate A–G), **guidance_text** (wrapper body), optionally guidance_conf_boost.
- Skip Decision Wrapper creation. Re-run classify_para + frontmatter-enrich + subfolder-organize with hard_target_path and guidance. After per-change snapshot and confidence ≥85% (or post_loop_conf ≥85%): **obsidian_ensure_structure**(parent of hard_target_path) → **obsidian_move_note**(path, hard_target_path, dry_run: true then false) → post-move frontmatter sync. **obsidian_rename_note** when name-enhance suggested and conf ≥85%.
- Update wrapper (used_at, processed: true); log Ingest-Log.md. Queue processor (Step 0) **moves wrapper to 4-Archives/Ingest-Decisions/** after apply.

---

## Batch and isolation

- Process **one note fully** (including obsidian_log_action) before the next. Batch limit: up to 5 notes per run (or configured); sequential.
- **On failure**: Log note path in Ingest-Log.md with #review-needed; **continue with next note**. Do not halt batch for single-note failure.

---

## Error handling

On any error (backup, classify_para, frontmatter-enrich, name-enhance, subfolder-organize, split_atomic, distill_note, append_to_hub, move_note, log_action, non-MD, embedded norm):

- Follow **Error Handling Protocol** in mcp-obsidian-integration.mdc. Pipeline: ingest-processing or full-autonomous-ingest; stage as appropriate. Include error_type in Errors.md entry table. Append to 3-Resources/Errors.md (heading, table, #### Trace, #### Summary); one-line ref in Ingest-Log.md. High severity: skip destructive steps for that note, continue.

## Run-Telemetry

- Before return, read **parent_run_id**, **queue_entry_id**, and **project_id** from the hand-off block for this run; use them in the Run-Telemetry note. Ensure `.technical/Run-Telemetry/` exists (e.g. obsidian_ensure_structure) before writing. Write one note to `.technical/Run-Telemetry/` per [Subagent-Safety-Contract](3-Resources/Second-Brain/Subagent-Safety-Contract.md) and [Logs § Run-Telemetry](3-Resources/Second-Brain/Logs.md) (required: actor, project_id, queue_entry_id, timestamp, parent_run_id from hand-off; optional: context, tool_calls, internals when available).

---

## Snapshots and checkpoints

- **External backup**: Every ingest run MUST start with obsidian_create_backup per note (BACKUP_DIR).
- **Per-change snapshots**: Before obsidian_split_atomic, obsidian_distill_note (rewrite), obsidian_append_to_hub, obsidian_move_note, obsidian_rename_note. When confidence ≥78% (moves into existing) or ≥85% (split, distill, new structure). 70–77%: no snapshot or move; frontmatter/links only, #review-needed. <70%: no destructive action, #review-needed in Ingest-Log.
- **Batch**: After every 5 notes (or configured), obsidian-snapshot type "batch" with notes/snapshot paths; log to Ingest-Log and Backup-Log.
- **Exclusions**: Backups/; Ingest/Decisions/** (wrappers only, not inputs); Ingest/watched-file.md, Watcher-Signal.md, Watcher-Result.md, watcher-protected: true.
