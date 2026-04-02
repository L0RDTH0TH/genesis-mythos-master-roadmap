---
title: Phase 4.2 — DM perspective read-model and rig contracts
roadmap-level: secondary
phase-number: 4
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-28
tags: [roadmap, genesis-mythos-master, phase, perspective, dm, free-cam, orthographic, cqrs]
para-type: Project
subphase-index: "4.2"
handoff_readiness: 82
handoff_readiness_scope: "DM presentation slice (D-131 parallel to 4.1): read-model contracts from committed sim observables → DmPresentationViewState_v0 / DmCameraBinding_v0; ToolActionQueue_v0 staging per 3.4.6; no mutation via presentation path; below min_handoff_conf 93; execution rollup/REGISTRY-CI advisory unchanged (D-062)"
execution_handoff_readiness: 38
handoff_gaps:
  - "**D-032 / D-043:** Literal replay header + golden DM presentation rows **TBD** — same deferral contract as **4.1**."
  - "**G-P*.*-REGISTRY-CI HOLD** and rollup **HR 92 < 93** unchanged by vault prose on **4.2** (**D-062**)."
  - "**DmCameraBinding_v0** vs **`CameraBinding_v0`** replay parity: **TBD** until coordinated literals with **3.1.1** / **D-032**."
  - "**T-DM-P01–P05** promotion state machine: vault-normative IDs only until execution harness lands (**3.4.6**)."
links:
  - "[[distilled-core]]"
  - "[[workflow_state]]"
  - "[[roadmap-state]]"
  - "[[phase-4-perspective-split-and-control-systems-roadmap-2026-03-19-1101]]"
  - "[[phase-4-1-player-first-perspective-read-model-and-rig-contracts-roadmap-2026-03-24-1201]]"
  - "[[decisions-log]]"
  - "[[phase-3-4-5-living-world-to-perspective-handoff-bridge-roadmap-2026-03-22-1205]]"
  - "[[phase-3-4-6-presentation-handoff-task-lanes-validation-harness-and-dm-promotion-roadmap-2026-03-22-1320]]"
  - "[[Ingest/Agent-Research/phase-4-2-dm-perspective-read-model-research-2026-03-28-2330]]"
---

## Phase 4.2 — DM perspective read-model and rig contracts (secondary)

**Distilled-core / state:** [[distilled-core]] · [[workflow_state]] · [[roadmap-state]]

**Authority:** [[decisions-log]] **D-131** — DM shell **conceptual** slice **in parallel** with **4.1**; **4.1** remains **player-first only** (**ARCH-FORK-02**); **no widening** of **4.1** MVP.

**Architect spine:** Same CQRS split as **4.1**: **`SimObservableBundleTelemetry_v0`** / **`post_apply_observable_root`** + **`TickCommitRecord_v0`** are the **read-model source**; **`DmPresentationViewState_v0`** and **`DmCameraBinding_v0`** are **query-side** projections; **`AgencySliceApplyLedger_v0`** is **not** reachable from DM presentation builders. DM **authoring** flows that must affect the sim route through **`ToolActionQueue_v0`** → promoted **`MutationIntent_v0`** per **3.4.5** / **3.4.6** and **D-044** Option A — not through camera or view-state mutators.

### Objectives

- Freeze **DM facet** semantics for **`dm_view_mode`**: **free-cam** vs **orthographic tabletop** (inputs, preimage columns, UX-only vs replay-candidate fields per **D-027**).
- Specify **`mode_transition_envelope_v0`** (working name) at the **presentation** boundary: duration, easing profile id, interrupt policy; default **`replay_relevant: false`** until **D-032** absorbs parameters.
- Map **T-DM-P01–P05** from [[phase-3-4-6-presentation-handoff-task-lanes-validation-harness-and-dm-promotion-roadmap-2026-03-22-1320]] into **checkable WBS leaves** (this note) without executing DM promotion inside **4.1**.
- Preserve **explicit non-claims:** no **PASS** on **G-P*.*-REGISTRY-CI**, no rollup **HR ≥ 93**, no Lane-C / **ReplayAndVerify** green from vault text alone.

### Interface table (v0)

| Artifact | Role | Upstream | Downstream | Status |
|----------|------|----------|------------|--------|
| `DmPresentationViewState_v0` | DM FOV / mode / facet hooks / tooling read surface | Committed observables + tick commit (same as **4.1**) | DM rig + DM UI read pipeline | Draft — literals **`@skipUntil(D-032)`** |
| `DmCameraBinding_v0` | DM rig ↔ world anchor (tabletop bounds / free-cam orbit) | Same + **3.4.x** commits | Deterministic DM camera replay (future golden) | Draft — parity vs **`CameraBinding_v0` TBD** |
| `ToolActionQueue_v0` | **Staging** for DM actions before promotion | **3.4.6** | **`MutationIntent_v0`** / **3.1.5** when promoted | Normative intent — not a presentation write |
| `mode_transition_envelope_v0` | Interpolation / easing / interrupt policy | UX layer | Presentation-only unless **D-032** expands replay | Draft |

