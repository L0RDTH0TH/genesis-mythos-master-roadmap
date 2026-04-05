---
title: Phase 3 — Living Simulation and Dynamic Agency
roadmap-level: primary
phase-number: 3
subphase-index: "0"
project-id: godot-genesis-mythos-master
status: active
priority: high
progress: 85
phase3_primary_checklist: complete
phase3_primary_rollup_post_34: complete
handoff_readiness: 86
created: 2026-03-30
tags:
  - roadmap
  - godot-genesis-mythos-master
  - phase
para-type: Project
links:
  - "[[godot-genesis-mythos-master-Roadmap-2026-03-30-0430]]"
---

## Phase 3 — Living Simulation and Dynamic Agency

Deliver a **layer tick–based living simulation** (weather, NPC agendas, factions, persistence) with explicit **DM overwrite semantics** distinguishing **live operator tweaks** from **structural re-generation requests**, and keep **simulation advancement** decoupled from **rendering** so previews, spectate, and full sessions can share contracts without sharing frame policy.

## Conceptual waiver & safety invariants

- **Conceptual track waiver (rollup / CI / HR):** Design authority on the **conceptual** track does **not** claim execution rollup, registry/CI closure, or HR-style proof rows; those are **execution-deferred** per [[3-Resources/Second-Brain/Docs/Dual-Roadmap-Track|Dual-Roadmap-Track]].
- **Determinism continuity:** Phase 3 **consumes** Phase 2’s **committed world** and **simulation-entry / first-tick** contracts (including shadow-to-live parity where applicable); Phase 3 does **not** re-derive **2.4** branch semantics or **2.5** audit surfaces—only **references** upstream handoff bundles.
- **`GMM-2.4.5-*`:** remain **reference-only** anchors for execution-track closure artifacts.

- [x] Core implementation task — **Simulation tick + event bus integration** (NL contract at primary; bodies under **3.1+**)
- [x] Core implementation task — **DM overwrite channels** (live tweak vs regen request — semantics at primary; channel shapes under secondaries)
- [x] Glue / integration task — **Vitality / consequence features** without breaking deterministic replay contracts (scoped at primary; detail under agency slices)

### Progress semantics (frontmatter)

`progress` is **0–100** for this note’s conceptual slice depth: **0** = stub only; **~20–25** = primary NL checklist complete enough to mint secondaries; **~50+** = secondaries drafted; **100** = phase-ready for execution handoff (still execution CI deferred).

## Scope

**In scope:** tick cadence for world state evolution; **agency** surfaces (NPC agendas, factions) that produce durable consequences; **persistence** contracts across sessions; **DM overwrite** semantics (what can change live vs what requires regen pipeline); **simulation vs rendering** separation for previews vs full sessions; **event bus** integration as the cross-cutting seam for sim-visible facts without dictating engine APIs.

**Out of scope:** concrete engine APIs, threading model, netcode, perf budgets, save-file schemas, and full narrative content pipelines (those remain data/injection inputs or later execution slices).

## Behavior (natural language)

**Actors:** **Simulation kernel** (advances tick index, applies scheduled work), **agency systems** (NPC/faction drivers), **weather/environment** drivers, **persistence** writer/loader, **DM** (live overrides + regen requests), **players** (inputs that become intents or operator actions), **rendering** (read-only observation of sim-visible state for display).

**Inputs:** committed world snapshot + replay anchors from Phase 2 handoff, operator/DM directives (live vs structural), player intents, tick budget / scheduling hints (conceptual—no numeric SLA at primary).

**Outputs:** updated world state at tick boundaries, sim-visible events on the bus, persistence checkpoints as defined by execution track, **regen requests** as structured intents (not executed at conceptual depth).

**Ordering (high level):** `tick advance → integrate external intents → agency/environment updates → consequence resolution → persist-eligible checkpoint → emit sim-visible events → (parallel) rendering consumes observations`.

## Interfaces

**Upstream (Phase 2):** consumes **simulation bootstrap** and **first committed tick trace** semantics; does not weaken **dry-run vs commit** boundaries established in Phase 2.

**Downstream (Phase 4+):** exposes stable **sim-visible** facts and **overwrite class** labels (live vs regen) for narrative/rendering layers without requiring them to understand full pipeline internals.

**Outward guarantees:**

- **Decoupling:** rendering observes **snapshots / observation channels**, not direct mutation of sim core (matches Phase 1 separation story).
- **Overwrite classes:** DM actions are tagged **live** (reversible within contract) vs **structural regen** (invalidates downstream caches per Phase 2 validation story—detailed in secondaries).

## Edge cases

- **Tick stall / backpressure:** sim may defer work to later ticks; **no silent cross-tick merge** of incompatible writes without explicit merge policy (execution-deferred).
- **DM live tweak vs regen:** if a tweak implies **world-graph** edits that Phase 2 would classify as **structural**, route to **regen request** path (NL only here).
- **Multi-session / preview:** preview runs consume **read-only** observation contracts; must not advance authoritative persistence without passing Phase 2 commit boundary semantics.

## Open questions

- Minimum **agency granularity** (per-NPC vs cohort vs faction-level) before execution prototypes.
- Whether **weather** is strictly deterministic from seed+bundle or admits operator “bias” knobs without breaking replay (execution-deferred).

## Pseudo-code readiness

At **primary** conceptual depth, **no pseudo-code** is required. Readers should be able to sketch module boundaries and tick ordering without algorithms; **interfaces + deterministic hooks** for secondaries start at **3.1**.

