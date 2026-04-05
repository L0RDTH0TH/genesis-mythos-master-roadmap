---
title: Mode Success Contracts
created: 2026-03-10
tags: [second-brain, contracts, pipelines, roadmap]
para-type: Resource
status: active
links: ["[[3-Resources/Second-Brain/Backbone]]", "[[3-Resources/Second-Brain/Pipelines]]", "[[3-Resources/Second-Brain/Queue-Alias-Table]]"]
---

# Mode Success Contracts

Single place that defines, for each **core mode**, what counts as **success**, what is a **silent failure** (never acceptable), and what **recovery path** must be taken. This is the reference used when updating docs, rules, and tests.

For each mode:

- **Success must end in one of**:
  - State file updated (frontmatter/body change that advances progress),
  - Queue entry appended (follow-up work),
  - Decision Wrapper created/updated, or
  - High-severity error logged (with `#review-needed` and recovery guidance).
- **Silent no-op** (content-only work that does not advance state, queue, wrapper, or error) is a **bug**, not an acceptable outcome.

## INGEST MODE (full-autonomous-ingest)

- **Success (per run, per note)**:
  - Phase 1 (propose-only) on `Ingest/**/*.md`:
    - Note is classified (frontmatter `para-type`, `status`, confidence) and, when applicable, split into atomic children.
    - Distill + highlight + next-actions + task reroute + hub append run as confidence allows.
    - A **Decision Wrapper** under `Ingest/Decisions/` (e.g. `Ingest-Decisions/`) is **created or refreshed** with 7 ranked PARA path options (A–G) for relocation.
  - Phase 2 (apply-mode via approved wrapper + EAT-QUEUE):
    - For each approved wrapper, after backup + snapshot and dry_run move:
      - Original note is moved/renamed from `Ingest/` into the user-approved PARA path.
      - Post-move para-type (and project-id when under `1-Projects/`) is synced.
      - Wrapper is archived to `4-Archives/Ingest-Decisions/...`.
- **Silent failure / no-op**:
  - Phase 1: Pipelines run but **no Decision Wrapper is created/updated** for a note that was in scope.
  - Phase 2: EAT-QUEUE Step 0 finds an approved ingest wrapper but **neither moves the note nor archives the wrapper nor logs an error**.
- **Recovery path**:
  - Log to `Ingest-Log` and `Errors.md` with `#review-needed`, including note path and whether wrapper or move failed.
  - For wrapper creation failures: create an **error Decision Wrapper** under `Ingest/Decisions/Errors/` pointing to the affected note.
  - For move failures: follow MCP fallback table (ensure_structure → retry move) before logging error-only.
- **Self-audit**:
  - EAT-QUEUE Step 0 iterates `Ingest/Decisions/**` and, for each wrapper with `approved: true` or `re-wrap: true`, must:
    - Re-read wrapper + target note path,
    - Apply the action (move/rename or re-wrap), or
    - Log a high-severity error and leave the wrapper in place for human review.

## ORGANIZE MODE (autonomous-organize)

- **Success (per run, per note)**:
  - Note is re-classified (frontmatter enriched) and either:
    - Moved to a **better PARA path** under `1-Projects/`, `2-Areas/`, or `3-Resources/` (after backup + snapshot + dry_run), and/or
    - Renamed via `name-enhance` when appropriate (after snapshot).
  - `Organize-Log` records the decision and any move/rename.
- **Silent failure / no-op**:
  - Pipeline runs but:
    - No frontmatter update, no move, no rename, **and** no Decision Wrapper or error is produced when confidence was low/mid-band.
- **Recovery path**:
  - Low band: create a **Low-Confidence** Decision Wrapper under `Ingest/Decisions/Low-Confidence/`.
  - Mid band decay: create a **Refinements** wrapper under `Ingest/Decisions/Refinements/`.
  - Any MCP or snapshot failure: log to `Errors.md` and mark `#review-needed` in `Organize-Log`.
- **Self-audit**:
  - After move/rename, re-read note path and confirm new location and para-type/project-id sync match the computed target; log outcome.

## DISTILL MODE (autonomous-distill)

- **Success (per run, per note)**:
  - Backed up and (when confidence ≥85%):
    - Distill layers + highlight + layer promotion + TL;DR callout + readability flag applied.
  - `Distill-Log` updated with loop fields, coverage stats, and any heuristics.
- **Silent failure / no-op**:
  - Mid-band distill run that neither:
    - Commits a (possibly shallower) structural distill, nor
    - Creates a Decision Wrapper, nor
    - Logs a clear error.
