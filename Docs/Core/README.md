---
title: Second Brain Backbone
created: 2026-02-28
tags: [pkm, second-brain, backbone, reference]
para-type: Resource
status: active
links: ["[[Resources Hub]]"]
---

**TL;DR** — Control center for the Second Brain automation stack. Start with **Prompt-Crafter** (“We are making a CODE/ROADMAP prompt”) or use the Quick-command section; expand the doc callouts below for Rules, Pipelines, Logs, and key references. Dashboard: [[3-Resources/Vault-Change-Monitor|Vault-Change-Monitor]]; audit: [[3-Resources/Second-Brain/System-Audit-Report-2026-03-12|System-Audit-Report-2026-03-12]].

---

## Quick-command (copy-paste)

| Trigger | What runs |
|---------|-----------|
| **INGEST MODE** | full-autonomous-ingest on Ingest/ |
| **EAT-QUEUE** | Step 0 wrappers first, then prompt-queue.jsonl by mode |
| **DISTILL MODE** | autonomous-distill |
| **EXPRESS MODE** | autonomous-express |
| **ARCHIVE MODE** | autonomous-archive |
| **ORGANIZE MODE** | autonomous-organize |
| **ROADMAP MODE** | Setup only (Phase 0 + roadmap-generate-from-outline) |
| **Resume roadmap** / **RESUME-ROADMAP** | Single continue (deepen default) |
| **We are making a prompt** | Question-led Prompt-Crafter (CODE or ROADMAP) |

---

## Major docs (expand to open)

> [!abstract]- **Rules** — Trigger → rule map, always + context
> [[3-Resources/Second-Brain/Rules|Rules]] — Always-applied and context (triggered) rules; full text in `.cursor/rules/`.

> [!abstract]- **Pipelines** — Trigger → pipeline, snapshot triggers, EAT-QUEUE flow
> [[3-Resources/Second-Brain/Pipelines|Pipelines]] — Trigger → pipeline, Decision Wrappers, confidence and safety.

> [!abstract]- **Cursor-Skill-Pipelines-Reference** — Canonical pipeline order and skills
> [[3-Resources/Second-Brain/Cursor-Skill-Pipelines-Reference|Cursor-Skill-Pipelines-Reference]] — Skill slots, snapshot triggers, apply-from-wrapper.

> [!abstract]- **Logs** — Where each pipeline logs
> [[3-Resources/Second-Brain/Logs|Logs]] — Ingest-Log, Distill-Log, Errors.md, Vault-Change-Monitor.

> [!abstract]- **Parameters** — Confidence bands, RESUME-ROADMAP params
> [[3-Resources/Second-Brain/Parameters|Parameters]] — Bands, queue defaults, context-tracking, research params.

> [!abstract]- **Queue-Sources** — prompt-queue.jsonl vs Task-Queue.md
> [[3-Resources/Second-Brain/Queue-Sources|Queue-Sources]] — Mode → file, validation, remove-stale on RESUME-ROADMAP append.

> [!abstract]- **Vault-Layout** — PARA folders, protected paths
> [[3-Resources/Second-Brain/Vault-Layout|Vault-Layout]] — Folder structure, Ingest/Decisions, .technical.

> [!abstract]- **Backbone** — System flow and safety
> [[3-Resources/Second-Brain/Backbone|Backbone]] — Stack, invariants, multi-run roadmap.

> [!abstract]- **Subagents / post-migration docs** — Architecture, pipelines, rules, user flows
> [[3-Resources/Second-Brain/Docs/README|Docs/README]] — Subagent architecture, delegation, Queue pipeline, EAT-QUEUE flow, Prompt Crafter flow; single entry point for post-migration docs under `Docs/`.

> [!abstract]- **CODE PARA and Roadmapping systems** — Canonical system overviews
> [[3-Resources/Second-Brain/Docs/CODE-PARA-System|Docs/CODE-PARA-System]] and [[3-Resources/Second-Brain/Docs/Roadmapping-System|Docs/Roadmapping-System]] — concise references for CODE lane PARA routing and roadmap multi-run system behavior.

