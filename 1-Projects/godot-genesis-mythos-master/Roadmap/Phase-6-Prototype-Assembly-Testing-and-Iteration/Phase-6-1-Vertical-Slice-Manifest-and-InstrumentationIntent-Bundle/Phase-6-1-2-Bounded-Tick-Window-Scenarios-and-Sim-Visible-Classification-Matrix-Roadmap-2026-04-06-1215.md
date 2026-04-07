---
title: Phase 6.1.2 — Bounded tick window scenarios + sim-visible classification matrix (NL)
roadmap-level: tertiary
phase-number: 6
subphase-index: "6.1.2"
project-id: godot-genesis-mythos-master
status: complete
priority: high
progress: 100
handoff_readiness: 87
created: 2026-04-06
tags:
  - roadmap
  - godot-genesis-mythos-master
  - phase-6
para-type: Project
links:
  - "[[Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle-Roadmap-2026-04-06-1200]]"
  - "[[Phase-6-1-1-Manifest-Field-Registry-FeedbackRecord-and-Instrumentation-Envelope-Roadmap-2026-04-07-1245]]"
  - "[[Branches/phase-6-operator-rollback-20260405/Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle/Phase-6-1-1-Manifest-Admission-Row-Bindings-and-Admission-Ticket-Vocabulary-Roadmap-2026-04-05-1918]]"
  - "[[Phase-6-Prototype-Assembly-Testing-and-Iteration-Roadmap-2026-03-30-0430]]"
  - "[[Phase-3-1-2-Tick-Scheduling-Defer-Merge-and-Work-Queue-Policy-Roadmap-2026-04-02-0020]]"
  - "[[Phase-3-1-3-Sim-Visible-Classification-and-DM-Overwrite-Channel-Mapping-Roadmap-2026-04-02-0035]]"
  - "[[Phase-3-1-4-Persistence-Checkpoint-Boundaries-Roadmap-2026-04-02-2240]]"
  - "[[decisions-log]]"
  - "[[workflow_state]]"
---

## Phase 6.1.2 — Bounded tick window scenarios + sim-visible classification matrix

> [!note] Active-tree remint (godot operator queue)
> This note **re-mints** tertiary **6.1.2** on the **post-rollback active tree**, scoped to [[Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle-Roadmap-2026-04-06-1200]] (secondary **6.1** remint **2026-04-06**). **`manifest_admission_row_id` (`mar.*`) join keys** match active **6.1.1** [[Phase-6-1-1-Manifest-Field-Registry-FeedbackRecord-and-Instrumentation-Envelope-Roadmap-2026-04-07-1245]] (stable IDs aligned to branch audit [[Branches/phase-6-operator-rollback-20260405/Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle/Phase-6-1-1-Manifest-Admission-Row-Bindings-and-Admission-Ticket-Vocabulary-Roadmap-2026-04-05-1918]]). Queue: `pool-remint-612-godot-gmm-20260406120001Z`.

This tertiary **implements** [[Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle-Roadmap-2026-04-06-1200]] § **Manifest — Tick window + sim-visible** for **Horizon-Q3** (`slice_id: horizon_q3_v1`): it names **bounded tick-window scenario rows** that stitch **admission-adjacent** **`manifest_admission_row_id`** values (authority: active **6.1.1** [[Phase-6-1-1-Manifest-Field-Registry-FeedbackRecord-and-Instrumentation-Envelope-Roadmap-2026-04-07-1245]]) to **3.1.2** defer-merge / work-queue closure, **3.1.3** sim-visible + DM overwrite classes, and **3.1.4** checkpoint boundaries—so **GWT-6-B** evidence cites **one matrix** without re-deriving Phase **3** bus semantics.

## Scope

**In scope (conceptual):**

- **Slice tick-window scenario catalog** — stable **`slice_tick_window_scenario_id`** rows describing **admission → first bounded window** stories (NL only); each row references ≥1 **`manifest_admission_row_id`** from active **6.1.1** and ≥1 **3.x** authority wikilink + heading.
- **Sim-visible × checkpoint matrix** — rows pair **sim-visible classification** expectations (from **3.1.3**) with **persistence checkpoint** obligations (from **3.1.4**) for each scenario—**labels and join keys only**, no new sim fields.
- **Defer-merge boundary echo** — each scenario states how **3.1.2** **WorkItem** closure / defer ledger interacts with the window boundary (read-only restatement).

**Out of scope:** execution traces, Dataview query bodies in hosts, `Roadmap/Execution/**`, perf timings, changing **3.1.x** authoritative definitions.

