---
name: Second Brain backbone docs
overview: Create a dedicated `3-Resources/Second-Brain/` folder and add fresh, consolidated documentation for Rules, Skills, Pipelines, Plugins, MCP tools, Configs, and Parameters, plus a backbone overview that ties the project together.
todos: []
isProject: false
---

# Second Brain Backbone Documentation Plan

## Goal

Create `**3-Resources/Second-Brain/**` and populate it with clean, single-source documentation for the project backbone: rules, skills, pipelines, plugins, MCP tools, configs, and parameters—without duplicating full procedural text from existing rules; instead summarizing and pointing to canonical sources.

---

## 1. Folder and index

- **Create** `3-Resources/Second-Brain/` (new directory).
- **Create** `3-Resources/Second-Brain/README.md` — index note with:
  - Short purpose of the folder (“backbone and reference for the Second Brain automation stack”).
  - Links to each doc below (Rules, Skills, Pipelines, Plugins, MCP Tools, Configs, Parameters, Logs, Vault-Layout, Queue-Sources, Templates).
  - Link to existing master references: [Cursor-Skill-Pipelines-Reference.md](3-Resources/Cursor-Skill-Pipelines-Reference.md), [Second-Brain-Config.md](3-Resources/Second-Brain-Config.md).
  - Frontmatter: `title`, `created`, `tags`, `para-type: Resource`, `links: ["[[Resources Hub]]"]`.

---

## 2. Rules

- **Create** `3-Resources/Second-Brain/Rules.md`.
- **Content** (concise):
  - **Always-applied** (from [.cursor/rules/always/](.cursor/rules/always/)): table with rule file name, one-line purpose (e.g. `00-always-core.mdc` → persona, Ingest-first; `mcp-obsidian-integration.mdc` → backups, MCP usage, snapshots, fallbacks; `second-brain-standards.mdc` → PARA, atomic notes, attachments; `confidence-loops.mdc` → bands 72–84, 85+, <72, single loop; `always-ingest-bootstrap.mdc` → INGEST MODE → full-autonomous-ingest; `watcher-result-append.mdc` → Watcher-Result.md contract).
  - **Context (triggered)** (from [.cursor/rules/context/](.cursor/rules/context/)): table with rule file, trigger/phrase or glob, pipeline or flow (e.g. `para-zettel-autopilot.mdc` / `Ingest/*.md` → full-autonomous-ingest; `auto-eat-queue.mdc` / EAT-QUEUE → queue processor; `auto-queue-processor.mdc` / PROCESS TASK QUEUE → task/roadmap queue; `auto-distill.mdc` / DISTILL MODE → autonomous-distill; `auto-archive.mdc` / ARCHIVE MODE → autonomous-archive; `auto-express.mdc` / EXPRESS MODE → autonomous-express; `auto-organize.mdc` / ORGANIZE MODE → autonomous-organize; `ingest-processing.mdc`, `non-markdown-handling.mdc`, `snapshot-sweep.mdc`, `auto-restore.mdc`, `auto-resurface.mdc` with one-line purpose).
  - **Canonical source**: “Full text lives in `.cursor/rules/always/*.mdc` and `.cursor/rules/context/*.mdc`; this table is a map only.
  - **Diagram**: Include a detailed Mermaid flowchart (or two): (1) Trigger → rule type (always vs context) → pipeline/flow, with each rule file as a node or in a subgraph; (2) optional: decision flow for which context rule fires (e.g. glob match, phrase match). See §14.”

---

## 3. Skills

