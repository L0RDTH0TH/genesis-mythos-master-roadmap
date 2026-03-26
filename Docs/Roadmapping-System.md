# Roadmapping System

**Version: 2026-03**

Canonical operational reference for roadmap automation: setup, resume actions, state ownership, dual-track behavior, and safe multi-run progression.

---

## Purpose

Document the roadmap lane as a controlled state machine:

- how roadmap runs are entered,
- how actions are selected and applied,
- which files are authoritative state,
- how conceptual/execution tracks coexist,
- and how safety/validation gates prevent drift.

---

## System scope

### In scope

- `ROADMAP MODE` setup behavior.
- `RESUME_ROADMAP` single-action continuation.
- Resume aliases normalized into action params.
- Dual-track conceptual/execution model.
- State artifacts and queue relationship.

### Out of scope

- CODE PARA lane pipeline internals (covered in `CODE-PARA-System.md`).

---

## Entry and action model

### Setup entry

- **`ROADMAP MODE`** is setup/bootstrap only.
- Initializes/ensures roadmap scaffolding and state files.
- Does not become a generic continue loop.

### Resume entry

- **`RESUME_ROADMAP`** performs one action per run.
- Default action is `deepen` if unspecified.
- Alias commands map into `RESUME_ROADMAP` + `params.action`.

### Single-action resume branches

- `deepen`
- `advance-phase`
- `recal`
- `handoff-audit`
- `sync-outputs`
- `revert-phase`
- `resume-from-last-safe`
- `expand`

This one-branch model preserves deterministic state transitions and auditable history.

---

## State authority and artifacts

### Canonical state files

- `Roadmap/roadmap-state.md`
- `Roadmap/workflow_state.md`
- plus supporting `decisions-log.md`, phase notes, and output notes

### Authority rule

- When narrative text disagrees with tracked state, state frontmatter/cursor fields are authoritative.
- State updates are treated as controlled mutations, not casual prose edits.

---

## Dual-track behavior

### Conceptual track

- Architecture/rationale track.
- Frozen conceptual notes are non-destructive by default.
- Changes are routed to companion artifacts (amendments/decision records) unless explicitly unfrozen.

### Execution track

- Implementation-facing continuation under `Roadmap/Execution/`.
- Uses execution-state artifacts for progression when execution track is active.

Reference: `Docs/Dual-Roadmap-Track.md`.

---

## Queue and orchestration relationship

- Roadmap payloads are commonly produced via prompt-crafter ROADMAP branch.
- Queue resolves mode/action and dispatches roadmap subagent execution.
- Resume actions can enqueue controlled follow-ups (for example via `queue_next`) for iterative continuation.
- Each processed roadmap queue request emits a watcher result line for operator visibility.

---

## Safety and drift controls

### Required gates

- Backup and per-change snapshot before destructive/structural roadmap mutations.
- Confidence gates must pass before transition-critical operations.
- Validation/audit branches (`recal`, handoff checks, validator layers) catch drift and structural mismatch.

### Progress integrity

- Phase progression is explicit (`advance-phase`) and gate-bound.
- Resume actions should not silently mutate multiple branches in one run.
- Context and state logging keep post-run diagnosis possible.

---

## Operational run lifecycle

1. Resolve project and roadmap directory.
2. Resolve mode and action (setup or single resume action).
3. Execute only the selected branch.
4. Apply state/safety gates at mutation points.
5. Write logs and watcher line.
6. Optionally append controlled follow-up queue entry.

---

## Canonical references

- `Docs/Entire-System-Reference.md`
- `Docs/Pipelines/Roadmap-Pipeline.md`
- `Docs/User-Flows/Roadmap-Resume-Flow.md`
- `Docs/Dual-Roadmap-Track.md`
- `Queue-Sources.md`
- `Parameters.md`
