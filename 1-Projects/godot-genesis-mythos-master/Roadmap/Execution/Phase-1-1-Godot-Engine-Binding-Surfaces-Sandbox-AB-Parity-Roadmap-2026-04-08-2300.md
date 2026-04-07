---
title: Phase 1.1 (Execution) — Godot engine binding surfaces vs sandbox A/B parity
created: 2026-04-08
tags:
  - roadmap
  - execution
  - godot-genesis-mythos-master
  - phase-1-1
  - godot
para-type: Project
project-id: godot-genesis-mythos-master
roadmap_track: execution
status: in-progress
progress: 22
handoff_readiness: 85
parent_slice: Phase-1-Execution-Vertical-Slice-Instrumentation-Spine-Roadmap-2026-04-08-2145
execution_local_index: "1.1"
---

# Phase 1.1 (Execution) — Godot engine binding surfaces (A/B vs sandbox reference)

**Execution-local slice `1.1`** under [[Phase-1-Execution-Vertical-Slice-Instrumentation-Spine-Roadmap-2026-04-08-2145]], per [[../decisions-log]] **D-Exec-1-numbering-policy**. Conceptual **6.1.x** notes remain **cross-links only** for design authority; this note owns **Godot-lane adapter** prose for instrumentation parity checks against the **sandbox** parallel lane (non-Godot or reference stack).

## Scope

- **In scope:** Name the **Godot 4.x** surfaces where the vertical-slice instrumentation spine (ObservationChannel → PresentationEnvelope) attaches for **lane A (Godot)** vs **lane B (sandbox reference)** — same logical contracts, different host shims.
- **Out of scope:** Shipping binaries, CI proofs, registry compare-table closure (**execution-deferred** per parent spine and [[../distilled-core]]).

## Godot binding surface inventory (adapter layer)

| Surface | Role in spine | Godot hook (lane A) | Sandbox reference hint (lane B) |
| --- | --- | --- | --- |
| **Tick / frame boundary** | Bounded tick window + first committed tick | `MainLoop::_iteration` / `_process` on `SceneTree`; `Engine::get_frames_drawn()` for monotonic frame id | Abstract “frame clock” or host main loop callback — must expose same **tick id** semantics to ObservationChannel |
| **High-resolution time** | Align ObservationChannel sample timestamps | `Time::get_ticks_usec()` (or `OS::get_ticks_usec()` legacy) | Wall or logical clock with **µs or stable tick** mapping documented in lane B adapter note |
| **Structured emission** | Labeled sample rows without corrupting operator UX | `print_rich` / `push_warning` gated behind `OS::is_stdout_verbose()` **or** dedicated `FileAccess` / ring buffer sink agreed in PMG | Equivalent log sink; **schema** must match Godot adapter output (JSONL row or envelope stub) |
| **Scene / node lifecycle** | Seed bundle → first tick handoff | `SceneTree::node_added` / `_ready` ordering on instrumented root | Same **lifecycle ordering contract** expressed for B’s host |
| **Extension boundary** | Optional native probes | **GDExtension** module load + `ClassDB` registration for `InstrumentationHost` shim | If B uses FFI/plugin, document symmetric **load order** vs Godot `GDExtension::initialize_level` |
| **Signals vs polling** | ObservationChannel fan-out | `Callable` + `emit_signal` patterns; `SceneTreeTimer` for bounded windows | B must expose **event or poll** equivalent with same **delivery guarantees** (at-most-once vs buffered) called out explicitly |

## A/B parity contract (operator-visible)

1. **Same envelope schema:** Both lanes emit rows compatible with the **InstrumentationIntentEnvelope** vocabulary imported from conceptual **6.1.1** (field names differ only where host forces — cross-link field-name divergences to the minted execution slice [[Phase-1-2-Registry-Telemetry-Stubs-Sandbox-AB-Parity-Roadmap-2026-04-09-0000]] for its **stub path table** + JSONL row schema; **GMM-2.4.5-*** compare/rollup closure remains execution-deferred per that note).
2. **Divergence logging:** When Godot exposes a capability B lacks (e.g. built-in frame id), lane B adapter must emit **`parity_gap: true`** stub rows — **not** silent drop.
3. **Queue / lane metadata:** Every sample row carries `queue_lane: godot` | `sandbox` (or configured tokens) for downstream rollup.

## NL checklist (1.1 mint)

- [x] Enumerate **≥5** distinct Godot engine or extension **binding** loci tied to the instrumentation spine (table above).
- [x] State **A/B parity** rules: shared schema, explicit gap flags, lane metadata.
- [x] Link parent **Phase 1** spine and **D-Exec-1** policy without rewriting conceptual **6.1.x** bodies.

## Acceptance hooks (post–IRA evidence)

- **H1:** Godot adapter must expose **`frame_id`** (from `Engine::get_frames_drawn()` or documented equivalent) on every ObservationChannel sample row schema.
- **H2:** Sandbox lane B adapter must declare **parity_gap** behavior when **`frame_id`** (or tick monotonicity) cannot be matched — no silent omission.
- **H3:** Lane metadata (`queue_lane`) is **mandatory** on stub emitters before **1.2** registry-row work lands.

## GWT-1-1-Exec-A–C

| ID | Claim | Evidence hook |
| --- | --- | --- |
| GWT-1-1-Exec-A | Godot-specific binding surfaces are named and mapped to spine stages | § Godot binding surface inventory |
| GWT-1-1-Exec-B | Sandbox lane is referenced as **comparand**, not authority over conceptual notes | § Scope + A/B parity contract |
| GWT-1-1-Exec-C | Slice is discoverable as **`1.1`** under execution-local policy | Frontmatter `execution_local_index` + parent link |

## Related

- Parent: [[Phase-1-Execution-Vertical-Slice-Instrumentation-Spine-Roadmap-2026-04-08-2145]]
- Next sibling (registry / telemetry stubs): [[Phase-1-2-Registry-Telemetry-Stubs-Sandbox-AB-Parity-Roadmap-2026-04-09-0000]]
- [[workflow_state-execution]]
- [[roadmap-state-execution]]
- [[../decisions-log]] (**D-Exec-1-numbering-policy**)
