---
title: Phase 4.1.2 — Cross-lane coherence and emphasis reconciliation
roadmap-level: tertiary
phase-number: 4
subphase-index: "4.1.2"
project-id: genesis-mythos-master
status: active
priority: high
progress: 58
handoff_readiness: 86
created: 2026-03-30
tags:
  - roadmap
  - genesis-mythos-master
  - phase-4
para-type: Project
links:
  - "[[Phase-4-1-Narrative-Rendering-and-Consumer-Surface-Lanes-Roadmap-2026-04-03-2015]]"
  - "[[Phase-4-1-1-Lane-Adapters-Emphasis-and-GWT-Narrowing-Roadmap-2026-04-03-2016]]"
  - "[[Phase-4-Perspective-Split-and-Control-Systems-Roadmap-2026-03-30-0430]]"
  - "[[Phase-3-4-1-Handoff-Seam-Catalog-and-Consumer-Contract-Rows-Roadmap-2026-04-03-0115]]"
  - "[[Phase-3-2-2-Freshness-Drift-Policy-Classes-Roadmap-2026-04-02-2350]]"
  - "[[decisions-log]]"
---

> [!note] #handoff-review
> `handoff_readiness: 86` — tertiary **4.1.2** — **cross-lane coherence** when **Narrative/UI** vs **Rendering** **emphasis** diverges under **mode graph** / **interpolator** transitions; **reconciliation** preserves **4.1.1** resolution order (**SeamId** → **ObservationChannel** → **freshness/drift**) and **one** sim truth; **GWT-4.1.2-A–K** narrows **GWT-4.1.1-*** for this slice. Next structural cursor **4.1.3** (continue **4.1** chain).

## Phase 4.1.2 — Cross-lane coherence and emphasis reconciliation

This **tertiary** extends **4.1.1** by naming **what must stay aligned** when the two consumer lanes **choose different emphasis kinds** or **coalescing aggressiveness** at the same tick/frame boundary: **cross-lane coherence** (no contradictory “what is primary” claims for the same **SeamId**-keyed fact) and **emphasis reconciliation** — deterministic rules for **which lane’s presentation projection wins in operator-visible comparisons** without elevating **preview_shadow** to **committed_session** or inventing checkpoint eligibility (**3.1.4**).

## Scope

**In scope:**

- **Coherence predicate (NL)** — for a fixed **sim tick** (or **frame-aligned** slice per **3.2.2**), both lanes **agree** on: (a) **SeamId** row identity from **3.4.1**, (b) subscribed **ObservationChannel** ids, (c) **authority_class** legibility (**3.2.1**). Divergence is allowed only in **emphasis rank** and **coalescing_policy_hook** behavior, not in **merge/checkpoint/overwrite** semantics (**3.1.3** / **3.1.4**).
- **Reconciliation order (NL)** — when narrative **emphasis** and rendering **emphasis** conflict on **which channel id is “foregrounded”**, **reconcile** using: **(1)** shared **mode graph** legality from Phase 4 primary (**4**), **(2)** **interpolator-fed** transition state (no new sim facts), **(3)** **tie-break**: **narrative** may carry **story-critical** emphasis only if **rendering** still receives **non-drop** contract per **3.2.2** **display_lag_disclosed** / **semantic_drift_bounded** (execution tuning deferred).
- **Subscription parity** — both lanes remain **subscribers** to the same upstream exports; reconciliation **does not** drop a **Rendering** subscription because **Narrative** elevated a channel (and vice versa) unless **3.2.2** drift policy explicitly allows **degraded** presentation (**execution-deferred** wire).

**Out of scope:**

- Pixel/UI layout, font metrics, GPU frame pacing (**execution-deferred**).
- Resolving **D-3.4-narrative-rendering-split** bundle policy (**execution-deferred**; remains in [[decisions-log]]).
- Netcode or replication (**conceptual waiver**).

## Behavior (natural language)

1. **Coherence check:** Before presenting, each lane evaluates **LaneAdapter** (**4.1.1**) + current **emphasis** projection; if the **same** **ObservationChannel** id is **top-ranked** in both lanes, **no reconciliation** — coherence holds.
2. **Divergent emphasis:** When **top-ranked** channel ids **differ**, lanes still **must not** assert conflicting **durability** or **checkpoint** stories — reconciliation is **presentation-only** and **must** surface **3.2.2** disclosure when operators compare lanes (**display_lag_disclosed** vs **semantic_drift_bounded**).
3. **Mode / interpolator transition:** On **camera** or **perspective mode** change (**4** primary), **freeze-then-update** emphasis: **subscriptions** stable per **4.1.1** § Behavior (3); **emphasis kinds** update only after **interpolator** reports **stable** handoff (NL contract; execution event order deferred).