- **Recovery path**:
  - Mid-band failure: create **Refinements** wrapper.
  - Low band: create **Low-Confidence** wrapper.
  - Snapshot or MCP failure: log error, skip destructive steps, leave note unchanged.
- **Self-audit**:
  - Confirm at end of run that either:
    - TL;DR / highlight structure changed, or
    - Appropriate wrapper/error was emitted and logged.

## EXPRESS MODE (autonomous-express)

- **Success (per run, per note)**:
  - Note is backed up and version-snapshotted.
  - Related content, mini-outline, and CTA are appended when express_conf ≥85% (or adjusted per mid-band soft loop).
  - `Express-Log` records actions and version paths.
- **Silent failure / no-op**:
  - express_conf in mid or high band but:
    - No outline/CTA written **and**
    - No Decision Wrapper, async preview, or error logged.
- **Recovery path**:
  - Mid band failure: create **Refinements** wrapper for express.
  - Low band: create **Low-Confidence** wrapper describing express options.
  - Snapshot/version failures: log to `Errors.md` and `Express-Log`, skip appends.
- **Self-audit**:
  - Verify that either:
    - Outline/CTA was appended (diff in note), or
    - A wrapper/error was created and logged as the outcome.

## ARCHIVE MODE (autonomous-archive)

- **Success (per run, per note)**:
  - archive-check ≥85% and a per-change snapshot succeeded.
  - Note is moved to `4-Archives/...` via ensure_structure + dry_run + move, with:
    - TL;DR or summary preserved,
    - Optional resurface-candidate mark,
    - Frontmatter `para-type: Archive` and `status: archived`.
  - `Archive-Log` and `Backup-Log` updated.
- **Silent failure / no-op**:
  - archive-check ≥85% but:
    - No move, no summary-preserve, no resurface mark, **and**
    - No error/wrapper created.
- **Recovery path**:
  - Mid band or low band archive_conf: create **Refinements** or **Low-Confidence** archive Decision Wrappers as per confidence-loops.
  - Any backup/snapshot/move failure: log error + `#review-needed`, skip destructive actions.
- **Self-audit**:
  - Confirm that all inspected candidates end the run in exactly one of:
    - Archived under `4-Archives/`,
    - Flagged via Decision Wrapper,
    - Logged error-only (no structural changes).

## ROADMAP MODE (setup-only, auto-roadmap)

- **Success (per run, per project)**:
  - For a project with a roadmap outline:
    - `1-Projects/<project_id>/Roadmap/roadmap-state.md` exists and parses,
    - `workflow_state.md`, `decisions-log.md`, and `distilled-core.md` exist or are created/updated as per Roadmap-Upgrade-Plan,
    - Initial phase tree and Phase-1 notes are created by `roadmap-generate-from-outline` when appropriate.
  - **ROADMAP MODE never runs RESUME-ROADMAP**; it is strictly setup.
- **Silent failure / no-op**:
  - ROADMAP MODE runs but:
    - No roadmap state artifacts are created/updated **and**
    - No error is logged and no wrapper created.
- **Recovery path**:
  - If state artifacts are invalid/missing: log to `Errors.md` with `#state-corrupt` or similar; create an **error Decision Wrapper** pointing at the project.
- **Self-audit**:
  - At end of ROADMAP MODE, re-read `roadmap-state.md` and `workflow_state.md` (when they should exist) and verify they are present and parseable.

## RESUME-ROADMAP (auto-roadmap, multi-run continue)

- **Success (per run)**:
  - One run = **one action** selected by `params.action` (default `deepen`).
  - At the end of the run, **exactly one** of the following must be true:
    1. **Advance**: roadmap-state and/or workflow_state advanced forward (e.g. new secondary/tertiary created; `current_phase` or `current_subphase_index` updated; iterations_per_phase incremented) with valid context metrics when tracking is enabled.
    2. **Follow-up queued**: a RESUME-ROADMAP / `RECAL-ROAD` / EXPAND-ROAD entry was appended to the queue for further work.
    3. **Wrapper created/updated**: a roadmap Decision Wrapper (e.g. roadmap-next-step, stall, handoff-readiness) was written under `Ingest/Decisions/Roadmap-Decisions/`.
    4. **High-severity error logged**: an error entry was appended to `Errors.md` with `#review-needed`, pointing at the relevant roadmap state/note (including context-tracking-missing or context-overflow).
  - When research is enabled for a deepen run, success additionally requires that **either**:
    - At least one Agent-Research note was written and considered inline (injected into deepen context), **or**
    - A research-empty/failure event was logged in `Errors.md` / Watcher-Result (no silent skip).
