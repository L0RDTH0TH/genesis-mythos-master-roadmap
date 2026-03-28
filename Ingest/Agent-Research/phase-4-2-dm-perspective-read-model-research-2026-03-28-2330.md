---
title: Phase 4.2 secondary — DM perspective read-model, CQRS, and mode transitions (research)
research_query: "DM free-cam and orthographic tabletop read-models over committed sim observables; CQRS boundary vs ToolActionQueue promotion; presentation mode-transition contracts; alignment with 3.4.5/3.4.6 T-DM-P01–P05"
linked_phase: "Phase 4.2 — DM perspective read-model and rig contracts"
project_id: genesis-mythos-master
created: 2026-03-28
tags: [research, agent-research, genesis-mythos-master, phase-4-2, dm, cqrs, presentation, orthographic]
para-type: Resource
agent-generated: true
research_tools_used: [vault_context, web_search, mcp_web_fetch]
research_escalations_used: 0
parent_handoff: "Roadmap nested research — resume-deepen phase 4.2 DM pre-deepen"
queue_entry_id: resume-deepen-phase4-2-dm-research-ctx-gmm-20260328T230000Z
pipeline_task_correlation_id: 46b74531-4e3d-4951-a400-ec862791eafe
---

# Phase 4.2 — DM presentation read-models (industry framing)

**Scope:** Non-normative synthesis for **[[phase-4-2-dm-perspective-read-model-and-rig-contracts-roadmap-2026-03-28-1200]]** (**D-131** sibling to **4.1**). **Authoritative** contracts remain **[[decisions-log]]**, **3.1.x**, **[[phase-3-4-5-living-world-to-perspective-handoff-bridge-roadmap-2026-03-22-1205]]**, **[[phase-3-4-6-presentation-handoff-task-lanes-validation-harness-and-dm-promotion-roadmap-2026-03-22-1320]]**, and **[[phase-4-1-player-first-perspective-read-model-and-rig-contracts-roadmap-2026-03-24-1201]]**.

**Decision-ID pointer:** References to **D-027**, **D-044**, and **D-060** here are **shorthand** only; authoritative text lives in **[[1-Projects/genesis-mythos-master/Roadmap/decisions-log]]** (search by id). This research note does **not** restate or amend those decisions.

## Vault anchor — do not duplicate

- **4.2 secondary** already states: mirror **4.1** pattern — committed sim observables + tick commits as read-model source; **no** mutation from DM presentation/tooling into **`AgencySliceApplyLedger_v0`**; **`DmPresentationViewState_v0`** / **`DmCameraBinding_v0`** working names; mode transition envelope stub; **non-claims** for replay/golden/registry CI under **D-032** / **D-043** same as **4.1**.
- **4.1 research** (**[[Ingest/Agent-Research/phase-4-1-secondary-player-first-read-rig-research-2026-03-24]]**) already covers generic CQRS presentation split, SnapNet-style sim vs frame, and rig/replay hygiene — this note **extends** that framing to **DM-specific** projections and **staging vs promotion** (**`ToolActionQueue_v0`**).
- **3.4.5** classifies DM tools as **(A)** view-only, **(B)** preview non-commit, or **(C)** **`MutationIntent_v0`** — **C** must use **3.1.5** ordering (**D-044**).
- **3.4.6** defines **T-DM-P01–P05** (promotion state machine, idempotency, gates, Apply vs Preview UX, telemetry) — all **DEFERRED** ledger tasks; DM **presentation** in **4.2** should remain **orthogonal** until promotion is explicit.

## 1. Two DM “cameras” as read-model facets, not write lanes

**Orthographic vs perspective (engines):** Orthographic projection uses a parallel viewing volume (uniform scale with depth); perspective uses a frustum. Tabletop / map-style DM views typically favor **orthographic** or **parallel** mappings for grid alignment; **free-cam** often behaves like a **perspective** rig with different input semantics. Both are **rendering / presentation choices** layered on top of **committed** world state — they do not, by themselves, define tick authority.

