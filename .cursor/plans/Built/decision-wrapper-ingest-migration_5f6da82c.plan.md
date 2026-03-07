---
name: decision-wrapper-ingest-migration
overview: Rework full-autonomous-ingest so that every Ingest run (single or batch) becomes a two-phase, Decision-Wrapper–gated flow where moves/renames only occur after explicit user approval, while still allowing safe in-note distill/metadata steps to run automatically.
todos:
  - id: update-ingest-rule
    content: Rewrite para-zettel-autopilot ingest rule so all initial INGEST runs create/refresh Decision Wrappers and never move/rename notes; only apply-mode ingest (with hard_target_path from wrappers) may move/rename.
    status: completed
  - id: update-pipelines-doc
    content: Align Cursor-Skill-Pipelines-Reference ingest section and diagrams with the new two-phase, Decision-Wrapper–gated ingest behavior.
    status: completed
  - id: adjust-ingest-bootstrap-processing
    content: Update always-ingest-bootstrap and ingest-processing rules to describe Phase 1 ingest as propose-only + wrappers, with relocation deferred to approved decisions.
    status: completed
  - id: refine-queue-processor
    content: Refine auto-eat-queue rule to clearly define how approved Decision Wrappers inject guidance-aware INGEST entries and trigger apply-mode ingest runs.
    status: completed
  - id: sync-backbone-docs
    content: Update supporting Second-Brain docs (Pipelines, Queue-Sources, Logs) and .cursor/sync mirrors to reflect the new ingest flow and maintain backbone-docs-sync invariants.
    status: completed
isProject: false
---

## Goals & Target Behavior

- **Ingest scope only (for now)**: Apply the Decision Wrapper human-in-the-loop pattern to the **full-autonomous-ingest** pipeline; leave ORGANIZE / DISTILL / EXPRESS / ARCHIVE behavior unchanged for now, but design ingest changes so the pattern can be reused later.
- **Moves/renames gated by approval**: No `obsidian_move_note` or `obsidian_rename_note` should run for Ingest notes until a Decision Wrapper under `Ingest/Decisions/` has `approved: true` (plus either `approved_option` or `approved_path`).
- **Safe in-note work still automatic**: For initial ingest runs, continue to run **frontmatter-enrich**, splitting, distill, highlights, next-action extraction, and other non-move steps; only the **final relocation/rename** of the note is held back behind user approval.

## Two-Phase Ingest Design

### Phase 1: Propose-only ingest + wrapper creation

- **Trigger**: `INGEST MODE` via Watcher / EAT-QUEUE or manual ingest commands; initial run on notes under `Ingest/*.md` after `ingest-processing` has handled non-MD and embedded images.
- **Behavior for every Ingest note (regardless of `ingest_conf`)**:
  - Run the existing non-destructive steps from [3-Resources/Second-Brain/Cursor-Skill-Pipelines-Reference.md](3-Resources/Second-Brain/Cursor-Skill-Pipelines-Reference.md): backup, `classify_para`, `frontmatter-enrich`, `name-enhance` (propose only), path proposal via `subfolder-organize`, optional split + `split-link-preserve`, `distill_note`, `distill-highlight-color`, `next-action-extract`, and `task-reroute` / hub appends (per current safety rules).
  - **Do not call** `obsidian_move_note` or `obsidian_rename_note` in this phase, even when `ingest_conf` is high.
  - For each Ingest note, call `obsidian_propose_para_paths` in `wrapper` mode and **create or refresh a Decision Wrapper** in `Ingest/Decisions/` using the template at [Templates/Decision-Wrapper.md](/home/darth/Documents/Second-Brain/Templates/Decision-Wrapper.md):
    - Map up to the top 7 candidate paths into options **A–G** with confidences and reasons.
    - Set wrapper frontmatter: `approved: false`, `decision_candidate: true`, `proposal_path` (wrapper path), `original_note`, `original_path`, `decision_priority`, etc., matching the template.
    - Update the original Ingest note frontmatter with `decision_candidate: true`, `proposal_path: <wrapper_path>`, and priority.
  - Log wrapper creation in `Ingest-Log.md` with a distinct flag (e.g. `#decision-wrapper-created`) and **explicitly stop** ingest processing for that note after wrapper creation.

### Phase 2: Apply run from approved Decision Wrappers

