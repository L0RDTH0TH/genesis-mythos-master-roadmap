# Subagent List

**Version: 2026-03 – post-subagent migration**

Quick reference: all subagents and the Queue rule — when each is used and main responsibilities.

---

## Table

| Name | Description | Triggers | Responsibilities |
|------|-------------|----------|-------------------|
| **Queue (Dispatcher)** | Processes prompt queue and task queue; Step 0 wrappers, read/validate/order, dispatch by mode, Watcher-Result, clear passed | EAT-QUEUE, Process queue, EAT-CACHE, PROCESS TASK QUEUE | Step 0 always-check wrappers; read `.technical/prompt-queue.jsonl` or `3-Resources/Task-Queue.md`; parse, validate, dedup, order; dispatch each entry; append Watcher-Result per id; clear passed entries |
| **Ingest** | Full-autonomous-ingest: Phase 1 propose + Decision Wrapper, Phase 2 apply-mode | INGEST MODE, Process Ingest, run ingests; queue mode INGEST MODE | List Ingest; non-MD handling; Phase 1 classify, frontmatter-enrich, propose path, Decision Wrapper (no move); Phase 2 apply when approved (move/rename); backup + snapshot before destructive steps |
| **Distill** | Autonomous-distill: progressive summarization, highlights, TL;DR, readability; distill-apply-from-wrapper | DISTILL MODE, distill this note, DISTILL LENS, HIGHLIGHT PERSPECTIVE; queue DISTILL MODE, BATCH-DISTILL | Backup; optional auto-layer-select; distill layers; distill-highlight-color; layer-promote; distill-perspective-refine; callout-tldr-wrap; readability-flag; confidence bands and Decision Wrappers for mid/low |
| **Express** | Autonomous-express: related content, outline, CTA, version snapshots; express-apply-from-wrapper | EXPRESS MODE, express this note, EXPRESS VIEW; queue EXPRESS MODE, BATCH-EXPRESS | Backup; version-snapshot; related-content-pull; research-scope (PMG); express-mini-outline; call-to-action-append; confidence bands and Decision Wrappers for mid/low |
| **Archive** | Autonomous-archive: move completed/inactive to 4-Archives/, summary preservation, ghost-folder sweep | ARCHIVE MODE, archive this note, send to Archives; queue ARCHIVE MODE | Backup; classify; archive-check; mid/low → refinement loop or Decision Wrapper; per-change snapshot before move; subfolder-organize; resurface-candidate-mark; summary-preserve; move; ghost-folder sweep |
| **Organize** | Autonomous-organize: re-classify, re-path, frontmatter-enrich, name-enhance, move in 1/2/3 | ORGANIZE MODE, re-organize this note, classify and move; queue ORGANIZE MODE; FORCE-WRAPPER with source under 1/2/3 | Backup; classify; frontmatter-enrich; subfolder-organize; mid/low → refinement or Decision Wrapper; name-enhance; per-change snapshot before rename/move; move; post-move frontmatter |
| **Roadmap** | ROADMAP MODE = setup only; RESUME-ROADMAP = one action per run (default deepen) | ROADMAP MODE, Resume roadmap, RESUME-ROADMAP; queue ROADMAP MODE, RESUME-ROADMAP and aliases | Resolve project_id; ROADMAP MODE: Phase 0, roadmap-state + workflow_state, roadmap-generate-from-outline; RESUME-ROADMAP: branch by action (deepen, advance-phase, recal, revert-phase, sync-outputs, handoff-audit, expand, etc.); snapshot state before/after; append workflow_state log row when state mutated |
| **Research** | Queue-only RESEARCH-AGENT: project_id + linked_phase, research-agent-run, queue INGEST/DISTILL for new notes | Queue mode RESEARCH-AGENT, RESEARCH-GAPS | Resolve project_id and linked_phase; run research-agent-run; queue INGEST (and optionally DISTILL) for new notes; Errors backstop when 0 notes; Watcher-Result per entry |
| **Internal Repair Agent (IRA)** | Nested helper only: structural repair planner; emits `suggested_fixes` with `risk_level`; caller pipeline applies fixes when guardrails allow | **Never** queue-dispatched; **never** called from Layer 1 post–little-val validator | Invoked only via nested **`Task`** from pipeline subagents (ingest, roadmap, archive, organize, distill, express, research when contract applies) per [[3-Resources/Second-Brain/Subagent-Safety-Contract|Subagent-Safety-Contract]] and **`.cursor/agents/internal-repair-agent.md`**. Full contract: little-val failure cycles; validator → IRA → apply → (little val) → second nested validator when configured (`ira_after_first_pass`, etc.). |
| **PromptCraft** | Recovery-only: suggested JSONL queue lines from `prompt_craft_request`, **A.5b** (`craft_source: a5b_post_little_val`), **A.1b** empty-queue bootstrap (`craft_source: empty_queue_bootstrap`), or Layer 0 failure context | **REPAIR CRAFT**, **PROMPT CRAFT RECOVERY** (Layer 0); queue **A.5d** when `recovery_auto_craft_enabled`; **A.5b** when `post_little_val_repair_use_prompt_craft`; **A.1b** when `queue_continuation.empty_queue_bootstrap_prompt_craft` | Read-mostly; deepMerge-style params; per-mode lint; returns `jsonl_lines_suggested` + `lint_blockers`; does **not** append `prompt-queue.jsonl` — Layer 0/L1 only. See [[Prompt-Craft-Subagent]]. |

