---
para-type: Archive
status: archived
---
# System Audit Report — Second Brain PARA-Zettel Autopilot

**Date:** 2026-03-06  
**Scope:** Comprehensive audit of Obsidian vault layout, Cursor rules and skills, MCP tools, pipelines, configs, parameters, queues, logs, templates, naming, highlighting, user flows, system diagrams, and related components.  
**Basis:** Canonical documents in `3-Resources/Second-Brain/` and `3-Resources/Second-Brain/Second-Brain-User-Flows/` (Skills-Structure-*, Cursor-Skill-Pipelines-Reference, User-Flow-*, System-Diagram-*, Second-Brain-Summary, Second-Brain-Config, Parameters, Vault-Layout, Queue-Alias-Table, Pipelines, Rules, Skills, Logs, Templates, Naming-Conventions, Color-Coded-Highlighting, Testing, Configs, Queue-Sources, MCP-Tools, Backbone, README, Responsibilities-Breakdown, PARA-Actionability-Rubric, Cursor-Project-Rules-Summary, Regression-Stability-Log, Second-Brain-Limitations, etc.).

---

## 1. Rules

| Component | Status | Evidence / Gap | Recommendation |
|-----------|--------|----------------|-----------------|
| Always-applied rules (8) | **Built** | All present: `00-always-core`, `mcp-obsidian-integration`, `second-brain-standards`, `confidence-loops`, `guidance-aware`, `always-ingest-bootstrap`, `watcher-result-append`, `backbone-docs-sync`. Rules.md table matches `.cursor/rules/always/*.mdc`. | — |
| Context rules (17) | **Built** | All present: para-zettel-autopilot, auto-eat-queue, auto-queue-processor, auto-distill, auto-archive, auto-express, auto-organize, ingest-processing, non-markdown-handling, snapshot-sweep, auto-restore, auto-resurface, auto-highlight-perspective, mobile-seed-detect, auto-distill-perspective, auto-express-view, auto-async-cascade. | — |
| Trigger → rule mapping | **Built** | Pipelines.md and Cursor-Skill-Pipelines-Reference trigger tables align with context rules. | — |
| Mid-band numeric range | **Inconsistency** | **confidence-loops.mdc** and **Parameters.md**: mid-band = 68–84%. **auto-archive.mdc**: "Mid (72 ≤ archive_conf ≤ 84)"; **auto-organize.mdc**: "Mid (72 ≤ path_conf ≤ 84)". Cursor-Skill-Pipelines-Reference §3 and §5 state "68 ≤ archive_conf ≤ 84" and "68 ≤ path_conf ≤ 84". | Standardize on **68–84%** in auto-archive.mdc and auto-organize.mdc to match confidence-loops and Parameters; or document an intentional archive/organize-specific 72% floor in Parameters.md. |
| Task-Decision wrapper lineage | **Partial** | Rules.md § "Task-Decision wrappers and decision lineage" describes appending a provenance block to `target_note` on apply; apply-from-wrapper table in Cursor-Skill-Pipelines-Reference does not list task-decision. | Add task-decision apply semantics to apply-from-wrapper table and auto-eat-queue Step 0 (or document as future). |
| Cursor-Project-Rules-Summary | **Partial** | References "always-core-interaction", "always-frontmatter-naming", "auto-logging" and older filename format (YYYY-MM-DD-kebab); current always rules use different names and Naming-Conventions use slug-first with date at end. | Update Cursor-Project-Rules-Summary to match current rule set and naming (kebab-slug-YYYY-MM-DD-HHMM). |

---

## 2. Skills

| Component | Status | Evidence / Gap | Recommendation |
|-----------|--------|----------------|-----------------|
| Pipeline skills (36 SKILL.md) | **Built** | All 36 skills under `.cursor/skills/` have SKILL.md; Cursor-Skill-Pipelines-Reference skill locations table matches. | — |
| prompt-crafter | **Doc-only** | Skills.md: "prompt-crafter (doc-only; optional skill)". No `.cursor/skills/prompt-crafter/SKILL.md`. Templates.md and User-Flow-Prompt-Crafter-* describe assembly from Config/templates. | Either implement prompt-crafter as a skill (with SKILL.md) or keep as doc-only and reference it only where "when implemented" is stated. |
| Apply-from-wrapper skills | **Built** | distill-apply-from-wrapper, express-apply-from-wrapper exist and are referenced in Queue-Sources and Cursor-Skill-Pipelines-Reference. | — |
| Skills by pipeline | **Built** | Skills.md and Cursor-Skill-Pipelines-Reference pipeline order and skill slots align with context rules. | — |
| SWITCH HIGHLIGHT ANGLE / HIGHLIGHT MULTI-ANGLE | **Gap** | Skills.md highlighter flow diagram shows triggers "SWITCH HIGHLIGHT ANGLE", "HIGHLIGHT MULTI-ANGLE"; Queue-Alias-Table and Pipelines trigger table do not list these. | Add to Queue-Alias-Table and Pipelines (or remove from Skills diagram if not implemented). |