- **Trigger**: User edits wrappers under `Ingest/Decisions/` (check exactly one option and/or set `approved_path`, add reasoning, and set `approved: true`), then runs **EAT-QUEUE** / `INGEST MODE` again.
- **auto-eat-queue + feedback-incorporate handshake**:
  - `auto-eat-queue` uses its existing pre-dispatch logic to **inject queue entries** for wrappers where `decision_candidate: true` and `approved: true` into the in-memory queue.
  - `feedback-incorporate` (see [.cursor/skills/feedback-incorporate/SKILL.md](/home/darth/Documents/Second-Brain/.cursor/skills/feedback-incorporate/SKILL.md)) resolves `approved_option` / `approved_path` into a `**hard_target_path`** and extracts wrapper reasoning as `guidance_text` for the original Ingest note.
  - The resulting queue entry for the original note runs full-autonomous-ingest in **guidance-aware** mode with `hard_target_path` and a `guidance_conf_boost`, but now in **apply** mode.
- **Apply-mode ingest behavior**:
  - Detect that a `hard_target_path` is present (and optionally that this is an ASYNC / decision-apply run) in the ingest context.
  - Skip Decision Wrapper creation for this note and go straight to **snapshot + move/rename**:
    - Reconfirm classification/path using the provided `hard_target_path` plus guidance, but do **not** override the user-chosen path unless there is a hard safety reason (e.g. invalid path).
    - Take per-change snapshots as already defined, then run `obsidian_move_note` (with `dry_run: true` then `dry_run: false`) and, if needed, `obsidian_rename_note` to apply the suggested filename.
  - Update the wrapper (e.g. `used_at`, keep `approved: true`) and logs to record that the decision was executed.

### Flow diagram

```mermaid
flowchart LR
  ingestInit[IngestInitialRun] --> classify[classify_para + frontmatter_enrich]
  classify --> distill[split/distill/next-actions/hub (no move)]
  distill --> wrapper[Create/refreshDecisionWrapper]
  wrapper --> userEdit[Userchecksoption+setsapproved]
  userEdit --> eatQueue[EAT-QUEUEinjectsINGESTentry]
  eatQueue --> applyRun[GuidanceAwareIngestApplyRun]
  applyRun --> moveSnap[Snapshot+dry_runmove/rename]
  moveSnap --> done[NoteinPARAfolder;wrapperlogged]
```



## Concrete Rule & Doc Changes

### 1. Update ingest master rule: `para-zettel-autopilot.mdc`

- In [.cursor/rules/context/para-zettel-autopilot.mdc](/home/darth/Documents/Second-Brain/.cursor/rules/context/para-zettel-autopilot.mdc):
  - **Replace** the current "high (ingest_conf ≥85): silent execute all steps" semantics with the two-phase behavior above: high confidence affects **which options are shown and ordering in the wrapper**, not whether moves auto-execute.
  - Make the **Decision Wrapper branch truly universal** for initial ingest runs (all confidence bands): the pipeline should always end in wrapper creation + stop for Ingest notes that don’t yet have an approved decision.
  - Add an explicit **apply-mode section** describing how the pipeline behaves when invoked with a `hard_target_path` from `feedback-incorporate` (no wrapper creation, only snapshot + move/rename under existing confidence and safety gates).
  - Clarify that **cross-note operations** like `task-reroute` and `append_to_hub` remain governed by their existing confidence and snapshot rules and are still allowed in Phase 1; only the **primary note’s move/rename** is gated by wrapper approval.

### 2. Sync pipeline reference: `Cursor-Skill-Pipelines-Reference.md`

- In [3-Resources/Second-Brain/Cursor-Skill-Pipelines-Reference.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Cursor-Skill-Pipelines-Reference.md):
  - Update the **full-autonomous-ingest** section (table + narrative around lines 143–189) to:
    - Remove mentions of auto-moving at high confidence.
    - Describe Phase 1 as "propose + wrapper" and Phase 2 as "apply from approved Decision Wrapper".
    - Clarify that `ingest_conf` and the mid-band loop now primarily affect **candidate ranking and wrapper priority**, not whether moves are executed immediately.
  - Update the ingest **mermaid flowchart** (currently showing a gate between high and wrapper) so that the Decision Wrapper node is used for all Ingest notes on the first run, with a separate branch showing the apply run from wrappers.
  - Ensure the **Snapshot triggers table** still accurately covers move/rename, but note that these only occur in apply-mode ingest.

### 3. Adjust ingest bootstrap & processing rules