---

## Nested subagent whitelist

Only the following **caller → nested subagent** pairs are allowed. Nested subagents are **helpers only** and must not orchestrate, write queues, create Decision Wrappers, or write Watcher-Result directly.

| Caller (pipeline subagent) | Allowed nested subagent(s) | Purpose |
|---------------------------|----------------------------|---------|
| **Roadmap**               | **Research**               | Pre-deepen or gap-focused research for the current project/phase; returns research summaries and note paths only. |
| **Roadmap**               | **Validator**              | Hostile validation for roadmap artifacts (e.g. `roadmap_handoff_auto`, handoff-style checks); returns validation report path and verdict; read-only on inputs except the report note. |
| **Roadmap**               | **Internal Repair Agent**   | When the contract requires: after little-val failures or per nested-validator policy, run IRA inside the same pipeline **Task**; apply `suggested_fixes` when gates pass; see **`.cursor/agents/internal-repair-agent.md`** and [[3-Resources/Second-Brain/Subagent-Safety-Contract|Subagent-Safety-Contract]]. |
| **Ingest / Organize / Archive / Distill / Express** | **Validator** | **Mandatory** (for Success): when the pipeline returns **Success** with **`little_val_ok: true`**, the subagent **must** have run **ValidatorSubagent** with the correct **`validation_type`** and params for that pipeline (`ingest_classification`, `organize_path`, `archive_candidate`, `distill_readability`, `express_summary` per [[3-Resources/Second-Brain/Queue-Sources|Queue-Sources]] § Post-pipeline validator / agent rules). Returns findings; tiered Success gate per Subagent-Safety-Contract (**`high` / `block_destructive`** blocks Success; **`needs_work`** may allow Success when tiering enabled). Validator does not orchestrate queues or wrappers. |
| **Ingest / Organize / Archive / Distill / Express** | **Internal Repair Agent** | When little val cannot reach `ok: true` within attempts, or when **`ira_after_first_pass`** (and related config) requires a pass after the first nested validator: run **IRA** inside the same pipeline **Task**, then re-run little val / second validator as specified in **`.cursor/agents/internal-repair-agent.md`**. **Queue (Layer 1) never invokes IRA** (including after post–little-val validator). |

- **Queue (Dispatcher)** is **never** called as a nested subagent.
- **Internal Repair Agent** is **never** queue-dispatched and **never** invoked by the post–little-val Validator pass on Layer 1; only nested from pipeline **Task** contexts per contract.
- **PromptCraft** is **never** called from IRA, Validator, or pipeline Tasks — only **Layer 0** (manual trigger) or **Layer 1** (queue **A.5d**, optional **A.5b**, optional **A.1b** empty-queue bootstrap).
- **Research** and **Validator** are treated as **leaf or near-leaf** subagents: they may in turn use MCP tools, but must not dispatch other pipeline subagents or manipulate queues.
- Any other nested pairing is **disallowed** unless it is added to this table and documented in both the caller’s and callee’s specs.

---

## Example invocations

- **Queue:** "EAT-QUEUE"
- **Ingest:** "INGEST MODE" or `{"mode":"INGEST MODE","source_file":"Ingest/Note.md"}`
- **Distill:** "DISTILL LENS: beginner"
- **Express:** "EXPRESS VIEW: stakeholder"
- **Archive:** "ARCHIVE MODE"
- **Organize:** "ORGANIZE MODE"
- **Roadmap:** "RESUME-ROADMAP" or "ROADMAP MODE"
- **Research:** `{"mode":"RESEARCH-AGENT","source_file":"1-Projects/X/Roadmap/Phase-1.md"}`
- **PromptCraft:** "REPAIR CRAFT" with pasted `prompt_craft_request` YAML, or automatic **A.5d** after pipeline failure when Config enabled, or **A.1b** when prompt queue empty and continuation bootstrap + PromptCraft flags enabled
