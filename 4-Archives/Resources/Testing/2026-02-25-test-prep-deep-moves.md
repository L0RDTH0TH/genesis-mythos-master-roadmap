---
title: Test prep — deep-nested PARA moves
created: 2026-02-25
para-type: Resource
status: active
tags: [test-prep, pipelines, move_note, ensure_structure]
---
# Test prep — deep-nested PARA moves

Summary of preparations for **Goal 4: Deep-nested PARA move behavior** (3–4 levels: `obsidian_ensure_structure` + `obsidian_move_note`).

## Fixes implemented

- **.cursor/rules/always/mcp-obsidian-integration.mdc**: Added section **"Documented behavior (fill after manual tests)"** with a table for:
  - Whether `obsidian_move_note` creates parent directories automatically.
  - Whether `obsidian_ensure_structure` creates a full 3–4 level path in one call.
  - Behavior when target path already exists (collision).
  - Case-sensitivity / invalid characters.
  - Suggested test path: `4-Archives/Test-Project-Archive/Subtheme/2026-02-25-archive-test.md`

No code or pipeline logic was changed; the rule now has a placeholder for empirically observed behavior once you run the test below.

## Test data prepared

- Use any existing note in `1-Projects/Test-Project/` as the source (e.g. **2026-02-25-archive-candidate.md** or a copy). Target path is **4-Archives/Test-Project-Archive/Subtheme/2026-02-25-archive-test.md** (4 segments: archive root, project-archive, subtheme, filename).

## Readiness

**Verified 2026-02-25.** Behavior documented in `.cursor/rules/always/mcp-obsidian-integration.mdc` and `3-Resources/Second-Brain-Limitations.md`. Use `obsidian_ensure_structure` with **folder_path** for target parent before deep moves.

## Verification complete (2026-02-25)

- [x] Verify deep-nested PARA move behavior (3–4 levels)  
  → **obsidian_ensure_structure**(folder_path: parent) + **obsidian_move_note** creates folders reliably.  
  → Conflict/already-exists: folders idempotent; target file overwrite (backup/snapshot first).

## Review Needed
Proposed para-type: resource. Assigned based on content/frontmatter (confidence ~70%). Do not move until reviewed.