## Phase 3 primary rollup (post-3.4 seam catalog / consumer rows)

> **Architect:** Same pass closes **Phase 3** at the **primary** note after secondaries **3.1–3.4** each reached **rollup** `handoff_readiness` **86** and **3.4.1** minted **SeamId** catalog + consumer contract tables. This section is **NL checklist + phase-level GWT closure** — **no** execution rollup, registry/CI, or HR proof claims (`GMM-2.4.5-*` remain reference-only).

**Spine closed in NL (conceptual):** secondaries **3.1** (chain **3.1.1–3.1.5**), **3.2** (rollup + **3.2.1–3.2.3**), **3.3** (rollup + **3.3.1–3.3.2**), **3.4** (rollup + **3.4.1**) are each structurally complete at declared depth; **3.4** binds Phase **4** consumption via **SeamId** rows without inventing a second checkpoint authority (**3.1.4** remains canonical for durability boundaries).

**Roll-up invariants (design authority):**

- **Ordering:** `tick advance → intents → agency/environment → consequence resolution → persist-eligible checkpoint → sim-visible bus events → (parallel) rendering observes observation channels` — consistent with primary **Behavior** and secondaries **3.1–3.4**.
- **Overwrite classes:** **live** vs **structural regen** remain NL-labeled through **3.1.3** / **3.2** / **3.4** — execution wire formats **deferred**.
- **Execution-deferred:** **D-3.1.5-***, **D-3.3-***, **D-3.4-*** rows in [[decisions-log]] stay **out of scope** for conceptual completion; see primary **Conceptual waiver** above.
- **Next structural operator choice:** **`advance-phase`** to Phase **4** when gates pass (primary `handoff_readiness` **86** + Phase 3 rollup narrative aligned), **or** optional Phase 3 polish only if PMG expands scope (not assumed here).

### GWT parity (phase-level **GWT-3-A–K** vs secondaries **3.1–3.4**)

| ID | Given | When | Then | Evidence (secondary / tertiary) |
| --- | --- | --- | --- | --- |
| **GWT-3-A** | **2.7.3** committed trace + Phase 2 commit boundary | Kernel admits world to **3.1** tick + bus | Monotonic tick + replay-visible **SimEvent** facts | [[Phase-3-1-Sim-Tick-and-Event-Bus-Spine-Roadmap-2026-03-30-2213]] |
| **GWT-3-B** | **3.1.1**–**3.1.2** ordering + merge policy | Work scheduled for a tick | Deterministic defer/merge closure before checkpoint eligibility | **3.1.2** + **3.1.4** |
| **GWT-3-C** | **3.1.3** classification + **3.1.5** agency | Intent/overwrite admitted | Sim-visible classification + **WorkItem** scheduling per merge matrix | **3.1.3**, **3.1.5** |
| **GWT-3-D** | **3.2.1** **ObservationChannel** + **3.2.2** freshness/drift | Renderer reads sim state | **preview_shadow** vs **committed_session** + policy classes — no authoritative checkpoint from preview | [[Phase-3-2-Simulation-Rendering-Decoupling-and-Observation-Channels-Roadmap-2026-04-02-2300]] rollup |
| **GWT-3-E** | **3.2.3** UX binds + **D-3.1.5-*** loci | Operator maps panels to channels | NL binding surfaces without closing wire formats | **3.2.3** |
| **GWT-3-F** | **3.3.1** cohesion seams + **3.3.2** matrix | Consequence + persistence evaluated | Vitality/consequence/durability story consistent with **3.1.4**/**3.3.2** **I-3.3-*** | [[Phase-3-3-Vitality-Consequence-and-Persistence-Cohesion-Roadmap-2026-04-03-0005]] rollup |
| **GWT-3-G** | **3.4** downstream handoff narrative | Phase 4 consumer reads exports | Sim-visible bundle + overwrite labels + durability boundary vs **3.1.4** / **3.3.x** | [[Phase-3-4-Downstream-Handoff-and-Phase-4-Readiness-Roadmap-2026-04-03-0100]] rollup |
| **GWT-3-H** | **3.4.1** **SeamId** rows | Consumer resolves a seam | One authoritative row — no reinterpretation of **3.1**/**3.2.1**/**3.3.2**/**3.1.4** anchors | [[Phase-3-4-1-Handoff-Seam-Catalog-and-Consumer-Contract-Rows-Roadmap-2026-04-03-0115]] |
| **GWT-3-I** | Open **D-3.4-*** in [[decisions-log]] | Operator needs consumer granularity | Decision loci exist — **execution-deferred** closure | **D-3.4-phase4-consumer-granularity**, **D-3.4-narrative-rendering-split** |
| **GWT-3-J** | Primary **Open questions** (agency granularity, weather bias) | Execution prototypes | Rows remain **execution-deferred** — do not block conceptual rollup | Primary § Open questions + **3.3** OQ |
| **GWT-3-K** | Conceptual waiver | Validator advisory (**missing_roll_up_gates**, etc.) | Treated as **execution-deferred** — not authoritative open gates for Phase 3 completion | [[roadmap-state]], [[distilled-core]] |

`handoff_readiness` on this primary note raised to **86** after rollup narrative alignment with secondaries **3.1–3.4** (`handoff_readiness` **86** on each secondary rollup note where applicable).

## Subphases & notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/godot-genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency"
WHERE roadmap-level = "primary" OR roadmap-level = "secondary" OR roadmap-level = "tertiary"
SORT subphase-index ASC, file.name ASC
```
