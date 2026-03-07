---
title: Automation Flows — MCP Server Improvement Proposals
created: 2026-02-26
updated: 2026-02-27
tags: [pkm, automation, cursor, obsidian, mcp, pipelines, improvement]
para-type: resource
status: active
links: 
source: Cross-reference of MCP server tools vs. Second-Brain Automations Setup Report
---
**Changelog**: 2026-02-27 — Implemented task-reroute skill per Task Rerouting and Recursive Checklist plan; ingest pipeline now invokes task-reroute after next-action-extract when task-like and confidence ≥78%; MCP find_parent, obsidian_create_task_note, append_tasks wired via skill.

### Purpose

This note cross-references the **[[2026-02-26-Second-Brain-Automations-Setup-Report]]** with the **Obsidian MCP server** (obsidian-para-zettel-autopilot) and proposes concrete improvements to automation flows using MCP tools that are either underused or not yet wired into the documented pipelines.

---

## 1. Cross-reference: Report vs. MCP tools

| Report section / flow | MCP tools currently assumed | Additional MCP tools available |
|------------------------|----------------------------|---------------------------------|
| §3 Safety (backups) | `obsidian_create_backup` | **`obsidian_ensure_backup`** — verify recent backup (max_age_minutes) before destructive ops or after long batches |
| §4–§5 Ingest pipeline | classify, frontmatter-enrich, subfolder-organize (skill), move, log | **`bootstrap_project_batch`**, **`confirm_bootstrap`**, **`obsidian_list_projects`** — project seed detection; **`obsidian_subfolder_organize`** (MCP) — path candidates with scores; **`append_tasks`**, **`find_parent`**, **`obsidian_create_task_note`** — task rerouting |
| §5.1–5.5 Confidence loops | LLM self-critique (confidence-loops.mdc) | **`calibrate_confidence`** — mid-band refinement with user-memory + critique; **`verify_classification`** — pre-move verification; **`propose_alternative_paths`** — fallback paths on failure |
| §5 Move / organize / archive | `obsidian_move_note`, `obsidian_ensure_structure` | **`obsidian_move_note(..., dry_run: true)`** — preview effects (path, backup status, risks) before commit |
| §5.4 Express (related content) | related-content-pull (skill) | **`obsidian_suggest_connections`** — semantic related notes + optional auto_insert of Related section |
| §6 Skills (no MOC/hub detail) | append_to_hub (MCP) | **`obsidian_append_to_moc`**, **`obsidian_generate_moc`** — MOC curation and generation |
| Not in report | — | **`obsidian_garden_review`** — orphans, distill candidates, weak_links; **`obsidian_curate_cluster`** — gaps, merges, synthesis; **`obsidian_refactor_to_zettel`** — literature → atomic zettel; **`health_check`** — MCP observability |

---

## 2. Proposed improvements by pipeline

### 2.1 full-autonomous-ingest

- **Bootstrap before classify**  
  At pipeline start, call **`bootstrap_project_batch`** with `paths` from `obsidian_list_notes("Ingest")` and `existing_projects_json` from **`obsidian_list_projects`**. If a seed project is detected (≥85%), either apply project creation or set `requires_confirmation` and have the agent ask the user, then **`confirm_bootstrap`** to apply in one step.  
  *Reference: Report §4.4, §5.1.*

- **Use MCP `obsidian_subfolder_organize` in refinement**  
  In mid-band (72–84%), use the **MCP** `obsidian_subfolder_organize` (path, para_type, max_candidates) to get 2–3 candidate paths with scores and rationale instead of (or in addition to) the skill’s single path. Feed the best candidate into **`calibrate_confidence`** and then **`verify_classification`** before any move.  
  *Reference: Report §5.1, confidence-loops.mdc.*

- **Pre-move verification chain**  
  Before **`obsidian_move_note`**: run **`calibrate_confidence`** (when in mid-band) → **`verify_classification`** (note_path, calibrated_output) → **`obsidian_move_note`(path, new_path, dry_run: true)**. Only call move with `dry_run: false` when verdict is "safe to move" and dry_run preview is acceptable.  
  *Reference: Report §3.3, §7.*

