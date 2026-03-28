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
handoff_readiness: 87
handoff_readiness_scope: "Player-first presentation spine (ARCH-FORK-02): read-model contracts from committed sim observables → PresentationViewState_v0 / CameraBinding_v0; no mutation via presentation path; T-P4-01…T-P4-05 bridge from 3.4.7; junior bundle + external CQRS/presentation framing (still below min_handoff_conf 93)"
execution_handoff_readiness: 42
handoff_gaps:
  - "**State hygiene (2026-03-26):** [[roadmap-state]] authoritative cursor text now matches [[workflow_state]] frontmatter (**`current_subphase_index` `4.1.2`**, **`last_auto_iteration` `force-forward-phase41-break-spin-gmm-20260326T203000Z`**) after repair queue **`repair-postlv-state-hygiene-gmm-20260326T210500Z`**; prior **4.1.1.10** cursor lines are explicitly historical only."
  - "**D-032 / D-043:** Literal replay header fields + golden presentation rows still **TBD** — normative text only until coordinated with **3.1.1** `replay_row_version`."
  - "**G-P*.*-REGISTRY-CI HOLD** on Phase **3.2.4** / **3.3.4** / **3.4.4** rollups **unchanged** by Phase 4 vault work (**D-062** traceability)."
  - "**Qualitative drift (`qualitative_audit_v0`):** **`drift_score_*` / `handoff_drift_*`** on [[roadmap-state]] are **not** numerically comparable across audits without a **versioned drift spec + input hash ([[drift-spec-qualitative-audit-v0]])** — see [[roadmap-state]] Notes **Drift scalar comparability**."
  - "**D-027:** Engine / language citations in examples remain illustrative unless a later decision adopts a stack."
links:
  - "[[distilled-core]]"
  - "[[workflow_state]]"
  - "[[roadmap-state]]"
  - "[[phase-4-perspective-split-and-control-systems-roadmap-2026-03-19-1101]]"
  - "[[phase-4-2-dm-perspective-read-model-and-rig-contracts-roadmap-2026-03-28-1200]]"
  - "[[phase-3-4-7-perspective-entry-wbs-and-phase-4-1-task-bridge-roadmap-2026-03-22-0748]]"
  - "[[phase-3-4-5-living-world-to-perspective-handoff-bridge-roadmap-2026-03-22-1205]]"
  - "[[phase-3-4-6-presentation-handoff-task-lanes-validation-harness-and-dm-promotion-roadmap-2026-03-22-1320]]"
  - "[[decisions-log]]"
  - "[[Ingest/Agent-Research/phase-4-1-secondary-player-first-read-rig-research-2026-03-24]]"
---

## Phase 4.1 — Player-first perspective read-model and rig contracts (secondary)

**Distilled-core ↔ active quaternary:** [[distilled-core]] · live **4.1.1.8** [[phase-4-1-1-8-operator-evidence-index-and-bundle-ingest-protocol-roadmap-2026-03-25-1200]] · bundle **4.1.1.7** [[phase-4-1-1-7-adapter-registry-rollup-handoff-bundle-and-closure-map-roadmap-2026-03-24-0926]] · machine cursor [[workflow_state]]

**Architect spine:** Operator pick **D-059 ARCH-FORK-02** — **player-first** perspective slice; **DM** shell is **not** in **4.1** MVP but is **authorized in parallel** on **4.2** per **D-131** ([[phase-4-2-dm-perspective-read-model-and-rig-contracts-roadmap-2026-03-28-1200]]). This secondary owns the **vault-normative** contract boundary for **player** presentation: inputs are **read-only** projections of **`SimObservableBundleTelemetry_v0`** / **`post_apply_observable_root`** and **`TickCommitRecord_v0`**-committed state (**3.1.6** / **3.1.1**), not a second mutation lane into **`AgencySliceApplyLedger_v0`** (**3.1.5**).

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
| **T-P4-04** | Replay/hash stub row | **`@skipUntil(D-032)`** — freeze **replay_row_version** / literal hash columns only after **3.1.1** coordination; Lane-C / **ReplayAndVerify** goldens **deferred** per **D-057** until **D-032** clears; **no** repo CI or **ReplayAndVerify** **PASS** claims in vault |
| **T-P4-05** | Handoff to DM shell (later) | Cross-link only — **not** executed in **4.1** first tranche |

