---
title: Phase 3.3.1 — Vitality, consequence, and persistence cohesion seams
roadmap-level: tertiary
phase-number: 3
subphase-index: "3.3.1"
project-id: genesis-mythos-master
status: active
priority: high
progress: 48
handoff_readiness: 85
created: 2026-04-03
tags:
  - roadmap
  - genesis-mythos-master
  - phase-3
para-type: Project
links:
  - "[[Phase-3-3-Vitality-Consequence-and-Persistence-Cohesion-Roadmap-2026-04-03-0005]]"
  - "[[Phase-3-1-4-Persistence-Checkpoint-Boundaries-Roadmap-2026-04-02-2240]]"
  - "[[Phase-3-1-5-Agency-Actor-Drivers-and-Intent-Scheduling-Roadmap-2026-04-02-2250]]"
  - "[[Phase-3-2-1-Observation-Channel-Taxonomy-Roadmap-2026-03-30-2310]]"
  - "[[decisions-log]]"
---

> [!note] #handoff-review
> `handoff_readiness: 85` — tertiary **3.3.1** — **cohesion seams** (**GWT-3.3-A–F**); **3.3.2** extends with **durability matrix** + **I-3.3-A–E** + **GWT-3.3-G–K** — [[Phase-3-3-2-Consequence-Durability-Matrix-and-Persistence-Invariants-Roadmap-2026-04-03-0020]]. Next: **secondary 3.3 rollup** — `workflow_state` **`current_subphase_index: "3.3"`**. Queue: `followup-deepen-phase3-332-gmm-20260403T002000Z`.

### Metric contract (progress vs handoff_readiness)

- **`progress` (48%):** first **tertiary** under **3.3** — seam vocabulary + **GWT-3.3-A–F** table + interface sketches; **3.3.2+** carry **durability matrix** detail.
- **`handoff_readiness` (85):** delegation-ready — junior can wire **VitalitySnapshot** / **ConsequenceRecord** / checkpoint gates without inventing a parallel bus or observation authority.

## Phase 3.3.1 — Cohesion seams (vitality / consequence / persistence)

This **tertiary** names the **three primary seams** where **3.3** must stay internally consistent: (1) **vitality → checkpoint** — which vitality signals are **replay-stable** vs **UX-only**; (2) **consequence → durability class** — how **ConsequenceRecord** semantics bind to **3.1.2** merge outcomes and **3.1.4** ordering; (3) **observation → persistence** — how **3.2.1** **ObservationChannel** exposes **checkpoint-visible** facts without a second durability authority.

## Scope

**In scope:**

- **Seam A — Vitality vs checkpoint eligibility:** NL contract for **VitalitySnapshot** (per tick / cohort): which fields **may** cross **3.1.4** tick-close gate vs remain **diagnostic-only** on **preview_shadow** paths.
- **Seam B — Consequence vs merge + checkpoint:** **ConsequenceRecord** minimum fields: **scope**, **durability_class** (`must_persist` | `ephemeral_ux` | `replay_only`), **lineage** to **3.1.2** merge resolution and **3.1.4** sequence.
- **Seam C — Observation vs persistence:** **3.2.1** **ObservationChannel** **authority_class** must **not** upgrade **preview_shadow** rows to **checkpoint-eligible** without **3.1.5** admission + **3.1.4** gate (re-states **3.2** boundary with **3.3** vocabulary).

**Out of scope:**

- Binary save formats, net sync, rendering shaders (**execution-deferred**).
- Resolving **D-3.1.5-*** operator picks — **execution-deferred** per [[decisions-log]].

## Behavior (natural language)

