---
name: enhanced-snapshots-rollback
overview: Design and integrate multi-layer snapshots, backups, and restore flows for the Obsidian PARA-Zettel MCP pipelines, adding per-change and batch checkpoints plus a Restore Hub while preserving existing backup-first safety.
todos: []
isProject: false
---

# Enhanced Snapshot and Restore Architecture

## High-level goals

- Add a **multi-layer safety net** on top of existing `obsidian_create_backup` so that every destructive action has:
  - A **per-change snapshot** inside the vault (human-visible, Dataview-friendly).
  - A **batch-level checkpoint** summarizing groups of changes.
  - A **clear restore path** via a dedicated Restore Hub note and a restore context rule.
- Keep behavior **deterministic and lightweight**: no fragile magic, no heavy zipping in the critical path, and no infinite feedback loops.
- Align confidence and safety behavior with the existing **≥85% auto-execute** rule for destructive actions, while keeping lower-risk signals flexible.

## Current state (summary)

- **Backups**:
  - Global MCP server `obsidian-para-zettel-autopilot` is configured in `[~/.cursor/mcp.json](~/.cursor/mcp.json)` with `BACKUP_DIR=/home/darth/Documents/Second-Brain-oops-Backups`.
  - Always-applied rule `[mcp-obsidian-integration.mdc](.cursor/rules/always/mcp-obsidian-integration.mdc)` enforces:
    - `obsidian_create_backup` at the start of ingest pipelines.
    - Option C – Zero-Manual (no shell mv/cp/rm; always via MCP, log backup path in `Ingest-Log.md`).
- **Pipelines**:
  - `[para-zettel-autopilot.mdc](.cursor/rules/context/para-zettel-autopilot.mdc)` is the ingest master, already using **≥85%** confidence for auto-actions and batch size up to 5.
  - `[Cursor-Skill-Pipelines-Reference.md](3-Resources/Cursor-Skill-Pipelines-Reference.md)` documents four pipelines and their order.
- **Snapshot-like behavior**:
  - Express pipeline already has a `version-snapshot` skill to write a dated copy into a `Versions/` subfolder for a note, but only for express / major appends.
  - Other pipelines (ingest, distill, archive) rely only on `obsidian_create_backup` (external BACKUP_DIR), not on in-vault snapshots.

## Design decisions

### 1. Snapshot directory layout inside the vault

- **Per-change snapshots**:
  - Create a vault-internal root folder: `Backups/Per-Change/`.
  - For each note at path `REL_PATH` (relative to vault root), per-change snapshot path pattern:
    - `Backups/Per-Change/REL_PATH--YYYYMMDD-HHMMSS.md.bak`
  - Preserve original folder structure by mirroring `REL_PATH` directories where possible, but keep depth ≤4 overall.
- **Batch snapshots / checkpoints**:
  - Create `Backups/Batch/` for lightweight batch notes, not full zips:
    - Each batch checkpoint is a summary note like `Backups/Batch/2026-02-25T001200Z-batch-0003.md`.
    - Content: metadata (timestamp, pipeline name, count of changes) and a table-like markdown list of changed notes and their associated per-change snapshot paths.
- **Logs and hubs**:
  - Continue using `Ingest-Log.md` for ingest summaries.
  - Add a dedicated **backup and restore log** note: `3-Resources/Backup-Log.md` for cross-pipeline snapshot/restore entries.
  - Add a **Restore Hub** note (for example `3-Resources/Restore Hub.md`) that surfaces snapshots and provides human-friendly restore instructions.

### 2. Environment and MCP configuration

- Extend MCP server config in `[~/.cursor/mcp.json](~/.cursor/mcp.json)` for `obsidian-para-zettel-autopilot` with two new environment variables:
  - `SNAPSHOT_DIR="/home/darth/Documents/Second-Brain/Backups/Per-Change"`.
  - `BATCH_SNAPSHOT_DIR="/home/darth/Documents/Second-Brain/Backups/Batch"`.
- Document these variables in `[mcp-obsidian-integration.mdc](.cursor/rules/always/mcp-obsidian-integration.mdc)` under a new **Snapshot configuration** section, clarifying:
  - They point **into the vault** (not the external `BACKUP_DIR`).
  - They are used for human-visible safety layers; `BACKUP_DIR` remains for external, immutable backups created by `obsidian_create_backup`.

