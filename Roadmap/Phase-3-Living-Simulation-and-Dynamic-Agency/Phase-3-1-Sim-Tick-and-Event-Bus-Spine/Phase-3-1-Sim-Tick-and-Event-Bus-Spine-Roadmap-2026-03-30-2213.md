---
title: Phase 3.1 — Sim tick + event bus spine
roadmap-level: secondary
phase-number: 3
subphase-index: "3.1"
project-id: godot-genesis-mythos-master
status: active
priority: high
progress: 52
handoff_readiness: 84
created: 2026-03-30
tags:
  - roadmap
  - godot-genesis-mythos-master
  - phase-3
para-type: Project
links:
  - "[[Phase-3-Living-Simulation-and-Dynamic-Agency-Roadmap-2026-03-30-0430]]"
  - "[[Phase-2-7-3-Shadow-to-Live-Parity-Admission-Ticket-Redemption-and-First-Committed-Tick-Trace-Roadmap-2026-03-30-1800]]"
  - "[[decisions-log]]"
---

> [!note] #handoff-review
> `handoff_readiness: 84` — secondary **3.1** — **sim tick cadence** + **event bus spine** (deterministic ordering, replay-visible **SimEvent** facts, subscriber lanes) + continuity from **2.7.3** **FirstCommittedTickTrace**; `GMM-2.4.5-*` remain **reference-only**. **Tertiary chain 3.1.1–3.1.5 complete:** **[[Phase-3-1-1-Event-Bus-Ordering-and-Pub-Sub-Lanes-Roadmap-2026-03-30-1830|3.1.1]]** + **[[Phase-3-1-2-Tick-Scheduling-Defer-Merge-and-Work-Queue-Policy-Roadmap-2026-04-02-0020|3.1.2]]** + **[[Phase-3-1-3-Sim-Visible-Classification-and-DM-Overwrite-Channel-Mapping-Roadmap-2026-04-02-0035|3.1.3]]** + **[[Phase-3-1-4-Persistence-Checkpoint-Boundaries-Roadmap-2026-04-02-2240|3.1.4]]** + **[[Phase-3-1-5-Agency-Actor-Drivers-and-Intent-Scheduling-Roadmap-2026-04-02-2250|3.1.5]]** (agency / actor drivers + intent scheduling). Next structural cursor **3.2** (mint next Phase 3 secondary).

## Phase 3.1 — Sim tick + event bus spine

This **secondary 3.1** slice is the first structural body under Phase 3 **living simulation**: it names how the **simulation kernel** advances **tick index**, how **work is scheduled** into a tick boundary, and how **sim-visible facts** cross-cut systems through a single **event bus** seam—without re-deriving Phase **2.4** branch semantics or **2.5** audit surfaces. Anchors `GMM-2.4.5-*` remain **reference-only** deferment IDs.

## Scope

**In scope:**

- **Tick monotonicity** — authoritative **tick index** advances in single steps; a tick groups **integrate intents → agency/environment → consequences → persist-eligible checkpoint → emit bus events → observation** per Phase 3 primary ordering (NL only).
- **Event bus spine** — typed **SimEvent** envelope (origin lane, tick id, stable fact id, payload outline) as the cross-cutting seam; **routing** (who may publish, who may subscribe) and **ordering guarantees** (total order per lane vs partial order across lanes) stated at NL.
- **Continuity from Phase 2** — **FirstCommittedTickTrace** from [[Phase-2-7-3-Shadow-to-Live-Parity-Admission-Ticket-Redemption-and-First-Committed-Tick-Trace-Roadmap-2026-03-30-1800]] is the **first committed tick** handoff into **tick ≥ 1** living sim; bus events emitted after that trace remain **replay-visible** in the same lineage story as **2.7.x**.

**Out of scope:**

- Concrete bus API, async executor, or transport (execution-deferred).
- Full persistence schema, netcode, or perf budgets (execution-deferred).
- **Rendering** frame policy (observation-only contract from Phase 3 primary).

## Behavior (natural language)

1. **Tick advance:** The kernel **increments** tick index only after **scheduled work** for the prior tick is **resolved or explicitly deferred** with a named policy (no silent merge of incompatible writes).
2. **Event bus:** Producers **publish** `SimEvent` records to the bus; consumers **receive** ordered streams per **subscription**; **DM overwrite classes** (live vs structural) tag events so downstream layers (Phase 3 primary) can **filter** without parsing world internals.
3. **Integration with 2.7.3:** The **first committed tick trace** remains the **bridge** from commit pipeline to sim; **3.1** does not add new commit semantics—it **consumes** trace identity as **input** to tick `0→1` and subsequent ticks.

## Interfaces

**Upstream (Phase 2):**

- First committed tick / shadow-to-live: [[Phase-2-7-3-Shadow-to-Live-Parity-Admission-Ticket-Redemption-and-First-Committed-Tick-Trace-Roadmap-2026-03-30-1800]].
- Simulation entry bootstrap: [[Phase-2-7-Simulation-Entry-Bootstrap-and-Deterministic-First-Tick-Roadmap-2026-04-01-0115]].

**Parent (Phase 3 primary):**

