---
name: roadmap-revert
description: Escape hatch for phase regret. Archives old phase to Roadmap/Branches/phase-N-revision-YYYYMMDD/; resets roadmap-state current_phase to N; re-queues EXPAND-ROAD from N with user_guidance (e.g. "Ignore prior choice X, use Y instead"). Use queue mode REVERT-PHASE or Commander "Reopen Phase".
---

# roadmap-revert

## When to use

- Queue mode **REVERT-PHASE** (payload: project_id or source_file, phase number N, optional user_guidance).
- Commander macro **"Reopen Phase"** (or "Revert Phase N") when user wants to re-open and rewrite a phase.

## Parameters

- **project_id** (required): From payload or source_file path.
- **phase_number** (required): Phase N to revert (re-open from this phase).
- **user_guidance** (optional): e.g. "Ignore previous decision X, use Y instead." Injected into EXPAND-ROAD queue entry.

## Instructions

1. **Resolve paths**: `roadmapDir = "1-Projects/{project_id}/Roadmap/"`. State path: `roadmapDir + "roadmap-state.md"`. Branch folder: `roadmapDir + "Branches/phase-{N}-revision-{YYYYMMDD}/"`.

2. **Backup and snapshot**: Call **obsidian_create_backup** for roadmap-state.md and any phase-N-output or phase note to be archived. Call **obsidian_snapshot** (per-change) on roadmap-state.md before modifying.

3. **Create branch folder**: **obsidian_ensure_structure**(folder_path: `Roadmap/Branches/phase-{N}-revision-{YYYYMMDD}`).

4. **Archive old phase**: Move or copy current phase-N-output (and linked phase roadmap note if desired) into the branch folder (e.g. `phase-N-output.md` → `Branches/phase-N-revision-YYYYMMDD/phase-N-output.md`). Update any links in roadmap-state that pointed at the old phase output to point at the branch copy or leave as historical reference.

5. **Reset state**: Update roadmap-state.md: set `current_phase` to N (so next resume continues from phase N). Optionally set `status: in-progress` if it was complete. Write via obsidian_update_note (after snapshot).

6. **Re-queue EXPAND-ROAD**: Append an entry to `.technical/prompt-queue.jsonl` with `mode: EXPAND-ROAD`, `source_file` pointing at the phase note or roadmap-state, `prompt` or `params.user_guidance` set to user_guidance (e.g. "Ignore prior choice X, use Y instead"). So the next EAT-QUEUE runs expansion from phase N with guidance.

7. **Error handling**: On failure, log trace to [Errors](3-Resources/Errors.md) with **#review-needed** per [mcp-obsidian-integration](.cursor/rules/always/mcp-obsidian-integration.mdc).

## MCP tools

- `obsidian_ensure_structure` — create Roadmap/Branches/phase-N-revision-YYYYMMDD/
- `obsidian_read_note` / `obsidian_update_note` — read and update roadmap-state.md
- `obsidian_move_note` or copy — archive phase output to branch folder (dry_run then commit)
- `obsidian_create_backup` — before any structural change
- obsidian-snapshot skill — per-change snapshot of roadmap-state before update

## Reference

- Multi-Run Roadmap plan § Escape hatch and hardening — REVERT-PHASE queue mode.
- [Queue-Sources](3-Resources/Second-Brain/Queue-Sources.md) — REVERT-PHASE.
