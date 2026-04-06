---
title: Phase 6.1.3 — ObservationChannel lane readout + presentation-time co-display (NL)
roadmap-level: tertiary
phase-number: 6
subphase-index: "6.1.3"
project-id: godot-genesis-mythos-master
status: complete
priority: high
progress: 100
handoff_readiness: 88
created: 2026-04-07
tags:
  - roadmap
  - godot-genesis-mythos-master
  - phase-6
para-type: Project
links:
  - "[[Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle-Roadmap-2026-04-06-1200]]"
  - "[[Phase-6-1-2-Bounded-Tick-Window-Scenarios-and-Sim-Visible-Classification-Matrix-Roadmap-2026-04-06-1215]]"
  - "[[Branches/phase-6-operator-rollback-20260405/Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle/Phase-6-1-1-Manifest-Admission-Row-Bindings-and-Admission-Ticket-Vocabulary-Roadmap-2026-04-05-1918]]"
  - "[[Phase-3-2-1-Observation-Channel-Taxonomy-Roadmap-2026-03-30-2310]]"
  - "[[Phase-4-1-3-Consumer-Surface-Framing-and-Presentation-Time-Validation-Roadmap-2026-04-03-2110]]"
  - "[[Phase-6-Prototype-Assembly-Testing-and-Iteration-Roadmap-2026-03-30-0430]]"
  - "[[decisions-log]]"
  - "[[workflow_state]]"
---

## Phase 6.1.3 — ObservationChannel lane readout + presentation-time co-display

> [!note] Active-tree remint (godot operator queue)
> This note **re-mints** tertiary **6.1.3** on the **post-rollback active tree**, scoped to [[Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle-Roadmap-2026-04-06-1200]] (secondary **6.1** remint **2026-04-06**) and aligned to active **6.1.2** [[Phase-6-1-2-Bounded-Tick-Window-Scenarios-and-Sim-Visible-Classification-Matrix-Roadmap-2026-04-06-1215]]. Prior **pre-rollback** copy for diff: [[Branches/phase-6-operator-rollback-20260405/Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle/Phase-6-1-3-ObservationChannel-Lane-Readout-and-Presentation-Time-Co-Display-Roadmap-2026-04-06-2130]]. **Out-of-order history:** operator queue `pool-remint-613-godot-gmm-20260406120002Z` closed **6.1.3** readout before tertiary **6.1.1** field-registry mint; **6.1.1** is now on the active tree — [[Phase-6-1-1-Manifest-Field-Registry-FeedbackRecord-and-Instrumentation-Envelope-Roadmap-2026-04-07-1245]] (queue `followup-deepen-phase611-after-pool-remint-613-20260407T123000Z`).

This tertiary **implements [[Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle-Roadmap-2026-04-06-1200]] § Manifest — Operator readout (ObservationChannel + 4.1.3 co-display)** for **Horizon-Q3** (`slice_id: horizon_q3_v1`): it binds **3.2.1** **ObservationChannel** identities to **4.1.3** **PresentationEnvelope** minimum fields and **presentation-time validation** predicates—**read-only** at the consumer boundary—so **GWT-6-C** evidence cites **one lane/readout matrix** without re-deriving **3.x** bus semantics or **4.1.x** lane adapter truth.

## Scope

**In scope (conceptual):**

- **Operator readout row catalog** — stable **`slice_operator_readout_id`** rows describing **which ObservationChannel subscriptions** appear together on an operator-facing **co-display card** for a given **`slice_tick_window_scenario_id`** (**6.1.2**).
- **Channel → envelope field binding** — for each readout row, list **required PresentationEnvelope fields** (**4.1.3** § Scope): **SeamId**, subscribed channel ids, **authority_class**, **freshness_class** / **drift_class**, **emphasis_kind** + rank, optional **reconciliation_tag**—**labels and join keys only**.
- **Presentation-time validation echo** — each row states which **4.1.3** § Behavior predicates apply (**envelope self-check**, **subscription parity** vs **3.2.1**, **withhold/degrade + 3.2.2 disclosure**) as **obligations**, not new gates.

**Out of scope:** UI implementation, Dataview bodies, `Roadmap/Execution/**`, extending **2.3** PreCommit bundles, changing **3.2.1** / **4.1.3** authoritative definitions.

