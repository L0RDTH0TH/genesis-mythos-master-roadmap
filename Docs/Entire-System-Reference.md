# Entire System Reference

**Version: 2026-03**

Canonical documentation of the full Second Brain system as operated in this vault: entry funnels, queue orchestration, CODE PARA pipelines, roadmapping pipelines, safety contracts, and observability.

---

## System scope

This reference covers:

- Trigger routing and instruction funnels.
- Prompt-crafter and queue contracts.
- CODE PARA execution model (ingest, organize, distill, express, archive).
- Roadmapping execution model (setup, resume, dual-track, state authority).
- Shared safety and recovery invariants.
- Logs, watcher signaling, and run telemetry.

---

## Entry funnels and orchestration

### Primary entry (preferred)

- **Question-led prompt crafting**: "We are making a prompt", "We are making a CODE prompt", "We are making a ROADMAP prompt".
- Q&A builds one validated payload (`mode` + optional `params`) and appends exactly one queue line only after confirmation.

### Secondary entry (manual/advanced)

- Direct mode phrases (`INGEST MODE`, `DISTILL MODE`, `ROADMAP MODE`, `RESUME_ROADMAP`, `EAT-QUEUE`, etc.) route through system funnels without prompt-crafter Q&A.
- Manual triggers still enforce the same safety contract.

### Queue orchestration chain

- `EAT-QUEUE` / `PROCESS TASK QUEUE` are routed to the queue/dispatcher layer.
- Queue processing applies Step 0 (wrapper handling), parses and validates entries, normalizes aliases, dispatches per mode, logs one watcher line per entry, then rewrites queue contents.
- Pipeline execution is delegated to the matching subagent contract for that mode.

---

## Core data planes

### Vault structure

- PARA roots: `1-Projects`, `2-Areas`, `3-Resources`, `4-Archives`.
- Intake root: `Ingest`.
- Attachments: `5-Attachments`.
- Queue files: `.technical/prompt-queue.jsonl` and `3-Resources/Task-Queue.md`.
- Safety history: `Backups/Per-Change`, `Backups/Batch`, plus external `BACKUP_DIR`.

### Roadmap state artifacts

- Per project under `1-Projects/<project_id>/Roadmap/`:
  - `roadmap-state.md`
  - `workflow_state.md`
  - `decisions-log.md`
  - derived phase and output notes

---

## CODE PARA execution model

### Pipeline family

- `INGEST MODE` -> classify and prepare new content from `Ingest/`.
- `ORGANIZE MODE` -> reclassify and relocate existing PARA notes.
- `DISTILL MODE` -> progressive refinement and readability shaping.
- `EXPRESS MODE` -> related context and publishable framing.
- `ARCHIVE MODE` -> archive-ready notes to `4-Archives/`.

### CODE run lifecycle

1. Input enters from prompt-crafter queue line or manual trigger.
2. Queue dispatch resolves mode and merged params.
3. Pipeline executes with confidence gates and snapshot/backup guards.
4. Result is logged to pipeline logs + watcher line.
5. Queue line is cleared on success or retained/marked on failure.

### Confidence behavior

- `>=85`: destructive changes allowed only after required snapshot.
- `68-84`: single non-destructive refinement loop.
- `<68`: no destructive change; proposal/wrapper path.

---

## Roadmapping execution model

### Setup vs resume split

- **`ROADMAP MODE`**: setup/bootstrap only.
- **`RESUME_ROADMAP`**: one action per run (default `deepen`).

### Resume action family

- `deepen`, `advance-phase`, `recal`, `handoff-audit`, `sync-outputs`, `revert-phase`, `resume-from-last-safe`, `expand`.
- Alias commands normalize into `RESUME_ROADMAP` + `params.action`.

### Dual-track rules

- Conceptual and execution tracks are distinct when dual-track is active.
- Frozen conceptual notes are non-destructive; amendments and decision records are create-only companion notes unless explicitly unfrozen.

### Roadmap state authority

- `roadmap-state.md` and `workflow_state.md` are canonical state, not narrative prose.
- State mutations are explicit, logged, and guarded by snapshot + confidence requirements.

---

## Shared safety contract

- Backups required before destructive mutations.
- Per-change snapshot required before move/rename/rewrite/structural operations.
- `obsidian_move_note` requires dry run before commit.
- No shell-based vault mutation (`cp`, `mv`, `rm`) for note operations.
- Protected paths (Backups, watcher files, protected notes) are excluded from destructive automation.

---

## Observability and recovery

### Runtime outputs

- Watcher output line per processed request in `3-Resources/Watcher-Result.md`.
- Pipeline logs in `3-Resources/*-Log.md`.
- Errors in `3-Resources/Errors.md` with trace and recovery guidance.
- Optional run telemetry artifacts under `.technical/Run-Telemetry/`.

### Recovery posture

- Decision wrappers are primary human approval gates for uncertain outcomes.
- Restore is user-triggered from snapshots/backups, not automatic rollback.

---

## Canonical references

- `Docs/CODE-PARA-System.md`
- `Docs/Roadmapping-System.md`
- `Queue-Sources.md`
- `Parameters.md`
- `Cursor-Skill-Pipelines-Reference.md`
- `Docs/Pipelines/Queue-Pipeline.md`
- `Docs/Pipelines/Ingest-Pipeline.md`
- `Docs/Pipelines/Roadmap-Pipeline.md`
- `Docs/Operations/Backup-and-Restore.md`
- `Docs/Operations/Errors-and-Recovery.md`
