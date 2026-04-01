---
title: Phase 4.1.1 — Lane adapters, emphasis, and GWT narrowing
roadmap-level: tertiary
phase-number: 4
subphase-index: "4.1.1"
project-id: genesis-mythos-master
status: active
priority: high
progress: 55
handoff_readiness: 85
created: 2026-04-03
tags:
  - roadmap
  - genesis-mythos-master
  - phase-4
para-type: Project
links:
  - "[[Phase-4-1-Narrative-Rendering-and-Consumer-Surface-Lanes-Roadmap-2026-04-03-2015]]"
  - "[[Phase-4-Perspective-Split-and-Control-Systems-Roadmap-2026-03-30-0430]]"
  - "[[Phase-3-4-1-Handoff-Seam-Catalog-and-Consumer-Contract-Rows-Roadmap-2026-04-03-0115]]"
  - "[[Phase-3-2-1-Observation-Channel-Taxonomy-Roadmap-2026-03-30-2310]]"
  - "[[decisions-log]]"
  - "[[Phase-4-1-2-Cross-Lane-Coherence-and-Emphasis-Reconciliation-Roadmap-2026-03-30-1200]]"
---

> [!note] #handoff-review
> `handoff_readiness: 85` — tertiary **4.1.1** — **lane adapters** bind **Narrative/UI** vs **Rendering** lanes to **3.4.1** **SeamId** rows + **3.2.1** **ObservationChannel** subscriptions; **emphasis** narrows which channel subsets each lane may elevate under Phase 4 **mode graph**; **GWT** rows below are **narrowed** evidence targets vs secondary **GWT-4.1-A–K**. **Superseded for cursor:** tertiary **4.1.2** minted — [[Phase-4-1-2-Cross-Lane-Coherence-and-Emphasis-Reconciliation-Roadmap-2026-03-30-1200]]; next structural cursor **4.1.3** (continue **4.1** chain).

## Phase 4.1.1 — Lane adapters, emphasis, and GWT narrowing

This **tertiary** decomposes **secondary 4.1** into actionable NL contracts for **how** each consumer lane **adapts** upstream handoff rows: **lane adapters** (subscription + refresh + coalescing policy hooks), **emphasis rules** (which **ObservationChannel** ids get visual or narrative priority under current **camera / perspective mode**), and **GWT narrowing** — explicit **Given / When / Then / Evidence** cells that map **GWT-4.1-A–K** to this slice only (no duplicate seam semantics).

## Scope

**In scope:**

- **LaneAdapter contract (NL)** — per-lane record: `{ lane_id, seam_id_refs[], observation_channel_ids[], freshness_class, drift_class, coalescing_policy_hook, authority_class_legibility }` anchored to **3.4.1** rows and **3.2.1** channel ids (no new seam ids).
- **Emphasis vocabulary (NL)** — finite set of **emphasis kinds** (e.g. `narrative_priority`, `render_budget_priority`, `dm_live_highlight`, `orthographic_tabletop_scope`) that **select** subsets of subscribed channels for presentation — **read-only**; cannot promote **preview_shadow** to **committed_session** semantics (**3.2.1** **authority_class**).
- **Mode graph handoff** — inputs from Phase 4 **primary** (perspective modes + interpolator) **constrain** which emphasis kinds are **legal** together (e.g. DM flight vs FP vs orthographic tabletop) without adding sim state.

**Out of scope:**

- Concrete UI control IDs, renderer batch APIs, or font/layout (**execution-deferred**).
- Closing **D-3.4-phase4-consumer-granularity** export cadence (**execution-deferred**).
- Bundle split resolution for **D-3.4-narrative-rendering-split** (**execution-deferred**; remains in [[decisions-log]]).

## Behavior (natural language)

1. **Adapter resolution order:** For each **SeamId** consumed, the lane adapter **first** resolves the **3.4.1** catalog row, **then** binds **ObservationChannel** ids from **3.2.1**, **then** applies **3.2.2** freshness/drift classes — **fixed order** so both lanes cannot diverge on seam meaning.
2. **Emphasis as projection:** Emphasis **reweights** which subscribed facts surface first in UX; it **does not** change merge eligibility, checkpoint boundaries (**3.1.4**), or overwrite class (**3.1.3**).
3. **GWT narrowing:** Each row in the table below is a **refinement** of the matching **GWT-4.1-*** id from the secondary — if a secondary row has no matching narrowed row here, evidence remains **planned** at tertiary **4.1.2+**.