- **Create** `3-Resources/Second-Brain/Skills.md`.
- **Content**:
  - Table: **Skill name** | **Path** (e.g. `.cursor/skills/<name>/SKILL.md`) | **Used in pipeline(s)** | **Slot (after)** | **One-line purpose**.
  - Pull from [Cursor-Skill-Pipelines-Reference.md](3-Resources/Cursor-Skill-Pipelines-Reference.md) “Skill locations” and pipeline tables for ingest, distill, archive, express, organize (frontmatter-enrich, subfolder-organize, split-link-preserve, distill-highlight-color, next-action-extract, task-reroute, auto-layer-select, layer-promote, callout-tldr-wrap, readability-flag, archive-check, resurface-candidate-mark, summary-preserve, version-snapshot, related-content-pull, express-mini-outline, call-to-action-append, obsidian-snapshot).
  - Add queue/task skills: roadmap-checklist, roadmap-ingest, add-roadmap-append, expand-road-assist, task-complete-validate.
  - **Canonical source**: “Per-skill behavior in `.cursor/skills/<name>/SKILL.md` and pipeline order in Cursor-Skill-Pipelines-Reference.
  - **Diagram**: Include detailed Mermaid diagram(s): (1) Skills-by-pipeline matrix or flowchart (which skills run in ingest vs distill vs archive vs express vs organize vs queue); (2) per-pipeline skill chain as a flowchart (e.g. ingest: backup → classify → frontmatter-enrich → subfolder-organize → split → split-link-preserve → distill → distill-highlight-color → next-action-extract → task-reroute → append_to_hub → move → log). See §14.”

---

## 4. Pipelines

- **Create** `3-Resources/Second-Brain/Pipelines.md`.
- **Content**:
  - **Trigger → pipeline** table from Cursor-Skill-Pipelines-Reference (INGEST MODE / process Ingest → full-autonomous-ingest; EAT-QUEUE → queue processor; PROCESS TASK QUEUE → task queue; DISTILL / ARCHIVE / EXPRESS / ORGANIZE MODE → respective autonomous pipeline).
  - For each of **full-autonomous-ingest**, **autonomous-distill**, **autonomous-archive**, **autonomous-express**, **autonomous-organize**: 3–4 bullet steps (backup → classify or optional steps → skill chain → move/log) and link to the reference section.
  - **Queue processor**: read queue → validate/dedup → sort by canonical order → dispatch by mode → Watcher-Result; mention [auto-eat-queue.mdc](.cursor/rules/context/auto-eat-queue.mdc) and [Task-Queue.md](3-Resources/Task-Queue.md).
  - **Queue sources**: Which file and when — `prompt-queue.jsonl` (Watcher / EAT-QUEUE; modes INGEST MODE, DISTILL MODE, etc.) vs `Task-Queue.md` (task/roadmap queue; modes TASK-ROADMAP, TASK-COMPLETE, ADD-ROADMAP-ITEM, etc.). Detail in [Queue-Sources.md](3-Resources/Second-Brain/Queue-Sources.md).
  - **Confidence and safety**: high ≥85% (destructive after snapshot), mid 72–84% (one refinement loop), low <72% (propose only); dry_run before move; backup/snapshot invariants. Reference confidence-loops.mdc and mcp-obsidian-integration.
  - **Diagrams**: Include detailed Mermaid flowcharts for each pipeline (full step sequence with decision nodes for confidence and dry_run), plus a canonical-order diagram and a combined pipeline-overview diagram. See §14.

---

## 5. Plugins

- **Create** `3-Resources/Second-Brain/Plugins.md`.
- **Content**:
  - **Obsidian (required)**: Dataview, Highlightr, Obsidian Local REST API, Watcher — one line each on role (queries, highlight colors, MCP REST, Watcher-Signal/Watcher-Result + queue).
  - **Obsidian (optional)**: Templater, Tasks, QuickAdd, Excalidraw — brief note if present in kit.
  - **Cursor**: rules under `.cursor/rules/`, skills under `.cursor/skills/`, MCP via `~/.cursor/mcp.json` (obsidian-para-zettel-autopilot).
  - **Watcher contract**: fixed paths (Ingest/watched-file.md, Watcher-Signal.md, Watcher-Result.md), watcher-protected frontmatter, no move/delete of these. Link to [Watcher-Plugin-Usage.md](3-Resources/Watcher-Plugin-Usage.md) or Watcher-Result contract in watcher-result-append.
  - **Diagram**: Include a detailed Mermaid diagram: Obsidian plugins (Dataview, Highlightr, Local REST API, Watcher) and Cursor (rules, skills, MCP) as components; data flow from Watcher → Signal → Cursor/MCP → Result; optional subgraph for Watcher-protected paths. See §14.

