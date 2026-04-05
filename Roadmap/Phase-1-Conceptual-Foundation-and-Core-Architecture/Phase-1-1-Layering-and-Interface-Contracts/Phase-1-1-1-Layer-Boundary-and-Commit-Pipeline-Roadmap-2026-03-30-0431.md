---
title: Phase 1.1.1 — Layer boundary and commit pipeline
roadmap-level: tertiary
phase-number: 1
subphase-index: "1.1.1"
project-id: godot-genesis-mythos-master
status: active
priority: high
progress: 35
handoff_readiness: 79
created: 2026-03-30
tags:
  - roadmap
  - godot-genesis-mythos-master
  - phase-1
para-type: Project
links:
  - "[[Phase-1-1-Layering-and-Interface-Contracts-Roadmap-2026-03-30-0500]]"
---

## Phase 1.1.1 — Layer boundary and commit pipeline

This tertiary slice tightens **how mutations cross layer boundaries** and what **commit** means between simulation and world state, so implementers can sketch transaction-shaped APIs without picking a storage engine.

## Scope

**In scope:** Ordering of staged changes within one tick; single-committer semantics for world state; what simulation may hold ephemerally vs what must be persisted; render’s read-only contract; where **validation** runs before commit (simulation-side vs world-state gate).

**Out of scope:** Database schemas, networking, threading, GPU resource lifetime, plugin load order. **Execution-deferred:** CI, HR/registry rollup, and registry closure artifacts.

## Behavior (natural language)

- **Tick slice:** For one logical tick: (1) input intents are collected and timestamped; (2) simulation evaluates rules and produces a **staged delta** (or list of mutation requests); (3) world state **commits** the delta through one API, rejecting illegal transitions as a batch; (4) rendering samples **post-commit** view data only.
- **Single committer:** Only the world-state subsystem applies authoritative mutations; simulation never writes entity fields directly—only requests.
- **Ephemeral simulation state:** Scratch buffers for pathfinding, prediction, or UI previews may exist but must not become authoritative without passing through commit.
- **Render cadence:** Render may run faster than simulation; it interpolates or extrapolates **from last committed snapshot** plus optional non-authoritative prediction flags (clearly labeled).

## Interfaces

- **Simulation → world state:** `StageDelta` / `RequestMutations(delta: WorldDeltaPreview)` → `CommitResult` (accepted | rejected-with-reason). World state exposes **read** for queries during staging but **commit** is the only write path.
- **World state → render:** `ReadViewModel(filter: ViewInterest)` returns immutable snapshot or copy-on-write view; version token increments on each commit so render can detect staleness.
- **Input → simulation:** Intents are **validated for shape** at ingress; semantic validation may be deferred to simulation but **authorization** (DM override vs player) is explicit on the intent object.
- **Adjacent slices:** Parent secondary [[Phase-1-1-Layering-and-Interface-Contracts-Roadmap-2026-03-30-0500]] owns the four-layer story; this note **narrows** to commit ordering. Phase 2 will bind **generation outputs** to the same commit path via injection stages.

## Edge cases

- **Partial commit failure:** If any mutation in a batch violates invariants, **reject entire batch** (default) or use explicitly documented **savepoint** semantics—here we assume **atomic batch** for conceptual clarity.
- **Destructive regen:** Large replacements still require **snapshot + dry-run** before commit (PMG invariant); this note references the hook only.
- **Deterministic replay:** If replay must be intent-only, simulation must not rely on hidden world-state side channels when reproducing a tick—flag as **open** below.

## Open questions

- Whether **soft validation** (warnings) may commit while **hard validation** blocks—default: hard blocks only unless DM policy allows soft commits for lore-only fields.
- Minimum **versioning** for mod layers observing commits (event stream vs poll)—deferred to execution plugin spec.

## Pseudo-code readiness

Readers can sketch **algorithm-shaped** steps without a repo:

```
on_tick(intents):
  staged = simulation.step(intents, world.read())
  result = world.commit(staged, validate=hard)
  if result.ok:
    render.signal_new_version(result.version)
  else:
    simulation.rollback_ephemeral()
    notify_conflict(result.reason)
```

Full API signatures, error enums, and persistence belong to **execution** tertiaries or depth-4 tasks.

## Research integration

> [!note] External grounding
> No `Ingest/Agent-Research/` notes were bound this run; alignment is **pattern-only** from transactional world-state and ECS-style commit patterns in game architecture literature.
