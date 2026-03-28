---
title: Phase 4.1 — Player-first perspective read-model and rig contracts
roadmap-level: secondary
phase-number: 4
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-24
tags: [roadmap, genesis-mythos-master, phase, perspective, player-first, arch-fork-02]
para-type: Project
subphase-index: "4.1"
handoff_readiness: 84
handoff_readiness_scope: "Player-first presentation spine (ARCH-FORK-02): read-model contracts from committed sim observables → PresentationViewState_v0 / CameraBinding_v0; no mutation via presentation path; T-P4-01…T-P4-05 bridge from 3.4.7"
execution_handoff_readiness: 34
handoff_gaps:
  - "**D-032 / D-043:** Literal replay header fields + golden presentation rows still **TBD** — normative text only until coordinated with **3.1.1** `replay_row_version`."
  - "**G-P*.*-REGISTRY-CI HOLD** on Phase **3.2.4** / **3.3.4** / **3.4.4** rollups **unchanged** by Phase 4 vault work (**D-062** traceability)."
  - "**D-027:** Engine / language citations in examples remain illustrative unless a later decision adopts a stack."
links:
  - "[[phase-4-perspective-split-and-control-systems-roadmap-2026-03-19-1101]]"
  - "[[phase-3-4-7-perspective-entry-wbs-and-phase-4-1-task-bridge-roadmap-2026-03-22-0748]]"
  - "[[phase-3-4-5-living-world-to-perspective-handoff-bridge-roadmap-2026-03-22-1205]]"
  - "[[phase-3-4-6-presentation-handoff-task-lanes-validation-harness-and-dm-promotion-roadmap-2026-03-22-1320]]"
  - "[[decisions-log]]"
---

## Phase 4.1 — Player-first perspective read-model and rig contracts (secondary)

**Architect spine:** Operator pick **D-059 ARCH-FORK-02** — **player-first** perspective slice before shared DM+player control-shell hardening. This secondary owns the **vault-normative** contract boundary for **player** presentation: inputs are **read-only** projections of **`SimObservableBundleTelemetry_v0`** / **`post_apply_observable_root`** and **`TickCommitRecord_v0`**-committed state (**3.1.6** / **3.1.1**), not a second mutation lane into **`AgencySliceApplyLedger_v0`** (**3.1.5**).

### Objectives

- Freeze **adapter → rig** decomposition aligned with **T-P4-01**…**T-P4-05** on [[phase-3-4-7-perspective-entry-wbs-and-phase-4-1-task-bridge-roadmap-2026-03-22-0748]] (**D-058**).
- Bind **`PresentationViewState_v0`** and **`CameraBinding_v0`** drafts from [[phase-3-4-5-living-world-to-perspective-handoff-bridge-roadmap-2026-03-22-1205]] (**D-056**) to **replay-stable** identifiers (hashes / profile ids) **without** claiming CI closure while **D-032** / **D-043** block literal replay columns.
- Keep **lane A/B/C** harness intent from [[phase-3-4-6-presentation-handoff-task-lanes-validation-harness-and-dm-promotion-roadmap-2026-03-22-1320]] (**D-057**): Lane-C / **ReplayAndVerify** rows remain **`@skipUntil(D-032)`** in vault prose.

### Interface table (v0)

| Artifact | Role | Upstream | Downstream | Status |
|----------|------|----------|------------|--------|
| `PresentationViewState_v0` | Player FOV / LOD hooks / presentation-stable hash inputs | Committed observables post-barrier (**3.1.6**) | First-person rig + UI read pipeline | Draft — literals TBD (**D-032**) |
| `CameraBinding_v0` | World rig ↔ sim entity / cell binding | Same + **3.4.x** living-world commits | Deterministic camera replay (future golden) | Draft — coupling TBD |
| `ToolActionQueue_v0` (DM) | Out of scope for **4.1** primary spine | **3.4.6** | Deferred per **ARCH-FORK-02** | Explicit defer |

### WBS trace (checkable leaves)

| ID | Intent | Evidence expectation |
|----|--------|----------------------|
| **T-P4-01** | Adapter boundary spec | Vault pseudo-code + link to observable preimage |
| **T-P4-02** | Rig contract | Player rig consumes `PresentationViewState_v0` only |
| **T-P4-03** | **SCOPED_VAULT** package boundary | No repo path assertions — vault-only (**D-058**) |
| **T-P4-04** | Replay/hash stub row | Placeholder until **replay_row_version** coordinated |
| **T-P4-05** | Handoff to DM shell (later) | Cross-link only — **not** executed in **4.1** first tranche |

### Honesty guards (**D-062**)

> [!warning] Operator advance vs rollup gates
> Macro **Phase 3 → 4** may be logged with **`wrapper_approved: true`** while rollup **`handoff_readiness` 92** remains **below** **`min_handoff_conf` 93** and **G-P*.*-REGISTRY-CI** remains **HOLD**. **Do not** treat Phase 4 deepen or this secondary as **REGISTRY-CI PASS** or automatic **HR 93** satisfaction.

### Risk register (v0)

| Risk | Mitigation |
|------|------------|
| Accidental sim writes from presentation path | CQRS labeling; code review gate; ledger writes only under **3.1.5** / **3.2.x** ordering (**D-044** Option A logged **2026-03-23**) |
| Hash preimage drift vs tick commit | Explicit `serialization_profile_id` + facet manifest intent (**D-037** defer) |
| Scope creep into DM free-cam | **ARCH-FORK-02** — document as **4.x** follow-up secondary, not **4.1** MVP |

### Roll-up gate (4.1.1.x → 4.1.2) — stub

| Gate id | Criterion | Does **not** claim |
|---------|-----------|-------------------|
| **G-P4-1-ADAPTER-CORE** | **4.1.1** preimage table + **4.1.1.1** registry sketch aligned; open tasks carry **`@skipUntil`** owners | REGISTRY-CI **PASS**, rollup **HR ≥ 93**, or repo CI green |
| **G-P4-1-RIG-NEXT** | **4.1.2** (**T-P4-02**) mint only after **G-P4-1-ADAPTER-CORE** row marked **PASS** on this note | Advance-phase eligibility under **`min_handoff_conf` 93** |

### Next (tertiary spine)

- **4.1.1** — Adapter preimage + stable column layout — **minted** [[phase-4-1-1-adapter-preimage-and-stable-column-layout-roadmap-2026-03-24-0018]]; **continued** with nested pre-deepen research + **4.1.1.1** task — queue **`resume-deepen-post-recal-p4-1-1-gmm-20260324T021500Z`**.
- **4.1.1.1** — Adapter row layout registry + **D-032** changelog hooks — **minted** [[phase-4-1-1-1-adapter-row-layout-registry-and-changelog-roadmap-2026-03-24-0228]].
- **4.1.2** — First-person rig deterministic consume order vs **RegenLaneTotalOrder_v0** (**D-044**) — next tertiary after **4.1.1.x** task closure or operator **deepen** override.
- **4.1.3** — Presentation golden / Lane-C placeholder when **D-032** clears.

## Tertiary notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, handoff_readiness AS "Handoff"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems"
WHERE roadmap-level = "tertiary" AND contains(subphase-index, "4.1")
SORT subphase-index ASC
```