---

## 3. Pipelines

| Component | Status | Evidence / Gap | Recommendation |
|-----------|--------|----------------|-----------------|
| full-autonomous-ingest (two-phase) | **Built** | Phase 1 (propose + Decision Wrapper) and Phase 2 (apply-mode via EAT-QUEUE) documented in Pipelines.md, Cursor-Skill-Pipelines-Reference, para-zettel-autopilot. | — |
| autonomous-distill, archive, express, organize | **Built** | All four pipelines documented with skill order, confidence bands, and snapshot triggers; context rules and reference align. | — |
| Queue processor (EAT-QUEUE) | **Built** | auto-eat-queue.mdc, Queue-Sources, Step 0 (wrappers), canonical order, Watcher-Result contract. | — |
| Task/roadmap queue | **Built** | auto-queue-processor, Task-Queue.md modes, add-roadmap-append, task-complete-validate, expand-road-assist, etc. | — |
| bootstrap_project_batch | **Partial** | Cursor-Skill-Pipelines-Reference §1: "After list_notes, call list_projects and bootstrap_project_batch … before classify_para." Optional/defensive; not all ingest runs may call it. | Document when to skip (e.g. no project seed) so agents do not assume it always runs. |
| Garden review / Curate cluster | **Partial** | Cursor-Skill-Pipelines-Reference: "Garden review" and "Curate cluster" flows via `obsidian_garden_review`, `obsidian_curate_cluster`; "interpret by agent; no dedicated context rule". | Add optional context rule or document trigger phrases in Queue-Alias-Table so dispatch is unambiguous. |
| Connection Ingest | **Missing** | Second-Brain-Limitations: "The planned **Connection Ingest** plugin is not currently implemented." Spec exists (Cursor-Ingest/2026-02-24-connection-ingest-plugin-spec.md); no plugin under `.obsidian/plugins/`. | Leave as documented limitation; implement when prioritised. |
| Snapshot triggers table | **Built** | Cursor-Skill-Pipelines-Reference § Snapshot triggers (all pipelines) and Pipelines § Snapshot triggers summary align; per-pipeline per-change and batch frequency documented. | — |

---

## 4. MCP Tools

| Component | Status | Evidence / Gap | Recommendation |
|-----------|--------|----------------|-----------------|
| Tool groups (Core, Backup, Move, PARA, Content, Tasks, Confidence, Batch, MOC, Other) | **Built** | MCP-Tools.md table matches tool descriptors under `mcps/user-obsidian-para-zettel-autopilot/tools/*.json` (40+ tools). | — |
| propose_para_paths | **Built** | MCP-Tools documents params (path, context_mode, rationale_style, max_candidates); descriptor is `propose_para_paths.json`. | Doc reference uses MCP tool name. |
| obsidian_ensure_backup, create_backup | **Built** | Documented; backup gate and ensure_backup vs create_backup in mcp-obsidian-integration. | — |
| move_note dry_run | **Built** | Documented in MCP-Tools, mcp-obsidian-integration, and all move-using pipelines. | — |
| obsidian_suggest_connections | **Built** | In MCP-Tools Content group; express pipeline and Cursor-Skill-Pipelines-Reference reference it. | — |

---

## 5. User Flows & System Diagrams

