---
title: Phase 3.3 — Vitality, consequence, and persistence cohesion
roadmap-level: secondary
phase-number: 3
subphase-index: "3.3"
project-id: godot-genesis-mythos-master
status: active
priority: high
progress: 72
handoff_readiness: 86
created: 2026-04-03
tags:
  - roadmap
  - godot-genesis-mythos-master
  - phase-3
para-type: Project
links:
  - "[[Phase-3-Living-Simulation-and-Dynamic-Agency-Roadmap-2026-03-30-0430]]"
  - "[[Phase-3-1-4-Persistence-Checkpoint-Boundaries-Roadmap-2026-04-02-2240]]"
  - "[[Phase-3-1-5-Agency-Actor-Drivers-and-Intent-Scheduling-Roadmap-2026-04-02-2250]]"
  - "[[Phase-3-2-Simulation-Rendering-Decoupling-and-Observation-Channels-Roadmap-2026-04-02-2300]]"
  - "[[decisions-log]]"
  - "[[Conceptual-Decision-Records/deepen-phase-3-3-secondary-vitality-consequence-persistence-2026-04-03-0005]]"
  - "[[Conceptual-Decision-Records/deepen-phase-3-3-secondary-rollup-nl-gwt-2026-04-03-0030]]"
  - "[[Phase-3-3-1-Vitality-Consequence-Persistence-Cohesion-Seams-Roadmap-2026-04-03-0012]]"
  - "[[Phase-3-3-2-Consequence-Durability-Matrix-and-Persistence-Invariants-Roadmap-2026-04-03-0020]]"
---

> [!note] #handoff-review
> `handoff_readiness: 86` — secondary **3.3 rollup** — **tertiary chain 3.3.1–3.3.2** complete; **NL checklist** + **GWT parity** (**GWT-3.3-A**–**K**) reconciled vs **3.3.1** seams + **3.3.2** matrix / **I-3.3-A–E**. **D-3.1.5-*** remain **execution-deferred** per [[decisions-log]]. `GMM-2.4.5-*` **reference-only**. **Next structural cursor:** mint **Phase 3 secondary 3.4** — align Phase 3 primary glue / downstream handoff (`workflow_state` **`current_subphase_index: "3.4"`**). Resolver: `gate_signature: structural-continue-phase-3-3-secondary` \| queue: `followup-deepen-phase3-33-rollup-gmm-20260403T002500Z`.

## Phase 3.3 — Vitality, consequence, and persistence cohesion

This **secondary 3.3** slice names how **living simulation** stays **coherent** across **time** and **observation surfaces**: **vitality** (what makes the world state meaningfully “alive” or stale at a tick/cohort level), **consequence** (which outcomes **must** persist as durable facts vs which can remain **preview-only** or **UX-interpreted**), and **persistence cohesion** (single checkpoint story across **3.1.4** durability, **3.1.5** agency outcomes, and **3.2.x** observation channels). It **does not** re-derive **3.1.1** bus order, **3.1.2** merge policy, or **3.2.1–3.2.3** observation taxonomy—it **references** them and adds the **cross-cutting durability + meaning** contract.

## Scope

**In scope:**

- **Vitality signals** — what the sim treats as **churn**, **stale cohorts**, **resource pressure**, or **dead-end state** at **NL** (tick-scoped or rolling-window; no numeric SLA at conceptual depth).
- **Consequence classes** — durable **consequence records** that must appear in **checkpoint-eligible** timelines vs **ephemeral** effects that **3.2** may display with **freshness/drift** disclosure only.
- **Persistence cohesion** — alignment between **3.1.4** checkpoint boundaries, **3.1.5** WorkItem/agency outcomes, and **3.2.1** `authority_class` so **replay**, **audit**, and **operator preview** do not disagree on what “really happened.”

**Out of scope:**

- Save-file schema, binary serialization, or migration (execution-deferred).
- Full economy/weather simulation math (execution-deferred).
- Closing **D-3.1.5-*** operator picks — remain **execution-deferred** per [[decisions-log]]; **3.3** may reference **binding loci** from **3.2.3** without new wire formats.

## Behavior (natural language)

