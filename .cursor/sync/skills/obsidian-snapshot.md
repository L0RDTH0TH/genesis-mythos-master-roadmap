---
name: obsidian-snapshot
description: Creates hashed, flattened per-change and batch snapshots inside the vault before destructive MCP actions, with retention guidance and integrity checks. Used across ingest, distill, archive, express, and organize pipelines as a system-level safety net.
---

# obsidian-snapshot

## When to use

- **Before any major destructive or structural change** in the pipelines:
  - full-autonomous-ingest: before `obsidian_split_atomic`, `obsidian_distill_note` (when rewriting), `obsidian_append_to_hub` (cross-note writes), `obsidian_move_note`, `obsidian_rename_note`, `obsidian_delete_note`.
  - autonomous-distill: before the first structural rewrite (e.g. distill layers / `layer-promote` / heavy `obsidian_update_note`).
  - autonomous-archive: after `archive-check` recommends archive (confidence ≥85%) but **before** `subfolder-organize` / `summary-preserve` / archive `move_note`.
  - autonomous-express: before large appends (e.g. `related-content-pull`, `express-mini-outline`, `call-to-action-append`), in addition to the narrative `version-snapshot` skill.
  - autonomous-organize: before `obsidian_rename_note` and before `obsidian_move_note` when confidence ≥85% for each.
- **Before batch sweeps** (e.g. ingesting 5+ notes, archive passes) to create summary checkpoints.

## Snapshot directory and naming

- Use vault-internal snapshot roots configured via MCP env:
  - `SNAPSHOT_DIR` → typically `/home/darth/Documents/Second-Brain/Backups/Per-Change`.
  - `BATCH_SNAPSHOT_DIR` → typically `/home/darth/Documents/Second-Brain/Backups/Batch`.
- **Do not mirror full folder trees**; instead, flatten to avoid deep, fragile directory structures:
  - Let `note_path` be the vault-relative path (e.g. `1-Projects/Project-X/2026-02-25-report.md`).
  - Build a **safe slug** from the filename (e.g. `2026-02-25-report`).
  - Compute a short, deterministic hash of the original path (e.g. first 8 chars of SHA256: `ab12cd34`).
  - Include a timestamp (`YYYYMMDD-HHMMSS`).
  - Per-change snapshot path pattern:
    - `SNAPSHOT_DIR/<slug>--<hash>--<timestamp>.md.bak`
- Each snapshot file MUST include frontmatter with at least:
  - `original_path` — vault-relative path to the source note.
  - `original_title` — title or filename of the note.
  - `pipeline` — ingest / distill / archive / express.
  - `snapshot_type` — `per-change` or `batch`.
  - `snapshot_created` — ISO timestamp.
  - `snapshot_hash` — content hash for integrity (see below).
  - `confidence` — numeric confidence used when deciding the destructive action.
  - `flag` — `none` or `#review-needed + reason`.
  - `immutable: true`, `para-type: Archive`, `status: frozen`.

## Per-change snapshots (`type: "per-change"`)

1. **Read the note**
   - Use `obsidian_read_note(path)` to get full content (including frontmatter, highlights, structure).

2. **Build snapshot path (flattened)**
   - Derive `slug` from filename (no slashes; safe characters only).
   - Compute a short hash from `note_path` (e.g. SHA256 truncated).
   - Get a timestamp string `YYYYMMDD-HHMMSS`.
   - Build `snapshot_path = SNAPSHOT_DIR + "/" + slug + "--" + hash + "--" + timestamp + ".md.bak"`.

3. **Compute integrity hash**
   - Compute `snapshot_hash` from the note content (e.g. SHA256 or MD5 of full text).
   - Store this in the snapshot frontmatter (`snapshot_hash`).

4. **Write immutable snapshot**
   - If needed, call `obsidian_ensure_structure` for the `SNAPSHOT_DIR` parent path (depending on MCP behavior).
   - Use `obsidian_update_note(path: snapshot_path, content: full_note_with_updated_frontmatter, mode: overwrite)` to create the snapshot.
   - The snapshot MUST never be modified by later skills; treat it as append-only history.

