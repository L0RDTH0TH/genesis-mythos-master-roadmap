---
title: Phase 2.2 - Intent resolver and hook mapping
roadmap-level: secondary
phase-number: 2
subphase-index: "2.2"
project-id: sandbox-genesis-mythos-master
status: active
priority: high
progress: 36
handoff_readiness: 80
created: 2026-03-30
tags:
  - roadmap
  - sandbox-genesis-mythos-master
  - phase-2
para-type: Project
links:
  - "[[Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-03-30-0430]]"
---

## Phase 2.2 - Intent resolver and hook mapping

This secondary slice defines how player and DM intent is translated into stable, typed hooks that the pipeline can consume without creating hidden state coupling or nondeterministic behavior.

## Scope

**In scope:**
- Intent ingestion surfaces (player, DM, system overrides) and normalization contracts.
- Resolver ordering and conflict classes (replace, merge, defer, reject).
- Hook namespaces and typed payload envelopes that downstream stages can rely on.
- Replay-safe intent snapshots and deterministic resolver outcomes for the same inputs.

**Out of scope:**
- Engine-specific API bindings and plugin wiring.
- Execution CI/registry closure and benchmark enforcement.
- UX copy for prompts/dialogue surfaces.

## Behavior (natural language)

Inputs enter through a canonical intent envelope that carries actor, target scope, and resolver metadata. The resolver first normalizes shape and identity, then applies priority and conflict rules, and finally emits stable hook payloads for pipeline stages.

Ordering:
- Normalize incoming intent envelopes.
- Validate and classify intent against allowed hook schema.
- Resolve conflicts by explicit priority rules.
- Emit deterministic hook payloads plus rejection/defer diagnostics.
- Persist replay snapshot metadata for restore and audit.

## Interfaces

Upstream:
- Consumes stage-pipeline spine and commit-boundary contracts from Phase 2.1.

Downstream:
- Tertiary notes under 2.2 define intent taxonomy, merge policy envelopes, and replay/error contracts.

Outward guarantees:
- Same seed + same intent set + same resolver config yields same hook outputs.
- Unknown or invalid intents never mutate world state directly; they become diagnostics or explicit deferred items.

## Edge cases

- Conflicting intents targeting the same hook in the same frame.
- Intent payload shape drift across versioned clients.
- Deferred intents that expire before replay.
- Hook namespace collisions between DM and player channels.

## Open questions

- Whether resolver precedence should be static by channel or dynamically policy-driven.
- Whether deferred intents are replayed automatically or require explicit operator approval.

## Pseudo-code readiness

At this depth, pseudo-code is not required. Readers should be able to sketch resolver stages, hook envelope schema boundaries, and deterministic conflict resolution flow without algorithm-level implementation detail.

## Research integration

> [!note] External grounding
> No `Ingest/Agent-Research/` notes were bound this run; alignment is pattern-only from deterministic event-resolution systems.

## Tertiary notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/sandbox-genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building/Phase-2-2-Intent-Resolver-and-Hook-Mapping"
WHERE roadmap-level = "tertiary" OR roadmap-level = "task"
SORT subphase-index ASC, file.name ASC
```
