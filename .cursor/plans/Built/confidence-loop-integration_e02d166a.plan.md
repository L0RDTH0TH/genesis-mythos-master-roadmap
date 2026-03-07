---
name: confidence-loop-integration
overview: Integrate your finalized confidence loop pattern (72–84% mid-band, ≥85% proceed, <72% manual) across all autonomous pipelines, including logging and self-critique templates, while preserving existing snapshot and safety rules.
todos:
  - id: define-loops-rule
    content: Create a new always-applied confidence-loops rule that encodes band thresholds, invariants, shared template, and log fields.
    status: completed
  - id: update-pipelines-reference
    content: Update Cursor-Skill-Pipelines-Reference.md to describe the 3-band confidence pattern, pipeline signals, loop behaviors, and logging schema with a state diagram.
    status: completed
  - id: wire-ingest-loop
    content: Integrate the ingest 72–84% refinement loop into full-autonomous-ingest, computing ingest_conf and gating destructive steps on post-loop confidence + snapshots.
    status: completed
  - id: wire-organize-archive-loops
    content: Add organize and archive loops (path and archive-refine) into their context rules, including neighbor/context checks and loop logging.
    status: completed
  - id: wire-express-distill-loops
    content: Implement soft-loop in autonomous-express and depth-control loop in autonomous-distill based on express_conf and distill_conf.
    status: completed
  - id: extend-logs-dataview
    content: Extend pipeline log formats and Dataview assumptions to include loop_* fields for monitoring loop effectiveness.
    status: completed
isProject: false
---

# Confidence Loop Integration Across Pipelines

## Goals

- Normalize confidence bands (low / mid-loop / high) and loop behavior across all autonomous pipelines.
- Keep all destructive actions behind both snapshot + ≥85% confidence gates, while adding a single non-destructive refinement loop in the 72–84% band.
- Extend pipeline logs with loop metadata for Dataview dashboards.

## Cross-cutting design

- **Standard bands**: Adopt the finalized thresholds everywhere:
  - **High-confidence (proceed)**: \ge 85.
  - **Mid-band (loop)**: 72 \le conf \le 84.
  - **Low-confidence**: <72 → *no loop*, direct manual review/candidate-only behavior.
- **Signals**: For each pipeline, define a single primary signal:
  - Ingest: `ingest_conf` (from classify/frontmatter + path proposal).
  - Organize: `path_conf` (from `subfolder-organize` in re-org mode).
  - Archive: `archive_conf` (from `archive-check`).
  - Express: `express_conf` (from outline/related-content readiness).
  - Distill: `distill_conf` (from `auto-layer-select` / depth evaluation or equivalent heuristic).
- **Loop invariants**:
  - At most **one loop iteration per note per pipeline run**; store `pre_loop_conf` and `post_loop_conf` for logging.
  - **Decay rule**: If `post_loop_conf <= pre_loop_conf`, immediately fall back to manual review behavior (no destructive step this run).
  - **Early exit**: If `post_loop_conf >= 90`, you may skip non-essential intermediate steps for that specific decision and go directly to snapshot + destructive action.
  - **Non-destructive loop content only**: Loops may adjust metadata/frontmatter, run analysis, generate *preview-only* drafts, and propose multi-path options, but must **not** move/rename/split or append into other notes.
- **Shared self-critique template**:
  - Implement a **single textual template** (as you wrote) referenced by:
    - full-autonomous-ingest (classification/path loop),
    - autonomous-organize (path loop),
    - autonomous-archive (archive readiness loop),
    - and adapted variants for express/distill.
  - Keep the implementation centralized in a new always-applied rule (e.g. `.cursor/rules/always/confidence-loops.mdc`) that defines:
    - The template text.
    - The band thresholds.
    - Generic state machine for `no-loop → loop → post-loop decision`.
- **Snapshot interaction**:
  - Do **not** take snapshots during the loop itself; snapshots remain tied to actual destructive steps as in `obsidian-snapshot/SKILL.md` and the pipelines reference.
  - After a loop, only proceed to snapshot + destructive action if the relevant signal is now **≥85%** and `post_loop_conf > pre_loop_conf`.

## Logging updates (all pipelines)

- **Extend log schema** in `3-Resources/Cursor-Skill-Pipelines-Reference.md` and each context rule (Ingest, Distill, Archive, Express, Organize) to include loop fields:
  - `loop_attempted: true|false`
  - `loop_band: "72-84" | "none"` (or other band label if extended later)
  - `pre_loop_conf: int`
  - `post_loop_conf: int`
  - `loop_outcome: increased | flat | decreased`
  - `loop_type: ingest-refine | organize-path | archive-refine | express-soft | distill-depth`
  - `loop_reason: short free-text` (e.g. `"ambiguous project-id"`, `"recent edits"`, `"open tasks"`).
