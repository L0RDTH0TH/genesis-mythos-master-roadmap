---
name: normalize-master-goal
description: Restructures a Project Master Goal (PMG) note to match the normalized Master-Goal template (One-line, Vision, Phases, Technical Integration, TL;DR, Related). Used before roadmap generation and on demand via NORMALIZE-MASTER-GOAL queue mode.
---

# normalize-master-goal

## When to use

- When **ROADMAP MODE – generate from outline** runs and the seed note is a PMG: run this skill **first** so the seed follows [[Templates/Master-Goal]] and phase parsing is reliable.
- When the user or queue requests **NORMALIZE-MASTER-GOAL** with a note path: normalize that note to the template.
- When you want to bring an ad-hoc or legacy master goal file into the standard structure for roadmap derivation and scoping.

## Scope

- **Applies to**: Notes that are Project Master Goals — `is_master_goal: true` in frontmatter **or** path/filename matches `*Master*Goal*` (or `*MasterGoal*`) under `1-Projects/` or `Ingest/`.
- **Skips**: Notes that are not PMGs; skip and log when in doubt.

## Inputs

- `path`: vault-relative path of the master goal note (from `source_file`, `original_note`, or trigger).

## High-level behavior

1. **Backup & snapshot**
   - Call `obsidian_create_backup` for the note path if not already backed up in this run.
   - Before rewriting the body, call **obsidian-snapshot** with `type: "per-change"` for the note (per mcp-obsidian-integration).

2. **Read and classify**
   - Use `obsidian_read_note(path)` to get frontmatter and body.
   - If `is_master_goal` is not true and filename/path does not match `*Master*Goal*` (or `*MasterGoal*`), **skip** normalization; return without writing. Optionally log "Not a PMG; skipped."

3. **Map content to template sections**
   - Use [[Templates/Master-Goal]] as the target structure:
     - **## One-line** — Single-sentence elevator pitch. If the note has a blockquote or line like "One-line Master Goal" or "One-line:", use that. Else derive from the first paragraph or a "TL;DR" / "In short" sentence.
     - **## Vision** — Full narrative (what we're building, for whom, why). Map from "Full output", "Master Goal v2.0", "Vision", or the main body. Preserve bullets and paragraphs.
     - **## Phases** — Top-level phases. Use headings like `### Phase N — <Name>` under `## Phases`. Map from existing "Phases", "Phase 1", "## 1. …", or infer from Vision subsections. Each phase gets a short paragraph or bullet list (seed for roadmap phases).
     - **## Technical Integration** — Optional. Map from "Technical Integration", "Technical", "Architecture", or similar. Omit if absent.
     - **## TL;DR** — Short summary. Map from "TL;DR", "In short", "Summary", or the last one-sentence summary in the note.
     - **## Related** — Links to MOC, roadmap, or related notes. Use existing `links` in frontmatter or a "Related" section; or leave placeholder bullets.
   - Preserve all substantive content; only restructure headings and order. Do not drop bullets or paragraphs.

4. **Write back**
   - Set frontmatter `is_master_goal: true` if not set. Leave other frontmatter (title, created, project-id, tags, links) unchanged unless missing (e.g. set project-id from path).
   - Build the new body from the mapped sections. Use `obsidian_update_note(path, content, mode: "overwrite")` to replace the body (or full note if you include frontmatter). Prefer overwriting the whole note so structure is consistent.

5. **Logging**
   - Append to `3-Resources/Ingest-Log.md` or a dedicated log line: "Normalized master goal: <path> to Master-Goal template." When invoked from ROADMAP MODE, the roadmap-generate-from-outline skill logs; when invoked from NORMALIZE-MASTER-GOAL queue mode, append to Watcher-Result.md.

## Phase parsing compatibility

- **roadmap-generate-from-outline** expects phases from the seed. After normalization, phases live under `## Phases` as `### Phase N — <Name>` with optional body. The roadmap skill should parse either:
  - Top-level `## Phase N — <Name>`, or
  - `### Phase N — <Name>` under `## Phases`.
- This skill does not run roadmap generation; it only restructures the PMG so that the roadmap skill can reliably find phase names and seed sentences.

## MCP tools

- `obsidian_read_note` — read the current note.
- `obsidian_update_note` — write the normalized content (after backup and snapshot).
- `obsidian_create_backup` — ensure backup exists.
- **obsidian-snapshot** skill — per-change snapshot before overwrite.

## Confidence

- Run when the note is clearly a PMG. If structure is ambiguous (e.g. multiple "Vision" blocks), prefer preserving content and placing it in the most appropriate section; add a short note in TL;DR if needed ("Normalized from legacy structure on <date>.").