---

## 6. MCP Tools

- **Create** `3-Resources/Second-Brain/MCP-Tools.md`.
- **Content**:
  - **Server**: `obsidian-para-zettel-autopilot` (configured in `~/.cursor/mcp.json`; descriptors in project `mcps/user-obsidian-para-zettel-autopilot/tools/*.json`).
  - **Grouped list** (no need to list every parameter in this doc): Core (read_note, update_note, search_replace, list_notes, global_search, manage_frontmatter, manage_tags); Backup (create_backup, ensure_backup); Move/structure (move_note, rename_note, ensure_structure); PARA/organize (classify_para, subfolder_organize); Content (split_atomic, distill_note, append_to_hub, suggest_connections); Tasks (create_task_note, append_tasks, find_parent); Confidence (calibrate_confidence, verify_classification, propose_alternative_paths); Batch (garden_review, curate_cluster); MOC (append_to_moc, generate_moc); Other (log_action, delete_note, refactor_to_zettel, bootstrap_project_batch, confirm_bootstrap, list_projects).
  - **Important params**: `dry_run` for move_note; `mode` for classify_para (area_first, conservative, liberal, balancer); `mode` for update_note (overwrite, create). Link to [2026-02-25-config-reference-obsidian-para-zettel-mcp.md](3-Resources/2026-02-25-config-reference-obsidian-para-zettel-mcp.md) or [Ingest/CONFIG-REFERENCE.md](Ingest/CONFIG-REFERENCE.md) for env and config.
  - **Diagram**: Include detailed Mermaid diagram(s): (1) Tool groups as subgraphs (Core, Backup, Move, PARA, Content, Tasks, Confidence, Batch, MOC, Other) with each tool name as a node; (2) optional flow: typical pipeline sequence of MCP calls (e.g. create_backup → classify_para → … → move_note → log_action). See §14.

---

## 7. Configs

- **Create** `3-Resources/Second-Brain/Configs.md`.
- **Content**:
  - **Vault/config note**: [Second-Brain-Config.md](3-Resources/Second-Brain-Config.md) — hub_names, archive (age_days, no_activity_days), highlight default_key, graph moc_strength; note “single source for pipelines/skills”.
  - **MCP env** (from mcp-obsidian-integration + config reference): OBSIDIAN_API_KEY, OBSIDIAN_REST_URL, OBSIDIAN_VAULT_PATH, BACKUP_DIR, SNAPSHOT_DIR, BATCH_SNAPSHOT_DIR; optional OBSIDIAN_CREATE_SKIP_BACKUP, MAX_BACKUP_AGE_MINUTES. One-line each. “Set in `~/.cursor/mcp.json` under `obsidian-para-zettel-autopilot.env`.”
  - **Paths**: BACKUP_DIR (external), SNAPSHOT_DIR (in-vault Per-Change), BATCH_SNAPSHOT_DIR (in-vault Batch). Link to mcp-obsidian-integration snapshot configuration.
  - **Cursor rules layout**: always vs context; globs in context rules.
  - **Diagram**: Include a detailed Mermaid diagram: config sources (Second-Brain-Config note, MCP env, paths) and how they feed into pipelines/skills; optional folder/layout of BACKUP_DIR vs SNAPSHOT_DIR vs BATCH_SNAPSHOT_DIR vs vault. See §14.

---

## 8. Parameters

