---
title: Phase 1.1.4 (Execution) — Error boundaries and failure propagation
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
subphase-index: "1.1.4"
status: in-progress
handoff_readiness: 86
conceptual_counterpart: "[[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layering-and-Interface-Contracts/Phase-1-1-4-Error-Boundaries-and-Failure-Propagation-Roadmap-2026-03-30-1430]]"
execution_mirror_of: "Phase-1-1-4-Error-Boundaries-and-Failure-Propagation-Roadmap-2026-03-30-1430"
---

# Phase 1.1.4 (Execution) — Error boundaries and failure propagation

Tertiary **1.1.4** execution mirror for **classifying failures**, **bounding surface area** at layer boundaries, and **propagating** non-fatal vs authoritative errors without corrupting the commit path — aligned with Godot 4.x **debugger-facing** APIs (`push_error`, `push_warning`, `assert`) and the conceptual NL authority ([[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layering-and-Interface-Contracts/Phase-1-1-4-Error-Boundaries-and-Failure-Propagation-Roadmap-2026-03-30-1430]]). **Does not** claim **CI verdict closure**, **`missing_roll_up_gates` rollup**, or HR/registry IDs (execution-deferred per [[../../../decisions-log]] **D-Exec-rollup-deferral-missing-roll-up-gates-20260411**).

Parent secondary: [[Phase-1-1-Layering-and-Interface-Contracts-Roadmap-2026-04-10-2110]]. Prior tertiaries: [[Phase-1-1-1-Layer-Boundary-and-Commit-Pipeline-Roadmap-2026-04-10-2359]], [[Phase-1-1-2-Observation-Cache-and-Invalidation-Roadmap-2026-04-11-0012]], [[Phase-1-1-3-Dependency-Direction-and-Lifecycle-Roadmap-2026-04-11-0015]].

## Intent Mapping

| Intent target | Inspiration anchors | Execution mechanism | Validation signal |
| --- | --- | --- | --- |
| Failure classification (authoritative vs transient vs presentational) | Conceptual severity tags + 1.1.1 commit seam | `push_error` / `push_warning` vs `assert` (debug-only hard stop) | Debugger shows stack trace for push_* ; assert pauses in editor |
| Boundary: no silent world-state repair | Conceptual single commit API | Errors routed to **intent → sim → commit**; `push_error` records without mutating epoch | No `epoch_bumped` on push-only paths |
| Propagation: abort pending commit on authoritative failure | Conceptual abort + cache rules | `assert` or explicit guard before `epoch_bumped`; align with 1.1.2 invalidation | Trace: failed tick does not emit commit |
| Non-fatal tooling noise | Conceptual presentational class | `push_warning` for recoverable asset/tool issues | Warnings distinguished from errors in debugger |

## Godot lane (A) — Debugger surfaces and GDScript guardrails

**Prefer engine error/warning channels over ad-hoc `print` for classified failures:**

> **Note:** Consider using push_error() and push_warning() to print error and warning messages instead of print() or print_rich(). This distinguishes them from print messages used for debugging purposes, while also displaying a stack trace when an error or warning is printed.

