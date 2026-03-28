---
title: Phase 4.1 secondary — Player-first read-model, presentation CQRS, camera rig & replay (research)
research_query: "CQRS read models from committed sim; presentation consuming TickCommitRecord/post_apply observables; camera rig deterministic replay hash-stable view state; junior adapter→rig closure evidence"
linked_phase: "Phase 4.1 secondary — player-first perspective read-model and rig contracts (ARCH-FORK-02 / D-059)"
project_id: genesis-mythos-master
created: 2026-03-24
tags: [research, agent-research, genesis-mythos-master, phase-4-1, cqrs, presentation, camera, replay, player-first]
para-type: Resource
agent-generated: true
research_tools_used: [vault_context, web_search, mcp_web_fetch]
research_escalations_used: 0
parent_handoff: "Roadmap nested research — resume-deepen phase 4.1 player-first GMM"
queue_entry_id: resume-deepen-phase4-1-player-first-gmm-20260324T010800Z
---

# Phase 4.1 secondary — Industry patterns for read models, presentation, and rig/replay coupling

**Scope:** Non-normative synthesis for **[[phase-4-1-player-first-perspective-read-model-and-rig-contracts-roadmap-2026-03-24-1201]]** (ARCH-FORK-02 / D-059). **Authoritative** contracts remain vault phase notes (**3.1.5**, **3.1.6**, **3.1.1**), **[[decisions-log]]**, and **D-032 / D-043 / D-037** deferrals.

## Vault anchor — do not duplicate

- **4.1 secondary** already states: read-only projections from **`SimObservableBundleTelemetry_v0`** / **`post_apply_observable_root`** + **`TickCommitRecord_v0`**; **no** mutation lane into **`AgencySliceApplyLedger_v0`**; **T-P4-01…T-P4-05**; Lane-C / **ReplayAndVerify** **`@skipUntil(D-032)`**; **REGISTRY-CI HOLD** honesty (**D-062**).
- **Prior synthesis:** [[Ingest/Agent-Research/phase-3-4-5-sim-presentation-camera-bridge-research-2026-03-22-1245]] (sim vs presentation, `PresentationViewState_v0` / `CameraBinding_v0` drafts), [[Ingest/Agent-Research/phase-4-1-1-adapter-preimage-stable-layout-cqrs-research-2026-03-23-2205]] (adapter row CQRS, preimage versioning), [[Ingest/Agent-Research/phase-4-primary-perspective-control-research-2026-03-24]] (G-P4 registry narrative).

This note adds **external** framing for (1) CQRS/read-model industry habits, (2) camera rig vs deterministic replay **conceptually**, and (3) a **junior closure checklist** for adapter→rig.

## 1. CQRS read models and presentation consuming committed simulation state

**Pattern — command/query split:** CQRS separates **writes** (commands, validation, domain rules) from **reads** (query models / projections). In event-sourced designs, **read models** are **projections** rebuilt or incrementally updated from an append-only history; they can be **versioned** and **rebuilt** when projection rules change. Schema evolution for projections commonly uses **tolerant readers**, **upcasters**, or **explicit event/version types** so consumers do not silently misinterpret bytes.

