---
name: MCP Pipelines Migration Plan
overview: Migrate the Second-Brain pipelines to integrate underutilized MCP tools (calibrate_confidence, verify_classification, dry_run, bootstrap, garden/curate flows), update core documentation (Setup Report and Cursor Skill Pipelines Reference), and enforce global safety (ensure_backup, dry_run before every move). The goal is to raise pipeline success rates via confidence enhancements while keeping existing safety invariants.
todos: []
isProject: false
---

# MCP Pipelines Migration Plan

This plan merges the improvement proposals from [2026-02-26-Automation-Flows-MCP-Improvements.md](Ingest/2026-02-26-Automation-Flows-MCP-Improvements.md) and [2026-02-26-Second-Brain-Automations-Setup-Report.md](Ingest/2026-02-26-Second-Brain-Automations-Setup-Report.md) with your detailed recommendations. All referenced MCP tools exist in the obsidian-para-zettel-autopilot server (tools verified under `~/.cursor/projects/.../mcps/user-obsidian-para-zettel-autopilot/tools/`).

---

## 1. Global safety and documentation (foundation)

Apply first so every pipeline can rely on consistent backup and move behavior.

### 1.1 Backup: `obsidian_ensure_backup` before batches

- **Where**: [mcp-obsidian-integration.mdc](.cursor/rules/always/mcp-obsidian-integration.mdc), [Cursor-Skill-Pipelines-Reference.md](3-Resources/Cursor-Skill-Pipelines-Reference.md), [Second-Brain-Automations-Setup-Report.md](Ingest/2026-02-26-Second-Brain-Automations-Setup-Report.md) §3.1.
- **Change**: Document that before long batches or after a gap (e.g. >15 minutes), call `**obsidian_ensure_backup`**(path, max_age_minutes) to confirm a recent backup exists; only call `**obsidian_create_backup`** when ensure_backup indicates one is needed or missing. Keep “no destructive action until backup exists” invariant.
- **Default value guidance**: Suggest `max_age_minutes: 1440` (24 hours) as a safe conservative default for most users/batches; allow tighter values (e.g. 60–180 min) for very active ingest runs. This prevents over-creation while still catching long-idle sessions.
- **Report**: Add subsection under §3.1 describing ensure_backup vs create_backup and when to use each.

### 1.2 Dry-run before every move

- **Where**: [mcp-obsidian-integration.mdc](.cursor/rules/always/mcp-obsidian-integration.mdc), [Cursor-Skill-Pipelines-Reference.md](3-Resources/Cursor-Skill-Pipelines-Reference.md), context rules (ingest, organize, archive).
- **Change**:
  - In **mcp-obsidian-integration.mdc**: Require that for any `**obsidian_move_note`** at ≥85% confidence, the agent must first call `**obsidian_move_note`**(path, new_path, `dry_run: true`), review returned effects (path, new_path, backup status, risks e.g. dangling links), then call again with `dry_run: false` to commit.
  - **Fallback (single canonical definition)**: If `dry_run` reports high-risk items (dangling links, overwrite conflicts, missing parents) **or** the actual move fails later: trigger `**propose_alternative_paths`** → feed top-1 or top-2 into `**calibrate_confidence`** (single retry) → `**verify_classification`** → `dry_run` again → commit; else append full `dry_run` output + error trace to log with `#review-needed` and pause that note. Document this once in the MCP fallback table; all pipelines (ingest, organize, archive) reference this same chain — do not duplicate fallback logic per pipeline.
  - In **Cursor-Skill-Pipelines-Reference.md**: In pipeline tables and flow descriptions, state that move is always "`dry_run` first, then commit."
  - In **Second-Brain-Automations-Setup-Report.md** §7: Add "Dry-run before move" and extend fallback table with the canonical fallback (see §1.2); "dry_run fails or risks → propose_alternative_paths → calibrate → verify → retry; else log."

