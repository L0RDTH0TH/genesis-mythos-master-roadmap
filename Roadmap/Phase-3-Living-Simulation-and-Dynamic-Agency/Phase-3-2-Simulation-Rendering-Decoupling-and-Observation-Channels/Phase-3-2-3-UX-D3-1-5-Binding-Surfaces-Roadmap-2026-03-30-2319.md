---
title: Phase 3.2.3 — UX binding surfaces for observation policy + D-3.1.5 loci
roadmap-level: tertiary
phase-number: 3
subphase-index: "3.2.3"
project-id: sandbox-genesis-mythos-master
status: active
priority: high
progress: 52
handoff_readiness: 85
created: 2026-03-30
tags:
  - roadmap
  - sandbox-genesis-mythos-master
  - phase-3
para-type: Project
links:
  - "[[Phase-3-2-Simulation-Rendering-Decoupling-and-Observation-Channels-Roadmap-2026-04-02-2300]]"
  - "[[Phase-3-2-2-Freshness-Drift-Policy-Classes-Roadmap-2026-04-02-2350]]"
  - "[[Phase-3-2-1-Observation-Channel-Taxonomy-Roadmap-2026-03-30-2310]]"
  - "[[Phase-3-1-5-Agency-Actor-Drivers-and-Intent-Scheduling-Roadmap-2026-04-02-2250]]"
  - "[[Phase-3-1-3-Sim-Visible-Classification-and-DM-Overwrite-Channel-Mapping-Roadmap-2026-04-02-0035]]"
  - "[[decisions-log]]"
---

> [!note] #handoff-review
> `handoff_readiness: 85` — tertiary **3.2.3** — **UX / operator binding surfaces** wire **ObservationChannel** (**3.2.1**) + **freshness/drift policy classes** (**3.2.2**) into **legible** preview vs committed semantics for tools and forge—without a second bus (**3.1.1**) or silent kernel writes. **D-3.1.5-*** (**faction cohort lane vs shard**, **forge-sourced preview default**) get **explicit NL binding rows** here; **execution** wire formats remain **deferred**. **3.2** tertiary chain **3.2.1–3.2.3** structurally complete — next cursor **secondary 3.2 rollup** (or Phase **3** primary polish). Resolver: `gate_signature: structural-continue-phase-3-2-secondary`, `effective_track: conceptual`.

### Metric contract (progress vs handoff_readiness)

- **`progress` (52%):** **UX binding matrix** + **GWT S–U** + disclosure sketches in place; pixel polish and engine types **execution-deferred**.
- **`handoff_readiness` (85):** **delegation quality** — designers/implementers can map **UI panels** → **ObservationChannel** + **freshness_class** / **drift_class** and route **forge/preview** admissions to **3.1.5** without guessing **3.1.3** classification.

## Phase 3.2.3 — UX binding surfaces (observation policy + D-3.1.5 loci)

This **tertiary** names **operator-visible surfaces** that **bind** **3.2.1** **ObservationChannel** identity (**lane**, **subscription_pattern**, **authority_class**) and **3.2.2** **freshness_class** / **drift_class** to **tooling behavior**: what the **player / DM / forge** sees, what is **labeled non-authoritative**, and where **D-3.1.5-*** questions attach **without** resolving execution data types.

## Scope

**In scope:**

- **Panel / surface taxonomy (NL):** **Committed inspector** (tick-aligned, committed_session) vs **Preview / forge suggestion** (preview_shadow, frame_aligned allowed) vs **Spectate / replay read-only** — each **must** declare **which ObservationChannel fields** it displays and **which admission path** applies when the operator **accepts** (**3.1.5** WorkItem).
- **Disclosure strings (NL contract):** **frame_aligned** surfaces **must** surface **drift_class** (**display_lag_disclosed** max lag / **semantic_drift_bounded** divergence class) per **3.2.2** — as **reader-visible labels**, not new sim authority.
- **D-3.1.5 binding rows (conceptual only):**
  - **D-3.1.5-faction-cohort-lane-vs-shard:** UX **binds** cohort/faction selectors to **`lane_id` / subscription scope** on **ObservationChannel** — **lane** = single bus lane subscription; **shard** = partitioned replica of lane families — **decision remains open**; this slice **requires** UI **not** to imply **cross-shard** authority without **3.1.2** merge + **3.1.5** admission (**NL**).
  - **D-3.1.5-forge-sourced-preview-default:** **Default** path labels **forge-sourced** suggestions as **preview_shadow** + **frame_aligned** until promoted — aligns **3.1.3** **preview_shadow** with **3.2.2**; **execution** typing deferred.

**Out of scope:**