## Behavior (natural language)

1. **Scenario-scoped readout:** Operators cite **`slice_operator_readout_id`** when they mean a **slice-local co-display** tied to a **`stws.hq3.*`** window from **6.1.2**; changing **3.x** or **4.x** truth still happens in upstream notes—this slice **composes** pins only.
2. **Authority honesty:** Readout rows **forbid** presenting **preview_shadow**-only channel sets with envelopes labeled **committed_session**—parity language mirrors **4.1.3** § Behavior (2) without adding sim-side enforcement.
3. **Co-display diffability:** When two readout rows share a **slice_tick_window_scenario_id** but target **different lane projections**, operator-visible comparison must remain **diffable** on **SeamId** + **authority_class** + **drift disclosure** per **4.1.3** § Behavior (3).

## Interfaces

**Upstream (secondary 6.1):** Consumes **Manifest — Operator readout** pins and **GWT-6 → 6.1** row **GWT-6-C**; does not widen **InstrumentationIntent** bundle rows (**6.1** owns `ii.presentation.envelope` / `ii.rules.eval_frame` declarations—**6.1.3** may cite them as alignment text only).

**Upstream (6.1.2):** **`slice_tick_window_scenario_id`** values are **join keys**—every readout row references ≥1 **`stws.hq3.*`** id.

**Upstream (3.2.1):** **ObservationChannel** taxonomy + **authority_class** — read-only.

**Upstream (4.1.3):** **PresentationEnvelope** + **presentation-time validation** — read-only.

**Downstream (rollup / 6.1+):** Secondary **6.1 rollup** closes **GWT-6.1** parity vs **6.1.1–6.1.3**; **6.1.4+** (if ever) must not silently drop readout rows without manifest pin update.

**Outward guarantees:**

- **No second consumer truth:** Envelope field bindings **reference** **4.1.3**; they do not define alternate presentation semantics.
- **Traceability:** Every catalog row + matrix row lists a **non-bypass** wikilink + explicit heading anchor (same style as **6.1.2** **GWT-6.1.2-G**).

## Operator readout row catalog (Horizon-Q3)

| slice_operator_readout_id | Human label (NL) | Join (`slice_tick_window_scenario_id`) | Subscribed ObservationChannel pattern (NL) | Primary anchors |
| --- | --- | --- | --- | --- |
| `sor.hq3.admit_closure_dual_lane` | **Co-display** for first closure window — narrative vs rendering lane envelopes side-by-side | `stws.hq3.admit_to_first_closure` | Two channels: one **committed_session** narrative lane + one **committed_session** rendering lane (exact channel ids **execution-deferred**) | [[Phase-3-2-1-Observation-Channel-Taxonomy-Roadmap-2026-03-30-2310]] § Behavior; [[Phase-4-1-3-Consumer-Surface-Framing-and-Presentation-Time-Validation-Roadmap-2026-04-03-2110]] § Behavior |
| `sor.hq3.dm_live_envelope` | **Single-lane** readout for **live_tweak** DM act inside window — envelope must carry **3.1.3** class + **3.2.2** disclosure when skew | `stws.hq3.dm_live_within_window` | One **live_tweak**-class channel family (ids **execution-deferred**) | [[Phase-3-1-3-Sim-Visible-Classification-and-DM-Overwrite-Channel-Mapping-Roadmap-2026-04-02-0035]] § Behavior; [[Phase-4-1-3-Consumer-Surface-Framing-and-Presentation-Time-Validation-Roadmap-2026-04-03-2110]] § Scope |
| `sor.hq3.regen_fence_readout` | **Fence callout** readout — operator sees **structural_regen** boundary without interior checkpoint claims | `stws.hq3.structural_regen_fence` | **Preview / fence** channel labeling only — **no** committed interior envelope | [[Phase-3-1-3-Sim-Visible-Classification-and-DM-Overwrite-Channel-Mapping-Roadmap-2026-04-02-0035]] § Edge cases; [[Phase-4-1-3-Consumer-Surface-Framing-and-Presentation-Time-Validation-Roadmap-2026-04-03-2110]] § Scope |

## Channel → PresentationEnvelope field matrix

