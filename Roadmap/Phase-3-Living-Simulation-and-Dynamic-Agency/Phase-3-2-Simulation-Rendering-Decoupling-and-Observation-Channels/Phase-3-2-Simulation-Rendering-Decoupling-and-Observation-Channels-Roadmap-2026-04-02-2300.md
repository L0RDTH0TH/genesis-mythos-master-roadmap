---
title: Phase 3.2 — Simulation / rendering decoupling + observation channels
roadmap-level: secondary
phase-number: 3
subphase-index: "3.2"
project-id: sandbox-genesis-mythos-master
status: active
priority: high
progress: 72
handoff_readiness: 86
created: 2026-04-02
tags:
  - roadmap
  - sandbox-genesis-mythos-master
  - phase-3
para-type: Project
links:
  - "[[Phase-3-Living-Simulation-and-Dynamic-Agency-Roadmap-2026-03-30-0430]]"
  - "[[Phase-3-1-Sim-Tick-and-Event-Bus-Spine-Roadmap-2026-03-30-2213]]"
  - "[[decisions-log]]"
  - "[[Phase-3-2-3-UX-D3-1-5-Binding-Surfaces-Roadmap-2026-03-30-2319]]"
  - "[[Conceptual-Decision-Records/deepen-phase-3-2-secondary-rollup-nl-gwt-2026-04-02-2355]]"
---

> [!note] #handoff-review
> `handoff_readiness: 86` — secondary **3.2 rollup** — **tertiary chain 3.2.1–3.2.3** complete; **NL checklist** + **GWT parity** (**GWT-3.2-A**–**K**) reconciled vs **3.2** open questions. **Observation freshness** closed at conceptual depth via **3.2.2** policy classes; wire-up / perf **execution-deferred**. **D-3.1.5-*** rows ([[decisions-log]]) remain **execution-deferred** (NL loci + UX binding surfaces in **3.2.3**; no operator picks). `GMM-2.4.5-*` **reference-only**. **Next structural cursor:** mint **Phase 3 secondary 3.3** — vitality / consequence / persistence cohesion (align Phase 3 primary checklist). Resolver: `gate_signature: structural-continue-phase-3-2-secondary` \| queue: `followup-deepen-phase3-32-rollup-gmm-20260402T235200Z`.

## Phase 3.2 — Simulation / rendering decoupling and observation channels

This **secondary 3.2** slice names how **rendering and operator tooling** consume **simulation state** without mutating the **authoritative tick kernel**, and how **preview / shadow / spectate** lanes stay **non-authoritative** relative to **persistence + bus publish** rules already anchored in **3.1.x**. It **does not** re-derive **3.1** ordering, merge policy, or checkpoint semantics—it **references** them and adds the **cross-cutting observation + preview** contract.

## Scope

**In scope:**

- **Observation channels** — read-only **snapshots** and **stream selectors** (what may be observed, at what cadence) distinct from **mutation** paths; alignment with Phase 3 primary “simulation vs rendering separation”.
- **Preview vs committed session boundary** — which lanes may **emit** sim-visible facts for UX (**preview** / **forge suggestion**) vs which paths require **WorkItem** admission per **3.1.5** and **3.1.2** merge matrix (NL only).
- **Carry-forward from D-3.1.5-*:** **Faction cohort lane vs shard** and **forge-sourced preview default** remain **execution-deferred**; **3.2.3** states **where** they bind as UX / NL loci; **decisions-log** rows **D-3.1.5-*** are **not** closed at conceptual depth.

**Out of scope:**

- Concrete render graph, GPU frame pacing, or netcode (execution-deferred).
- Changing **3.1** bus total-order or checkpoint authority (upstream).

## Behavior (natural language)

1. **Observation:** Rendering and narrative layers **subscribe** to **observation channels** derived from post-tick **SimEvent** streams and **checkpoint-visible** state; they **never** apply **DM overwrite** or **agency** mutations directly—those remain **kernel-side** per **3.1** story.
2. **Preview lanes:** **Preview** / **shadow** runs may **display** counterfactual or suggested state but **must not** publish **authoritative** bus events or **persistence checkpoints** unless they pass the same **commit boundary** story as Phase **2.7.3** / **3.1.4** (re-affirmed at NL).
3. **D-3.1.5 carry:** Open questions on **faction cohort lane vs shard** and **forge-sourced preview default** are **tracked** under [[decisions-log]] and referenced in **Open questions** below—resolution **execution-deferred**; **3.2.3** provides **binding surfaces** without closing wire formats.

