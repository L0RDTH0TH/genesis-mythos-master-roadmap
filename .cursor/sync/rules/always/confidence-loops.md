---
description: Shared confidence bands, refinement loops, and self-critique template for autonomous pipelines.
alwaysApply: true
---

# Confidence Loops & Self-Critique (All Pipelines)

- **Purpose**: Normalize how confidence is interpreted across ingest, organize, archive, express, and distill pipelines, and define a single, non-destructive refinement loop in the mid-confidence band.
- **Scope**: Applies to all autonomous pipelines described in `3-Resources/Cursor-Skill-Pipelines-Reference.md` and their context rules under `.cursor/rules/context/`.

## Standard Confidence Bands

- **High-confidence (proceed)**: \(\ge 85\%\) (or **tunable** `high_threshold` from Second-Brain-Config when present)
  - Destructive actions (move, rename, split, structural distill, large appends) are allowed **only** in this band and only after a successful per-change snapshot.
- **Mid-band (loop)**: \(68\% \le conf \le 84\%\) (or **tunable** `mid: [min, max]` from Second-Brain-Config when present)
  - Triggers **at most one** non-destructive refinement loop per note per pipeline run.
- **Low-confidence**: \(<68\%\) (or below configured mid minimum)
  - **No loop**. Do not perform destructive actions; treat outputs as proposals / candidates and hand them off to **user decision flows** (e.g. Decision Wrappers for ingest, async preview + `approved: true` for other pipelines) rather than auto-applying changes.

**Tunable bands**: When `confidence_bands` is set in `3-Resources/Second-Brain-Config.md` (e.g. `mid: [80, 90]`, `high_threshold: 90`), rules and skills **read** these values; otherwise fallback to the defaults above. See Parameters.md.

**Loop-skip flag**: When a note has frontmatter **`loop-skip: true`** (or **`skip_refinement_loop: true`**), **skip** the mid-band refinement loop for that note (trusted path). Proceed to snapshot + destructive action only if confidence already meets high threshold; otherwise treat as proposal. Document in Parameters.md and pipeline reference.

## Pipeline Signals

Each pipeline exposes a single primary confidence signal that drives loop decisions:

- **full-autonomous-ingest**: `ingest_conf`
  - Derived after `classify_para` + `frontmatter-enrich` + non-destructive `subfolder-organize` path proposal.
- **autonomous-organize**: `path_conf`
  - Derived from `subfolder-organize` in re-org mode after `frontmatter-enrich`.
- **autonomous-archive**: `archive_conf`
  - Derived from `archive-check` (archive readiness).
- **autonomous-express**: `express_conf`
  - Derived after `related-content-pull` / outline readiness assessment.
- **autonomous-distill**: `distill_conf`
  - Derived from `auto-layer-select` / depth evaluation or equivalent heuristics.

Pipelines MAY track additional internal confidences (e.g. per-skill gates), but destructive steps are governed by these primary signals plus snapshot success.

## Loop Invariants

- **Single loop**: At most **one refinement loop per note per pipeline run**.
- **Pre/post tracking**: Store:
  - `pre_loop_conf` (integer, 0–100)
  - `post_loop_conf` (integer, 0–100)
- **Decay rule**:
  - If `post_loop_conf <= pre_loop_conf`, immediately fall back to **user decision behavior**:
    - No destructive actions for this note in the current run.
    - Log best-guess classification/path and mark `#review-needed` where appropriate.
    - For ingest specifically, this means routing into the **Decision Wrapper / user-decision loop** (create or update the wrapper under `Ingest/Decisions/` for that note) rather than leaving the note in Ingest/ with only a `#review-needed` flag.
- **Early exit**:
  - If `post_loop_conf \(\ge 90\%\)`:
    - You may skip **non-essential** remaining steps for that specific decision and proceed directly to:
      - Per-change snapshot (via `obsidian-snapshot` skill).
      - The gated destructive action (e.g. move, structural distill, expressive append) for that pipeline.
- **Non-destructive loop content only**:
  - Allowed within the loop:
    - Metadata / tags / frontmatter updates on the **current note**.
    - Analysis, self-critique, and re-scoring.
    - Multi-path proposals (alternate paths or archive/organize options).
    - Preview-only drafts (distill/express) that are **not yet written back**.
  - Forbidden within the loop:
    - `obsidian_move_note`, `obsidian_rename_note`, `obsidian_split_atomic`.
    - Cross-note appends such as `append_to_hub`, `related-content-pull` writes, or distill rewrites.
    - Any destructive MCP action (delete, overwrite) on any note.

## Shared Self-Critique Template

Use this template for loops in ingest, organize, archive, and adapted versions for express/distill. Populate it with the previous decision and evidence before re-scoring:

> **Previous output**: [PASTE classify/para-type + path + confidence]  
>  
> **Assumptions**: What weak assumptions did you make about PARA actionability, project-id, or atomicity?  
>  
> **Evidence check**: Does title/headings/tasks/backlinks contradict or support the decision?  
>  
> **Risks**: Where could this go wrong (e.g., over-generalization, missed nuance)?  
>  
> **Neighbor fit**: How well does this align with similar notes in the proposed folder/hub?  
>  
> **Revised**: Propose updated para-type / project-id / path (or top 2–3 candidates with scores).  
>  
> **New confidence**: 0–100% (justify downward adjustment if uncertain).

**Output only** from the loop: revised classification/path (or ranked candidates) + `post_loop_conf` + one-sentence rationale.

## Interaction with Snapshots

- Loops run **before** any per-change snapshot; snapshots are reserved for actual destructive steps.
- After a loop:
  - Proceed to snapshot + destructive action **only if**:
    - The relevant primary signal is now \(\ge 85\%\), **and**
    - `post_loop_conf > pre_loop_conf`, **and**
    - Snapshot creation via `obsidian-snapshot` succeeds for that note.
  - If any of these conditions fail:
    - Skip the destructive action for this note in the current run.
    - Log with `#review-needed` where appropriate.

## Loop Logging Fields

All pipelines that implement loops must add the following fields to their log entries (Ingest, Organize, Archive, Express, Distill):

- `loop_attempted: true|false`
- `loop_band: "68-84" | "none"` (or other label if extended later)
- `pre_loop_conf: int` (0–100; 0 or `null` when no loop)
- `post_loop_conf: int` (0–100; 0 or `null` when no loop)
- `loop_outcome: increased | flat | decreased`
- `loop_type: ingest-refine | organize-path | archive-refine | express-soft | distill-depth`
- `loop_reason: short free-text` (e.g. `"ambiguous project-id"`, `"recent edits"`, `"open tasks found"`).

These values should be recorded consistently in:

- The human-readable log notes (`3-Resources/*-Log.md`).
- The `changes` string or structured fields of `obsidian_log_action`, so Dataview queries can aggregate loop behavior across pipelines.

## Proposal auto-escalation (re-queue after edit)

When a **low-confidence** proposal is logged (proposal callout written to the note), the user can **add `approved: true` to the note's frontmatter** and run **EAT-QUEUE** again. The auto-eat-queue rule (optional pre-dispatch) scans for notes with `approved: true` and a matching proposal id/tag and injects a queue entry or processes inline, so the next run re-processes that note. See `3-Resources/Second-Brain/Templates.md` (Re-queue after edit) and Queue-Sources.
