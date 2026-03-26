# CODE PARA System

**Version: 2026-03**

Canonical operational reference for the CODE lane: how content moves from capture to PARA placement and maintenance through ingest, organize, distill, express, archive, and queue orchestration.

---

## Purpose

Define the full CODE execution model end-to-end:

- entry paths (prompt-crafter and manual),
- queue contracts and dispatch behavior,
- PARA classification and movement policy,
- confidence/snapshot safety gates,
- logs, watcher output, and failure handling.

---

## System scope

### In scope

- `INGEST MODE`
- `ORGANIZE MODE`
- `DISTILL MODE`
- `EXPRESS MODE`
- `ARCHIVE MODE`
- `EAT-QUEUE` / `Process queue`
- `PROCESS TASK QUEUE`
- question-led prompt-crafter CODE branch and queue append contract

### Out of scope

- Roadmap setup/resume semantics (see `Roadmapping-System.md`).

---

## Entry and dispatch model

### Preferred entry

1. Craft a CODE payload (`mode` + optional `params`) through question-led prompt-crafter.
2. Confirm append.
3. Write one JSONL entry to `.technical/prompt-queue.jsonl` (or to task queue for task modes).
4. Run `EAT-QUEUE` / `PROCESS TASK QUEUE`.

### Manual/advanced entry

- Direct triggers (`INGEST MODE`, `DISTILL MODE`, etc.) bypass prompt-crafter Q&A but still route through the same dispatch and safety contracts.

### Dispatch sequence

1. Queue Step 0 checks/handles approved wrappers.
2. Queue file is read and validated.
3. Modes are normalized and ordered.
4. Matching pipeline subagent is dispatched.
5. One watcher result line is written per processed entry.
6. Successful queue entries are removed; failures are retained/marked.

---

## PARA mapping and lifecycle policy

### Capture and classification

- New/unhandled inputs begin in `Ingest/`.
- Ingest classifies to PARA intent (`1-Projects`, `2-Areas`, `3-Resources`) and enriches metadata before movement decisions.

### Placement and maintenance

- **Ingest** is proposal-first by default (Decision Wrapper path), with explicit direct-move exceptions for qualified agent-generated notes.
- **Organize** re-evaluates and can rename/move active PARA notes when confidence and snapshot gates pass.
- **Distill/Express** refine content quality and communication shape; they do not redefine PARA type by default.
- **Archive** moves only archive-ready notes into `4-Archives/`.

### Queue-bound wrapper lifecycle

- Mid/low confidence and specific policy outcomes produce wrappers under `Ingest/Decisions/**`.
- Wrapper approvals are applied by queue Step 0 before normal queue entry dispatch.

---

## Pipeline responsibilities (CODE lane)

- **Ingest**: intake handling, non-md companion handling, metadata enrichment, proposal/wrapper or qualified direct apply.
- **Organize**: path recalibration, optional name enhancement, safe move pathing.
- **Distill**: layered refinement, readability support, highlight/lens shaping.
- **Express**: related content pull, outline framing, CTA/publishability shaping.
- **Archive**: readiness evaluation, summary preservation, safe move to archives, ghost-folder cleanup.

---

## Safety and confidence contract

### Required guards

- Backup gate before destructive actions.
- Per-change snapshot before rewrite/move/rename/structural append.
- `obsidian_move_note` dry run before commit.

### Confidence bands

- `>=85`: destructive operations may proceed after snapshot gate passes.
- `68-84`: one non-destructive refinement loop maximum.
- `<68`: no destructive action; proposal/wrapper/review route.

### Protected behavior

- No shell vault mutation for note operations.
- Backups/snapshots and protected watcher paths are excluded from destructive automation.

---

## Observability and outputs

- Queue run emits one line per request in `3-Resources/Watcher-Result.md`.
- Pipelines log into `3-Resources/Ingest-Log.md`, `Organize-Log.md`, `Distill-Log.md`, `Express-Log.md`, `Archive-Log.md`, and `Backup-Log.md`.
- Failures are summarized in `3-Resources/Errors.md` with trace and recovery guidance.

---

## Practical execution pattern

1. Craft or trigger a CODE mode.
2. Dispatch through queue.
3. Execute one pipeline entry fully.
4. Apply safety gates on each destructive boundary.
5. Log result + watcher line.
6. Continue next queue entry.

This keeps CODE runs deterministic, auditable, and recoverable while preserving PARA structure discipline.

---

## Canonical references

- `Docs/Entire-System-Reference.md`
- `Docs/Pipelines/Ingest-Pipeline.md`
- `Docs/Pipelines/Organize-Pipeline.md`
- `Docs/Pipelines/Distill-Pipeline.md`
- `Docs/Pipelines/Express-Pipeline.md`
- `Docs/Pipelines/Archive-Pipeline.md`
- `Docs/Pipelines/Queue-Pipeline.md`
- `Queue-Sources.md`
- `Parameters.md`