| Component | Status | Evidence / Gap | Recommendation |
|-----------|--------|----------------|-----------------|
| System-Diagram (High / Mid / Detailed) | **Built** | Second-Brain-User-Flows/System-Diagram-High-Level.md, System-Diagram-Mid-Level.md, System-Diagram-Detailed.md exist with Mermaid. | — |
| User-Flow-Diagram (High / Mid / Detailed) | **Built** | User-Flow-Diagram-High-Level.md, User-Flow-Diagram-Mid-Level.md, User-Flow-Diagram-Detailed.md in Second-Brain-User-Flows. | — |
| User-Flow-Skills (High / Mid / Detailed) | **Built** | User-Flow-Skills-High-Level.md, User-Flow-Skills-Mid-Level.md, User-Flow-Skills-Detailed.md. | — |
| User-Flow-Rules (High / Mid / Detailed) | **Built** | User-Flow-Rules-High-Level.md, User-Flow-Rules-Mid-Level.md, User-Flow-Rules-Detailed.md. | — |
| User-Flow-Prompt-Crafter (High / Mid / Detailed) | **Built** | User-Flow-Prompt-Crafter-High-Level.md, User-Flow-Prompt-Crafter-Mid-Level.md, User-Flow-Prompt-Crafter-Detailed.md. | — |
| Skills-Structure / Rules-Structure / Prompt-Crafter-Structure | **Built** | High-Level, Mid-Level, Detailed variants exist in Second-Brain-User-Flows. | — |
| Cross-references from backbone | **Built** | Backbone and README point to Pipelines, Logs, Vault-Layout, etc.; no broken internal links found in audited docs. | — |

---

## 6. Configs

| Component | Status | Evidence / Gap | Recommendation |
|-----------|--------|----------------|-----------------|
| Second-Brain-Config | **Built** | hub_names, archive, highlight, graph, queue, snapshot, depths, confidence_bands documented; multiple roots (3-Resources/Second-Brain-Config.md, 3-Resources/Second-Brain/Second-Brain-Config.md). | Prefer one canonical path and link from Configs.md to avoid drift. |
| MCP env (BACKUP_DIR, SNAPSHOT_DIR, BATCH_SNAPSHOT_DIR, etc.) | **Built** | Configs.md table and mcp-obsidian-integration snapshot configuration align. | — |
| batch_size_for_snapshot | **Built** | In Second-Brain-Config under snapshot; mcp-obsidian-integration and Pipelines reference it. | — |
| Exclusions canonical list | **Built** | Configs.md and Vault-Layout list Backups/, Logs, Hubs, Watcher paths, .technical/, tests/, watcher-protected. | — |
| exclusions.yaml | **Gap** | Configs.md: "Optional: maintain a machine-readable exclusions.yaml in this folder." Not present. | Add only if tooling or automation will consume it. |

---

## 7. Parameters

| Component | Status | Evidence / Gap | Recommendation |
|-----------|--------|----------------|-----------------|
| Confidence bands (high ≥85%, mid 68–84%, low <68%) | **Built** | Parameters.md and confidence-loops.mdc; tunable via Second-Brain-Config. | Fix archive/organize context rules to 68–84% (see Rules). |
| Loop fields (loop_attempted, pre_loop_conf, post_loop_conf, etc.) | **Built** | Parameters.md and Cursor-Skill-Pipelines-Reference log format; pipeline rules require these in logs. | — |
| user_guidance, guidance_conf_boost, decision_candidate, decision_priority | **Built** | Parameters.md and guidance-aware.mdc. | — |
| clear_guidance_after_run | **Partial** | guidance-aware: "Clearing or archiving user_guidance after a successful run is configurable … Implementation of the clear step is a follow-up." | Implement when desired or remove "follow-up" and mark as optional. |
| Queue modes (prompt-queue, Task-Queue) | **Built** | Parameters.md and Queue-Sources list modes; Queue-Alias-Table maps triggers to modes. | — |

---

## 8. Queues

| Component | Status | Evidence / Gap | Recommendation |
|-----------|--------|----------------|-----------------|
| prompt-queue.jsonl location and format | **Built** | `.technical/prompt-queue.jsonl`; Queue-Sources and Queue-Alias-Table; mode, prompt, source_file, id, params. | — |
| Task-Queue.md | **Built** | 3-Resources/Task-Queue.md; modes TASK-ROADMAP, TASK-COMPLETE, ADD-ROADMAP-ITEM, etc. | — |
| .cursorignore and queue visibility | **Verified** | Queue-Sources: "ensure .cursorignore does not hide it — add !.technical/prompt-queue.jsonl". Repo `.cursorignore` contains `!.technical/prompt-queue.jsonl` (after `.technical/**` and `*.jsonl`); queue file is visible to Cursor. | — |
| CHECK_WRAPPERS | **Built** | Step 0 always-check wrappers; CHECK_WRAPPERS is internal; Ingest-Log CHECK_WRAPPERS prefix for greppability. | — |
| Canonical order | **Built** | INGEST → ORGANIZE → TASK-ROADMAP → DISTILL → EXPRESS → ARCHIVE → TASK-COMPLETE → ADD-ROADMAP-ITEM in Queue-Sources and Queue-Alias-Table. | — |

