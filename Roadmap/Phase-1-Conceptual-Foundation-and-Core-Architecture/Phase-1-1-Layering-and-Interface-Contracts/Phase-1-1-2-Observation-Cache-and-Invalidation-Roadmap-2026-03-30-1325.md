---
title: Phase 1.1.2 — Observation, cache, and invalidation across layers
roadmap-level: tertiary
phase-number: 1
subphase-index: "1.1.2"
project-id: godot-genesis-mythos-master
status: active
priority: high
progress: 30
handoff_readiness: 78
created: 2026-03-30
tags:
  - roadmap
  - godot-genesis-mythos-master
  - phase-1
para-type: Project
links:
  - "[[Phase-1-1-Layering-and-Interface-Contracts-Roadmap-2026-03-30-0500]]"
---

## Phase 1.1.2 — Observation, cache, and invalidation across layers

This tertiary continues the **1.1 layering slice** by specifying how layers **observe** neighbors without violating authority, what may be **cached** locally for latency, when **invalidation** must run relative to commits, and where **hot-swap** or **tooling** may replace implementations behind stable contracts.

## Scope

**In scope:** Read-only observation paths; cache layers (render, UI, tooling) vs authoritative state; version or epoch tokens for stale detection; invalidation ordering tied to the commit pipeline from [[Phase-1-1-1-Layer-Boundary-and-Commit-Pipeline-Roadmap-2026-03-30-0431]]; explicit seams where modules may be swapped without changing adjacent contracts.

**Out of scope:** Distributed replication, CRDT merge policies, GPU resource eviction, asset streaming manifests. **Execution-deferred:** CI, registry closure, HR rollup artifacts.

## Behavior (natural language)

- **Observation:** Downstream layers consume **snapshots** or **subscription feeds** from upstream; upstream never depends on downstream for correctness. Observation may be **poll** (version check) or **push** (event after commit) — both are allowed if the contract states which one applies per boundary.
- **Cache:** Render and preview paths may keep **derived** caches (meshes, layout, compiled shaders) keyed by `(entity set hash, commit version)`; caches must treat version bumps as **hard invalidation** unless a slice explicitly allows speculative/predictive frames (then labeled non-authoritative).
- **Invalidation:** On successful `world.commit`, increment an **epoch** or **view generation**; all derived caches that incorporate committed state must either rebuild or mark dirty before the next frame that claims authority.
- **Hot-swap:** Simulation backends, render pipelines, or input providers may be replaced at **named injection points** if they honor the same interface contract; swap requires **quiesce** (drain in-flight intents) or **deferred activation** next tick — exact policy is execution-track; here we require a **single swap coordinator** hook.

## Interfaces

- **World state → observers:** `subscribe(interest)` / `read_version()` — returns monotonic version after each commit; observers compare before expensive work.
- **Simulation → world state:** Unchanged from 1.1.1 — staging still ends in `commit`; observation of pre-commit staging is **debug-only** or **explicit opt-in** to avoid split-brain reads.
- **Rendering → caches:** `prepare_frame(view_model, version)` — if `version` lags committed epoch, renderer may show last frame with **stale** flag for tooling, not for authoritative gameplay decisions.
- **Adjacent slices:** Parent secondary [[Phase-1-1-Layering-and-Interface-Contracts-Roadmap-2026-03-30-0500]] owns stack story; [[Phase-1-1-1-Layer-Boundary-and-Commit-Pipeline-Roadmap-2026-03-30-0431]] owns commit ordering; Phase 2 binds **generation** outputs to the same version/epoch semantics at injection stages.

## Edge cases

- **Predictive rendering:** If render extrapolates beyond last commit for feel, **rollback** on mismatch must not apply authoritative mutations — only visual reconciliation.
- **Tooling / editor overlays:** May read wider snapshots than play mode; must not write except through the same commit path as play.
- **Mod hot-reload:** Replacing code behind a contract without restart — requires **interface stable** + swap coordinator; failure rolls back to last good implementation (execution detail).

## Open questions

- Whether **subscription granularity** is per-entity, per-chunk, or per-layer topic (affects scaling; deferred to execution perf budget).
- Coalescing invalidations when many small commits land in one tick — **batch epoch bump** vs fine-grained (policy TBD execution).

## Pseudo-code readiness

Readers can sketch invalidation without a repo:

```
on_commit_success(new_version):
  broadcast_version(new_version)
  for cache in registered_derived_caches:
    if cache.key_space overlaps committed_delta:
      cache.invalidate_or_rebuild()
render.last_authoritative_version = new_version
```

Full scheduler integration and thread barriers belong to **execution** track or depth-4 tasks.

## Research integration

> [!note] External grounding
> No `Ingest/Agent-Research/` notes were bound this run; alignment is **pattern-only** from common game-client cache invalidation and reactive UI patterns. Operator acceptance for **`safety_unknown_gap`**: see **Operator pick logged (2026-03-30)** under `decisions-log.md` → **Conceptual autopilot** (queue_entry_id `resume-gmm-followup-20260330T132500Z`).
