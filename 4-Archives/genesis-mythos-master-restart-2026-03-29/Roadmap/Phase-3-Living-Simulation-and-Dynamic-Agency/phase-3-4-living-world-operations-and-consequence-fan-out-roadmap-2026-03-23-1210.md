---
title: Phase 3.4 — Living world operations and consequence fan-out
roadmap-level: secondary
phase-number: 3
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-23
tags: [roadmap, genesis-mythos-master, phase, living-world, npc, faction, weather]
para-type: Project
subphase-index: "3.4"
handoff_readiness: 85
execution_handoff_readiness: 50
handoff_readiness_scope: vault-normative draft — slice taxonomy + RNG namespaces + regen coupling vs 3.2; golden/replay rows TBD (D-032 / D-044 / D-047)
handoff_gaps:
  - "Live tertiary cursor: **3.4.9** post-**recal** junior handoff / WBS bundle — [[phase-3-4-9-post-recal-task-decomposition-junior-handoff-bundle-roadmap-2026-03-22-1225]]; prior **3.4.8** policy — [[phase-3-4-8-high-context-util-policy-and-phase-4-stub-readiness-roadmap-2026-03-22-1205]]; **3.4.7** WBS — [[phase-3-4-7-perspective-entry-wbs-and-phase-4-1-task-bridge-roadmap-2026-03-22-0748]]; **3.4.6** — [[phase-3-4-6-presentation-handoff-task-lanes-validation-harness-and-dm-promotion-roadmap-2026-03-22-1320]]; **3.4.5** bridge — [[phase-3-4-5-living-world-to-perspective-handoff-bridge-roadmap-2026-03-22-1205]]; machine authority: [[workflow_state]] + [[roadmap-state]]. **3.4.4** rollup (**D-055**) remains **historical closure** context — next: **recal** (ctx **>** threshold **80** per **D-060**), **3.4.10+**, mint first **Phase 4** secondary after **D-059**, **handoff-audit**, or operator **D-044**; registry / golden rows still vault-TBD (**D-032** / **D-043**)"
  - "RegenLaneTotalOrder_v0 A/B still unpinned per D-044 — do not assert single interleaving story for regen-heavy living-world edits"
links:
  - "[[phase-3-living-simulation-and-dynamic-agency-roadmap-2026-03-19-1101]]"
  - "[[phase-3-1-simulation-tick-scheduler-and-time-quanta-roadmap-2026-03-21-2346]]"
  - "[[phase-3-2-dm-overwrite-regeneration-gates-roadmap-2026-03-21-2347]]"
  - "[[phase-3-3-persistence-cross-session-consequence-propagation-roadmap-2026-03-21-2348]]"
  - "[[phase-3-3-4-phase-3-3-secondary-closure-rollup-and-advance-readiness-roadmap-2026-03-23-1200]]"
  - "[[distilled-core]]"
  - "[[decisions-log]]"
---

## Phase 3.4 — Living world operations and consequence fan-out

> **Architect:** After **3.3.4** secondary closure (**D-050**), Phase **3** gains a fourth workstream for **ambient simulation** that must remain **tick-total**, **replay-stable**, and **persistence-aware** — not a parallel wall-clock universe.

**Deliverables (draft):** Normative binding for **NPC / faction / environmental cycles** (schedules, weather-like fields, territory or stance fan-out) as **additional ordered work inside `tick_epoch`**, consuming **agency slices** or an explicit sub-scheduler that still publishes through **`AgencySliceApplyLedger_v0`** and **`TickCommitRecord_v0`**.

**Non-goals (this secondary):** Choosing engine stack (**D-027**); literal golden rows (blocked on **D-032** / **D-043** / operator **D-044** fork).

### Acceptance sketch — DEFERRED (normative vs execution)

