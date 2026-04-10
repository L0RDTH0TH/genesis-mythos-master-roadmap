---
title: Phase 1.1.1 (Execution) — Layer boundary and commit pipeline
created: 2026-04-10
tags:
  - roadmap
  - execution
  - godot
  - sandbox-comparand
project-id: godot-genesis-mythos-master
roadmap_track: execution
roadmap-level: tertiary
phase-number: 1
subphase-index: "1.1.1"
status: in-progress
handoff_readiness: 86
conceptual_counterpart: "[[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layering-and-Interface-Contracts/Phase-1-1-1-Layer-Boundary-and-Commit-Pipeline-Roadmap-2026-03-30-0431]]"
execution_mirror_of: "Phase-1-1-1-Layer-Boundary-and-Commit-Pipeline-Roadmap-2026-03-30-0431"
---

# Phase 1.1.1 (Execution) — Layer boundary and commit pipeline

Tertiary **1.1.1** execution mirror for **layer boundary + commit pipeline** on the parallel spine. Binds conceptual NL (single committer, staged delta → commit, render read-only) to **Godot 4.x** tick boundaries (`_physics_process`, `SceneTree` frame signals) and **GDScript** signal wiring for post-physics notification. Parent secondary: [[Phase-1-1-Layering-and-Interface-Contracts-Roadmap-2026-04-10-2110]].

## Intent Mapping

| Intent target | Inspiration anchors | Execution mechanism | Validation signal |
| --- | --- | --- | --- |
| Fixed-tick sim vs frame UI | Conceptual 1.1.1 tick slice + PMG single committer | `_physics_process` for staged work; deferred commit group or `physics_frame` ordering | AC-1.1.1.1-* + hook IDs in closure map |
| Post-physics observation | SceneTree signal docs | `SceneTree.physics_frame` / `process_frame` boundaries | Trace log shows ordering vs `_physics_process` |
| Decoupled notify after commit | GDScript signals docs | `signal commit_completed` emit after store apply | Connect test stub receives after physics tick |

## Godot lane (A) — tick boundary + commit seam

Official stable docs establish **physics processing** as fixed-rate vs **process** as frame-rate–dependent, which maps directly to conceptual “one tick” staging:

> Processing: Nodes can override the "process" state, so that they receive a callback on each frame requesting them to process (do something). Normal processing (callback `_process()`, toggled with `set_process()`) happens as fast as possible and is dependent on the frame rate, so the processing time delta (in seconds) is passed as an argument. Physics processing (callback `_physics_process()`, toggled with `set_physics_process()`) happens a fixed number of times per second (60 by default) and is useful for code related to the physics engine.

