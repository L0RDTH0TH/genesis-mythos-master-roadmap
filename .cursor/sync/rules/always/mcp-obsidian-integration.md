---
description: MCP Obsidian integration — tool chaining, logging, safety, and fallbacks
globs: "*"
alwaysApply: true
---

# MCP Obsidian integration

## Canonical folder names (this vault only)

**Never use** the legacy/alternate names below. This vault uses only:

| Use (correct) | Never use |
|---------------|-----------|
**BLACKLIST — never use or reference:** `00 Inbox`, `10 Zettelkasten`, `99 Attachments`, `99 Templates`. Do not create or propose any new PARA or folder patterns.

| **Ingest** | 00 Inbox |
| **Templates** | 99 Templates |
| **5-Attachments** or **Attach** | 99 Attachments |
| *(no such folder)* | 10 Zettelkasten — use PARA roots and subfolders only |

All path proposals, `obsidian_ensure_structure`, `obsidian_refactor_to_zettel`, classify/subfolder outputs, and logs must use only: **Ingest**, **Templates**, **5-Attachments** (or **Attach**), and **1-Projects**, **2-Areas**, **3-Resources**, **4-Archives**. See [[3-Resources/Second-Brain/Vault-Layout]].

---

- Use **obsidian-mcp-server** from **global config only** (`~/.cursor/mcp.json`); do not use project-level setup scripts.
- **Ingest processing**: Follow para-zettel-autopilot; chain MCP tools: **obsidian_create_backup** (first), then `obsidian_classify_para`, `obsidian_split_atomic`, `obsidian_distill_note`, `obsidian_append_to_hub`, `obsidian_move_note`, `obsidian_log_action`; verify after each step. For destructive steps, also call the **obsidian-snapshot** skill (see `.cursor/skills/obsidian-snapshot/SKILL.md`) to create a per-change snapshot before proceeding. **Non-markdown in Ingest:** handle per ingest-processing and non-markdown-handling rules; create companion .md then attempt move of original to 5-Attachments/[subtype]/ via obsidian_ensure_structure + obsidian_create_backup + obsidian_move_note (backup required first; on success omit #needs-manual-move; on failure leave in Ingest/ with #needs-manual-move and log). Exception: the optional move-attachment-to-99 skill may run `mv` only for Ingest → 5-Attachments/ when explicitly invoked by the user.
- **Option C – Zero-Manual**: Every ingest starts with a backup; destructive MCP calls use internal ensure_backup gate; never propose cp/mv/rm shell commands except the move-attachment-to-99 skill (narrow exception: Ingest → 5-Attachments/ only, user-invoked); log backup_path(s) from create_backup in Ingest-Log.md. Snapshots add an additional, in-vault safety layer and must never replace external backups.
- **Prompt → action**: read note → `obsidian_read_note`; move → classify then propose path; search → `obsidian_global_search`; list folder → `obsidian_list_notes`; update/append → `obsidian_update_note` / `obsidian_search_replace`; frontmatter/tags → `obsidian_manage_frontmatter` / `obsidian_manage_tags`.
- **Logging**: Append short entries to `mcp-setup-log.md` or `Ingest-Log.md` after MCP calls. Include backup path in the `changes` string or log line when available. Snapshot calls should also be logged to `3-Resources/Backup-Log.md` with original note path, snapshot path, pipeline, confidence, and any `#review-needed` flags.
- **Safety**: Prefer read and propose over delete/overwrite; no hardcoded API keys.

## Snapshot configuration

- The Obsidian MCP server uses three filesystem roots for safety:
  - `BACKUP_DIR` — external, immutable-like backups created by `obsidian_create_backup` (e.g. `/home/darth/Documents/Second-Brain-oops-Backups`). Treat this as the last-resort recovery location and store it on encrypted or otherwise protected storage when the vault is synced or shared.
  - `SNAPSHOT_DIR` — in-vault per-change snapshots for human-visible, Dataview-friendly rollbacks (e.g. `/home/darth/Documents/Second-Brain/Backups/Per-Change`). Files here are append-only and should never be edited by skills or rules.
  - `BATCH_SNAPSHOT_DIR` — in-vault batch checkpoint notes summarizing groups of changes (e.g. `/home/darth/Documents/Second-Brain/Backups/Batch`).
- Always ensure that `SNAPSHOT_DIR` and `BATCH_SNAPSHOT_DIR`:
  - Live **inside the vault** but **outside** any globbed rule scopes like `Ingest/*` to avoid recursive processing.
  - Are not used as working directories for other tools; only snapshot and restore-related logic should touch them.

### Version-snapshot create behavior (2026-02-25 update)

- **`obsidian_update_note` with `mode: "create"`** is used by the version-snapshot skill when writing a **new** version file under `Versions/`. The server **skips the destination backup gate** for this mode (no backup required for the target path, since it does not exist yet). The **source note** is always backed up at pipeline start via `obsidian_create_backup`, and the obsidian-snapshot skill can create a per-change snapshot of the source before any appends; the version file is an additional narrative copy, not a substitute for source backup/snapshot.
- Version paths use timestamped filenames `<original_slug>--<YYYYMMDD-HHMMSS>.md` so each run targets a non-existent path and the create succeeds. If the path already exists, the server fails the create (no overwrite); the skill uses a fresh timestamp per run to avoid collisions.

### Integrate snapshots into external backups

- **External backups** (e.g. rsync, restic, Obsidian Sync, or a local backup plugin) **SHOULD** include `SNAPSHOT_DIR` and `BATCH_SNAPSHOT_DIR` for full point-in-time recovery. These paths are exposed as environment variables for the Obsidian MCP server in `~/.cursor/mcp.json` (under `obsidian-para-zettel-autopilot` → `env`). Backup scripts or tools can read the same paths from that config to include in vault-wide backups.
- If using naive full backups, consider **incremental or deduplicating** tools (e.g. restic, Borg, rclone with versioning) so that repeated snapshot runs do not bloat backup storage; per-change and batch snapshots accumulate over time.
- See `3-Resources/enhanced-snapshots.md` for a short reference and tool suggestions.

### Batch snapshot threshold

- **batch_size_for_snapshot**: Read from [3-Resources/Second-Brain-Config](3-Resources/Second-Brain-Config.md) (e.g. default 5). When **queue length or batch size > this value**, use **BATCH_SNAPSHOT_DIR** for the run (one batch snapshot for the group). When **≤ this value**, use **per-change** snapshots per note as usual. Fine-tunes overhead: large batches get one batch snapshot; small/mobile single-item runs stay per-change.

### Snapshot chaining guidelines

- Before any destructive MCP call (moves, renames, deletes, or substantial overwrites), the agent should:
  1. Confirm **confidence ≥85%** for the underlying action.
  2. Call the **obsidian-snapshot** skill with `type: "per-change"` for the target note.
  3. If snapshot creation succeeds, proceed with the destructive step.
  4. If snapshot creation fails (misconfigured directories, write failure, integrity issues):
     - Skip the destructive action for that note.
     - Log the error and snapshot failure in `3-Resources/Backup-Log.md` with `#review-needed`.
     - Continue with the next note in the batch.
- **Path before every move**: Before any **`obsidian_move_note`**, call **`obsidian_ensure_structure`**(folder_path: *parent directory of new_path*) so the target path exists (create if missing). This applies to all pipelines (ingest apply-mode, organize, archive, non-md move). Idempotent when the path already exists.
- **Dry-run before every move**: For any **`obsidian_move_note`** at ≥85% confidence, the agent must first call **`obsidian_move_note`**(path, new_path, `dry_run: true`), review returned effects, then call again with `dry_run: false` to commit. No move commit without a prior successful dry_run review.
- **Post-move frontmatter sync**: After every successful **`obsidian_move_note`**(..., `dry_run: false`): (1) If new_path is under a PARA root (1-Projects, 2-Areas, 3-Resources, 4-Archives), set **para-type** on the note at new_path from the first segment (1-Projects→Project, 2-Areas→Area, 3-Resources→Resource, 4-Archives→Archive) via **`obsidian_manage_frontmatter`**. (2) If new_path is under **1-Projects/** and has a second path segment (project folder), set **project-id** to that segment (slugified). (3) If new_path is under **4-Archives/**, set **status** to **archived**. If destination is not under a PARA root (e.g. 5-Attachments), skip all.
- Destructive MCP calls covered by this rule include at least:
  - `obsidian_split_atomic`
  - `obsidian_distill_note` when it rewrites content
  - `obsidian_append_to_hub` when it appends into other notes
  - **task-reroute** (per-change snapshot of **target** note before `append_tasks`)
  - `obsidian_move_note`
  - `obsidian_rename_note`
  - `obsidian_delete_note`

### Security considerations

- Snapshots in `Backups/` are copies of note content. When the vault is synced or published:
  - Prefer to keep `Backups/` and `BACKUP_DIR` on encrypted storage or excluded from any public repos.
  - Do not rely on snapshots as an access-control boundary; treat them as additional history, not as a security feature.

## MCP fallback table

When an MCP call fails due to path or structure issues, use the following behavior:

| Scenario | Action |
|----------|--------|
| **obsidian_move_note** fails (e.g. "parent does not exist" or target directory missing) | Call **obsidian_ensure_structure** with **folder_path** set to the target parent (e.g. `4-Archives/Test-Project-Archive/Subtheme`), then retry **obsidian_move_note**. If ensure_structure is not available or fails, log the error and propose the user create the parent directory manually; do not proceed with move. |
| **obsidian_update_note** to a **new path** fails (e.g. file does not exist and parent dir missing) | For **version-snapshot** (new file under `Versions/`): use `obsidian_update_note(path, content, mode: "create")` so the server skips the destination backup gate. For other new-file cases: use `obsidian_read_note` + `obsidian_update_note(path, content, mode: overwrite)` or `mode: "create"` if the server supports it. If the server does not create parent dirs, call **obsidian_ensure_structure** for the parent path first; otherwise propose creating the parent path manually. |
| **obsidian_create_backup** fails | Abort the pipeline. Do not proceed with any destructive or move operations. Log the failure and flag `#review-needed`. |

Document actual MCP server behavior (e.g. whether parent dirs are created automatically) in this rule or in the pipelines reference when confirmed. When `obsidian_move_note` `dry_run` reports high-risk items (dangling links, overwrite conflicts, missing parents) or the actual move later fails, pipelines may additionally call **`propose_alternative_paths`** (backed by the ranked PARA proposal engine `propose_para_paths` on the MCP server) before retrying, as described in the main rule.

## Documented behavior (verified 2026-02-25)

Deep-nested PARA move behavior verified from MCP server and Obsidian Local REST API plugin code; pipelines and skills rely on the following.

### obsidian_move_note + obsidian_ensure_structure (deep-nested PARA)

| Observation | Result |
|-------------|--------|
| Does `obsidian_move_note` create parent directories automatically? | **No.** The REST API plugin calls `vault.createFolder(dirname(filepath))` once; Obsidian's `createFolder` does not create parent folders recursively. Deep moves (3–4 levels) can fail if intermediate folders are missing. |
| Does `obsidian_ensure_structure` create full path (3–4 levels) in one call? | **Yes (with `folder_path`).** Call `obsidian_ensure_structure` with optional **folder_path** set to the target parent (e.g. `4-Archives/Test-Project-Archive/Subtheme`). The server creates that path recursively with `os.makedirs(..., exist_ok=True)`. Without `folder_path`, only top-level PARA folders are created. |
| If target path already exists (file at `new_path`), what happens? | **Overwrite.** Move is copy-then-delete; PUT overwrites existing file. Backup gate and per-change snapshot (before move) are the safety net; no separate "target exists" check. |
| Already-exists folders when using `obsidian_ensure_structure`? | **Idempotent.** Existing directories are skipped; safe to call multiple times. |
| Case-sensitivity / invalid characters in path? | Paths are used as-is; no normalization. Invalid filesystem characters can cause errors. |

**Required flow for every move:** Backup → (optional) per-change snapshot → **obsidian_ensure_structure**(folder_path: *parent of new_path*) → **obsidian_move_note**(path, new_path, `dry_run: true`) → review effects → **obsidian_move_note**(path, new_path, `dry_run: false`) → **then** set para-type (and when under 1-Projects/ project-id, when under 4-Archives/ status: archived) on the note at new_path (see "Post-move frontmatter sync" above). The ensure_structure step is mandatory so synthetic or non-existent target paths are created before the move.

*Test path used for verification:* `4-Archives/Test-Project-Archive/Subtheme/2026-02-25-archive-test.md` (4 segments).

## Restore-queue mode

**Restore** from snapshots is always **user-triggered**. **restore-queue** mode: user maintains a list (e.g. in Errors.md or a dedicated `3-Resources/Restore-Queue.md`) of snapshot paths to restore. Format: one path per line or a table with columns `snapshot_path`, `original_path` (optional). Processor reads the list and runs restore steps one-by-one: read snapshot content → write to original path (or specified target). No auto-restore; no automatic deletion of snapshots. Document the list format in Logs.md or Backup-Log so users know how to enqueue restores.