## Interfaces

**Parent:**

- [[Phase-4-1-Narrative-Rendering-and-Consumer-Surface-Lanes-Roadmap-2026-04-03-2015]] — dual lanes + **GWT-4.1-A–K**.
- [[Phase-4-1-1-Lane-Adapters-Emphasis-and-GWT-Narrowing-Roadmap-2026-04-03-2016]] — adapters + **GWT-4.1.1-A–K**.

**Upstream:**

- [[Phase-3-4-1-Handoff-Seam-Catalog-and-Consumer-Contract-Rows-Roadmap-2026-04-03-0115]] — **SeamId** rows.
- [[Phase-3-2-2-Freshness-Drift-Policy-Classes-Roadmap-2026-04-02-2350]] — disclosure vs drift classes.

**Phase 4 primary:**

- [[Phase-4-Perspective-Split-and-Control-Systems-Roadmap-2026-03-30-0430]] — mode graph + camera/interpolator.

## Edge cases

- **Rapid mode flip:** emphasis reconciliation **must not** skip **coherence predicate** between frames — worst case: hold prior emphasis one frame with **explicit stale disclosure** (**3.2.2**).
- **Orthographic tabletop vs narrative close-up:** **orthographic_tabletop_scope** vs **narrative_priority** may both be legal — reconciliation ties to **mode graph** + **interpolator** stability, not to a second **SeamId** bundle.

## Open questions

- Minimum **operator-visible** “compare lanes” affordance for coherence failures (**execution-deferred** UX).
- Whether **forge-sourced preview defaults** (**D-3.1.5-forge-sourced-preview-default**) participate in **tie-break** at reconciliation layer — **execution-deferred**.

## Pseudo-code readiness

**Mid-technical:** structured bullets for **coherence predicate** + **reconciliation order**; executable pseudo-code optional at **4.1.3** if chain escalates.

## Tertiary slice GWT — narrowed vs **GWT-4.1.1-A–K**

| Narrow ID | Parent GWT | Given | When | Then | Evidence (this slice) |
| --- | --- | --- | --- | --- | --- |
| **GWT-4.1.2-A** | **GWT-4.1.1-A** | **SeamId** resolved | Lanes disagree on emphasis rank | Still same row + channel ids; coherence on authority | § Behavior (1)(2) |
| **GWT-4.1.2-B** | **GWT-4.1.1-B** | **preview_shadow** | Reconciliation applied | Never promoted to durable | § Scope + **3.2.1** |
| **GWT-4.1.2-C** | **GWT-4.1.1-C** | **3.2.2** classes | Lanes compared | Disclosure explicit | § Behavior (2) |
| **GWT-4.1.2-D** | **GWT-4.1.1-D** | Checkpoint UX | Cross-lane copy | No fake checkpoint | § Scope |
| **GWT-4.1.2-E** | **GWT-4.1.1-E** | DM overwrite | Emphasis diverges | Still **live** vs **structural** story | § Behavior (2) |
| **GWT-4.1.2-F** | **GWT-4.1.1-F** | Mode switch | Interpolator handoff | Subscriptions stable; emphasis updates after stable handoff | § Behavior (3) |
| **GWT-4.1.2-G** | **GWT-4.1.1-G** | **D-3.4-narrative-rendering-split** | Bundle policy TBD | Coherence + reconciliation do not invent bundle split | [[decisions-log]] |
| **GWT-4.1.2-H** | **GWT-4.1.1-H** | **D-3.4-phase4-consumer-granularity** | Cadence TBD | No semantic change | [[decisions-log]] |
| **GWT-4.1.2-I** | **GWT-4.1.1-I** | High-frequency events | Narrative vs render coalescing | **3.2.2** disclosure if skewed | § Edge cases |
| **GWT-4.1.2-J** | **GWT-4.1.1-J** | Render budget stress | Reconciliation under load | **SeamId** semantics unchanged | § Scope |
| **GWT-4.1.2-K** | **GWT-4.1.1-K** | Execution-only validator codes | Advisory | Conceptual waiver | [[roadmap-state]] |

## Research integration

- None (vault-first pattern).

## Tertiary notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-1-Narrative-Rendering-and-Consumer-Surface-Lanes"
WHERE roadmap-level = "secondary" OR roadmap-level = "tertiary" OR roadmap-level = "task"
SORT subphase-index ASC, file.name ASC
```