### 3. Tool and skill layer

- **New conceptual MCP tool spec**:
  - Add a reference spec note `[3-Resources/obsidian_snapshot_TOOL.md](3-Resources/obsidian_snapshot_TOOL.md)` describing a hypothetical `obsidian_snapshot` tool with:
    - Params: `note_path` (string), `type` ("per-change" or "batch"), `description` (string), and optional `changed_notes` array for batch checkpoints.
    - Behavior for `type="per-change"`:
      - Build a snapshot path under `SNAPSHOT_DIR` mirroring the original path and appending a timestamp suffix.
      - Copy the note content unchanged into the snapshot file (immutable snapshot).
      - Return `snapshot_path` string.
    - Behavior for `type="batch"`:
      - Create a summary markdown file under `BATCH_SNAPSHOT_DIR` listing all changed notes, their per-change snapshots, timestamps, pipeline, and confidence ranges.
      - Return `batch_snapshot_path` string.
    - Logging expectations: examples of how callers should log snapshot paths with `obsidian_log_action` and append entries into `Backup-Log.md`.
  - This spec is **forward-looking**: it defines desired behavior for a native tool implementation, without assuming it already exists.
- **New snapshot skill as an immediate implementation**:
  - Add a project skill `[.cursor/skills/obsidian-snapshot/SKILL.md](.cursor/skills/obsidian-snapshot/SKILL.md)` that implements equivalent behavior **using existing MCP tools**:
    - Uses `obsidian_read_note` and `obsidian_update_note` with `mode: overwrite` to write snapshots into `Backups/Per-Change` and `Backups/Batch`.
    - Follows the same path patterns as the tool spec.
    - Documents how to avoid parent-dir issues (`obsidian_ensure_structure` fallback) and how to log to `Backup-Log.md`.
  - Pipelines and rules will initially call this **skill-level behavior**, not a real MCP tool, so there is no immediate dependency on server changes.

### 4. Confidence thresholds and anomaly checks

- **Unify destructive-action thresholds**:
  - For any step that **moves, renames, deletes, or overwrites substantial content**, standardize on **≥85%** confidence for auto-execution.
  - Non-destructive or additive operations (e.g., readability flags, lightweight highlight additions) may keep slightly lower gates (e.g., 70–80%) as currently documented, but they should still benefit from snapshots when they significantly change note structure.
- **Pre-action anomaly checks** (applied inside the snapshot skill and in updated rules):
  - Verify that `note_path` exists and is inside the configured vault root.
  - Compute the snapshot path and ensure it **does not overwrite** an existing snapshot (always append timestamp; if collision, append a random suffix).
  - Confirm that `SNAPSHOT_DIR` and `BATCH_SNAPSHOT_DIR` are not pointing to `Ingest/` or other globs that rules directly act on (to avoid recursive triggering).
  - If any anomaly is detected (invalid path, missing env, cannot write snapshot):
    - Log an error in `Backup-Log.md` with `#review-needed`.
    - **Skip the destructive step** and let the calling pipeline continue to the next note.

### 5. Idempotency and loop safety

- Ensure snapshots and batch notes are stored in folders that **no existing rule globs match**:
  - Confirm no `.cursor/rules/context/*.mdc` rule uses `Backups/`** in its `globs`.
  - In new rules, explicitly state: "Never process notes under `Backups/` automatically." The Restore pipeline should only be **trigger-based**.
- Make per-change snapshots **append-only**:
  - The snapshot skill never edits an existing snapshot; it only writes new files.
- In Restore flows, explicitly mark **restored notes** in frontmatter (e.g., `restored_from_snapshot: PATH`) so they do not automatically get re-snapshotted in a tight loop without human prompting.

## File-by-file changes

### 1. `~/.cursor/mcp.json` (MCP server config)

- Under the `obsidian-para-zettel-autopilot` server entry, add:
  - `SNAPSHOT_DIR` and `BATCH_SNAPSHOT_DIR` env vars as described above.
- Document in a comment or in `[3-Resources/obsidian_snapshot_TOOL.md](3-Resources/obsidian_snapshot_TOOL.md)` that these directories must exist (or that the server will create them) and should not be used as working directories for other tools.