1. **Vitality:** The kernel **emits** a minimal **vitality snapshot** (per tick or per cohort policy) that is **sim-visible** and **replay-stable** when it is **checkpoint-eligible**; **preview** and **shadow** lanes may **approximate** vitality for UX but **must not** authoritatively advance **checkpoint sequence** without **3.1.5** admission (re-affirms **3.2** preview/committed boundary).
2. **Consequence:** Agency and environment systems produce **ConsequenceRecord**-shaped semantics (NL): **scope** (what slice of world state is touched), **durability class** (must persist vs may be rolled back), and **lineage** to **3.1.2** merge outcomes and **3.1.4** checkpoint ordering. **Observation** (**3.2.1**) maps **consequence** to **ObservationChannel** without inventing a second authority.
3. **Persistence cohesion:** **One** durability story: **replay anchors** from Phase **2.6.3** / **2.7.x** remain valid; **3.1.4** gates **what** becomes durable at tick close; **3.3** states **which consequences** are **required** to cross that gate vs **optional** UX overlays.

## Interfaces

**Upstream (3.1 chain):**

- **3.1.4** — checkpoint eligibility + preview/replay non-authoritative durability — [[Phase-3-1-4-Persistence-Checkpoint-Boundaries-Roadmap-2026-04-02-2240]].
- **3.1.5** — agency outcomes → WorkItems + SimEvent ordering — [[Phase-3-1-5-Agency-Actor-Drivers-and-Intent-Scheduling-Roadmap-2026-04-02-2250]].

**Upstream (3.2 chain):**

- **3.2.1–3.2.3** — observation channels, freshness/drift, UX binding surfaces — [[Phase-3-2-Simulation-Rendering-Decoupling-and-Observation-Channels-Roadmap-2026-04-02-2300]] and tertiaries.

**Parent (Phase 3 primary):**

- [[Phase-3-Living-Simulation-and-Dynamic-Agency-Roadmap-2026-03-30-0430]] — sim vs render + **glue** row on vitality/consequence without breaking deterministic replay.

**Downstream (3.3.1–3.3.2 + rollup):**

- **3.3.1** — [[Phase-3-3-1-Vitality-Consequence-Persistence-Cohesion-Seams-Roadmap-2026-04-03-0012]] — **cohesion seams** + **GWT-3.3-A–F** (`handoff_readiness` **85**).
- **3.3.2** — [[Phase-3-3-2-Consequence-Durability-Matrix-and-Persistence-Invariants-Roadmap-2026-04-03-0020]] — **consequence durability matrix** + **persistence invariants** + **GWT-3.3-G–K** (`handoff_readiness` **85**).
- **Rollup (this note):** secondary **3.3** **NL closure** + **GWT parity** table **GWT-3.3-A**–**K**; CDR [[Conceptual-Decision-Records/deepen-phase-3-3-secondary-rollup-nl-gwt-2026-04-03-0030]].
- **Next:** mint **Phase 3 secondary 3.4** — see [[workflow_state]] **`current_subphase_index`** and Phase 3 primary **downstream / Phase 4 handoff** glue as scope allows.

**Outward guarantees:**

- **No duplicate durability authority:** **3.1.4** checkpoint ordering remains **canonical**; **3.3** does not introduce a parallel “persist” path for **preview_shadow** lanes.

## Edge cases

- **Consequence vs cosmetic:** A **rendering-only** effect that never crosses **3.1.4** eligibility **must not** be treated as a **consequence** for replay — **3.2.2** drift disclosure may still show it.
- **Cohort collapse:** If vitality signals **stall** (no churn N ticks), **no silent regen** — structural regen remains **Phase 2.7** / **DM overwrite** story, not a **3.3** shortcut.

## Open questions

- **D-3.3-consequence-granularity-npc-faction-region** — Minimum **consequence granularity** for **NPC vs faction vs region** before execution prototypes — **execution-deferred**; authoritative row [[decisions-log]] **D-3.3-consequence-granularity-npc-faction-region**.
- **D-3.3-vitality-determinism-vs-operator-bias** — Whether **vitality** is strictly **deterministic from seed+bundle** or admits **operator bias** knobs without breaking replay — **execution-deferred**; authoritative row [[decisions-log]] **D-3.3-vitality-determinism-vs-operator-bias**.