— [Node](https://docs.godotengine.org/en/stable/classes/class_node.html)

> Called once on each physics tick, and allows Nodes to synchronize their logic with physics ticks.

— [Node — `_physics_process`](https://docs.godotengine.org/en/stable/classes/class_node.html#class-node-private-method-physics-process)

**SceneTree ordering (commit / observe boundaries):**

> **physics_frame()** — Emitted immediately before `Node._physics_process()` is called on every node in this tree.

> **process_frame()** — Emitted immediately before `Node._process()` is called on every node in this tree.

— [SceneTree — Signals](https://docs.godotengine.org/en/stable/classes/class_scenetree.html#class-scenetree-signal-physics-frame)

**GDScript signals (emit after staged state is valid):**

> Signals are a tool to emit messages from an object that other objects can react to. To create custom signals for a class, use the `signal` keyword.

— [GDScript basics — Signals](https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_basics.html#signals)

### Runnable seam sketch (Godot 4.x GDScript)

Illustrative only — names match parent `IGameLoopKernel` / store facades; precision citations above gate API usage.

```gdscript
extends Node

signal commit_completed(tick_index: int, ok: bool)

var _tick_index: int = 0

func _physics_process(delta: float) -> void:
    # Staged delta from sim intent drain (lane-specific; no direct world mutation here)
    var staged := _kernel_step_staged(delta)
    var ok: bool = world_state_store.apply_delta_staged(staged, _tick_index)
    if ok:
        commit_completed.emit(_tick_index, true)
    else:
        commit_completed.emit(_tick_index, false)
    _tick_index += 1
```

`process_mode` for auxiliary UI or render-facing nodes can be set per layer (`PROCESS_MODE_INHERIT` default; disabled when pause must freeze non-sim layers) — see [Node — ProcessMode](https://docs.godotengine.org/en/stable/classes/class_node.html#enum-node-processmode).

## Sandbox lane (B) — comparand

Fixed-step C++ scheduler replaces `_physics_process`; same **single committer** and **emit-after-commit** pattern using a typed callback + observer channel (no GDScript in lane B deliverables in this note).

## Acceptance criteria (tertiary 1.1.1)

| ID | Criterion | Evidence target | Status |
| --- | --- | --- | --- |
| AC-1.1.1.1-A | Physics vs process boundary cited for tick work | Verbatim quotes + link rows above | Met |
| AC-1.1.1.1-B | Post-physics notify path documented | `commit_completed` + SceneTree ordering rationale | Met |
| AC-1.1.1.1-C | No authoritative render write in sketch | Comment + negative test hook ID in closure map | Planned |

## Roll-up closure map (progressive evidence)

Queue: `followup-deepen-exec-phase1-1-godot-20260410T210701Z` / deepen `followup-deepen-exec-phase1-1-godot-20260410T210701Z`.

| Gate ID | Evidence packet | This-run progress | Next evidence |
| --- | --- | --- | --- |
| `GMM-2.4.5-replay-diff` | `.../godot-phase1-gmm-245-replay-diff.md` | Parent hash pair still authoritative; **add tick-index column** tying replay rows to `_tick_index` | Two-run diff matrix rows |
| `GMM-2.4.5-lineage-closure` | `.../godot-phase1-gmm-245-lineage-closure.md` | Schema path reserved | Verdict rows + lineage IDs |
| `CI-seam-expansion` | `.../godot-phase1-ci-seam-expansion.md` | Owners restated | Record stress **CI run IDs** + artifact links |

Statuses remain **open** until packets carry verdict / CI IDs; this run advances **godot_code_precision** traceability for **1.1.1**.

## Gate evidence / waivers (repair pass — `missing_roll_up_gates`)

> **Architect:** Queue `followup-deepen-exec-phase1-1-1-godot-20260410T211500Z` asked to record **gate evidence / waivers** for nested validator code **`missing_roll_up_gates`** on tertiary **1.1.1** after the prior deepen mint. Vault cursor is already **`1.1.2`** ([[../../../workflow_state-execution]]); this section is **repair documentation** on the **1.1.1** mirror, not a cursor rewind.

**Waivers (execution-deferred — do not treat as authoritative rollup closure):**

| Code | Scope | Waiver basis | Honest status |
| --- | --- | --- | --- |
| `missing_roll_up_gates` | `GMM-2.4.5-*`, `CI-seam-expansion` | Real rollup closure needs **verdict rows**, **lineage IDs**, and **stress CI run IDs** — **not** inventable in markdown | **Open** — **execution-deferred** per [[3-Resources/Second-Brain/Docs/Dual-Roadmap-Track|Dual-Roadmap-Track]] and the execution rollup waiver in [[../../../roadmap-state-execution]]; structural **deepen** along the parallel spine continues per [[../../../workflow_state-execution]] |

**Cross-links (stub binding, not fake closure):**

- Handoff-audit repair queue: `repair-handoff-audit-godot-exec-phase1-rollup-20260410T210700Z` (stub evidence packets under `3-Resources/Second-Brain/Validator-Reports/Execution-Gates/`).
- **No** CI run IDs or matrix verdict rows are claimed here.

**Schema-level evidence already in this note (not rollup-complete):**

- Tick-index column intent in the closure map ties replay rows to `_tick_index`; **two-run diff matrix** rows remain **outstanding**.

This satisfies the queue **`user_guidance`** to record **waiver/evidence posture** for **`missing_roll_up_gates`** without fabricating IDs or marking gates closed.

## Related

- Conceptual authority: [[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layering-and-Interface-Contracts/Phase-1-1-1-Layer-Boundary-and-Commit-Pipeline-Roadmap-2026-03-30-0431]]
- Parent secondary (execution): [[Phase-1-1-Layering-and-Interface-Contracts-Roadmap-2026-04-10-2110]]
