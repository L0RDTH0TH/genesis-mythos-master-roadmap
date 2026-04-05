---
title: Phase 4 — Perspective Split and Control Systems
roadmap-level: primary
phase-number: 4
subphase-index: "4"
project-id: godot-genesis-mythos-master
status: active
priority: high
progress: 85
phase4_primary_checklist: complete
phase4_primary_rollup_nl_gwt: complete
handoff_readiness: 86
created: 2026-03-30
tags:
  - roadmap
  - godot-genesis-mythos-master
  - phase
para-type: Project
links:
  - "[[godot-genesis-mythos-master-Roadmap-2026-03-30-0430]]"
  - "[[Phase-4-1-Narrative-Rendering-and-Consumer-Surface-Lanes-Roadmap-2026-04-03-2015]]"
---

## Phase 4 — Perspective Split and Control Systems

Ship **first-person player immersion**, **DM free-flight plus orthographic tabletop precision**, and a **unified camera / interpolator abstraction** so mode switches stay smooth—while **consuming** Phase 3 **sim-visible** exports and **SeamId**-keyed consumer rows from [[Phase-3-4-1-Handoff-Seam-Catalog-and-Consumer-Contract-Rows-Roadmap-2026-04-03-0115]] without re-deriving **3.1** bus semantics or **3.1.4** checkpoint authority.

## Conceptual waiver & safety invariants

- **Conceptual track waiver (rollup / CI / HR):** Design authority on the **conceptual** track does **not** claim execution closure for renderer perf budgets, input device drivers, or full netcode—those are **execution-deferred** per [[3-Resources/Second-Brain/Docs/Dual-Roadmap-Track|Dual-Roadmap-Track]].
- **Upstream continuity:** Phase 4 **reads** **ObservationChannel** + **authority_class** (**preview_shadow** vs **committed_session**) from **3.2.x**, **freshness/drift** classes from **3.2.2**, **overwrite** labels from **3.1.3**, and **durability/checkpoint** boundaries from **3.1.4** / **3.3.2**—through **3.4.1** **SeamId** rows only; **no** silent reinterpretation of upstream anchors.
- **`D-3.4-phase4-consumer-granularity`** / **`D-3.4-narrative-rendering-split`** ([[decisions-log]]): remain **execution-deferred** bundle-shape choices; Phase 4 primary names **NL loci** only.

### Progress semantics (frontmatter)

`progress` is **0–100** for this note’s conceptual slice depth: **~25** = primary NL checklist complete enough to mint secondaries; **~50+** = secondaries drafted; **100** = phase-ready for execution handoff (still execution CI deferred).

- [x] Core implementation task — **Player first-person rig + interaction raycasts** (NL contract at primary; camera space + input → sim-visible intents—bodies under **4.1+**)
- [x] Core implementation task — **DM rigs (free-flight + orthographic)** sharing scene graph + **sim-visible** observation contracts (**3.2.1** taxonomy)
- [x] Glue / integration task — **Camera interpolator module** with easing profiles—bridges **committed_session** vs **preview_shadow** observation paths without breaking **3.1.4** checkpoint semantics

## Scope

**In scope:** **Perspective modes** (player FP, DM flight, DM tabletop orthographic); **camera state machine** and **interpolator** contracts; **input routing** that preserves **overwrite class** semantics from Phase 3; **narrative-facing** vs **rendering-facing** consumer surfaces as **two consumption lanes** of the same **SeamId** handoff (per **D-3.4-narrative-rendering-split**—NL only here).

**Out of scope:** concrete engine APIs, GPU pipeline, asset pipeline, netcode, full UX skinning, and **bundle granularity** closure (**D-3.4-phase4-consumer-granularity**)—execution-deferred.

## Behavior (natural language)

**Actors:** **Player** (first-person camera + interaction intents), **DM** (free-flight + orthographic tabletop camera + overwrite-capable operator actions per **3.1.3**), **camera controller** (mode switching + interpolation), **rendering** (consumes **ObservationChannel** streams per **3.2.x**), **narrative/UI** (consumes **sim-visible** facts + seam rows—may differ **refresh** policy from renderer).

**Inputs:** **committed_session** and **preview_shadow** observation frames per **3.2.1**; **SeamId**-resolved rows from **3.4.1**; operator mode switches (DM vs player); **3.1.5** agency/sim-visible events as optional drivers for camera emphasis (not re-simulated here).

**Outputs:** **stable camera intents** (mode, rig profile, interpolation envelope) that downstream rendering can execute; **no** authoritative sim mutation from Phase 4—**overwrite** remains **3.1.3** / **3.4** story.

**Ordering (high level):** `observe sim-visible frame (per channel authority) → apply perspective mode + rig → interpolate camera pose → emit render/narrative consumer views` — **downstream of** Phase 3 tick/checkpoint ordering, not parallel to sim core.

## Interfaces

**Upstream (Phase 3):** consumes **3.4.1** **SeamId** catalog + consumer contract tables; **forbidden** to invent alternate checkpoint semantics vs **3.1.4**; **preview_shadow** lanes remain non-authoritative for persistence.

**Downstream (Phase 5+):** exposes **mode-switch** and **interpolator** contracts for rules/plugins without mandating renderer implementation.

**Outward guarantees:**

- **Dual consumption:** **Narrative** and **rendering** may attach to different **ObservationChannel** subsets—**D-3.4-narrative-rendering-split** is a **bundle policy** question, not a second sim truth.
- **Interpolation:** camera transitions declare **easing class** + **max duration** so **3.2.2** **drift** classes stay meaningful (display lag disclosed vs semantic drift).

