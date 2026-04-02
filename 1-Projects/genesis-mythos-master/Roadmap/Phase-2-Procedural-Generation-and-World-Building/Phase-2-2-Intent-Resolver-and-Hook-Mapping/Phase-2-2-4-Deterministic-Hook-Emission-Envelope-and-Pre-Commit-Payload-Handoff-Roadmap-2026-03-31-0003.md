---
title: Phase 2.2.4 — Deterministic hook emission envelope and pre-commit payload handoff
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.2.4"
project-id: genesis-mythos-master
status: active
priority: high
progress: 36
handoff_readiness: 80
created: 2026-03-31
tags:
  - roadmap
  - genesis-mythos-master
  - phase-2
para-type: Project
links:
  - "[[Phase-2-2-Intent-Resolver-and-Hook-Mapping-Roadmap-2026-03-30-2310]]"
  - "[[Phase-2-2-3-Conflict-Resolution-Priority-Ordering-and-Merge-Policy-Roadmap-2026-03-31-0002]]"
---

## Phase 2.2.4 — Deterministic hook emission envelope and pre-commit payload handoff

This tertiary defines how the resolver emits final hook payload envelopes after merge-policy outcomes are known, while preserving a strict pre-commit boundary. The output is a deterministic, replay-safe emission bundle that downstream stages can validate before any commit-path side effects.

## Scope

**In scope:**
- Canonical `HookEmissionEnvelope` shape for resolved intents after **2.2.3**.
- Deterministic ordering and envelope identity rules for hook payload emission.
- Pre-commit handoff contract (`PreCommitHookPayloadBundle`) from resolver output to stage consumers.
- Rejection/defer side-channel payloads that preserve rationale without mutating commit-path state.
- Boundary between `resolved` and `commit-ready` states, including explicit validation labels.

**Out of scope:**
- Runtime commit executor implementation details.
- CI/registry closure artifacts and production hardening.
- UX-facing formatting for diagnostics surfaced to users.

## Behavior (natural language)

Ordering:
1. Consume `ResolvedIntentSet` and `ConflictDecisionLog` from **2.2.3**.
2. Project each accepted intent into canonical hook payload fragments.
3. Assemble deterministic `HookEmissionEnvelope` records with stable ids and ordering keys.
4. Build a `PreCommitHookPayloadBundle` that contains:
   - ordered emission envelopes,
   - deferred/rejected diagnostics,
   - validation labels required for pre-commit checks.
5. Hand off the bundle to pre-commit validation stages; no commit-path state mutation occurs in this tertiary.

Determinism contract:
- Same resolved input + same policy/catalog revisions yields identical emission envelopes and ordering.
- Any unresolved/deferred payload remains diagnostic-only and cannot leak into commit-ready payloads.

## Interfaces

Natural-language type sketches:

- **HookEmissionEnvelope:** `{ envelopeId, hookNamespace, hookKey, payload, orderingKey, sourceIntentIds }`
- **PreCommitHookPayloadBundle:** `{ envelopes[], deferredDiagnostics[], rejectedDiagnostics[], validationLabels[] }`
- **EmissionDeterminismMeta:** `{ policyRevision, catalogRevision, orderingHash, frameToken }`

Adjacent slices:
- **[[Phase-2-2-3-Conflict-Resolution-Priority-Ordering-and-Merge-Policy-Roadmap-2026-03-31-0002]]** provides ordered conflict-resolved intents.
- Parent **[[Phase-2-2-Intent-Resolver-and-Hook-Mapping-Roadmap-2026-03-30-2310]]** requires normalize -> classify -> resolve -> emit sequencing with replay guarantees.

## Edge cases

- Multiple winners mapping to same hook namespace with different payload shapes: enforce schema-compatible envelope projection or reject with deterministic code.
- Emission ordering ties after policy resolution: break ties using canonical tuple key (`orderingKey`) only.
- Deferred intent accidentally emitted due to stale cache: enforce deferred gate in bundle assembly.
- Catalog revision drift between resolve and emit: mark bundle invalid for commit path and emit diagnostics-only output.

## Open questions

- **D-2.2.4-validation-label-contract:** Whether validation labels should be coarse (stage-level) or fine-grained per envelope field group.
- **D-2.2.4-bundle-size-policy:** Whether large pre-commit bundles should chunk by namespace before validation or remain single-frame atomic.

## Pseudo-code readiness

At depth 3, this slice specifies deterministic emission and pre-commit handoff boundaries clearly enough for depth-4 implementation planning. Algorithm-level batching/chunking internals remain execution-deferred.

## Research integration

> [!note] External grounding
> No `Ingest/Agent-Research/` notes were bound this run; alignment is pattern-only from deterministic event-emission envelope contracts in staged policy pipelines.
