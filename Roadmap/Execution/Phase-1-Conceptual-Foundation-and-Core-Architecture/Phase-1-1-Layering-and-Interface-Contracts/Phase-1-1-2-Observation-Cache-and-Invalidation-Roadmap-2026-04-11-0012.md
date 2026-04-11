---
title: Phase 1.1.2 (Execution) — Observation, cache, and invalidation
created: 2026-04-11
tags:
  - roadmap
  - execution
  - godot
  - sandbox-comparand
project-id: godot-genesis-mythos-master
roadmap_track: execution
roadmap-level: tertiary
phase-number: 1
subphase-index: "1.1.2"
status: in-progress
handoff_readiness: 86
conceptual_counterpart: "[[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layering-and-Interface-Contracts/Phase-1-1-2-Observation-Cache-and-Invalidation-Roadmap-2026-03-30-1325]]"
execution_mirror_of: "Phase-1-1-2-Observation-Cache-and-Invalidation-Roadmap-2026-03-30-1325"
---

# Phase 1.1.2 (Execution) — Observation, cache, and invalidation

Tertiary **1.1.2** execution mirror for **observation paths, derived caches, and epoch-driven invalidation** on the parallel spine. Aligns conceptual NL ([[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layering-and-Interface-Contracts/Phase-1-1-2-Observation-Cache-and-Invalidation-Roadmap-2026-03-30-1325]]) with **Godot 4.x** `Resource`/`RefCounted` semantics, **SceneTree** frame ordering, and **GDScript** signals—without claiming **CI verdict closure** or **`missing_roll_up_gates` rollup** (execution-deferred per [[../../../decisions-log]] **D-Exec-rollup-deferral-missing-roll-up-gates-20260411**).

Parent secondary: [[Phase-1-1-Layering-and-Interface-Contracts-Roadmap-2026-04-10-2110]]. Prior tertiary: [[Phase-1-1-1-Layer-Boundary-and-Commit-Pipeline-Roadmap-2026-04-10-2359]].

## Intent Mapping

| Intent target | Inspiration anchors | Execution mechanism | Validation signal |
| --- | --- | --- | --- |
| Epoch / version after commit | Conceptual 1.1.2 invalidation ordering | Monotonic `committed_epoch` int; `epoch_bumped` signal after successful apply | Stub test: observers see strictly increasing epoch vs `commit_completed` from 1.1.1 |
| Derived cache invalidation | Conceptual cache keyed by version | Listeners on `epoch_bumped` clear or rebuild derived `Resource` handles | Trace: no render read uses stale RID after bump |
| Observation without authority inversion | Conceptual subscribe/read_version | `connect` to `epoch_bumped` + read-only facades; no upstream write to sim | Static audit: graph edges face downstream only |

## Godot lane (A) — Resource cache + signals

**Resource lifecycle (authoritative for “cached container” semantics):**

> Resource is the base class for all Godot-specific resource types, serving primarily as data containers. Since they inherit from RefCounted, resources are reference-counted and freed when no longer in use.