## Edge cases

- **Mode switch during overwrite storm:** DM **live** class actions may reorder emphasis; **structural regen** requests remain **Phase 2/3** routing—Phase 4 only **observes** sim-visible deltas.
- **Preview vs session parity:** **preview_shadow** cameras must not drive **committed_session**-only UX affordances that imply persistence (align **3.2.1** authority_class).
- **Orthographic + large worlds:** clipping / level-of-detail policy is **execution-deferred**; primary only requires **named** risk in open questions.

## Open questions

- Minimum **field-of-view / rig** parameter set before execution prototypes (tied to **D-3.4-phase4-consumer-granularity** when bundles split).
- Whether **DM orthographic** and **free-flight** share one **interpolator** clock or **two lanes** with explicit handoff (execution-deferred).

## Pseudo-code readiness

At **primary** conceptual depth, **no pseudo-code** is required. **Interfaces + mode graph** for secondaries start at **4.1**.

## Phase-level **GWT-4-A–K** (rollup closure vs secondaries **4.1–4.2**)

> **Rollup:** After secondaries **4.1** and **4.2** each reached **GWT-4.1** / **GWT-4.2** family parity vs their tertiaries, this table binds **phase-level** hooks to **rollup evidence** (not re-litigating tertiary rows).

| ID | Given | When | Then | Evidence (rollup / upstream) |
| --- | --- | --- | --- | --- |
| **GWT-4-A** | **3.4.1** **SeamId** row for observation export | Phase 4 consumes sim-visible bundle | Camera / narrative adapters read **one** authoritative seam row | [[Phase-3-4-1-Handoff-Seam-Catalog-and-Consumer-Contract-Rows-Roadmap-2026-04-03-0115]]; **4.1** rollup [[Phase-4-1-Narrative-Rendering-and-Consumer-Surface-Lanes-Roadmap-2026-04-03-2015]] |
| **GWT-4-B** | **3.2.1** **ObservationChannel** + **authority_class** | Renderer selects channel | **preview_shadow** cannot author persistence claims | **3.2** rollup + **3.2.1**; **4.1** rollup (lane adapters + authority) |
| **GWT-4-C** | **3.2.2** freshness/drift class | Frame presented | Tick-aligned vs frame-aligned policy explicit for camera | **3.2.2**; **4.1** rollup + **4.1.2** cross-lane coherence |
| **GWT-4-D** | **3.1.4** checkpoint boundary | Mode switch requested | Interpolation does not fake checkpoint eligibility | **3.1.4**; **4.2** rollup (session orchestration + transition graph vs checkpoints) |
| **GWT-4-E** | **3.1.3** overwrite class | DM action observed | Camera emphasis respects **live** vs **structural** story | **3.1.3**; **4.1** / **4.2** rollups (emphasis + orchestration coherence) |
| **GWT-4-F** | Player **FP** rig | Player session | Interaction intents remain sim-admissible per **3.1.5** | Primary § Behavior; **4.2** rollup (**4.2.1** transition graph) |
| **GWT-4-G** | DM **free-flight** rig | DM session | Non-tabletop movement does not imply regen | Primary § Behavior; **4.2** rollup |
| **GWT-4-H** | DM **orthographic** rig | Tabletop session | Map-scale camera stable vs **3.3** persistence story | Primary § Behavior; **4.2** rollup |
| **GWT-4-I** | **D-3.4-narrative-rendering-split** | Consumer bundle policy chosen | NL acknowledges **two lanes** without dual sim truth | [[decisions-log]]; **4.1** rollup |
| **GWT-4-J** | **D-3.4-phase4-consumer-granularity** | Export cadence chosen | Decision row exists—execution closure deferred | [[decisions-log]]; **4.1** rollup |
| **GWT-4-K** | Conceptual waiver | Validator advisory | Execution-only gaps **deferred**—not blocking primary closure | [[roadmap-state]], [[distilled-core]]; **4.2** rollup (repair / escalation readouts execution-deferred) |

`handoff_readiness` **86** after primary NL checklist + **GWT-4** **rollup** parity vs secondaries **4.1** + **4.2** (CDR [[Conceptual-Decision-Records/deepen-phase-4-primary-rollup-nl-gwt-2026-03-31-1200]]). Queue **`user_guidance`** that referenced **secondary 4.1 rollup only** was **stale**; authoritative deepen target was **Phase 4 primary rollup** per Layer 1 **`effective_target`**.

## Phase 4 primary rollup (NL + GWT-4 vs secondaries 4.1–4.2)

- **NL closure:** Scope / behavior / interfaces / edges / open questions remain consistent with **4.1** (consumer lanes + presentation envelope + presentation-time validation + operator legibility) and **4.2** (session orchestration + transition graph + ledger parity + replay/repair/escalation readouts)—without claiming execution bundle closure (**D-3.4-*** execution-deferred).
- **One-truth:** **SeamId** + **ObservationChannel** authority flows from **3.4.1** / **3.2.x**; secondaries do not introduce a second sim checkpoint authority.
- **Next (conceptual):** **`advance-phase`** Phase **4→5** when gate conditions met, or **`RECAL-ROAD`** first for high ctx util per [[workflow_state]] ## Log.

## Subphases & notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/godot-genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems"
WHERE roadmap-level = "primary" OR roadmap-level = "secondary" OR roadmap-level = "tertiary"
SORT subphase-index ASC, file.name ASC
```