- **Silent failure / no-op**:
  - RESUME-ROADMAP runs, creates or edits roadmap content, **but**:
    - `roadmap-state.md` / `workflow_state.md` are unchanged,
    - No follow-up is queued,
    - No wrapper is created/updated,
    - No high-severity error is logged.
  - This pattern (content-but-no-state/queue/wrapper/error) is **never acceptable**; treat as a bug.
- **Recovery path**:
  - If state integrity checks fail in `roadmap-resume`: log `#state-corrupt` in `Errors.md` and create an **Errors** Decision Wrapper; do not deepen.
  - If context-utilization gates or drift checks trigger: queue `RECAL-ROAD` and record that in `workflow_state` Log; optionally set `status: blocked`.
  - If handoff gates fail: create a **roadmap-next-step** wrapper rather than advancing.
- **Self-audit**:
  - At the end of each RESUME-ROADMAP run, re-read `roadmap-state.md` and `workflow_state.md` and verify that the run ended in advance, queue, wrapper, or error; if not, log an explicit error.

## RESEARCH-AGENT (research-agent-run)

- **Success (per run)**:
  - For the requested scope:
    - External research is fetched and synthesized into one or more notes under `Ingest/Agent-Research/`, **and**
    - Corresponding INGEST MODE (and optional DISTILL MODE when `research_distill: true`) entries are queued for those notes, **or**
    - A clear error is logged when fetch/synthesis fails.
  - RESEARCH-AGENT no longer appends RESUME-ROADMAP; roadmap continuation always flows through explicit RESUME-ROADMAP deepen/recal/etc. entries.
- **Silent failure / no-op**:
  - Mode is triggered but:
    - No new research notes are written under `Ingest/Agent-Research/`,
    - No ingest/distill entries are queued,
    - And no error is produced.
  - **When 0 notes are written**, the queue processor must **not** treat as success: append Watcher-Result failure and mark entry `queue_failed: true`; do not count as success.
- **Recovery path**:
  - Log to `Errors.md` with enough details to re-run the research manually; optionally create a low-severity Decision Wrapper linked to the originating note/phase.
- **Self-audit**:
  - Confirm at the end of the run that either:
    - At least one path under `Ingest/Agent-Research/` was written **and** ingest/distill follow-ups were queued, or
    - An error was logged and surfaced to the user.

## EAT-QUEUE / PROCESS QUEUE (auto-eat-queue)

- **Success (per run)**:
  - Step 0 (CHECK_WRAPPERS) enumerates `Ingest/Decisions/**` and:
    - Applies any wrapper with `approved: true` or `re-wrap: true`, archiving it on success, or
    - Logs an error for wrappers that could not be applied.
  - Remaining queue entries in `.technical/prompt-queue.jsonl` (or pasted EAT-CACHE payload) are:
    - Parsed and validated,
    - Deduplicated and ordered by canonical sequence,
    - Dispatched by mode,
    - Each ending in a concrete outcome (state change, queue append, wrapper, or error).
  - A **Watcher-Result** line is appended for each processed entry.
- **Silent failure / no-op**:
  - Queue entries are consumed but:
    - Neither state nor wrappers nor errors reflect their processing, **and**
    - No Watcher-Result line is appended for them.
- **Recovery path**:
  - On invalid queue entries: mark as `queue_failed`, log to `Errors.md`, and, when configured, use `queue-cleanup` to sweep.
  - On dispatch failure: log the error, keep or re-append the entry with `queue_failed: true` for manual review.
- **Self-audit**:
  - Verify that, for each processed entry, there is a corresponding Watcher-Result line and at least one of state/queue/wrapper/error was affected.

## PROCESS TASK QUEUE (auto-queue-processor)

- **Success (per run)**:
  - Entries in `3-Resources/Task-Queue.md` (TASK-ROADMAP, TASK-COMPLETE, ADD-ROADMAP-ITEM, EXPAND-ROAD, etc.) are:
    - Parsed and validated,
    - Handled by the appropriate skill (e.g. add-roadmap-append, task-complete-validate),
    - Reflected in notes (tasks updated, roadmap items appended) or wrappers/errors when blocked.
- **Silent failure / no-op**:
  - Entries are removed or marked as processed without any corresponding note change, wrapper, or logged error.
- **Recovery path**:
  - Log to `Errors.md` and, where appropriate, create a Decision Wrapper in `Ingest/Decisions/Errors/` or a low-confidence wrapper for the affected note.
- **Self-audit**:
  - Confirm that each processed Task-Queue entry either:
    - Updated a note,
    - Created a wrapper, or
    - Logged an explicit error.