## Interfaces

**Upstream (3.1 chain):**

- **3.1.1–3.1.5** — bus ordering, scheduling, classification, checkpoints, agency/work admission — [[Phase-3-1-Sim-Tick-and-Event-Bus-Spine-Roadmap-2026-03-30-2213]] and tertiaries **3.1.1**–**3.1.5**.

**Parent (Phase 3 primary):**

- [[Phase-3-Living-Simulation-and-Dynamic-Agency-Roadmap-2026-03-30-0430]] — sim vs render decoupling + DM overwrite semantics.

**Downstream (3.2.1–3.2.3 + rollup):**

- **3.2.1** — [[Phase-3-2-1-Observation-Channel-Taxonomy-Roadmap-2026-03-30-2310]] — **observation channel taxonomy** vs **3.1.1** lanes + **preview_shadow** / committed boundary (`handoff_readiness` **85**).
- **3.2.2** — [[Phase-3-2-2-Freshness-Drift-Policy-Classes-Roadmap-2026-04-02-2350]] — **freshness** (**tick_aligned** vs **frame_aligned**) + **drift** (**semantic_drift_bounded** vs **display_lag_disclosed**) policy classes on **3.2.1** **ObservationChannel** (`handoff_readiness` **85**).
- **3.2.3** — [[Phase-3-2-3-UX-D3-1-5-Binding-Surfaces-Roadmap-2026-03-30-2319]] — **UX binding surfaces** + **D-3.1.5-*** NL loci (`handoff_readiness` **85**).
- **Rollup (this note):** secondary **3.2** **NL closure** + **GWT parity** table **GWT-3.2-A**–**K**; CDR [[Conceptual-Decision-Records/deepen-phase-3-2-secondary-rollup-nl-gwt-2026-04-02-2355]].
- **Next:** mint **Phase 3 secondary 3.3** — see [[workflow_state]] **`current_subphase_index`** and Phase 3 primary **vitality / consequence** glue row.

**Outward guarantees:**

- **Non-authoritative preview** cannot advance **tick index**, **checkpoint sequence**, or **authoritative SimEvent** publish without explicit **admission** per **3.1.5** / **3.1.2**.

## Edge cases

- **Operator tool mismatch:** a UI that bypasses **observation** and pokes **world** directly → classed as **DM overwrite** per **3.1.3** mapping; if structural → **regen request**, not a rendering concern.
- **Stale observation:** renderers may show **slightly stale** snapshots; **authoritative** timelines remain **tick-ordered** — **3.2.2** names **freshness_class** / **drift_class**; perf tuning **execution-deferred**.

## Secondary 3.2 rollup (NL checklist + GWT parity)

**NL checklist (secondary depth):**

- [x] Scope / Behavior / Interfaces / Edge cases / Open questions coherent with **3.1.x** upstream and Phase 3 primary.
- [x] **Tertiary chain 3.2.1–3.2.3** complete — taxonomy (**3.2.1**), freshness/drift (**3.2.2**), UX + **D-3.1.5** loci (**3.2.3**).
- [x] **GWT parity:** **GWT-3.2-A**–**K** trace **3.2.1** / **3.2.2** / **3.2.3** coverage on this secondary surface (rollup rows **C–K**).
- [x] **D-3.1.5-*** — **execution-deferred** per [[decisions-log]]; prose does **not** treat them as conceptual hard gates.

**GWT parity mapping (tertiary → rows):**

| Tertiary | GWT rows |
| --- | --- |
| 3.2.1 | GWT-3.2-C — GWT-3.2-E |
| 3.2.2 | GWT-3.2-F — GWT-3.2-H |
| 3.2.3 | GWT-3.2-I — GWT-3.2-K |

## Open questions

