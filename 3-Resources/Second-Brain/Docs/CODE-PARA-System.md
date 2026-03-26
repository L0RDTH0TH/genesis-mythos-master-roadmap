# CODE PARA System

**Version: 2026-03**

Defines how CODE-side automation flows map into PARA and how queue-driven runs behave from prompt craft to pipeline execution.

---

## Purpose

Provide one canonical reference for the CODE lane: ingest, organize, distill, express, archive, and queue orchestration, with safety and confidence gates.

---

## Scope

- **In scope:** `INGEST MODE`, `ORGANIZE MODE`, `DISTILL MODE`, `EXPRESS MODE`, `ARCHIVE MODE`, `EAT-QUEUE`, `PROCESS TASK QUEUE`, prompt-crafter CODE branch.
- **Out of scope:** roadmap setup/deepen semantics (covered in `Roadmapping-System.md` and `Pipelines/Roadmap-Pipeline.md`).

---

## Core Flow

1. Craft a CODE payload (`mode` + optional `params`) with question-led prompt crafter.
2. Append one JSONL queue line after explicit confirmation.
3. Run `EAT-QUEUE` (or `PROCESS TASK QUEUE` for task modes).
4. Queue layer validates, orders, and dispatches by mode to the correct subagent.
5. Pipeline executes under guardrails (backup/snapshot/confidence).
6. One `Watcher-Result` line is appended per processed queue entry.

---

## PARA Mapping Rules

- **Ingest starts in `Ingest/`** and classifies to PARA (`1-Projects`, `2-Areas`, `3-Resources`) before move.
- **Phase 1 ingest is propose-first** (Decision Wrapper path), except explicit direct-move policy branches for qualifying agent-generated notes.
- **Organize re-evaluates existing PARA notes** and may rename/move when confidence and snapshot gates pass.
- **Archive moves only to `4-Archives/`** for completed/inactive notes after archive checks.
- **Distill/Express are refinement pipelines** over active PARA notes and do not redefine PARA classification.

---

## Safety Contract (CODE lane)

- Backup before destructive actions.
- Per-change snapshot before rewrite/move/rename/append-into-other-note operations.
- Confidence gates:
  - `>=85`: destructive actions allowed after snapshot.
  - `68-84`: one non-destructive refinement loop.
  - `<68`: no destructive actions; route to Decision Wrapper / review flow.
- `obsidian_move_note` must use `dry_run: true` before commit.

---

## Queue + Routing Notes

- Prompt queue: `.technical/prompt-queue.jsonl`.
- Task queue: `3-Resources/Task-Queue.md`.
- Queue dispatch order and mode routing are governed by `Queue-Sources.md`.
- `EAT-QUEUE` always runs wrapper Step 0 before processing queue entries.

---

## Related Docs

- `Pipelines/Ingest-Pipeline.md`
- `Pipelines/Organize-Pipeline.md`
- `Pipelines/Distill-Pipeline.md`
- `Pipelines/Express-Pipeline.md`
- `Pipelines/Archive-Pipeline.md`
- `Pipelines/Queue-Pipeline.md`
- `Queue-Sources.md`
- `Parameters.md`
