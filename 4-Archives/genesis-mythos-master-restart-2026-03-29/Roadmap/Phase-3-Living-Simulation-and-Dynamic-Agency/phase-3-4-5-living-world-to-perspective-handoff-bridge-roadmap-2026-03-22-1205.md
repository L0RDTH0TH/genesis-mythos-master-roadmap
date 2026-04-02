---
title: Phase 3.4.5 — Living world → perspective handoff bridge
roadmap-level: tertiary
phase-number: 3
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-22
tags: [roadmap, genesis-mythos-master, phase, living-world, phase-4, presentation, handoff-bridge]
para-type: Project
subphase-index: "3.4.5"
handoff_readiness: 84
handoff_readiness_scope: "Vault-normative bridge from committed sim observables (3.1.6 / 3.4.x) to Phase 4 presentation (FPV / DM tools); explicit non-authoritative presentation layer vs TickCommitRecord_v0; D-044 still HOLD for any same-tick DM/regen/ambient interleaving claims"
execution_handoff_readiness: 40
handoff_gaps:
  - "Literal `PresentationViewState_v0` / `CameraBinding_v0` field rows + golden replay coupling still TBD until D-032 / D-043 / operator D-044"
  - "Phase 4 primary checklists remain un-owned by this tertiary — this note scopes **contract boundary** only"
links:
  - "[[phase-3-4-living-world-operations-and-consequence-fan-out-roadmap-2026-03-23-1210]]"
  - "[[phase-3-4-4-phase-3-4-secondary-closure-rollup-and-advance-readiness-roadmap-2026-03-23-1935]]"
  - "[[phase-3-1-6-tick-scoped-observable-bundle-post-apply-replay-bridge-roadmap-2026-03-22-0047]]"
  - "[[phase-4-perspective-split-and-control-systems-roadmap-2026-03-19-1101]]"
  - "[[decisions-log]]"
  - "[[distilled-core]]"
---

## Phase 3.4.5 — Living world → perspective handoff bridge

**TL;DR:** Define the **read-model boundary** between **committed simulation state** (`post_apply_observable_root`, facet allow-list, `TickCommitRecord_v0`) and **Phase 4** cameras / DM tooling so presentation never silently becomes a co-author of tick ordering. DM free-cam and player FPV consume **derived** `PresentationViewState_v0`; only explicit **`MutationIntent_v0`** / regen paths participate in **3.1.5** / **3.2.x** ordering.

### Objectives

1. Classify Phase 4 inputs as **view-only**, **preview overlay**, or **intent producers** — only the third may append to **`AgencySliceApplyLedger_v0`** with stable IDs.
2. Bind **camera / tool subscriptions** to **facet_manifest_id** allow-list output from **3.4.3** / **D-037** — no direct preimage holes.
3. Preserve **D-027**: wall-clock and render frame rate affect **UX interpolation only**, not committed hashes.

### Contract sketch (draft)

| Artifact | Role | Replay authority |
|----------|------|------------------|
| `PresentationViewState_v0` | Derived pose, blend weights, non-committing extrapolation | **Non-authoritative** |
| `CameraBinding_v0` | Role → facet subscription graph | **Non-authoritative** |
| `ToolActionQueue_v0` (optional) | DM actions **before** promotion to `MutationIntent_v0` | **Staging only** until promoted; bounded stub — see **ToolActionQueue_v0 bounds** below |

### `PresentationViewState_v0` — field rows (draft)

| field | type | authoritative? | in `TickCommitRecord_v0` preimage? | notes |
| --- | --- | --- | --- | --- |
| `derived_pose_hash` | `u256` or bytes32 stub | no | **excluded** — presentation-only | Hash of interpolated view state; must not feed sim preimage |
| `interpolation_alpha_q16` | `u16` | no | **excluded** | UX smoothing; wall-clock derived per **D-027** |
| `active_camera_role_id` | string enum stub | no | **excluded** | Maps to `CameraBinding_v0` |
| `presentation_tick_seq` | `u64` | no | **excluded** | Render-frame counter; independent of `tick_epoch` |

### `CameraBinding_v0` — field rows (draft)

| field | type | authoritative? | preimage / facet | notes |
| --- | --- | --- | --- | --- |
| `binding_id` | `u128` or uuid stub | no | n/a | Stable id for DM / player rig |
| `subscribed_facet_ids` | list of `facet_manifest_id` | no | **must** ⊆ **3.4.3** / **D-037** allow-list | No direct holes into disallowed facets |
| `world_anchor_ref` | cell / entity ref stub | no | read-only vs last committed observables | Must not imply new mutation path |

### ToolActionQueue_v0 bounds (draft)

- **`tool_action_queue_schema_id`:** `TAQ_V0_DRAFT` (explicit version stub).
- **`max_queued_actions`:** bounded integer (default **TBD** by operator; placeholder **64** in examples only).
- **`tool_action_idempotency_key`:** required on enqueue; duplicate key → no-op / ledger-hit semantics **TBD** with **3.1.5** `mutation_id` patterns — deferral tracked on **3.4.6** **T-DM-P02** ([[phase-3-4-6-presentation-handoff-task-lanes-validation-harness-and-dm-promotion-roadmap-2026-03-22-1320]] § Execution / DEFERRED ledger).
- **Promotion gate:** only **`MutationIntent_v0`** (or approved DM path) may append to **`AgencySliceApplyLedger_v0`**; queue entries **never** appear in **`TickCommitRecord_v0`** until promoted and ordered per **3.2.x** / **D-044**.

