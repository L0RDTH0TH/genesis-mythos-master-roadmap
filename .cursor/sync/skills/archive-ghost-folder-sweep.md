---
name: archive-ghost-folder-sweep
description: Remove empty ancestor folders of moved notes post-archive via obsidian_remove_empty_folder (MCP only). Used after log_action in autonomous-archive when moved_notes_list non-empty.
---

# archive-ghost-folder-sweep

## When to use

- **After** all moves and log_action in an archive run, when at least one note was moved (pipeline context provides moved_notes_list).
- Optional: queue mode ARCHIVE-GHOST-SWEEP (Queue-Sources.md) for manual triggers later.

## Inputs

- **moved_notes_list** (required): array of original source paths of notes successfully moved. No log parsing—agent passes from run context.
- **dry_run** (default true): passed through to obsidian_remove_empty_folder.

## Algorithm

1. obsidian_ensure_backup (max_age_minutes: 1440).
2. Compute candidates: for each path, parents to PARA root; unique set; sort deepest-first.
3. Pull archive.folder_blacklist from Second-Brain-Config (default: ["/Templates/", "/.technical/", "/Backups/"] + PARA roots). Skip blacklisted candidates.
4. If len(candidates) > 5 → obsidian-snapshot (batch), log to Backup-Log.md.
5. Loop over candidates: obsidian_remove_empty_folder(folder_path, dry_run: true) → review → commit (dry_run: false). No shell rmdir.
6. Log to Archive-Log.md (timestamp, pipeline: archive, actions, confidence, snapshot_path, flag: #ghost-sweep); on failure to Errors.md.

## Confidence bands (confidence-loops)

- High ≥85%: commit after ensure_backup/snapshot.
- Mid 68–84%: preview in Archive-Log + #review-needed + one loop; commit if post_loop_conf ≥85%.
- Low <68%: propose only.

## MCP tools

- obsidian_ensure_backup, obsidian_create_backup
- obsidian_list_notes (verify empty when needed)
- obsidian_remove_empty_folder (folder_path, dry_run; recursive: false)
- obsidian-snapshot (batch when candidates > 5)