- **Observation freshness** — **conceptually closed** at this rollup: **3.2.2** [[Phase-3-2-2-Freshness-Drift-Policy-Classes-Roadmap-2026-04-02-2350]] owns **tick_aligned** vs **frame_aligned** + drift classes; **wire-up, perf budgets, and UX defaults** remain **execution-deferred** (dual-track waiver).
- **D-3.1.5-faction-cohort-lane-vs-shard** — **execution-deferred**; NL loci in **3.2.3**; authoritative row [[decisions-log]] **D-3.1.5-faction-cohort-lane-vs-shard**.
- **D-3.1.5-forge-sourced-preview-default** — **execution-deferred**; ties **3.1.3** `preview_shadow`; **3.2.3** binding surfaces; [[decisions-log]] **D-3.1.5-forge-sourced-preview-default**.

## Pseudo-code readiness

At **secondary** conceptual depth, **no pseudo-code** is required. **Interface sketches** and **channel matrices** live in **3.2.1–3.2.3** tertiaries.

## GWT (Given / When / Then) — secondary prose

| ID | Given | When | Then |
| --- | --- | --- | --- |
| GWT-3.2-A | A **preview** lane displays suggested state | User accepts suggestion | Admission follows **3.1.5** WorkItem path — not silent kernel mutation |
| GWT-3.2-B | A **committed** session tick closes | Renderer observes | Observation reflects **checkpoint-eligible** facts per **3.1.4** — no duplicate authority |
| GWT-3.2-C | An **ObservationChannel** is defined per **3.2.1** | Subscription resolves against **3.1.1** `(lane, subscription_pattern)` | Channel carries **authority_class** **committed_session** \| **preview_shadow** consistent with **3.1.3** / **3.1.4** |
| GWT-3.2-D | Channel is **preview_shadow** | Operator invokes preview UX | No authoritative **SimEvent** publish or durability checkpoint without **3.1.5** admission |
| GWT-3.2-E | Multiple channels target the same **3.1.1** lane | Selector chooses observation stream | **3.2.1** taxonomy prevents ambiguous merge of **committed** vs **preview** facts |
| GWT-3.2-F | **freshness_class** is **tick_aligned** | Tick **k** closes | Observation cadence aligns to **3.1.2** tick closure — no fake “between-tick” authority |
| GWT-3.2-G | **freshness_class** is **frame_aligned** | Frame presents UI | Display may lead tick; **drift_class** (**display_lag_disclosed**) makes lag legible per **3.2.2** |
| GWT-3.2-H | **drift_class** is **semantic_drift_bounded** | Drift exceeds bound | UI surfaces disclosure / resync path — **execution** implements thresholds |
| GWT-3.2-I | Operator panel binds to **ObservationChannel** + **freshness**/**drift** | Panel renders **D-3.1.5** locus (cohort vs shard) | Legible **NL** surface only — **execution-deferred** wire format |
| GWT-3.2-J | Forge-sourced suggestion path is shown | Default path is preview | Matches **D-3.1.5-forge-sourced-preview-default** deferral — **3.1.3** `preview_shadow` preserved |
| GWT-3.2-K | **3.2.3** UX row references **3.2.1** + **3.2.2** | Operator drills down | Trace lands on **3.1.x** authority — no new kernel mutation seam |

## Risk register v1

| Risk | Mitigation | Owner / defer |
| --- | --- | --- |
| Preview lane leaks authoritative writes | **GWT-3.2-A/D** + **3.2.1** `authority_class` + **3.1.5** WorkItem | Closed at conceptual rollup |
| Stale observation misread as truth | **3.2.2** **freshness_class** / **drift_class** + **GWT-3.2-F–H** | Perf tuning **execution-deferred** |
| D-3.1.5-* cohorts / forge default unresolved | **3.2.3** binding surfaces + [[decisions-log]] rows; **not** closed without operator pick | **execution-deferred** |

## Tertiary notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/sandbox-genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-2-Simulation-Rendering-Decoupling-and-Observation-Channels"
WHERE roadmap-level = "secondary" OR roadmap-level = "tertiary" OR roadmap-level = "task"
SORT subphase-index ASC, file.name ASC
```
