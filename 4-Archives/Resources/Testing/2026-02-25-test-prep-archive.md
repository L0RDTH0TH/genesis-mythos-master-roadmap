---
title: Test prep — autonomous-archive
created: 2026-02-25
para-type: Resource
status: active
tags: [test-prep, pipelines, autonomous-archive]
---
# Test prep — autonomous-archive

Summary of preparations for **Goal 2: Run archive sweep** (5–15 old/completed/project-archivable notes).

## Fixes implemented

- **.cursor/rules/always/mcp-obsidian-integration.mdc**: Added section **"Documented behavior (fill after manual tests)"** with a table for recording:
  - Whether `obsidian_move_note` creates parent dirs.
  - Whether `obsidian_ensure_structure` creates 3–4 levels in one call.
  - Behavior when target path already exists (collision).
  - Case-sensitivity / invalid characters.
  - Suggested test path: `4-Archives/Test-Project-Archive/Subtheme/2026-02-25-archive-test.md`
- **3-Resources/Archive-Log.md**: Added "Example entries (template)" with one sample line so format is clear before first run.

## Test data prepared

- **1-Projects/Test-Project/2026-02-25-archive-candidate.md** — status complete, no open tasks, has TL;DR callout; ready for archive-check and move.
- **1-Projects/Test-Project/2026-02-25-archive-candidate-2.md** — same; use to run a small batch (add more completed notes under Test-Project if you want 5–15).

## Readiness

**Mostly ready.** Behavior doc is a template; after you run one manual move (see Goal 4 test path), fill the table in `mcp-obsidian-integration.mdc` so future archive sweeps have documented expectations.

## User next steps

1. **Optional — document move behavior first:** Run a single manual test move to a 3–4 level path (e.g. move one note to `4-Archives/Test-Project-Archive/Subtheme/...`). Record results in the "Documented behavior" table in `mcp-obsidian-integration.mdc`. (See also [[2026-02-25-test-prep-deep-moves]].)
2. **Run archive sweep:** In Cursor, say: **"ARCHIVE MODE – safe batch autopilot on 1-Projects/Test-Project/"** or **"Archive completed notes in Test-Project"**. Ensure only Test-Project scope.
3. **Verify:** Check `3-Resources/Archive-Log.md` and `3-Resources/Backup-Log.md` for entries; confirm notes moved to `4-Archives/Test-Project-Archive/...` and per-change snapshots exist.

## Review Needed
Proposed para-type: resource. Assigned based on content/frontmatter (confidence ~70%). Do not move until reviewed.