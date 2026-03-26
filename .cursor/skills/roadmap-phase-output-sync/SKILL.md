---
name: roadmap-phase-output-sync
description: Keeps phase-X-output.md aligned with the canonical phase roadmap note. Compare narrative; report #review-needed or auto-refresh from phase roadmap (snapshot + backup before overwrite). Single writer: only pipeline updates phase-X-output. Use after phase writes, during RECAL-ROAD, or on queue mode SYNC-PHASE-OUTPUTS.
---

# roadmap-phase-output-sync

## When to use

- After phase-output writes in the autonomous-roadmap chain.
- During **RECAL-ROAD** (optionally, every N phases).
- On-demand: queue mode **SYNC-PHASE-OUTPUTS** or Commander "Sync phase outputs".

## Parameters

- **project_id** (required): Project containing the Roadmap folder.
- **phase_number** (optional): Sync only this phase; if omitted, sync all phase-X-output.md under the project Roadmap.
- **mode** (optional): From [Second-Brain-Config](3-Resources/Second-Brain/Second-Brain-Config.md) `phase_output_sync`: `report_only` (default) or `auto_refresh`.

## Instructions

1. **Resolve paths**: `roadmapDir = "1-Projects/{project_id}/Roadmap/"`. List phase roadmap notes (e.g. under `Phase-N-<Name>/` or matching `Phase-*-Roadmap*.md`) and corresponding `phase-X-output.md` in Roadmap/.

2. **For each phase** (or the given phase_number):
   - **Canonical source**: The phase roadmap note (e.g. `Phase-N-<Name>-Roadmap-….md`) is the source of truth.
   - **Derived**: `phase-X-output.md` in Roadmap/ is the derived extract.
   - **Create when missing (template-backed)**: If `phase-X-output.md` does not exist yet, create it from `Templates/Roadmap/Artifacts/phase-output.md` (fill `{{project_id}}`, `{{phase_number}}`, and `{{phase_roadmap_note}}`) before doing any comparisons. Do not treat “missing derived file” as out-of-sync; create then proceed.
   - Read both; compare narrative (headings, key bullets, decisions). Use semantic similarity or diff of key sections; flag if meaningfully out of sync (e.g. missing section, contradictory content).

3. **If in sync**: Log "phase X in sync" to pipeline log (e.g. Roadmap-Log or Ingest-Log with tag `roadmap-phase-sync`); continue.

4. **If out of sync**:
   - **report_only** (or config `phase_output_sync: report_only`): Append to [Errors](3-Resources/Errors.md) or Feedback-Log with **#review-needed**, short summary (phase, path, what differs). Do not overwrite phase-X-output.
   - **auto_refresh**: Call **obsidian_snapshot** on `phase-X-output.md` (per-change), then **obsidian_create_backup** for the path, then refresh phase-X-output body from the canonical phase roadmap note (extract narrative/summary). Write via `obsidian_update_note`. Log "phase X refreshed from canonical" to pipeline log.

5. **Error handling**: On read/write failure, log trace to [Errors](3-Resources/Errors.md) with **#review-needed** per [mcp-obsidian-integration](.cursor/rules/always/mcp-obsidian-integration.mdc) Error Handling Protocol.

## MCP tools

- `obsidian_list_notes` — list phase notes and phase-X-output under Roadmap/
- `obsidian_read_note` — read canonical phase roadmap and phase-X-output
- `obsidian_snapshot` (obsidian-snapshot skill) — before overwrite when auto_refresh
- `obsidian_create_backup` — before overwrite when auto_refresh
- `obsidian_update_note` — write refreshed phase-X-output (auto_refresh only)

## Reference

- [Vault-Layout § Roadmap state artifacts](3-Resources/Second-Brain/Vault-Layout.md) — phase-X-output Approach A, phase output sync rule.
- Multi-Run Roadmap plan — Phase 0 phase output sync rule.