- [[Phase-3-Living-Simulation-and-Dynamic-Agency-Roadmap-2026-03-30-0430]] — tick-based living simulation + DM overwrite + sim/render decoupling + event bus at primary.

**Downstream (3.1+):**

- **3.1.1** — [[Phase-3-1-1-Event-Bus-Ordering-and-Pub-Sub-Lanes-Roadmap-2026-03-30-1830]] — lane-scoped ordering + pub/sub registration + GWT D–F.
- **3.1.2** — [[Phase-3-1-2-Tick-Scheduling-Defer-Merge-and-Work-Queue-Policy-Roadmap-2026-04-02-0020]] — tick work queue + deferral ledger + merge policy matrix (GWT G–I).
- **3.1.3** — [[Phase-3-1-3-Sim-Visible-Classification-and-DM-Overwrite-Channel-Mapping-Roadmap-2026-04-02-0035]] — sim-visible classification + DM overwrite channel mapping (GWT J–L).
- **3.1.4** — [[Phase-3-1-4-Persistence-Checkpoint-Boundaries-Roadmap-2026-04-02-2240]] — persistence checkpoint boundaries (GWT M–O).
- **3.1.5** — [[Phase-3-1-5-Agency-Actor-Drivers-and-Intent-Scheduling-Roadmap-2026-04-02-2250]] — actor lanes + intent → WorkItem admission + agency SimEvent story (GWT P–R); **3.1** tertiary chain complete.
- **3.2** — [[Phase-3-2-Simulation-Rendering-Decoupling-and-Observation-Channels-Roadmap-2026-04-02-2300]] — simulation / rendering decoupling + observation channels (`handoff_readiness` **82**); **3.2.1+** tertiaries next.

**Outward guarantees:**

- **Replay visibility:** any fact needed for deterministic replay references **tick id** + **event lineage** (NL); crypto hashes deferred.
- **Decoupling:** rendering and narrative layers **subscribe** to bus / observation surfaces; they do not mutate sim core.

## Edge cases

- **Tick stall / backpressure:** kernel may **defer** subsystem work to later ticks; **no silent cross-tick merge** of incompatible writes without explicit merge policy (execution-deferred).
- **Bus overload:** high-volume **SimEvent** streams may require **chunking** or **rollup** policies — execution-deferred; conceptual slice names **overflow** as **failure mode** (stall + operator visibility).
- **Multi-session / preview:** preview runs **must not** publish authoritative bus events that advance persistence without Phase 2 commit boundary semantics (read-only observation path).

## Open questions

- **Default subscription granularity** for forge vs DM vs operator tools (single lane vs per-faction cohort) — **execution-deferred** until agency slice.
- Whether **weather** events share the same bus **lane** as **faction** events or **separate namespaces** — tertiary decision.

## Pseudo-code readiness

At **secondary** conceptual depth, **no pseudo-code** is required; interfaces are NL contracts referencing Phase 2 handoff notes and Phase 3 primary. **Algorithm sketches** for **ordering** and **publish/subscribe** may appear in **3.1.1+** tertiaries.

## Risk register v0 (slice 3.1)

| Risk | Mitigation | Decision locus / deferral |
| --- | --- | --- |
| **Tick stall / backpressure** | Defer subsystem work to later ticks with explicit policy; no silent merge of incompatible writes | Tertiary **3.1.1+** (scheduling + merge policy NL) |
| **Bus overload / event flood** | Chunking or rollup failure mode; operator-visible stall (not silent drop) | Execution formats deferred; ordering namespaces in **3.1.1+** |
| **Preview vs authoritative publish** | Preview runs read-only; no persistence advance without Phase 2 commit boundary | [[Phase-2-7-3-Shadow-to-Live-Parity-Admission-Ticket-Redemption-and-First-Committed-Tick-Trace-Roadmap-2026-03-30-1800]], Phase 3 primary **Edge cases** |

## Testable acceptance surface (secondary, prose)

| # | Given | When | Then |
| --- | --- | --- | --- |
| A | A **tick index** `T` and scheduled work for `T` | The kernel closes tick `T` | Tick index advances to `T+1` monotonically; no duplicate authoritative `T` closure |
| B | A **FirstCommittedTickTrace** from **2.7.3** and tick `T ≥ 1` | Simulation runs | Bus-emitted **SimEvent** facts remain **replay-visible** with tick + lineage references (NL) |
| C | Producers publish **SimEvent** to the bus | Subscribers consume per subscription | Ordering guarantees stated per lane hold; DM overwrite class tags preserved on events |

## Research integration

> [!note] External grounding
> No `Ingest/Agent-Research/` notes bound this mint; continuity is from **2.7.3** first committed tick trace + Phase 3 primary checklist ([[Phase-3-Living-Simulation-and-Dynamic-Agency-Roadmap-2026-03-30-0430]]).

## Tertiary notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/godot-genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-1-Sim-Tick-and-Event-Bus-Spine"
WHERE roadmap-level = "primary" OR roadmap-level = "secondary" OR roadmap-level = "tertiary" OR roadmap-level = "task"
SORT subphase-index ASC, file.name ASC
```