---

## 9. Logs

| Component | Status | Evidence / Gap | Recommendation |
|-----------|--------|----------------|-----------------|
| Pipeline logs (Ingest, Distill, Archive, Express, Organize, Name-Review, Backup, Feedback, Prompt, Wrapper-Sync, Errors) | **Built** | Logs.md table; locations 3-Resources/*.md. Files exist or are created on first write. | — |
| Log line format and loop_* fields | **Built** | Cursor-Skill-Pipelines-Reference and Logs.md; backup path and snapshot path in changes string. | — |
| Vault-Change-Monitor MOC | **Built** | 3-Resources/Vault-Change-Monitor.md exists; Logs.md describes log → MOC flow. | — |
| Errors.md entry structure | **Built** | Heading, metadata table, #### Trace, #### Summary; Error Handling Protocol in mcp-obsidian-integration. | — |
| log-rotate skill | **Built** | .cursor/skills/log-rotate/SKILL.md; Logs.md references rotation to Logs-Archive. | — |
| Restore-Queue format | **Partial** | Logs.md and mcp-obsidian-integration describe restore-queue mode (user-maintained list); format documented. Implementation is user-triggered only. | — |

---

## 10. Templates

| Component | Status | Evidence / Gap | Recommendation |
|-----------|--------|----------------|-----------------|
| Templates/ and Decision-Wrapper | **Built** | Templates/Decision-Wrapper.md exists; A–G, wrapper_type, original_path, no default approved. | — |
| Prompt-Components (laptop) | **Built** | Templates.md: Templates/Prompt-Components/ for prompt-crafter assembly. | Verify folder and expected snippets exist if prompt-crafter is used. |
| Chat-Prompts | **Partial** | Templates.md and Chat-Prompts.md; optional Templates/Chat-Prompts/. | — |
| Ingest/By-Type | **Partial** | Templates.md: "Templates/Ingest/By-Type/"; referenced for Ingest-Selector. | Confirm path exists if pipelines depend on it. |
| Standard callouts (proposal, preview, success, feedback) | **Built** | Templates.md documents text and usage. | — |

---

## 11. Naming Conventions

| Component | Status | Evidence / Gap | Recommendation |
|-----------|--------|----------------|-----------------|
| Core format kebab-slug-YYYY-MM-DD-HHMM | **Built** | Naming-Conventions.md; date and time at end; referenced by second-brain-standards, subfolder-organize, name-enhance. | — |
| MOCs, Hubs, PMG patterns | **Built** | Naming-Conventions.md; * Hub.md, *Master*Goal*; name-enhance protections. | — |
| Date/slug source priority | **Built** | created frontmatter, file stat, ingest/current date. | — |

---

## 12. Highlighting

| Component | Status | Evidence / Gap | Recommendation |
|-----------|--------|----------------|-----------------|
| Color-Coded-Highlighting and Highlightr-Color-Key | **Built** | Color-Coded-Highlighting.md; master key semantics; project highlight_key; analogous/complementary. | — |
| distill-highlight-color, layer-promote, highlight-perspective-layer | **Built** | Skills and pipeline order; perspective/lens from frontmatter and triggers. | — |
| highlight_angles, data-drift-level | **Built** | Skills.md and highlight-perspective-layer; express-mini-outline can read highlight_angles. | — |

---

## 13. Testing

| Component | Status | Evidence / Gap | Recommendation |
|-----------|--------|----------------|-----------------|
| tests/ layout (unit, integration, fixtures, sb_contracts) | **Built** | Testing.md; 3-Resources/Second-Brain/tests/; exclusions so pipelines do not process tests. | — |
| Run instructions | **Built** | Testing.md: unittest discover and run_tests.py --repl. | — |
| PARA regression and Regression-Stability-Log | **Partial** | Regression-Stability-Log.md and para-regression.md; flip-rate metric and baseline table are TODO. | Fill baseline row when first run is done; document rubric version. |
| Responsibilities-Breakdown vs tests | **Gap** | Responsibilities-Breakdown describes pipeline/skill ownership; Testing.md does not explicitly map tests to responsibility boundaries. | Optional: add a short "Test coverage by responsibility" to Testing.md. |

---

## 14. Vault Layout

| Component | Status | Evidence / Gap | Recommendation |
|-----------|--------|----------------|-----------------|
| Folder blacklist (00 Inbox, 10 Zettelkasten, 99 Attachments, 99 Templates) | **Built** | Vault-Layout.md and mcp-obsidian-integration; canonical names Ingest, Templates, 5-Attachments. | — |
| PARA + Ingest, Backups, Versions, .technical | **Built** | Vault-Layout folder table and full folder tree diagram. | — |
| Ingest/Decisions subfolders and archive mirror | **Built** | Vault-Layout § Ingest/Decisions subfolders; Re-Wrap; Wrapper-MOC at Ingest/Decisions/Wrapper-MOC.md (exists). | — |
| Root-level technical files | **Built** | .cursorignore, .stignore, .obsidianignore at root. | — |
| Exclusions flow | **Built** | Vault-Layout and Configs canonical list; context rules list exclusions. | — |

---

## 15. Other Referenced Components

| Component | Status | Evidence / Gap | Recommendation |
|-----------|--------|----------------|-----------------|
| PARA-Actionability-Rubric | **Built** | 3-Resources/Second-Brain/PARA-Actionability-Rubric.md; tie-breaker Projects > Areas > Resources > Archives; tools must follow. | — |
| Second-Brain-Limitations | **Built** | Connection Ingest not implemented; deep-nested move and split linking verified and documented. | — |
| Backbone, README, Responsibilities-Breakdown | **Built** | Present and cross-linked; Backbone narrative and README index match. | — |
| 2026-02-24-building-a-second-brain-code-para-summary | **Partial** | User list referenced "2026-02-24-building-a-second-brain-code-para-summary.md"; Second-Brain-Summary.md exists with BASB/CODE/PARA content (created 2026-02-21). May be same or related. | Clarify doc name if used in links. |

---

## Summary

### Overall health: **~85% complete**

- **Built/implemented:** Rules (25 files), skills (36 with SKILL.md), pipelines (ingest two-phase, distill, archive, express, organize, queue processor, task queue), MCP tool set, configs and parameters, queues and alias table, logs and destinations, templates (Decision-Wrapper, callouts), naming conventions, highlighting semantics, vault layout and exclusions, user-flow and system-diagram docs, PARA-Actionability-Rubric, Limitations, Backbone, README, Responsibilities-Breakdown. Safety invariants (backup-first, dry_run before move, ensure_structure, per-change/batch snapshots, Error Handling Protocol) are documented and wired into pipeline rules.

- **Missing/partial:** Connection Ingest (planned, not implemented); prompt-crafter (doc-only); bootstrap_project_batch and Garden/Curate flows (optional or "interpret by agent"); clear_guidance_after_run (follow-up); Task-Decision wrapper apply semantics (documented in Rules, not in apply-from-wrapper table); Regression-Stability-Log baseline (TODO); Cursor-Project-Rules-Summary and optional exclusions.yaml/Ingest-By-Type paths.

- **Gaps:** Mid-band range **72 vs 68** (closed: 68–84% everywhere); Skills diagram triggers SWITCH HIGHLIGHT ANGLE / HIGHLIGHT MULTI-ANGLE (closed: added to Queue-Alias-Table and Pipelines); .cursorignore for `.technical/prompt-queue.jsonl` (closed: verified — exception present in repo); optional test-coverage-by-responsibility.

- **Recommendations (priority):**
  1. **Safety / consistency:** Standardize mid-band to **68–84%** in auto-archive.mdc and auto-organize.mdc (or document 72% floor in Parameters).
  2. **Safety:** ~~Confirm `.cursorignore` does not hide `.technical/prompt-queue.jsonl`~~ — verified: `.cursorignore` contains `!.technical/prompt-queue.jsonl`.
  3. **Docs:** Update Cursor-Project-Rules-Summary to current rule names and naming (kebab-slug-YYYY-MM-DD-HHMM).
  4. **Completeness:** Add Task-Decision apply step to apply-from-wrapper table and Step 0 (or mark as future).
  5. **Clarity:** Align Skills highlighter diagram with Queue-Alias-Table (add or remove SWITCH HIGHLIGHT ANGLE / HIGHLIGHT MULTI-ANGLE).
  6. **Testing:** Run PARA regression once and fill Regression-Stability-Log baseline row.

No invented components; all findings are grounded in the listed canonical documents and current repo state.