### WBS → roll-up stub evidence map (vault-only — queue `resume-deepen-post-cursor-repair-p4-1-gmm-20260324T052800Z`)

> [!info] Validator anchor (non-normative)
> Compare-final **`.technical/Validator/roadmap-handoff-auto-genesis-mythos-master-20260324T130000Z-phase4-post-distilled-core-reconcile.md`** — **`primary_code: missing_roll_up_gates`**, **`needs_work`**. This subsection is **stub / traceability only**; it does **not** assert **HR ≥ 93**, **REGISTRY-CI PASS**, or repo-green **ReplayAndVerify**.

| WBS id | Linked roadmap artifact(s) | Stub evidence (what exists in vault today) | Explicit non-claims |
|--------|---------------------------|---------------------------------------------|---------------------|
| **T-P4-01** | [[phase-4-1-1-adapter-preimage-and-stable-column-layout-roadmap-2026-03-24-0018]] | Preimage / column table + upstream links to **3.1.6** / committed observables narrative | No golden row; no CI proof |
| **T-P4-02** | This note § Adapter → rig consume order; future **4.1.2** tertiary | Pseudo-code sketch only; **G-P4-1-RIG-NEXT** remains **FAIL (stub)** until adapter gate **PASS** | No rig implementation or harness green |
| **T-P4-03** | This note + [[decisions-log]] **D-058** | **SCOPED_VAULT** wording — package boundary without repo paths | No VCS layout assertions |
| **T-P4-04** | [[phase-4-1-1-1-adapter-row-layout-registry-and-changelog-roadmap-2026-03-24-0228]] | Registry / changelog sketch with **`@skipUntil(D-032)`** rows | No **replay_row_version** freeze; no Lane-C closure |
| **T-P4-05** | [[phase-3-4-6-presentation-handoff-task-lanes-validation-harness-and-dm-promotion-roadmap-2026-03-22-1320]] (cross-link) | Intent-only cross-link — **ARCH-FORK-02** defers DM shell | No DM promotion execution in **4.1** tranche |

### Honesty guards (**D-062**)

> [!warning] Operator advance vs rollup gates
> Macro **Phase 3 → 4** may be logged with **`wrapper_approved: true`** while rollup **`handoff_readiness` 92** remains **below** **`min_handoff_conf` 93** and **G-P*.*-REGISTRY-CI** remains **HOLD**. **Do not** treat Phase 4 deepen or this secondary as **REGISTRY-CI PASS** or automatic **HR 93** satisfaction.

### Risk register (v0)

| Risk | Mitigation |
|------|------------|
| Accidental sim writes from presentation path | CQRS labeling; code review gate; ledger writes only under **3.1.5** / **3.2.x** ordering (**D-044** Option A logged **2026-03-23**) |
| Hash preimage drift vs tick commit | Explicit `serialization_profile_id` + facet manifest intent (**D-037** defer) |
| Scope creep into DM free-cam | **ARCH-FORK-02** + **D-131** — DM belongs on **[[phase-4-2-dm-perspective-read-model-and-rig-contracts-roadmap-2026-03-28-1200]]**, not **4.1** MVP |

### Research integration (pre-deepen — **GMM-P4-1-SECONDARY-DEEPEN**)

Full synthesis: [[Ingest/Agent-Research/phase-4-1-secondary-player-first-read-rig-research-2026-03-24|phase-4-1-secondary-player-first-read-rig-research-2026-03-24]]. **Non-normative** industry framing; contracts stay on **3.1.x** / **decisions-log** / **D-032**/**D-043**/**D-037**.

