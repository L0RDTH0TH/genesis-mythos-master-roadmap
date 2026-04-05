---
title: Phase 3.2.2 — Freshness and drift policy classes (tick-aligned vs frame-aligned)
roadmap-level: tertiary
phase-number: 3
subphase-index: "3.2.2"
project-id: godot-genesis-mythos-master
status: active
priority: high
progress: 50
handoff_readiness: 85
created: 2026-04-02
tags:
  - roadmap
  - godot-genesis-mythos-master
  - phase-3
para-type: Project
links:
  - "[[Phase-3-2-Simulation-Rendering-Decoupling-and-Observation-Channels-Roadmap-2026-04-02-2300]]"
  - "[[Phase-3-2-1-Observation-Channel-Taxonomy-Roadmap-2026-03-30-2310]]"
  - "[[Phase-3-1-1-Event-Bus-Ordering-and-Pub-Sub-Lanes-Roadmap-2026-03-30-1830]]"
  - "[[Phase-3-1-2-Tick-Scheduling-Defer-Merge-and-Work-Queue-Policy-Roadmap-2026-04-02-0020]]"
  - "[[Phase-3-1-4-Persistence-Checkpoint-Boundaries-Roadmap-2026-04-02-2240]]"
  - "[[decisions-log]]"
  - "[[Phase-3-2-3-UX-D3-1-5-Binding-Surfaces-Roadmap-2026-03-30-2319]]"
---

> [!note] #handoff-review
> `handoff_readiness: 85` — tertiary **3.2.2** — **freshness / drift policy classes** bind **ObservationChannel** (**3.2.1**) to **sim tick closure** (**3.1.2**) and **checkpoint authority** (**3.1.4**) via **tick-aligned** vs **frame-aligned** consumption modes; **semantic drift** vs **display lag** are named without inventing a second bus (**3.1.1**). **D-3.1.5-*** remain **execution-deferred**. **3.2.3** minted — [[Phase-3-2-3-UX-D3-1-5-Binding-Surfaces-Roadmap-2026-03-30-2319]]. Next structural cursor **secondary 3.2 rollup** after tertiary chain **3.2.1–3.2.3** complete.

### Metric contract (progress vs handoff_readiness)

- **`progress` (50%):** slice **checklist breadth** — policy classes + GWT + sketches in place; finer UX tuning and **D-3.1.5** binds remain **execution-deferred** / **3.2.3+**.
- **`handoff_readiness` (85):** **delegation quality** — implementers can tag channels with **freshness_class** and **drift_class** without guessing **3.1** ordering or **checkpoint** semantics.

## Phase 3.2.2 — Freshness and drift policy classes

This **tertiary** names **two orthogonal axes** for observation consumers: **freshness alignment** (**tick-aligned** vs **frame-aligned**) and **drift posture** (**semantic drift** bounds vs **display lag** disclosure). It **extends** **3.2.1** **ObservationChannel** records with **non-mutating** policy fields that **reference** **3.1.1** bus lanes, **3.1.2** tick closure, and **3.1.4** checkpoint visibility — **without** changing upstream kernel semantics.

## Scope

**In scope:**

- **Freshness policy classes (NL):**
  - **tick_aligned** — materialize observation **only** on **sim tick boundaries** (after **3.1.2** closure rules for the active tick); **ObservationChannel** exports carry **`sim_tick_id`** (or equivalent monotonic tick token) as the **staleness stamp**; **committed_session** channels **default** to **tick_aligned** unless explicitly documented otherwise.
  - **frame_aligned** — **presentation sampling** between ticks (render / UI frame cadence); **may** interpolate or hold last tick snapshot; **must** pair with **authority_class = preview_shadow** for any **non-checkpoint** visual (per **3.2.1** + **3.1.3**); **never** claims **checkpoint eligibility** or **authoritative SimEvent** export.
- **Drift policy classes (NL):**
  - **semantic_drift_bounded** — **preview_shadow** may diverge from **committed_session** **only** in ways **declared** by **3.1.3** classification + **3.2.1** **authority_class**; **cross-check** at **tick** boundaries when operator promotes preview → work (**3.1.5**).
  - **display_lag_disclosed** — **frame_aligned** channels **declare** **max_display_lag** in **NL** (frames or ms) as **UX contract**, not **sim authority**; **does not** override **3.1.4** ordering of **persistence**.

**Out of scope:**

- Net-sync, input sampling, GPU pacing (execution-deferred).
- Resolving **D-3.1.5-*** (faction cohort / forge preview default) — remain **execution-deferred**; **binding locus** **3.2.3+** / [[decisions-log]].

## Behavior (natural language)

1. **Tick-aligned path:** For **tick_aligned** **ObservationChannel**, **materialize_observation_channel** (**3.2.1** sketch) runs **after** **tick T** is **closed** per **3.1.2** (work queue + merge outcomes) and **checkpoint visibility** per **3.1.4** for **committed** facts.
2. **Frame-aligned path:** For **frame_aligned** **ObservationChannel**, **samples** **last closed tick** or **preview buffer** at **render cadence**; **does not** advance **sim_tick_id**; **preview_shadow** only for **counterfactual** streams.
3. **Drift checks:** **semantic_drift_bounded** requires **explicit** **divergence class** in channel metadata when **preview** and **committed** **both** subscribe to **overlapping** **(lane, pattern)** — default **bounded** by **3.1.3** **preview_shadow** rules; **unbounded** divergence is **routing error**.
4. **Bus boundary:** **3.1.x** **event bus** remains **single** ordering story — **freshness class** is **consumer contract**, **not** a **new** **lane** or **publisher**.