### 2. `.cursor/rules/always/mcp-obsidian-integration.mdc`

- Add a **Snapshot configuration** section:
  - Explain the relationship between `BACKUP_DIR`, `SNAPSHOT_DIR`, and `BATCH_SNAPSHOT_DIR`.
  - Clarify that `obsidian_create_backup` writes external backups into `BACKUP_DIR` while the snapshot skill writes in-vault copies.
- Extend the tool chaining guidance:
  - Before any destructive MCP call (e.g., `obsidian_split_atomic`, `obsidian_update_note` with overwrite or heavy append, `obsidian_move_note`, `obsidian_rename_note`, `obsidian_delete_note`):
    - Call the snapshot skill (`obsidian-snapshot`) with `type="per-change"` **if** confidence ≥85%.
    - If the confidence is below 85%, do not perform the destructive step; log a `#review-needed` entry instead.
- Update the fallback table to mention snapshot behavior:
  - If `obsidian_create_backup` fails, **abort** as already documented.
  - If snapshot creation fails, skip the destructive step, log to `Backup-Log.md` with `#review-needed`, and continue with the next note.

### 3. `.cursor/rules/context/para-zettel-autopilot.mdc`

- Extend the **Pipeline** description to include snapshot behavior:
  - For ingest runs (`Ingest/*.md`), keep `obsidian_create_backup` at the very start.
  - Before each of the following actions, invoke per-change snapshots (through the snapshot skill):
    - `obsidian_split_atomic` (since it can restructure content across files).
    - `obsidian_distill_note` when it overwrites parts of the note.
    - `obsidian_append_to_hub` and any cross-note append that could cause duplication.
    - `obsidian_move_note` and `obsidian_rename_note`.
  - Emphasize the **one-note-at-a-time** processing plus snapshot: complete `backup → snapshot → change → log_action` for a note before moving to the next.
- Add **batch snapshot logic**:
  - Introduce a conceptual counter: after processing every 5 notes (or configured batch size), invoke a batch checkpoint via the snapshot skill with `type="batch"` and a list of those notes and their per-change snapshots.
  - Log the resulting batch snapshot path into both `Ingest-Log.md` and `Backup-Log.md`.

### 4. Other context rules

- **Distill pipeline rule** (e.g., `auto-distill` rule when created):
  - Document that the pipeline must:
    - Call `obsidian_create_backup` once per run for each note.
    - Call the snapshot skill before multi-step distill/formatting operations (e.g., before running `distill-highlight-color`, `layer-promote`, `callout-tldr-wrap` if they overwrite sections using `obsidian_update_note`).
- **Archive pipeline rule** (e.g., `auto-archiving` rule when present):
  - After `archive-check` passes with ≥85% confidence, but **before** `subfolder-organize` and `summary-preserve`, take a per-change snapshot.
  - Mention that if a later heuristic (e.g., in `archive-check` or `summary-preserve`) detects anomalies, the pipeline may propose a restore from the newest snapshot instead of moving.

### 5. New context rule: `.cursor/rules/context/auto-restore.mdc`

- Add a new context rule file triggered by phrases like:
  - "RESTORE MODE", "rollback last change", "restore from snapshot".
- Content:
  - Scope: Trigger-based only; never runs automatically on save or batch without explicit user intent.
  - Behavior outline:
    - Read `Restore Hub.md` and `Backup-Log.md` to find the most recent per-change or batch snapshots for the target note or timestamp.
    - Present the user with a short list of candidate snapshots (e.g. last N items) with descriptions.
    - When the user explicitly chooses a snapshot (in Cursor prompt), the pipeline uses `obsidian_read_note` on the snapshot path and `obsidian_update_note` to write back into the original note path.
    - Log the restore in `Backup-Log.md` and in the note’s frontmatter (`restored_from_snapshot`, `restored_at`).
  - Safety notes:
    - Never delete snapshots during restore.
    - Do not auto-restore; always require a user-triggered instruction.

## New / updated skills and resources

### 1. `.cursor/skills/obsidian-snapshot/SKILL.md` (new)

- Define **When to use**:
  - Before any major destructive change in ingest, distill, archive, or express pipelines.