- **Committed sim as read-model source:** `post_apply_observable_root` + `TickCommitRecord_v0` are the **authoritative snapshot**; adapter → rig → presentation are **CQRS-style query projections**, not writers to `AgencySliceApplyLedger_v0`.
- **Sim vs presentation cadence:** Simulation may advance **0..n times per rendered frame** (rollback / catch-up); presentation consumes the **latest committed** snapshot **once per frame** for cosmetics (interpolation, VFX) — see synthesis § SnapNet-style split.
- **Projection versioning:** Treat `adapter_row_layout_id`, `serialization_profile_id`, and **D-032**/**D-043** literal freeze as the vault analogue of CQRS projection schema evolution / tolerant readers.
- **Camera / rig:** Separate **replay-relevant** inputs (derivable from committed ticks only) from **D-027** UX-only presentation fields; prefer explicit `binding_id` + `world_anchor_ref` + facet subscription graph over hidden global mutable camera state.
- **Handoff gate (`min_handoff_conf` 93):** Secondary **HR 87** remains **below** bar; **rollup HR 92** and **G-P*.*-REGISTRY-CI HOLD** are **unchanged** by this vault edit (**D-062**).

### Adapter → rig consume order (vault sketch, mid-technical)

```text
// Pseudocode intent only — not repo-bound (T-P4-03 SCOPED_VAULT).
function BuildPresentationViewState_v0(tick_commit: TickCommitRecord_v0, observables: SimObservableBundleTelemetry_v0): PresentationViewState_v0 {
  assert_no_mutation_path_to_AgencySliceApplyLedger();  // CQRS: presentation is read side
  let preimage = canonical_preimage_rows(observables, serialization_profile_id);  // literals @skipUntil(D-032) where applicable
  return PresentationViewState_v0.from_committed(preimage, tick_commit.tick_id, tick_commit.commit_hash);
}

function ApplyCameraBinding_v0(pvs: PresentationViewState_v0, binding: CameraBinding_v0): RigPose_v0 {
  // Rig reads PresentationViewState_v0 only (T-P4-02). No sim writes.
  return RigPose_v0.resolve(binding.world_anchor_ref, pvs);
}
```

### Junior handoff bundle (checklist)

| # | Evidence required before claiming adapter→rig “done” in repo |
|---|----------------------------------------------------------------|
| 1 | **No write path** from presentation/rig into apply ledger (static scan + arch review). |
| 2 | Facet allow-list ⊆ **D-037** defer scope; no silent expansion. |
| 3 | Preimage in/out table on **4.1.1** aligned with **T-P4-01**; registry row on **4.1.1.1** carries **`@skipUntil(D-032)`** where literals absent. |
| 4 | Lane-C / **ReplayAndVerify** rows remain stubbed per **D-057** until **D-032** clears. |
| 5 | **D-062** copy deck: do **not** claim REGISTRY-CI PASS or rollup **HR ≥ 93** from Phase 4.1 work alone. |

> [!info] Executable acceptance (not closed)
> **T-P4-04** / Lane-C / **ReplayAndVerify** acceptance is **not satisfied** in any executable or CI-testable sense while **`@skipUntil(D-032)`** remains on the replay/hash stub row. Vault-only checklist items and interface tables **do not** substitute for literal **`replay_row_version`** + golden rows coordinated with **3.1.1**.

### Roll-up gate (4.1.1.x → 4.1.2) — measured stub

| Gate id | Status | Criterion | Evidence (vault) | Does **not** claim |
|---------|--------|-----------|------------------|-------------------|
| **G-P4-1-ADAPTER-CORE** | **FAIL (stub)** | **4.1.1** preimage table + **4.1.1.1** registry sketch aligned; open tasks carry **`@skipUntil`** owners | [[phase-4-1-1-adapter-preimage-and-stable-column-layout-roadmap-2026-03-24-0018]] preimage table · [[phase-4-1-1-1-adapter-row-layout-registry-and-changelog-roadmap-2026-03-24-0228]] registry / **`@skipUntil(D-032)`** rows | REGISTRY-CI **PASS**, rollup **HR ≥ 93**, or repo CI green |
| **G-P4-1-RIG-NEXT** | **FAIL (stub)** | **4.1.2** (**T-P4-02**) mint only after **G-P4-1-ADAPTER-CORE** row marked **PASS** on this note | *(blocked — upstream gate still* **FAIL (stub)** *)* | Advance-phase eligibility under **`min_handoff_conf` 93** |

#### Roll-up closure gaps (numbered)

1. **4.1.1** / **4.1.1.1** alignment and registry rows are **not** closed for macro rollup while **G-P*.*-REGISTRY-CI** remains **HOLD** and rollup **HR 92 < 93** (**D-062**).
2. **D-032** / **D-043** literal replay header + golden presentation columns remain **TBD**; normative text only until **3.1.1** `replay_row_version` coordination.
3. Lane-C / **ReplayAndVerify** rows remain **`@skipUntil(D-032)`** per **D-057**.

#### Acceptance criteria (vault-only, per gate — checkable from linked notes)

- **G-P4-1-ADAPTER-CORE:** [[phase-4-1-1-adapter-preimage-and-stable-column-layout-roadmap-2026-03-24-0018]] preimage table exists and cross-links **3.1.6** observables; [[phase-4-1-1-1-adapter-row-layout-registry-and-changelog-roadmap-2026-03-24-0228]] registry sketch lists **`@skipUntil(D-032)`** where literals absent; [[decisions-log]] picks (**D-044** A, **D-032** A, **D-059** ARCH-FORK-02) cited — **no** fabricated **PASS** rows.
- **G-P4-1-RIG-NEXT:** **4.1.2** note not minted until **G-P4-1-ADAPTER-CORE** shows **PASS** on **this** secondary (today: **FAIL (stub)**).

### Next (tertiary spine)

- **4.1.1** — Adapter preimage + stable column layout — **minted** [[phase-4-1-1-adapter-preimage-and-stable-column-layout-roadmap-2026-03-24-0018]]; **continued** with nested pre-deepen research + **4.1.1.1** task — queue **`resume-deepen-post-recal-p4-1-1-gmm-20260324T021500Z`**.
- **4.1.1.1** — Adapter row layout registry + **D-032** changelog hooks — **minted** [[phase-4-1-1-1-adapter-row-layout-registry-and-changelog-roadmap-2026-03-24-0228]].
- **4.1.2** — First-person rig deterministic consume order vs **RegenLaneTotalOrder_v0** (**D-044**) — **minted** [[phase-4-1-2-rig-consume-order-and-deterministic-binding-roadmap-2026-03-26-2100]] via BREAK-SPIN forward-only run.
- **4.1.3** — Control contracts + presentation golden placeholder lane — **minted** [[phase-4-1-3-control-contracts-and-presentation-golden-placeholder-roadmap-2026-03-26-2100]] with explicit `@skipUntil(D-032)` boundaries.
- **4.1.4** — Control read-model and golden-row selection contract — **minted** [[phase-4-1-4-control-read-model-and-golden-row-selection-contract-roadmap-2026-03-27-0320]] from 4.1.3 slice-exit to maintain forward-only conceptual progression.

> [!info] BREAK-SPIN forward-only update (2026-03-26 21:00)
> Operator guidance was honored: this pass advanced net-new 4.1 structure outside the `4.1.1.10` witness-appendix loop while preserving advisory hold language (rollup HR 92 < 93, REGISTRY-CI HOLD, missing_roll_up_gates).

## Tertiary notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, handoff_readiness AS "Handoff"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems"
WHERE roadmap-level = "tertiary" AND contains(subphase-index, "4.1")
SORT subphase-index ASC
```
