# Roadmapping System

**Version: 2026-03**

Canonical reference for roadmap automation behavior across setup, resume actions, dual-track operation, and roadmap queue execution.

---

## Purpose

Summarize how roadmap work is executed safely in multi-run mode, including conceptual vs execution tracks, action routing, and state authority.

---

## Entry Modes

- **`ROADMAP MODE`**: setup only (Phase 0/state/bootstrap generation path).
- **`RESUME_ROADMAP`**: one action per run (default action: `deepen`).
- Alias actions normalize to `RESUME_ROADMAP` with `params.action` (for example `RECAL-ROAD`, `SYNC-PHASE-OUTPUTS`, `REVERT-PHASE`).

---

## Single-Action Resume Model

Each resume run performs one branch:

- `deepen`
- `advance-phase`
- `recal`
- `handoff-audit`
- `sync-outputs`
- `revert-phase`
- `resume-from-last-safe`
- `expand`

This keeps state transitions explicit and auditable across many iterations.

---

## State Authority

Roadmap state is owned by project roadmap files:

- `Roadmap/roadmap-state.md`
- `Roadmap/workflow_state.md`

On any conflict between narrative text and machine cursor, treat state frontmatter and latest authoritative cursor fields as canonical.

---

## Dual-Track Model

- **Conceptual track**: design structure and rationale with freeze protections when marked frozen.
- **Execution track**: implementation-facing continuation under `Roadmap/Execution/`.
- Conceptual frozen notes are non-destructive by default; amendments and decision records are created as new companion notes.

Reference: `Docs/Dual-Roadmap-Track.md`.

---

## Roadmap Safety

- Backup and per-change snapshot before destructive/structural writes.
- Confidence gates apply to roadmap decisions and downstream actions.
- Recal and validator passes are used to prevent silent drift.
- Queue follow-ups are appended when configured (`queue_next`) to continue controlled progression.

---

## Queue Relationship

- Roadmap entries are usually crafted through prompt-crafter ROADMAP branch.
- Queue processor resolves action and dispatches to roadmap subagent.
- Each processed queue entry should produce one watcher result line.

---

## Related Docs

- `Pipelines/Roadmap-Pipeline.md`
- `User-Flows/Roadmap-Resume-Flow.md`
- `Docs/Dual-Roadmap-Track.md`
- `Queue-Sources.md`
- `Parameters.md`