5. **Log snapshot**
   - Append an entry to `3-Resources/Backup-Log.md` capturing:
     - Timestamp, `type: per-change`, `note: <original_path>`, `snapshot: <snapshot_path>`, `pipeline`, `confidence`, and optional `flag`.
   - Include a short reason if the snapshot was taken due to anomaly handling or special conditions.

6. **Anomalies and failures**
   - Before writing, verify:
     - `note_path` is inside the configured vault root.
     - `SNAPSHOT_DIR` is not under `Ingest/` or other rule globs to avoid recursive processing.
   - If `SNAPSHOT_DIR` is misconfigured, `obsidian_update_note` fails, or hashing cannot be computed:
     - Log a `#review-needed` entry in `Backup-Log.md` with the error.
     - **Do not perform** the pending destructive action for that note; skip it and continue with the next note in the batch.

## Batch snapshots (`type: "batch"`)

1. **Caller responsibility**
   - The pipeline calling this skill passes a small list of `{ note_path, snapshot_path }` pairs (per-change snapshots already created).

2. **Create batch checkpoint**
   - Construct a batch filename under `BATCH_SNAPSHOT_DIR`, e.g.:
     - `BATCH_SNAPSHOT_DIR/2026-02-25T001200Z-batch-0003.md`.
   - Content should be a markdown summary including:
     - Batch timestamp.
     - Pipeline name and run context (e.g. `INGEST MODE – safe batch autopilot`).
     - Table or list of original notes and their snapshot paths (with confidence ranges).

3. **Log batch**
   - Append an entry to `Backup-Log.md` noting the batch path and the number of notes included.

4. **Frequency**
   - Ingest: every 5 processed notes (or configured batch size).
   - Distill: approximately every 3 notes in a focused run.
   - Archive: once per archive sweep.
   - Express: once per larger express session if desired; per-change snapshots alone are typically sufficient for single-note express.

## Retention and snapshot sweep

- Retention knobs (documented; actual enforcement is via a separate snapshot-sweep rule, not here):
  - `SNAPSHOT_MAX_DAYS` (e.g. keep last 30 days of per-change snapshots).
  - `SNAPSHOT_MAX_PER_NOTE` (e.g. keep last 100 snapshots per `original_path`).
- A dedicated context rule (e.g. `snapshot-sweep.mdc`) should:
  - Be **trigger-based** (phrases like “SNAPSHOT SWEEP” or “clean old snapshots”).
  - Move older snapshots into `Backups/Archives/` by default, not delete them outright.
  - Log all moves and any manual deletion recommendations to `Backup-Log.md` with `#review-needed`.
- This skill itself does **not** delete snapshots; it only creates them and logs metadata.

## Integrity and restore checks

- Each snapshot carries a `snapshot_hash`.
- During restore (see `auto-restore.mdc` rule):
  - Recompute the hash of the snapshot content.
  - If `snapshot_hash` does not match:
    - Treat the snapshot as compromised.
    - Abort restore from that snapshot.
    - Log `#review-needed` with reason in `Backup-Log.md` and recommend falling back to external `BACKUP_DIR` backups.

## MCP tools

- `obsidian_read_note` — read full note content and frontmatter.
- `obsidian_update_note` — write snapshot files (per-change and batch) using `mode: overwrite`.
- `obsidian_ensure_structure` — ensure `SNAPSHOT_DIR` / `BATCH_SNAPSHOT_DIR` parents exist when the server does not create parent directories automatically.

## Confidence gate

- Run per-change snapshots whenever the destructive action is allowed:
  - **≥85%** confidence for moves, renames, deletes, and large overwrites.
- If confidence is below this threshold:
  - Skip the destructive action entirely, log `#review-needed`, and do **not** snapshot (no state change).

## External backups