Execution checkboxes below are **not** “unchecked TODOs” — they map to **adoption decisions** and **open engineering work**. Normative coverage lives in **D-052 / D-053 / D-054** (tertiaries) and **D-055** (rollup); literal repo/golden proof remains **TBD** until **D-044**, **D-032**, **D-043**, **D-048**, **D-049**, and **2.2.3**/**D-020** materialize.

| Sketch line (intent) | Normative anchor | Execution / evidence still TBD |
| --- | --- | --- |
| Tick-scoped intents vs **3.1.4** / **3.1.5** | **D-052**–**D-054** + **3.1** spine | Golden replay rows for ambient + ledger merge |
| **RegenRequest_v0** / **`regen_apply_sequence`** | **D-053**, **D-044** (HOLD until A/B) | **D-044** logged; regen lane goldens |
| **ResumeCheckpoint_v0** / **PersistenceBundle_vN** | **3.3.x**, **D-048** / **D-049** | Migrate-and-resume harness + registry rows |

## Research integration (external grounding)

- **Constraint stack:** Living-world work (NPC schedules, weather cycles, faction fan-out) must flow through existing **Phase 3.1** contracts (`TickCommitRecord_v0`, `AgencySliceSchedule_v0`, mutation apply ledger, post-apply observable hash) — see [[phase-3-1-simulation-tick-scheduler-and-time-quanta-roadmap-2026-03-21-2346]]; **3.2** regen / DM ordering (`regen_apply_sequence`, `RegenLaneTotalOrder_v0`) — [[phase-3-2-dm-overwrite-regeneration-gates-roadmap-2026-03-21-2347]]; **3.3** persistence + **D-050** rollup on [[phase-3-3-4-phase-3-3-secondary-closure-rollup-and-advance-readiness-roadmap-2026-03-23-1200]] / [[phase-3-3-persistence-cross-session-consequence-propagation-roadmap-2026-03-21-2348]].
- **Synthesis (full):** [[Ingest/Agent-Research/phase-3-4-living-world-operations-research-2026-03-23]]
- **External anchors:** [Fix Your Timestep!](https://gafferongames.com/post/fix_your_timestep/) (fixed logical dt + accumulator vs render), [Deterministic Lockstep](https://gafferongames.com/post/deterministic_lockstep/) (replay = inputs + total order), [PCG — independent streams](https://www.pcg-random.org/useful-features.html) (namespaced RNG so ambient sim does not steal entropy from proc/agency), [Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html) (append-only events + snapshots for resume — aligns with `ResumeCheckpoint_v0` / migration harness narrative).

## Risk register (v0)

| Risk | Signal | Mitigation | Owner |
|------|--------|------------|-------|
| Hidden wall-clock ordering | NPC updates bypass slice schedule | Force all mutations through **3.1.x** publish path; ban background threads that touch authoritative state | Eng |
| RNG cross-talk | Weather stream consumes agency entropy | Dedicated stream namespaces per **D-034** / research synthesis | Eng |
| Regen vs tick ambiguity | Faction territory regen unordered vs player intents | **`RegenRequest_v0`** + **D-044** fork logged before normative closure | Operator + eng |
| Persistence mismatch | Long-horizon world fields skip bundle version | Bind fields to **PersistenceBundle_vN** + matrix outcomes (**D-048**) | Eng |

### Tertiary spine

- **3.4.1** — [[phase-3-4-1-ambient-slice-taxonomy-and-schedule-binding-roadmap-2026-03-23-1620]] — ambient slice taxonomy + schedule binding + RNG matrix + regen/persistence predicates — **D-052** (draft).
- **3.4.2** — [[phase-3-4-2-living-world-consequence-fan-out-and-ordered-projection-roadmap-2026-03-23-1805]] — ordered projection chain ledger → observable barrier → tick commit; research-integrated — **D-053** (draft).
- **3.4.3** — [[phase-3-4-3-living-world-facet-manifest-catchup-and-replay-parity-roadmap-2026-03-23-1810]] — facet manifest + serialization_profile coupling; idempotent catch-up deferral; replay parity — **D-054** (draft).
- **3.4.4** — [[phase-3-4-4-phase-3-4-secondary-closure-rollup-and-advance-readiness-roadmap-2026-03-23-1935]] — **G-P3.4-\*** secondary closure rollup + advance readiness — **D-055** (draft).
- **3.4.5** — [[phase-3-4-5-living-world-to-perspective-handoff-bridge-roadmap-2026-03-22-1205]] — living-world → Phase 4 presentation bridge (`PresentationViewState_v0` / `CameraBinding_v0`) — **D-056** (draft).
- **3.4.6** — [[phase-3-4-6-presentation-handoff-task-lanes-validation-harness-and-dm-promotion-roadmap-2026-03-22-1320]] — task lanes A/B/C, `PresentationProjectionHarness` sketch, `ToolActionQueue_v0` promotion tasks — **D-057** (draft).
- **3.4.7** — [[phase-3-4-7-perspective-entry-wbs-and-phase-4-1-task-bridge-roadmap-2026-03-22-0748]] — Phase 4.1 entry WBS (`T-P4-01`…`T-P4-05`), adapter→rig split, L1 **`missing_task_decomposition`** alignment — **D-058** (draft).
- **3.4.8** — [[phase-3-4-8-high-context-util-policy-and-phase-4-stub-readiness-roadmap-2026-03-22-1205]] — automation policy at high **Ctx Util** (~threshold **80%**), **RECAL** / **handoff-audit** / narrow deepen matrix, **CQRS** read/write vocabulary for adapter→rig — **D-060** (draft).
- **3.4.9** — [[phase-3-4-9-post-recal-task-decomposition-junior-handoff-bundle-roadmap-2026-03-22-1225]] — post-**recal** WBS leaves + junior handoff pack (**GMM-HYG-01** / **GMM-DLG-01** / **GMM-TREE-01**) for **3.4.8** validator ladder + L1 **`missing_task_decomposition`** — **D-061** (draft).
- **3.4.10+** — *(optional expansion, first **Phase 4** secondary mint after **D-059**, or further `recal`)* — TBD after operator **D-044** / **D-059** / **`advance-phase`** policy.

## Tertiary notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency"
WHERE (roadmap-level = "secondary" OR roadmap-level = "tertiary" OR roadmap-level = "task") AND contains(subphase-index, "3.4")
SORT subphase-index ASC, file.name ASC
```