- **Create** `3-Resources/Second-Brain/Parameters.md`.
- **Content**:
  - **Confidence bands**: high ≥85%, mid 72–84%, low <72%; primary signals per pipeline (ingest_conf, path_conf, archive_conf, express_conf, distill_conf).
  - **Loop fields** (for logs/Dataview): loop_attempted, loop_band, pre_loop_conf, post_loop_conf, loop_outcome, loop_type, loop_reason (from confidence-loops.mdc).
  - **Queue modes**: prompt queue (INGEST MODE, ORGANIZE MODE, TASK-ROADMAP, DISTILL MODE, EXPRESS MODE, ARCHIVE MODE, TASK-COMPLETE, ADD-ROADMAP-ITEM, etc.); task queue modes from [Task-Queue.md](3-Resources/Task-Queue.md): TASK-ROADMAP, TASK-COMPLETE, ADD-ROADMAP-ITEM, EXPAND-ROAD, REORDER-ROADMAP, DUPLICATE-ROADMAP, MERGE-ROADMAPS, EXPORT-ROADMAP, PROGRESS-REPORT.
  - **Watcher-Result line**: requestId, status, message, trace, completed (ISO8601).
  - **Log line fields**: timestamp, pipeline, note path, confidence, actions taken/skipped, backup path, snapshot path(s), flag; plus loop_* when applicable. Reference Cursor-Skill-Pipelines-Reference for Log format.
  - **Diagram**: Include detailed Mermaid diagram(s): (1) Confidence bands and loop (eval → high/mid/low with outcomes and loop_* fields); (2) Watcher-Result line structure; (3) optional: queue modes as a flowchart or table visual. See §14.
  - **Log line fields** (reference): Cursor-Skill-Pipelines-Reference “Log format”.
   if “Log format” is already in the bullet above.)
  - Reference Cursor-Skill-Pipelines-Reference “Log format”.

---

## 9. Backbone overview

- **Create** `3-Resources/Second-Brain/Backbone.md`.
- **Content** (narrative, 1–2 screens):
  - **Purpose**: One note that explains how the system fits together for a maintainer or new reader.
  - **Stack**: Obsidian vault (PARA + CODE) + Cursor (rules + skills) + Obsidian MCP server (tools) + Watcher (signals/queue).
  - **Flow**: User/Watcher triggers → rule match (always + context) → pipeline runs → MCP tools + skills in order → backup/snapshot before destructive steps → confidence gates and optional loop → move/log.
  - **Safety**: Backup-first (BACKUP_DIR), in-vault snapshots (Per-Change, Batch), dry_run before move, Error Handling Protocol to Errors.md, no shell cp/mv/rm on vault.
  - **PARA**: 1-Projects, 2-Areas, 3-Resources, 4-Archives; subfolder depth ≤4; project-id + themes drive paths.
  - **Diagrams**: Include detailed Mermaid flowcharts per §14 (system flow, safety flow, PARA/CODE). Do not skimp; use full step-level detail where it helps.
  - **Restore and rollback**: Restore is user-triggered only (e.g. auto-restore, snapshot-sweep rules). Per-change snapshots live in Backups/Per-Change; external backups in BACKUP_DIR; no auto-restore. Document where recovery procedures live (rules/skills).
  - Links to Rules, Skills, Pipelines, Plugins, MCP-Tools, Configs, Parameters, Logs, Vault-Layout, Queue-Sources, Templates and to Cursor-Skill-Pipelines-Reference, mcp-obsidian-integration, Second-Brain-Config.

---

## 10. Logs and observability