### WBS trace (checkable leaves)

| ID | Intent | Evidence expectation |
|----|--------|----------------------|
| **T-DM-P01** | Promotion state machine | Vault table: idle → staged → gated → promoted; link **3.4.6** |
| **T-DM-P02** | Idempotency + denial codes | Reason codes aligned with **2.2.x** / regen taxonomy where applicable |
| **T-DM-P03** | Preconditions / merge gates | **regen-before-merge** / **D-044** ordering cited; no new merge semantics |
| **T-DM-P04** | **Preview** vs **Apply** | **Preview** must not enqueue promotion; **Apply** may stage **ToolActionQueue_v0** |
| **T-DM-P05** | Telemetry + audit | DM tool traces observable in vault sketch; **`@skipUntil(D-032)`** for literal rows |

### WBS → roll-up stub evidence map (vault-only)

> [!info] Validator anchor (non-normative)
> This subsection is **stub / traceability only**; it does **not** assert **HR ≥ 93**, **REGISTRY-CI PASS**, or repo-green **ReplayAndVerify**.

| WBS id | Linked roadmap artifact(s) | Stub evidence (vault today) | Explicit non-claims |
|--------|---------------------------|----------------------------|---------------------|
| **T-DM-P01–P03** | This note + [[phase-3-4-6-presentation-handoff-task-lanes-validation-harness-and-dm-promotion-roadmap-2026-03-22-1320]] | Lane **B/C** intent echoed; promotion table in prose | No harness **PASS** |
| **T-DM-P04** | This note § CQRS pseudocode | Preview/Apply split stated | No executable closure |
| **T-DM-P05** | This note § Junior bundle | Checklist row | No CI telemetry proof |

### Honesty guards (**D-062**)

> [!warning] Operator advance vs rollup gates
> **4.2** vault work does **not** clear **G-P*.*-REGISTRY-CI** or raise macro rollup to **`min_handoff_conf` 93**. **G-P4-DM-SHELL** on [[phase-4-perspective-split-and-control-systems-roadmap-2026-03-19-1101]] stays **OPEN** for prose, not implementation closure.

### Risk register (v0)

| Risk | Mitigation |
|------|------------|
| Accidental sim writes from DM presentation / “god camera” tooling | CQRS labeling; static review; **`assert_no_mutation_path_to_AgencySliceApplyLedger`** pattern in pseudocode |
| Collapsing **Preview** into **Apply** | **T-DM-P04** checklist; promotion state machine |
| Scope creep into **4.1** player-first MVP | **D-131** + **ARCH-FORK-02** — player contracts stay on **4.1** only |
| Orthographic / free-cam preimage drift vs tick commit | Same **`serialization_profile_id`** + facet rules as **4.1**; **D-037** defer |

### Research integration (pre-deepen — **resume-deepen-phase4-2-dm-research-ctx-gmm-20260328T230000Z**)

**Key takeaways**

- DM **free-cam** vs **orthographic tabletop** are **presentation facets** on the same **committed** sim observables; they are not alternate write lanes.
- **CQRS:** **`DmPresentationViewState_v0`** / **`DmCameraBinding_v0`** are **read-side**; **`ToolActionQueue_v0`** is **staging**; **`AgencySliceApplyLedger_v0`** only via promoted **`MutationIntent_v0`** (**3.1.5** / **D-044**).
- **T-DM-P01–P05:** deepen threads **promotion state machine**, **idempotency**, **gates**, **Apply vs Preview**, and **telemetry** without collapsing presentation into the queue.
- **Mode transitions:** use a **presentation envelope** (duration, easing profile id, interrupt policy); do not conflate transition smoothing with tick/decision boundaries (**D-032** if replay ever absorbs transition params).
- **D-060 (conceptual_v1):** use this block to **deepen forward**; do not **`recal`** solely for execution-advisory rollup/CI signals unless a **hard** coherence stop applies — authoritative **D-060** text remains in **[[decisions-log]]**.

**Decisions / constraints**

- Keep **4.1** **player-first** MVP unchanged; all DM shell depth stays on **4.2** (**D-131**).
- **`DmCameraBinding_v0`** vs **`CameraBinding_v0`** replay parity: **TBD** until literals; see full synthesis §3b stub.
- **Non-claims:** replay columns, golden rows, registry CI unchanged vs **4.1** (**D-032** / **D-043**).

**Links**

