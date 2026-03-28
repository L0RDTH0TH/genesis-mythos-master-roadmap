---
name: roadmap-audit
description: Scans phase notes and decisions-log for cross-phase drift; computes drift score; creates Decision Wrapper when drift > threshold; logs exact drift score in consistency report; auto-reverts when ignored wrappers exceed config. Used in RECAL-ROAD.
---

# roadmap-audit

## When to use

- As part of **RECAL-ROAD** (queue mode or Commander "Recalibrate roadmap"). Auto-triggered after every 3 phases, or when any phase conf < 88%, or when drift > **drift_score_threshold** (default 0.08; from Parameters roadmap block).
- Optionally every N phases in the autonomous-roadmap chain.
- On-demand when user wants to check roadmap consistency.

## Parameters

- **project_id** (required): Project containing the Roadmap folder.
- **roadmap_dir** (optional): Override path; default `1-Projects/{project_id}/Roadmap/`.
- **drift_score_threshold** (optional): From Parameters or Second-Brain-Config roadmap block; default **0.08**. Drift above this forces wrapper with revert prioritized.
- **handoff_gaps_drift_penalty** (optional): From config roadmap block (e.g. 0.3). When present, add this per phase where `handoff_gaps.length > 2` (or configurable threshold) to drift score; cap total drift in 0.0–1.0. Log in consistency report when hand-off gaps contributed.
- **ignored_wrappers_auto_revert** (optional): From config; default **3**. When count of ignored recal wrappers for this roadmap ≥ this value, auto-revert to last high-conf phase instead of creating another wrapper.

## Instructions

1. **Resolve tree root**: Default **`roadmapDir`** = `1-Projects/{project_id}/Roadmap/`. **Dual track:** If **`params.roadmap_track`** is **`execution`** or **`roadmap-state.md`** frontmatter **`roadmap_track`** is **`execution`**, set **`phaseTreeRoot`** = `roadmapDir/<execution_subfolder>/` (default **`Execution`**) for phase note listing; else **`phaseTreeRoot`** = **`roadmapDir`**. Always read **conceptual** **`roadmap-state.md`** at **`roadmapDir`** for **`current_phase`** / project cursor. **List phase notes**: Under **`phaseTreeRoot`**, list phase roadmap notes; read **decisions-log.md** (under **`roadmapDir`**) and **roadmap-state.md**. Read project master goal or Source note for semantic diff.

2. **Semantic diff and drift score**: Do semantic diff of phase content against master goal + **distilled-core.md**. Compute **drift score** (e.g. 0.0–1.0; higher = more drift). When **handoff_gaps_drift_penalty** is set in config, add it per phase where phase note has `handoff_gaps` and length > 2 (or configured threshold); cap total drift in 0.0–1.0. Compare phase content and decisions-log entries; identify contradictions. Assign **severity**: low (cosmetic), medium (clarification needed), high (actionable contradiction).

3. **Consistency report**: Output a **consistency report** callout in roadmap-state.md body (or linked note). **Log the exact drift score** (numeric) in that report so state carries the last recal result. When hand-off gaps contributed to drift, note that in the report. Update **handoff_drift_last_recal** in roadmap-state frontmatter (parallel to drift_score_last_recal). If **handoff_drift_last_recal > 0.2**, force hand-off audit (run hand-off-audit for current or flagged phases).

4. **Auto-fix minor (optional)**: When queue payload or config has **auto_fix_minor: true**, include hand-off minors (e.g. auto-add basic acceptance criteria if the only gap is "no criteria"); cap confidence bump at +5% to avoid over-automation.

5. **If ignored_wrappers ≥ ignored_wrappers_auto_revert** (for this roadmap): Do **not** create a new wrapper. **Auto-revert** to last high-conf phase: archive bad phase to `Roadmap/Branches/`, reset `current_phase` in roadmap-state, re-queue EXPAND-ROAD from there. Log "Auto-reverted due to repeated ignored drift warnings" to Ingest-Log or Backup-Log. Snapshot roadmap-state before and after update.

6. **If drift > drift_score_threshold** (default 0.08): Force a **Decision Wrapper** with **"A: Revert to last safe phase"** as the default/first option (revert prioritized). Other options: Re-apply with changes, Align phase with Phase 1, Update Phase 1 to match, Leave as-is, Re-run EXPAND-ROAD with guidance, etc. Pad to 7 (A–G). Set `wrapper_type: roadmap-decision`, `pipeline: roadmap`, `original_path` to roadmap-state or master roadmap, `clunk_severity: high`. Ensure **obsidian_ensure_structure** for `Ingest/Decisions/Roadmap-Decisions` (or Refinements per vault convention). Log CHECK_WRAPPERS and append to Watcher-Result.

7. **If any drift has severity > medium** (and drift ≤ threshold, or no numeric threshold yet): Create Decision Wrapper as above; prefer "A: Revert to last safe phase" when drift is high.

8. **If no drifts or all low**: Log "roadmap-audit: no actionable drifts" and update roadmap-state with drift_score_last_recal (e.g. 0). Return.

9. **Error handling**: On read failure or exception, log trace to [Errors](3-Resources/Errors.md) with **#review-needed** per [mcp-obsidian-integration](.cursor/rules/always/mcp-obsidian-integration.mdc) Error Handling Protocol.

## MCP tools

- `obsidian_list_notes` — list phase notes under Roadmap/
- `obsidian_read_note` — read phase notes and decisions-log
- `obsidian_ensure_structure` — ensure Ingest/Decisions subfolder exists
- `obsidian_update_note` or create wrapper note — create Decision Wrapper
- `obsidian_log_action` — log to Ingest-Log / Roadmap-Log

## Reference

- Multi-Run Roadmap plan Phase 2 — RECAL-ROAD, confidence gates, roadmap-validate.
- [Cursor-Skill-Pipelines-Reference](3-Resources/Second-Brain/Cursor-Skill-Pipelines-Reference.md) — RECAL-ROAD dispatch.
