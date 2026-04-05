---
title: Phase 3.1.5 — Agency, actor drivers, and intent scheduling
roadmap-level: tertiary
phase-number: 3
subphase-index: "3.1.5"
project-id: sandbox-genesis-mythos-master
status: active
priority: high
progress: 46
progress_note: slice-local depth estimate vs siblings 3.1.1–3.1.4 (not Phase 3 rollup %)
handoff_readiness: 85
created: 2026-04-02
tags:
  - roadmap
  - sandbox-genesis-mythos-master
  - phase-3
para-type: Project
links:
  - "[[Phase-3-1-Sim-Tick-and-Event-Bus-Spine-Roadmap-2026-03-30-2213]]"
  - "[[Phase-3-1-4-Persistence-Checkpoint-Boundaries-Roadmap-2026-04-02-2240]]"
  - "[[Phase-3-1-2-Tick-Scheduling-Defer-Merge-and-Work-Queue-Policy-Roadmap-2026-04-02-0020]]"
  - "[[Phase-3-1-1-Event-Bus-Ordering-and-Pub-Sub-Lanes-Roadmap-2026-03-30-1830]]"
  - "[[Phase-3-Living-Simulation-and-Dynamic-Agency-Roadmap-2026-03-30-0430]]"
  - "[[decisions-log]]"
---

> [!note] #handoff-review
> `handoff_readiness: 85` — tertiary **3.1.5** — **agency / actor drivers** bind **who may schedule work into tick `T`** and **how intents enter** the **3.1.2** work queue after **2.2.x** envelope semantics, with **bus-visible** publication per **3.1.1** and **classification** per **3.1.3** before **3.1.4** durability; `GMM-2.4.5-*` remain **reference-only**. **3.1 chain 3.1.1–3.1.5 complete**; next structural cursor **3.2** (mint next Phase 3 secondary).

## Phase 3.1.5 — Agency, actor drivers, and intent scheduling

This **tertiary** defines **actor lanes** and **agency drivers** that turn **normalized intents** (Phase **2.2** contract family) into **tick-scoped work items** and **SimEvent-eligible actions** without re-deriving **2.4** commit envelopes—while staying consistent with **tick closure** (**3.1.2**), **bus ordering** (**3.1.1**), **sim-visible classification** (**3.1.3**), and **checkpoint gates** (**3.1.4**).

## Scope

**In scope:**

- **Actor lane taxonomy (NL):** deterministic labels for **who** may enqueue tick work (e.g. DM lane, system/sim lane, player/operator lane, forge-adjacent read-mostly lane) and **how lanes interact** with **merge policy** from **3.1.2**.
- **Intent → WorkItem admission:** binding rules from a **resolved intent** (post-**2.2** classify/resolve) to a **WorkItem** record for tick `T` with explicit **priority slot** and **defer compatibility** vs **3.1.2** matrix.
- **Agency vs environment:** which driver classes may **mutate world-authoritative state** vs **emit observation / preview** per **3.1.3** classes in the same tick.

**Out of scope:**

- Concrete ECS, scripting VM, or network replication (**execution-deferred**).
- Full intent schema registry beyond **HookPayloadOutline** cross-references (**execution-deferred**).

## Behavior (natural language)