[Source: Unity — Cameras overview](https://docs.unity3d.com/Manual/CamerasOverview.html) *(current Manual; legacy versioned path `…/530/…` retained in Sources for traceability — verify if links rot)*

[Source: Unreal Engine — Orthographic camera](https://dev.epicgames.com/documentation/en-us/unreal-engine/orthographic-camera-in-unreal-engine)

**Map to vault:** Treat **`DmPresentationViewState_v0`** as a **facet** (or split type) with **`dm_view_mode: free_cam | orthographic_tabletop`** (names illustrative). **Inputs** to the facet are still **read-only** slices of **`post_apply_observable_root`** / **`TickCommitRecord_v0`**-anchored bundles — same CQRS story as **`PresentationViewState_v0`** for players (**4.1**). **Replay-relevant** fields should be those **derivable from committed ticks**; **D-027** UX-only fields (smoothing, gizmos, editor chrome) stay out of preimage until explicitly scoped.

**Combined projection patterns:** Engines sometimes stack orthographic gameplay planes with perspective layers for parallax — useful **analogy** for “one committed world, multiple presentation projections,” not a stack prescription.

[Source: Combining perspective and orthographic for 2D parallax](https://www.gamedeveloper.com/programming/combining-perspective-and-orthographic-camera-for-parallax-effect-in-2d-game)

## 2. CQRS read models, tooling, and the promotion boundary

**Projections are derived and replaceable:** A projection consumes authoritative events/commits and produces **query-optimized** read state; it is **not** the source of truth and can be rebuilt when rules change.

[Source: Projections — CQRS.com](https://www.cqrs.com/event-driven-architecture/projections/)

**DM tooling split (aligns with vault):**

| Layer | Role | Vault hook |
|--------|------|------------|
| **Read / query** | Free-cam, ortho map, overlays, inspectors | **`DmPresentationViewState_v0`**, adapters from **3.1.6** observables |
| **Staging** | DM edits **before** ordering | **`ToolActionQueue_v0`** (**3.4.5** bounds) |
| **Write / command** | Ordered mutation | **`MutationIntent_v0`** → **`AgencySliceApplyLedger_v0`** (**3.1.5**) |

**Critical invariant:** **No** code path from **presentation** or **read-model builders** directly appends to the apply ledger. If a DM gesture **mutates** sim, it must traverse **promotion** (**T-DM-P01–P03**) and **D-044** lanes — matching **T-DM-P04** (**Apply vs Preview**): preview never enqueues promotion.

## 3. Mode transition / interpolation at the presentation boundary

**Presentation-only transitions:** Camera / view transitions are commonly implemented as **interpolators** (duration, easing, interruption policy) over **view state**, decoupled from **gameplay** transaction boundaries — i.e. smoothing does not redefine **what tick** a decision belongs to.

[Source: Cinemachine — Camera control and transitions](https://docs.unity3d.com/Packages/com.unity.cinemachine%403.1/manual/concept-camera-control-transitions.html)

[Source: deck.gl — Animations and transitions](https://deck.gl/docs/developer-guide/animations-and-transitions) — **analogy only** (web map / GL stack transitions); **not** a prescribed Godot or DM engine choice.

**Contract sketch for vault (non-normative):**

- **`mode_transition_envelope_v0` (working name):** `from_mode`, `to_mode`, `duration_ms`, `easing_profile_id`, **`interrupt_policy`** (queue / cancel / blend), **`replay_relevant: bool`** (usually **false** unless a future decision freezes transition parameters into replay — **D-032** territory).
- **Commit boundary:** Sim **decisions** remain keyed to **tick / intent** ordering; transitions only **re-target** which **read projection** is active and how **intermediate poses** are shown.

## 3b. Interface stub (non-normative — mirrors phase 4.2 table, not closure)

Strawman field groups for deepen; **TBD** stays honest until **[[phase-4-2-dm-perspective-read-model-and-rig-contracts-roadmap-2026-03-28-1200]]** interface table is filled.

| Artifact | Field group (strawman) | Replay-relevant? | UX-only (D-027 carve-out) | Parity vs 4.1 |
| --- | --- | --- | --- | --- |
| **`DmPresentationViewState_v0`** | `dm_view_mode`, subscribed facets, FOV / ortho size inputs | Only if derivable from committed observables + tick id | Smoothing, gizmo chrome, transition `t` | Same CQRS spine as **`PresentationViewState_v0`** |
| **`DmCameraBinding_v0`** | `binding_id`, `world_anchor_ref`, facet subscription graph | **TBD** — must match **`CameraBinding_v0`** replay story when literals exist (**D-032**) | Preview camera while staged in **ToolActionQueue_v0** | **Explicit defer:** parity row on phase note is **TBD**; deepen must either freeze fields or extend **`@skipUntil`** |

## 4. Checklist — mirror **4.1** without widening **4.1** MVP

| # | Check | Rationale |
|---|--------|-----------|
| 1 | DM rig consumes **only** committed observables + tick metadata | Same as **T-P4-02** spirit for player |
| 2 | **Zero** write path from **`Dm*`** builders into **`AgencySliceApplyLedger_v0`** | **4.2** opening tranche + **D-131** parallel slice |
| 3 | **`ToolActionQueue_v0`** changes are **staging** until **T-DM-P01** promotion | **3.4.5** / **3.4.6** |
| 4 | **T-DM-P04** — “Preview” DM tools do not call promotion | Avoid accidental writes |
| 5 | Replay / golden / registry claims remain **`@skipUntil(D-032)`** / **D-043** | Honesty parity with **4.1** |
| 6 | **D-060** (**conceptual_v1**): treat this research as **deepen fuel**, not a substitute for **recal** when a **hard** coherence stop demands it — see **[[decisions-log]]** | Operator discipline from **[[roadmap-state]]** notes |

## 5. Mapping industry ideas → **T-DM-P01–P05** (WBS hints for deepen)

| Task ID | Suggested deepen focus |
|---------|-------------------------|
| **T-DM-P01** | Explicit states: `staged` → `validated` → `promoted_to_intent` → `ordered` — **exclude** pure view-mode switches unless they enqueue staging |
| **T-DM-P02** | Align **`tool_action_idempotency_key`** with **`mutation_id`** patterns when promoted |
| **T-DM-P03** | Promotion gate checklist references **facet scope** + **D-044** lane |
| **T-DM-P04** | Document **Apply** (may enqueue **ToolActionQueue_v0**) vs **Preview** (read-model only) for DM ortho / free-cam tools |
| **T-DM-P05** | Telemetry for **queue depth** / **rejection reasons** includes **presentation-only** reject path (e.g. attempted write blocked) |

## Raw sources (vault)

- No separate **Raw/** bundle this run (nested pre-deepen time budget). Traceability is captured in **Fetch log (this run)** below instead of a full archived scrape.

## Fetch log (this run)

| URL (normalized) | Claim used in this note |
| --- | --- |
| https://www.cqrs.com/event-driven-architecture/projections/ | Projections = derived read models; replaceable |
| https://docs.unity3d.com/Manual/CamerasOverview.html | Orthographic vs perspective overview |
| https://dev.epicgames.com/documentation/en-us/unreal-engine/orthographic-camera-in-unreal-engine | Orthographic camera product docs |
| https://www.gamedeveloper.com/programming/combining-perspective-and-orthographic-camera-for-parallax-effect-in-2d-game | Stacked projection analogy |
| https://docs.unity3d.com/Packages/com.unity.cinemachine%403.1/manual/concept-camera-control-transitions.html | Presentation-layer camera transitions |
| https://deck.gl/docs/developer-guide/animations-and-transitions | Interpolator / transition parameters (analogy) |

## Sources

- [Projections — CQRS.com](https://www.cqrs.com/event-driven-architecture/projections/)
- [Unity — Cameras overview](https://docs.unity3d.com/Manual/CamerasOverview.html)
- [Unity — Cameras overview (legacy /530/ path)](https://docs.unity3d.com/530/Documentation/Manual/CamerasOverview.html)
- [Unreal Engine — Orthographic camera](https://dev.epicgames.com/documentation/en-us/unreal-engine/orthographic-camera-in-unreal-engine)
- [Game Developer — Orthographic + perspective parallax](https://www.gamedeveloper.com/programming/combining-perspective-and-orthographic-camera-for-parallax-effect-in-2d-game)
- [Cinemachine — Camera control and transitions](https://docs.unity3d.com/Packages/com.unity.cinemachine%403.1/manual/concept-camera-control-transitions.html)
- [deck.gl — Animations and transitions](https://deck.gl/docs/developer-guide/animations-and-transitions)
- Vault: [[phase-4-2-dm-perspective-read-model-and-rig-contracts-roadmap-2026-03-28-1200]], [[phase-4-1-player-first-perspective-read-model-and-rig-contracts-roadmap-2026-03-24-1201]], [[phase-3-4-5-living-world-to-perspective-handoff-bridge-roadmap-2026-03-22-1205]], [[phase-3-4-6-presentation-handoff-task-lanes-validation-harness-and-dm-promotion-roadmap-2026-03-22-1320]], [[Ingest/Agent-Research/phase-4-1-secondary-player-first-read-rig-research-2026-03-24]]

## Related

- **D-131** / **ARCH-FORK-02** — player **4.1** vs DM **4.2** split
- **D-057** — lane A/B/C harness; DM promotion sequencing