1. **Vitality seam:** Kernel publishes **VitalitySnapshot** with **checkpoint_eligible** boolean per cohort/slice — **false** for **preview_shadow**-only paths; **true** only when **3.1.5** WorkItem outcomes and **3.1.4** ordering already committed the slice for the tick.
2. **Consequence seam:** Every durable consequence **references** one **3.1.2** merge outcome id (NL) and **3.1.4** checkpoint sequence id — **no** floating consequences that lack merge lineage.
3. **Observation seam:** **3.2.1** channels with **authority_class: preview_shadow** **must** label **non_authoritative_persistence** in rollup narratives; **committed_session** channels **only** surface facts that passed **Seam A**/**Seam B**.

## Interfaces

**Upstream:**

- **3.1.4** — [[Phase-3-1-4-Persistence-Checkpoint-Boundaries-Roadmap-2026-04-02-2240]] — checkpoint ordering + preview non-authoritative durability.
- **3.1.5** — [[Phase-3-1-5-Agency-Actor-Drivers-and-Intent-Scheduling-Roadmap-2026-04-02-2250]] — WorkItem → SimEvent → agency outcomes.
- **3.2.1** — [[Phase-3-2-1-Observation-Channel-Taxonomy-Roadmap-2026-03-30-2310]] — **ObservationChannel** + **authority_class**.

**Parent:**

- **3.3** — [[Phase-3-3-Vitality-Consequence-and-Persistence-Cohesion-Roadmap-2026-04-03-0005]] — secondary cohesion story.

**Downstream:**

- **3.3.2** — [[Phase-3-3-2-Consequence-Durability-Matrix-and-Persistence-Invariants-Roadmap-2026-04-03-0020]] — **consequence durability matrix** + **persistence invariants** — **minted**.
- **3.3 rollup** — secondary **3.3** NL + GWT parity vs **3.3.1–3.3.2** (next deepen target **3.3**).

**Outward guarantees:**

- **No duplicate durability authority** — **3.1.4** remains canonical for “what persisted this tick.”
- **Vitality** never **replaces** **3.1.5** admission — it **summarizes** churn for checkpoint-eligible slices only.

## Edge cases

- **Cosmetic vitality:** UI “pulse” effects with **no** **3.1.4** eligibility — **not** in **VitalitySnapshot** checkpoint slice; **3.2.2** drift disclosure may still show them.
- **Stale cohort:** **Zero churn** N ticks — **vitality** may flag **stale** without triggering **structural regen** (remains **2.7.x** / DM story).

## Open questions

- Minimum **VitalitySnapshot** field set for **faction vs region** granularity before execution prototypes.
- Whether **consequence lineage** ids are **logical-only** vs **cryptographic** in execution (**execution-deferred**).

## Pseudo-code readiness

**Mid-technical (depth 3):** interface sketches — **no** production API.

### Record sketches

```
VitalitySnapshot =
  { tick_id
  , cohort_id
  , checkpoint_eligible        // bool; false when preview_shadow-only
  , churn_signal_level         // NL enum: nominal | pressure | stale | collapsed
  , lineage_to_workitems[]     // refs 3.1.5 WorkItem ids (NL)
  }

ConsequenceRecord =
  { consequence_id
  , scope_descriptor           // what world slice
  , durability_class           // must_persist | ephemeral_ux | replay_only
  , merge_lineage_id           // ties 3.1.2 resolution
  , checkpoint_sequence_ref    // ties 3.1.4 ordering
  }
```

## GWT (3.3 — seam acceptance)

| ID | Gate | Evidence |
| --- | --- | --- |
| GWT-3.3-A | **VitalitySnapshot.checkpoint_eligible** false on preview-only paths | Behavior + Seam A |
| GWT-3.3-B | **ConsequenceRecord.merge_lineage_id** mandatory for **must_persist** | Seam B |
| GWT-3.3-C | **3.2.1** **preview_shadow** does not advance checkpoint sequence | Seam C + 3.1.4 cite |
| GWT-3.3-D | **No orphan consequences** (every **must_persist** has merge + checkpoint refs) | Seam B |
| GWT-3.3-E | **Vitality** does not bypass **3.1.5** admission | Interfaces + Edge |
| GWT-3.3-F | **ObservationChannel** authority matches **durability_class** exposure | Seam C |

## Risk register v0

| Risk | Mitigation | Owner / defer |
| --- | --- | --- |
| Vitality mistaken for save-game truth | **checkpoint_eligible** bit + **3.1.4** cite | **3.3.2** matrix |
| Two consequence taxonomies (sim vs UX) | Single **ConsequenceRecord** + **durability_class** | Tertiary chain |