- **Create** `3-Resources/Second-Brain/Logs.md`.
- **Content**:
  - **Pipeline logs**: Ingest-Log, Distill-Log, Archive-Log, Express-Log, Organize-Log, Backup-Log — where each lives (`3-Resources/*.md`), what gets appended (timestamp, pipeline, note path, confidence, actions, backup/snapshot paths, flag; loop_* when applicable).
  - **Errors**: Single place for pipeline errors — `3-Resources/Errors.md`; standard entry format (heading, metadata table, Trace, Summary with Root cause, Impact, Suggested fixes, Recovery). Reference Error Handling Protocol in mcp-obsidian-integration.
  - **Observability**: Optional `3-Resources/MCP-Health-YYYY-MM.md` (monthly rotation); when to call `health_check` (e.g. every N notes in a batch or on first error). Fallback to Backup-Log or MCP-Observability if preferred.
  - **Diagram**: Include detailed Mermaid diagram(s): (1) Log destinations (Ingest-Log, Distill-Log, Archive-Log, Express-Log, Organize-Log, Backup-Log, Errors.md) as nodes with what gets written to each; (2) Error entry structure (heading → metadata table → Trace → Summary); (3) optional: when health_check is called in a batch. See §14.

---

## 11. Vault layout and exclusions

- **Create** `3-Resources/Second-Brain/Vault-Layout.md`.
- **Content**:
  - **Folder structure**: PARA roots (1-Projects, 2-Areas, 3-Resources, 4-Archives), Ingest, Backups (Per-Change, Batch, Versions), Templates, 5-Attachments (PDFs, Images, Audio, Documents, Other). One-line purpose of each.
  - **Exclusions**: What pipelines must not process — Backups/, **/Log*.md, **/* Hub.md, Watcher paths (Ingest/watched-file.md, Watcher-Signal.md, Watcher-Result.md), notes with `watcher-protected: true`. Brief note that context rules list these in Excludes sections.
  - **Diagram**: Include a detailed Mermaid diagram: full vault folder tree (root → 1-Projects, 2-Areas, 3-Resources, 4-Archives, Ingest, Backups with Per-Change/Batch/Versions, Templates, 5-Attachments with PDFs/Images/Audio/Documents/Other); optional second diagram: exclusions as a set or "do not process" flow. See §14.

---

## 12. Queue sources

- **Create** `3-Resources/Second-Brain/Queue-Sources.md`.
- **Content**:
  - **prompt-queue.jsonl** (`3-Resources/prompt-queue.jsonl`): Used by Watcher and EAT-QUEUE. One JSON object per line; fields include `mode`, `prompt`, `source_file`, `id` (requestId). Modes: INGEST MODE, ORGANIZE MODE, TASK-ROADMAP, DISTILL MODE, EXPRESS MODE, ARCHIVE MODE, TASK-COMPLETE, ADD-ROADMAP-ITEM, etc. Processed in canonical pipeline order; results to Watcher-Result.md.
  - **Task-Queue.md** (`3-Resources/Task-Queue.md`): Used by PROCESS TASK QUEUE / EAT-QUEUE for task/roadmap actions. Same line format; modes: TASK-ROADMAP, TASK-COMPLETE, ADD-ROADMAP-ITEM, EXPAND-ROAD, REORDER-ROADMAP, DUPLICATE-ROADMAP, MERGE-ROADMAPS, EXPORT-ROADMAP, PROGRESS-REPORT. Results to Watcher-Result.md and Mobile-Pending-Actions.md.
  - **When to use which**: Watcher appends to prompt-queue (or equivalent); task toolbar commands append to Task-Queue. Reference auto-eat-queue and auto-queue-processor.
  - **Diagram**: Include detailed Mermaid diagram(s): (1) Full queue processor flow (read file or EAT-CACHE → parse → validate → filter queue_failed → dedup → sort by canonical order → for each entry: dispatch by mode → run pipeline → append Watcher-Result); (2) Two entry points (prompt-queue.jsonl vs Task-Queue.md) with modes listed; (3) optional: canonical pipeline order as a horizontal flow. See §14.

---

## 13. Templates

- **Create** `3-Resources/Second-Brain/Templates.md`.
- **Content**:
  - **Where**: Templates live in `Templates/` (e.g. Ingest-template, AI-Output, Mobile-AI-Question). Optional subfolders by project or type.
  - **Purpose**: Used for new notes, ingest flow, and AI outputs so that structure and frontmatter are consistent.
  - **Backbone note**: Templates are backbone in that **the system is designed for consistent formatting** — frontmatter (created, tags, para-type, status), headings, callouts, and link patterns are standardized so pipelines, skills, and Dataview can rely on predictable structure. Reference second-brain-standards (frontmatter on every new .md, atomic notes, attachment syntax).
  - **Diagram**: Include a detailed Mermaid diagram: (1) Template → new note flow (Templates/ → Ingest or PARA; frontmatter fields, structure); (2) consistent-formatting backbone (frontmatter, headings, callouts, links) as inputs to pipelines/Dataview. See §14.

---

## 14. Mermaid diagrams

**Do not skimp.** Make every graph **detailed** and add diagrams at **every available opportunity**. Use camelCase/PascalCase for node IDs; no spaces. Quote edge labels that contain parentheses or special characters. No explicit colors (theme handles it). Do not use click, style, or classDef for colors.

- **Backbone.md** (multiple detailed diagrams): (1) **System flow** — Full flowchart: User/Watcher triggers → phrase/glob match → Rules (always + context with triggers) → Pipeline selection → Skills + MCP in sequence → Obsidian vault; include every major step. (2) **Safety flow** — Backup/Snapshot before destructive steps; decision node confidence ≥85%; create_backup → per-change snapshot → move/rename/split/distill/append. (3) **PARA/CODE flow** — PARA folders and CODE stages; where each pipeline fits.
- **Pipelines.md** (multiple detailed diagrams): (1) **Canonical order** — INGEST → ORGANIZE → TASK-ROADMAP → DISTILL → EXPRESS → ARCHIVE → TASK-COMPLETE → ADD-ROADMAP-ITEM. (2) **Full ingest flowchart** — Every step from list_notes through backup, classify_para, frontmatter-enrich, subfolder-organize, confidence/loop, split_atomic, split-link-preserve, distill_note, distill-highlight-color, next-action-extract, task-reroute, append_to_hub, move_note (dry_run then commit), log_action; decision nodes. (3) **Distill / Archive / Express / Organize** — Same detail for each. (4) **Confidence band flow** — eval → high/mid/low with outcomes and loop_*. Reuse Cursor-Skill-Pipelines-Reference ingest flowchart. **Pipeline flow** (redundant with above; remove if present): Either (a) one combined flowchart for the five autonomous pipelines (backup → classify/skills → move/log) with short labels, or (b) a single “canonical order” diagram (e.g. INGEST → ORGANIZE → TASK-ROADMAP → DISTILL → EXPRESS → ARCHIVE) plus a minimal ingest-step chain (backup → classify → frontmatter → subfolder → split → distill → hub → move → log). Reuse or adapt the existing ingest flowchart from Cursor-Skill-Pipelines-Reference if present.
- **Parameters.md**: (1) **Confidence bands and loop** — eval → high/mid/low; loop_* fields. (2) **Watcher-Result line** — requestId, status, message, trace, completed. (3) **Queue modes** — prompt-queue vs task-queue. Reference confidence-loops.mdc.
- **Queue-Sources.md** (detailed): (1) **Full queue processor** — Read (file or EAT-CACHE) → parse → validate → filter queue_failed → dedup → sort by canonical order → for each: dispatch by mode → run pipeline → append Watcher-Result. (2) **Two entry points** — prompt-queue.jsonl vs Task-Queue.md with modes; results to Watcher-Result and Mobile-Pending-Actions. (3) **Canonical order** horizontal flow.
- **Vault-Layout.md** (detailed): (1) **Full folder tree** — Root → 1–4 (PARA), Ingest, Backups (Per-Change, Batch, Versions), Templates, 5-Attachments (PDFs, Images, Audio, Documents, Other); every level. (2) **Exclusions** — Backups/, Log*.md, * Hub.md, Watcher paths; do-not-process flow.
- **Logs.md** (detailed): (1) **Log destinations** — Ingest-Log, Distill-Log, Archive-Log, Express-Log, Organize-Log, Backup-Log, Errors.md; what gets written; which pipeline. (2) **Error entry structure** — heading → metadata table → Trace → Summary. (3) **Health check** — when called (every N notes, on error).
- **Templates.md** (detailed): (1) **Template → note flow** — Templates/ → Ingest or PARA; frontmatter and structure. (2) **Consistent-formatting backbone** — frontmatter, headings, callouts, links as inputs to pipelines/Dataview.
- **Configs.md** (detailed): **Config sources** — Second-Brain-Config + MCP env (BACKUP_DIR, SNAPSHOT_DIR, BATCH_SNAPSHOT_DIR) → how they feed pipelines/skills; optional folder layout.
- **MCP-Tools.md** (detailed): (1) **Tool groups** — Subgraphs for Core, Backup, Move, PARA, Content, Tasks, Confidence, Batch, MOC, Other with every tool name. (2) **Typical MCP sequence** — create_backup → classify_para → … → move_note → log_action for ingest.
- **Plugins.md** (detailed): **Component and data flow** — Obsidian plugins (Dataview, Highlightr, Local REST API, Watcher) + Cursor (rules, skills, MCP); Watcher → Signal → Cursor/MCP → Result; Watcher-protected paths subgraph.

Add diagrams at every available opportunity; do not skimp on detail.

---

## 15. Cross-links and standards

- Add `links` in frontmatter to Resources Hub (or main hub) where appropriate.
- README.md must link to Logs, Vault-Layout, Queue-Sources, and Templates.
- Use `[[note]]` for in-vault links; relative paths for `.cursor/` when useful.
- All new notes: title, created (YYYY-MM-DD), tags, para-type: Resource, status: active.
- Do not duplicate long procedural content from .mdc or Cursor-Skill-Pipelines-Reference; summarize and link.

---

## 16. Post-documentation: backbone-docs sync rule and .cursor/sync sync

**After** all documentation in `3-Resources/Second-Brain/` is created, add or update a rule so that future changes to the backbone trigger (1) documentation updates and (2) sync of rules and skills to `.cursor/sync/`.

- **Create or modify** a rule in `.cursor/rules/always/` (e.g. a new file `backbone-docs-sync.mdc` or a subsection in an existing always rule such as `second-brain-standards.mdc` or `00-always-core.mdc`).
- **Content** (concise):
  - **Trigger**: When the user or the agent modifies any **backbone** component — i.e. files under `.cursor/rules/` (always or context), `.cursor/skills/`, pipeline definitions or trigger mapping (e.g. in Cursor-Skill-Pipelines-Reference or context rules), MCP server config or tool behavior (`~/.cursor/mcp.json` or project `mcps/`), `3-Resources/Second-Brain-Config.md`, or any note in `3-Resources/Second-Brain/` — then: **(A)** update the corresponding backbone documentation in `3-Resources/Second-Brain/` to represent the new behavior; **(B)** when **rules** or **skills** are modified, also sync to `.cursor/sync/` (see below).
  - **Sync rule for rules and skills to `.cursor/sync/`**: When a file under `.cursor/rules/always/`, `.cursor/rules/context/`, or `.cursor/skills/<name>/` is created, renamed, or its content is changed, **update the corresponding file under `.cursor/sync/`** so the sync folder reflects the current rules and skills. Mapping: `.cursor/rules/always/<name>.mdc` ↔ `.cursor/sync/rules/always/<name>.md`; `.cursor/rules/context/<name>.mdc` ↔ `.cursor/sync/rules/context/<name>.md`; `.cursor/skills/<name>/SKILL.md` ↔ `.cursor/sync/skills/<name>.md`. Copy or convert content as needed (e.g. .mdc → .md); preserve meaning. If a rule or skill is removed, remove the corresponding sync file. Ensure `.cursor/sync/` stays in sync with `.cursor/rules/` and `.cursor/skills/` whenever those are modified.
  - **What to update (Second-Brain docs)**: Map the changed artifact to the right doc(s) in `3-Resources/Second-Brain/`: Rules → Rules.md (and tables/diagrams); Skills → Skills.md; Pipelines / trigger mapping → Pipelines.md; Plugins → Plugins.md; MCP tools/config → MCP-Tools.md, Configs.md; Parameters (confidence, queue modes, log format) → Parameters.md; Log destinations or error format → Logs.md; vault layout or exclusions → Vault-Layout.md; queue sources or modes → Queue-Sources.md; templates or formatting standards → Templates.md; high-level flow or safety → Backbone.md. Refresh **Mermaid diagrams** in those docs so they stay accurate; do not leave outdated flows or node lists.
  - **Intent**: Keep `3-Resources/Second-Brain/` as the single source of truth for backbone documentation; keep `.cursor/sync/` as the synced copy of rules and skills for reference or tooling; whenever behavior or structure changes, update both the docs (and diagrams) and the sync folder in the same pass or as an immediate follow-up.
- **Placement**: Prefer a dedicated always-applied rule (e.g. `backbone-docs-sync.mdc`) so the instruction is easy to find and maintain; alternatively append a short “Backbone docs sync” subsection to an existing always rule with a link to `3-Resources/Second-Brain/README.md`.

---

## File summary


| File                                        | Purpose                                                                   |
| ------------------------------------------- | ------------------------------------------------------------------------- |
| `3-Resources/Second-Brain/README.md`        | Index and entry point                                                     |
| `3-Resources/Second-Brain/Rules.md`         | Always + context rules map                                                |
| `3-Resources/Second-Brain/Skills.md`        | Skills table with pipeline/slot                                           |
| `3-Resources/Second-Brain/Pipelines.md`     | Trigger→pipeline, flow summary, safety, queue sources ref                 |
| `3-Resources/Second-Brain/Plugins.md`       | Obsidian + Cursor plugins and Watcher                                     |
| `3-Resources/Second-Brain/MCP-Tools.md`     | Obsidian MCP tool groups and key params                                   |
| `3-Resources/Second-Brain/Configs.md`       | Second-Brain-Config + MCP env + paths                                     |
| `3-Resources/Second-Brain/Parameters.md`    | Confidence, loop fields, queue modes, log format                          |
| `3-Resources/Second-Brain/Logs.md`          | Pipeline logs, Errors.md, observability / health_check                    |
| `3-Resources/Second-Brain/Vault-Layout.md`  | Folder structure + exclusions (what not to process)                       |
| `3-Resources/Second-Brain/Queue-Sources.md` | prompt-queue.jsonl vs Task-Queue.md; when each is used                    |
| `3-Resources/Second-Brain/Templates.md`     | Where templates live; backbone: system designed for consistent formatting |
| `3-Resources/Second-Brain/Backbone.md`      | High-level narrative, diagram, restore/rollback; links to all             |

**Post-docs (step 16):** `.cursor/rules/always/backbone-docs-sync.mdc` — when backbone is modified, update Second-Brain docs and diagrams; when rules or skills are modified, sync to `.cursor/sync/rules/` and `.cursor/sync/skills/`.

Documentation first; then add the backbone-docs sync rule (§16). After implementation: (1) optionally add a link from Resources Hub or Cursor-Skill-Pipelines-Reference to `3-Resources/Second-Brain/README.md`; (2) ensure the new always-applied rule (e.g. `backbone-docs-sync.mdc`) is in place so that future backbone changes trigger documentation updates and (when rules/skills change) sync to `.cursor/sync/`.