---
name: expand-road-assist
description: Parses user text into structured sub-phases/tasks or suggests reasonable breakdown if blank; appends under target section/task; links back to roadmap/MOC. Use when EAT-QUEUE processes mode EXPAND-ROAD.

---

# expand-road-assist

## When to use

- When **auto-queue-processor** dispatches a queue entry with **mode: EXPAND-ROAD**.
- Payload: `primaryPath`, `sectionOrTaskLocator`, `userText` (string or null).

## Instructions

1. **Read primary**: Use `obsidian_read_note`(primaryPath) to get the roadmap and locate the target section or task (by sectionOrTaskLocator: heading name or block-id).

2. **Content**:
   - If **userText** is present: Parse it into structured sub-phases and/or tasks (e.g. bullet list with `###` and `- [ ]`). Keep format consistent with [Roadmap-Standard-Format](3-Resources/Roadmap-Standard-Format.md).
   - If **userText** is blank: **Suggest** a reasonable breakdown (e.g. 2–3 sub-phases or tasks) based on the target section/task title. **Propose-only if confidence <85%**; do not write without user intent. If confidence ≥85%, can append a minimal suggested structure.

3. **Append**: Insert the new structure **under** the target section/task (e.g. after the target heading or task line). Use `obsidian_search_replace` or `obsidian_update_note` to insert the new content. **Snapshot before write** per mcp-obsidian-integration.

4. **Link back**: Ensure the new content or the roadmap note links to the project MOC if applicable (e.g. frontmatter `links` or in-body link).

5. **No autonomous restructure**: Do not rewrite or restructure existing roadmap content beyond appending under the target. Do not initiate expand without user intent (queue entry).

6. **Log**: Append result to Watcher-Result and Mobile-Pending-Actions.

7. **Post-step — Phase fork detection (optional):** After expand writes content, if [Second-Brain-Config](3-Resources/Second-Brain/Second-Brain-Config.md) has `phase_fork_heuristic: "strict"`, scan the written output (expanded section/phase text) for choice indicators: "or", "vs", "options:". If any are found: set frontmatter **`phase_forks`** on the roadmap note (array, e.g. `["grid-size", "camera-type"]` — derive short slugs from the section or choice context) and auto-queue creation of a Phase Direction Wrapper under `Ingest/Decisions/Roadmap-Decisions/` (chain like INGEST → ORGANIZE per [Queue-Sources](3-Resources/Second-Brain/Queue-Sources.md)). When **creating** the Phase Direction Wrapper: fill options A–G with **conceptual end-state** descriptions only — one sentence per option describing *what the situation is* after that choice; no technical terms (e.g. "One shared grid everywhere — same behavior on every device and screen"). Store technical resolution in wrapper frontmatter (e.g. `technical_by_option: { "A": "...", "B": "..." }`) for provenance; do not put technical text in the main option list. See [Cursor-Skill-Pipelines-Reference § Phase-direction wrapper creation](3-Resources/Second-Brain/Cursor-Skill-Pipelines-Reference.md) and [Templates/Decision-Wrapper-Phase-Direction.md](Templates/Decision-Wrapper-Phase-Direction.md). If `phase_fork_heuristic: "off"`, skip this step; only explicit `phase_forks` in frontmatter (set by user) then trigger wrapper creation when the post-step or processor runs. **Low-confidence:** Per [Parameters § Confidence bands](3-Resources/Second-Brain/Parameters.md), when confidence <68% treat as propose-only (do not write wrapper without user approval). When the user has already set **`phase_forks`** (frontmatter array) on the note, always create the Phase Direction Wrapper for that phase when this post-step runs.

## MCP tools

- `obsidian_read_note` — read primary roadmap
- `obsidian_search_replace` / `obsidian_update_note` — insert new content under target
- obsidian-snapshot skill — snapshot before write

## Confidence gate

**≥85%**: Write suggested or parsed structure. **<85%**: Propose-only; do not write. Log and update Mobile-Pending-Actions.
