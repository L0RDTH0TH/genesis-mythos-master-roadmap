---
title: Phase 4.1.1 — Adapter preimage and stable column layout
roadmap-level: tertiary
phase-number: 4
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-24
tags: [roadmap, genesis-mythos-master, phase-4, perspective, adapter, t-p4-01]
para-type: Project
subphase-index: "4.1.1"
handoff_readiness: 91
handoff_readiness_scope: "T-P4-01: Presentation adapter preimage from committed sim observables; stable column layout aligned with 3.1.1 replay_row_version stub — literals @skipUntil(D-032/D-043)"
execution_handoff_readiness: 32
handoff_gaps:
  - "**D-032 / D-043:** Replay header literals + presentation golden rows **TBD** — adapter table uses **normative column names only**."
  - "**3.1.1:** `replay_row_version` / tick preimage field freeze — cross-link only until operator coordinates."
  - "**G-P*.*-REGISTRY-CI HOLD** unchanged by this tertiary (**D-062**)."
links:
  - "[[phase-4-1-player-first-perspective-read-model-and-rig-contracts-roadmap-2026-03-24-1201]]"
  - "[[phase-4-perspective-split-and-control-systems-roadmap-2026-03-19-1101]]"
  - "[[phase-3-1-1-deterministic-tick-epoch-and-hash-preimage-boundaries-roadmap-2026-03-22-0015]]"
  - "[[Ingest/Agent-Research/phase-4-primary-perspective-control-research-2026-03-24]]"
  - "[[Ingest/Agent-Research/phase-4-1-1-adapter-preimage-stable-layout-cqrs-research-2026-03-23-2205]]"
  - "[[decisions-log]]"
---

## Phase 4.1.1 — Adapter preimage and stable column layout (tertiary)

**Spine:** **T-P4-01** from [[phase-4-1-player-first-perspective-read-model-and-rig-contracts-roadmap-2026-03-24-1201]] — freeze the **vault-normative** boundary: which **committed** sim artifacts feed `PresentationViewState_v0` / `CameraBinding_v0`, and the **stable column layout** for adapter rows (hash inputs, profile ids, binding ids) pending **3.1.1** replay preimage coordination.

### TL;DR

- Adapter consumes **only** post-barrier observables and tick-committed state (**3.1.6** / **3.1.1** narrative); **no** write-back into **`AgencySliceApplyLedger_v0`** (**3.1.5**).
- Column layout is **versioned** (`adapter_row_layout_id`) and **hash-stable** under `serialization_profile_id` once **D-032** clears — until then, **sketch + @skipUntil(D-032)**.
- **ARCH-FORK-02** (**D-059**): player-first; DM tooling columns **out of scope** for this tertiary.

### Preimage authority table (v0)

| Column (normative name) | Source (vault intent) | Replay inclusion |
|-------------------------|----------------------|------------------|
| `tick_id` | `TickCommitRecord_v0` | Yes (when literal row exists) |
| `post_apply_observable_root` hash | **3.1.6** bundle | Yes |
| `serialization_profile_id` | Facet manifest intent (**D-037** defer) | Yes |
| `presentation_stable_inputs` | Derived allow-list from committed facets | Yes |
| `camera_binding_id` | `CameraBinding_v0` stable id | Yes |
| `fov_lod_parameters` | `PresentationViewState_v0` (presentation-only) | Lane-C **`@skipUntil(D-032)`** |

### Algorithm sketch (adapter build — mid-technical)

```text
function BuildPresentationAdapterRow(tick_id, committed_bundle, profile_id) -> AdapterRow_v0:
  assert committed_bundle.phase == "post_apply"  // 3.1.6 barrier
  preimage = CanonicalizeForProfile(committed_bundle, profile_id)
  return AdapterRow_v0{
    tick_id,
    observable_root_hash = Hash(preimage.root, profile_id),
    serialization_profile_id = profile_id,
    camera_binding_id = committed_bundle.binding_id,
    presentation_stable_inputs = preimage.allow_list_columns,
    // fov_lod_parameters omitted until D-032 literal contract
  }
```