[Source: Event versioning and CQRS deeper insights](https://www.cqrs.com/deeper-insights/event-versioning/)

**Games and sim engines — simulation vs presentation:** Netcode-oriented docs describe **simulation** as logic that advances **authoritative networked (gameplay) state**, possibly **multiple times per rendered frame** (rollback, catch-up). **Presentation** runs **once per rendered frame**: it **positions the scene** from the **current simulation snapshot** — meshes, shaders, VFX, audio — without feeding back into gameplay. Aliasing between fixed sim tick rate and variable refresh is handled by **interpolation** between **committed** simulation samples for visuals only.

[Source: Simulation vs. Presentation | SnapNet](https://snapnet.dev/docs/core-concepts/simulation-vs-presentation)

**Map to vault (conceptual, not engine-specific):**

| Industry idea | Vault hook |
|---------------|------------|
| Command side / write model | **`AgencySliceApplyLedger_v0`**, mutation intents, tick commit path (**3.1.5** / **3.2.x**) |
| Committed authoritative snapshot | **`post_apply_observable_root`**, **`TickCommitRecord_v0`** (**3.1.6** / **3.1.1**) |
| Read model / projection | **Adapter rows**, **`PresentationViewState_v0`**, **`CameraBinding_v0`** — pure functions of **committed** inputs |
| Projection versioning | **`adapter_row_layout_id`**, **`serialization_profile_id`** / facet manifest (**D-037**), **`replay_row_version`** coordination (**D-032**) |

**Anti-pattern:** Any “shortcut” that lets presentation or adapters **append** to the apply ledger or alter **tick preimage** without the sanctioned command path — a **second write lane** that breaks determinism and replay parity (already called out in [[Ingest/Agent-Research/phase-4-1-1-adapter-preimage-stable-layout-cqrs-research-2026-03-23-2205]]).

**Event-sourced game examples (illustrative):** Phoenix LiveView / event-sourced game articles describe **views** as **projections** from events (rebuild vs running mode). Useful as **analogy** for “presentation is not the transaction boundary,” not as stack prescription.

[Source: Event-sourced game architecture (Charles Desneuf)](https://blog.charlesdesneuf.com/articles/phoenix-liveview-event-sourced-game-architecture/)

## 2. Camera rig binding, deterministic replay, and hash-stable “view state”

**Determinism and replay (networking context):** Lockstep and rollback designs emphasize **fixed tick**, **stable ordering**, **seeded RNG**, and often **fixed-point** or carefully controlled floats so that **inputs → state** is reproducible. **Camera pose for gameplay** may need to be **derivable from committed sim** if replays must not depend on local render history; **cosmetic** camera (shake, smoothing) can stay in **presentation** only.

[Source: Deterministic lockstep overview](https://gafferongames.com/post/deterministic_lockstep/)

[Source: Rollback / GGPO-style resim overview](https://outof.pizza/posts/rollback/)

**Engine-agnostic contract shape (aligns with vault drafts):**

1. **Binding identity:** Stable **`binding_id`** / role id in **`CameraBinding_v0`** — identifies *which* rig consumes *which* read-model slice (facet allow-list per **D-037** intent).
2. **Inputs:** Only **committed** observables + explicit **`world_anchor_ref`** (cell/entity ref) — no hidden global mutable “camera state” that sim does not see.
3. **Replay-stable vs presentation-only fields:** Separate **hashes/ids** that must match golden/replay tables (**when D-032/D-043 allow**) from **interpolation alpha**, **presentation_tick_seq**, **derived_pose_hash** marked **non-authoritative** in **[[phase-3-4-5-living-world-to-perspective-handoff-bridge-roadmap-2026-03-22-1205]]**.
4. **Rollback / multi-step sim:** If the runtime can **resim** several ticks per frame, **rig setup** that touches **physics or gameplay** must live in **sim** or in **read-model** derived **strictly** from committed ticks — not in “run once per frame” presentation that **skips** on resim.

[Source: Simulation vs. Presentation | SnapNet](https://snapnet.dev/docs/core-concepts/simulation-vs-presentation)

**Hash-stable view state (conceptual):** Treat “view state” for **replay** as a **pure function** `f(committed_tick_bundle, layout_id, profile_id)` with **documented exclusion** of wall-clock and frame-rate-only fields (**D-027**). Until literals freeze, vault-honest stance: **stub rows** + **`@skipUntil(D-032)`** / **D-043** — no **CI PASS** for presentation golden columns.

## 3. Junior-dev checklist — evidence before claiming **adapter → rig closure**

Use this as **Definition of Done** for **T-P4-01** + **T-P4-02** handoff (vault tasks), not as a substitute for operator decisions.

| # | Evidence | Pass criterion (draft) |
|---|----------|-------------------------|
| 1 | **Source of truth** | Written statement: rig inputs come **only** from **`post_apply`** / committed bundle + **`TickCommitRecord_v0`** linkage — **not** pre-barrier or speculative bundles. |
| 2 | **No write path** | Code or pseudo-code review: **zero** calls from presentation/adapter/rig into **`AgencySliceApplyLedger_v0`** or tick preimage mutation. |
| 3 | **Facet allow-list** | **`subscribed_facet_ids`** ⊆ **D-037** manifest; no “direct preimage holes.” |
| 4 | **Layout / profile ids** | **`adapter_row_layout_id`** and **`serialization_profile_id`** (or stubs) documented; changelog hook noted for **D-032** coordination. |
| 5 | **Replay scope** | Table row: which fields are **in** vs **out** of **`TickCommitRecord_v0` preimage**; Lane-C cells **`@skipUntil(D-032)`** where literals absent. |
| 6 | **Determinism story** | For each **replay-relevant** camera/pose field: either (a) derived from committed sim only, or (b) explicitly **excluded** with **D-027**-style UX-only labeling. |
| 7 | **Ordering / regen** | If DM/player intents exist, reference **D-044** / **RegenLaneTotalOrder_v0** — no silent same-tick mixing **proven** until literals exist. |
| 8 | **Registry honesty** | **G-P\*.\*-REGISTRY-CI HOLD** acknowledged; no claim of **REGISTRY-CI PASS** or **HR ≥ min_handoff_conf** from this slice alone (**D-062**). |

## Raw sources (vault)

- No new raw bundle for this run; citations are inline above.

## Sources

- [Simulation vs. Presentation | SnapNet](https://snapnet.dev/docs/core-concepts/simulation-vs-presentation)
- [Deterministic Lockstep | Gaffer On Games](https://gafferongames.com/post/deterministic_lockstep/)
- [Making a GGPO-style rollback networking multiplayer game](https://outof.pizza/posts/rollback/)
- [Event Versioning - CQRS, Event Sourcing & co.](https://www.cqrs.com/deeper-insights/event-versioning/)
- [Building an event-sourced game with Phoenix Liveview: Architecture](https://blog.charlesdesneuf.com/articles/phoenix-liveview-event-sourced-game-architecture/)
- Vault: [[phase-4-1-player-first-perspective-read-model-and-rig-contracts-roadmap-2026-03-24-1201]], [[phase-3-4-5-living-world-to-perspective-handoff-bridge-roadmap-2026-03-22-1205]], [[Ingest/Agent-Research/phase-4-1-1-adapter-preimage-stable-layout-cqrs-research-2026-03-23-2205]]

## Related

- [[phase-3-4-7-perspective-entry-wbs-and-phase-4-1-task-bridge-roadmap-2026-03-22-0748]] (**D-058** WBS)
- [[phase-3-4-6-presentation-handoff-task-lanes-validation-harness-and-dm-promotion-roadmap-2026-03-22-1320]] (**D-057** lanes)
