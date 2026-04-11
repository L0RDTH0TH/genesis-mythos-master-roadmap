---
title: Phase 1.1.3 (Execution) — Dependency direction and lifecycle
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
subphase-index: "1.1.3"
status: in-progress
handoff_readiness: 86
conceptual_counterpart: "[[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layering-and-Interface-Contracts/Phase-1-1-3-Dependency-Direction-and-Lifecycle-Roadmap-2026-03-30-1420]]"
execution_mirror_of: "Phase-1-1-3-Dependency-Direction-and-Lifecycle-Roadmap-2026-03-30-1420"
---

# Phase 1.1.3 (Execution) — Dependency direction and lifecycle

Tertiary **1.1.3** execution mirror for **acyclic cross-layer dependency rules**, **SceneTree parent/child wiring**, and **boot / teardown ordering** on the parallel spine. Aligns conceptual NL ([[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layering-and-Interface-Contracts/Phase-1-1-3-Dependency-Direction-and-Lifecycle-Roadmap-2026-03-30-1420]]) with **Godot 4.x** `Node` lifecycle (`_enter_tree`, `_exit_tree`, `tree_exiting`) and **`add_child`** — **without** claiming **CI verdict closure**, **`missing_roll_up_gates` rollup**, or registry IDs (execution-deferred per [[../../../decisions-log]] **D-Exec-rollup-deferral-missing-roll-up-gates-20260411**).

Parent secondary: [[Phase-1-1-Layering-and-Interface-Contracts-Roadmap-2026-04-10-2110]]. Prior tertiaries: [[Phase-1-1-1-Layer-Boundary-and-Commit-Pipeline-Roadmap-2026-04-10-2359]], [[Phase-1-1-2-Observation-Cache-and-Invalidation-Roadmap-2026-04-11-0012]].

## Intent Mapping

| Intent target | Inspiration anchors | Execution mechanism | Validation signal |
| --- | --- | --- | --- |
| Dependency direction (DAG across layers) | Conceptual authority / data-flow edges | `Node` parent chain + explicit `add_child` order; no upstream write except commit path | Audit: sim/render edges match allow-list |
| Injection / registration seams | Conceptual named stages | Child nodes registered under owner `Node` after tree entry; teardown uses `_exit_tree` order | Stub: registry empty after `remove_child` |
| Lifecycle + quiesce before swap | Conceptual boot/teardown + epoch from 1.1.2 | `_exit_tree` last-after-children; connect `tree_exiting` for quiesce hook | Trace: `epoch_bumped` not emitted after `tree_exiting` fires |

## Godot lane (A) — SceneTree order and lifecycle

**Enter / ready ordering (authoritative for “who runs first”):**

> When a node is added to the scene tree, it receives the NOTIFICATION_ENTER_TREE notification and its _enter_tree() callback is triggered. Child nodes are always added after their parent node, i.e. the _enter_tree() callback of a parent node will be triggered before its child's.

