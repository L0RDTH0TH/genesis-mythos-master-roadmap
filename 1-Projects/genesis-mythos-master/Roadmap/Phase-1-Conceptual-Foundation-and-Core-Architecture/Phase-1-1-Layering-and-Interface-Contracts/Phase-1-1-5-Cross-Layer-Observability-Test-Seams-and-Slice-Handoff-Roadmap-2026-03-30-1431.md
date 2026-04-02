---
title: Phase 1.1.5 — Cross-layer observability, test seams, and layering slice handoff
roadmap-level: tertiary
phase-number: 1
subphase-index: "1.1.5"
project-id: genesis-mythos-master
status: active
priority: high
progress: 24
handoff_readiness: 75
created: 2026-03-30
tags:
  - roadmap
  - genesis-mythos-master
  - phase-1
para-type: Project
links:
  - "[[Phase-1-1-Layering-and-Interface-Contracts-Roadmap-2026-03-30-0500]]"
---

## Phase 1.1.5 — Cross-layer observability, test seams, and layering slice handoff

This tertiary **closes the Phase 1.1 layering slice** by naming how teams **observe** behavior across boundaries, **inject test doubles** without violating commit rules from [[Phase-1-1-1-Layer-Boundary-and-Commit-Pipeline-Roadmap-2026-03-30-0431]], and what **“slice complete”** means before moving to secondary **1.2** (procedural generation graph skeleton — Phase 1 primary checklist).

## Scope

**In scope:** Per-layer **diagnostic surfaces** (trace correlation IDs, layer-scoped health flags, non-authoritative counters); **boundary test seams** (where simulation may be swapped for a deterministic stub; where render may consume frozen snapshots); **handoff criteria** for declaring the **1.1.x** tertiaries coherent enough for **1.2** design work.

**Out of scope:** Concrete telemetry backends, CI job definitions, performance profilers, or HR/rollup registry artifacts (**execution-deferred**).

## Behavior (natural language)

- **Observability:** Each layer exposes a **minimal contract** for “what happened this tick” — e.g. world state exposes commit epoch + rejected mutation count; simulation exposes step outcome + retry depth; render exposes frame drop reason class; input exposes intent validation summary. Cross-layer traces use a **single correlation id** carried on intents and commits (conceptual only — wire format deferred).
- **Test seams:** Tests target **published seams**: inject **fake world state** behind the commit API; **clock-controlled** simulation; **golden** render inputs; **record/replay** intents at the input boundary. No layer tests reach around a boundary into another layer’s private graph.
- **Slice handoff:** Layering slice is **complete** when tertiaries **1.1.1–1.1.5** each satisfy the NL checklist at or above the conceptual floor; **1.2** may deepen the **generation graph** without revisiting layer identities from **1.1**.

## Interfaces

- **`DiagnosticsSink` (conceptual):** Layer-local registration for structured events; **no** circular dependency — sinks do not call back into simulation during the same tick.
- **`TestHooks` registry (conceptual):** Named hooks only at **documented** boundaries (commit API, intent ingress, render snapshot read).
- **Adjacent slices:** Depends on **1.1.1–1.1.4**; **1.2** consumes **injection points** named at generation vs live-play boundaries from **1.1** secondary.

## Edge cases

- **Headless / batch:** Render diagnostics may be null; authoritative paths still emit commit diagnostics.
- **Stress / soak:** Correlation ids must not exhaust bounded queues — **drop policy** is non-authoritative (execution-deferred).

## Open questions

- Whether **replay** tests require **full** deterministic simulation or **snapshot-only** assertions at boundaries (deferred to execution test plan).
- **Minimum** observability for MVP vs **full** ops story (product + execution).

## Pseudo-code readiness

```
on_tick_end(correlation_id):
  world_state.emit_diagnostics(epoch, correlation_id)
  simulation.emit_diagnostics(step_result, correlation_id)
  render.emit_diagnostics(frame_class, correlation_id)  # may be no-op
  assert no_layer_writes_peer_internals()
```

## Research integration

> [!note] External grounding
> No `Ingest/Agent-Research/` notes were bound this run; alignment is **pattern-only** from layered diagnostics, boundary testing, and slice-complete gating in large modular systems.
