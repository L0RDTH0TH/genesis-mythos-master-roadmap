---
title: Phase 4.1.3 — Consumer-surface framing, presentation-time validation, and operator legibility
roadmap-level: tertiary
phase-number: 4
subphase-index: "4.1.3"
project-id: godot-genesis-mythos-master
status: active
priority: high
progress: 62
handoff_readiness: 87
created: 2026-04-03
tags:
  - roadmap
  - godot-genesis-mythos-master
  - phase-4
para-type: Project
links:
  - "[[Phase-4-1-Narrative-Rendering-and-Consumer-Surface-Lanes-Roadmap-2026-04-03-2015]]"
  - "[[Phase-4-1-2-Cross-Lane-Coherence-and-Emphasis-Reconciliation-Roadmap-2026-03-30-1200]]"
  - "[[Phase-4-1-1-Lane-Adapters-Emphasis-and-GWT-Narrowing-Roadmap-2026-04-03-2016]]"
  - "[[Phase-4-Perspective-Split-and-Control-Systems-Roadmap-2026-03-30-0430]]"
  - "[[Phase-3-4-1-Handoff-Seam-Catalog-and-Consumer-Contract-Rows-Roadmap-2026-04-03-0115]]"
  - "[[Phase-3-2-1-Observation-Channel-Taxonomy-Roadmap-2026-03-30-2310]]"
  - "[[decisions-log]]"
---

> [!note] #handoff-review
> `handoff_readiness: 87` — tertiary **4.1.3** — **consumer-surface framing** (presentation envelope per lane), **presentation-time validation** (legibility vs upstream facts — **not** PreCommit / Phase **2.3** gates), and **operator legibility** for compare-lanes; **GWT-4.1.3-A–K** narrows **GWT-4.1.2-*** for this slice. **Tertiary chain 4.1.1–4.1.3** structurally complete under secondary **4.1**; next structural cursor **4.1** (secondary **4.1 rollup** — NL + **GWT-4.1** parity vs **4.1.1–4.1.3**).

## Phase 4.1.3 — Consumer-surface framing, presentation-time validation, and operator legibility

This **tertiary** closes the **4.1** tertiary chain (with **4.1.1** adapters + **4.1.2** coherence/reconciliation) by naming how **operator-visible surfaces** wrap subscribed **ObservationChannel** facts: each lane emits a **presentation envelope**—a bounded NL contract listing **SeamId** provenance, **authority_class** (**3.2.1**), **freshness/drift** class (**3.2.2**), **emphasis** projection (**4.1.1**), and **reconciliation** outcome when applicable (**4.1.2**). **Presentation-time validation** means **read-only** checks that the envelope is **internally consistent** and **honest** vs the lane’s subscriptions; it **does not** re-run **Phase 2** **PreCommitVerificationBundle** semantics or invent new **checkpoint** or **merge** authority (**3.1.4**). **Operator legibility** requires that side-by-side lane views (when operators compare narrative vs rendering) surface **explicit** **3.2.2** disclosure when skew exists—without elevating **preview_shadow** to **committed_session**.

## Scope

**In scope:**

- **Presentation envelope (NL)** — minimum fields carried with any consumer-visible bundle: **SeamId** (from **3.4.1**), subscribed **ObservationChannel** ids, **authority_class**, **freshness_class** / **drift_class**, **emphasis_kind** + rank (from **4.1.1**), optional **reconciliation_tag** when **4.1.2** tie-break applied.
- **Presentation-time validation (NL)** — predicates that reject **impossible** combinations (e.g., envelope claims **committed_session** while subscription set only allows **preview_shadow** for that channel) and **missing disclosure** when **4.1.2** coherence predicate would fail—**presentation-only** failure modes; **no** new sim-side gates.
- **Operator legibility** — compare-lanes affordance at NL: both envelopes visible for the same tick/frame slice must be **diffable** on **SeamId** + **authority** + **drift disclosure**; execution UX layout deferred.

**Out of scope:**

- Implementing UI panels, diff widgets, or accessibility (**execution-deferred**).
- Extending **Phase 2.3** V-* gates into Phase 4 presentation (**forbidden** authority merge).
- **D-3.4-narrative-rendering-split** bundle policy closure (**execution-deferred**; remains in [[decisions-log]]).

## Behavior (natural language)