### Research integration

#### Key takeaways

- **Layout + preimage:** Keep **normative column names** in the adapter table; version **`adapter_row_layout_id`** and align with **3.1.1** **`replay_row_version`** when stub rows freeze — no silent renames vs rollups.
- **Profiles:** **`serialization_profile_id`** (D-037 intent) governs canonical bytes for **`post_apply_observable_root`** / observable hashes; until manifest + registry are frozen, vault text stays **intent-only** for CI stability.
- **CQRS:** **`PresentationViewState_v0` / `CameraBinding_v0` / adapter rows** are **read models** over **post_apply** committed bundles; **do not** write **`AgencySliceApplyLedger_v0`** from presentation.
- **Deferrals:** **`@skipUntil(D-032)`** / **`@skipUntil(D-043)`** for literals and preimage formulas; **D-045** covers **3.2.3** regen **ReplayAndVerify** deferrals — separate from **4.1.1** Lane-C skips.
- **Honesty:** Rollup **handoff_readiness 92** remains **below `min_handoff_conf` 93**; **G-P\*.\*-REGISTRY-CI** stays **HOLD** per **[[roadmap-state]]** — **no** narrative that registry CI **PASS** clears advance gates.

#### Decisions / constraints

- On **D-032** clearance: add explicit **changelog** tying **`adapter_row_layout_id`**, new replay columns, and **`TickCommitRecord_v0`** field names.

#### Links

- [[Ingest/Agent-Research/phase-4-1-1-adapter-preimage-stable-layout-cqrs-research-2026-03-23-2205]]
- [[Ingest/Agent-Research/phase-4-primary-perspective-control-research-2026-03-24]]

#### Sources

- Full synthesis + hostile validation trace: [[Ingest/Agent-Research/phase-4-1-1-adapter-preimage-stable-layout-cqrs-research-2026-03-23-2205]] (nested `research_synthesis` Validator→IRA→Validator per Research return).

#### Child task (quaternary)

- **4.1.1.1** — [[phase-4-1-1-1-adapter-row-layout-registry-and-changelog-roadmap-2026-03-24-0228]] — registry sketch + D-032 changelog hooks.
- **4.1.1.8** — [[phase-4-1-1-8-operator-evidence-index-and-bundle-ingest-protocol-roadmap-2026-03-25-1200]] — evidence-bundle ingest protocol (follows **4.1.1.7** closure map).

### Tasks

- [x] Integrate pre-deepen research (`resume-deepen-post-recal-p4-1-1-gmm-20260324T021500Z`) — [[Ingest/Agent-Research/phase-4-1-1-adapter-preimage-stable-layout-cqrs-research-2026-03-23-2205]]; cite Layer-1 compare **`.technical/Validator/roadmap-handoff-auto-genesis-mythos-master-20260324T020000Z-layer1-post-deepen-001800Z.md`** when reconciling HR **92** vs **93**.
- [ ] Align adapter column names with **3.1.1** stub row (no silent rename vs rollup tables) — `@skipUntil(D-032/D-043, 3.1.1 stub row literal freeze)`
- [ ] Document **@skipUntil(D-032)** for any presentation-only golden column — `@skipUntil(D-032, Lane-C literal contract)`
- [ ] Cross-check **RegenLaneTotalOrder_v0** (**D-044** Option A) — adapter read order does not introduce a second ordering lane — `@skipUntil(D-045, regen golden rows + TickCommitRecord field alignment)`
- [ ] Close **4.1.1.1** task checklist when **`adapter_row_layout_id`** registry sketch is accepted — `@skipUntil(task-4.1.1.1, quaternary task checklist completion)`

### Parent

- **Secondary:** [[phase-4-1-player-first-perspective-read-model-and-rig-contracts-roadmap-2026-03-24-1201]]