— [Node — Description (Scene tree)](https://docs.godotengine.org/en/stable/classes/class_node.html#description)

> This means that when adding a node to the scene tree, the following order will be used for the callbacks: _enter_tree() of the parent, _enter_tree() of the children, _ready() of the children and finally _ready() of the parent (recursively for the entire scene tree).

— [Node — Description (Scene tree)](https://docs.godotengine.org/en/stable/classes/class_node.html#description)

**Teardown ordering (swap / quiesce):**

> Called when the node is about to leave the SceneTree (e.g. upon freeing, scene changing, or after calling remove_child() in a script). If the node has children, its _exit_tree() callback will be called last, after all its children have left the tree.

— [Node — `_exit_tree`](https://docs.godotengine.org/en/stable/classes/class_node.html#class-node-private-method-exit-tree)

**`tree_exiting` signal (late de-init hook — node still valid):**

> Emitted when the node is just about to exit the tree. The node is still valid. As such, this is the right place for de-initialization (or a "destructor", if you will).
>
> This signal is emitted after the node's _exit_tree(), and before the related NOTIFICATION_EXIT_TREE.

— [Node — `tree_exiting`](https://docs.godotengine.org/en/stable/classes/class_node.html#class-node-signal-tree-exiting)

**Dynamic wiring (`add_child`):**

> Called when the node enters the SceneTree (e.g. upon instantiating, scene changing, or after calling add_child() in a script). If the node has children, its _enter_tree() callback will be called first, and then that of the children.

— [Node — `_enter_tree`](https://docs.godotengine.org/en/stable/classes/class_node.html#class-node-private-method-enter-tree)

> void add_child(node: Node, force_readable_name: bool = false, internal: InternalMode = 0)

— [Node — `add_child`](https://docs.godotengine.org/en/stable/classes/class_node.html#class-node-method-add-child)

**GDScript signals (custom registration seam):**

> Signals are a tool to emit messages from an object that other objects can react to. To create custom signals for a class, use the `signal` keyword.

— [GDScript basics — Signals](https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_basics.html#signals)

### Runnable seam sketch (Godot 4.x GDScript)

Illustrative only — extends **1.1.1** commit owner + **1.1.2** `epoch_bumped` with **registration** and **quiesce** ordering. Uses the same token grammar as sibling execution notes (`extends`, `signal`, `connect`) with citations above.

```gdscript
extends Node

signal seam_registered(seam_id)
signal seam_quiesced(seam_id)

var _seams = {}

func mount_seam(seam_id, impl):
    add_child(impl)
    _seams[seam_id] = impl
    seam_registered.emit(seam_id)

func unmount_seam(seam_id):
    var n = _seams.get(seam_id, null)
    if n == null:
        return
    seam_quiesced.emit(seam_id)
    remove_child(n)
    n.queue_free()
    _seams.erase(seam_id)
```

**Swap discipline:** `_exit_tree()` on the seam implementation runs **before** the parent’s `_exit_tree()` when unwinding nested children (see `_exit_tree` description above). Emit **quiesce** / stop **epoch** consumers in the child’s `_exit_tree()` or via `tree_exiting` (docs: after `_exit_tree()`, before `NOTIFICATION_EXIT_TREE`) — align with [[Phase-1-1-2-Observation-Cache-and-Invalidation-Roadmap-2026-04-11-0012]] so `epoch_bumped` does not race teardown.

## Sandbox lane (B) — comparand

C++ uses explicit **init / shutdown** virtuals on a **directed** module graph; teardown walks dependents-before-dependencies — no GDScript in lane B deliverables in this note.

## Acceptance criteria (tertiary 1.1.3)

| ID | Criterion | Evidence target | Status |
| --- | --- | --- | --- |
| AC-1.1.3-A | Parent/child `_enter_tree` / `_ready` order cited for dependency direction | Verbatim quotes + stable links above | Met |
| AC-1.1.3-B | `_exit_tree` / `tree_exiting` cited for teardown ordering | Verbatim quotes + links above | Met |
| AC-1.1.3-C | No rollup / CI IDs claimed | Explicit deferral + closure map | Met |

## Roll-up closure map (progressive evidence)

**Honest status:** `GMM-2.4.5-*` + CI seam rows remain **open** (execution-deferred). This note adds **lifecycle hook IDs** only — **not** CI run IDs or verdict matrix closure.

| Gate ID | Evidence packet | This-run progress | Next evidence |
| --- | --- | --- | --- |
| `GMM-2.4.5-replay-diff` | `.../godot-phase1-gmm-245-replay-diff.md` | Unchanged | Two-run diff matrix rows |
| `GMM-2.4.5-lineage-closure` | `.../godot-phase1-gmm-245-lineage-closure.md` | Unchanged | Verdict rows + lineage IDs |
| `CI-seam-expansion` | `.../godot-phase1-ci-seam-expansion.md` | Unchanged | Stress **CI run IDs** |

Queue context: `followup-deepen-exec-phase1-113-godot-20260411T001500Z` — **do not** claim **rollup debt** closed in-doc; **D-Exec-rollup-deferral-missing-roll-up-gates-20260411** remains authoritative.

## Related

- Conceptual authority: [[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layering-and-Interface-Contracts/Phase-1-1-3-Dependency-Direction-and-Lifecycle-Roadmap-2026-03-30-1420]]
- Parent secondary (execution): [[Phase-1-1-Layering-and-Interface-Contracts-Roadmap-2026-04-10-2110]]
- Commit seam: [[Phase-1-1-1-Layer-Boundary-and-Commit-Pipeline-Roadmap-2026-04-10-2359]]
- Observation / epoch: [[Phase-1-1-2-Observation-Cache-and-Invalidation-Roadmap-2026-04-11-0012]]