## Interfaces

**Parent:**

- [[Phase-4-1-Narrative-Rendering-and-Consumer-Surface-Lanes-Roadmap-2026-04-03-2015]] — dual lanes + **GWT-4.1-A–K** scaffold.

**Upstream:**

- [[Phase-3-4-1-Handoff-Seam-Catalog-and-Consumer-Contract-Rows-Roadmap-2026-04-03-0115]] — **SeamId** rows.
- [[Phase-3-2-1-Observation-Channel-Taxonomy-Roadmap-2026-03-30-2310]] — **ObservationChannel** + **authority_class**.
- [[Phase-3-2-2-Freshness-Drift-Policy-Classes-Roadmap-2026-04-02-2350]] — freshness/drift classes.

**Phase 4 primary:**

- [[Phase-4-Perspective-Split-and-Control-Systems-Roadmap-2026-03-30-0430]] — mode graph + camera/interpolator abstraction.

## Edge cases

- **Emphasis vs coalescing conflict:** narrative **coalescing_policy_hook** may batch more aggressively than rendering — still must disclose **display_lag_disclosed** vs **semantic_drift_bounded** per **3.2.2** when operators compare lanes.
- **Orthographic + emphasis:** large tabletop views may apply **`orthographic_tabletop_scope`** emphasis without implying a second **SeamId** bundle (**3.4.1** row remains authoritative).

## Open questions

- Minimum shared **emphasis kind** enum size for cross-lane test matrices (**execution-deferred**).
- Whether **narrative** lane may attach **forge-sourced** preview defaults (**D-3.1.5-forge-sourced-preview-default**) at emphasis layer — **execution-deferred** wire policy.

## Pseudo-code readiness

**Mid-technical:** interface sketches for **LaneAdapter** resolution order and **emphasis** selection as structured bullets; no executable pseudo-code required at **4.1.1** unless **4.1.2** escalates.

## Tertiary slice GWT — narrowed vs **GWT-4.1-A–K**

| Narrow ID | Parent GWT | Given | When | Then | Evidence (this slice) |
| --- | --- | --- | --- | --- | --- |
| **GWT-4.1.1-A** | **GWT-4.1-A** | **SeamId** row | Lane adapter resolves | Resolution order: catalog → channel → freshness/drift | § Behavior (1) |
| **GWT-4.1.1-B** | **GWT-4.1-B** | **authority_class** | Emphasis applied | **preview_shadow** never treated as durable | § Scope emphasis |
| **GWT-4.1.1-C** | **GWT-4.1-C** | **3.2.2** classes | Lane presents frame/tick | Classes explicit per adapter record | § LaneAdapter contract |
| **GWT-4.1.1-D** | **GWT-4.1-D** | Checkpoint boundary | “Save-adjacent” UX | No fake checkpoint | § Behavior (2) + **3.1.4** |
| **GWT-4.1.1-E** | **GWT-4.1-E** | DM overwrite | Emphasis reflects live vs structural | No re-classification | § Behavior (2) |
| **GWT-4.1.1-F** | **GWT-4.1-F** | Mode switch | Adapter + emphasis | Subscriptions stable; presentation changes only | § Scope mode graph |
| **GWT-4.1.1-G** | **GWT-4.1-G** | **D-3.4-narrative-rendering-split** | Bundle policy TBD | Two lanes, one sim truth preserved | [[decisions-log]] (deferral explicit) |
| **GWT-4.1.1-H** | **GWT-4.1-H** | **D-3.4-phase4-consumer-granularity** | Cadence TBD | Decision row exists | [[decisions-log]] |
| **GWT-4.1.1-I** | **GWT-4.1-I** | High-frequency events | Narrative coalescing | Staleness/disclosure per **3.2.2** | § Edge cases |
| **GWT-4.1.1-J** | **GWT-4.1-J** | Render budget stress | Degradation | **SeamId** semantics unchanged | § Behavior + **3.2.2** |
| **GWT-4.1.1-K** | **GWT-4.1-K** | Execution-only validator codes | Advisory | Conceptual waiver | [[roadmap-state]] |

## Research integration

- None (vault-first pattern).
