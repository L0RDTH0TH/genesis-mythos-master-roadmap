---
name: roadmap-checklist
description: From a roadmap note (or any note with sections and wiki-links), produce a hierarchical checklist by following [[links]] recursively up to max_depth with cycle detection. Output in-note or new note; optional flatten and status-sync. Use when triggered manually or via ROADMAP MODE.
---

# roadmap-checklist

## When to use

- **Manually** (e.g. "Generate hierarchical checklist for this note" or "ROADMAP MODE – generate checklist for current note").
- **Optional**: If a dedicated context rule exists for ROADMAP MODE, this skill runs when the user requests a hierarchical checklist from a roadmap note.
- **Not** part of the default ingest pipeline (recursion can be heavy); keep as opt-in so ingest stays fast.

## Instructions

1. **Parse note**: Use `obsidian_read_note`(path). Extract:
   - **Sections**: headings (`##`, `###`).
   - **Tasks**: lines matching `- [ ]` or `- [x]` (preserve status if status-sync is true).
   - **Wiki-links**: `[[Link]]` and `[[Link|Alias]]`; resolve to vault paths (strip alias; resolve link to .md path via convention or `obsidian_list_notes` on parent folder). **Exclude** #tags and non-.md links (e.g. `[[file.pdf]]`).

2. **Build tree (recursion)**:
   - Maintain a **visited set** of resolved note paths to avoid cycles (e.g. A → B → A).
   - **max_depth** (default **3**): at depth ≥ max_depth, do not follow further links.
   - **max links per note** (e.g. 10): cap how many links are followed from a single note to avoid explosion.
   - **Vault-size check**: if total links encountered in the run exceed a threshold (e.g. 100), warn and cap max_depth at 2 (or stop recursion).
   - For each wiki-link in the current note: if resolved path not in visited and depth < max_depth, add path to visited, recurse (read linked note, extract its sections/tasks/links, append as subtasks), then continue. Reuse **next-action-extract** logic for task extraction in linked notes (identify task-like lines and `- [ ]` / `- [x]`) for consistency.
   - **Memoization** (optional): cache parsed note content (e.g. by path) in a transient structure for the run to avoid re-reading the same note if linked from multiple places.

3. **Output**:
   - **output === "in_note"**: Append a new section (e.g. `## Generated Checklist`) to the **same** note with the hierarchical markdown (nested `- [ ]` / `- [x]` with indentation). **Backup and per-change snapshot before append** per mcp-obsidian-integration.
   - **output === "new_note"**: Create a new note (e.g. same folder, name like `Checklist.md` or `<original-slug>-Checklist.md`) with the checklist content. Use `obsidian_update_note` with mode create or overwrite as appropriate; ensure parent folder exists (`obsidian_ensure_structure`). Snapshot before write if overwriting.
   - **filter**: "tasks-only" — include only lines that are tasks (ignore section headers without tasks). "full-hierarchy" — include all headings as parent lines with their tasks as children.
   - **flatten** (optional): Output a flat list of all tasks (no nesting) in addition to or instead of the hierarchical view; document in skill or params.
   - **status-sync**: If true, preserve `- [x]` from source notes in the generated checklist; otherwise output all as `- [ ]`.
   - **Frontmatter**: Optionally update the target note's `next-actions` (e.g. top-level task titles only) via `obsidian_manage_frontmatter` if desired; keep format consistent with vault (JSON array string or comma-separated).

4. **Safeguards**:
   - **max_depth** (default 3).
   - **visited set** (resolved paths) to prevent cycles.
   - **max links per note** (e.g. 10).
   - **Vault-size check**: e.g. if total links seen > 100, warn and cap depth at 2.
   - **Memoization**: cache parsed notes for the run to avoid duplicate reads.

5. **Log**: Log outcome (path, depth reached, task count, output path) to a suitable log (e.g. Ingest-Log or a dedicated Roadmap-Checklist-Log); include snapshot path if created.

## MCP tools

- `obsidian_read_note` — read note at path; resolve and read linked notes during recursion
- `obsidian_list_notes` — optional: resolve wiki-link to path (list folder, match by name)
- `obsidian_update_note` — append section (in_note) or write new note (new_note); backup/snapshot first
- `obsidian_ensure_structure` — ensure parent folder exists when creating new note
- `obsidian_manage_frontmatter` — optional: set next-actions on target note
- obsidian-snapshot skill — per-change snapshot before append or overwrite
- `obsidian_create_backup` — before destructive write if not already done in pipeline

## Confidence gate

**≥85%**: Execute (parse, recurse, write). **<85%**: Propose checklist structure only; do not write. For manual trigger, user can confirm; document in skill that low confidence means propose-only.

## Risks and mitigations

- **Circular links**: Visited set prevents infinite recursion.
- **Performance**: max_depth, max links per note, and vault-size cap keep runs bounded; document that this is for focused roadmap notes, not whole-vault scans.
- **Sync/conflicts**: Same as other append/update flows; backup and per-change snapshot before writing.

## Trigger (document for user)

- **ROADMAP MODE** – generate hierarchical checklist for current note (if context rule exists).
- **Manual**: "Generate checklist for [[this note]]" or "Run roadmap-checklist on current file."
- **Hotkey/URI**: Document in skill or in Mobile-Toolbar-Task-Commands that user can bind a command to run Cursor with this intent (e.g. URI or prompt template).
