---
description: "Blacklist raw vault deletes (rm/rmdir/find-delete); require move-to-trash under .trash/ with manifest. Shell mv to trash is the only allowed shell relocation for delete intent."
globs: []
alwaysApply: true
---

# Execution safety blacklist (vault paths)

- **Role:** Prevent whole-vault or path **destructive deletes** via shell. **Delete intent** must be implemented as **move to trash**, not `rm`. Works with [[3-Resources/Second-Brain/Docs/Safety-Invariants|Safety Invariants]] and [[3-Resources/Second-Brain/Docs/Backup-and-Recovery-Strategy|Backup-and-Recovery-Strategy]].
- **Does not replace:** MCP backup/snapshot gates for **pipeline** steps; Obsidian **Settings → Files & Links → Deleted files → Move to Obsidian trash** (operator-mandatory per docs).

## Forbidden (vault-root paths)

For any path inside the **Second-Brain vault root**, agents **must not** invoke:

- `rm`, `rm -rf`, `rmdir` (recursive or not)
- `find ... -delete`, `find ... -exec rm`, `shred`, `unlink` via shell on vault files
- Truncate/overwrite as a stand-in for delete without MCP/snapshot policy

**Violation:** Record **`task_error`** (or `#review-needed` for interactive runs), **halt** further destructive shell ops; do **not** claim Success for the overall task if delete was required to proceed.

## Required rewrite (delete intent)

When removal is genuinely required (cleanup, user request):

1. Prefer **Obsidian MCP** (`obsidian_delete_note` only where contract allows) or **`./scripts/move-to-trash.sh <path> [...]`** from vault root — see [[scripts/move-to-trash.sh|move-to-trash.sh]].
2. **Move target** to **`.trash/<YYYYMMDD-HHMMSS>/`** preserving relative path under that bucket (script handles this). Manifest append: **`.trash/TRASH-MANIFEST.log`** (one line per move: ISO time, from → to).
3. **Emptying `.trash/`** (permanent delete) is **operator-only** with explicit human confirmation — agents do **not** run `rm -rf .trash` or bulk purge.

## Allowed shell `mv` (narrow)

- **`scripts/move-to-trash.sh`** implementation uses `mv` — **only** this pattern for delete intent.
- Other shell `mv`/`cp` on vault notes remains **out of scope** for pipelines (still use MCP per [[.cursor/rules/always/mcp-obsidian-integration.mdc|mcp-obsidian-integration]]); the exception list in Safety Invariants (attachment skill) stays unchanged.

## Cross-links

- [[.cursor/rules/agents/curator-mandatory-backup|curator-mandatory-backup]] — mandatory post-edit Curator commit+push; no public export ad-hoc push