- **Update canonical log line example** (Ingest-Log and mirrored logs) to show these fields appended at the end, so Dataview can query loop behavior without breaking existing dashboards.
- Ensure `obsidian_log_action` calls in each pipeline pass these values into the `changes` string or structured fields, mirroring the reference.

## Pipeline-specific integration

### 1. full-autonomous-ingest

- **Signal**: Define `ingest_conf` after `frontmatter-enrich` + `subfolder-organize` proposal, derived from:
  - classification/frontmatter confidence, and
  - confidence of the proposed `new_path` from `subfolder-organize`.
- **High (≥85%)**:
  - Keep existing behavior: per-change snapshot **then** `split_atomic` → `split-link-preserve` → `distill_note` → `distill-highlight-color` → `next-action-extract` → `append_to_hub` → `move_note`.
  - Retain internal `subfolder-organize` rule that differentiates new structure vs existing folder (e.g. existing-folder moves allowed at slightly lower internal confidence), but ensure the **pipeline-level decision to move** still requires `ingest_conf ≥ 85`.
- **Mid (72–84%) loop**:
  - Insert a **classification/path refinement loop** between `subfolder-organize` and any destructive step:
    - Run self-critique using the shared template, feeding in the current para-type, `project-id`, proposed path, and `ingest_conf`.
    - Ask `subfolder-organize` (non-destructively) to propose 2–3 candidate paths with scores.
    - Select the best candidate and compute `post_loop_conf`.
  - **Decisions**:
    - If `post_loop_conf >= 90`: early-exit → snapshot → proceed with full ingest pipeline, including move.
    - If `85 <= post_loop_conf <= 89`: snapshot → proceed with ingest pipeline normally (no extra early-exit skips beyond what you already considered non-essential).
    - Else (or if `post_loop_conf <= pre_loop_conf`): do **not** move/split/distill; keep the note in `Ingest/`, log the best-guess classification/path, set `#review-needed`, and treat as manual review candidate.
- **Low (<72%)**:
  - Skip the loop entirely; apply only safest metadata updates (e.g. minimal frontmatter) as already allowed.
  - Do **not** split/distill or move; log only best-guess classification/path + low confidence and tag for manual review.

### 2. autonomous-organize

- **Signal**: `path_conf` from `subfolder-organize` after `frontmatter-enrich` in re-org mode.
- **High (≥85%)**:
  - Maintain current behavior: snapshot → optional `obsidian_rename_note` → snapshot → `obsidian_move_note` → log.
- **Mid (72–84%) loop**:
  - Add a **neighbor/context loop** before rename/move:
    - Compare the note against siblings/peers in the candidate folders using headings, tags, and backlinks/hubs.
    - Run the shared self-critique template focused on path fit (`loop_type: organize-path`).
    - Optionally generate 2–3 alternative paths (e.g. different subfolders) with scores.
  - **Decisions**:
    - If `post_loop_conf >= 90` or `85–89`: snapshot → apply rename (if warranted) and move.
    - Else or if `post_loop_conf <= pre_loop_conf`: skip rename/move, log alternative paths + reasons, and tag `#review-needed`.
- **Low (<72%)**:
  - No loop; path proposals remain *propose-only* and no rename/move is executed. Log as such.

### 3. autonomous-archive

- **Signal**: `archive_conf` from `archive-check` (`≥85%` currently required to move).
- **High (≥85%)**:
  - Keep current sequence: per-change snapshot → `subfolder-organize` (archive path) → `resurface-candidate-mark` → `summary-preserve` → move → log.
- **Mid (72–84%) loop**:
  - Add an **archive-refine loop** right after `archive-check` but **before** any snapshot or structural changes:
    - Re-scan for open tasks and recency of edits using `archive-check` heuristics.
    - Optionally run a **non-destructive TL;DR refresh preview** (no write-back) to test whether the note feels “closed”.
    - Run the shared self-critique template with emphasis on readiness and related active notes.
    - Compute `post_loop_conf`.
  - **Decisions**:
    - If `post_loop_conf >= 90` or `85–89`: proceed with the existing snapshot + archive move chain.
    - Else or if `post_loop_conf <= pre_loop_conf`: skip archive move; leave the note active, log proposed archive path + reason, and tag as archive candidate only.
- **Low (<72%)**:
  - Don’t attempt the loop; mark note as **archive candidate** (e.g. via frontmatter flag) but keep it in active PARA, logging the low-confidence recommendation.

