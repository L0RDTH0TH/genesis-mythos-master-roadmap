---
title: Enhanced Snapshots and Restore Safety
created: 2026-02-25
para-type: Resource
status: active
tags: [snapshots, backups, safety, cursor, obsidian, pipelines]
---
# Enhanced Snapshots and Restore Safety

This note summarizes the enhanced snapshot and restore architecture layered on top of the existing `obsidian_create_backup` behavior for the Obsidian PARA-Zettel MCP pipelines.

## Layers of protection

- **External backups (`BACKUP_DIR`)**
  - Created by `obsidian_create_backup` at the start of pipelines.
  - Stored outside the vault (e.g. `/home/darth/Documents/Second-Brain-oops-Backups`).
  - Recommended: keep this directory on encrypted or otherwise protected storage if the vault is synced or shared.

- **In-vault per-change snapshots (`SNAPSHOT_DIR`)**
  - Created by the `obsidian-snapshot` skill (and future `obsidian_snapshot` MCP tool).
  - Flattened naming: `Backups/Per-Change/<slug>--<short-path-hash>--<timestamp>.md.bak`.
  - Each snapshot stores frontmatter:
    - `original_path`, `original_title`, `pipeline`, `snapshot_type`, `snapshot_created`, `snapshot_hash`, `confidence`, `flag`, `immutable: true`, `para-type: Archive`, `status: frozen`.

- **Batch checkpoints (`BATCH_SNAPSHOT_DIR`)**
  - Summarize multiple per-change snapshots per run (e.g. every 5 ingest notes).
  - Include markdown tables linking original notes to snapshot paths and confidence ranges.

- **Restore hub and logs**
  - `3-Resources/Backup-Log.md` — human-facing index of snapshot, backup, and restore events.
  - `3-Resources/Restore Hub.md` — UI for recent snapshots, failures, storage health, and restore checklist.

## Integrate snapshots into external backups

**External backups** (e.g. rsync, restic, Obsidian Local Backup) **SHOULD** include `SNAPSHOT_DIR` and `BATCH_SNAPSHOT_DIR` for full point-in-time recovery. Paths are exposed in `~/.cursor/mcp.json` under the Obsidian MCP server `env`; backup scripts can read the same values to include these directories in vault-wide backups. If using naive full backups, consider **incremental or deduplicating** tools (e.g. restic, Borg, rclone with versioning) so repeated snapshot runs do not bloat storage. See also [[enhanced-snapshots]] for a short reference.

## Example snapshot behavior (skill-level)

High-level pseudocode for per-change snapshots (see `.cursor/skills/obsidian-snapshot/SKILL.md` for instructions):

```text
1. Read note content via obsidian_read_note(path).
2. Build flattened snapshot path under SNAPSHOT_DIR:
   - slug = safe filename
   - hash = short hash of original path
   - timestamp = YYYYMMDD-HHMMSS
   - snapshot_path = SNAPSHOT_DIR/slug--hash--timestamp.md.bak
3. Compute snapshot_hash from the note content and inject into snapshot frontmatter
   along with original_path, pipeline, snapshot_type, etc.
4. Ensure SNAPSHOT_DIR exists (obsidian_ensure_structure with folder_path if needed) and write
   the snapshot with obsidian_update_note(path: snapshot_path, mode: overwrite).
5. Append a concise line to Backup-Log.md linking original note and snapshot path.
6. If anything fails, log #review-needed and skip the destructive action for this note.
```

Batch snapshots follow a similar pattern but summarize multiple `{note_path, snapshot_path}` pairs in a single markdown file under `Backups/Batch/`.

## Rule integrations (overview)

- **Always-applied rule (`mcp-obsidian-integration.mdc`)**
  - Documents `BACKUP_DIR`, `SNAPSHOT_DIR`, and `BATCH_SNAPSHOT_DIR`.
  - Requires calling `obsidian-snapshot` before destructive MCP calls when confidence ≥85%.
  - On snapshot failure, destructive actions are skipped and `#review-needed` is logged.

- **Ingest rule (`para-zettel-autopilot.mdc`)**
  - Preserves: one-note-at-a-time processing, up to 5 notes per batch, continue-on-failure.
  - Adds:
    - Per-change snapshots before `split_atomic`, `distill_note` (rewrite), `append_to_hub`, `move_note`, and `rename_note`.
    - Batch checkpoints every 5 notes, logged in both `Ingest-Log.md` and `Backup-Log.md`.
    - Explicit exclusion of `Backups/` from ingest processing.

- **Restore rule (`auto-restore.mdc`)**
  - Trigger-based RESTORE MODE flow with integrity checks (recompute `snapshot_hash`).
  - Presents candidate snapshots, verifies hashes, then overwrites original notes and logs restores.

- **Snapshot sweep rule (`snapshot-sweep.mdc`)**
  - Trigger-based retention helper (e.g. “SNAPSHOT SWEEP – apply retention”).
  - Moves aged/excess snapshots into `Backups/Archives/` and logs; only deletes when explicitly requested.

## Performance notes (for future benchmarking)

When you benchmark this system, consider capturing:

| Pipeline   | Batch size | Snapshots enabled | Avg time/note (s) | Overhead vs baseline |
|-----------|------------|-------------------|--------------------|----------------------|
| Ingest    | 5          | yes (per + batch) |                    |                      |
| Distill   | 5          | per-change only   |                    |                      |
| Archive   | 5          | per-change only   |                    |                      |
| Express   | 5          | per-change + version-snapshot |         |                      |

- If overhead exceeds ~10–15% in practice:
  - You can reduce batch checkpoint frequency (e.g. every 10 notes instead of 5).
  - Or, for short runs, snapshot only before the first destructive step instead of every small write, while still keeping `obsidian_create_backup` in place.

## Where to look next

- `.cursor/skills/obsidian-snapshot/SKILL.md` — skill-level instructions and details on hashing, flattening, and retention.
- `3-Resources/obsidian_snapshot_TOOL.md` — conceptual MCP tool spec for a future native `obsidian_snapshot` implementation.
- `.cursor/rules/context/auto-restore.mdc` — RESTORE MODE behavior.
- `.cursor/rules/context/snapshot-sweep.mdc` — trigger-based retention helper.

## Review Needed
Proposed para-type: resource. Assigned based on content/frontmatter (confidence ~70%). Do not move until reviewed.