---
title: Phase 2.1 (Execution) — Procedural / world execution stub (sandbox A/B parity)
created: 2026-04-09
tags:
  - roadmap
  - execution
  - godot-genesis-mythos-master
  - phase-2-1
  - godot
para-type: Project
project-id: godot-genesis-mythos-master
roadmap_track: execution
status: in-progress
progress: 22
handoff_readiness: 85
parent_slice: Phase-2-Execution-Procedural-World-Spine-Roadmap-2026-04-09-2016
execution_local_index: "2.1"
conceptual_counterpart: "[[../Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-03-30-0430]]"
---

# Phase 2.1 (Execution) — Procedural / world execution stub (A/B vs sandbox reference)

**Execution-local slice `2.1`** under [[Phase-2-Execution-Procedural-World-Spine-Roadmap-2026-04-09-2016]], per [[../decisions-log]] **D-Exec-1-numbering-policy**. This note owns **vault-only** stubs for **procedural generation** and **world-building** host surfaces on **lane A (Godot)** with explicit **lane B (sandbox)** comparand rows — same logical contracts, different host shims. **No** registry CI, compare-table closure, or **`GMM-2.4.5-*`** “done” claims until **scripts/CI** exist (**D-Exec-1.2-GMM-245-stub-vs-closure**).

## Scope

- **In scope:** Name the **first** execution-shaped **proc/world** attachment points after Phase **1** instrumentation (ObservationChannel / PresentationEnvelope) — how **seed → world graph → observable deltas** enter the same **envelope schema family** as instrumentation rows, at **stub** depth.
- **Out of scope:** Shipping binaries, **GMM-2.4.5-*** compare/rollup/retention closure, production **registry JSONL** writers — **execution-deferred** per parent spine and [[../distilled-core]].

## Procedural / world surface inventory (adapter layer)

| Surface | Role in spine | Godot hook (lane A) | Sandbox reference hint (lane B) |
| --- | --- | --- | --- |
| **World / scene root** | Deterministic host for proc experiments | `World3D` / `Node3D` root + `SceneTree` current scene; optional `SubViewport` isolation for proc-only harness | Abstract “world host” with stable **root id** + tick boundary — must expose same **scene identity** semantics for envelope correlation |
| **Seed / RNG contract** | Replayable proc streams | `RandomNumberGenerator` with explicit **seed** + documented **stream split** (what consumes which draw) | Same **seed + stream split** contract expressed for B’s RNG (language-agnostic pseudocode row) |
| **Graph / parameter bundle** | Proc outputs as structured inputs to world | `Resource`-backed parameter objects or plain `Dictionary` with **schema version** field | B declares symmetric **schema version** + field names for diff/compare stubs |
| **Observation fan-out** | Proc/world events visible to ObservationChannel | Reuse **1.3** harness contract: labeled emission paths into **InstrumentationIntentEnvelope**-compatible rows | B emits **same row keys** where comparand exists; otherwise **`parity_gap: true`** stub |
| **Presentation readout** | Operator-visible proc/world state | Tie-in to **1.4** `PresentationReadoutRowStub` — proc/world rows are **additional row kinds**, not a second envelope | B documents matching **readout kind** strings or explicit **unsupported** with gap flag |

## A/B parity contract (operator-visible)

1. **Same envelope schema family:** Proc/world stub rows remain compatible with the **InstrumentationIntentEnvelope** vocabulary and **lane metadata** (`queue_lane: godot` \| `sandbox`) — field-name divergences cross-linked to **1.2** stub path table when registry paths matter; **`GMM-2.4.5-*`** closure remains **execution-deferred**.
2. **Divergence logging:** When Godot exposes a capability B lacks (e.g. built-in `SubViewport` isolation), lane B adapter must emit **`parity_gap: true`** stub rows — **not** silent drop.
3. **Non-closure row:** Do **not** claim **SCHEMA / RETENTION / VALIDATOR-COMPARE-TABLE** for **`GMM-2.4.5-*`** until **scripts/CI** and compare harness exist (inherits **D-Exec-1.2-GMM-245-stub-vs-closure**).

## NL checklist (2.1 mint)

- [x] Enumerate **≥5** distinct **proc/world** loci tied to the **Phase 2** spine (table above).
- [x] State **A/B parity** rules: shared schema family, explicit gap flags, lane metadata — **no** **`GMM-2.4.5-*`** closure.
- [x] Link parent **Phase 2** spine and upstream **Phase 1** instrumentation chain without rewriting conceptual **Phase 2** body.

## Acceptance hooks (post–IRA evidence)

- **H1:** Godot stub declares **seed + stream split** ownership (which subsystem draws from which RNG stream) before **2.x** expansion.
  - **Evidence stub (vault-only):** pseudo-code shape: `rng_main = RNG(seed0); rng_proc = rng_main.split_stream("proc_graph"); rng_world = rng_main.split_stream("world_delta");` — each consumer names its stream id in emitted envelope rows (`rng_stream_id`).
- **H2:** Sandbox lane B declares **parity_gap** behavior when **SubViewport** / Godot-specific isolation cannot be matched — no silent omission.
  - **Stub row shape:** `{ "kind": "parity_gap", "lane": "sandbox", "feature": "SubViewport_isolation", "parity_gap": true }` appended when B cannot mirror Godot-only isolation semantics.
- **H3:** Proc/world row kinds are **named** and aligned to **1.4** readout kinds where applicable.
  - **Named kinds (initial):** `proc_graph_emit`, `world_delta_emit`, `presentation_readout_proc` — each maps to a **1.4** `PresentationReadoutRowStub` **kind** string or declares `unsupported` + `parity_gap`.

## GWT-2-1-Exec-A–C

| ID | Claim | Evidence hook |
| --- | --- | --- |
| GWT-2-1-Exec-A | Godot-specific proc/world surfaces are named and mapped to spine + instrumentation continuity | § Procedural / world surface inventory |
| GWT-2-1-Exec-B | Sandbox lane is referenced as **comparand**, not authority over conceptual Phase 2 | § Scope + A/B parity contract |
| GWT-2-1-Exec-C | Slice is discoverable as **`2.1`** under execution-local policy | Frontmatter `execution_local_index` + parent link |

## Related

- Parent: [[Phase-2-Execution-Procedural-World-Spine-Roadmap-2026-04-09-2016]]
- Prior instrumentation chain: [[Phase-1-Execution-Vertical-Slice-Instrumentation-Spine-Roadmap-2026-04-08-2145]]
- [[workflow_state-execution]]
- [[roadmap-state-execution]]
- [[../decisions-log]] (**D-Exec-1-numbering-policy**, **D-Exec-1.2-GMM-245-stub-vs-closure**)
