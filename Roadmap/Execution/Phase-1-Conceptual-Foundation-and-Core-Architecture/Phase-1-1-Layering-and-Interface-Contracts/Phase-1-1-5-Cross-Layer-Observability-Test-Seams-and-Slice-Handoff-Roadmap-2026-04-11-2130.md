---
title: Phase 1.1.5 (Execution) — Cross-layer observability, test seams, and slice handoff
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
subphase-index: "1.1.5"
status: in-progress
handoff_readiness: 86
conceptual_counterpart: "[[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layering-and-Interface-Contracts/Phase-1-1-5-Cross-Layer-Observability-Test-Seams-and-Slice-Handoff-Roadmap-2026-03-30-1431]]"
execution_mirror_of: "Phase-1-1-5-Cross-Layer-Observability-Test-Seams-and-Slice-Handoff-Roadmap-2026-03-30-1431"
---

# Phase 1.1.5 (Execution) — Cross-layer observability, test seams, and slice handoff

Tertiary **1.1.5** execution mirror: **frame/tick-correlated diagnostics**, **published test seams** at documented boundaries, and **slice-handoff language** for closing **1.1.x** before **1.2** — aligned with Godot 4.x **Performance** / **Engine** introspection surfaces and the conceptual NL authority ([[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layering-and-Interface-Contracts/Phase-1-1-5-Cross-Layer-Observability-Test-Seams-and-Slice-Handoff-Roadmap-2026-03-30-1431]]). **Does not** claim **CI verdict closure**, **`missing_roll_up_gates` rollup**, or HR/registry IDs (execution-deferred per [[../../../decisions-log]] **D-Exec-rollup-deferral-missing-roll-up-gates-20260411**).

Parent secondary: [[Phase-1-1-Layering-and-Interface-Contracts-Roadmap-2026-04-10-2110]]. Prior tertiaries: [[Phase-1-1-1-Layer-Boundary-and-Commit-Pipeline-Roadmap-2026-04-10-2359]] … [[Phase-1-1-4-Error-Boundaries-and-Failure-Propagation-Roadmap-2026-04-11-2105]].

## Intent Mapping

| Intent target | Inspiration anchors | Execution mechanism | Validation signal |
| --- | --- | --- | --- |
| Cross-layer correlation id (conceptual) | Single id on intents + commits | Tie lightweight counters to **process** vs **physics** frame indices from **Engine** | Log row can cite `get_process_frames` / `get_physics_frames` at seam |
| Observability without new backends | DiagnosticsSink NL | **Performance.get_monitor** for a **non-authoritative** health scalar at slice boundaries | Debugger / metrics panel shows monitor when hooked |
| Test seams at published boundaries | TestHooks registry | Substitute **Node**-shaped owners behind **add_child** / signal seams from **1.1.3**; no peer-layer private access | Headless scene can swap stub before `_ready` |
| Slice handoff | 1.1.1–1.1.5 checklist | Explicit “1.1.x slice” closure paragraph; **next structural** = **1.2** (not a fake **1.1.6**) | roadmap-state + workflow cursor advance to **1.2** |

## Godot lane (A) — Engine / Performance observability (whitelist-stable docs)

**Frame indices for correlation (tick / physics alignment):**

> Returns the total amount of frames drawn. On headless mode, or if the **RenderingServer** can not render anything, this still increments every frame.