- Full synthesis: [[Ingest/Agent-Research/phase-4-2-dm-perspective-read-model-research-2026-03-28-2330]]
- Mirror pattern: [[Ingest/Agent-Research/phase-4-1-secondary-player-first-read-rig-research-2026-03-24]]
- Bridges: [[phase-3-4-5-living-world-to-perspective-handoff-bridge-roadmap-2026-03-22-1205]], [[phase-3-4-6-presentation-handoff-task-lanes-validation-harness-and-dm-promotion-roadmap-2026-03-22-1320]]

### DM adapter → rig consume order (vault sketch)

```text
// Pseudocode intent only — SCOPED_VAULT (T-P4-03 pattern applies by analogy).
function BuildDmPresentationViewState_v0(
  tick_commit: TickCommitRecord_v0,
  observables: SimObservableBundleTelemetry_v0,
  dm_view_mode: enum { FREE_CAM, ORTHO_TABLETOP }
): DmPresentationViewState_v0 {
  assert_no_mutation_path_to_AgencySliceApplyLedger();
  let preimage = canonical_dm_preimage_rows(observables, dm_view_mode, serialization_profile_id);
  return DmPresentationViewState_v0.from_committed(preimage, tick_commit.tick_id, tick_commit.commit_hash, dm_view_mode);
}

function ApplyDmCameraBinding_v0(dm_pvs: DmPresentationViewState_v0, binding: DmCameraBinding_v0): DmRigPose_v0 {
  // Rig reads DmPresentationViewState_v0 only. No sim writes.
  return DmRigPose_v0.resolve(binding.world_anchor_ref, dm_pvs);
}

// DM tools that change world state: enqueue ToolActionQueue_v0 entries; never write ledger from this path.
```

### Conceptual handoff checklist (NL)

- **Scope:** **4.2** DM presentation read-models, rigs, and mode transitions; **out of scope:** **4.1** player-first contracts, new merge/regen semantics, repo layout.
- **Behavior:** Per tick, DM views consume **latest committed** snapshot once per frame for cosmetics; **Apply** paths stage **`ToolActionQueue_v0`**; ledger mutations only after promotion.
- **Interfaces:** Upstream **3.1.6** / **3.1.1**; lateral **4.1** (parity, not scope expansion); downstream **3.4.6** task IDs.
- **Edge cases:** Mid-transition tick advance → snap or cancel envelope per **interrupt_policy** (TBD enum); regen-before-merge still **D-044**.
- **Open questions:** Which envelope fields (if any) become **D-032** replay literals; exact **`DmCameraBinding_v0`** field parity with **`CameraBinding_v0`**.
- **Pseudo-code readiness:** Builders above are sufficient to start implementation sketches without inventing a second write lane.

### Junior handoff bundle (checklist)

| # | Evidence required before claiming DM adapter→rig “done” in repo |
|---|------------------------------------------------------------------|
| 1 | **No write path** from DM presentation/rig into **`AgencySliceApplyLedger_v0`**. |
| 2 | **Preview** tools cannot promote to **`MutationIntent_v0`** without explicit **Apply** / gate pass (**T-DM-P04**). |
| 3 | **`ToolActionQueue_v0`** staging documented; ordering vs **D-044** cited. |
| 4 | **`@skipUntil(D-032)`** on literal replay columns where absent (same as **4.1**). |
| 5 | **D-062** copy deck: no **REGISTRY-CI PASS** or rollup **HR ≥ 93** claims from **4.2** prose. |

### Roll-up gate (4.2 → future DM tertiary spine) — measured stub

| Gate id | Status | Criterion | Evidence (vault) | Does **not** claim |
|---------|--------|-----------|------------------|-------------------|
| **G-P4-DM-READ-MODEL** | **FAIL (stub)** | WBS **T-DM-P01–P05** rows + interface table + CQRS pseudocode | This note | REGISTRY-CI **PASS**, HR **≥ 93** |
| **G-P4-DM-SHELL** | **OPEN** | Primary Phase 4 row + cross-links | [[phase-4-perspective-split-and-control-systems-roadmap-2026-03-19-1101]] | Implementation closure |

#### Roll-up closure gaps (numbered)

1. Literal replay + golden rows **TBD** (**D-032** / **D-043**).
2. **REGISTRY-CI HOLD** on upstream rollups unchanged (**D-062**).
3. **T-DM-P*** executable harness remains **3.4.6** execution debt, not **4.2** conceptual completion bar.

### Next (tertiary spine — not minted this run)

- Future **4.2.1+** tertiaries may expand preimage tables and registry rows **without** moving **4.1** scope.

## Tertiary notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, handoff_readiness AS "Handoff"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems"
WHERE (roadmap-level = "tertiary" OR roadmap-level = "task") AND contains(subphase-index, "4.2")
SORT subphase-index ASC
```