### Acceptance observables (non-golden)

Doc-level checks (vault-honest; not **ReplayAndVerify** until **D-032** / **D-043**):

1. This note’s **field tables** contain an explicit **excluded-from-preimage** row for every `PresentationViewState_v0` field listed.
2. **`CameraBinding_v0.subscribed_facet_ids`** is stated to reference only **`facet_manifest_id`** values in scope of **D-054** / **D-037** (no new facet namespace).
3. **ToolActionQueue_v0** section states **non-participation** in **`TickCommitRecord_v0`** until promotion + ordering gates.

### DEFERRED ledger (inventory)

| item | owner | blocked_by | unblock IDs / notes |
| --- | --- | --- | --- |
| Presentation / camera golden row | eng + operator | replay header freeze | **D-032**, **D-043** |
| Literal preimage coupling for presentation hashes | eng | header + row versioning | **D-032**, **3.1.1** `replay_row_version` |
| Same-tick DM / regen / ambient story | operator | regen policy fork | **D-044** |
| Mixed-tick ambient CI registry rows | eng | registry policy | **2.2.3**, **D-020**, **G-P3.4-REGISTRY-CI** |

### Dependencies

- **D-044** — any narrative that places **DM tool apply** in the **same** `tick_epoch` as **regen** or **ambient scalars** stays **dual-track / provisional** until **RegenLaneTotalOrder_v0** A/B is logged.
- **D-055** — **G-P3.4-*** rollup remains authoritative for **3.4** secondary closure; this tertiary **does not** re-open PASS rows.

## Research integration

### Key takeaways

- **Sim vs render:** Use a **fixed-tick sim** and a **variable-rate presentation** layer; leftover frame time becomes interpolation/extrapolation **alpha** for visuals only — not new ledger rows. See [Fix Your Timestep!](https://gafferongames.com/post/fix_your_timestep/).
- **Observable bundle as read model:** Treat **`post_apply_observable_root`** / facet allow-list output as the **authoritative snapshot** Phase 4 cameras consume; camera pose, VFX, and audio belong in **presentation**, which should run **once per rendered frame** while sim may advance **0..n** times per frame in networked/rollback-style designs. See [Simulation vs. Presentation | SnapNet](https://snapnet.dev/docs/core-concepts/simulation-vs-presentation/).
- **DM tools:** Decide explicitly whether free-cam / ortho tools are **(A)** view-only over last committed observables, **(B)** preview that never commits, or **(C)** **`MutationIntent_v0`** producers; **C** must use the same ordering/regen story as ambient slices (**D-044** still HOLD).
- **Contract candidates (draft):** `PresentationViewState_v0` (derived, non-replay-authoritative), `CameraBinding_v0` (role → facet subscriptions), optional `ToolActionQueue_v0` for DM actions that become intents.

### Decisions / constraints

- **Do not** let presentation layers append to **`AgencySliceApplyLedger_v0`** or alter **`TickCommitRecord_v0`** preimage without going through defined mutation / DM-overwrite paths (**3.2.x**).
- **Preserve D-027:** presentation may use wall time for **UX only**; it must not leak into committed sim preimage or observable hashing.
- **Regen interleaving:** Until **D-044** is resolved, any story that mixes **DM tool application** with ambient/regen in the **same** `tick_epoch` should stay **dual-track / provisional** like **3.4.2–3.4.4**.

### Links

- [[Ingest/Agent-Research/phase-3-4-5-sim-presentation-camera-bridge-research-2026-03-22-1245|Full synthesis note]]
- **Next sibling (execution decomposition):** [[phase-3-4-6-presentation-handoff-task-lanes-validation-harness-and-dm-promotion-roadmap-2026-03-22-1320]] (**D-057**)
- Related vault: [[phase-3-1-6-tick-scoped-observable-bundle-post-apply-replay-bridge-roadmap-2026-03-22-0047]], [[phase-4-perspective-split-and-control-systems-roadmap-2026-03-19-1101]]

## Tasks

- [ ] Publish **`PresentationViewState_v0`** field stub (non-authoritative) + explicit exclusion from `TickCommitRecord_v0` preimage table
- [ ] Publish **`CameraBinding_v0`** row linking **Phase 4** rig goals to **facet_manifest_id** subscriptions (**D-054** / **D-037**)
- [ ] **DEFERRED (D-044)** — Dual-track note: DM tool → intent promotion vs same-tick regen/ambient remains **provisional** until operator logs **RegenLaneTotalOrder_v0** A/B
- [ ] **DEFERRED (goldens)** — No `ReplayAndVerify` row for presentation until **D-032** / **D-043** replay header freeze

## Pseudo-code — presentation tick (non-authoritative)

```text
on_render_frame(dt_real):
  committed = last_tick.TickCommitRecord_v0.committed_sim_observable_hash
  view = PresentationViewState_v0.interpolate(
    from_state = sim_read_model(committed),
    alpha = clamp(dt_real / presentation_smoothing_budget, 0, 1)
  )
  // view MUST NOT write AgencySliceApplyLedger_v0
  render(view)
```