- Widget frameworks, accessibility audits, netcode (**execution-deferred**).
- Closing **D-3.1.5** with code IDs — **decisions-log** remains authority for **open**/**deferred** status until operator pick + execution track.

## Behavior (natural language)

1. **Channel picker / panel routing:** Any UI that **subscribes** to sim-visible output **selects** an **ObservationChannel** record; **authority_class** **preview_shadow** **cannot** present **checkpoint-eligible** **exports** or **authoritative** **SimEvent** **publish** affordances (**3.2.1**, **3.1.4**).
2. **Forge / suggestion lane:** **Forge-sourced** **candidates** **default** to **preview_shadow** **ObservationChannel** **or** **explicitly tagged** **counterfactual** channel — **promotion** **only** via **3.1.5** **WorkItem** admission (**3.1.2** merge outcomes).
3. **Faction / cohort UX:** **Until** **D-3.1.5** resolved, **UI** **must** **label** whether the **panel** **scopes** to **lane**-local cohorts vs **shard**-partitioned views — **no** **silent** **upgrade** to **committed_session** **authority**.
4. **Freshness / drift legibility:** **tick_aligned** **panels** **show** **sim_tick_id** **staleness**; **frame_aligned** **panels** **show** **max_display_lag** / **divergence class** per **3.2.2** — **cosmetic** **only** relative to **3.1.2** **closure**.

## Interfaces

**Upstream:**

- **3.2.1** — [[Phase-3-2-1-Observation-Channel-Taxonomy-Roadmap-2026-03-30-2310]] — **ObservationChannel** **(lane, subscription_pattern, authority_class)**.
- **3.2.2** — [[Phase-3-2-2-Freshness-Drift-Policy-Classes-Roadmap-2026-04-02-2350]] — **freshness_class**, **drift_class** on channels.
- **3.1.3** — [[Phase-3-1-3-Sim-Visible-Classification-and-DM-Overwrite-Channel-Mapping-Roadmap-2026-04-02-0035]] — **preview_shadow** vs **committed** **classification**.
- **3.1.5** — [[Phase-3-1-5-Agency-Actor-Drivers-and-Intent-Scheduling-Roadmap-2026-04-02-2250]] — **intent → WorkItem** **admission** for **promotion** paths.

**Parent:**

- **3.2** — [[Phase-3-2-Simulation-Rendering-Decoupling-and-Observation-Channels-Roadmap-2026-04-02-2300]] — **secondary** **rollup** **target** **next** **deepen** **after** **this** **slice**.

**Downstream:**

- **Secondary 3.2 rollup** — NL **closure** row + **GWT** **parity** **vs** **3.2** **open** **questions** **when** **ready** — **not** **in** **this** **tertiary** **body**.

**Outward guarantees:**

- **No** **UX** **path** **may** **bypass** **3.1.5** **for** **kernel** **mutation** **from** **preview** **lanes**.
- **D-3.1.5** **rows** **gain** **grep-stable** **UX** **anchor** **phrases** **in** **this** **note** **+** **decisions-log** **cross-links** — **not** **closure**.

## Edge cases

- **Multi-panel coherence:** **Same** **tick** **committed** **+** **frame** **preview** **side-by-side** — **must** **not** **contradict** **sim_tick_id** **ordering**; **preview** **labels** **non-authoritative**.
- **Operator overrides:** **DM** **live** **tweak** **vs** **regen** **remains** **3.1.3** — **UX** **routes** **structural** **regen** **to** **regen** **intent** **path** **(Phase** **3** **primary** **/ upstream)**.

## Open questions

- **Exact** **shard** **visual** **metaphor** **(tabs** **vs** **filters)** — **execution-deferred** **/ UX** **research**.
- **Accessibility** **of** **drift** **disclosures** — **execution-deferred**.

## Pseudo-code readiness

**Mid-technical (depth 3):** **interface** **sketches** **only** — **no** **shipping** **API**.

### UX ↔ channel binding sketch

```
UxSurface =
  { panel_id
  , primary_observation_channel_ref  // ties to ObservationChannel id / key (NL)
  , optional_secondary_channels[]    // overlays; still non-authoritative if preview_shadow
  , admission_action                 // none | propose_work_item | (execution: promote)
  , freshness_expectation            // tick_aligned | frame_aligned (must match 3.2.2)
  , drift_disclosure_mode            // semantic_drift_bounded | display_lag_disclosed | none
  , d3_1_5_binding_tags[]            // [faction_cohort_scope, forge_preview_default] — labels only
  }
```

## GWT (Given / When / Then) — UX / binding

| ID | Given | When | Then |
| --- | --- | --- | --- |
| GWT-3.2.3-S | A **preview_shadow** channel is shown | Operator hits **Accept** | **3.1.5** **WorkItem** **path** **is** **the** **only** **mutation** **story** |
| GWT-3.2.3-T | **Forge** **suggests** **state** | Default **surface** | **Tagged** **preview_shadow** **+** **frame_aligned** **per** **D-3.1.5** **carry** |
| GWT-3.2.3-U | **Faction** **panel** **scoped** **ambiguously** | **D-3.1.5** **still** **open** | **UI** **shows** **lane** **vs** **shard** **scope** **label** **without** **claiming** **merge** **authority** |

## Related

- **Decisions:** [[decisions-log]] — **D-3.1.5-faction-cohort-lane-vs-shard**, **D-3.1.5-forge-sourced-preview-default**
- **CDR:** [[Conceptual-Decision-Records/deepen-phase-3-2-3-ux-d3-1-5-binding-surfaces-2026-03-30-2319]]
