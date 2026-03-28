---
title: Phase 4 primary — perspective read-model, CQRS, replay vs presentation (research)
research_query: "CQRS read-model vs sim write; FP vs DM orthographic tooling; golden-row ReplayAndVerify on presentation when tick commits authoritative"
linked_phase: Phase-4-primary-perspective-split (macro Phase 4; ARCH-FORK-02; D-062 vs REGISTRY-CI HOLD)
project_id: genesis-mythos-master
created: 2026-03-24
tags: [research, agent-research, genesis-mythos-master, phase-4, cqrs, replay, perspective]
para-type: Resource
agent-generated: true
research_tools_used: [web_search, mcp_web_fetch]
research_escalations_used: 0
parent_handoff: "Roadmap RESUME_ROADMAP pre-deepen nested research — primary phase-4 roadmap + 4.1 player-first spine"
---

# Phase 4 primary — perspective / control research (stack-agnostic)

**Non-normative prior art** for macro **Phase 4** ([[phase-4-perspective-split-and-control-systems-roadmap-2026-03-19-1101]]) and the **4.1** player-first spine ([[phase-4-1-player-first-perspective-read-model-and-rig-contracts-roadmap-2026-03-24-1201]]). Per **D-027**, engine- or language-specific examples below are **illustrative only**; contracts in **3.1.x / 3.4.x** vault notes remain authoritative.

## Vault anchor (do not duplicate)

- **Player-first fork:** **ARCH-FORK-02** / **D-059** — DM shell + shared control deferred after **4.1** spine.
- **Interfaces:** `PresentationViewState_v0`, `CameraBinding_v0` consume **committed** observables / tick ledger — not a second mutation lane into agency apply (**4.1** table).
- **CI honesty:** **G-P4-REGISTRY-CI** **HOLD**; Lane-C / **ReplayAndVerify** literal rows **`@skipUntil(D-032)`** until replay header fields land.
- **Prior synthesis:** [[phase-3-4-5-sim-presentation-camera-bridge-research-2026-03-22-1245]] (fixed timestep vs presentation, SnapNet-style sim/presentation split).

## 1. CQRS: presentation read-model vs simulation write path

**Pattern:** **Command Query Responsibility Segregation** separates **writes** (commands that enforce invariants and commit authoritative state) from **reads** (queries served from **projections** / read models optimized for consumers). In event-oriented designs, committed events feed **projectors** that update read models asynchronously; the **write model** stays the source of truth.

