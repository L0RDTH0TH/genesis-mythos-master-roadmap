---
title: Phase 4.1 — Narrative + rendering consumer surface lanes
roadmap-level: secondary
phase-number: 4
subphase-index: "4.1"
project-id: sandbox-genesis-mythos-master
status: complete
priority: high
progress: 100
handoff_readiness: 86
created: 2026-04-03
tags:
  - roadmap
  - sandbox-genesis-mythos-master
  - phase-4
para-type: Project
links:
  - "[[Phase-4-Perspective-Split-and-Control-Systems-Roadmap-2026-03-30-0430]]"
  - "[[Phase-3-4-1-Handoff-Seam-Catalog-and-Consumer-Contract-Rows-Roadmap-2026-04-03-0115]]"
  - "[[Phase-3-2-1-Observation-Channel-Taxonomy-Roadmap-2026-03-30-2310]]"
  - "[[decisions-log]]"
  - "[[Phase-4-1-1-Lane-Adapters-Emphasis-and-GWT-Narrowing-Roadmap-2026-04-03-2016]]"
  - "[[Phase-4-1-2-Cross-Lane-Coherence-and-Emphasis-Reconciliation-Roadmap-2026-03-30-1200]]"
  - "[[Phase-4-1-3-Consumer-Surface-Framing-and-Presentation-Time-Validation-Roadmap-2026-04-03-2110]]"
---

> [!note] #handoff-review
> `handoff_readiness: 86` — secondary **4.1 rollup complete** — **narrative-facing** vs **rendering-facing** **consumer surface lanes** over one **SeamId** / **ObservationChannel** truth; **GWT-4.1-A–K** parity checked against **4.1.1–4.1.3** and upstream **3.4.1** / **3.2.1–3.2.3** references; **D-3.4-narrative-rendering-split** + **D-3.4-phase4-consumer-granularity** remain execution-deferred decision rows. **Tertiary 4.1.1** — [[Phase-4-1-1-Lane-Adapters-Emphasis-and-GWT-Narrowing-Roadmap-2026-04-03-2016]]; **4.1.2** — [[Phase-4-1-2-Cross-Lane-Coherence-and-Emphasis-Reconciliation-Roadmap-2026-03-30-1200]]; **4.1.3** — [[Phase-4-1-3-Consumer-Surface-Framing-and-Presentation-Time-Validation-Roadmap-2026-04-03-2110]]. Next structural cursor: **4.2** (next secondary under Phase 4).

## Phase 4.1 — Narrative + rendering consumer surface lanes

This **secondary 4.1** slice is the first structural body under Phase **4 perspective split**: it names **two consumption lanes**—**narrative/UI** and **rendering**—that **attach** to **Phase 3** **ObservationChannel** exports and **Phase 3.4.1** **SeamId** / consumer rows **without** re-deriving **3.1** bus semantics, **3.1.4** checkpoint authority, or **3.2** preview/commit boundaries. **Camera rigs** and **interpolator** contracts (Phase 4 primary) **consume** the same upstream facts through **lane-appropriate adapters** (refresh policy, batching, emphasis) while preserving **one** authoritative sim story.

## Scope

**In scope:**

- **Dual consumer lanes** — **Narrative/UI** lane vs **rendering** lane as **distinct subscribers** to the same **sim-visible** exports (per **3.2.1** taxonomy + **authority_class**), with **explicit** per-lane **refresh** and **coalescing** policy hooks at NL (not wire formats).
- **SeamId-first handoff** — Phase 4 consumers **resolve** inputs through **3.4.1** catalog rows (forbidden silent seam duplication vs primary § Interfaces).
- **Interpolator + mode graph inputs** — how **camera intent** (FP / DM flight / orthographic) **selects** which **ObservationChannel** subsets each lane may **emphasize** (read-only emphasis; no sim mutation).

**Out of scope:**

- Concrete renderer API, UI framework, or asset pipeline (execution-deferred).
- Closing **D-3.4-phase4-consumer-granularity** export cadence (execution-deferred).
- Netcode, GPU perf, or input device drivers (conceptual waiver).

## Behavior (natural language)

1. **Lane registration:** Each consumer lane declares **which ObservationChannel ids** it may **subscribe** to and under which **freshness_class** / **drift_class** expectations (**3.2.2**), with **preview_shadow** vs **committed_session** legibility preserved.
2. **No dual truth:** Both lanes **read** the same **SeamId-keyed** row semantics from **3.4.1**; differences are **presentation policy** (cadence, batching, emphasis), not alternate checkpoint or overwrite semantics.
3. **Interpolation handoff:** **Camera / mode** transitions (primary § Behavior) **feed** lane adapters so **tick-aligned** vs **frame-aligned** presentation stays consistent with **3.2.2** classes.

## Interfaces

**Upstream (Phase 3):**

- Handoff catalog: [[Phase-3-4-1-Handoff-Seam-Catalog-and-Consumer-Contract-Rows-Roadmap-2026-04-03-0115]].
- Observation taxonomy: [[Phase-3-2-1-Observation-Channel-Taxonomy-Roadmap-2026-03-30-2310]]; freshness/drift: [[Phase-3-2-2-Freshness-Drift-Policy-Classes-Roadmap-2026-04-02-2350]]; UX binds: [[Phase-3-2-3-UX-D3-1-5-Binding-Surfaces-Roadmap-2026-03-30-2319]].

