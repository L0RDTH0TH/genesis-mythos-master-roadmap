---
title: Phase 2.1.5 — Replay ledger, canonical diff surface, and restore cursor
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.1.5"
project-id: genesis-mythos-master
status: active
priority: high
progress: 42
handoff_readiness: 77
created: 2026-03-30
tags:
  - roadmap
  - genesis-mythos-master
  - phase-2
para-type: Project
links:
  - "[[Phase-2-1-Pipeline-Stages-Seed-to-World-Roadmap-2026-03-30-2205]]"
  - "[[Phase-2-1-4-Bundle-Identity-Seam-Catalog-Stability-and-Replay-Diff-Roadmap-2026-03-30-2305]]"
---

## Phase 2.1.5 — Replay ledger, canonical diff surface, and restore cursor

This tertiary finalizes the `2.1` slice by adding a stable **replay ledger contract** on top of the `2.1.4` identity and seam-catalog model. The goal is to make replay/debug sessions deterministic and resumable: a run can expose *what changed*, *why it changed*, and *where to resume* after a validation stop, without mutating authoritative world state.

## Scope

**In scope:**
- A conceptual **ReplayLedgerEntry** shape that records bundle identity, seam catalog revision, selected validation labels, and deterministic resume cursor metadata.
- A **canonical diff surface** for tool-facing comparison between two staged bundles (schema-level only; no binary format).
- Rules for **restore cursor** derivation after dry-run failure: where the next replay begins and what previous artifacts remain trusted.

**Out of scope:**
- Persistent storage engine, encryption, or concrete event-stream implementation.
- Execution-track CI closure and runtime observability pipelines.

## Behavior (natural language)

Actors: pipeline runner, validation gate, replay tooling, and operator.

- After Stage 4 validation, the pipeline emits one logical replay-ledger entry for the staged bundle attempt.
- If validation passes, the ledger marks the cursor as `commit-ready` and points to the Stage 5 boundary token.
- If validation fails, the ledger marks the cursor as `restore-required` and includes a deterministic resume pointer to the last trusted seam/apply boundary.
- Diff inspection reads two ledger-linked bundle identities and returns deterministic change classes: seam delta, ordered op delta, label delta, and cursor movement.

## Interfaces

- **ReplayLedgerEntry (NL):** `{ bundleIdentity, seamCatalogRevision, validationLabelSet, resumeCursor, stageWindow, timestampLogical }`
- **ResumeCursor (NL):** `{ resumeFromSeam, resumeFromApplyOrdinal, requiresCatalogMigration }`
- **CanonicalDiffSurface (NL):** `{ seamDelta[], opDelta[], labelDelta[], cursorDelta }`

Upstream:
- Uses `2.1.4` contracts for bundle identity and seam catalog revision.

Downstream:
- Stage 5 commit and execution-track runbooks can consume replay cursor metadata without re-deriving seam/order state.

## Edge cases

- Catalog revision mismatch during restore: cursor is valid only when migration policy explicitly maps old seams to new seams.
- Partial replay over stale labels: restore must reject stale validation labels instead of silently applying.
- Diff noise from ordering-only changes: canonical surface distinguishes harmless canonical reorder from semantic seam/op drift.

## Open questions

- Whether resume cursor should support multi-branch speculative replay in one ledger model or require one cursor per deterministic branch.
- Whether replay-ledger retention policy is global (project-wide) or phase-scope specific on execution track.

## Pseudo-code readiness

```
build_replay_ledger(bundle, validation_result):
  cursor = derive_resume_cursor(bundle, validation_result)
  return ReplayLedgerEntry(bundle.identity, bundle.catalog_rev, validation_result.labels, cursor)

diff_replay(a, b):
  return CanonicalDiffSurface(
    seam_delta(a, b),
    op_delta(a, b),
    label_delta(a, b),
    cursor_delta(a.cursor, b.cursor)
  )
```

## Research integration

> [!note] External grounding
> No `Ingest/Agent-Research/` notes were bound this run; alignment is **pattern-only** from deterministic replay pipelines and failure-resume ledger practice.