> [!abstract]- **Entire system reference** — Full canonical contract in one document
> [[3-Resources/Second-Brain/Docs/Entire-System-Reference|Docs/Entire-System-Reference]] — unified documentation for funnels, queues, CODE PARA pipelines, roadmap lane, safety gates, logs, and recovery.

> [!abstract]- **Backup and restore** — Single reference for backups, snapshots, retention, RESTORE MODE
> [[3-Resources/Second-Brain/Docs/Operations/Backup-and-Restore|Docs/Operations/Backup-and-Restore]] — BACKUP_DIR, SNAPSHOT_DIR, ensure_backup vs create_backup, per-change/batch, snapshot-sweep, restore flow, Restore-Queue.

> [!abstract]- **Where to find** — Index of all docs (config, MCP, queue, logs, backup, errors, triggers)
> [[3-Resources/Second-Brain/Docs/Reference/Where-to-Find|Docs/Reference/Where-to-Find]] — One place to find any documented topic; no “missing doc” — search the haystack from here.

---

## Recent activity (Dataview)

Use **Vault-Change-Monitor** as the live dashboard. Example queries (run in Obsidian with Dataview):

- **Recent Ingest**: `TABLE file.mtime as "Time", excerpt FROM "3-Resources/Ingest-Log.md" LIMIT 10`
- **Recent errors**: `LIST FROM "3-Resources/Errors" LIMIT 5`
- **Pending wrappers**: `LIST FROM "Ingest/Decisions" WHERE !processed`

---

## Documentation index (full)

