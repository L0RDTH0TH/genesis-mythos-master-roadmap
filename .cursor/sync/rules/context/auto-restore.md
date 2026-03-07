---
description: Trigger-based restore rule for rolling back notes from in-vault snapshots created by obsidian-snapshot, with integrity checks and explicit user choice.
globs: "*"
---

# Auto-restore (RESTORE MODE)

When the user explicitly requests a restore, e.g. with prompts like:

- **"RESTORE MODE – rollback last change"**
- **"RESTORE MODE – rollback last change to [[Note Title]]"**
- **"restore from snapshot"** or similar phrasing,

follow this restore flow:

1. **Scope and discovery**
   - Identify the target note from the prompt (explicit path/link if provided; otherwise the currently open note).
   - Read `3-Resources/Restore Hub.md` and `3-Resources/Backup-Log.md` to discover recent snapshots related to that note:
     - Prefer per-change snapshots in `Backups/Per-Change/` whose frontmatter `original_path` matches the target note.
     - Optionally include recent batch checkpoints in `Backups/Batch/` for additional context.

2. **Present candidate snapshots**
   - List a small set (e.g. last 3–5) of candidate snapshots with:
     - Snapshot path, timestamp (`snapshot_created`), pipeline, and confidence.
   - Ask the user (via Cursor prompt) which snapshot to restore from, or whether to cancel.

3. **Integrity check**
   - For the chosen snapshot:
     - Read the snapshot via `obsidian_read_note(snapshot_path)`.
     - Recompute the content hash and compare to the stored `snapshot_hash` in frontmatter.
   - If hashes do not match:
     - Do **not** restore from this snapshot.
     - Log an entry in `3-Resources/Backup-Log.md` with `#review-needed` and reason (e.g. `snapshot_hash mismatch`).
     - Recommend falling back to external backups in `BACKUP_DIR`.

4. **Apply restore**
   - If integrity passes:
     - Overwrite the original note at `original_path` using `obsidian_update_note(path: original_path, content: snapshot_content, mode: overwrite)`.
     - Add or update frontmatter fields on the restored note:
       - `restored_from_snapshot: <snapshot_path>`
       - `restored_at: <ISO timestamp>`
     - Append a restore entry to `3-Resources/Backup-Log.md` noting the original path, snapshot path, and outcome.

5. **Safety notes**
   - Never delete snapshot files as part of restore; they remain part of the history.
   - Do not auto-restore or run this rule without a clear, user-triggered request.
   - Do not process notes under `Backups/` themselves; this rule only reads from snapshot notes and writes back to non-Backups paths.

---
description: Trigger-based restore rule for rolling back notes from in-vault snapshots created by obsidian-snapshot, with integrity checks and explicit user choice.
globs: "*"
---

# Auto-restore (RESTORE MODE)

When the user explicitly requests a restore, e.g. with prompts like:

- **"RESTORE MODE – rollback last change"**
- **"RESTORE MODE – rollback last change to [[Note Title]]"**
- **"restore from snapshot"** or similar phrasing,

follow this restore flow:

1. **Scope and discovery**
   - Identify the target note from the prompt (explicit path/link if provided; otherwise the currently open note).
   - Read `3-Resources/Restore Hub.md` and `3-Resources/Backup-Log.md` to discover recent snapshots related to that note:
     - Prefer per-change snapshots in `Backups/Per-Change/` whose frontmatter `original_path` matches the target note.
     - Optionally include recent batch checkpoints in `Backups/Batch/` for additional context.

2. **Present candidate snapshots**
   - List a small set (e.g. last 3–5) of candidate snapshots with:
     - Snapshot path, timestamp (`snapshot_created`), pipeline, and confidence.
   - Ask the user (via Cursor prompt) which snapshot to restore from, or whether to cancel.

3. **Integrity check**
   - For the chosen snapshot:
     - Read the snapshot via `obsidian_read_note(snapshot_path)`.
     - Recompute the content hash and compare to the stored `snapshot_hash` in frontmatter.
   - If hashes do not match:
     - Do **not** restore from this snapshot.
     - Log an entry in `3-Resources/Backup-Log.md` with `#review-needed` and reason (e.g. `snapshot_hash mismatch`).
     - Recommend falling back to external backups in `BACKUP_DIR`.

4. **Apply restore**
   - If integrity passes:
     - Overwrite the original note at `original_path` using `obsidian_update_note(path: original_path, content: snapshot_content, mode: overwrite)`.
     - Add or update frontmatter fields on the restored note:
       - `restored_from_snapshot: <snapshot_path>`
       - `restored_at: <ISO timestamp>`
     - Append a restore entry to `3-Resources/Backup-Log.md` noting the original path, snapshot path, and outcome.

5. **Safety notes**
   - Never delete snapshot files as part of restore; they remain part of the history.
   - Do not auto-restore or run this rule without a clear, user-triggered request.
   - Do not process notes under `Backups/` themselves; this rule only reads from snapshot notes and writes back to non-Backups paths.
