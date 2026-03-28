---
name: atomize-subagent-refactor
overview: Extract note atomization (split_atomic + split-link-preserve) from ingest-specific logic into a dedicated ATOMIZE subagent that can be used from ingest and directly on PARA notes.
todos:
  - id: define-behavior
    content: Clarify Atomize subagent responsibilities, triggers, and input/output contract
    status: completed
  - id: add-atomize-rule
    content: Create AtomizeSubagent rule file with pipeline steps (backup, snapshot, split_atomic, split-link-preserve, logging)
    status: completed
  - id: wire-dispatcher
    content: Add ATOMIZE MODE to Queue-Sources, Queue-Alias-Table, and dispatcher routing
    status: completed
  - id: refactor-ingest
    content: Refactor ingest Phase 1 post-process to delegate splitting to Atomize instead of inlining split_atomic
    status: completed
  - id: enable-para-use
    content: Allow ATOMIZE MODE to run on PARA notes directly with appropriate exclusions
    status: completed
  - id: update-safety-logging
    content: Integrate Atomize with confidence-loops, snapshot triggers, logs, and Watcher-Result
    status: completed
  - id: update-docs-sync
    content: Update Pipelines, Rules, and .cursor/sync docs to include Atomize subagent details
    status: completed
isProject: false
---

### Atomize Subagent Refactor Plan

#### 1. Clarify desired behavior and responsibilities

- **Define responsibilities**: Document that the Atomize subagent owns `obsidian_split_atomic` + `split-link-preserve`, plus minimal safety gates (backups, snapshots, confidence handling), but **no moves/renames**.
- **Modes & triggers**:
  - Introduce a new queue mode and manual trigger, e.g. `**ATOMIZE MODE` / `ATOMIZE_MODE`** for stand-alone use on PARA notes.
  - Define how ingest calls it: as a **sub-pipeline step** (e.g. `ingest-post-process` delegates to Atomize for the split stage) rather than inlining split logic.
- **Inputs/outputs**:
  - Inputs: `source_file` path, optional `hard_target_folder` or constraints (probably none initially), and confidence threshold hints.
  - Outputs: list of child note paths, basic telemetry (split happened / skipped, reasons).

#### 2. Add Atomize subagent rule file

- **Create a new agent rule** (mirroring Distill/Express/Organize patterns), e.g. `[.cursor/rules/agents/atomize.mdc]`, with:
  - Subagent description: autonomous-atomize — split multi-idea notes into atomic notes, write `split_from` / `split_into` and parent `## Splits` section; **no moves, renames, or PARA reclassification**.
  - Activation: trigger phrases ("ATOMIZE MODE – safe batch autopilot", "atomize this note"), and queue mode `"ATOMIZE MODE"` dispatched from EAT-QUEUE.
  - Pipeline steps:
    - Backup via `obsidian_create_backup` on the source note.
    - Optional `classify_para` only if needed for confidence or exclusions (respect existing confidence-loops + exclusions rules).
    - Per-change snapshot before `obsidian_split_atomic` when confidence ≥85%.
    - Call `obsidian_split_atomic` with appropriate parameters (same as current ingest usage).
    - Run `split-link-preserve` skill to wire parent/children.
    - Log to an appropriate log (either Ingest-Log or a new Atomize-Log, depending on how you want to track it) and Run-Telemetry.
  - Confidence handling: use `ingest_conf` or a new `atomize_conf` signal; enforce ≥85% for actual split and link writes; otherwise no-op or propose-only.

#### 3. Wire Atomize into Pipelines / dispatcher

- **Pipelines doc** (`3-Resources/Second-Brain/Pipelines.md`):
  - Add Atomize to the Quick Reference table and detailed breakdown: Trigger → `autonomous-atomize` → rule `auto-atomize` / `AtomizeSubagent`.
  - Update ingest flowchart textually to show that the split step is now handled by Atomize subagent or a shared atomize sub-pipeline.
- **Queue-Sources / Queue-Alias-Table**:
  - Add `ATOMIZE MODE` as a recognized mode with param schema (`source_file`, optional scope).
  - Ensure the Queue/Dispatcher subagent dispatches `mode: "ATOMIZE MODE"` to the new Atomize subagent, similar to DISTILL/EXPRESS/ORGANIZE.

#### 4. Refactor ingest to delegate atomization

- **Ingest agent rule** (`.cursor/rules/agents/ingest.mdc`) and associated context rules:
  - Replace direct `obsidian_split_atomic` + `split-link-preserve` steps in Phase 1 post-process with a **call or logical delegation** to the Atomize pipeline (maintaining the same snapshot and confidence gates).
  - Keep ingest-specific constraints (e.g. only split when note is still in `Ingest/` and not a wrapper, respect ingest confidence bands) but move the mechanics of splitting into the new subagent’s responsibilities.
  - Ensure that post-atomize, ingest continues with distill / next-action-extract / task-reroute / append_to_hub unchanged.
- **Sub-pipeline naming**: Optionally document an `atomize-core` sub-pipeline alongside `ingest-core` and `ingest-post-process` in Pipelines.md to make debugging easy.

#### 5. Make Atomize callable from PARA notes

- **Manual triggers**:
  - Document that from any note under 1-Projects/ / 2-Areas/ / 3-Resources/, the user can say "ATOMIZE MODE – safe batch autopilot" or "atomize this note" to run the Atomize pipeline without moving the note.
  - Respect existing exclusions (4-Archives, Backups, Logs, hubs, watcher-protected) as in other pipelines.
- **Queue integration**:
  - Allow prompt-crafter to target `ATOMIZE MODE` as a CODE prompt mode so users can queue atomization runs over sets of notes.

#### 6. Align with confidence, safety, and logging standards

- **Confidence-loops**:
  - Decide whether Atomize uses `ingest_conf` from classify_para or defines `atomize_conf`; in either case, integrate with the shared confidence-loops rule (≥85% for destructive split; 68–84% one refinement loop; <68% propose-only, possibly a Decision Wrapper for manual review).
- **Snapshots & backups**:
  - Ensure Atomize strictly follows snapshot triggers (backup + per-change snapshot before split, no split if snapshot fails).
- **Logs and Watcher-Result**:
  - Decide where to log: reuse Ingest-Log.md or create `Atomize-Log.md`; update `Logs.md` and Run-Telemetry references accordingly.
  - Make sure Watcher-Result lines are appended when Atomize runs via EAT-QUEUE.

#### 7. Update documentation and sync copies

- **Backbone docs**:
  - Update `3-Resources/Second-Brain/Rules.md`, `Cursor-Skill-Pipelines-Reference`, and any distill/ingest-related docs to mention Atomize as a separate subagent.
- **Sync folder**:
  - Add/update the mirrored rule under `.cursor/sync/rules/agents/atomize.md` to match `.cursor/rules/agents/atomize.mdc`.
- **Examples**:
  - Add short usage examples in Pipelines.md and/or README: one for ingest-triggered atomization and one for stand-alone Atomize on a PARA note.