In-vault snapshots (`SNAPSHOT_DIR`, `BATCH_SNAPSHOT_DIR`) should be included in external backups (rsync, restic, Obsidian Local Backup, etc.) for full point-in-time recovery. Paths are exposed in `~/.cursor/mcp.json`; see `3-Resources/enhanced-snapshots.md` and the always-applied MCP rule (`mcp-obsidian-integration.mdc`) for guidance and tool suggestions.

---
name: obsidian-snapshot
description: Creates hashed, flattened per-change and batch snapshots inside the vault before destructive MCP actions, with retention guidance and integrity checks. Used across ingest, distill, archive, and express pipelines as a system-level safety net.
---

# obsidian-snapshot

## When to use

- **Before any major destructive or structural change** in the four pipelines:
  - full-autonomous-ingest: before `obsidian_split_atomic`, `obsidian_distill_note` (when rewriting), `obsidian_append_to_hub` (cross-note writes), `obsidian_move_note`, `obsidian_rename_note`, `obsidian_delete_note`.
  - autonomous-distill: before the first structural rewrite (e.g. distill layers / `layer-promote` / heavy `obsidian_update_note`).
  - autonomous-archive: after `archive-check` recommends archive (confidence ≥85%) but **before** `subfolder-organize` / `summary-preserve` / archive `move_note`.
  - autonomous-express: before large appends (e.g. `related-content-pull`, `express-mini-outline`, `call-to-action-append`), in addition to the narrative `version-snapshot` skill.
- **Before batch sweeps** (e.g. ingesting 5+ notes, archive passes) to create summary checkpoints.

## Snapshot directory and naming

- Use vault-internal snapshot roots configured via MCP env:
  - `SNAPSHOT_DIR` → typically `/home/darth/Documents/Second-Brain/Backups/Per-Change`.
  - `BATCH_SNAPSHOT_DIR` → typically `/home/darth/Documents/Second-Brain/Backups/Batch`.
- **Do not mirror full folder trees**; instead, flatten to avoid deep, fragile directory structures:
  - Let `note_path` be the vault-relative path (e.g. `1-Projects/Project-X/2026-02-25-report.md`).
  - Build a **safe slug** from the filename (e.g. `2026-02-25-report`).
  - Compute a short, deterministic hash of the original path (e.g. first 8 chars of SHA256: `ab12cd34`).
  - Include a timestamp (`YYYYMMDD-HHMMSS`).
  - Per-change snapshot path pattern:
    - `SNAPSHOT_DIR/<slug>--<hash>--<timestamp>.md.bak`
- Each snapshot file MUST include frontmatter with at least:
  - `original_path` — vault-relative path to the source note.
  - `original_title` — title or filename of the note.
  - `pipeline` — ingest / distill / archive / express.
  - `snapshot_type` — `per-change` or `batch`.
  - `snapshot_created` — ISO timestamp.
  - `snapshot_hash` — content hash for integrity (see below).
  - `confidence` — numeric confidence used when deciding the destructive action.
  - `flag` — `none` or `#review-needed + reason`.
  - `immutable: true`, `para-type: Archive`, `status: frozen`.

## Per-change snapshots (`type: "per-change"`)

1. **Read the note**
   - Use `obsidian_read_note(path)` to get full content (including frontmatter, highlights, structure).

2. **Build snapshot path (flattened)**
   - Derive `slug` from filename (no slashes; safe characters only).
   - Compute a short hash from `note_path` (e.g. SHA256 truncated).
   - Get a timestamp string `YYYYMMDD-HHMMSS`.
   - Build `snapshot_path = SNAPSHOT_DIR + "/" + slug + "--" + hash + "--" + timestamp + ".md.bak"`.

3. **Compute integrity hash**
   - Compute `snapshot_hash` from the note content (e.g. SHA256 or MD5 of full text).
   - Store this in the snapshot frontmatter (`snapshot_hash`).