[Source: CQRS Pattern: Separating Write Models from Query Models at Scale](https://www.abstractalgorithms.dev/cqrs-pattern-read-write-model-separation)

**Game-shaped reading:** The same separation appears when “commands” are player/DM intents that enqueue work, “state” is simulation results, and “queries” are what UI, cameras, and tools consume. A practical failure mode in multiplayer-style designs is treating **projections** as truth — that invites concurrency and ordering bugs; **committed simulation state** (or its tick-scoped ledger) must remain authoritative.

[Source: Building a Multiplayer Risk Game with Claude — projections vs source of truth](https://medium.com/@roger.torres/building-a-multiplayer-risk-game-with-claude-what-worked-what-broke-and-why-4d86fd990b3b)

**Genesis mapping (contract-level, D-027-safe):**

- **Write path:** `AgencySliceApplyLedger_v0` / ordered apply → `TickCommitRecord_v0` (vault **3.1.5–3.1.6** narrative).
- **Read path:** `PresentationViewState_v0` / `CameraBinding_v0` are **read models** over **post-commit observables** (`post_apply_observable_root` / allow-listed facets) — **no** silent write-back from presentation; tool actions that mutate world state belong in **sanctioned** intent lanes (defer DM `ToolActionQueue_v0` detail per **D-059**).

## 2. Deterministic tick, camera rig, and replay coupling to observables

**Fixed timestep vs variable render:** Reproducible engines typically **quantize simulation** to a fixed dt while rendering may run at variable frame rate; presentation interpolates **between committed sim states** without changing the authoritative transition graph.

[Source: Fix Your Timestep!](https://gafferongames.com/post/fix_your_timestep/)

**Inputs vs outputs vs state (replay):** Classic replay guidance distinguishes **inputs** (including quantized **time** as an input), **persistent game state**, and **outputs** (e.g. GPU-bound vertex streams). **Outputs** do not affect reproducibility *unless* other systems mistakenly **read rendering-derived data back into simulation** (e.g. collision using GPU-only buffers) — then that data becomes part of **state** for replay purposes.

[Source: Instant Replay: Building a Game Engine with Reproducible Behavior](https://www.gamedeveloper.com/design/instant-replay-building-a-game-engine-with-reproducible-behavior)

**First-person / view split (illustrative):** Some engines use **multiple cameras / render layers** so a **world** view and a **view-model** (arms, held items) can differ in FOV and layering while still driven by one logical player state. Treat as **presentation composition** of one read model, not a second sim.

[Source: Bevy example — First person view model](https://bevyengine.org/examples-webgpu/camera/first-person-view-model/)

**Observable coupling:** Player camera rig parameters should be **pure functions** of **committed** observables + **replay-stable** binding ids (`CameraBinding_v0`), plus **local** presentation smoothing (lag, spring) that does **not** feed tick preimage. Aligns with **T-P4-02** (“rig consumes `PresentationViewState_v0` only”).

## 3. First-person vs DM orthographic tooling (defer DM shell per D-059)

**Editor / tooling orthographic pattern:** Professional content tools routinely provide **orthographic viewports** (top/front/side) with **different navigation** than perspective “game” cameras — marquee selection, pan, zoom — suited to layout and measurement rather than player embodiment.

[Source: Viewport Controls | Unreal Engine Level Editor](https://docs.unrealengine.com/4.26/en-US/BuildingWorlds/LevelEditor/Viewports/ViewportControls/)

**Brush / grid editors:** Classic map editors combine **3D** and **multi 2D orthographic** views for precision placement; entity linking and UV tools live in the **tool** layer, not the runtime player loop.

[Source: TrenchBroom Reference Manual](https://trenchbroom.github.io/manual/latest/index.html)

**Genesis mapping:** **D-059** explicitly **defers** the **DM free-cam + orthographic + shared control shell** until after the **player-first** read-model spine. Research takeaway: specify **4.1** as **player FPV read pipeline** + contracts; capture **DM orthographic** as a **separate tool profile** (input mapping, selection model, grid snapping) in a **later** secondary so **presentation read-model** tables do not sprawl into DM UX before **G-P4-PLAYER** closes.

## 4. Golden rows / ReplayAndVerify vs presentation when sim tick commits are authoritative

**Per-tick hashing:** Ecosystem crates/docs describe **hashing post-tick snapshots** (or structured state views) to detect divergence between replays — verification stays on **sim-visible state**, not on pixels.

[Source: murk-replay docs — snapshot hashing](https://docs.rs/murk-replay/latest/murk_replay/)

**Where presentation fits:** If **Lane-C / ReplayAndVerify** rows are **presentation-layer** (e.g. camera pose, FOV, culling outcomes), they must still be **defined as pure functions** of **tick-committed preimage** + **stable serialization profiles** (`serialization_profile_id` / facet manifest intent — vault **D-037** defer). Otherwise, **non-deterministic render timing** or **GPU readbacks** reintroduce the “outputs became state” failure mode from §2.

**Practical split for CI (aligned with vault honesty guards):**

| Layer | Golden / replay gate target |
|--------|-----------------------------|
| **Sim commit** | `TickCommitRecord_v0`, regen ledger rows, observable bundle hashes (**authoritative**) |
| **Presentation** | **Derived** golden vectors — optional, **skipped** until **D-032** / **D-043** literal replay columns exist (**G-P4-REGISTRY-CI HOLD**) |

**Networking analogy:** Deterministic lockstep / replay-friendly designs stress **identical sim inputs + ordering** across machines; presentation may differ if it does not feed back.

[Source: Deterministic simulation for lockstep multiplayer (overview)](https://www.daydreamsoft.com/blog/deterministic-simulation-for-lockstep-multiplayer-engines)

## 5. Decision candidates (for decisions-log / 4.1 deepen)

- Label **presentation adapters** as **CQRS query side** in code/docs; **forbid** mutation except via explicit command API.
- Require **camera pose / FOV** in replay goldens to list **preimage column ids** (observable + binding + profile), not ad-hoc engine structs (**D-027**).
- Keep **DM orthographic** out of **4.1** acceptance criteria; track as **4.x** tool secondary after **G-P4-PLAYER** progress (**D-059**).
- When **D-032** clears, add **presentation golden rows** as **Tier-B** checks (derived from sim goldens), not replacements for tick commit vectors.

## Sources

- [Abstract Algorithms — CQRS read/write separation](https://www.abstractalgorithms.dev/cqrs-pattern-read-write-model-separation)
- [Medium — Multiplayer Risk / projections lesson](https://medium.com/@roger.torres/building-a-multiplayer-risk-game-with-claude-what-worked-what-broke-and-why-4d86fd990b3b)
- [Gaffer On Games — Fix Your Timestep](https://gafferongames.com/post/fix_your_timestep/)
- [Game Developer — Instant Replay / inputs, outputs, state](https://www.gamedeveloper.com/design/instant-replay-building-a-game-engine-with-reproducible-behavior)
- [Bevy — First person view model example](https://bevyengine.org/examples-webgpu/camera/first-person-view-model/)
- [Unreal Engine 4.26 — Viewport controls (orthographic tooling)](https://docs.unrealengine.com/4.26/en-US/BuildingWorlds/LevelEditor/Viewports/ViewportControls/)
- [TrenchBroom — Reference manual](https://trenchbroom.github.io/manual/latest/index.html)
- [docs.rs — murk-replay](https://docs.rs/murk-replay/latest/murk_replay/)
- [Daydreamsoft — Deterministic simulation / lockstep overview](https://www.daydreamsoft.com/blog/deterministic-simulation-for-lockstep-multiplayer-engines)

## Raw sources (vault)

- No new raw note this run; external pages cited inline above. Related prior run: [[phase-3-4-5-sim-presentation-camera-bridge-research-2026-03-22-1245]].
