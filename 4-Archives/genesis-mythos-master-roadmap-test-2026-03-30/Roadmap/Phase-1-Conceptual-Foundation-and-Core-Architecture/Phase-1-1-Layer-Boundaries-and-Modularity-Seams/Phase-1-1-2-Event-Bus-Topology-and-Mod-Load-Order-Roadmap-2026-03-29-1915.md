---
title: Phase 1.1.2 — Event bus topology and mod-load order
roadmap-level: tertiary
phase-number: 1
subphase-index: "1.1.2"
project-id: genesis-mythos-master
status: active
priority: high
progress: 12
created: 2026-03-29
tags: [roadmap, genesis-mythos-master, phase]
para-type: Project
links:
  - "[[Phase-1-1-Layer-Boundaries-and-Modularity-Seams-Roadmap-2026-03-29-1731]]"
  - "[[Phase-1-1-Layer-Boundaries-and-Modularity-Seams/Phase-1-1-1-Replaceability-Seams-and-Hook-Surface-Roadmap-2026-03-29-1905]]"
  - "[[Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-03-29-1730]]"
handoff_readiness: 80
handoff_gaps:
  - "Peer secondary **1.2** exists and was deepened (snapshots/dry-run); remaining: execution typing for **bus transports** and **mod sandbox** only"
---

## Phase 1.1.2 — Event bus topology and mod-load order

**Parent slice:** [[Phase-1-1-Layer-Boundaries-and-Modularity-Seams-Roadmap-2026-03-29-1731]]. **Builds on** [[Phase-1-1-Layer-Boundaries-and-Modularity-Seams/Phase-1-1-1-Replaceability-Seams-and-Hook-Surface-Roadmap-2026-03-29-1905]] **S-H** and **S-G** seams: this slice names **how events flow** across layers and **in what order third-party or optional modules** may attach, without picking a concrete message broker or scripting runtime (**D-027**).

### Scope

- **In scope:** Conceptual **topology** (single logical bus vs partitioned topics/domains), **ordering guarantees** visible to game logic, and **mod-load / adapter registration order** relative to validation and simulation startup.
- **Out of scope:** Wire format, IPC, threading model, plugin manifest schema, and sandbox implementation — **execution track**.

### Behavior

1. **Publication paths** — Events emitted from **simulation / authoritative state** and from **generation / staging** are classified into **domains** (e.g. world-facts, presentation-hints, audit). Each domain declares whether consumers may feed back into **intent construction** (rare, audited) or only into **read models** (default).
2. **Topology choices** — **Single logical bus** simplifies tracing but risks cross-talk; **partitioned buses** (by domain) reduce accidental coupling but need explicit **bridge rules** when a workflow spans domains. This roadmap picks **partitioned-by-default** with **documented bridges** only where Phase 1.1 layer diagram allows an edge.
3. **Mod-load order** — **Core contracts** register first (validation policies, stage validators per **S-H3**), then **world observation hooks** (**S-H2**), then **player/operator adapters** (**S-H1**), then **optional mods** that extend seams without bypassing ordering. **Hard rule:** no mod may register a consumer that runs **before** core fail-closed validators for the same lane unless explicitly whitelisted in a later execution decision.
4. **Replay and determinism** — Bus delivery order for the same tick/run must be **stable given the same manifest + intent ordering**; cross-partition ordering is defined by a **global sequencing contract** (e.g. monotonic run log slice) — detailed numbering on execution track.

### Interfaces (conceptual)

| Surface | Producer | Consumer | Guarantee |
| --- | --- | --- | --- |
| **Domain topic** | Stage or sim | Hooks / projections | Typed manifest reference; no anonymous payloads |
| **Bridge** | Two domains | Orchestrator | Explicit bridge id + audit; no silent fan-in |
| **Registration slot** | Mod / adapter | Bus registry (conceptual) | Slot id + relative priority band (core / world / player / extension) |

### Edge cases

- **Circular bridge** (domain A → B → A) — treated like generation graph cycles: **disallowed by default**; if ever allowed, requires hazard doc + termination (defer execution proof).
- **Late-loaded mod** after run start — must not reorder committed authoritative facts; may only attach to **forward** delivery or explicit **reload** boundary (execution).
- **Fat event** carrying both fact and presentation — split into **authoritative fact** vs **derived view** references to preserve **S-L4** (presentation does not author core facts).

### Open questions

- Exact **domain taxonomy** (count and names) — **pattern** acceptable until Phase 2–3 narratives demand more splits.
- Whether **user-generated content** shares the same bus domains as engine mods — **TBD** with trust tiering on execution track.

### Pseudo-code readiness (mid-technical)

```text
function RegisterAdapter(slotBand, adapterId, handler) -> OK | Reject
  // slotBand in { core, world_observation, player_operator, extension }
  // Reject if handler bypasses declared validator ordering for its lane

function PublishEvent(domainId, manifest, payloadRef, sequencingWitness)
  // payloadRef points to typed artifact; sequencingWitness ties to run log
```

Reader can place **hook seams** from 1.1.1 on a **bus topology** without assuming Kafka, NATS, or in-process queues.

### Checklist (handoff-oriented)

- [x] **Partitioned-by-default** topology with **bridge** rules aligned to Phase 1.1 layer edges.
- [x] **Mod-load / registration bands** ordered after core validators.
- [x] **Replay / sequencing** called out at conceptual level.
- [x] **Peer 1.2** secondary — **done:** [[Phase-1-2-Safety-Invariants-Snapshots-and-Dry-Run-Roadmap-2026-03-29-1731]] (2026-03-29 deepen). Execution **transports** remain deferred.

## Related

- [[Phase-1-1-Layer-Boundaries-and-Modularity-Seams-Roadmap-2026-03-29-1731]] — parent secondary.
- [[Phase-1-1-Layer-Boundaries-and-Modularity-Seams/Phase-1-1-1-Replaceability-Seams-and-Hook-Surface-Roadmap-2026-03-29-1905]] — seam IDs **S-H\***, **S-G\***.
- [[decisions-log]] — **D-027** stack-agnostic authority.
