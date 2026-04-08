---
name: roadmap-validate
description: Cross-checks phase content against the project master-goal (or Source note). Flags mismatches to Errors.md with #review-needed. Used after roadmap-audit or as part of RECAL-ROAD.
---

# roadmap-validate

## When to use

- After **roadmap-audit** in the RECAL-ROAD chain.
- As part of **RECAL-ROAD** (post-audit validation step).
- On-demand to verify phase content aligns with master goal.

## Parameters

- **project_id** (required): Project containing the Roadmap folder.
- **master_goal_path** (optional): Override path to master goal note; default derived from project (e.g. `*Master*Goal*` or Source note under Roadmap/).

## Instructions

1. **Resolve master goal**: Find the project master goal note (filename/path containing Master-Goal or MasterGoal, or `Roadmap/Source-*.md`). Read its content (One-line, Vision, Phases, key constraints).

2. **List phase notes**: Under `1-Projects/{project_id}/Roadmap/`, list phase roadmap notes (Phase-N-*).

3. **Cross-check each phase**: For each phase note, use **obsidian_global_search** (or semantic comparison) to verify phase content aligns with master goal (e.g. phase assumes engine X, master says Y; phase scope contradicts Vision). Document mismatches with short summary (phase path, master excerpt, contradiction).

4. **Append to Errors.md**: For each mismatch, append an entry to [Errors](3-Resources/Errors.md) with **#review-needed**: heading (e.g. `### YYYY-MM-DD HH:MM — Roadmap phase/master mismatch`), metadata table (`pipeline: roadmap-validate`, `severity`, `timestamp`, `error_type: phase-master-mismatch`), #### Trace, #### Summary (Root cause, Impact, Suggested fixes, Recovery). Enables proactive catch before drift compounds.

5. **MOC violation check (MOCs all the way down):** For each phase and secondary roadmap note under `1-Projects/{project_id}/Roadmap/` (notes with `roadmap-level: primary` or `roadmap-level: secondary` and `subphase-index` matching "N" or "N.M"): if that note's **folder contains at least one child note** (sibling .md in the same folder or in a subfolder), the parent note MUST contain a Dataview code block whose FROM path is that folder. **Flag only when the folder has one or more child notes but the parent note lacks the block** (empty secondaries are not violations). If a violation is found, append an entry to [Errors](3-Resources/Errors.md) with `error_type: roadmap-moc-missing`, `#review-needed`, and a short Summary (Root cause: "Phase/Secondary MOC missing Dataview block"; Suggested fixes: add "## Subphases & notes" or "## Tertiary notes" section with canonical Dataview block FROM that folder). Optionally create a Decision Wrapper under `Ingest/Decisions/Roadmap-Decisions/` so the user can add the block and re-run. Documented in [Roadmap-Quality-Guide](3-Resources/Second-Brain/Roadmap-Quality-Guide.md) § MOC violation check.

6. **Error handling**: On read/search failure, log trace to Errors.md with #review-needed per [mcp-obsidian-integration](.cursor/rules/always/mcp-obsidian-integration.mdc) Error Handling Protocol.

## MCP tools

- `obsidian_read_note` — read master goal and phase notes
- `obsidian_list_notes` — list phase notes under Roadmap/
- `obsidian_global_search` — search for key terms from master in phase content (or vice versa) to detect contradictions
- `obsidian_search_replace` or append — add entry to Errors.md

## Reference

- Multi-Run Roadmap plan Phase 2 — roadmap-validate post-audit.
- [Cursor-Skill-Pipelines-Reference](3-Resources/Second-Brain/Cursor-Skill-Pipelines-Reference.md) — RECAL-ROAD, roadmap-audit, roadmap-validate.
