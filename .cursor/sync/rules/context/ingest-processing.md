---
description: Ingest folder processing and non-MD handling
globs: "Ingest/**"
alwaysApply: false
---

# Ingest Folder Processing Rule

Applies to: Ingest/**

When any task, chat, or agent session references Ingest/ or new/unprocessed files:

1. **List Ingest**: Use `obsidian_list_notes("Ingest")` for .md; **additionally** list non-.md in Ingest (e.g. workspace glob/list) — MCP may return only notes.
2. **Non-.md**: For each non-.md file, follow non-markdown-handling.mdc: create companion .md (e.g. `YYYY-MM-DD_OriginalName-Summary.md`), place in 1-Projects/2-Areas/3-Resources/4-Archives (default 3-Resources if uncertain; ask user if needed). Non-markdown-handling now **attempts automatic move** of the original to `5-Attachments/[subtype]/` via obsidian_ensure_structure + obsidian_create_backup + obsidian_move_note after creating the companion; if the move or backup fails, behavior falls back to leaving the file in Ingest/ with manual-move callout and #needs-manual-move. Add embeds/links in companion using `![[5-Attachments/PDFs/original.pdf]]` etc. (or the final path after successful auto-move).

### Embedded Attachment Normalization (Images in Ingest/*.md)

After non-.md handling completes, and before running **Phase 1 of full-autonomous-ingest (propose-only + Decision Wrapper, no moves/renames)** on .md files:

1. Scan the note content for image embeds:
   - `![[...png]]`, `![[...jpg]]`, `![[...jpeg]]`, `![[...gif]]`, `![[...webp]]`, `![[...svg]]`, `![[...bmp]]`
   - Also catch common pasted names: "Pasted image", "Screenshot", etc.

2. For every image whose physical file is currently in Ingest/ or vault root:
   - Rewrite the link in the note to `![[5-Attachments/Images/original-filename.ext]]`
   - Collect list of files needing manual move.

   **Optional rename suggestion (user-applied):** Propose moving + renaming images to something more descriptive based on note title/context, e.g. if note title = "Meeting 2026-02-26 Notes" → suggest `Meeting-2026-02-26-screenshot-1.png`. Add a "Bonus" line to the callout (see step 3) encouraging renaming during move for better search.

3. Add this standardized callout at the top of the updated note (after frontmatter):
   ```markdown
   > [!todo] Manual image relocation needed
   > Image embeds have been normalized to point to `5-Attachments/Images/`.
   > Please drag the following file(s) from **Ingest/** (or vault root) to **`5-Attachments/Images/`** using Obsidian's file explorer (or Finder/Files app):
   >
   > - Pasted image 2026-02-26 at 01.23.45.png
   > - screenshot-from-phone.jpg
   >
   > After moving:
   > - Verify embeds still work (preview the note).
   > - Remove the `#needs-attachment-relocation` and `#attachment-relocation-pending` tags from this note.
   > - Optionally commit changes if git-enabled.
   >
   > **Bonus:** Consider renaming during move for better search (e.g., `Meeting-2026-02-26-key-diagram.png` instead of generic pasted name).
   ```

4. Add tags `#needs-attachment-relocation` and `#attachment-relocation-pending` to the note (remove both after manual move). The second tag supports Dataview queries (e.g. `TABLE file.name FROM #attachment-relocation-pending`).

5. Output the full updated .md content for review/apply.

**MCP SAFETY:** Never attempt to move image files. User performs the one-time drag-drop in Obsidian file explorer or Finder (takes <10 seconds per batch).

3. **.md**: After non-MD handling and embedded attachment normalization, run **Phase 1 of full-autonomous-ingest (propose-only + Decision Wrapper, no moves/renames)** on all `Ingest/**/*.md` (excluding `Ingest/Decisions/**` and watcher/control notes) per always-ingest-bootstrap + para-zettel-autopilot (optional bootstrap → backup → classify_para → … → log_action → create/refresh Decision Wrapper for relocation). **Move/rename (with dry_run first, then commit) only occurs later in Phase 2 apply-mode ingest runs triggered by approved Decision Wrappers; dry_run and move safety remain enforced there per mcp-obsidian-integration.mdc.**
4. Report: "Processed X files. Ingest/ now empty/cleared" (or list remaining and why).

**Exclusion — Watcher control note**: Treat `Ingest/watched-file.md` (frontmatter `watcher-protected: true`) as a control note only; do **not** run non-MD handling, embedded normalization, or ingest pipeline steps on this file.

Unsupported types (e.g. video without transcript): create stub .md in Ingest with "Requires manual transcription → ![[5-Attachments/Audio/...]]" and tag `#needs-human`.

Always propose full .md content for new notes for review; respect MCP safety (backup before destructive steps, snapshot per mcp-obsidian-integration).

After processing a batch, if git is enabled and user prefers, propose a single commit message (e.g. "Ingest: process N files, companions created") for the user to run.

## MCP SAFETY

- For non-.md files: create companion .md + embed/link, then **attempt** move of original to 5-Attachments/[subtype]/ via obsidian_ensure_structure + obsidian_create_backup + obsidian_move_note (backup required first; on backup failure do not move). If the server rejects or fails (e.g. only .md supported), leave original in Ingest/ and add frontmatter tag: #needs-manual-move and failure callout.
- In the companion note, on failure add: manual-move callout and #needs-manual-move; on success add success callout and do not add #needs-manual-move.
- Never use shell mv/cp/rm except when the move-attachment-to-99 skill is explicitly invoked by the user (see non-markdown-handling and mcp-obsidian-integration.mdc).

## Error handling

If listing Ingest, non-MD handling, embedded image normalization, or full-autonomous-ingest fails for a file or note:

- Follow the **Error Handling Protocol** in `mcp-obsidian-integration.mdc` (§ Error Handling Protocol).
- Pipeline name: `ingest-processing` or `full-autonomous-ingest` as appropriate; stage: e.g. `non-md companion`, `embedded image normalization`, `ingest pipeline`. Include **error_type** in the summary and in the Errors.md entry table.
- Log to `3-Resources/Errors.md` (standard entry format: heading, metadata table, #### Trace, #### Summary) and reference in `Ingest-Log.md`.
- On backup or MCP failure for one item: skip that item, log, continue with the rest.