**Parent (Phase 4 primary):**

- [[Phase-4-Perspective-Split-and-Control-Systems-Roadmap-2026-03-30-0430]] — perspective modes + camera/interpolator abstraction + **D-3.4-*** NL loci.

**Downstream (4.1+):**

- **4.1.1–4.1.3** — tertiaries under **4.1** decompose **lane adapters**, **cross-lane coherence / reconciliation**, **presentation envelope + presentation-time validation + operator legibility**; **secondary 4.1 rollup complete** (NL checklist + **GWT-4.1** parity vs **4.1.1–4.1.3**); **next** — **4.2** secondary mint.

**Outward guarantees:**

- **Authority alignment:** lanes cannot treat **preview_shadow** as **committed_session** for persistence-adjacent UX affordances (**3.2.1** **authority_class**).
- **Overwrite story:** DM **live** vs **structural** emphasis remains **3.1.3** / Phase 3 primary—Phase 4 lanes **reflect**, do not re-classify overwrite semantics.

## Edge cases

- **Lane skew:** narrative refreshes faster than render budget allows—must remain **honest** under **3.2.2** **display_lag_disclosed** vs **semantic_drift_bounded** (NL contract; execution tuning deferred).
- **Mode switch mid-emphasis:** camera/interpolator transitions must not **invent** checkpoint eligibility (**3.1.4**).
- **Orthographic + seam bundles:** large-tabletop orthographic views still **consume** the same **SeamId** rows—no alternate durability semantics.

## Open questions

- Whether **narrative** lane maintains a **separate coalescing clock** than **rendering** for the same channel id (**D-3.4-narrative-rendering-split** bundle policy).
- Minimum **emphasis** vocabulary shared across lanes (execution-deferred wire enums).

## Pseudo-code readiness

At **secondary** depth, **interfaces + algorithm sketches** for **lane adapters** may appear in **4.1.1+** tertiaries; **no** full pseudo-code requirement at **4.1** secondary container.

## Secondary slice GWT (**GWT-4.1-A–K**) — evidence narrows at tertiaries

| ID | Given | When | Then | Evidence (planned / upstream) |
| --- | --- | --- | --- | --- |
| **GWT-4.1-A** | **3.4.1** **SeamId** row resolved | Lane consumes export | Both lanes cite **same** seam semantics | [[Phase-3-4-1-Handoff-Seam-Catalog-and-Consumer-Contract-Rows-Roadmap-2026-04-03-0115]] |
| **GWT-4.1-B** | **3.2.1** **ObservationChannel** + **authority_class** | Lane subscribes | **preview_shadow** cannot author persistence claims | **3.2** rollup + **3.2.1** |
| **GWT-4.1-C** | **3.2.2** freshness/drift class | Frame/tick presented | Policy class explicit per lane | **3.2.2** |
| **GWT-4.1-D** | **3.1.4** checkpoint boundary | Lane renders “save-adjacent” UX | No fake checkpoint eligibility | **3.1.4** |
| **GWT-4.1-E** | **3.1.3** overwrite class | DM action observed | Emphasis reflects **live** vs **structural** story | **3.1.3** |
| **GWT-4.1-F** | Phase 4 **mode graph** | Mode switch | Interpolator handoff preserves lane subscriptions | Primary § Behavior |
| **GWT-4.1-G** | **D-3.4-narrative-rendering-split** | Bundle policy chosen | Two lanes, **one** sim truth | [[decisions-log]] |
| **GWT-4.1-H** | **D-3.4-phase4-consumer-granularity** | Export cadence chosen | Decision row exists—execution closure deferred | [[decisions-log]] |
| **GWT-4.1-I** | Narrative lane coalescing | High-frequency sim events | No silent drop—staleness/disclosure policy | **3.2.2** + § Edge cases |
| **GWT-4.1-J** | Rendering lane budget (execution-deferred perf) | Frame budget stress | Degradation path does not reinterpret **SeamId** semantics—stall/disclose per **3.2.2** drift classes; GPU policy **out of scope** for conceptual slice | [[Phase-3-2-2-Freshness-Drift-Policy-Classes-Roadmap-2026-04-02-2350]] § Edge cases; [[roadmap-state]] § Conceptual track waiver |
| **GWT-4.1-K** | Dual-track conceptual waiver (rollup / CI advisory) | Validator surfaces execution-only codes | **Not** blocking conceptual completion when deferrals explicit | [[roadmap-state]] § Conceptual track waiver; [[distilled-core]] § Conceptual track waiver |

## Research integration

- None for this slice (vault-first pattern); external benchmarks deferred.

## Tertiary notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/sandbox-genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-1-Narrative-Rendering-and-Consumer-Surface-Lanes"
WHERE roadmap-level = "secondary" OR roadmap-level = "tertiary" OR roadmap-level = "task"
SORT subphase-index ASC, file.name ASC
```