## Interfaces

**Upstream (3.1.x + 3.2.1):**

- **3.1.1** — [[Phase-3-1-1-Event-Bus-Ordering-and-Pub-Sub-Lanes-Roadmap-2026-03-30-1830]] — **lane order** + **replay-visible** iterator contract.
- **3.1.2** — [[Phase-3-1-2-Tick-Scheduling-Defer-Merge-and-Work-Queue-Policy-Roadmap-2026-04-02-0020]] — **tick closure** / **defer-merge** — **tick_aligned** freshness **waits** on this boundary.
- **3.1.4** — [[Phase-3-1-4-Persistence-Checkpoint-Boundaries-Roadmap-2026-04-02-2240]] — **checkpoint** vs **preview** — **committed_session** + **tick_aligned** **must** align with **checkpoint_visibility** from **3.2.1** sketch.
- **3.2.1** — [[Phase-3-2-1-Observation-Channel-Taxonomy-Roadmap-2026-03-30-2310]] — **ObservationChannel** **(lane, subscription_pattern, authority_class)** — this slice **adds** **freshness_class** + **drift_class** fields **downward** only.

**Parent:**

- **3.2** — [[Phase-3-2-Simulation-Rendering-Decoupling-and-Observation-Channels-Roadmap-2026-04-02-2300]] — sim/render decoupling + observation **secondary**.

**Downstream (3.2.3):**

- **3.2.3** — [[Phase-3-2-3-UX-D3-1-5-Binding-Surfaces-Roadmap-2026-03-30-2319]] — **UX / operator** binding surfaces for **D-3.1.5-*** + **frame** disclosure strings (`handoff_readiness` **85**); **next:** **secondary 3.2 rollup**.

**Outward guarantees:**

- **tick_aligned** + **committed_session** **cannot** legally **skip** **3.1.2** tick closure for **authoritative** facts.
- **frame_aligned** **cannot** **emit** **checkpoint-eligible** **exports** — **preview_shadow** **only** for **non-authoritative** **streams** per **3.2.1**.

## Edge cases

- **Multi-rate UI:** Mixed **tick_aligned** panels + **frame_aligned** overlays — **must** **label** **freshness_class** in **UX contract** (execution) — conceptual **requires** **no** **silent** **authority** **upgrade**.
- **Pause / step:** When **sim** **pauses**, **tick_aligned** **observations** **freeze** at **last closed tick**; **frame_aligned** **may** **still** **animate** **preview** **only** — **semantic_drift_bounded** **still** **applies**.

## Open questions

- **D-3.1.5-faction-cohort-lane-vs-shard** — **execution-deferred**; may **subdivide** **lane_id** **bindings** for **observation** — **3.2.3+** / [[decisions-log]].
- **D-3.1.5-forge-sourced-preview-default** — **execution-deferred**; **frame_aligned** **preview** **defaults** **tie** here — **no closure** **in** **3.2.2**.

## Pseudo-code readiness

**Mid-technical (depth 3):** interface sketches — **no** production API.

### Policy-enriched channel record sketch

```
ObservationChannelPolicy =
  { channel_id
  , base : ObservationChannel   // from 3.2.1
  , freshness_class             // tick_aligned | frame_aligned
  , drift_class                 // semantic_drift_bounded | display_lag_disclosed
  , max_display_lag             // optional NL disclosure for frame_aligned UX
  , sim_tick_stamp              // required when tick_aligned + committed export
  }
```

### Freshness selection sketch

```
select_freshness_policy(ch : ObservationChannelPolicy) =
  if ch.base.authority_class == committed_session
  then require(ch.freshness_class == tick_aligned)   // default committed path
  else allow(frame_aligned with preview_shadow)      // preview UX
```

## GWT (Given / When / Then) — tertiary

| ID | Given | When | Then |
| --- | --- | --- | --- |
| GWT-3.2.2-A | Channel **K** is **tick_aligned** + **committed_session** | Tick **T** closes per **3.1.2** | **K** **materializes** **only** **post-closure** facts **eligible** per **3.1.4** |
| GWT-3.2.2-B | Channel **F** is **frame_aligned** | Authoritative export / replay runs | **F** **excluded** from **checkpoint** **export** (**preview_shadow** or **spectate** only) |
| GWT-3.2.2-C | **Preview** diverges from **committed** on same **(lane, pattern)** | Operator promotes work | **3.1.5** **WorkItem** **admission** — **not** **silent** **kernel** **mutation** |

## Risk register (delta vs 3.2.1)

| Risk | Mitigation | Owner / defer |
| --- | --- | --- |
| **Frame** path mistaken for **authority** | **GWT-3.2.2-B** + **authority_class** **parity** in **3.2.1** | **UX** **execution** |
| **Tick** **staleness** **confused** with **bug** | **display_lag_disclosed** **NL** **for** **frame_aligned** | **3.2.3** **copy** |

## Related

- Parent **3.2**: [[Phase-3-2-Simulation-Rendering-Decoupling-and-Observation-Channels-Roadmap-2026-04-02-2300]]
- Prior **3.2.1**: [[Phase-3-2-1-Observation-Channel-Taxonomy-Roadmap-2026-03-30-2310]]
- Next **3.2.3**: [[Phase-3-2-3-UX-D3-1-5-Binding-Surfaces-Roadmap-2026-03-30-2319]]
- Decisions / deferrals: [[decisions-log]]
