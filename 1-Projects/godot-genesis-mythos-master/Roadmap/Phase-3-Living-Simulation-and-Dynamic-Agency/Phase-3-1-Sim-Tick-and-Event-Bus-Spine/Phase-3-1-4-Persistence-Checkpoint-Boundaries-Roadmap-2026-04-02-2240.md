---
title: Phase 3.1.4 — Persistence checkpoint boundaries
roadmap-level: tertiary
phase-number: 3
subphase-index: "3.1.4"
project-id: godot-genesis-mythos-master
status: active
priority: high
progress: 44
progress_note: slice-local depth estimate vs siblings 3.1.1–3.1.3 (not Phase 3 rollup %)
handoff_readiness: 85
created: 2026-04-02
tags:
  - roadmap
  - godot-genesis-mythos-master
  - phase-3
para-type: Project
links:
  - "[[Phase-3-1-Sim-Tick-and-Event-Bus-Spine-Roadmap-2026-03-30-2213]]"
  - "[[Phase-3-1-3-Sim-Visible-Classification-and-DM-Overwrite-Channel-Mapping-Roadmap-2026-04-02-0035]]"
  - "[[Phase-3-1-2-Tick-Scheduling-Defer-Merge-and-Work-Queue-Policy-Roadmap-2026-04-02-0020]]"
  - "[[Phase-3-Living-Simulation-and-Dynamic-Agency-Roadmap-2026-03-30-0430]]"
  - "[[decisions-log]]"
---

> [!note] #handoff-review
> `handoff_readiness: 85` — tertiary **3.1.4** — **persistence checkpoint boundaries** tie **tick closure** from **3.1.2** to **durable sim state** records without re-deriving Phase **2.4** commit envelopes; **bus-visible** facts (**3.1.1**) and **sim-visible classification** (**3.1.3**) remain ordered **before** checkpoint emission; `GMM-2.4.5-*` remain **reference-only**. Next structural cursor **3.1.5** (agency / actor drivers under **3.1**).

## Phase 3.1.4 — Persistence checkpoint boundaries

This **tertiary** defines **when** a persistence **checkpoint** is allowed relative to **tick `T` closure**, **merge outcomes**, and **SimEvent** publication—so **replay** and **cold-start** stories stay coherent with **2.7.3** **FirstCommittedTickTrace** and **2.4.5** audit-handoff semantics at NL depth only.

## Scope

**In scope:**

