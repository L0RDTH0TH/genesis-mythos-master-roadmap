---
title: Queue Alias Table
created: 2026-03-06
tags: [pkm, second-brain, queue, alias, trigger]
para-type: Resource
status: active
links: ["[[Resources Hub]]", "[[3-Resources/Second-Brain/README]]", "[[3-Resources/Second-Brain/Queue-Sources]]"]
---

# Queue Alias Table

Single reference for **what you say** (aliases / trigger phrases) and **what runs** (queue file, processor, mode). See [[3-Resources/Second-Brain/Queue-Sources]] for queue format and [[.cursor/rules/context/auto-eat-queue|auto-eat-queue]] for processor flow.

## Command aliases → Queue processor

Phrases that start or drive queue processing. Case-insensitive; partial match usually works.

| Alias / phrase you say | Processor | Queue file | Notes |
|------------------------|-----------|------------|--------|
| **EAT-QUEUE** | auto-eat-queue | `.technical/prompt-queue.jsonl` | Step 0 (wrappers) then dispatch by mode; Watcher-Result per entry |
| **Process queue** | auto-eat-queue | `.technical/prompt-queue.jsonl` | Same as EAT-QUEUE |
| **eat cache** / **EAT-CACHE** | auto-eat-queue | (pasted payload or prompt-queue) | EAT-CACHE = inline/pasted queue payload instead of file |
| **PROCESS TASK QUEUE** | auto-queue-processor | `3-Resources/Task-Queue.md` | Task/roadmap modes only; Watcher-Result + Mobile-Pending-Actions |

## Pipeline trigger phrases → Queue mode

Natural-language triggers that correspond to queue **modes** (used when Watcher/Commander appends an entry or when the agent maps your phrase to a mode).

| Trigger phrase (example) | Canonical mode | Pipeline |
|---------------------------|----------------|----------|
| INGEST MODE, **Process Ingest**, run ingests | INGEST MODE | full-autonomous-ingest |
| **ORGANIZE MODE** – safe batch autopilot, re-organize this note, classify and move | ORGANIZE MODE | autonomous-organize |
| **DISTILL MODE** – safe batch autopilot, distill this note, refine this note | DISTILL MODE | autonomous-distill |
| **EXPRESS MODE** – safe batch autopilot, express this note, generate outline | EXPRESS MODE | autonomous-express |
| **ARCHIVE MODE** – safe batch autopilot, archive this note, send to Archives | ARCHIVE MODE | autonomous-archive |
| Enhance highlights from seeds, **SEEDED-ENHANCE** | SEEDED-ENHANCE | highlight-seed-enhance (via organize/distill context) |
| **BATCH-DISTILL** (after cascade proposal) | BATCH-DISTILL | autonomous-distill (batch) |
| **BATCH-EXPRESS** (after cascade proposal) | BATCH-EXPRESS | autonomous-express (batch) |
| Re-process after async preview | ASYNC-LOOP | Re-run with approved/feedback |
| Name-enhance batch, **NAME-REVIEW** | NAME-REVIEW | name-enhance (batch; optional scope) |
| Create wrapper instead of destructive step | **FORCE-WRAPPER** | Pipeline inferred from source_file; output = Decision Wrapper |
| (internal) Check approved wrappers first | CHECK_WRAPPERS | Step 0 of auto-eat-queue (always runs) |
| **GARDEN REVIEW**, run garden review, orphans and distill candidates, garden health, vault orphans, distill candidates sweep | **GARDEN-REVIEW** | auto-garden-review: obsidian_garden_review → feed report to distill/organize batches |
| **CURATE CLUSTER** #tag, suggest gaps and merges, cluster curate #tag, theme gaps #tag, merge suggestions 3-Resources/… | **CURATE-CLUSTER** | auto-curate-cluster: obsidian_curate_cluster → analyze report; optional split/MOC/merge |

## Task-Queue modes (Task-Queue.md)

Used when you say **PROCESS TASK QUEUE** or when entries are appended to `3-Resources/Task-Queue.md`.

| Mode | Skill / behavior |
|------|-------------------|
| TASK-ROADMAP | Roadmap open / display |
| TASK-COMPLETE | task-complete-validate |
| ADD-ROADMAP-ITEM | add-roadmap-append |
| EXPAND-ROAD | expand-road-assist |
| REORDER-ROADMAP | Reorder roadmap items |
| DUPLICATE-ROADMAP | Duplicate roadmap |
| MERGE-ROADMAPS | Merge two roadmaps |
| EXPORT-ROADMAP | Export roadmap |
| PROGRESS-REPORT | Progress report output |

## Lens / view aliases (set context, then run pipeline)

These set frontmatter or queue payload, then invoke the same pipelines.

| Phrase | Frontmatter / payload | Pipeline |
|--------|------------------------|----------|
| **DISTILL LENS: [angle]** | `distill_lens: [angle]` | autonomous-distill (with lens) |
| **EXPRESS VIEW: [angle]** | `express_view: [angle]` | autonomous-express (with view) |
| **HIGHLIGHT PERSPECTIVE: [lens]** | `highlight_perspective: [lens]` or queue `perspective` | distill/highlight pass with perspective |
| **SWITCH HIGHLIGHT ANGLE: [angle]** | `highlight_active_angle: [angle]` | Set current angle; re-run highlight for that angle or CSS/Dataview-driven switch |
| **HIGHLIGHT MULTI-ANGLE: [list]** | `highlight_angles: [list]` | Queue runs per angle or single batch applying multiple angles; see highlight-perspective-layer |

## Cross-references

- **Queue format and modes**: [[3-Resources/Second-Brain/Queue-Sources]]
- **Canonical order (prompt queue)**: INGEST → ORGANIZE → TASK-ROADMAP → DISTILL → EXPRESS → ARCHIVE → TASK-COMPLETE → ADD-ROADMAP-ITEM
- **Parameters (queue modes)**: [[3-Resources/Second-Brain/Parameters#Queue modes]]
- **Pipelines overview**: [[3-Resources/Second-Brain/Pipelines]]