### 1.3 Health check and observability

- **Where**: Pipelines Reference (new subsection or “Periodic / on-error” section), [Second-Brain-Automations-Setup-Report.md](Ingest/2026-02-26-Second-Brain-Automations-Setup-Report.md) §3.5 or §8.
- **Change**: Document that every N notes (e.g. 10) in a batch, or on first error in a run, call `**health_check`** and log result (status, metrics, serverIdentifier). Prefer a dedicated note `**3-Resources/MCP-Health-YYYY-MM.md`** (monthly rotation) instead of appending forever to Backup-Log.md — keeps observability cleaner; fallback to Backup-Log.md or **3-Resources/MCP-Observability.md** if preferred. No code in rules; documentation only so agents know when and where to log.
- **On non-OK status**: When `**health_check`** returns non-OK status, automatically call `**obsidian_ensure_backup`** as a defensive measure before continuing the batch.

---

## 2. full-autonomous-ingest pipeline

### 2.1 Bootstrap at start

- **Where**: [Cursor-Skill-Pipelines-Reference.md](3-Resources/Cursor-Skill-Pipelines-Reference.md) §1 (full-autonomous-ingest), [Second-Brain-Automations-Setup-Report.md](Ingest/2026-02-26-Second-Brain-Automations-Setup-Report.md) §4.4 and §5.1.
- **Change**: After `**obsidian_list_notes("Ingest")`**, call `**obsidian_list_projects`** and `**bootstrap_project_batch**`(paths, existing_projects_json). If a project seed is detected (≥85%), either auto-apply project creation or set requires_confirmation and ask user, then `**confirm_bootstrap**` to apply in one step. Insert this **before** classify_para in the documented pipeline order and in the ingest flowchart.
- **Defensive note**: If `**bootstrap_project_batch`** returns multiple possible projects or low-confidence matches (<85%), default to requires_confirmation = true and prompt user rather than auto-applying.

### 2.2 Mid-band: MCP path candidates + calibration/verification

- **Where**: [Cursor-Skill-Pipelines-Reference.md](3-Resources/Cursor-Skill-Pipelines-Reference.md) ingest confidence loop and skill table, [confidence-loops.mdc](.cursor/rules/always/confidence-loops.mdc) (reference only).
- **Change**: In **mid-band (72–84% inclusive)**, use **MCP** `**obsidian_subfolder_organize`**(path, para_type, max_candidates) to get 2–3 candidate paths with scores/rationale (in addition to or instead of the skill’s single path). Feed the best candidate into `**calibrate_confidence`**(prior_output: classification + path) then `**verify_classification**`(note_path, calibrated_output). Only proceed to snapshot + move when verdict is “safe to move” and dry_run preview is acceptable. Document in pipeline table and ingest loop description.

### 2.3 Pre-move chain (ingest)

- **Where**: Same as above; [ingest-processing.mdc](.cursor/rules/context/ingest-processing.mdc).
- **Change**: Before `**obsidian_move_note`**: (when in mid-band) **calibrate_confidence** → **verify_classification** → **obsidian_move_note**(..., **dry_run: true**) → if OK, **obsidian_move_note**(..., dry_run: false). Add to §4.4 and §5.1 in the report and to ingest-processing.mdc (enforce dry_run in move rules).

### 2.4 Fallback on move failure

- **Where**: [mcp-obsidian-integration.mdc](.cursor/rules/always/mcp-obsidian-integration.mdc) fallback table, [Cursor-Skill-Pipelines-Reference.md](3-Resources/Cursor-Skill-Pipelines-Reference.md), report §7.
- **Change**: If move fails (e.g. missing parent) or dry_run surfaces risks: call `**propose_alternative_paths`**(note_path, para_context, max_candidates) → feed top candidate into **calibrate_confidence** (one retry) → **verify_classification** → move (dry_run then commit). If still failing, log with #review-needed and full trace. Already partly covered in §1.2; ensure ingest and other pipelines reference this in their “on failure” behavior.

