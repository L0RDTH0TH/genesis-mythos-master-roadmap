# Examples

**Version: 2026-03 – post-subagent migration**

Concrete usage examples for common flows: INGEST MODE, RESUME-ROADMAP deepen, DISTILL LENS, EAT-QUEUE, and others.

---

## Purpose

Copy-paste or adapt these triggers and queue payloads to run pipelines and understand how the Queue and subagents interact.

---

## INGEST MODE

1. User says **"INGEST MODE"** or **"Process Ingest"** (or "run ingests").
2. System-funnels route to the **Ingest subagent** (or legacy ingest rule).
3. Subagent lists `Ingest/`, runs non-MD handling and embedded image normalization as needed, then for each .md runs **Phase 1**: classify PARA, frontmatter-enrich, propose path, create Decision Wrapper (no move). If the run was triggered by an **approved wrapper** (e.g. after EAT-QUEUE Step 0), it runs **Phase 2 apply-mode**: move/rename to approved path after snapshot and dry_run.
4. **Example:** "Process Ingest" → Ingest runs on notes in `Ingest/*.md`; new or ambiguous notes get a Decision Wrapper; user approves; next EAT-QUEUE applies the move.

---

## RESUME-ROADMAP deepen

1. User runs **EAT-QUEUE** with e.g. `{"mode":"RESUME-ROADMAP","project_id":"my-project","id":"req-1"}` (action defaults to **deepen**).
2. Dispatcher loads the **Queue rule**. Queue runs **Step 0**, then reads `.technical/prompt-queue.jsonl`, parses/validates/orders, and dispatches the RESUME-ROADMAP entry to the **Roadmap subagent**.
3. Roadmap resolves project_id, reads `roadmap-state.md` and `workflow_state.md`, merges params, runs **one deepen step** (roadmap-deepen), updates workflow_state (and may append a follow-up RESUME-ROADMAP line when queue_next !== false), then returns a summary and appends a Watcher-Result line for req-1.
4. **Example:** One EAT-QUEUE run can process one or more queue lines; each RESUME-ROADMAP entry triggers one action (e.g. one deepen step).

---

## DISTILL LENS

1. User says **"DISTILL LENS: beginner"** (with current note in context).
2. System-funnels route to the **Distill subagent**.
3. Subagent sets or uses **distill_lens** (e.g. "beginner") and runs autonomous-distill: backup, optional auto-layer-select, distill layers, distill-highlight-color, layer-promote, distill-perspective-refine, callout-tldr-wrap, readability-flag. Confidence bands apply; mid/low may create a Decision Wrapper.
4. **Example:** "DISTILL LENS: beginner" on a technical note → TL;DR and highlights shaped for a beginner audience.

---

## EXPRESS VIEW

1. User says **"EXPRESS VIEW: stakeholder high-level"** or adds a queue entry with **express_view** set.
2. System-funnels or Queue dispatches to the **Express subagent**.
3. Subagent runs: backup, version-snapshot, related-content-pull, research-scope (if PMG), express-mini-outline, express-view-layer (using express_view), call-to-action-append.
4. **Example:** EXPRESS VIEW: stakeholder → outline and Related section tuned for a stakeholder.

---

## EAT-QUEUE (batch)

1. User says **"EAT-QUEUE"** (or "Process queue", "EAT-CACHE", "eat cache").
2. **Dispatcher** loads the **Queue rule**.
3. Queue runs **Step 0:** Scan `Ingest/Decisions/**`; for each wrapper with approved (or re-wrap/re-try) and not processed, apply (e.g. move note to approved_path, archive wrapper to 4-Archives/Ingest-Decisions/).
4. Queue reads `.technical/prompt-queue.jsonl`, parses, validates, dedups, orders by canonical order.
5. For each entry: dispatch by mode to the right subagent (or skill); append one line to `3-Resources/Watcher-Result.md` (requestId, status, message, trace, completed).
6. Clear passed entries from the queue file (re-read, omit processed_success_ids, write back).
7. **Example:** Queue with one INGEST MODE and one RESUME-ROADMAP → Step 0 runs; then Ingest runs for the first entry, then Roadmap for the second; two Watcher-Result lines; both entries cleared.

---

## PROCESS TASK QUEUE

1. User says **"PROCESS TASK QUEUE"** (or EAT-QUEUE with clear intent for the task queue).
2. Queue rule runs the **Task-queue flow**: read `3-Resources/Task-Queue.md`, parse JSON lines, dispatch by mode (TASK-ROADMAP, TASK-COMPLETE, ADD-ROADMAP-ITEM, EXPAND-ROAD, etc.) to the corresponding skills.
3. Append one line per processed entry to Watcher-Result; update `3-Resources/Mobile-Pending-Actions.md`; optional banner cleanup; optionally clear processed entries.
4. **Example:** One TASK-COMPLETE entry → task-complete-validate runs; one ADD-ROADMAP-ITEM → add-roadmap-append runs.

---

## RESEARCH-AGENT (queue)

1. Queue contains e.g. `{"mode":"RESEARCH-AGENT","source_file":"1-Projects/X/Roadmap/Phase-2.md","id":"req-2"}`.
2. Queue rule dispatches to the **Research subagent**.
3. Research resolves **project_id** and **linked_phase** from the path. If either missing, skip entry and append Watcher-Result failure.
4. Research runs **research-agent-run** (vault-first → query gen → fetch → synthesize → write to `Ingest/Agent-Research/`).
5. For each new note path, Research instructs the parent/Queue to queue **INGEST MODE** (and optionally **DISTILL MODE** if params.research_distill). Queue processor preserves these when merging at Step 8.
6. Research appends one Watcher-Result line for req-2. If 0 notes returned, add error entry and treat as failure (no processed_success_ids).
7. **Example:** RESEARCH-AGENT with source_file pointing at a phase note → research runs for that phase; new notes land in Ingest/Agent-Research/ and get INGEST (and optionally DISTILL) queue entries for the next EAT-QUEUE.

---

<!-- Gap filled from old Cursor-Skill-Pipelines-Reference.md / Queue-Sources.md -->
- **Laptop-only:** EAT-QUEUE and PROCESS TASK QUEUE are run from the laptop; queue files are written from the laptop (Crafter, Commander, or manual). Mobile does not append to queues; see Mobile-Migration-Spec.
- **Fast-path:** When the prompt queue has exactly **one valid entry**, the Queue rule skips dedup and sort and dispatches that entry immediately (Queue-Sources; queue.mdc A.2).