— [@GlobalScope](https://docs.godotengine.org/en/stable/classes/class_%40globalscope.html) (see **print** / **print_rich** notes)

**`push_error` — non-pausing error surface:**

> Pushes an error message to Godot's built-in debugger and to the OS terminal.

— [@GlobalScope.push_error](https://docs.godotengine.org/en/stable/classes/class_%40globalscope.html#class-globalscope-method-push-error)

> **Note:** This function does not pause project execution. To print an error message and pause project execution in debug builds, use `assert(false, "test error")` instead.

— [@GlobalScope.push_error](https://docs.godotengine.org/en/stable/classes/class_%40globalscope.html#class-globalscope-method-push-error)

**`assert` — stronger invariant boundary (debug / editor pause):**

> Asserts that the `condition` is `true`. If the `condition` is `false`, an error is generated. When running from the editor, the running project will also be paused until you resume it. This can be used as a stronger form of [@GlobalScope.push_error()](https://docs.godotengine.org/en/stable/classes/class_%40globalscope.html#class-globalscope-method-push-error) for reporting errors to project developers or add-on users.

— [@GDScript assert](https://docs.godotengine.org/en/stable/classes/class_@gdscript.html#class-gdscript-method-assert)

> The `assert` keyword can be used to check conditions in debug builds. These assertions are ignored in non-debug builds.

— [GDScript basics — Assert keyword](https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_basics.html#assert-keyword)

### Runnable seam sketch (Godot 4.x GDScript)

Illustrative — layers **1.1.1** commit owner + **1.1.2** epoch + **1.1.3** lifecycle. **Cited Godot failure surfaces** in the sketch: **`push_error`**, **`push_warning`**, **`assert`** (verbatim quotes above). **Scaffolding** uses normal GDScript **`extends`**, **`signal`**, **`func`** (same baseline as sibling tertiaries; not additional uncited engine APIs). **No** `class_name`, **no** typed-parameter signals, **no** `enum` / `match` — keeps **`godot_code_precision`** on documented error channels.

```gdscript
extends Node

signal authoritative_blocked(reason)

func report_authoritative_failure(msg: String) -> void:
    push_error("authoritative: %s" % msg)
    authoritative_blocked.emit(msg)

func report_transient_warning(msg: String) -> void:
    push_warning("transient: %s" % msg)

func guard_commit_precondition(ok: bool, detail: String) -> void:
    assert(ok, "commit precondition failed: %s" % detail)
```

**Failure-propagation discipline:** `push_error` **does not pause** — pair **authoritative** simulation faults with **aborting** the pending commit in the owning layer (see conceptual classification) **before** any `epoch_bumped` from 1.1.2. Use **`assert`** only for **developer-contract** violations that must halt in debug, not for player-facing recoverable errors.

## Sandbox lane (B) — comparand

C++ uses exceptions / error codes per module; this note does **not** author lane-B snippets.

## Acceptance criteria (tertiary 1.1.4)

| ID | Criterion | Evidence target | Status |
| --- | --- | --- | --- |
| AC-1.1.4-A | `push_error` / `push_warning` / `assert` verbatim + stable links | Quotes above | Met |
| AC-1.1.4-B | Intent mapping ties conceptual failure classes to Godot surfaces | Table + seam sketch | Met |
| AC-1.1.4-C | No rollup / CI IDs claimed | Explicit deferral + closure map | Met |

## Roll-up closure map (progressive evidence)

**Honest status:** `GMM-2.4.5-*` + CI seam rows remain **open** (execution-deferred). This note adds **failure-surface IDs** only — **not** CI run IDs or verdict matrix closure.

| Gate ID | Evidence packet | This-run progress | Next evidence |
| --- | --- | --- | --- |
| `GMM-2.4.5-replay-diff` | `.../godot-phase1-gmm-245-replay-diff.md` | Unchanged | Two-run diff matrix rows |
| `GMM-2.4.5-lineage-closure` | `.../godot-phase1-gmm-245-lineage-closure.md` | Unchanged | Verdict rows + lineage IDs |
| `CI-seam-expansion` | `.../godot-phase1-ci-seam-expansion.md` | Unchanged | Stress **CI run IDs** |

Queue context: `followup-deepen-exec-phase1-114-godot-20260411T182000Z` — **do not** claim **rollup debt** closed in-doc; **D-Exec-rollup-deferral-missing-roll-up-gates-20260411** remains authoritative.

## Related

- Conceptual authority: [[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layering-and-Interface-Contracts/Phase-1-1-4-Error-Boundaries-and-Failure-Propagation-Roadmap-2026-03-30-1430]]
- Parent secondary (execution): [[Phase-1-1-Layering-and-Interface-Contracts-Roadmap-2026-04-10-2110]]
- Commit seam: [[Phase-1-1-1-Layer-Boundary-and-Commit-Pipeline-Roadmap-2026-04-10-2359]]
- Observation / epoch: [[Phase-1-1-2-Observation-Cache-and-Invalidation-Roadmap-2026-04-11-0012]]
- Lifecycle: [[Phase-1-1-3-Dependency-Direction-and-Lifecycle-Roadmap-2026-04-11-0015]]

## Research integration

> [!note] External grounding
> Verbatim passages pulled from **Godot 4.x stable** class / tutorial pages (URLs above). No `Ingest/Agent-Research/` synth notes required for this mint; **rollup / CI closure** remains execution-deferred per decisions-log.