4. **Write immutable snapshot**
   - If needed, call `obsidian_ensure_structure` for the `SNAPSHOT_DIR` parent path (depending on MCP behavior).
   - Use `obsidian_update_note(path: snapshot_path, content: full_note_with_updated_frontmatter, mode: overwrite)` to create the snapshot.
   - The snapshot MUST never be modified by later skills; treat it as append-only history.

5. **Log snapshot**
   - Append an entry to `3-Resources/Backup-Log.md` capturing:
     - Timestamp, `type: per-change`, `note: <original_path>`, `snapshot: <snapshot_path>`, `pipeline`, `confidence`, and optional `flag`.
   - Include a short reason if the snapshot was taken due to anomaly handling or special conditions.

6. **Anomalies and failures**
   - Before writing, verify:
     - `note_path` is inside the configured vault root.
     - `SNAPSHOT_DIR` is not under `Ingest/` or other rule globs to avoid recursive processing.
   - If `SNAPSHOT_DIR` is misconfigured, `obsidian_update_note` fails, or hashing cannot be computed:
     - Log a `#review-needed` entry in `Backup-Log.md` with the error.
     - **Do not perform** the pending destructive action for that note; skip it and continue with the next note in the batch.

## Batch snapshots (`type: "batch"`)

1. **Caller responsibility**
   - The pipeline calling this skill passes a small list of `{ note_path, snapshot_path }` pairs (per-change snapshots already created).

2. **Create batch checkpoint**
   - Construct a batch filename under `BATCH_SNAPSHOT_DIR`, e.g.:
     - `BATCH_SNAPSHOT_DIR/2026-02-25T001200Z-batch-0003.md`.
   - Content should be a markdown summary including:
     - Batch timestamp.
     - Pipeline name and run context (e.g. `INGEST MODE – safe batch autopilot`).
     - Table or list of original notes and their snapshot paths (with confidence ranges).

3. **Log batch**
   - Append an entry to `Backup-Log.md` noting the batch path and the number of notes included.

4. **Frequency**
   - Ingest: every 5 processed notes (or configured batch size).
   - Distill: approximately every 3 notes in a focused run.
   - Archive: once per archive sweep.
   - Express: optional; usually per-change snapshots + `version-snapshot` are sufficient.

## Retention and snapshot sweep

- Retention knobs (documented; actual enforcement is via a separate snapshot-sweep rule, not here):
  - `SNAPSHOT_MAX_DAYS` (e.g. keep last 30 days of per-change snapshots).
  - `SNAPSHOT_MAX_PER_NOTE` (e.g. keep last 100 snapshots per `original_path`).
- A dedicated context rule (e.g. `snapshot-sweep.mdc`) should:
  - Be **trigger-based** (phrases like "SNAPSHOT SWEEP" or "clean old snapshots").
  - Move older snapshots into `Backups/Archives/` by default, not delete them outright.
  - Log all moves and any manual deletion recommendations to `Backup-Log.md` with `#review-needed`.
- This skill itself does **not** delete snapshots; it only creates them and logs metadata.

## Integrity and restore checks

- Each snapshot carries a `snapshot_hash`.
- During restore (see `auto-restore.mdc` rule):
  - Recompute the hash of the snapshot content.
  - If `snapshot_hash` does not match:
    - Treat the snapshot as compromised.
    - Abort restore from that snapshot.
    - Log `#review-needed` with reason in `Backup-Log.md` and recommend falling back to external `BACKUP_DIR` backups.

## MCP tools

- `obsidian_read_note` — read full note content and frontmatter.
- `obsidian_update_note` — write snapshot files (per-change and batch) using `mode: overwrite`.
- `obsidian_ensure_structure` — ensure `SNAPSHOT_DIR` / `BATCH_SNAPSHOT_DIR` parents exist when the server does not create parent directories automatically.

## Confidence gate

- Run per-change snapshots whenever the destructive action is allowed:
  - **≥85%** confidence for moves, renames, deletes, and large overwrites.
- If confidence is below this threshold:
  - Skip the destructive action entirely, log `#review-needed`, and do **not** snapshot (no state change).
