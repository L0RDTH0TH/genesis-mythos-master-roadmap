---
name: roadmap-advance-phase
description: Advances roadmap to the next phase when gate conditions are met. Snapshot state; depth-aware gate (phases 1–4 softer, 5–6 strict); update roadmap-state and workflow_state; log. Used when RESUME-ROADMAP has params.action "advance-phase" or user approves option C on a roadmap-next-step wrapper.
---

# roadmap-advance-phase

## When to use

- When **RESUME-ROADMAP** runs with **params.action: "advance-phase"** (from queue or from approved roadmap-next-step wrapper option C).
- Invoked by auto-roadmap when branching by action.

## Inputs

- **project_id** (required): From auto-roadmap (queue payload, source_file, or user).
- **workflow_state path**: `1-Projects/<project_id>/Roadmap/workflow_state.md` (conceptual) or `.../Roadmap/Execution/workflow_state-execution.md` (execution track — resolve per Dual-Roadmap-Track).
- **roadmap-state path**: `1-Projects/<project_id>/Roadmap/roadmap-state.md` (conceptual) or `.../Roadmap/Execution/roadmap-state-execution.md` (execution track).
- **wrapper_approved** (optional): When true (user chose "Advance to Phase N" on a wrapper), gate is satisfied and proceed.
- **Timestamp resolution (for Log row):** Caller may pass **queue_entry_timestamp** (UTC ISO 8601), **local_timestamp** (string `YYYY-MM-DD HH:MM`), and **display_timezone** (IANA from Config). Resolve the Timestamp cell for the new row using the same order as roadmap-deepen: (1) valid local_timestamp → use it; (2) queue_entry_timestamp + display_timezone → convert UTC to that zone, format `YYYY-MM-DD HH:MM`; on conversion failure log to Errors.md and fall back to server time; (3) server "now". Do not fail the run for timestamp resolution. See Parameters § Timestamp resolution. If this skill ever appends a queue entry, do not copy `timestamp` or `local_timestamp` from the current entry (per Queue-Sources).
- **Run-Telemetry (hand-off):** Caller (auto-roadmap) must pass **parent_run_id**, **queue_entry_id**, **project_id**, and **timestamp** (e.g. from the hand-off block) when invoking this skill so the skill can write the Run-Telemetry note with required fields.

## Instructions

1. **Resolve paths**: `roadmapDir = "1-Projects/<project_id>/Roadmap/"`. **Dual track:** **`active_track`** = `params.roadmap_track` if present, else **`roadmap_track`** from **`roadmapDir/roadmap-state.md`** (default **`conceptual`**). **`execution_subfolder`** from Config (default **`Execution`**). **`phaseTreeRoot`** = `roadmapDir + execution_subfolder + "/"` when **`execution`**, else **`roadmapDir`**. **Active pair** (same as roadmap-deepen): if **`execution`** → read/update **`phaseTreeRoot/workflow_state-execution.md`** + **`phaseTreeRoot/roadmap-state-execution.md`**; if **`conceptual`** → **`roadmapDir/workflow_state.md`** + **`roadmapDir/roadmap-state.md`**. **Snapshot and update** only that pair before any write.

2. **Snapshot before any write**: Per [mcp-obsidian-integration](.cursor/rules/always/mcp-obsidian-integration.mdc), call **obsidian-snapshot** (obsidian-snapshot skill, type per-change) for **roadmap-state** and **workflow_state** before updating state. No state write without prior snapshot.

3. **Optional MOC check (before Gate):** Optionally verify the current phase roadmap note (path derived from roadmap-state current_phase) contains a Dataview block whose FROM path is that phase folder. If the phase folder has child notes and the phase note **lacks** the block, log to [Errors](3-Resources/Errors.md) with `error_type: roadmap-moc-missing` and `#review-needed`; do not update state; optionally create a Decision Wrapper under `Ingest/Decisions/Roadmap-Decisions/` ("Phase N missing MOC block"). See [roadmap-validate](.cursor/skills/roadmap-validate/SKILL.md) step 5 and [Roadmap-Quality-Guide](3-Resources/Second-Brain/Roadmap-Quality-Guide.md) § MOC violation check.