1. **Envelope assembly:** After **LaneAdapter** resolution (**4.1.1**) and optional **reconciliation** (**4.1.2**), the lane builds a **PresentationEnvelope** record (NL struct) attached to each operator-visible export batch.
2. **Presentation-time validation:** Before paint/narration commit at the consumer boundary, run **envelope self-check** + **subscription parity check** vs **3.4.1** row + **3.2.1** authority—fail closed to **withhold or degrade** presentation with **3.2.2** disclosure (not silent sim mutation).
3. **Compare-lanes:** When both lanes present the same **SeamId**-keyed fact, operator-visible comparison **must** show **matching** authority + drift story or **explicit** mismatch disclosure (already required by **4.1.2** § Behavior (2)).

## Interfaces

**Parent:**

- [[Phase-4-1-Narrative-Rendering-and-Consumer-Surface-Lanes-Roadmap-2026-04-03-2015]] — dual lanes + **GWT-4.1-A–K**.
- [[Phase-4-1-2-Cross-Lane-Coherence-and-Emphasis-Reconciliation-Roadmap-2026-03-30-1200]] — coherence + reconciliation.
- [[Phase-4-1-1-Lane-Adapters-Emphasis-and-GWT-Narrowing-Roadmap-2026-04-03-2016]] — adapters + emphasis.

**Upstream:**

- [[Phase-3-4-1-Handoff-Seam-Catalog-and-Consumer-Contract-Rows-Roadmap-2026-04-03-0115]] — **SeamId** rows.
- [[Phase-3-2-1-Observation-Channel-Taxonomy-Roadmap-2026-03-30-2310]] — **authority_class**.

**Cross-phase (non-authoritative):**

- Phase **2.3** **PreCommitVerificationBundle** — **not** invoked by presentation-time validation; referenced only to **forbid** accidental re-use of commit gates as display checks.

## Edge cases

- **Envelope too large for frame budget:** degrade **emphasis** or **coalescing** per lane policy (**4.1.1**)—**not** **SeamId** semantics; **3.2.2** disclosure applies.
- **Forge-sourced preview defaults (**D-3.1.5-forge-sourced-preview-default**):** envelope **must** label forge-default provenance without implying **committed_session** (**execution-deferred** bind).

## Open questions

- Whether **presentation-time validation** failures should emit a **distinct operator-facing code** from **4.1.2** coherence failures (**execution-deferred** taxonomy).

## Pseudo-code readiness

**Mid-technical:** structured bullet schema for **PresentationEnvelope** + validation predicates; optional executable pseudo-code stub for operator tooling (**execution-deferred**).

## Tertiary slice GWT — narrowed vs **GWT-4.1.2-A–K**

| Narrow ID | Parent GWT | Given | When | Then | Evidence (this slice) |
| --- | --- | --- | --- | --- | --- |
| **GWT-4.1.3-A** | **GWT-4.1.2-A** | **SeamId** resolved | Envelope built | Same row + channel ids as coherence | § Behavior (1) |
| **GWT-4.1.3-B** | **GWT-4.1.2-B** | **preview_shadow** | Envelope validated | Never labeled committed | § Scope |
| **GWT-4.1.3-C** | **GWT-4.1.2-C** | **3.2.2** classes | Compare lanes | Disclosure explicit | § Behavior (3) |
| **GWT-4.1.3-D** | **GWT-4.1.2-D** | Checkpoint UX | Presentation-time check | No PreCommit gate smuggle | § Scope + Interfaces |
| **GWT-4.1.3-E** | **GWT-4.1.2-E** | DM overwrite | Envelope | Emphasis reflects **live** vs **structural** | § Behavior (1) |
| **GWT-4.1.3-F** | **GWT-4.1.2-F** | Mode switch | Envelope after interpolator | Stable subscriptions per **4.1.2** | § Behavior (1) |
| **GWT-4.1.3-G** | **GWT-4.1.2-G** | **D-3.4-narrative-rendering-split** | Bundle policy TBD | Envelope does not invent split | [[decisions-log]] |
| **GWT-4.1.3-H** | **GWT-4.1.2-H** | **D-3.4-phase4-consumer-granularity** | Cadence TBD | No semantic change | [[decisions-log]] |
| **GWT-4.1.3-I** | **GWT-4.1.2-I** | High-frequency events | Envelope batching | **3.2.2** on skew | § Edge cases |
| **GWT-4.1.3-J** | **GWT-4.1.2-J** | Render budget stress | Validation under load | **SeamId** semantics unchanged | § Edge cases |
| **GWT-4.1.3-K** | **GWT-4.1.2-K** | Execution-only validator codes | Advisory | Conceptual waiver | [[roadmap-state]] |

## Research integration

- None (vault-first pattern).

## Tertiary notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/godot-genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-1-Narrative-Rendering-and-Consumer-Surface-Lanes"
WHERE roadmap-level = "secondary" OR roadmap-level = "tertiary" OR roadmap-level = "task"
SORT subphase-index ASC, file.name ASC
```