1. **Lane precedence:** When two lanes produce **compatible** WorkItems for `T`, **3.1.2** merge ordering applies; when **incompatible**, **3.1.2** **block** / **defer** paths run before any **PersistenceCheckpoint** (**3.1.4**).
2. **Intent scheduling:** **Agency drivers** consume **deterministic hook emission** handoff semantics from **2.2.4**/**2.2.5** as **logical inputs** to **WorkItem** creation—without reopening **2.4** branch tables.
3. **Bus publication:** **SimEvent** emissions that **announce agency outcomes** follow **3.1.1** lane order; **preview_shadow** agency may not assert authoritative world mutation (**3.1.3**).

## Interfaces

**Upstream:**

- **3.1.2:** [[Phase-3-1-2-Tick-Scheduling-Defer-Merge-and-Work-Queue-Policy-Roadmap-2026-04-02-0020]] — work queue + defer-merge is the **sink** for admitted intents.
- **3.1.1:** [[Phase-3-1-1-Event-Bus-Ordering-and-Pub-Sub-Lanes-Roadmap-2026-03-30-1830]] — bus ordering for agency-announcing events.
- **3.1.3:** [[Phase-3-1-3-Sim-Visible-Classification-and-DM-Overwrite-Channel-Mapping-Roadmap-2026-04-02-0035]] — classification filters **authoritative** agency mutations vs **observation-only** paths.
- **3.1.4:** [[Phase-3-1-4-Persistence-Checkpoint-Boundaries-Roadmap-2026-04-02-2240]] — checkpoints only after tick closure + classification gates.

**Phase 2 handoff:**

- **2.2.x** intent resolver chain (normalize → classify → resolve → emit) — cited as **logical upstream**; no branch table replay here.
- **2.7.3:** [[Phase-2-7-3-Shadow-to-Live-Parity-Admission-Ticket-Redemption-and-First-Committed-Tick-Trace-Roadmap-2026-03-30-1800]] — first committed tick trace remains **prior** to living-sim agency at `T≥1`.

**Downstream:**

- **Phase 3 secondary 3.2+** (mint on next structural deepen) — additional living-simulation bodies (e.g. environment systems, faction AI) consume **actor lane** + **WorkItem** contracts defined here at NL.

**Outward guarantees:**

- **No silent cross-lane merge** of incompatible agency outcomes—always **3.1.2** explicit outcome.
- **Replay narrative:** agency-originated **SimEvent** records cite **actor lane** + **tick id** + **intent lineage id** (NL) for audit continuity.

## Edge cases

- **DM emergency override:** competes with **system** lane—**3.1.2** priority matrix + **3.1.3** DM overwrite class must agree before merge closure.
- **Zero-agency tick:** environment-only ticks still advance **T** with **empty** agency WorkItem set (closure rules unchanged).
- **Multi-intent same actor:** dedupe/idempotency hooks from **2.2.1** prevent duplicate **WorkItem** rows for the same logical intent.

## Open questions

- **Faction cohort scheduling:** whether cohorts share one **lane** or **shard** by faction id — **execution-deferred** binding.
- **Forge-sourced suggestions:** whether they enter as **preview-only** WorkItems by default — ties to **3.1.3** **preview_shadow** (**TBD with contract** until Phase 3 **3.2+**).

## Pseudo-code readiness

**Mid-technical (depth 3):** sketches only.

### Admit intent to WorkItem

```
admit_intent_to_tick(intent_ref, lane, T):
  assert classified_per_2_2_2(intent_ref)
  assert compatible_with_merge_matrix(intent_ref, T, lane)  # 3.1.2
  enqueue WorkItem(tick=T, lane=lane, intent_ref=intent_ref)
```

### Agency SimEvent publish

```
on_agency_outcome(work_item_closed):
  if classification(emit) == authoritative_tick:
    publish SimEvent(kind=agency_outcome, tick=T, lineage=intent_ref)  # 3.1.1
```

## Risk register (delta vs 3.1.4)

| Risk | Mitigation | Decision locus |
| --- | --- | --- |
| **Agency bypasses merge matrix** | WorkItem admission requires **3.1.2** compatibility | This note + **3.1.2** |
| **Preview lane mutates world** | **3.1.3** classification gate + no checkpoint without closure | This note + **3.1.3** + **3.1.4** |

## Testable acceptance (GWT) — tertiary

Extends **3.1** A–C, **3.1.1** D–F, **3.1.2** G–I, **3.1.3** J–L, **3.1.4** M–O.

| # | Given | When | Then |
| --- | --- | --- | --- |
| P | Resolved **intent** + **actor lane** | Admission runs for tick `T` | **WorkItem** exists with **lane** + **intent lineage** reference (NL) |
| Q | **Incompatible** agency outcomes | Merge matrix evaluates | **3.1.2** **block** or **defer**; **no** **PersistenceCheckpoint** until resolved (**3.1.4**) |
| R | **preview_shadow** agency path | Publish attempted | **No** authoritative **SimEvent** / world mutation without reclassification (**3.1.3**) |

## Research integration

> [!note] External grounding
> No `Ingest/Agent-Research/` notes bound this mint; continuity is from **2.2.x** resolver chain + **3.1.1–3.1.4** spine notes + Phase 3 primary ([[Phase-3-Living-Simulation-and-Dynamic-Agency-Roadmap-2026-03-30-0430]]).