| slice_operator_readout_id | SeamId required | authority_class echo | freshness / drift echo | emphasis_kind source | presentation-time validation predicate (NL) | Explicit heading anchor (GWT-6.1.3-G audit) |
| --- | --- | --- | --- | --- | --- | --- |
| `sor.hq3.admit_closure_dual_lane` | Yes — from **3.4.1** row cited by lane | **3.2.1** per channel | **3.2.2** classes per channel | **4.1.1** per lane | Subscription parity + compare-lanes disclosure | **4.1.3** — `## Behavior` (1–3); **3.2.1** — `## Behavior` |
| `sor.hq3.dm_live_envelope` | Yes | **committed_session** or explicit **preview** per **3.2.1** | **3.2.2** on DM skew | **4.1.1** + **4.1.2** when reconciliation applies | Envelope self-check + no PreCommit smuggle | **4.1.3** — `## Scope`; **3.1.3** — `## Behavior` |
| `sor.hq3.regen_fence_readout` | Yes — seam for fence surface | **preview_shadow** / fence labels only | **3.2.2** **disclosure** mandatory | Coarse / degraded emphasis per **4.1.1** edge | Withhold interior committed claims | **4.1.3** — `## Edge cases`; **6.1.2** — matrix row `stws.hq3.structural_regen_fence` |

## GWT-6.1.3-A–K (narrowed vs GWT-6-C / secondary delegation)

| ID | Then (evidence expectation) | Primary / secondary anchor |
| --- | --- | --- |
| **GWT-6.1.3-A** | Catalog **Operator readout row** lists ≥3 stable `slice_operator_readout_id` values | **GWT-6-C** delegation |
| **GWT-6.1.3-B** | Matrix **Channel → PresentationEnvelope** lists ≥3 rows tied to readout IDs | **4.1.3** / **3.2.1** |
| **GWT-6.1.3-C** | Each readout row joins ≥1 **`stws.*`** ID from **6.1.2** | **6.1.2** catalog |
| **GWT-6.1.3-D** | `sor.hq3.admit_closure_dual_lane` cites **4.1.3** compare-lanes behavior | **4.1.3** |
| **GWT-6.1.3-E** | `sor.hq3.dm_live_envelope` cites **3.1.3** live vs structural labels | **3.1.3** |
| **GWT-6.1.3-F** | `sor.hq3.regen_fence_readout` states execution-deferred interior checkpoint story | **6.1.2** + conceptual waiver |
| **GWT-6.1.3-G** | Outward guarantee **Traceability** — explicit heading column populated | This note § Interfaces |
| **GWT-6.1.3-H** | Outward guarantee **No second consumer truth** explicit in Behavior §1 | **4.1.3** |
| **GWT-6.1.3-I** | Downstream **6.1 rollup** contract references `slice_operator_readout_id` | This note § Interfaces |
| **GWT-6.1.3-J** | **InstrumentationIntent** **`ii.presentation.envelope`** may cite `sor.hq3.*` rows as alignment (no new intent rows) | Secondary **6.1** bundle |
| **GWT-6.1.3-K** | Open questions include at least one execution-deferred item | Below |

## Edge cases

- **Partial subgraph manifest:** Readout rows **not** listed here are **out of slice** until manifest adds pins—no silent “full 4.1 dual-lane” claim.
- **Stale wikilink:** **`slice_operator_readout_id`** remains stable; repair wikilinks in **handoff-audit** if **4.1.3** / **3.2.1** titles move.

## Open questions

- Whether **slice_operator_readout_id** should appear in **export JSON** for lab automation (**execution-deferred** wire format).
- Distinct operator-facing **codes** for presentation-time validation failures vs **4.1.2** coherence failures (**execution-deferred** — see **4.1.3** Open questions).

## Pseudo-code readiness

Depth **3** — tables + NL invariants only; **algorithm sketches** optional; no pseudo-code required on conceptual track for this slice.

## Parent

- Secondary: [[Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle-Roadmap-2026-04-06-1200]]

## Research integration

> [!note] External grounding
> Vault-first; continuity from **6.1** manifest operator readout pins + **6.1.2** scenarios + **3.2.1** + **4.1.3** only.