## Pseudo-code readiness

At **secondary** conceptual depth, **no pseudo-code** is required. **Matrices** and **class tables** live in **3.3.1+** tertiaries.

## Secondary 3.3 rollup (NL checklist + GWT parity)

**NL checklist (secondary depth):**

- [x] Scope / Behavior / Interfaces / Edge cases / Open questions coherent with **3.1.x** / **3.2.x** upstream and Phase 3 primary glue row.
- [x] **Tertiary chain 3.3.1–3.3.2** complete — cohesion seams (**3.3.1**), durability matrix + invariants (**3.3.2**).
- [x] **GWT parity:** **GWT-3.3-A**–**K** trace **3.3.1** / **3.3.2** coverage on this secondary surface (rollup maps **A–F** to **3.3.1**, **G–K** to **3.3.2**).
- [x] **D-3.1.5-*** — **execution-deferred** per [[decisions-log]]; prose does **not** treat them as conceptual hard gates.

**GWT parity mapping (tertiary → rows):**

| Tertiary | GWT rows |
| --- | --- |
| 3.3.1 | GWT-3.3-A — GWT-3.3-F |
| 3.3.2 | GWT-3.3-G — GWT-3.3-K |

## GWT (Given / When / Then) — secondary prose

| ID | Given | When | Then |
| --- | --- | --- | --- |
| GWT-3.3-A | **VitalitySnapshot** is emitted for a tick/cohort | Path is **preview_shadow**-only | **checkpoint_eligible** is **false** — no checkpoint authority from vitality UX |
| GWT-3.3-B | A **must_persist** **ConsequenceRecord** is admitted | Merge resolves | **merge_lineage_id** binds to **3.1.2** outcome before **3.1.4** checkpoint exposure |
| GWT-3.3-C | **ObservationChannel** is **preview_shadow** | Operator views preview | **No** authoritative checkpoint sequence advance — **3.1.4** gate preserved |
| GWT-3.3-D | **must_persist** row exists | Replay/audit lists consequences | Every row has **merge_lineage_id** + **checkpoint_sequence_ref** — **no** orphan durability |
| GWT-3.3-E | **Vitality** summarizes churn | WorkItem admission pending | **Vitality** does **not** bypass **3.1.5** — admission remains canonical |
| GWT-3.3-F | **ObservationChannel** exposes a fact | **durability_class** vs **authority_class** | **committed_session** only if matrix + **I-3.3-B** allow — **no** class mismatch |
| GWT-3.3-G | **must_persist** + merge **denied** | Operator checks live session | **No** **committed_session** claim of durable truth — matrix forbids |
| GWT-3.3-H | **I-3.3-B** required | **3.2.1** committed observation renders | **checkpoint_sequence_ref** present before committed exposure |
| GWT-3.3-I | **ephemeral_ux** after **deny** | Preview shows effect | **preview_shadow** + **3.2.2** drift disclosure — not checkpoint-eligible |
| GWT-3.3-J | **replay_only** fact exists | Tick advances | **No** checkpoint sequence advance from replay-only rows (**I-3.3-E**) |
| GWT-3.3-K | **ephemeral_ux** is shown | Later tick would “promote” | **No** silent promotion — **I-3.3-D** — new tick + **3.1.5** + **3.1.4** if ever promoted |

## Risk register v1

| Risk | Mitigation | Owner / defer |
| --- | --- | --- |
| Two durability truths (checkpoint vs observation) | **3.2.1** `authority_class` + **3.1.4** gate + **3.3** matrix + **GWT-3.3-F/G** | Closed at conceptual rollup |
| Vitality mistaken for authoritative regen | **D-3.1.5-*** + **3.1.3** overwrite classes — **execution-deferred** picks | [[decisions-log]] |
| Matrix drift vs **3.1.2** merge enum | **merge_lineage_id** mandatory for **must_persist**; **GWT-3.3-B/H** | RECAL if needed |

## Tertiary notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/godot-genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-3-Vitality-Consequence-and-Persistence-Cohesion"
WHERE roadmap-level = "secondary" OR roadmap-level = "tertiary" OR roadmap-level = "task"
SORT subphase-index ASC, file.name ASC
```