- Define **Instructions** for `type="per-change"`:
  - Use `obsidian_read_note(path)` to get full content.
  - Build a `snapshot_path` under `SNAPSHOT_DIR` based on relative note path plus timestamp suffix.
  - Use `obsidian_update_note(path: snapshot_path, content, mode: overwrite)` to create an immutable copy; if parent creation fails, try `obsidian_ensure_structure` (if available) and retry.
  - Append an entry to `Backup-Log.md` recording timestamp, type, original path, `snapshot_path`, pipeline, and confidence.
- Define **Instructions** for `type="batch"`:
  - Accept a list of `{note_path, snapshot_path}` entries from the caller.
  - Write a new markdown file in `BATCH_SNAPSHOT_DIR` summarizing these changes.
  - Append an entry to `Backup-Log.md` referencing this batch.
- Define **Confidence gate and anomaly behavior**:
  - Run snapshots whenever the destructive action is allowed (≥85%), but treat failure to snapshot as a hard stop for that specific action.

### 2. `3-Resources/obsidian_snapshot_TOOL.md` (new)

- Document a future MCP tool that mirrors the snapshot skill behavior, with:
  - Parameter schema (JSON-like snippet) for `note_path`, `type`, `description`, and optional `batch_details`.
  - Pseudocode similar to the user’s suggestion, adapted to vault-relative paths and BACKUP_DIR/SNAPSHOT_DIR separation.
  - Explicit mention that until the tool exists, the `.cursor/skills/obsidian-snapshot` skill provides equivalent effects by orchestrating existing MCP tools.

### 3. `3-Resources/Backup-Log.md` (new)

- Create a log note capturing snapshot and restore events across all pipelines.
- Define a consistent log line format (similar to but focused on backups):
  - Example: `YYYY-MM-DD HH:MM | type: per-change | note: PATH | snapshot: PATH | pipeline: ingest | confidence: 92% | flag: [none or #review-needed + reason]`.
- Include a short **How to restore** section linking to `Restore Hub.md` and describing the manual restore process.

### 4. `3-Resources/Restore Hub.md` (new)

- Purpose: Central UI for humans and Dataview to inspect snapshots.
- Content sections:
  - Explanation of snapshot layers and how they relate to `obsidian_create_backup`.
  - A Dataview block that lists recent snapshot notes in `Backups/Per-Change/` and `Backups/Batch/`.
  - A checklist-style mini-guide for manual restore:
    - Identify snapshot path.
    - Confirm it’s the correct version.
    - Use RESTORE MODE or manually copy content back.

### 5. `3-Resources/2026-02-25-enhanced-snapshots.md` (new)

- Summarize the enhanced snapshot and restore design:
  - State the rationale (oops-prevention, trustworthiness, layered safety).
  - Show small code snippets for:
    - Snapshot skill behavior.
    - Example rule snippet from `mcp-obsidian-integration.mdc` referencing snapshots.
    - Example restore flow.
  - Link to: `Cursor-Skill-Pipelines-Reference.md`, `Restore Hub.md`, and `Backup-Log.md`.

### 6. Minor updates to existing skills

- `**version-snapshot` skill**:
  - Clarify in the SKILL.md that `version-snapshot` is **express-only** and aimed at preserving narrative versions, whereas `obsidian-snapshot` is a **system-level safety net** used across pipelines.
- `**archive-check` skill**:
  - Add a final step in the instructions: if the heuristics detect inconsistencies (e.g., open tasks but `status: complete`), recommend **not archiving** and suggest reviewing recent snapshots instead; include a short note to consult `Restore Hub.md`.

## Pipeline integration details

### Ingest (full-autonomous-ingest)

- Effective sequence per note:
  - `obsidian_create_backup` → classify → frontmatter-enrich → (optional propose-only branches) →
  - **Before split/distill/move/rename**: run `obsidian-snapshot` with `type="per-change"`.
  - Perform the destructive or structural change.
  - Log actions including snapshot paths in both `Ingest-Log.md` and `Backup-Log.md`.
- Every **batch of 5 notes**:
  - Call `obsidian-snapshot` with `type="batch"` summarizing those 5 notes.

### Distill (autonomous-distill)