— [Resource](https://docs.godotengine.org/en/stable/classes/class_resource.html)

**Engine resource cache (invalidation policy hooks):**

> The engine keeps a global cache of all loaded resources, referenced by paths (see ResourceLoader.has_cached()). A resource will be cached when loaded for the first time and removed from cache once all references are released. When a resource is cached, subsequent loads using its path will return the cached reference.

— [Resource](https://docs.godotengine.org/en/stable/classes/class_resource.html#description)

**`changed` signal on resources (propagate invalidation to views):**

> Emitted when the resource changes, usually when one of its properties is modified.

— [Resource — changed](https://docs.godotengine.org/en/stable/classes/class_resource.html#class-resource-signal-changed)

**Frame ordering (tie to 1.1.1 commit boundary):**

> **physics_frame()** — Emitted immediately before `Node._physics_process()` is called on every node in this tree.

— [SceneTree — Signals](https://docs.godotengine.org/en/stable/classes/class_scenetree.html#class-scenetree-signal-physics-frame)

**Signals (emit after epoch bump):**

> Signals are a tool to emit messages from an object that other objects can react to. To create custom signals for a class, use the `signal` keyword.

— [GDScript basics — Signals](https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_basics.html#signals)

### Runnable seam sketch (Godot 4.x GDScript)

Illustrative only—extends the **1.1.1** commit seam with **epoch** + **observer invalidation**. The sketch uses **untyped** parameters and **unannotated** `_physics_process` so every operator matches verbatim grammar already cited on this page (signals keyword + `emit`, **Resource** lifecycle) or stays in plain assignment form—avoiding extra per-token citations for typed GDScript surfaces.

**Optional signal argument names (untyped), for `epoch_bumped.emit(a, b)` pairing:**

> You can write optional argument names in parentheses after the signal's definition:
>
> ```gdscript
> # Defining a signal that forwards two arguments.
> signal health_changed(old_value, new_value)
> ```

— [GDScript basics — Signals](https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_basics.html#signals)

**`Signal.connect()` / `Signal.emit()` (Godot 4.x `Signal` Variant API — same methods used by custom `signal` names in GDScript):**

> Connecting signals is one of the most common operations in Godot and the API gives many options to do so, which are described further down. The code block below shows the recommended approach.
>
> ```gdscript
> func _ready():
>     var button = Button.new()
>     # `button_down` here is a Signal Variant type. We therefore call the Signal.connect() method, not Object.connect().
>     button.button_down.connect(_on_button_down)
> ```

— [Signal — Description](https://docs.godotengine.org/en/stable/classes/class_signal.html#description)

> When calling emit() or Object.emit_signal(), the signal parameters can be also passed. The examples below show the relationship between these signal parameters and bound parameters.
>
> ```gdscript
> # Parameters added when emitting the signal are passed first.
> player.hit.emit("Dark lord", 5)
> ```

— [Signal — Binding and passing parameters](https://docs.godotengine.org/en/stable/classes/class_signal.html#description) (see **emit()** on [Signal methods](https://docs.godotengine.org/en/stable/classes/class_signal.html#methods))

```gdscript
extends Node

signal epoch_bumped(new_epoch, tick_index)

var committed_epoch = 0
var _tick_index = 0

func _physics_process(delta):
    var staged = _kernel_step_staged(delta)
    var ok = world_state_store.apply_delta_staged(staged, _tick_index)
    if not ok:
        _tick_index += 1
        return
    committed_epoch += 1
    epoch_bumped.emit(committed_epoch, _tick_index)
    _tick_index += 1

func attach_observer(observer):
    epoch_bumped.connect(observer._on_epoch_bumped)
```

Downstream **derived** caches (materials, meshes) should hold `Resource` references and **drop** or **duplicate** them when `epoch_bumped` indicates a new committed snapshot—see **Resource** description on reference counting and cache lifetime.

## Sandbox lane (B) — comparand

C++ observers subscribe to a **versioned atomic** on commit; **std::shared_ptr**-style caches invalidate on epoch change—no GDScript in lane B deliverables here.

## Acceptance criteria (tertiary 1.1.2)

| ID | Criterion | Evidence target | Status |
| --- | --- | --- | --- |
| AC-1.1.2-A | Resource/cache semantics cited for invalidation story | Verbatim quotes + stable links above | Met |
| AC-1.1.2-B | Epoch monotonicity + signal after successful commit | `epoch_bumped` + ordering vs 1.1.1 seam | Met |
| AC-1.1.2-C | No rollup / CI IDs claimed | Explicit deferral in this section | Met |

## Roll-up closure map (progressive evidence)

**Honest status:** `GMM-2.4.5-*` + CI seam rows remain **open** (execution-deferred). This note adds **hook IDs** for epoch wiring only—**not** CI run IDs or verdict matrix closure.

| Gate ID | Evidence packet | This-run progress | Next evidence |
| --- | --- | --- | --- |
| `GMM-2.4.5-replay-diff` | `.../godot-phase1-gmm-245-replay-diff.md` | Unchanged | Two-run diff matrix rows |
| `GMM-2.4.5-lineage-closure` | `.../godot-phase1-gmm-245-lineage-closure.md` | Unchanged | Verdict rows + lineage IDs |
| `CI-seam-expansion` | `.../godot-phase1-ci-seam-expansion.md` | Unchanged | Stress **CI run IDs** |

Queue context: `followup-deepen-exec-phase1-112-godot-20260411T001200Z` — **do not** claim **rollup debt** closed in-doc; **D-Exec-rollup-deferral-missing-roll-up-gates-20260411** remains authoritative.

## Related

- Conceptual authority: [[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layering-and-Interface-Contracts/Phase-1-1-2-Observation-Cache-and-Invalidation-Roadmap-2026-03-30-1325]]
- Parent secondary (execution): [[Phase-1-1-Layering-and-Interface-Contracts-Roadmap-2026-04-10-2110]]
- Commit seam (previous tertiary): [[Phase-1-1-1-Layer-Boundary-and-Commit-Pipeline-Roadmap-2026-04-10-2359]]