- **Checkpoint record (NL):** a logical **PersistenceCheckpoint** descriptor bound to **`tick_id`**, **merge closure token** from **3.1.2** (tick `T` resolved/deferred matrix), and **authoritative vs preview** lane per **3.1.3** classifications.
- **Ordering contract:** no **PersistenceCheckpoint** for tick `T` may be emitted **before** (a) tick `T` **closure** per **3.1.2** and (b) **bus-visible** **SimEvent** ordering commitments per **3.1.1** for facts that must precede durability (NL ordering story).
- **DM overwrite classes:** **live tweak** checkpoints may **cohabit** a tick with compatible merges; **structural regen** checkpoints **must** follow **escalation / defer** outcomes from **3.1.2**/**3.1.3** (no silent durability of incompatible merges).

**Out of scope:**

- Storage engine, fsync policy, WAL segments, binary snapshot formats (**execution-deferred**).
- Net replication and multi-writer CRDTs (**execution-deferred**).

## Behavior (natural language)

1. **After merge closure:** When **3.1.2** declares tick `T` **closed** (no incompatible **WorkItem** remains without explicit defer), the kernel may emit **one** primary **PersistenceCheckpoint** for **`world_state`** authority (logical identity only).
2. **Classification gates:** **3.1.3** **`preview_shadow`** / **`replay_only`** streams **must not** produce **PersistenceCheckpoint** rows that advance **authoritative** durability; they may emit **observation-only** checkpoint markers for tooling (**execution format deferred**).
3. **Trace continuity:** **FirstCommittedTickTrace** remains the **first** authoritative durability handoff from Phase 2; **3.1.4** checkpoints for `T≥1` reference **tick lineage** + **checkpoint sequence** (NL) without re-opening **2.4** branch tables.

## Interfaces

**Upstream:**

- **3.1.2:** [[Phase-3-1-2-Tick-Scheduling-Defer-Merge-and-Work-Queue-Policy-Roadmap-2026-04-02-0020]] — tick closure + merge matrix is the **gate** before checkpoint.
- **3.1.3:** [[Phase-3-1-3-Sim-Visible-Classification-and-DM-Overwrite-Channel-Mapping-Roadmap-2026-04-02-0035]] — classification filters what may become **durable** vs **observation-only**.
- **3.1.1:** [[Phase-3-1-1-Event-Bus-Ordering-and-Pub-Sub-Lanes-Roadmap-2026-03-30-1830]] — bus ordering precedes checkpoint when events are part of durability story.

**Phase 2 handoff:**

- **2.7.3:** [[Phase-2-7-3-Shadow-to-Live-Parity-Admission-Ticket-Redemption-and-First-Committed-Tick-Trace-Roadmap-2026-03-30-1800]] — first committed tick trace.
- **2.4.5:** [[Phase-2-4-5-Commit-Decision-Finalization-Replay-Safety-and-Audit-Handoff-Roadmap-2026-03-31-0345]] — finalization / replay-safety **reference-only** authority links (`GMM-2.4.5-*`).

**Downstream:**

- **3.1.5+** — agency / actor drivers and scheduling of intent into ticks (named in **3.1** Interfaces).

**Outward guarantees:**

- **Monotonic durability:** checkpoint sequence never **rewrites** prior tick authority without explicit **recal/repair** class event (NL).
- **Replay hook:** each checkpoint cites **tick id** + **event lineage slice** sufficient for replay narrative (NL).

## Edge cases

- **Tick stall with partial durability:** if closure **defers** critical merges, checkpoint may be **deferred** to `T+k` with operator-visible **stall** (extends **3.1** backpressure story).
- **Conflicting checkpoint requests:** two subsystems request durability for **incompatible** world views — **3.1.2** **block** path prevents checkpoint emission.
- **Forge / operator exports:** read-only exports may snapshot **observation checkpoint markers** without advancing authoritative sequence.

## Open questions

- **Checkpoint granularity:** per-tick single blob vs **sharded** domain checkpoints — **execution-deferred**; this note requires **at least** one logical checkpoint per closed tick for **authoritative** lane.
- **Cross-session restore:** minimum **cold-start** bundle vs full world — ties to **2.6.3** replay anchor (**execution-deferred** binding).

## Pseudo-code readiness

**Mid-technical (depth 3):** sketches only.

### Emit checkpoint (post-close)

```
on_tick_closed(T, merge_matrix_outcome):
  assert merge_matrix_outcome != INCOMPATIBLE_UNRESOLVED
  assert bus_ordering_published_for(T)  # 3.1.1 contract subset
  emit PersistenceCheckpoint(tick_id=T, authority_lane=authoritative_tick)
```

### Preview / shadow path

```
on_preview_publish(class == preview_shadow):
  assert no_authoritative_PersistenceCheckpoint_for(T)
  may_emit ObservationCheckpointMarker(non_authoritative=True)
```

## Risk register (delta vs 3.1.3)

| Risk | Mitigation | Decision locus |
| --- | --- | --- |
| **Durability before bus order** | Ordering gate + explicit bus publish subset | This note + **3.1.1** |
| **Preview promoted to durable** | Classification + checkpoint guard | This note + **3.1.3** |

## Testable acceptance (GWT) — tertiary

Extends **3.1** A–C, **3.1.1** D–F, **3.1.2** G–I, **3.1.3** J–L.

| # | Given | When | Then |
| --- | --- | --- | --- |
| M | Tick `T` **closed** per **3.1.2** with **compatible** merges | Persistence path runs | **PersistenceCheckpoint** exists with **`tick_id=T`** and **merge closure** reference (NL) |
| N | **SimEvent** ordering commitments required for durability | Before checkpoint | **Bus ordering** story from **3.1.1** satisfied for those facts |
| O | **preview_shadow** classification on publish path | Checkpoint phase | **No authoritative** world checkpoint for `T` from preview lane |

## Research integration

> [!note] External grounding
> No new `Ingest/Agent-Research/` notes; continuity from **3.1.1–3.1.3** + Phase 2 **2.7.3** / **2.4.5** reference links.

## Related

- Parent: [[Phase-3-1-Sim-Tick-and-Event-Bus-Spine-Roadmap-2026-03-30-2213]]
- Prior tertiaries: [[Phase-3-1-1-Event-Bus-Ordering-and-Pub-Sub-Lanes-Roadmap-2026-03-30-1830]], [[Phase-3-1-2-Tick-Scheduling-Defer-Merge-and-Work-Queue-Policy-Roadmap-2026-04-02-0020]], [[Phase-3-1-3-Sim-Visible-Classification-and-DM-Overwrite-Channel-Mapping-Roadmap-2026-04-02-0035]]
