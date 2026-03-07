---
name: research-scope
description: During express on a PMG (or note with is_master_goal true / *Master*Goal* path), aggregates already-ingested Resources relevant to the project and surfaces them via a proposal callout; commits Scoped Resources section only on second pass after approved. Vault-only; no external search.
---

# research-scope

## When to use

- **After** related-content-pull, **before** express-mini-outline in the autonomous-express pipeline.
- When the note is a **Project Master Goal (PMG)** or has frontmatter `is_master_goal: true` or path/filename matches `*Master*Goal*.md`.

## Instructions

1. **Detect PMG**: If note path or frontmatter does not indicate a PMG (`is_master_goal: true` or filename pattern `*Master*Goal*.md`), skip (no-op).

2. **Read PMG**: Use `obsidian_read_note(path)` to get `project-id`, `## Phases` or key phrases, and any phase headings for keyword extraction.

3. **Search vault**: Use `obsidian_global_search` and/or `obsidian_list_notes` under `3-Resources/` filtered by project-id (frontmatter or path) and tags/keywords derived from phase headings. Find already-ingested Resource notes relevant to the project.

4. **Propose-first by default**: Do **not** auto-append a `## Scoped Resources` section to the PMG on first pass. Instead insert a **proposal callout** in the PMG body via `obsidian_update_note(path, content, mode: append)`:
   - Format:
     ```markdown
     > [!proposal] Scoped Research Suggestions
     > Confidence: <N>%
     > Suggested additions:
     > - [[path/to/Note-A]] — one-line reason ^[source: project-id + phase "PhaseName"]
     > - [[path/to/Note-B]] — one-line reason ^[source: tag #tagname]
     > Add to PMG? (Set approved: true and re-run EXPRESS or EAT-QUEUE to commit.)
     ```
   - **Lightweight source citation**: For each suggested resource, append inline `^[source: <reason>]` (e.g. `project-id + phase "Terrain"`, `tag #minecraft-beta`) so the user can trace why it was suggested.
   - Only **commit** (append actual `## Scoped Resources` section to PMG) on a **second pass** when the note has `approved: true` in frontmatter or explicit EAT-QUEUE guidance to commit scoping.

5. **Confidence gates**:
   - **≥85%**: Insert proposal callout **and** optionally append the PMG wikilink to each **suggested resource note's** `links` array (via `obsidian_manage_frontmatter`) for bidirectionality; do **not** append `## Scoped Resources` to the PMG body unless user has approved (second pass).
   - **68–84%**: Proposal callout only; no auto-append to PMG body or to resource notes' links.
   - **<68%**: Do not write to the PMG; log to Feedback-Log (or Express-Log) as "low-confidence scoping candidate" with note path and confidence; no callout.

6. **Commit (second pass)**: When running again and the PMG has `approved: true` (or queue payload indicates commit), and the proposal callout is present: create per-change snapshot (obsidian-snapshot skill), then append a proper `## Scoped Resources` section with the same links and citations; optionally remove or collapse the proposal callout to avoid duplication. Never insert into PMG unless user has approved or confidence ≥90% with explicit user_guidance.

7. **Log**: Append result to Express-Log (and Feedback-Log when confidence <68%) with confidence, note path, and whether proposal or commit was performed.

## MCP tools

- `obsidian_read_note` — read PMG and optional resource notes
- `obsidian_global_search` — find Resources by project-id / tags / keywords
- `obsidian_list_notes` — list 3-Resources/ or project-scoped folders
- `obsidian_update_note` — append proposal callout or ## Scoped Resources (mode: append)
- `obsidian_manage_frontmatter` — append to resource notes' links when ≥85% (optional)

## Confidence gate

**≥85%**: Proposal callout + optional link-back to resource notes' links; commit only on second pass when approved. **68–84%**: Proposal callout only. **<68%**: No PMG write; log to Feedback-Log as low-confidence scoping candidate.

## Safety

- Snapshot before any append to PMG when committing on second pass (use obsidian-snapshot skill).
- Never insert into the PMG body unless the user has approved (or confidence ≥90% with explicit user_guidance).