4. **Gate (depth-aware; wrapper overrides; dual-track per [[3-Resources/Second-Brain/Docs/Control-Plane-Heuristics-v2|Control-Plane-Heuristics-v2]] §3.2)**:
   - If **wrapper_approved** (user chose advance on a roadmap-next-step wrapper): proceed.
   - Else **current_phase ≤ 4:** Advance if **handoff-audit(current_phase) ≥ 70%** OR **depth ≥ 3 coverage ≥ 80%** (i.e. at least 80% of secondaries under current phase have at least one tertiary). If not met, abort and log; do not update state.
   - Else **current_phase ≥ 5** and **`active_track` === `conceptual`:** Require **handoff-audit(current_phase) ≥ 85%** only. **Do not** require a depth-4 pseudo-code block on the conceptual tree (NL / checklist completeness is sufficient per dual-track spec).
   - Else **current_phase ≥ 5** and **`active_track` === `execution`:** Require **handoff-audit(current_phase) ≥ 85%** AND at least one **depth-4 note with a pseudo-code block** under current phase (per canonical target). If not met, abort and log; do not update state.

5. **Update roadmap-state**:
   - Append current_phase to **completed_phases** (array).
   - Set **current_phase** to current_phase + 1.
   - Increment **version**; set **last_run** to now (YYYY-MM-DD-HHMM).
   - If current_phase is now 6 and all conditions for "target reached" are met, set **status** to **complete**; else leave status as-is (e.g. generating).

6. **Update workflow_state**:
   - Set **iterations_per_phase** for the new current_phase to 0 (or omit key so it starts fresh).
   - Set **status** to **in-progress**.
   - Clear or reset **current_subphase_index** (e.g. null or "1" for the new phase's first secondary).
   - **Table format:** Preserve the **separator row** when updating workflow_state (the `| --- | --- | ... |` line after the header). If missing, add it so the table is valid Markdown. See [Vault-Layout § workflow_state ## Log table format (Markdown)](3-Resources/Second-Brain/Vault-Layout.md).
   - **Append position:** Append one row **only at the end** of the ## Log table (after the last existing data row). Do not insert between header and first data row or in the middle of existing rows. Use search_replace after the last pipe-delimited line in the first `## Log` block, or reconstruct as header + separator + existing rows in order + new row.
   - Append one row to **## Log** using the **same 12-column schema as roadmap-deepen**: `Timestamp | Action | Target | Iter Obj | Iter Phase | Ctx Util % | Leftover % | Threshold | Est. Tokens / Window | Util Delta % | Confidence | Status / Next`. For advance-phase rows, set **Ctx Util %**, **Leftover %**, **Threshold**, **Est. Tokens / Window**, **Util Delta %**, and **Confidence** to `"-"`. **Timestamp:** Resolve using the inputs above (local_timestamp → queue_entry_timestamp + display_timezone → server time); validate and catch conversion errors per roadmap-deepen; do not fail the run. Example: `| 2026-03-08 15:00 | advance-phase | Phase 2 | 0 | 0 | - | - | - | - | - | - | next deepen (in-progress) |`.

7. **Run-Telemetry:** Ensure `.technical/Run-Telemetry/` exists (obsidian_ensure_structure), then write one note to `.technical/Run-Telemetry/` with **required** fields only: actor: roadmap, project_id, queue_entry_id, timestamp, parent_run_id (from hand-off). Optional: chain_segment. Context/token fields are omitted (advance-phase does not compute context metrics). Naming: `Run-YYYYMMDD-HHMMSS-<project_id>-roadmap.md`. See [Logs § Run-Telemetry](3-Resources/Second-Brain/Logs.md) and [Vault-Layout § .technical/Run-Telemetry](3-Resources/Second-Brain/Vault-Layout.md).

8. **Log**: Append to Ingest-Log (and optionally Backup-Log) a short line: "Advance-phase: project <project_id>, phase <old> → <new>; snapshot taken." Same pattern as [roadmap-generate-from-outline](.cursor/skills/roadmap-generate-from-outline/SKILL.md) Step 5.

## MCP tools

- `obsidian_read_note` — read roadmap-state, workflow_state.
- `obsidian_update_note` — update roadmap-state and workflow_state frontmatter and body.
- **obsidian-snapshot** skill — per-change snapshot of roadmap-state and workflow_state before any write.

## Reference

- [Vault-Layout § Roadmap state artifacts](3-Resources/Second-Brain/Vault-Layout.md) — roadmap-state and workflow_state schema.
- [auto-roadmap](.cursor/rules/context/auto-roadmap.mdc) — branches to this skill when params.action === "advance-phase".
- [Parameters](3-Resources/Second-Brain/Parameters.md) — RESUME-ROADMAP params contract; depth-aware advance condition.
- [Roadmap-Quality-Guide § Roadmap automation target](3-Resources/Second-Brain/Roadmap-Quality-Guide.md) — target definition and handoff-audit threshold.