- For each note to be distilled:
  - `obsidian_create_backup`.
  - `obsidian-snapshot` before the first structural rewrite (e.g., initial distill layer or `layer-promote`).
  - Run `distill-highlight-color`, `layer-promote`, `callout-tldr-wrap`, `readability-flag` as currently specified.
  - Log to `Backup-Log.md` noting any snapshot and the applied skills.

### Archive (autonomous-archive)

- For each candidate note:
  - `obsidian_create_backup`.
  - Run `archive-check`; if confidence <85%, log and stop (no snapshot needed because no destructive action follows).
  - If archiving is recommended:
    - Run `obsidian-snapshot` before `subfolder-organize` / `summary-preserve` / `move_note`.
    - After move, log snapshot and new location.

### Express (autonomous-express)

- Sequence per note:
  - `obsidian_create_backup`.
  - `version-snapshot` (as currently designed) to create a semantic version copy.
  - Optionally also call `obsidian-snapshot` for system-level consistency before heavy append operations.
  - Continue with `related-content-pull`, `express-mini-outline`, `call-to-action-append`.

## Restore flow design

### Conceptual flow

```mermaid
flowchart LR
  user[User says "RESTORE MODE"] --> restoreRule[auto-restore rule]
  restoreRule --> readHub[Read Restore Hub + Backup-Log]
  readHub --> showOptions[Show candidate snapshots]
  showOptions --> userChoice[User picks snapshot]
  userChoice --> applyRestore[Read snapshot, overwrite original note]
  applyRestore --> logRestore[Append restore entry to Backup-Log + frontmatter]
```



- This flow is **explicitly user-driven** to preserve trust.
- The restore rule and Restore Hub provide guidance, but no automatic mass-restore actions are performed without clear prompts.

## Testing and validation plan

- **Sandbox notes**:
  - Create a `Test-Ingest/` folder with 10–15 synthetic notes including:
    - Normal ingest candidates.
    - Notes with invalid paths or missing frontmatter.
    - Low-confidence classification cases.
- **Scenario tests** (manual in the initial iteration):
  - Run `INGEST MODE` on the sandbox and verify:
    - Each destructive change has a corresponding per-change snapshot in `Backups/Per-Change/`.
    - Every 5 notes produces a batch checkpoint in `Backups/Batch/`.
    - `Backup-Log.md` contains well-formatted entries.
  - Trigger RESTORE MODE on one of the test notes and walk through a full restore.
- **Failure mode tests**:
  - Temporarily misconfigure `SNAPSHOT_DIR` (e.g., to a read-only or non-existent path) and verify:
    - Destructive actions are skipped.
    - `Backup-Log.md` and `Ingest-Log.md` get `#review-needed` entries explaining the failure.
- **Performance check**:
  - Roughly time an ingest batch before and after snapshots.
  - If overhead exceeds about 10–15% for typical batches, consider minor optimizations (such as grouping non-critical snapshots or trimming batch checkpoint detail) without removing per-change safety.

## QuickAdd / trigger integration

- Extend existing QuickAdd macros or templates (outside this repo, via Obsidian UI) to add:
  - A command that sends a prompt to Cursor like: `RESTORE MODE – rollback last change to [[Note Title]]`.
  - Optional shortcuts for "Show recent snapshots for this note" that open `Restore Hub.md` and filter Dataview queries.
- Document in `3-Resources/2026-02-25-enhanced-snapshots.md` how to set up these QuickAdd actions.

## Implementation todos

- Define and implement the `obsidian-snapshot` skill, including path rules, anomaly handling, and logging.
- Extend `mcp-obsidian-integration.mdc` and `para-zettel-autopilot.mdc` to integrate per-change snapshots and batch checkpoints before destructive actions.
- Add new resources: `obsidian_snapshot_TOOL.md`, `Backup-Log.md`, `Restore Hub.md`, and `2026-02-25-enhanced-snapshots.md`.
- Create the `auto-restore.mdc` context rule and wire it to RESTORE MODE prompts.
- Update `version-snapshot` and `archive-check` skills with clarifying notes about the new snapshot safety layer.
- Run sandbox ingest, distill, archive, and express tests to validate correctness, failure behavior, and performance.

