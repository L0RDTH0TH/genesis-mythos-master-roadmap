---
title: Phase 3.1.1 — Event bus ordering + pub/sub lanes
roadmap-level: tertiary
phase-number: 3
subphase-index: "3.1.1"
project-id: godot-genesis-mythos-master
status: active
priority: high
progress: 48
handoff_readiness: 85
created: 2026-03-30
tags:
  - roadmap
  - godot-genesis-mythos-master
  - phase-3
para-type: Project
links:
  - "[[Phase-3-1-Sim-Tick-and-Event-Bus-Spine-Roadmap-2026-03-30-2213]]"
  - "[[Phase-3-Living-Simulation-and-Dynamic-Agency-Roadmap-2026-03-30-0430]]"
  - "[[decisions-log]]"
---

> [!note] #handoff-review
> `handoff_readiness: 85` — tertiary **3.1.1** — **lane-scoped ordering** + **pub/sub registration** NL sketches + **GWT** rows aligned to secondary **3.1** risk register / acceptance surface; `GMM-2.4.5-*` remain **reference-only**. **3.1.2** minted — [[Phase-3-1-2-Tick-Scheduling-Defer-Merge-and-Work-Queue-Policy-Roadmap-2026-04-02-0020]]. Next structural cursor **3.1.3** (DM overwrite channel mapping / sim-visible classification).

## Phase 3.1.1 — Event bus ordering and pub/sub lanes

This **tertiary** tightens **secondary 3.1**’s bus spine: it names **how `SimEvent` streams are ordered** for replay, how **subscriptions** bind to **lanes / namespaces**, and how **publishers** remain **deterministic under conflict**—without specifying APIs, transports, or executor models (execution-deferred).

## Scope

**In scope:**

- **Ordering model (NL + sketches):** per-**lane** total order vs **cross-lane** partial order; **tie-break** keys when two events share tick + lane (e.g. stable publisher id, monotonic sequence within publisher).
- **Pub/sub sketch:** registration records (who subscribes to which **lane + topic key**), **delivery** as ordered iterator per subscription, and **visibility rules** for preview vs authoritative publishers (extends **3.1** edge case).
- **DM overwrite class on events:** preserved on ordered delivery so filters downstream do not parse world internals (carries **3.1** Behavior).

**Out of scope:**

- Concrete topic graph, async delivery, back-pressure implementation (execution-deferred).
- Persistence of bus cursor / consumer offsets (execution-deferred; named as **failure mode** only).

## Behavior (natural language)

1. **Lane-scoped ordering:** For each **lane** `L`, the bus exposes a **total order** over `SimEvent` records emitted in tick `T` that share `L`. Cross-lane, order is **not** guaranteed unless an explicit **cross-lane barrier** contract is invoked (execution-deferred format).
2. **Pub/sub:** Subscribers **register** `(lane, subscription_key)` pairs; the kernel **materializes** an ordered stream per registration by **merging** only events matching that registration, **preserving** within-lane order. Unmatched events are ignored by that subscription without affecting other subscribers’ orders.
3. **Preview vs authoritative:** Preview publishers **must not** advance the authoritative tick/bus cursor; their events are tagged **preview** and are **excluded** from replay-export streams (extends **3.1** multi-session edge).

## Interfaces

**Upstream:**

- Parent secondary: [[Phase-3-1-Sim-Tick-and-Event-Bus-Spine-Roadmap-2026-03-30-2213]] — `SimEvent` envelope, lanes, DM overwrite class.
- Phase 2 handoff: [[Phase-2-7-3-Shadow-to-Live-Parity-Admission-Ticket-Redemption-and-First-Committed-Tick-Trace-Roadmap-2026-03-30-1800]] — trace id for tick lineage.

**Downstream:**

- **3.1.2+** — tick **scheduling** / **defer-merge** policy, agency drivers, persistence checkpoints.

**Outward guarantees:**

- **Replay:** A consumer replaying lane `L` for tick `T` sees the **same** ordered sequence as the canonical bus log for `(T,L)` (NL contract).
- **Filtering:** DM overwrite class + lane id are **sufficient** for observation layers to route without parsing payloads.

## Edge cases

- **Same tick, same lane, concurrent publishers:** Ordering uses declared **tie-break** (publisher id + monotonic seq); no silent merge of incompatible facts (defer to **3.1.2** merge policy if needed).
- **Subscription churn mid-tick:** Registration changes take effect **at tick boundary** unless an explicit **hot-swap** policy is later defined (execution-deferred); default: **next tick**.
- **Empty stream:** Subscriber receives **empty ordered iterator** — not an error; distinguishes **stall** (no progress) vs **no events**.

## Open questions

- Whether **weather** and **faction** events share a lane or use **separate namespaces** — **execution-deferred** until agency slice; this note assumes **namespace encoded in subscription_key** without fixing schema.

## Pseudo-code readiness

**Mid-technical (depth 3):** algorithm sketches below; no production API.

### Ordering sketch (per lane)

```
ordered_events(L, T) =
  sort_by( filter(events_in_tick(T), lane == L),
           key = (publisher_id, seq_within_publisher) )
```

### Pub/sub sketch

```
subscriptions_for(lane) -> list of Subscription
for each sub in subscriptions_for(L):
  stream(sub) = ordered_events(L, T) filtered by sub.topic_pattern
```

## Risk register (delta vs 3.1 secondary)

| Risk | Mitigation | Decision locus |
| --- | --- | --- |
| **Cross-lane race misread as bug** | Document **partial order** across lanes; barriers explicit | Execution **barrier** contract deferred |
| **Subscription churn ambiguity** | Default **next-tick** visibility | **3.1.2** if hot-swap required |

## Testable acceptance (GWT) — tertiary

Aligns with secondary **3.1** acceptance **A–C** and adds **lane/subscription** coverage.

| # | Given | When | Then |
| --- | --- | --- | --- |
| D | Two publishers emit on **lane L** in tick **T** | Bus closes **L** for **T** | Events are **totally ordered** per tie-break; replay stream matches |
| E | Subscriber **S** registered for `(L, topic_pattern)` | Events published in **T** | **S** sees **filtered** ordered stream; other subscribers unaffected |
| F | **Preview** publisher emits | Export/replay **authoritative** stream | Preview-tagged events **excluded** from authoritative replay export |

## Research integration

> [!note] External grounding
> No new `Ingest/Agent-Research/` notes; continuity from parent **3.1** + Phase 3 primary + **2.7.3** trace semantics.

## Related

- Parent: [[Phase-3-1-Sim-Tick-and-Event-Bus-Spine-Roadmap-2026-03-30-2213]]
