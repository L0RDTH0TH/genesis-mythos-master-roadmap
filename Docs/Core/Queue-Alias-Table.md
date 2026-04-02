---
title: Queue Alias Table
created: 2026-03-06
tags: [pkm, second-brain, queue, alias, trigger]
para-type: Resource
status: active
links:
  - [[Resources Hub]]
  - [[3-Resources/Second-Brain/README]]
  - [[3-Resources/Second-Brain/Queue-Sources]]
---

# Queue Alias Table

Single reference for **what you say** (aliases / trigger phrases) and **what runs** (queue file, processor, mode). See [[3-Resources/Second-Brain/Queue-Sources]] for queue format and [[.cursor/rules/context/auto-eat-queue|auto-eat-queue]] for processor flow. For a **minimal set of core modes and their guarantees**, see [[3-Resources/Second-Brain/Triggers-Quick-Reference|Triggers-Quick-Reference]]; this note lists additional aliases and specialized modes.  
**Origin semantics:** Question-led Prompt-Crafter is the **primary** way to create queue entries (it emits `mode` + `params` directly); the aliases in this table are **manual/advanced** call formats that power users, Watcher, or Commander may use to drive the same modes without going through Q&A. All such calls are still subject to `core-guardrails` and are routed via `system-funnels`.

## Command aliases → Queue processor

Phrases that start or drive queue processing. Case-insensitive; partial match usually works.


| Alias / phrase you say        | Processor            | Queue file                       | Notes                                                             |
| ----------------------------- | -------------------- | -------------------------------- | ----------------------------------------------------------------- |
| **EAT-QUEUE**                 | auto-eat-queue       | `.technical/prompt-queue.jsonl`  | Step 0 (wrappers) then dispatch by mode; Watcher-Result per entry |
| **Process queue**             | auto-eat-queue       | `.technical/prompt-queue.jsonl`  | Same as EAT-QUEUE                                                 |
| **eat cache** / **EAT-CACHE** | auto-eat-queue       | (pasted payload or prompt-queue) | EAT-CACHE = inline/pasted queue payload instead of file           |
| **PROCESS TASK QUEUE**        | auto-queue-processor | `3-Resources/Task-Queue.md`      | Task/roadmap modes only; Watcher-Result + Mobile-Pending-Actions  |


## Pipeline trigger phrases → Queue mode (manual/advanced entry)

Natural-language triggers that correspond to queue **modes** (used when Watcher/Commander appends an entry or when the agent maps your phrase to a mode). These are considered **manual/advanced call formats** — power-user shortcuts that bypass the Prompt-Crafter Q&A. For high-safety, prefer generating entries via the question-led Prompt-Crafter; direct phrases are reserved for laptop-only, trusted flows and are still subject to `core-guardrails` and routed via `system-funnels`.