- **Fallback paths on move failure**  
  If move fails (e.g. missing parent) or dry_run surfaces risks: call **`propose_alternative_paths`** (note_path, para_context, max_candidates) → feed top candidate into **`calibrate_confidence`** for one retry → **`verify_classification`** → move. If still failing, log with `#review-needed` and full trace.  
  *Reference: Report §7 fallback table.*

- **Task rerouting**  
  **Implemented** via the **task-reroute** skill (`.cursor/skills/task-reroute/SKILL.md`). After **next-action-extract**, when confidence ≥78% and the note is task-like (weighted score ≥70), the pipeline runs task-reroute: **`find_parent`** (area_name, keywords) or project path from frontmatter → **`obsidian_create_task_note`** (new task note) or **`append_tasks`** (append to existing parent). Per-change snapshot of the **target** note before append_tasks; log to Ingest-Log. See [[3-Resources/Cursor-Skill-Pipelines-Reference]] ingest table and pipeline order.  
  *Reference: Report §5.1 next-action-extract.*

### 2.2 autonomous-organize

- **Path candidates and verification**  
  Use **`obsidian_subfolder_organize`** (MCP) for 2–3 path candidates in re-org mode. In mid-band, run **`calibrate_confidence`** (prior_output: path_conf, para_type, selected_path) → **`verify_classification`** → **`obsidian_move_note`(..., dry_run: true)** then commit.  
  *Reference: Report §5.5, auto-organize.mdc.*

- **Alternative paths on failure**  
  On move failure or dry_run risks, use **`propose_alternative_paths`** → **`calibrate_confidence`** (one retry) → verify → move; else log and flag.  
  *Reference: Report §7.*

### 2.3 autonomous-archive

- **Same verification chain**  
  After **archive-check** (≥85%) and before **subfolder-organize** / **move**: **`calibrate_confidence`** (if mid-band) → **`verify_classification`** (calibrated_output with archive path) → **`obsidian_move_note`(..., dry_run: true)** → then commit after snapshot.  
  *Reference: Report §5.3, auto-archive.mdc.*

### 2.4 autonomous-express

- **Related content via MCP**  
  Complement or optionally replace the first step of **related-content-pull** with **`obsidian_suggest_connections`** (note_path, num_suggestions, auto_insert, suggested_links). Use client LLM to rank and pass `suggested_links` with `auto_insert: true` to append a Related section.  
  *Reference: Report §5.4.*

- **MOC integration**  
  When a note becomes a natural “hub” for a theme, use **`obsidian_append_to_moc`** (source_path, moc_path, section, line) or **`obsidian_generate_moc`** (topic, moc_path, tag/folder, content) so express runs can maintain MOCs alongside hub appends.  
  *Reference: Report §6 skill catalog; MOCs not in report.*

### 2.5 autonomous-distill

- **No change to core steps**  
  Optional: use **`obsidian_garden_review`** (scope, focus: distill_candidates) to pre-select notes that need distill; then run autonomous-distill on that set.  
  *Reference: Report §5.2.*

---

## 3. New flows using MCP-only tools

### 3.1 Garden review (new trigger)

- **Trigger**: e.g. *"GARDEN REVIEW"*, *"run garden review"*, *"orphans and distill candidates"*.
- **Flow**: Call **`obsidian_garden_review`** with scope (e.g. `folder:3-Resources` or `all`), focus `orphans` | `distill_candidates` | `weak_links` | `all`, optional **output_path** (e.g. `3-Resources/Garden-Review-YYYY-MM-DD.md`), and **auto_apply** true/false (set frontmatter like `needs-distill: true`, `orphan: true` with backups).
- **Downstream**: Use the report (and optional flags) to feed **autonomous-distill** and **autonomous-organize** batches.  
  *Reference: Report §2 trigger phrases; no garden flow today.*

### 3.2 Curate cluster (new trigger)

- **Trigger**: e.g. *"CURATE CLUSTER #tag"*, *"suggest gaps and merges for 3-Resources"*.
- **Flow**: Call **`obsidian_curate_cluster`** (query: tag or folder, optional note_list, actions: suggest_gaps, suggest_merges, generate_synthesis). Client LLM analyzes the report and can call **obsidian_split_atomic**, **obsidian_generate_moc**, or merge proposals.  
  *Reference: Report §6; no cluster-curation flow.*

### 3.3 Refactor to zettel (ingest alternative)

