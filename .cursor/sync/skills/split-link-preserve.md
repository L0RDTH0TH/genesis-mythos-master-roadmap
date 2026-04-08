---
name: split-link-preserve
description: After obsidian_split_atomic, writes split_from on each child and split_into (or "Splits" section) on the parent for traceability and Dataview. Minimal, Zettelkasten-friendly. Use in full-autonomous-ingest immediately after split_atomic.
---

# split-link-preserve

## When to use

- **Immediately after** `obsidian_split_atomic` in the full-autonomous-ingest pipeline.
- Only when confidence is **≥85%** that the split succeeded and child paths are known; otherwise skip or propose links only.
- Per-change snapshot for the **parent** note is already taken before `obsidian_split_atomic` by the pipeline; this skill only adds metadata and sections (no destructive delete). If editing multiple new child notes, prefer minimal writes (frontmatter first) to limit scope.

## Design (minimal & Zettelkasten-friendly)

- **Children**: YAML `split_from: "[[Original Note Title]]"`; if `related` frontmatter exists, append the original link (do not overwrite).
- **Parent**: Append (or under existing ## Splits) a **Splits / Extracted** bullet list: `- [[New Atomic Note Title]] — brief one-line reason`.
- **Navigation**: Rely on Obsidian backlinks pane for reverse navigation; no separate backlink note.
- **Idempotent**: Do not duplicate bullets on parent; do not duplicate the original link in `related` on children. Snapshot before edit when required by pipeline.

---

## Instructions

1. **Inputs**: From the pipeline you have the **original (parent) note path** and the **list of child note paths** returned by `obsidian_split_atomic`. If the MCP does not return child paths, use `obsidian_list_notes` on the same folder or infer from the split tool output. Derive **original note title** from parent path (filename without extension, or first `# ` heading in parent) for wikilink `[[Original Note Title]]`.

2. **On each child note**:
   - **split_from**: Use `obsidian_manage_frontmatter`(path: child_path, key: `split_from`, value: `"[[Original Note Title]]"`, action: set). Use the parent’s note title as the wikilink text (human-readable).
   - **related (append only)**: Use `obsidian_read_note`(child_path) to read current frontmatter. If the note has a `related` key and it is a list (array), append `"[[Original Note Title]]"` to that list only if not already present, then use `obsidian_manage_frontmatter`(path: child_path, key: `related`, value: JSON array string of the new list, action: set). If there is no `related` key, do not create one (keep it lightweight).

3. **On the parent note** (if it still exists after split):
   - Use `obsidian_read_note`(parent_path) to confirm it exists and to get current content.
   - **Idempotent check**: If the note already contains a section headed `## Splits` (or "Splits / Extracted"), and a bullet with the same `[[Child Note Title]]` already exists, do not add a duplicate bullet for that child.
   - **Brief description**: For each new child, derive a one-line reason from the child note (e.g. first sentence of body, or first heading). Truncate to a short phrase (e.g. ~60 chars) for readability.
   - **Append**:
     - If `## Splits` already exists: append under that section the new bullets only (one per child not already listed): `- [[Child Note Title]] — brief one-line reason`.
     - If `## Splits` does not exist: append at the bottom of the note: `\n\n## Splits\n\nSplits / Extracted\n\n- [[Child Note Title 1]] — reason\n- [[Child Note Title 2]] — reason\n` (and so on for each child).
   - Use `obsidian_update_note`(path: parent_path, content: full note content with new/updated section, mode: overwrite) or a safe append (e.g. `obsidian_search_replace` to insert after a known line). Prefer overwrite only when you have read the full note and are appending the new block; ensure pipeline has already taken a per-change snapshot before split so parent is safe.
   - **Optional frontmatter**: You may set `split_into` on the parent as a JSON array of child paths for Dataview (e.g. `"[\"path1\", \"path2\"]"`) via `obsidian_manage_frontmatter`; this is optional if the bullet list is the primary traceability.

4. **Logging**: Include in the ingest log that split-link-preserve ran (parent path, number of children, paths updated). No separate snapshot is required by this skill if the pipeline already snapshotted before `obsidian_split_atomic`; snapshot-before-edit for each new child is pipeline-level policy.

---

## MCP tools

- `obsidian_read_note` — read parent and children to get titles, frontmatter (`related`), and existing ## Splits section
- `obsidian_manage_frontmatter` — set `split_from` (and optionally `split_into` on parent); set `related` on child when appending
- `obsidian_update_note` / `obsidian_search_replace` — append or update ## Splits section on parent
- `obsidian_list_notes` — fallback to discover child paths if split_atomic does not return them

---

## Confidence gate

**≥85%**: Apply frontmatter and Splits section. **<85%**: Propose links only; do not write.

---

## Output

- **Child notes**: `split_from: "[[Original Note Title]]"` in YAML; `related` array appended with original link if `related` already exists.
- **Parent note**: Section `## Splits` with "Splits / Extracted" and bullets `- [[Child Title]] — brief one-line reason`; optional `split_into` frontmatter for Dataview.
- Enables Dataview queries (e.g. `LIST FROM "" WHERE split_from`) and Obsidian backlinks for "notes split from X" and "note X split into Y, Z".