## Behavior (natural language)

1. **Scenario-first reading:** Operators cite **`slice_tick_window_scenario_id`** when they mean a **slice-local tick-window slice** of the **3.x** story; they cite **bus / checkpoint** phase notes when changing upstream truth.
2. **Admission carry-forward:** Scenarios **assume** **`mar.hq3.pin.2_7_3`** redemption narrative is satisfied before **`stws.hq3.*`** windows that mention **live** ticks—no alternate redemption path.
3. **DM class persistence:** Matrix cells use **only** **3.1.3** **live_tweak** vs **structural_regen** (and related labels as named on **3.1.3**) — no third overwrite class at this depth.

## Interfaces

**Upstream (secondary 6.1):** Consumes **Manifest — Tick window + sim-visible classification** pins and **GWT-6 → 6.1** row **GWT-6-B**; does not widen **InstrumentationIntent** bundle rows (those remain declared on **6.1**; **6.1.2** may cite **`ii.sim.tick_closure`** as alignment text only).

**Upstream (6.1.1):** **`manifest_admission_row_id`** values are **join keys** for admission-adjacent scenario rows—**6.1.2** does not add or rename **`mar.*`** IDs. **Active-tree authority:** [[Phase-6-1-1-Manifest-Field-Registry-FeedbackRecord-and-Instrumentation-Envelope-Roadmap-2026-04-07-1245]] (stable **`mar.hq3.*`** IDs; branch note remains audit-only diff).

**Upstream (Phase 3.1.x):** Read-only — **3.1.2** work queue / defer-merge; **3.1.3** classification + DM channels; **3.1.4** checkpoints.

**Downstream (6.1.3+):** Next mint on active tree — **ObservationChannel** + **4.1.3** readout; audit reference [[Branches/phase-6-operator-rollback-20260405/Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle/Phase-6-1-3-ObservationChannel-Lane-Readout-and-Presentation-Time-Co-Display-Roadmap-2026-04-06-2130]] must be **re-minted** before links are authoritative on the active tree. This **6.1.2** requires downstream notes to reference these **`slice_tick_window_scenario_id`** values when extending tick-adjacent operator surfaces.

**Outward guarantees:**

- **No second tick truth:** Tick ordering vocabulary (**tick_index**, closure, defer) matches **3.1.2** / **3.1.4** — scenarios **describe** windows; they do not define new ordering primitives.
- **Traceability:** Every scenario row + every matrix row lists a **non-bypass** wikilink + heading anchor (same style as active **6.1.1** **GWT-6.1.1-G**).

## Slice tick-window scenario catalog (Horizon-Q3)

| slice_tick_window_scenario_id | Human label (NL) | Admission join (`manifest_admission_row_id`) | Primary 3.x anchors |
| --- | --- | --- | --- |
| `stws.hq3.admit_to_first_closure` | First **bounded** window after **live** admission — **WorkItem** ledger must close or explicitly defer before window end | `mar.hq3.pin.2_7_3`, `mar.hq3.pin.2_7_1` | [[Phase-3-1-2-Tick-Scheduling-Defer-Merge-and-Work-Queue-Policy-Roadmap-2026-04-02-0020]] § Behavior; [[Phase-3-1-4-Persistence-Checkpoint-Boundaries-Roadmap-2026-04-02-2240]] § Behavior |
| `stws.hq3.dm_live_within_window` | **live_tweak** class DM act inside window — checkpoints still **tick-scoped** per **3.1.4** | `mar.hq3.slice_identity` | [[Phase-3-1-3-Sim-Visible-Classification-and-DM-Overwrite-Channel-Mapping-Roadmap-2026-04-02-0035]] § Behavior; [[Phase-3-1-4-Persistence-Checkpoint-Boundaries-Roadmap-2026-04-02-2240]] § Edge cases |
| `stws.hq3.structural_regen_fence` | **structural_regen** class act — treated as **out-of-window** for slice story unless secondary manifest explicitly promotes a regen leg (deferred) | `mar.hq3.slice_identity` | [[Phase-3-1-3-Sim-Visible-Classification-and-DM-Overwrite-Channel-Mapping-Roadmap-2026-04-02-0035]] § Edge cases; [[Phase-3-1-2-Tick-Scheduling-Defer-Merge-and-Work-Queue-Policy-Roadmap-2026-04-02-0020]] § Interfaces |

## Sim-visible × checkpoint matrix (per scenario)

