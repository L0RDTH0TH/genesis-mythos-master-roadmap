---
name: move-attachment-to-99
description: Fallback for moving a non-markdown file from Ingest/ to 5-Attachments/[subtype] when obsidian_move_note does not support binaries. Explicit user invocation only; includes built-in backup before mv. This is the only sanctioned exception to "no shell mv/cp/rm" in the vault (narrow scope: Ingest → 5-Attachments/ only).
---

# move-attachment-to-99

## When to use

- **Only when the user explicitly requests it**, e.g. "Invoke move-attachment for [file]" or "Move attachment X to 5-Attachments". Never auto-trigger. Use when obsidian_move_note has failed for a non-.md file (e.g. server returns "only markdown supported") and the user confirms they want to move the file via this skill.
- After ingest has created a companion .md and the original binary is still in Ingest/ with #needs-manual-move.

## Invocation

- **Explicit user request only.** Do not invoke this skill automatically. When the user asks to move an attachment or run move-attachment for a specific file, proceed with the steps below.

## Inputs

- **source_path** (required): Vault-relative path to the file (e.g. `Ingest/document.pdf`). Must start with `Ingest/`.
- **subtype** (required): One of `PDFs`, `Images`, `Audio`, `Documents`, `Other`. Determines destination folder under 5-Attachments/.

## Validation (before any move)

1. **Source:** Confirm source_path exists, is under the vault, and starts with `Ingest/`. If not, abort and log.
2. **Destination:** Build destination as `5-Attachments/<subtype>/<basename>`. If a file already exists at that path, use a timestamped name: `<basename_stem>_YYYYMMDD_HHMMSS.<ext>` and use that as the final destination.
3. **Scope:** Destination must be exactly under `5-Attachments/` (one of the five subtypes). No other paths are allowed.

## Steps

1. **Backup (required):** Before moving, create a backup of the source file. Prefer `obsidian_create_backup` with paths including the binary path; if the MCP server does not support backing up non-.md files, copy the file to a safe location (e.g. `Ingest/Backups/<basename>.bak` or the external BACKUP_DIR if known) using a single copy operation. Log the backup path. If backup fails, do not proceed with the move.
2. **Ensure structure:** Ensure `5-Attachments/<subtype>/` exists (e.g. via `obsidian_ensure_structure` with folder_path, or by creating the directory if using shell).
3. **Move:** Run a single `mv` command: move source_path to the validated destination path (vault root + destination). Use absolute paths if needed (vault root from workspace or config). No other shell file operations.
4. **Update companion (if any):** If a companion .md exists for this file, update its `source` frontmatter and add the success callout `> [!success] File moved to [[5-Attachments/<subtype>/<final-filename>]].` Remove #needs-manual-move from the companion.
5. **Log:** Append to Ingest-Log.md (or Backup-Log.md) that move-attachment-to-99 was used, with source path, destination path, and backup path.

## Exception to no-shell rule

- This skill is the **only** exception in the Second Brain rules that allows running `mv` (or equivalent) on vault files. It is documented in mcp-obsidian-integration.mdc and non-markdown-handling.mdc. The scope is strictly: source in Ingest/, destination in 5-Attachments/[subtype]/.
- Do not use this skill for any other path or for .md notes (use obsidian_move_note for those).

## Error handling

- If validation fails: do not run mv; report to user and log.
- If backup fails: do not run mv; report and log.
- If mv fails: report the error; the file remains in Ingest/; log with #review-needed.
