---
title: Decision Codex Surface Spec
created: 2026-04-08
tags: [decision-codex, spec, roadmap, lore]
source: Decision Tracking Enhancement Plan
---

# Decision codex surface spec

This is a specification-only artifact for a lightweight Decision Codex surface.
No runtime app implementation is included in this pass.

## Goals

- Make decision history queryable for DM operations.
- Provide a filtered, read-only player mirror for player-visible policy changes.
- Keep decision-to-lore propagation deterministic and auditable.

## Surface 1: DM view (authoritative operations)

Required capabilities:

- Full decisions list across relevant project scopes.
- Relationship graph/backlink view between decisions and phase/execution artifacts.
- Filters:
  - Date range
  - Phase / subphase
  - Subsystem (frontend, simulation, persistence, platform)
  - `World Impact` presence/class
  - Status (`active`, `amended`, `superseded`, `deferred`)
- Keyword search (decision id, rationale text, queue id, validator report id).
- "Decisions since last session" preset.

Minimum row fields:

- Decision id
- Date
- Status
- Category
- World Impact summary (or `none`)
- Linkage count
- Last amendment date
- Last validator/queue reference

## Surface 2: Player-facing mirror (read-only)

Scope:

- Include only player-visible decisions (for example, UX behavior, scheduling rules, lore continuity rules).
- Exclude operator-only mechanics (internal safety gates, CI/registry closure mechanics, low-level queue repair internals).

Required behavior:

- Read-only listing with human-readable summaries.
- Linked to lore/journal/event surfaces when available.
- Hide internal ids by default unless explicitly elevated to player-safe metadata.

Suggested fields:

- Decision headline
- What changed for players
- Effective date/session
- Linked lore/journal note

## Lore integration contract (spine hook)

On decision commit (or manual trigger), append a human-readable mirror line under `Meta/Decisions/` through the spine event path.

Required payload for the append event:

- `decision_id`
- `project_id`
- `summary_for_humans`
- `world_impact_summary` (if present)
- `effective_date`
- `source_linkages` (decision note + phase/context link)

Contract notes:

- Append-only (never rewrite prior lore mirror events).
- If commit-time hook is unavailable, allow manual replay trigger using the same payload shape.
- Mark replayed lines with a deterministic idempotency marker to avoid duplicate event spam.

## Data contract expectations

Decision entries feeding this codex should expose:

- Option class (`explicit_options`, `single_option`, `deferred`)
- Rationale presence
- Linkages presence
- World Impact requirement + presence flags

These flags align with queue/harness decision completeness signals for advisory/strict validation.

## Non-goals for this pass

- No UI runtime implementation.
- No search index service implementation.
- No live graph rendering implementation.
- No automatic permission/auth model implementation beyond spec boundaries.