- **When**: In **full-autonomous-ingest**, if the note is classified as literature or fleeting and atomic split is desired, consider **`obsidian_refactor_to_zettel`** (input_path, output_folder, split: true/false) as an alternative or complement to **`obsidian_split_atomic`**. When split is true, server splits on `##` and creates permanent zettel notes with frontmatter.  
  *Reference: Report §5.1 split_atomic; Zettelkasten not in pipeline.*

### 3.4 Health and observability

- **When**: Every N notes (e.g. 10) in a batch, or on first error in a run, call **`health_check`**. Log result (status, metrics, serverIdentifier) to **Backup-Log.md** or a small **3-Resources/MCP-Observability.md** for connectivity, vault path, backup dir writability, and recent errors.  
  *Reference: Report §3.5 logging.*

---

## 4. Safety and backup

- **Explicit ensure_backup**  
  Before long batches or after a gap (e.g. >15 minutes), call **`obsidian_ensure_backup`** (path, max_age_minutes) to confirm a recent backup exists instead of blindly calling **`obsidian_create_backup`** again. Reduces redundant backups while keeping the “backup exists” invariant.  
  *Reference: Report §3.1.*

- **Dry-run before every move**  
  Document and enforce: for any **`obsidian_move_note`** at ≥85% confidence, first call with **dry_run: true**, review proposed effects (path, new_path, backup status, risks e.g. dangling links), then call again with **dry_run: false** to commit.  
  *Reference: Report §7; MCP move_note supports dry_run.*

---

## 5. Summary table: MCP tool → improvement

| MCP tool | Improvement |
|----------|-------------|
| **calibrate_confidence** | Use in all pipelines for mid-band (72–84%) refinement; integrate with user-memory and shared self-critique. |
| **verify_classification** | Run after calibrate_confidence, before every move; gate on verdict "safe to move". |
| **propose_alternative_paths** | On move failure or dry_run risks; one retry with calibrate → verify → move. |
| **obsidian_subfolder_organize** | Use MCP for 2–3 path candidates in ingest, organize, archive; feed into calibration/verification. |
| **obsidian_move_note(dry_run: true)** | Always dry_run before commit; document in report and rules. |
| **obsidian_ensure_backup** | Optional pre-check before destructive batches; avoid redundant create_backup. |
| **bootstrap_project_batch** + **confirm_bootstrap** + **obsidian_list_projects** | Ingest: detect project seed, create project or confirm with user before classify. |
| **find_parent** + **append_tasks** + **obsidian_create_task_note** | Ingest: task rerouting and task-note creation under Areas/Projects. |
| **obsidian_suggest_connections** | Express: related content with optional auto_insert. |
| **obsidian_append_to_moc** / **obsidian_generate_moc** | Express/organize: MOC curation and generation. |
| **obsidian_garden_review** | New GARDEN REVIEW flow; feed distill/organize. |
| **obsidian_curate_cluster** | New CURATE CLUSTER flow; gaps, merges, synthesis. |
| **obsidian_refactor_to_zettel** | Ingest option for literature/fleeting → atomic zettel. |
| **health_check** | Periodic or on-error; log to Backup-Log or MCP-Observability. |

---

## 6. Documentation updates

- **[[2026-02-26-Second-Brain-Automations-Setup-Report]]**: Add a subsection under §2 or §8 listing the new triggers (GARDEN REVIEW, CURATE CLUSTER) and under §5 the verification chain (calibrate_confidence → verify_classification → move dry_run → commit). Extend §7 to require dry_run before move.
- **Cursor Skill Pipelines Reference**: Register bootstrap_project_batch at ingest start; add calibrate_confidence and verify_classification to the canonical pipeline tables for ingest, organize, archive; add optional MOC and garden/curate steps where relevant.
- **mcp-obsidian-integration.mdc**: Document dry_run usage for obsidian_move_note; add fallback row for “move dry_run fails or risks” → propose_alternative_paths → calibrate → verify → retry.

---

## 7. Changelog

| Date       | Change |
|-----------|--------|
| **2026-02-26** | Companion created; cross-reference with Automations Setup Report and MCP tool descriptors; improvement proposals for ingest, organize, archive, express, distill; new flows (garden review, curate cluster, refactor-to-zettel, health_check); safety (ensure_backup, dry_run). |

## Review Needed
Proposed para-type: resource. Assigned based on content/frontmatter (confidence ~70%). Do not move until reviewed.