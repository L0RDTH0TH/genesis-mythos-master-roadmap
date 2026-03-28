---
title: Phase 3.4.5 — Sim → presentation / camera bridge (prior art)
research_query: "deterministic sim observable bundle to client presentation; DM tooling vs tick ordering"
linked_phase: Phase-3-4-5 (pre-mint tertiary — sim→render bridge for Phase 4 prep)
project_id: genesis-mythos-master
created: 2026-03-22
tags: [research, agent-research, genesis-mythos-master, phase-3-4, phase-4, determinism]
para-type: Resource
agent-generated: true
research_tools_used: [web_search, mcp_web_fetch]
research_escalations_used: 0
parent_handoff: "roadmap pre-deepen nested research; queue_entry_id a1b-pc-gmm-deepen-20260322T120530Z"
---

# Phase 3.4.5 research — living-world observables → perspective / camera layer

**Scope:** Non-normative prior art for opening **Phase 3.4.5** as a tertiary bridge between **Phase 3.4** (tick-scoped ledgers, `post_apply_observable_root`, facet manifest, regen **D-044** HOLD) and **Phase 4** (player FPV vs DM free-cam / orthographic tools). Does **not** override vault contracts in **3.1.5–3.1.6**, **3.4.2–3.4.4**, or **D-027** (no wall-clock leakage into preimage).

## Vault anchor (do not duplicate)

- Authoritative sim outputs after ordered apply: **`AgencySliceApplyLedger_v0`** → **`post_apply_observable_root`** / **`SimObservableBundleTelemetry_v0`** → **`TickCommitRecord_v0`** ([[phase-3-1-6-tick-scoped-observable-bundle-post-apply-replay-bridge-roadmap-2026-03-22-0047]]).
- Facet allow-list + serialization profile: **3.4.3**; same-tick regen vs ambient ordering remains **HOLD** until **D-044** ([[phase-3-4-4-phase-3-4-secondary-closure-rollup-and-advance-readiness-roadmap-2026-03-23-1935]]).
- Phase 4 product intent: FPV for players, free-cam + orthographic for DMs, transition smoothness ([[phase-4-perspective-split-and-control-systems-roadmap-2026-03-19-1101]]).

## Industry pattern 1 — Fixed timestep vs variable presentation

Games that need **stable simulation** decouple **simulation updates** (fixed dt, possibly multiple steps per real frame) from **rendering** (variable frame rate). The common pattern is an **accumulator**: consume real elapsed time in chunks of fixed dt; use leftover fractional dt as an **interpolation alpha** between previous and current sim state for smooth drawing.

[Source: Fix Your Timestep!](https://gafferongames.com/post/fix_your_timestep/)

**Bridge implication for Genesis Mythos:** Your `tick_epoch` is the authority clock; any **visual** smoothing (camera lag, interpolation) should be **presentation-only** and must not write back into mutation ledgers without explicit **`MutationIntent_v0`** semantics.

## Industry pattern 2 — Explicit simulation vs presentation phases

SnapNet’s documentation states a hard split: **simulation** advances gameplay/networked state (may run **0 or many times per rendered frame** in networked rollback-style clients), while **presentation** runs **once per rendered frame** to spawn meshes, VFX, audio, shaders — cosmetic-only, derived from sim state.

[Source: Simulation vs. Presentation | SnapNet](https://snapnet.dev/docs/core-concepts/simulation-vs-presentation/)

**Bridge implication:** Treat **Phase 4** camera rigs as **presentation consumers** of a **read model** built from allow-listed facets / observable bundle — not as co-equal writers to tick commit. DM “god view” is still a **view** unless a deliberate tool path emits sanctioned intents (compare to your regen / DM overwrite gates in Phase 3.2).

## Industry pattern 3 — DM / editor tooling vs simulation tick

Broad engine docs emphasize **ordered sub-phases inside a tick** (e.g. pre-tick, tick, post-tick) so networking, physics, and gameplay agree on ordering. Dedicated **editor** or **tool** layers often either:

- **Flush tool commands** into the sim at defined boundaries (before/after tick), or  
- **Maintain a parallel sandbox** that does not reorder authoritative tick work (live-edit “world” products sometimes collapse editor/runtime — that is a product choice, not a determinism-friendly default).

[Source: Dreamlab tick loop overview](https://docs.dreamlab.gg/guide/tick-loop/) (illustrative ordering only; not normative for this vault)

**Bridge implication:** For **DM free-cam** and orthographic tooling, specify whether camera pose and tool hits are (**A**) pure presentation + UI hit-testing against **last committed** observable snapshot, (**B**) **preview** overlays that never touch commit until confirmed, or (**C**) **intent sources** that enqueue **`MutationIntent_v0`** / DM-overwrite rows per **3.2.x**. Mixing **B** and **C** without explicit barriers risks the same class of “same-tick interleaving” ambiguity called out for **D-044**.

## Suggested contract sketch (for 3.4.5 normative draft — proposal only)

1. **`PresentationViewState_v0` (non-authoritative):** Derived each render frame from `post_apply_observable_root` preimage + facet manifest; versioned separately from `replay_row_version` (presentation may skip frames; sim may not).
2. **`CameraBinding_v0`:** Maps role (player | DM) → which facets / spatial indices are subscribed; **no** direct ledger append.
3. **`ToolActionQueue_v0` (DM):** If tools mutate world state, entries convert to **explicit** intents with `mutation_id` and participate in **3.1.5** ordering — never “side channel” into regen or ambient rows.

## Raw sources (vault)

- (none — external fetches only this run)

## Sources

- https://gafferongames.com/post/fix_your_timestep/
- https://snapnet.dev/docs/core-concepts/simulation-vs-presentation/
- https://docs.dreamlab.gg/guide/tick-loop/
- https://andreleite.com/posts/2025/game-loop/fixed-timestep-game-loop/ (secondary; fixed-timestep loop explainer)