| Trigger phrase (example)                                                                                                     | Canonical mode             | Pipeline                                                                                                                                                                                                                                                                             |
| ---------------------------------------------------------------------------------------------------------------------------- | -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| INGEST MODE, **Process Ingest**, run ingests                                                                                 | INGEST_MODE                | full-autonomous-ingest                                                                                                                                                                                                                                                               |
| **ORGANIZE MODE** – safe batch autopilot, re-organize this note, classify and move                                           | ORGANIZE_MODE              | autonomous-organize                                                                                                                                                                                                                                                                  |
| **DISTILL MODE** – safe batch autopilot, distill this note, refine this note                                                 | DISTILL_MODE               | autonomous-distill                                                                                                                                                                                                                                                                   |
| **EXPRESS MODE** – safe batch autopilot, express this note, generate outline                                                 | EXPRESS_MODE               | autonomous-express                                                                                                                                                                                                                                                                   |
| **ARCHIVE MODE** – safe batch autopilot, archive this note, send to Archives                                                 | ARCHIVE_MODE               | autonomous-archive                                                                                                                                                                                                                                                                   |
| **ATOMIZE MODE** – safe batch autopilot, atomize this note                                                                   | ATOMIZE_MODE               | autonomous-atomize (AtomizeSubagent): `obsidian_split_atomic` + `split-link-preserve` with no moves/renames; callable from Ingest/ or directly on PARA notes under 1-Projects/, 2-Areas/, 3-Resources/                                                                              |
| Enhance highlights from seeds, **SEEDED-ENHANCE**                                                                            | SEEDED_ENHANCE             | highlight-seed-enhance (via organize/distill context)                                                                                                                                                                                                                                |
| **BATCH-DISTILL** (after cascade proposal)                                                                                   | BATCH_DISTILL              | autonomous-distill (batch)                                                                                                                                                                                                                                                           |
| **BATCH-EXPRESS** (after cascade proposal)                                                                                   | BATCH_EXPRESS              | autonomous-express (batch)                                                                                                                                                                                                                                                           |
| Re-process after async preview                                                                                               | ASYNC_LOOP                 | Re-run with approved/feedback                                                                                                                                                                                                                                                        |
| Name-enhance batch, **NAME-REVIEW**                                                                                          | NAME_REVIEW                | name-enhance (batch; optional scope)                                                                                                                                                                                                                                                 |
| Create wrapper instead of destructive step                                                                                   | **FORCE_WRAPPER**          | Pipeline inferred from source_file; output = Decision Wrapper                                                                                                                                                                                                                        |
| (internal) Check approved wrappers first                                                                                     | CHECK_WRAPPERS             | Step 0 of auto-eat-queue (always runs)                                                                                                                                                                                                                                               |
| **GARDEN REVIEW**, run garden review, orphans and distill candidates, garden health, vault orphans, distill candidates sweep | **GARDEN_REVIEW**          | auto-garden-review: obsidian_garden_review → feed report to distill/organize batches                                                                                                                                                                                                 |
| **CURATE CLUSTER** #tag, suggest gaps and merges, cluster curate #tag, theme gaps #tag, merge suggestions 3-Resources/…      | **CURATE_CLUSTER**         | auto-curate-cluster: obsidian_curate_cluster → analyze report; optional split/MOC/merge                                                                                                                                                                                              |
| **ROADMAP MODE** (generate from outline)                                                                                     | **ROADMAP_MODE**           | auto-roadmap: setup only (Phase 0 + workflow_state + roadmap-generate-from-outline); no continue logic                                                                                                                                                                               |
| **Resume roadmap**, **RESUME_ROADMAP**                                                                                       | **RESUME_ROADMAP**         | auto-roadmap: single continue entry; params.action = deepen (default) \| recal \| revert-phase \| sync-outputs \| handoff-audit \| resume-from-last-safe \| expand. **Context tracking:** default **ON** for all deepen runs; dashes (`\"-\"`) in `workflow_state ## Log` context columns are only valid when a specific queue entry explicitly sets `enable_context_tracking: false`. |
| **Recalibrate roadmap**, RECAL-ROAD                                                                                          | **RESUME_ROADMAP** (alias) | params.action: "recal" → roadmap-audit + optional sync + validate                                                                                                                                                                                                                    |
| **Sync phase outputs**                                                                                                       | **RESUME_ROADMAP** (alias) | params.action: "sync-outputs" → roadmap-phase-output-sync                                                                                                                                                                                                                            |
| **Reopen Phase**, **Revert Phase N**, REVERT-PHASE                                                                           | **RESUME_ROADMAP** (alias) | params.action: "revert-phase", params.phase: N → roadmap-revert                                                                                                                                                                                                                      |
| **Resume from last safe phase**, RESUME-FROM-LAST-SAFE                                                                       | **RESUME_ROADMAP** (alias) | params.action: "resume-from-last-safe" → find safe phase then deepen                                                                                                                                                                                                                 |
| **Handoff audit**, HANDOFF-AUDIT                                                                                             | **RESUME_ROADMAP** (alias) | params.action: "handoff-audit" → hand-off-audit on phase                                                                                                                                                                                                                             |
| **Expand road**, EXPAND-ROAD                                                                                                 | **RESUME_ROADMAP** (alias) | params.action: "expand", sectionOrTaskLocator, userText → expand-road-assist. For **aggressive structure** (folders + notes): use action: "deepen" with granularity + user_guidance; see [[3-Resources/Second-Brain/Roadmap-Quality-Guide#Aggressive deepening (crank the levers)]]. |
| **DEEPEN-AGGRESSIVE**                                                                                                        | **RESUME_ROADMAP** (alias) | params.action: "deepen", inject_extra_state: true, token_cap: 50000, branch_factor: 4, highlight_angles: ["narrative","tech","edge"]. Smoke test: run EAT-QUEUE → expect util 45–65% on next workflow_state Log row. See Queue-Sources § DEEPEN-AGGRESSIVE.                          |
| **Queue research for phase**, **Queue Research: Phase**, RESEARCH-AGENT                                                      | **RESEARCH_AGENT**         | research-agent-run: query → fetch → synthesize; write to Ingest/Agent-Research/; queue INGEST_MODE for new notes; Commander macro "Queue Research: Phase"                                                                                                                            |
| **Queue Research: Gaps**, **RESEARCH-GAPS**                                                                                  | **RESEARCH_AGENT** (alias) | research-agent-run (gap-fill): scan current phase note for gaps via MCP read_note + gap detection; append RESEARCH_AGENT entry with `gaps` array. Commander macro "Queue Research: Gaps" runs from roadmap phase note.                                                               |
| **Normalize master goal**, NORMALIZE-MASTER-GOAL                                                                             | **NORMALIZE_MASTER_GOAL**  | normalize-master-goal: restructure PMG at source_file to Master-Goal template                                                                                                                                                                                                        |
| **Scoping** (PMG), SCOPING MODE                                                                                              | **SCOPING_MODE** (alias)   | DISTILL_MODE then EXPRESS_MODE on same note (PMG); research-scope runs in express                                                                                                                                                                                                    |
| **Audit context**, AUDIT-CONTEXT                                                                                             | **AUDIT_CONTEXT**          | context-vs-pipeline-audit: compare workflow_state context vs pipeline focus; output to Audit-Context-Focus.md                                                                                                                                                                        |


## Chain command aliases (Phase 3)

Single queue entry that expands into multiple pipelines in order: run dependency mode(s) first, then primary with collected results. Format: `PRIMARY_MODE-DEP1-DEP2-...`. See [[3-Resources/Second-Brain/Queue-Sources#Chain modes (Phase 3)|Queue-Sources § Chain modes]].


| Trigger phrase (example)                                      | Canonical chain mode                 | Execution order                                                                 |
| ------------------------------------------------------------- | ------------------------------------ | ------------------------------------------------------------------------------- |
| **Resume roadmap with research**, RESUME_ROADMAP-RESEARCH      | RESUME_ROADMAP-RESEARCH              | RESEARCH_AGENT → RESUME_ROADMAP (research results injected into roadmap hand-off) |
| **Resume roadmap with research and ingest**, RESUME_ROADMAP-RESEARCH-INGEST | RESUME_ROADMAP-RESEARCH-INGEST       | RESEARCH_AGENT → INGEST_MODE → RESUME_ROADMAP                                   |


## Task-Queue modes (Task-Queue.md)

Used when you say **PROCESS TASK QUEUE** or when entries are appended to `3-Resources/Task-Queue.md`.


| Mode              | Skill / behavior       |
| ----------------- | ---------------------- |
| TASK_ROADMAP      | Roadmap open / display |
| TASK_COMPLETE     | task-complete-validate |
| ADD_ROADMAP_ITEM  | add-roadmap-append     |
| EXPAND_ROAD       | expand-road-assist     |
| REORDER_ROADMAP   | Reorder roadmap items  |
| DUPLICATE_ROADMAP | Duplicate roadmap      |
| MERGE_ROADMAPS    | Merge two roadmaps     |
| EXPORT_ROADMAP    | Export roadmap         |
| PROGRESS_REPORT   | Progress report output |


## Lens / view aliases (set context, then run pipeline)

These set frontmatter or queue payload, then invoke the same pipelines.


| Phrase                              | Frontmatter / payload                                  | Pipeline                                                                                       |
| ----------------------------------- | ------------------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| **DISTILL LENS: [angle]**           | `distill_lens: [angle]`                                | autonomous-distill (with lens)                                                                 |
| **EXPRESS VIEW: [angle]**           | `express_view: [angle]`                                | autonomous-express (with view)                                                                 |
| **HIGHLIGHT PERSPECTIVE: [lens]**   | `highlight_perspective: [lens]` or queue `perspective` | distill/highlight pass with perspective                                                        |
| **SWITCH HIGHLIGHT ANGLE: [angle]** | `highlight_active_angle: [angle]`                      | Set current angle; re-run highlight for that angle or CSS/Dataview-driven switch               |
| **HIGHLIGHT MULTI-ANGLE: [list]**   | `highlight_angles: [list]`                             | Queue runs per angle or single batch applying multiple angles; see highlight-perspective-layer |


## Cross-references

- **Aggressive deepening** (queue chain, hierarchy, validate): [[3-Resources/Second-Brain/Roadmap-Quality-Guide#Aggressive deepening (crank the levers)]]
- **Queue format and modes**: [[3-Resources/Second-Brain/Queue-Sources]]
- **Canonical order (prompt queue)**: INGEST_MODE → ORGANIZE_MODE → TASK_ROADMAP → RESEARCH_AGENT → … → ARCHIVE_MODE → AUDIT_CONTEXT → TASK_COMPLETE → ADD_ROADMAP_ITEM
- **Parameters (queue modes)**: [[3-Resources/Second-Brain/Parameters#Queue modes]]
- **Pipelines overview**: [[3-Resources/Second-Brain/Pipelines]]



https://grok.com/share/c2hhcmQtMg_cdc1a5ea-1287-4d3a-8102-e1f9a01dd653