### 2.5 Task rerouting (recommended when task-like)

- **Where**: [Cursor-Skill-Pipelines-Reference.md](3-Resources/Cursor-Skill-Pipelines-Reference.md) §1, [Second-Brain-Automations-Setup-Report.md](Ingest/2026-02-26-Second-Brain-Automations-Setup-Report.md) §5.1.
- **Change**: **Recommended** when next-action-extract confidence ≥78% and para-type includes task-like indicators. When classification or balancer suggests task under Area/Project, use `**find_parent`**(area_name, keywords) for candidate parents, then `**obsidian_create_task_note`**(parent_path, title, content) or `**append_tasks**`(parent_path, tasks). Document as a recommended step after **next-action-extract** so task-heavy ingests create proper task notes or append to existing hubs.

### 2.6 Optional: refactor to zettel

- **Where**: Pipelines Reference §1, report §5.1.
- **Change**: For literature/fleeting notes where atomic split is desired, document `**obsidian_refactor_to_zettel`**(input_path, output_folder, split: true/false) as an alternative or complement to **obsidian_split_atomic** (when split is true, server splits on ## and creates permanent zettel with frontmatter). No mandatory change to pipeline order; optional branch.
- **Constraint**: Only offer/apply when input note length > ~800 words or contains multiple clear `##` headings; otherwise prefer existing **obsidian_split_atomic** skill.

---

## 3. autonomous-organize pipeline

- **Where**: [Cursor-Skill-Pipelines-Reference.md](3-Resources/Cursor-Skill-Pipelines-Reference.md) §5, [auto-organize.mdc](.cursor/rules/context/auto-organize.mdc), [Second-Brain-Automations-Setup-Report.md](Ingest/2026-02-26-Second-Brain-Automations-Setup-Report.md) §5.5.
- **Change**:
  - Use `**obsidian_subfolder_organize`** (MCP) for 2–3 path candidates in re-org mode (replace or complement skill-based single path in mid-band). **Mid-band = 72–84% inclusive** for organize-path loop.
  - Insert verification chain in mid-band: **calibrate_confidence**(prior_output: path_conf, para_type, selected_path) → **verify_classification** → **obsidian_move_note**(..., `dry_run: true`) → then commit. Document in pipeline order and organize-path loop.
  - **Reuse the same fallback chain defined in §1.2 dry-run section** — do not duplicate fallback logic per pipeline. On move failure or `dry_run` risks: reference §1.2 (propose_alternative_paths → calibrate → verify → `dry_run` again → commit; else log and flag).
  - In **auto-organize.mdc**: Add requirement for `dry_run` before move and reference MCP fallback table for dry_run/alternative paths.

---

## 4. autonomous-archive pipeline

- **Where**: [Cursor-Skill-Pipelines-Reference.md](3-Resources/Cursor-Skill-Pipelines-Reference.md) §3, [auto-archive.mdc](.cursor/rules/context/auto-archive.mdc), [Second-Brain-Automations-Setup-Report.md](Ingest/2026-02-26-Second-Brain-Automations-Setup-Report.md) §5.3.
- **Change**:
  - After **archive-check** (≥85%) and before **subfolder-organize** / move: if **mid-band (72–84% inclusive)** post-check, run **calibrate_confidence** → **verify_classification**(calibrated_output with archive path) → **obsidian_move_note**(..., `dry_run: true`) → then commit after snapshot. Use **obsidian_subfolder_organize** for archive path candidates where applicable.
  - **Reuse the same fallback chain defined in §1.2 dry-run section** — do not duplicate fallback logic per pipeline.
  - Document in pipeline table and archive confidence bands; add `dry_run` requirement in auto-archive.mdc.

---

## 5. autonomous-express pipeline

- **Where**: [Cursor-Skill-Pipelines-Reference.md](3-Resources/Cursor-Skill-Pipelines-Reference.md) §4, [auto-express.mdc](.cursor/rules/context/auto-express.mdc), [Second-Brain-Automations-Setup-Report.md](Ingest/2026-02-26-Second-Brain-Automations-Setup-Report.md) §5.4.
- **Change**:
  - Complement or optionally replace the first step of **related-content-pull** with `**obsidian_suggest_connections`**(note_path, num_suggestions, auto_insert, suggested_links). Use client LLM to rank and pass suggested_links with `auto_insert: true` to append a Related section. **If `auto_insert: true` is used, wrap inserted Related section in a collapsible callout `[!related]` to keep notes visually clean.**
  - For hub-like notes: add optional step `**obsidian_append_to_moc`**(source_path, moc_path, section, line) or `**obsidian_generate_moc`**(topic, moc_path, tag/folder, content) after outline generation. Document in pipeline and skill catalog (§6 in report).

---

## 6. autonomous-distill pipeline

- **Where**: [Cursor-Skill-Pipelines-Reference.md](3-Resources/Cursor-Skill-Pipelines-Reference.md) §2, [Second-Brain-Automations-Setup-Report.md](Ingest/2026-02-26-Second-Brain-Automations-Setup-Report.md) §5.2.
- **Change**: **Strongly recommended** for batch mode (>5 notes): use `**obsidian_garden_review`**(scope/folder, focus: **distill_candidates**, output_path, auto_apply) to pre-select notes that need distill; then run autonomous-distill on that set. Optional for single-note triggers. Document as “strongly recommended batch init when >5 notes” in pipeline order and report.

---

## 7. New flows and triggers

### 7.1 Garden review (new trigger)

- **Where**: [Cursor-Skill-Pipelines-Reference.md](3-Resources/Cursor-Skill-Pipelines-Reference.md) trigger table and new subsection, [Second-Brain-Automations-Setup-Report.md](Ingest/2026-02-26-Second-Brain-Automations-Setup-Report.md) §2 and §8.
- **Change**: Add trigger phrases: “GARDEN REVIEW”, “run garden review”, “orphans and distill candidates”, **“garden health”**, **“vault orphans”**, **“distill candidates sweep”**. Flow: `**obsidian_garden_review`**(scope, focus: orphans | distill_candidates | weak_links | all, output_path optional, auto_apply). Suggest `**auto_apply: false` by default** during initial adoption (safer). Downstream: use report to feed autonomous-distill and autonomous-organize batches. Add to report §2 (triggers) and §8 (extensions); add pipeline entry in Pipelines Reference (no new context rule required if trigger is interpreted by existing rules).

### 7.2 Curate cluster (new trigger)

- **Where**: Same as 7.1.
- **Change**: Add triggers: “CURATE CLUSTER #tag”, “suggest gaps and merges for 3-Resources”, **“cluster curate #tag”**, **“theme gaps #tag”**, **“merge suggestions 3-Resources/…”**. Flow: `**obsidian_curate_cluster`**(query: tag or folder, note_list optional, actions: suggest_gaps, suggest_merges, generate_synthesis). Suggest `**auto_apply: false` by default** during initial adoption. Client LLM analyzes report and can call obsidian_split_atomic, obsidian_generate_moc, or merge proposals. Document in §2 and §8 and Pipelines Reference.

---

## 8. Documentation and reference alignment

- **Second-Brain-Automations-Setup-Report.md**  
  - §2: New triggers (GARDEN REVIEW, CURATE CLUSTER).  
  - §3.1: ensure_backup vs create_backup.  
  - §3.5 or new §3.6: health_check and MCP-Health-YYYY-MM.md / MCP-Observability.md.  
  - §4.4, §5.1: Ingest bootstrap, verification chain, dry_run, task rerouting, optional refactor_to_zettel.  
  - §5.2: Distill optional garden_review pre-step.  
  - §5.3: Archive calibration/verify/dry_run chain.  
  - §5.4: Express suggest_connections and MOC steps.  
  - §5.5: Organize subfolder_organize MCP, calibration/verify/dry_run.  
  - §7: Dry-run requirement and fallback row for dry_run/alternative paths.  
  - §8: How to extend (reference new flows and MCP tools).
  - **After each phase**, re-run a small ingest batch (3–5 known notes) and verify in logs: `dry_run` usage, calibration/verification calls, backup existence, and `#review-needed` rate before/after.
- **Cursor-Skill-Pipelines-Reference.md**  
  - Update flowchart and tables for ingest (bootstrap, calibrate, verify, dry_run, propose_alternative_paths, task steps).  
  - Update organize, archive, express, distill with new steps and dry_run.  
  - Add entries for Garden Review and Curate Cluster (trigger → flow, no new rule file if handled by existing context).
- **.cursor/rules/always/mcp-obsidian-integration.mdc**  
  - Dry-run requirement for move_note.  
  - Fallback row: dry_run fails or risks → propose_alternative_paths → calibrate → verify → retry; else log.  
  - Optional: mention ensure_backup for batches.
- **Context rules**  
  - **ingest-processing.mdc**: Enforce dry_run in move rules.  
  - **auto-organize.mdc**: Dry_run before move; reference fallback.  
  - **auto-archive.mdc**: Verification chain and dry_run before move.

---

## 9. Confidence impact (summary)


| Enhancement                              | Estimated impact                                                             | Tools                                                               |
| ---------------------------------------- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| Mid-band refinement (calibrate + verify) | +10–15% resolution to ≥85%                                                   | calibrate_confidence, verify_classification                         |
| Pre-move gates and dry_run               | Reduce errors 20–30%                                                         | dry_run: true, propose_alternative_paths                            |
| Multi-candidate paths                    | +5–10% accuracy, better fallbacks                                            | obsidian_subfolder_organize                                         |
| Bootstrap and pre-selection              | Early structure, targeted runs                                               | bootstrap_project_batch, obsidian_garden_review                     |
| Observability                            | Proactive issue detection                                                    | health_check, obsidian_ensure_backup                                |
| **Overall expected**                     | +15–25% fewer #review-needed entries, higher destructive-action success rate | Combined effect of layered verification + fallbacks + observability |


---

## 10. Implementation order (suggested)

1. **Phase 1 – Safety and docs**: §1.1 (ensure_backup), §1.2 (`dry_run` + fallback table), §1.3 (health_check). Update mcp-obsidian-integration.mdc and report §3, §7. **Validation step**: Process 5–10 sample Ingest notes → check logs for new MCP calls, `dry_run` behavior, backup invariant, confidence lifts.
2. **Phase 2 – Ingest**: §2.1–2.4 (bootstrap, MCP path candidates, calibration/verification, pre-move chain, fallback). Update Pipelines Reference §1, report §4.4 and §5.1, ingest-processing.mdc. **Validation step**: Same as Phase 1.
3. **Phase 3 – Organize and archive**: §3 and §4. Update Pipelines Reference and auto-organize.mdc, auto-archive.mdc, report §5.3 and §5.5. **Validation step**: Same as Phase 1.
4. **Phase 4 – Express and distill**: §5 and §6. Update Pipelines Reference and report §5.2 and §5.4. **Validation step**: Same as Phase 1.
5. **Phase 5 – New flows and polish**: §7 (Garden Review, Curate Cluster), §2.5–2.6 (task rerouting, refactor_to_zettel), §8 (full doc pass). **Validation step**: Same as Phase 1.

No new Cursor skill files are required; all behavior is MCP tools + documentation and rule edits. After each phase, re-run a small ingest batch (3–5 known notes) and verify in logs: `dry_run` usage, calibration/verification calls, backup existence, and `#review-needed` rate before/after.