- [[3-Resources/Second-Brain/Rules|Rules]] — Always-applied and context (triggered) rules map
- [[3-Resources/Second-Brain/Skills|Skills]] — Skills by pipeline and slot
- [[3-Resources/Second-Brain/Pipelines|Pipelines]] — Trigger → pipeline, flows, safety
- [[3-Resources/Second-Brain/Responsibilities-Breakdown|Responsibilities-Breakdown]] — What each pipeline, skill, and rule performs/enforces; responsibility boundaries
- [[3-Resources/Second-Brain/Plugins|Plugins]] — Obsidian and Cursor plugins
- [[3-Resources/Second-Brain/MCP-Tools|MCP Tools]] — Obsidian MCP tool groups and params
- [[3-Resources/Second-Brain/Configs|Configs]] — Second-Brain-Config and MCP env
- [[3-Resources/Second-Brain/Color-Coded-Highlighting|Color-Coded-Highlighting]] — How semantic highlighting links and relates ideas across projects (color key, highlight_key, color theory)
- [[3-Resources/Second-Brain/Parameters|Parameters]] — Confidence bands, queue modes, log format
- [[3-Resources/Second-Brain/Logs|Logs]] — Pipeline logs, Errors.md, observability
- [[3-Resources/Second-Brain/Docs/Operations/Backup-and-Restore|Docs/Operations/Backup-and-Restore]] — Backups, snapshots, retention, RESTORE MODE, Restore-Queue
- [[3-Resources/Second-Brain/Docs/Operations/Logs-and-Observability|Docs/Operations/Logs-and-Observability]] — Log locations, Backup-Log, rotation, Vault-Change-Monitor
- [[3-Resources/Second-Brain/Docs/Operations/Errors-and-Recovery|Docs/Operations/Errors-and-Recovery]] — Error Handling Protocol, Errors.md structure, recovery
- [[3-Resources/Second-Brain/Docs/Reference/Where-to-Find|Docs/Reference/Where-to-Find]] — Index: config, MCP, vault, queue, logs, backup, errors, triggers
- [[3-Resources/Second-Brain/Vault-Layout|Vault-Layout]] — Folder structure and exclusions
- [[3-Resources/Second-Brain/Queue-Sources|Queue-Sources]] — prompt-queue.jsonl vs Task-Queue.md
- [[3-Resources/Second-Brain/Queue-Alias-Table|Queue-Alias-Table]] — command/trigger aliases → processor and mode
- [[3-Resources/Second-Brain/Naming-Conventions|Naming-Conventions]] — Note and file naming (kebab-slug-YYYY-MM-DD-HHMM; date and time at end)
- [[3-Resources/Second-Brain/Templates|Templates]] — Consistent formatting backbone
- [[3-Resources/Second-Brain/Chat-Prompts|Chat-Prompts]] — Standardized Cursor chat prompt strings, question-led prompt crafting (CODE/ROADMAP kickoffs), templates, and validation
- [[3-Resources/Second-Brain/Prompt-Crafter-Param-Table|Prompt-Crafter-Param-Table]] — Param table (question order, parentage, accepts_manual_text) for question-led prompt crafting
- [[3-Resources/Second-Brain/Prompt-Crafter-Examples|Prompt-Crafter-Examples]] — Transcript-style question-led examples (CODE, ROADMAP, A/B/C, manual text phase)
- [[3-Resources/Second-Brain/User-Questions-and-Options-Reference|User-Questions-and-Options-Reference]] — Every user-facing question and options in presentation order (question-led crafter, Decision Wrappers, Commander macro)
- [[3-Resources/Second-Brain/Mobile-Migration-Spec|Mobile-Migration-Spec]] — Mobile = observe + fill Ingest only; laptop-only queue and crafting
- [[3-Resources/Second-Brain/Testing|Testing]] — Automated tests (unit, integration, fixtures); how to run and add tests
- [[3-Resources/Second-Brain/Backbone|Backbone]] — High-level narrative and system flow
- [[3-Resources/Second-Brain/Docs/README|Docs/README]] — **Subagents / post-migration docs** (architecture, pipelines, rules, user flows; entry point for `Docs/`)
- [[3-Resources/Second-Brain/Docs/CODE-PARA-System|Docs/CODE-PARA-System]] — Canonical CODE lane overview (PARA mapping, queue routing, safety gates)
- [[3-Resources/Second-Brain/Docs/Roadmapping-System|Docs/Roadmapping-System]] — Canonical roadmap lane overview (setup/resume, dual-track, state authority)
- [[3-Resources/Second-Brain/Docs/Entire-System-Reference|Docs/Entire-System-Reference]] — Full-system canonical reference (entry funnels, queues, CODE PARA, roadmap, safety, observability)
- [[3-Resources/Second-Brain/Roadmap-Quality-Guide|Roadmap-Quality-Guide]] — Multi-run roadmap quality, confidence gate, RECAL-ROAD, one-shot deprecated
- [[3-Resources/Second-Brain/Cursor-Agent-Ingest-Workflow|Cursor-Agent-Ingest-Workflow]] — Agent-output drop zone, direct move, tech_level
- **Second-Brain-User-Flows/** — User flow diagrams (High/Mid/Detailed) and rules; Decision Wrapper, Step 0, re-try, phase-direction. question-led prompt crafter user flow and architecture diagrams (User-Flow-Prompt-Crafter-*, Prompt-Crafter-Structure-*) and related docs verified for consistency 2026-03-10.
- **Post-process stabilizers (variance dampeners):** Low-variance post-AI steps (ingest re-rank + pad-to-7, distill short-note core bias + emoji fallback, archive confidence-floor, queue conf-conditional TASK-ROADMAP bump). See [[3-Resources/Second-Brain/Pipelines#Post-process stabilizers (variance dampeners)|Pipelines § Post-process stabilizers]] and [[3-Resources/Second-Brain/Backbone#Post-process stabilizers (variance dampeners)|Backbone]].
- [[3-Resources/Deprecated-Vestigial-Audit|Deprecated-Vestigial-Audit]] — Audit of deprecated/vestigial logging, root files, and path references

Mermaid diagrams appear in **Backbone**, **Rules**, **Skills**, **Pipelines**, **MCP-Tools**, **Configs**, **Logs**, **Vault-Layout**, **Queue-Sources**, **Parameters**, **Templates**, and **Plugins** where applicable.

## How to use this documentation

- **Start at Backbone** for system flow, safety, and component roles.
- **Use Rules and Pipelines** for trigger phrases and pipeline sequences.
- **Use Skills and MCP-Tools** for step-by-step behavior and tool usage.
- **Use Logs and Parameters** for observability, log format, and tuning.

## Mental model in 60 seconds

**Preferred path (Prompt-Crafter)** → when you want a safe, multi-step automation run, start with **“We are making a CODE prompt”** or **“We are making a ROADMAP prompt”** in Chat/Agent. The question-led Prompt-Crafter collects mode + params via Q&A, assembles a validated payload, appends it to the appropriate queue (prompt-queue.jsonl or Task-Queue.md), and EAT-QUEUE / PROCESS TASK QUEUE dispatches it through funnels and pipelines.

**Direct/manual triggers (advanced)** → for quick runs, you can still say **INGEST MODE**, **DISTILL MODE**, **EXPRESS MODE**, **ARCHIVE MODE**, **EAT-QUEUE**, or **PROCESS TASK QUEUE**, but these are treated as **manual/advanced** entry points: they bypass Prompt-Crafter Q&A, assume more context, and are intended for trusted laptop usage only. They still obey core guardrails (backups, snapshots, confidence bands) and are routed via system funnels into the same pipelines.

**New stuff** → put in Ingest/ → (preferred) craft an **INGEST MODE** entry via Prompt-Crafter → or say **INGEST MODE** (or Process Ingest) → classify → enrich → distill → organize → hub/link → note lands in PARA (Projects, Areas, or Resources). **Maintenance** → open a note → say **DISTILL MODE**, **HIGHLIGHT PERSPECTIVE**, or **ARCHIVE MODE** → or run **EAT-QUEUE** to process the next queue entry.

## Usage at a glance

- **Ingest**: Put file in Ingest/, say **INGEST MODE** or **Process Ingest**.
- **Distill**: Open a note, say **DISTILL MODE – safe batch autopilot** (or queue BATCH-DISTILL).
- **Express**: Open a distilled note, say **EXPRESS MODE – safe batch autopilot**.
- **Archive**: Say **ARCHIVE MODE – safe batch autopilot** on a folder to move completed notes to 4-Archives/.
- **Organize**: Say **ORGANIZE MODE – safe batch autopilot** (optionally on a folder) to re-classify and move.
- **Queue**: Populate `.technical/prompt-queue.jsonl` or Task-Queue.md, then say **EAT-QUEUE** or **PROCESS TASK QUEUE**. See [[3-Resources/Second-Brain/Queue-Sources|Queue-Sources]] for queue modes.

## Trigger cheat sheet

| Spoken / UI trigger | What actually happens | Typical use-case |
|---------------------|------------------------|------------------|
| **INGEST MODE** | full-autonomous-ingest on Ingest/ contents | New files dropped in Ingest |
| **DISTILL MODE** | autonomous-distill (or BATCH-DISTILL on selection/folder) | Improve existing notes |
| **ARCHIVE MODE** | archive-check + move completed/no-task notes to 4-Archives/ | Cleanup old projects |
| **EAT-QUEUE** | **Step 0:** Check approved wrappers (Ingest/Decisions/**) first — apply move, archive wrapper to 4-Archives/Ingest-Decisions/; then process prompt-queue.jsonl by mode; append Watcher-Result | Apply approved Decision Wrappers; then continue queue |
| **ORGANIZE MODE** | autonomous-organize (re-classify and move in PARA) | Re-organize folder or note |
| **EXPRESS MODE** | autonomous-express (related content, outline, CTA) | Prepare note for sharing |
| **ROADMAP MODE**, **Resume roadmap** | Default: multi-run (Phase 0 bootstrap, distill per phase, conf ≥85% gate, recal when drift > 0.08). If state exists and in-progress/blocked: roadmap-resume → roadmap-generate-from-outline with resume_from. One-shot **deprecated** (use **ROADMAP-ONE-SHOT** if you must). Queue: RESUME-ROADMAP, RESUME-FROM-LAST-SAFE, RECAL-ROAD. **Mobile:** Avoid direct edits to roadmap-state.md frontmatter — use Commander macros. |

> [!danger] **ROADMAP MODE is now multi-run only.** One-shot is deprecated and will not receive updates. Use **ROADMAP-ONE-SHOT** if you must. See [[3-Resources/Second-Brain/Roadmap-Quality-Guide|Roadmap-Quality-Guide]].

**Roadmap seed:** Prefer the Project Master Goal note (filename contains `Master-Goal` or `MasterGoal` under `1-Projects/<project-id>/`); if multiple candidates, prefer highest `created` or `roadmap-seed: true`. See [[3-Resources/Second-Brain/Naming-Conventions|Naming-Conventions]].

See [[3-Resources/Second-Brain/Pipelines|Pipelines]] for the full trigger table.

## Key invariants / safety guarantees

See [[3-Resources/Second-Brain/Backbone#Key invariants / safety guarantees|Backbone § Key invariants]] for the system's safety promises (no deletes without move/snapshot, backup + dry-run before destructive ops, exclusions for Backups/Logs, preserve creation time).

## Troubleshooting common failure modes

- **Note stays in Ingest/ forever** → **Phase 1 never moves notes.** Open the Decision Wrapper in `Ingest/Decisions/Ingest-Decisions/`, check one option A–G (or set `approved_path`), set `approved: true` in frontmatter, then run **EAT-QUEUE** so Step 0 applies the move and archives the wrapper. If no wrapper exists, run INGEST MODE first; if confidence was &lt;68%, the wrapper is still created with A–G options.
- **No frontmatter / missing para-type** → always-core rule may not have run, or classify_para was skipped; ensure note is in Ingest/ and INGEST MODE was triggered.
- **Colors not applying** → Highlightr plugin disabled; wrong or missing highlight_key; or distill-highlight-color skill not run (run DISTILL MODE or HIGHLIGHT PERSPECTIVE).
- **Move fails with "parent does not exist"** → ensure_structure was not called for target parent; see MCP fallback in [[.cursor/rules/always/mcp-obsidian-integration|mcp-obsidian-integration]]; retry after ensuring parent path exists.
- **Watcher shows failure** → Check Watcher-Result.md for requestId, trace, and completed timestamp; see [[3-Resources/Second-Brain/Logs|Logs]] for error entry format and [[3-Resources/Errors]] for logged errors.

## Changelog (doc updates)

- **2026-03-08**: **Documentation audit (zero gaps):** Cursor-Skill-Pipelines-Reference: fixed stale `obsidian_propose_para_paths` → `propose_para_paths`. README index: added Roadmap-Quality-Guide, Cursor-Agent-Ingest-Workflow. Backbone links: same. Queue-Alias-Table: added RESUME-FROM-LAST-SAFE, NORMALIZE-MASTER-GOAL, SCOPING MODE. User flows verified current. **Follow-up audit:** Replaced remaining `obsidian_propose_para_paths` with `propose_para_paths` in Testing.md, Regression-Stability-Log.md, User-Flow-Rules-Mid-Level, Rules-Structure-Mid-Level, Prompt-Crafter-Structure-Detailed, PARA-Actionability-Rubric, System-Diagram (Mid/Detailed), Skills-Structure (High/Detailed), para-regression.md, test Mermaid files, System-Audit-Report. Added **Deprecated-Vestigial-Audit** stub at 3-Resources/Deprecated-Vestigial-Audit.md; doc covers folder blacklist, MCP naming, and where audits are recorded. **2026-03-11:** Audit reports (Flow-Graphs-Audit, Architecture-Graphs-Audit, System-Audit-Report-2026-03-06) moved to **4-Archives/Resources/Second-Brain-Audits/** — they are point-in-time audits, not evergreen documentation.
- **2026-03-07**: **Documentation and user workflow Mermaids** updated to match current behavior: (1) **EAT-QUEUE Step 0 first** — always-check wrappers runs before reading prompt-queue.jsonl; apply approved → move note to approved_path, archive wrapper to 4-Archives/Ingest-Decisions/ (subfolders mirrored). (2) **Ingest Phase 1** — no move/rename in Phase 1; note stays in Ingest/ until user approves wrapper and runs EAT-QUEUE. (3) Pipelines.md: Queue processor summary, full ingest flowchart, and new "EAT-QUEUE flow (Step 0 before queue)" Mermaid. (4) Queue-Sources.md: Full queue processor flow Mermaid now starts with Step 0. (5) User-Flow-Diagram High/Mid/Detailed: Ingest Phase 1 vs 2, EAT-QUEUE what user gets, queue processing, and EAT-QUEUE Step 0 diagrams updated. (6) README: EAT-QUEUE trigger cheat sheet and "Note stays in Ingest" troubleshooting. (7) Backbone: Flow paragraph now states Step 0 runs first and wrapper archive path.
- **2026-03-06**: **Second-Brain docs sync**: Fixed Cursor-Skill-Pipelines-Reference path (all links now use `3-Resources/Second-Brain/Cursor-Skill-Pipelines-Reference`). Reference doc: trigger table (ingest-processing, auto-archive, auto-garden-review, auto-curate-cluster), `propose_para_paths` (no obsidian_ prefix), new **Apply-from-wrapper (Step 0)** table including task-decision; Skill locations table extended (obsidian-snapshot, log-rotate, move-attachment-to-99, research-scope, distill/express-apply-from-wrapper, link-to-pmg-if-applicable). Parameters: added `task-decision` to wrapper_type. Backbone: added Cursor-Skill-Pipelines-Reference to links list.
- **2026-03-07**: Integrated ghost folder sweep for archive via MCP tool. Skill **archive-ghost-folder-sweep** runs after log_action when notes were moved; uses **obsidian_remove_empty_folder** only (no shell rmdir). Folder ops group and descriptor in MCP-Tools; auto-archive Step 9 and Ghost folders subsection; Skills.md and pipeline reference updated.
- **2026-03-06**: **Testing system completion**: PARA regression suite made runnable. Added 7 fixture notes in [[3-Resources/Second-Brain/tests/fixtures/para-regression|tests/fixtures/para-regression/]] (5 core + 2 edge-case for tie-breaker/flip-rate); filled table in [[3-Resources/Second-Brain/tests/para-regression|para-regression]] with note_path, golden_top_path, content_snippet, acceptable_alts, notes. [[3-Resources/Second-Brain/Regression-Stability-Log|Regression-Stability-Log]]: added **Baseline Run Procedure** (steps 1, 1.5 clear wrappers, 2–7) and rubric version lock in step 7; first row remains TODO until first run. [[3-Resources/Second-Brain/Testing|Testing]]: added **Test coverage by responsibility** table mapping to [[3-Resources/Second-Brain/Responsibilities-Breakdown|Responsibilities-Breakdown]]. Fixtures README updated. See plan finish_testing_system.
- **2026-03-06**: **MCP tools doc cleanup**: [[3-Resources/Second-Brain/MCP-Tools|MCP-Tools]] tool groups and diagram now use exact MCP names from descriptors (`mcps/user-obsidian-para-zettel-autopilot/tools/*.json`): `obsidian_*` for vault tools, `propose_para_paths` (not `obsidian_propose_para_paths`), `health_check` added to Other. Full parameter schemas pointed to descriptor JSONs. All references to the ranked PARA tool updated to `propose_para_paths` in Parameters, Rules, Pipelines, Backbone, Templates, Cursor-Skill-Pipelines-Reference, and rule/sync copies.
- **2026-03-03**: Doc audit: Vault-Layout folder blacklist (never use 00 Inbox, 10 Zettelkasten, 99*); Versions/ under note parent not Backups/Versions; Cursor-Skill-Pipelines-Reference: auto-archive (not auto-archiving), loop_band 68-84, obsidian-snapshot in Skill locations; Queue-Sources NAME-REVIEW in modes. **Full audit**: Rules/Skills/Pipelines/Parameters/Logs/Vault-Layout/Queue-Sources/Configs/MCP-Tools/Templates/Plugins/Naming-Conventions cross-checked; trigger table fix: `auto-ingest-processing` → `ingest-processing` in Cursor-Skill-Pipelines-Reference (rule file is ingest-processing.mdc). **Zero-gap pass**: README index + Naming-Conventions; Backbone links + Naming-Conventions + Color-Coded-Highlighting; Cursor-Skill-Pipelines-Reference Skill locations + log-rotate + move-attachment-to-99; Parameters queue modes note (SEEDED-ENHANCE, BATCH-*, ASYNC-LOOP, NAME-REVIEW).
- **2026-03-02**: Added Guidance-Aware Run Contract — user_guidance frontmatter + rule + feedback-incorporate extension. Re-runs now natively respect user refinement instructions (soft hint for classify, path, split, distill); see guidance-aware.mdc and Parameters (user_guidance, guidance_conf_boost).
- **2026-03**: Responsibility columns and usage examples across all Second-Brain docs; trigger and tuning cheat sheets; troubleshooting section; key invariants in Backbone.
- **2026-02**: SEEDED-ENHANCE pipeline; Commander integration; queue modes (BATCH-DISTILL, BATCH-EXPRESS, ASYNC-LOOP).

## Onboarding: Monitor changes

- **MOC**: Monitor recent pipeline activity and system health via [Vault-Change-Monitor](3-Resources/Vault-Change-Monitor.md). Use it as the single dashboard for last N log entries, Commander-triggered events, and health summaries.
- **Depths with Commander Quickstart**: Tap "Queue Highlight Perspective" (or equivalent) on mobile toolbar; approve preview on laptop — observe gradients and lens/view in notes and logs. See [Commander-Plugin-Usage](3-Resources/Commander-Plugin-Usage.md) and depth plan.

## Testing Remediations

Use these steps to verify frontend and backend clunk remediations (banner cleanup, queue fast-path, queue-cleanup, batch snapshot threshold, proposal re-queue, etc.).

### Happy path

1. Queue a single **Task Complete** on mobile (or add one line to Task-Queue.md).
2. Verify the **in-note pending banner** appears on the affected note (or in Mobile-Pending-Actions): `> [!note] Pending: … queued — run **PROCESS TASK QUEUE** or **EAT-QUEUE** to apply.`
3. Tap one-tap **Process Queue** (or run **EAT-QUEUE** / **PROCESS TASK QUEUE** in Cursor).
4. Verify the task is marked complete and **banner cleanup** removes the pending callout from the note.
5. Check [[3-Resources/Mobile-Pending-Actions]] and [[3-Resources/Watcher-Result]] for success line.

### Edge cases

1. **Low-conf loop**: Trigger a note in mid-band (68–84%); verify proposal callout appears. Add `approved: true` to frontmatter, run EAT-QUEUE again; verify the note is re-processed.
2. **Success ≤ failure**: Run with one success and one failure (e.g. two queue entries, one invalid). Verify **banner cleanup does not** remove pending callouts from the failed item's note (only when success > failure).
3. **Queue-cleanup**: Set `auto_cleanup_after_process: true` in Second-Brain-Config. Run EAT-QUEUE with a failed entry; verify queue-cleanup marks it and appends a line to [[3-Resources/Errors]].
4. **Batch snapshot threshold**: Run with queue size > `batch_size_for_snapshot` (e.g. 5); verify BATCH_SNAPSHOT_DIR is used. Run with 1–2 items; verify per-change snapshots only.
5. **Mobile seed (SEEDED-ENHANCE)**: Add `<mark>...</mark>` on mobile (no `data-highlight-source`). On laptop, run SEEDED-ENHANCE (queue entry with `mode: "SEEDED-ENHANCE"` and `source_file` set, or trigger "Enhance highlights from seeds"). Verify highlight-seed-enhance runs: seed-weighted extensions and optional gradient; log seed count in Organize-Log or Feedback-Log.

### Mobile Edges

- **Queue BATCH-DISTILL on mobile**: Confirm laptop batch doesn't overwhelm (e.g. cap at 10 items or async_preview_threshold). Verify batch snapshot when batch size > batch_size_for_snapshot.
- **Queue perspective/lens on mobile, process on laptop**: Add queue entry (e.g. HIGHLIGHT PERSPECTIVE or DISTILL LENS) on phone; run EAT-QUEUE on laptop; verify gradients and angles in note and in Distill-Log.
- **Async previews**: Verify previews land in Mobile-Pending-Actions without sync lags; approve via Commander "Async Approve" or approved: true and re-run EAT-QUEUE.

## Master references

- [[3-Resources/Second-Brain/Cursor-Skill-Pipelines-Reference|Cursor-Skill-Pipelines-Reference]] — Canonical pipeline order and skill locations
- [[3-Resources/Second-Brain-Config|Second-Brain-Config]] — Hub names, archive, highlight, graph
