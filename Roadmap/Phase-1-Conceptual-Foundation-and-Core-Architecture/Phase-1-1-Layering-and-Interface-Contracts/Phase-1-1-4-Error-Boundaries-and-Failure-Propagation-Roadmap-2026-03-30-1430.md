---
title: Phase 1.1.4 — Error boundaries, failure propagation, and recovery contracts
roadmap-level: tertiary
phase-number: 1
subphase-index: "1.1.4"
project-id: sandbox-genesis-mythos-master
status: active
priority: high
progress: 26
handoff_readiness: 76
created: 2026-03-30
tags:
  - roadmap
  - sandbox-genesis-mythos-master
  - phase-1
para-type: Project
links:
  - "[[Phase-1-1-Layering-and-Interface-Contracts-Roadmap-2026-03-30-0500]]"
---

## Phase 1.1.4 — Error boundaries, failure propagation, and recovery contracts

This tertiary closes the **reliability / cross-cutting contract** portion of the **1.1 layering slice**: how failures are **classified**, **bounded** so they do not corrupt authoritative layers, and how **recovery** composes with the commit pipeline ([[Phase-1-1-1-Layer-Boundary-and-Commit-Pipeline-Roadmap-2026-03-30-0431]]), observation/cache invalidation ([[Phase-1-1-2-Observation-Cache-and-Invalidation-Roadmap-2026-03-30-1325]]), and dependency/lifecycle rules ([[Phase-1-1-3-Dependency-Direction-and-Lifecycle-Roadmap-2026-03-30-1420]]).

## Scope

**In scope:** Per-layer **error surfaces** (what each layer may surface as failure vs internal retry); **propagation rules** across layer boundaries (when a failure becomes a hard stop vs degraded mode); **invariants** that must hold after a failure (no partial world state commits; no orphaned observers); **recovery hooks** (retry, rollback to last committed snapshot, or quiesce + swap) aligned with lifecycle from 1.1.3.

**Out of scope:** Concrete exception types, stack traces, crash reporting SDKs, telemetry backends. **Execution-deferred:** CI failure policies, HR/rollup closure artifacts.

## Behavior (natural language)

- **Classification:** Failures are tagged **authoritative** (world state / commit path), **transient** (simulation step may retry), **presentational** (render may drop frames), or **tooling** (editor may cancel without affecting play state).
- **Boundaries:** A lower layer failure **must not** be “fixed” by a higher layer writing back into world state except through the **single commit API** from 1.1.1. Rendering and tools **surface** errors to the user but **route** fixes through intents → simulation → commit.
- **Propagation:** Simulation failures that would leave world state inconsistent **abort the commit** for that tick; observation caches from 1.1.2 invalidate on any **epoch/version** bump from failed-then-retried paths.
- **Recovery:** **Soft recovery** — retry bounded steps; **hard recovery** — reload last consistent snapshot (PMG safety invariant); **swap recovery** — coordinate with swap coordinator so teardown order from 1.1.3 still holds.

## Interfaces

- **`Result<T, Failure>`-shaped contracts** at layer boundaries (conceptual): simulation returns structured failure that world state committer interprets; render receives **read-only** failure summaries for UI.
- **Failure subscription:** Observers may register for **non-fatal** failure channels (e.g. asset missing) without subscribing to **fatal** authoritative corruption signals (those trigger global quiesce).
- **Adjacent slices:** Depends on 1.1.1–1.1.3; Phase 2+ bind concrete graph nodes to these failure classes.

## Edge cases

- **Cascading failures:** Multiple layers fail in one tick — **single root cause** wins; others logged as secondary; commit aborted once.
- **Headless / batch:** Presentational failures suppressed; authoritative failures still block commits.
- **Preview / tool paths:** Non-authoritative failures must not bump epoch or invalidate caches as if a real commit occurred.

## Open questions

- Whether **user-visible** failure taxonomy is a single enum or per-layer vocab with mapping (deferred to UX + execution).
- **Crash-only** detection vs **detectable logical** inconsistency (execution observability).

## Pseudo-code readiness

```
on_layer_failure(layer, failure):
  if failure.severity == authoritative:
    committer.abort_pending()
    world_state.assert_consistent_or_reload_snapshot()
  elif failure.severity == transient:
    sim.schedule_retry(bounded=3)
  notify_observers(failure.summary_non_authoritative())
```

## Research integration

> [!note] External grounding
> No `Ingest/Agent-Research/` notes were bound this run; alignment is **pattern-only** from layered error-handling and fail-safe commit practice in engines and editors.
