---
title: Phase 2.2.1 — Intent envelope normalization and identity binding
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.2.1"
project-id: genesis-mythos-master
status: active
priority: high
progress: 30
handoff_readiness: 77
created: 2026-03-30
tags:
  - roadmap
  - genesis-mythos-master
  - phase-2
para-type: Project
links:
  - "[[Phase-2-2-Intent-Resolver-and-Hook-Mapping-Roadmap-2026-03-30-2310]]"
---

## Phase 2.2.1 — Intent envelope normalization and identity binding

This tertiary pins the **first concrete resolver stage**: turn heterogeneous player/DM/system inputs into a **canonical intent envelope** with stable **identity binding**, so later classification and conflict resolution operate on comparable objects.

## Scope

**In scope:**
- Canonical intent envelope shape (required fields, optional blocks, version tag).
- Actor identity binding (player vs DM vs system; stable actor keys across sessions when contract says so).
- Channel and frame identity (which pipeline frame / regen cycle the intent belongs to).
- Normalization rules for duplicate or near-duplicate submissions (idempotency keys, dedupe windows).

**Out of scope:**
- Full hook taxonomy and merge policy envelopes (later **2.2.x** tertiaries).
- Engine-specific serialization and network transport.
- Execution-track CI, registry closure, or cryptographic proof of intent origin.

## Behavior (natural language)

Ordering (within this slice):
1. **Ingest** raw intent records from allowed surfaces (UI, API adapter stubs, system overrides) into a single **normalization queue** per frame.
2. **Normalize** each record to the canonical envelope: fill defaults, coerce enums, attach resolver metadata (source priority hint only — not final precedence).
3. **Bind identity**: assign stable **IntentRecordId** (logical key) and **ActorBinding** (who is speaking; optional party/role when DM tools are involved).
4. **Dedupe / fold**: within a configurable window, merge or reject duplicates per `IntentRecordId` + target scope per normalization policy.
5. **Emit** normalized envelopes to the **validation/classify** stage (next resolver step — **2.2.2**), never skipping validation on “fast paths.”

Determinism contract:
- Same raw intent bytes + same normalization config + same frame identity ⇒ same normalized envelope set (including ordering rules for ties).

## Interfaces

Natural-language type sketches (not APIs):

- **RawIntentRecord:** `{ surface, payload, optionalActorHint, clientVersion }`
- **CanonicalIntentEnvelope:** `{ intentRecordId, actorBinding, channelId, frameId, targetScope, payloadNormalized, normalizationRevision }`
- **NormalizationPolicy:** `{ dedupeWindow, idempotencyRules, defaultActorResolution }`

Adjacent slices:
- Parent **[[Phase-2-2-Intent-Resolver-and-Hook-Mapping-Roadmap-2026-03-30-2310]]** defines resolver spine and hook mapping intent; this tertiary makes **normalization + identity** explicit so **classify → resolve → emit** stages do not smuggle hidden state.

## Edge cases

- Missing actor hint: resolve via policy default or reject as invalid (no silent guess that changes replay outcomes).
- Client version skew: normalization revision tags incompatible payloads for explicit defer/reject paths.
- Duplicate intents in the same frame with conflicting payloads: last-writer vs merge — must be policy-defined, not ad hoc in stage code.

## Open questions

- **D-2.2.1-intent-id-scope:** Whether `IntentRecordId` is purely logical or also tied to a stable cryptographic identity in execution — tracked under [[decisions-log]] (**D-2.2.1-intent-id-scope**); execution-deferred.
- **D-2.2.1-dedupe-window:** How wide the dedupe window is for collaborative edits (session vs frame vs wall-clock) — tracked under [[decisions-log]] (**D-2.2.1-dedupe-window**); execution-deferred.

## Pseudo-code readiness

At depth 3, mid-technical: interfaces + ordering + determinism contract; algorithm-level pseudocode optional. No depth-4 pseudo-code required for conceptual completion of this slice.

## Research integration

> [!note] External grounding
> No `Ingest/Agent-Research/` notes were bound this run; alignment is pattern-only from deterministic normalization + identity-binding patterns. **Operator pick (pattern-only accepted):** see [[decisions-log]] operator pick for queue_entry_id `resume-deepen-a1b-bootstrap-20260330T233800Z-gmm` (closes `safety_unknown_gap` for this slice alongside D-rows).
