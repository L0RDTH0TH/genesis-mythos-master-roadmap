# Subagent List

**Version: 2026-03 – post-subagent migration**

Table of all subagents and the Queue rule: name, description, responsibilities, and triggers.

---

## Purpose

Quick reference for what each subagent does and when it is used (trigger phrases and queue modes).

---

## Inventory

| Name | Description | When used (triggers) | Key responsibilities | Example invocation |
|------|-------------|----------------------|----------------------|--------------------|
| **Queue (Dispatcher)** | Processes prompt queue and task queue; Step 0 wrappers, read/validate/order, dispatch by mode, Watcher-Result, clear passed | EAT-QUEUE, Process queue, EAT-CACHE, PROCESS TASK QUEUE | Step 0 always-check wrappers; read prompt-queue.jsonl or Task-Queue.md; parse, validate, dedup, order; dispatch each entry; append Watcher-Result per id; clear passed | "EAT-QUEUE" |
| **Ingest** | Full-autonomous-ingest: Ingest/ processing, Phase 1 propose + Decision Wrapper, Phase 2 apply-mode | INGEST MODE, Process Ingest, run ingests; queue mode INGEST MODE | List Ingest; non-MD + image norm; Phase 1 classify, frontmatter-enrich, propose path, create Decision Wrapper (no move); Phase 2 apply when approved wrapper | "INGEST MODE" or `{"mode":"INGEST MODE","source_file":"Ingest/Note.md"}` |
| **Distill** | Autonomous-distill: progressive summarization, highlights, TL;DR, readability; distill-apply-from-wrapper | DISTILL MODE, distill this note, DISTILL LENS, HIGHLIGHT PERSPECTIVE; queue DISTILL MODE, BATCH-DISTILL | Backup; optional auto-layer-select; distill layers; distill-highlight-color; layer-promote; distill-perspective-refine; callout-tldr-wrap; readability-flag; confidence bands | "DISTILL LENS: beginner" |
| **Express** | Autonomous-express: related content, outline, CTA, version snapshots; express-apply-from-wrapper | EXPRESS MODE, express this note, EXPRESS VIEW; queue EXPRESS MODE, BATCH-EXPRESS | Backup; version-snapshot; related-content-pull; research-scope (PMG); express-mini-outline; call-to-action-append; confidence bands | "EXPRESS VIEW: stakeholder" |
| **Archive** | Autonomous-archive: move completed/inactive to 4-Archives/, summary preservation, ghost-folder sweep | ARCHIVE MODE, archive this note, send to Archives; queue ARCHIVE MODE | Backup; classify; archive-check; mid/low bands → refinement or Decision Wrapper; per-change snapshot before move; subfolder-organize; resurface-candidate-mark; summary-preserve; move; ghost-folder sweep | "ARCHIVE MODE" |
| **Organize** | Autonomous-organize: re-classify, re-path, frontmatter-enrich, name-enhance, move in 1/2/3 | ORGANIZE MODE, re-organize this note, classify and move; queue ORGANIZE MODE; FORCE-WRAPPER with source under 1/2/3 | Backup; classify; frontmatter-enrich; subfolder-organize; mid/low bands → refinement or Decision Wrapper; name-enhance; per-change snapshot; move; post-move frontmatter | "ORGANIZE MODE" |
| **Roadmap** | ROADMAP MODE = setup only; RESUME-ROADMAP = one action per run (default deepen) | ROADMAP MODE, Resume roadmap, RESUME-ROADMAP; queue ROADMAP MODE, RESUME-ROADMAP and aliases | Resolve project_id; ROADMAP MODE: Phase 0, roadmap-state + workflow_state, roadmap-generate-from-outline; RESUME-ROADMAP: read params, validate action, branch (deepen, advance-phase, recal, revert-phase, sync-outputs, handoff-audit, expand, etc.); snapshot state before/after | "RESUME-ROADMAP" or "ROADMAP MODE" |
| **Research** | Research helper: queue-only RESEARCH-AGENT pipeline **plus** optional nested helper for inline research consumables | Queue mode RESEARCH-AGENT, RESEARCH-GAPS; nested helper when enabled from roadmap/express/etc. | For RESEARCH-AGENT: resolve project_id and linked_phase; run research-agent-run; queue INGEST (and optionally DISTILL) for new notes; Errors backstop when 0 notes; Watcher-Result. As nested helper: provide `research_consumables` (injection_block_markdown, synth_note_paths, summary, etc.) to caller; never touch queues, wrappers, or Watcher-Result | `{"mode":"RESEARCH-AGENT","source_file":"1-Projects/X/Roadmap/Phase-1.md"}` |