- In [.cursor/rules/always/always-ingest-bootstrap.mdc](/home/darth/Documents/Second-Brain/.cursor/rules/always/always-ingest-bootstrap.mdc):
  - Clarify that "Process Ingest" now means: run `ingest-processing` (non-MD + embedded normalization) → Phase 1 ingest (propose + wrappers, no moves) for all `Ingest/*.md`.
  - Mention that relocation out of `Ingest/` is performed later via approved Decision Wrappers and EAT-QUEUE.
- In [.cursor/rules/context/ingest-processing.mdc](/home/darth/Documents/Second-Brain/.cursor/rules/context/ingest-processing.mdc):
  - Update the final step description (currently "run full-autonomous-ingest on all Ingest/*.md") to note that this run is **propose-only + Decision Wrapper creation**, not an immediate move out of Ingest.

### 4. Refine queue processor rule: `auto-eat-queue.mdc`

- In [.cursor/rules/context/auto-eat-queue.mdc](/home/darth/Documents/Second-Brain/.cursor/rules/context/auto-eat-queue.mdc):
  - In the **pre-dispatch section**, make the Decision Wrapper injection path explicit as the canonical route for ingest moves: wrappers with `approved: true` become INGEST or ASYNC-LOOP entries targeting the original note with `prompt` populated from wrapper reasoning.
  - In step 5–6 (dispatch/run), note that **INGEST MODE entries for Ingest notes without a `hard_target_path` are treated as Phase 1 runs** (no moves/renames; wrappers only), while entries that come from wrappers (with `hard_target_path`) trigger Phase 2 apply runs.
  - Keep the existing safeguards (no destructive pipelines on `Ingest/` paths until INGEST has been run) but clarify that "INGEST has been run" now means Phase 1 + an approved wrapper for that note.

### 5. Update Decision Wrapper template & docs (light touch)

- The existing template at [Templates/Decision-Wrapper.md](/home/darth/Documents/Second-Brain/Templates/Decision-Wrapper.md) is largely compatible; optionally:
  - Add a brief note near the top that **moves/renames only happen after this wrapper has `approved: true` and EAT-QUEUE is run**, so the user understands the workflow.
  - Ensure there is an optional field (e.g. `used_at`) to record when a decision was applied; this can be populated by the apply-mode ingest run.
- In the Second-Brain docs (e.g. [3-Resources/Second-Brain/Pipelines.md], [3-Resources/Second-Brain/Queue-Sources.md], [3-Resources/Second-Brain/Logs.md]):
  - Add a short **"Ingest with Decision Wrappers"** subsection describing the two-phase flow and how it appears in dashboards and Dataview queries.

### 6. Backbone sync: rules → `.cursor/sync/`

- For every modified rule file under `.cursor/rules/` (especially `para-zettel-autopilot.mdc`, `always-ingest-bootstrap.mdc`, `ingest-processing.mdc`, `auto-eat-queue.mdc`):
  - Update the corresponding mirror files under `.cursor/sync/rules/...` per [backbone-docs-sync.mdc](/home/darth/Documents/Second-Brain/.cursor/rules/always/backbone-docs-sync.mdc).
  - Optionally append concise entries to `.cursor/sync/changelog.md` noting the shift to Decision-Wrapper–gated ingest.

## Migration & Testing Strategy

- **No behavior change for other pipelines**: Verify that ORGANIZE / DISTILL / EXPRESS / ARCHIVE rules and docs remain correct; only references to ingest decision flows (e.g. in confidence-loops examples) may need wording tweaks.
- **Incremental rollout**:
  - Start by running the updated ingest flow only on a small subset of Ingest notes (e.g. a test capture batch) and inspect resulting Decision Wrappers under `Ingest/Decisions/`.
  - Approve a few wrappers and run EAT-QUEUE to confirm that apply-mode ingest moves notes into the expected PARA paths and logs are correct (Ingest-Log + Watcher-Result).
- **Dataview/dashboard updates**:
  - Ensure existing Decision Wrapper Dataview queries in the template continue to list pending and recent decisions; extend them if needed to surface `used_at` and whether a decision has been applied.

## Extensibility Stubs for Future Pipelines

- Document, but do not yet implement, that the same two-phase pattern can later be applied to **autonomous-organize** and **autonomous-archive** by:
  - Replacing mid-band auto-move behavior with proposal notes or Decision Wrapper–like structures, plus `approved: true` gates.
  - Reusing the existing `feedback-incorporate` + EAT-QUEUE loop (possibly with different templates) to approve reorganizations and archive moves.
- Keep this future direction briefly noted in [3-Resources/Second-Brain/Pipelines.md] so the ingest implementation can be mirrored without rethinking the contracts.