| slice_tick_window_scenario_id | Sim-visible expectation (NL) | Checkpoint obligation (NL) | Explicit heading anchor (GWT-6.1.2-G audit) |
| --- | --- | --- | --- |
| `stws.hq3.admit_to_first_closure` | **Committed_session**-visible facts only inside window; **preview_shadow** lanes do not satisfy checkpoint rows | At least one **tick-scoped** durability record aligns with **3.1.4** ordering vs bus | **3.1.4** — `## Behavior` (checkpoints); **3.1.2** — `## Behavior` (defer-merge) |
| `stws.hq3.dm_live_within_window` | DM channel maps to **3.1.3** **live_tweak** — sim-visible class stable across the window | Checkpoint captures **before/after** DM act within **same** tick closure when act claims tick alignment | **3.1.3** — `## Behavior` (classification); **3.1.4** — `## Edge cases` |
| `stws.hq3.structural_regen_fence` | Regen class acts **not** modeled as ordinary window interior—operator sees **fence** callout in slice story | Checkpoints **not** asserted for interior of regen until execution track defines regen chunking — **execution-deferred** | **3.1.3** — `## Edge cases`; **roadmap-state** conceptual waiver |

## GWT-6.1.2-A–K (narrowed vs GWT-6-B / secondary delegation)

| ID | Then (evidence expectation) | Primary / secondary anchor |
| --- | --- | --- |
| **GWT-6.1.2-A** | Catalog **Slice tick-window scenario** lists ≥3 stable `slice_tick_window_scenario_id` values | **GWT-6-B** delegation |
| **GWT-6.1.2-B** | Matrix **Sim-visible × checkpoint** lists ≥3 rows tied to scenario IDs | **3.1.3** / **3.1.4** |
| **GWT-6.1.2-C** | Each scenario row joins ≥1 **`mar.*`** ID from active **6.1.1** catalog | [[Phase-6-1-1-Manifest-Field-Registry-FeedbackRecord-and-Instrumentation-Envelope-Roadmap-2026-04-07-1245]] |
| **GWT-6.1.2-D** | `stws.hq3.admit_to_first_closure` cites **3.1.2** + **3.1.4** behaviors | **3.1.2**, **3.1.4** |
| **GWT-6.1.2-E** | `stws.hq3.dm_live_within_window` cites **3.1.3** live vs structural labels | **3.1.3** |
| **GWT-6.1.2-F** | `stws.hq3.structural_regen_fence` states execution-deferred checkpoint story | Conceptual waiver |
| **GWT-6.1.2-G** | Outward guarantee **Traceability** — explicit heading column populated | This note § Interfaces |
| **GWT-6.1.2-H** | Outward guarantee **No second tick truth** explicit in Behavior §1 | **3.1.2** / **3.1.4** |
| **GWT-6.1.2-I** | Downstream **6.1.3+** contract references `slice_tick_window_scenario_id` | This note § Interfaces |
| **GWT-6.1.2-J** | **InstrumentationIntent** **`ii.sim.tick_closure`** may cite `stws.hq3.admit_to_first_closure` as alignment (no new intent rows) | Secondary **6.1** bundle |
| **GWT-6.1.2-K** | Open questions include at least one execution-deferred item | Below |

## Edge cases

- **Partial subgraph manifest:** If secondary **6.1** lists a **minimal** vertical leg, scenarios **not** listed here are **out of slice** until manifest adds pins—no silent “full 3.x” claim.
- **Stale wikilink:** **`slice_tick_window_scenario_id`** remains stable; repair wikilinks in **handoff-audit** if **3.1.x** titles move.
- **Out-of-order remint:** **6.1.2** minted before active **6.1.1** — resolved by **2026-04-07** active **6.1.1** mint (**`mar.*`** stable IDs on disk).

## Open questions

- Whether **lab burn-down** should sort scenarios by **P0/P1** (**execution-deferred** priority tier).
- Minimum **operator card** shape linking **`stws.*`** + **`mar.*`** in exports (**execution-deferred** wire format).

## Pseudo-code readiness

Depth **3** — tables + NL invariants only; **algorithm sketches** optional; no pseudo-code required on conceptual track for this slice.

## Parent

- Secondary: [[Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle-Roadmap-2026-04-06-1200]]

## Research integration

> [!note] External grounding
> Vault-first; continuity from **6.1** manifest + **3.1.2** / **3.1.3** / **3.1.4** + **6.1.1** **`mar.*`** row IDs ([[Phase-6-1-1-Manifest-Field-Registry-FeedbackRecord-and-Instrumentation-Envelope-Roadmap-2026-04-07-1245]]).