— [Engine.get_frames_drawn](https://docs.godotengine.org/en/stable/classes/class_engine.html#class-engine-method-get-frames-drawn)

> Returns the total amount of frames passed since engine started, **not** paused by **Engine.set_pause** or **SceneTree.pause**.

— [Engine.get_process_frames](https://docs.godotengine.org/en/stable/classes/class_engine.html#class-engine-method-get-process-frames)

> Returns the total amount of fixed process frames passed since the engine started. This number increases every physics frame, even when the game is paused.

— [Engine.get_physics_frames](https://docs.godotengine.org/en/stable/classes/class_engine.html#class-engine-method-get-physics-frames)

**Optional health scalar at boundaries (non-authoritative):**

> Returns the value of one of the available monitors. You should provide one of the [Monitor](https://docs.godotengine.org/en/stable/classes/class_performance.html#enum-performance-monitor) constants as the argument, like this: `Performance.get_monitor(Performance.TIME_FPS)`.

— [Performance.get_monitor](https://docs.godotengine.org/en/stable/classes/class_performance.html#class-performance-method-get-monitor)

### Runnable seam sketch (Godot 4.x GDScript)

Illustrative — layers **1.1.1** commit owner + **1.1.3** lifecycle + **1.1.4** failure surfaces. **Cited APIs** in the sketch: **`Engine.get_process_frames`**, **`Engine.get_physics_frames`**, **`Performance.get_monitor`** (verbatim doc roles above). **Scaffolding** uses **`extends`**, **`signal`**, **`func`** only (same baseline as sibling tertiaries). **No** `class_name`, **no** typed-parameter signals, **no** `enum` / `match` — keeps **`godot_code_precision`** on documented surfaces.

```gdscript
extends Node

signal seam_tick_correlation(process_frame, physics_frame)

func emit_boundary_probe() -> void:
    var pf: int = Engine.get_process_frames()
    var phf: int = Engine.get_physics_frames()
    var _drawn: int = Engine.get_frames_drawn()
    seam_tick_correlation.emit(pf, phf)

func read_non_authoritative_fps_scalar() -> float:
    return Performance.get_monitor(Performance.TIME_FPS)
```

**Discipline:** Monitors and frame indices are **diagnostic** only — they **do not** satisfy **`GMM-2.4.5-*`** or CI rollup; they pair with **1.1.4** `push_error` when a seam violates published contracts.

## Sandbox lane (B) — comparand

C++ tests and profilers are out of scope for this note; lane B remains contract-named only.

## Acceptance criteria (tertiary 1.1.5)

| ID | Criterion | Evidence target | Status |
| --- | --- | --- | --- |
| AC-1.1.5-A | `Engine` frame APIs + `Performance.get_monitor` verbatim + stable links | Quotes above | Met |
| AC-1.1.5-B | Intent mapping ties conceptual observability / test seams / slice handoff to Godot surfaces | Tables + seam sketch | Met |
| AC-1.1.5-C | No rollup / CI IDs claimed | Explicit deferral + closure map | Met |

## Roll-up closure map (progressive evidence)

**Honest status:** `GMM-2.4.5-*` + CI seam rows remain **open** (execution-deferred). This note adds **observability seam IDs** only — **not** CI run IDs or verdict matrix closure.

| Gate ID | Evidence packet | This-run progress | Next evidence |
| --- | --- | --- | --- |
| `GMM-2.4.5-replay-diff` | `.../godot-phase1-gmm-245-replay-diff.md` | Unchanged | Two-run diff matrix rows |
| `GMM-2.4.5-lineage-closure` | `.../godot-phase1-gmm-245-lineage-closure.md` | Unchanged | Verdict rows + lineage IDs |
| `CI-seam-expansion` | `.../godot-phase1-ci-seam-expansion.md` | Unchanged | Stress **CI run IDs** |

Queue context: `followup-deepen-exec-phase1-115-godot-20260411T213000Z` — **do not** claim **rollup debt** closed in-doc; **D-Exec-rollup-deferral-missing-roll-up-gates-20260411** remains authoritative.

## Related

- Conceptual authority: [[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layering-and-Interface-Contracts/Phase-1-1-5-Cross-Layer-Observability-Test-Seams-and-Slice-Handoff-Roadmap-2026-03-30-1431]]
- Parent secondary (execution): [[Phase-1-1-Layering-and-Interface-Contracts-Roadmap-2026-04-10-2110]]
- Prior tertiary: [[Phase-1-1-4-Error-Boundaries-and-Failure-Propagation-Roadmap-2026-04-11-2105]]

## Research integration

> [!note] External grounding
> Verbatim passages from **Godot 4.x stable** class pages (URLs above). No `Ingest/Agent-Research/` synth notes required for this mint; **rollup / CI closure** remains execution-deferred per decisions-log.
