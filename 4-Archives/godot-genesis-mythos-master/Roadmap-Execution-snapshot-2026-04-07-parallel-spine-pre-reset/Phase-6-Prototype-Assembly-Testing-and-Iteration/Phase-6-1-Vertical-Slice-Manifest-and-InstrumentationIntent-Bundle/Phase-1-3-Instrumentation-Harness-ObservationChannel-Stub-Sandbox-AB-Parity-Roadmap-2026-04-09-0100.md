---
title: Phase 1.3 (Execution) — Instrumentation harness / ObservationChannel stub (A/B parity)
created: 2026-04-09
tags:
  - roadmap
  - execution
  - godot-genesis-mythos-master
  - phase-1-3
  - godot
  - instrumentation
  - observation-channel
para-type: Project
project-id: godot-genesis-mythos-master
roadmap_track: execution
status: in-progress
progress: 16
handoff_readiness: 85
parent_slice: Phase-1-Execution-Vertical-Slice-Instrumentation-Spine-Roadmap-2026-04-08-2145
conceptual_counterpart: ../../../Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle/Phase-6-1-3-ObservationChannel-Lane-Readout-and-Presentation-Time-Co-Display-Roadmap-2026-04-07-1015
execution_local_index: "1.3"
---

# Phase 1.3 (Execution) — Instrumentation harness / ObservationChannel stub (sandbox A/B parity)

**Execution-local slice `1.3`** under [[Phase-1-Execution-Vertical-Slice-Instrumentation-Spine-Roadmap-2026-04-08-2145]], after [[Phase-1-2-Registry-Telemetry-Stubs-Sandbox-AB-Parity-Roadmap-2026-04-09-0000]]. This note defines a **vault-resolvable** **instrumentation harness stub** and **ObservationChannel** contract that **wires** [[Phase-1-1-Godot-Engine-Binding-Surfaces-Sandbox-AB-Parity-Roadmap-2026-04-08-2300]] engine/binding surfaces (time loop, logging hooks, GDExtension boundaries) to **1.2** registry + telemetry **sink paths** — without claiming **`GMM-2.4.5-*`** compare scripts, CI, or host-binary proof (**execution-deferred**). **Progress here (`progress` frontmatter) is slice-local**; the Phase 1 parent spine rolls up **`max(children)`** per its § **Execution progress semantics**.

## Scope

- **In scope:** **ObservationChannel stub** interface (named fields, lane id, tick/frame correlation id), **harness placement** (where a future `ObservationChannel` adapter would attach relative to **1.1** inventory), **one sample row** schema flowing into **1.2** `envelope_stub.jsonl`, and **A/B parity** (lane A Godot vs lane B sandbox) at the **contract** level only.
- **Out of scope:** Implementing Godot binaries, automated diff vs conceptual **6.1.3**, or closing **`GMM-2.4.5-*`** rows; mutating frozen conceptual notes under `Roadmap/` outside `Execution/`.

## Harness ↔ surfaces ↔ telemetry (stub wiring table)

| Concern | **1.1** surface (reference) | **1.3** harness hook (stub) | **1.2** sink (reference) |
| --- | --- | --- | --- |
| Tick / frame identity | **1.1** MainLoop / SceneTree / time vocabulary | `observation_correlation_id` = `{tick_seq, lane, slice_id}` emitted at “post-tick commit” boundary (stub prose) | Row in `envelope_stub.jsonl` per **1.2** path table |
| Logging / errors | **1.1** logging + GDExtension boundary | `ObservationChannel.emit_sample({ level, code, lane })` — **no** host code; contract only | Same JSONL schema as **1.2** telemetry rows |
| Registry fields | **1.1** binding inventory | Optional `field_id` echo when sample ties to manifest field (from **6.1.1** ids, read-only) | **1.2** `fields.jsonl` stub alignment |

## ObservationChannel stub contract (both lanes)

**Type shape (documentation-only):**

```pseudo
struct ObservationSampleStub {
  queue_lane: "godot" | "sandbox"
  observation_correlation_id: string
  tick_seq: int
  channel: string            // e.g. "sim_visible", "presentation_co_display"
  payload_ref: string        // path or uri-shaped stub, not a live resource
  parity_gap: bool?          // same semantics as 1.1 / 1.2
}
```

- **Lane A (Godot):** samples **conceptually** attach after **1.1**-listed hooks; paths remain under `user://gmm_telemetry/` per **1.2**.
- **Lane B (sandbox):** identical **schema**; path column from **1.2** `<sandbox-user-data>/gmm_telemetry/envelope_stub.jsonl`.

## NL checklist (1.3 mint)

- [x] **ObservationChannel** stub **named** and tied to **1.1** surfaces + **1.2** sinks (table above).
- [x] **A/B parity** explicit (same schema, lane-specific paths only).
- [x] **`GMM-2.4.5-*`** **not** claimed closed — deferral pointer to **1.2** § GMM rows + [[../../../distilled-core]].

## GWT-1-3-Exec-A–C

| ID | Claim | Evidence hook |
| --- | --- | --- |
| GWT-1-3-Exec-A | **1.1 → 1.3 → 1.2** wiring is traceable in one table | § Harness ↔ surfaces ↔ telemetry |
| GWT-1-3-Exec-B | **ObservationChannel** stub is **schema-addressable** per lane | § ObservationChannel stub contract |
| GWT-1-3-Exec-C | No false **registry/CI closure** | § Scope + cross-link to **1.2** deferral rows |

## Related

- Parent: [[Phase-1-Execution-Vertical-Slice-Instrumentation-Spine-Roadmap-2026-04-08-2145]]
- Next: [[Phase-1-4-PresentationEnvelope-Stub-Sandbox-AB-Parity-Roadmap-2026-04-09-1830]]
- Prior: [[Phase-1-2-Registry-Telemetry-Stubs-Sandbox-AB-Parity-Roadmap-2026-04-09-0000]]
- Surfaces: [[Phase-1-1-Godot-Engine-Binding-Surfaces-Sandbox-AB-Parity-Roadmap-2026-04-08-2300]]
- [[workflow_state-execution]]
- [[roadmap-state-execution]]
- Conceptual readout source: [[../../../Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle/Phase-6-1-3-ObservationChannel-Lane-Readout-and-Presentation-Time-Co-Display-Roadmap-2026-04-07-1015]]