### 4. autonomous-express (soft loop)

- **Signal**: `express_conf` after `related-content-pull` (readiness to append outline/CTA).
- **High (≥85%)**:
  - Keep current flow: backup → version-snapshot → related-content-pull → express-mini-outline → call-to-action-append.
- **Mid (72–84%) soft loop**:
  - Since this is mostly additive (not structural), use a **soft loop**:
    - Generate a **short preview outline** and coherence/fidelity self-critique without writing to the note.
    - Re-score to `post_loop_conf`.
  - **Decisions**:
    - If `post_loop_conf >= 90`: commit the full outline + CTA as planned.
    - If `85–89`: optionally commit a **reduced outline** (e.g. fewer sections or shorter summary) + CTA.
    - Else or if `post_loop_conf <= pre_loop_conf`: skip related-content-pull/outline; optionally add a small CTA like “needs further distill before publish”, and log.
- **Low (<72%)**:
  - No expressive work beyond (optional) tiny CTA and logging; rely on prior distill/organize runs first.

### 5. autonomous-distill (depth control)

- **Signal**: `distill_conf` from `auto-layer-select` or a dedicated depth-evaluation step.
- **High (≥85%)**:
  - Run full planned distill depth: auto-layer-select (if enabled) → distill layers → distill-highlight-color → layer-promote → callout-tldr-wrap → readability-flag.
- **Mid (72–84%) loop**:
  - Insert a **depth self-critique loop** before running structural distill:
    - Use the shared template focused on depth choice and risk of nuance loss.
    - Consider a shallower plan (e.g. 1–2 layers instead of 3) and compute new `distill_conf` for that shallower plan (`post_loop_conf`).
  - **Decisions**:
    - If shallower-plan `post_loop_conf ≥ 85`: run the shallower structural distill.
    - Else or if `post_loop_conf <= pre_loop_conf`: skip structural distill; run only `readability-flag` (and optionally light, non-structural metadata tweaks) and log.
- **Low (<72%)**:
  - Do not run structural distill; only apply `readability-flag` and update frontmatter/flags.

## Documentation and rule updates

- **Pipelines reference** (`3-Resources/Cursor-Skill-Pipelines-Reference.md`):
  - Update the “Confidence gates” sections for each pipeline to reference the 3-band pattern, loop behavior, and early-exit rules instead of purely single thresholds.
  - Add a short **state diagram** (Mermaid) for one representative pipeline (e.g. ingest) showing states: `evaluate → high / mid / low → (loop) → snapshot → destructive step`.
- **Context rules** (`auto-archive.mdc`, `auto-distill.mdc`, `auto-express.mdc`, `auto-organize.mdc`, ingest/para-zettel rules):
  - Insert a compact “Confidence loop” subsection summarizing when that rule attempts a loop, which signal it uses, and what actions are allowed within the loop.
  - Ensure snapshot sections explicitly reference that loops are **pre-snapshot** and non-destructive.
- **Skills** (frontmatter-enrich, subfolder-organize, archive-check, auto-layer-select, express-mini-outline):
  - Where appropriate, document how each skill exposes or contributes to the pipeline’s primary signal (`ingest_conf`, `path_conf`, etc.), without baking full loop logic directly into the skill.
  - Keep loop orchestration at the **pipeline/rule level**, so skills remain reusable and single-purpose.

## Todos

- **define-loops-rule**: Create a new always-applied rule file (e.g. `.cursor/rules/always/confidence-loops.mdc`) that formalizes the 3-band thresholds, loop invariants (max 1 iteration, decay rule, early exit), shared self-critique template, and generic logging fields.
- **update-pipelines-reference**: Update `Cursor-Skill-Pipelines-Reference.md` with the new confidence band pattern, pipeline-specific signals, loop behaviors, and logging schema, plus a representative Mermaid state diagram.
- **wire-ingest-loop**: Adjust the ingest/autonomous-ingest rules to compute `ingest_conf`, insert the 72–84% classification/path refinement loop, and gate all destructive steps on post-loop ≥85% + successful snapshot.
- **wire-organize-archive-loops**: Update `auto-organize.mdc` and `auto-archive.mdc` to introduce the path and archive-refine loops with neighbor/context checks, and to log loop metadata.
- **wire-express-distill-loops**: Update `auto-express.mdc` and `auto-distill.mdc` with soft-loop and depth-control behavior, ensuring they only adjust outlines/depth when post-loop confidence justifies it.
- **extend-logs-dataview**: Update log format examples and (later) Dataview queries/dashboards to incorporate `loop_`* fields so you can monitor where loops raise or suppress actions over time.

