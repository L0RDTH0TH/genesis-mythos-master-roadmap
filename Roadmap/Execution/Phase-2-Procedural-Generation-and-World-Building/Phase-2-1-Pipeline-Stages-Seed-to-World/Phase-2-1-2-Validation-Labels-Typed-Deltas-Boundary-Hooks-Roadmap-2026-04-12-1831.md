---
title: Phase 2.1.2 (Execution) — Validation labels ↔ typed deltas
created: 2026-04-12
tags:
  - roadmap
  - execution
  - godot
project-id: godot-genesis-mythos-master
roadmap_track: execution
phase: 2
subphase: "2.1.2"
roadmap-level: tertiary
status: in-progress
handoff_readiness: 86
handoff_gaps:
  - "Rollup / registry / CI proof rows remain execution-deferred per D-Exec-rollup-deferral."
handoff_audit_last: "2026-04-12T18:31:00Z"
conceptual_counterpart: "[[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-2-Stage-Family-Bodies-and-Boundary-Hooks-Roadmap-2026-03-30-1015]]"
---

# Phase 2.1.2 (Execution) — Validation labels ↔ typed deltas

Execution remint for **Phase 2 tertiary 2.1.2** on the parallel spine. Binds conceptual NL from [[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-2-Stage-Family-Bodies-and-Boundary-Hooks-Roadmap-2026-03-30-1015]] (validation outcome labels → downstream typed deltas at the dry-run/commit boundary) to Godot-typed carrier shapes consistent with [[Phase-2-1-1-Stage-Family-Bodies-and-Boundary-Hooks-Roadmap-2026-04-12-1830]] and [[Phase-2-1-Pipeline-Stages-Seed-to-World-Roadmap-2026-04-12-1616]].

## Intent mapping (execution)

| Conceptual contract | Execution mechanism | Godot metaphor |
| --- | --- | --- |
| `ValidationDecisionLabels` → consumer trace | Stable keyed map from label id → human/diagnostic string | [Dictionary](https://docs.godotengine.org/en/stable/classes/class_dictionary.html) keyed by [StringName](https://docs.godotengine.org/en/stable/classes/class_stringname.html) for interned keys |
| Typed delta fan-out after validation | Stage 4 attaches labels + bounded `TypedStageDeltaBundle` branches | [Variant](https://docs.godotengine.org/en/stable/classes/class_variant.html) as tagged union carrier; avoid silent coercion |
| Boundary hook callback | Single dispatch from labels + artifact → commit gate | [Callable](https://docs.godotengine.org/en/stable/classes/class_callable.html) `is_valid` guard before invoke (same fail-closed pattern as 2.1.1) |

### Doc anchors (stable)

> Dictionary stores values under keys; StringName is an optimized string-like type used for unique names.  
> — paraphrased from Godot class references: [Dictionary](https://docs.godotengine.org/en/stable/classes/class_dictionary.html), [StringName](https://docs.godotengine.org/en/stable/classes/class_stringname.html).

## Label ↔ delta mapping (sketch)

```text
# Pseudocode shape — not a committed engine API
func map_validation_to_deltas(
  labels: Dictionary,        # StringName -> String (diagnostics)
  staged: Dictionary        # stage_id -> Variant (typed bundle leaf)
) -> Dictionary:
  if not _validator_gate_ok(labels, staged):
    return {}                # fail-closed: empty deltas, labels still visible
  return _materialize_typed_deltas(labels, staged)
```

- **Fail-closed:** if Stage 4 denies commit, `map_validation_to_deltas` returns an **empty** delta map while preserving **labels** for tooling (matches conceptual partial-failure clause).
- **Determinism:** mapping depends only on `labels` + staged bundle identity (seed + intent hooks already fixed upstream per 2.1.1).

## Acceptance criteria (execution-first)

| ID | Criterion | Evidence | Status |
| --- | --- | --- | --- |
| AC-2.1.2-A | Label map uses stable `StringName` keys; no ad-hoc string literals in hot path | Key table + grep | Planned |
| AC-2.1.2-B | Deny-commit path emits **zero** typed deltas but retains label map | Blocked-commit trace | Planned |
| AC-2.1.2-C | Commit-allowed path produces deltas consistent with Stage 2 bundle schema | Cross-stage diff harness | Planned |

## Explicit deferrals (D-Exec-rollup-deferral)

- **`GMM-2.4.5-*`**, HR closure, CI run IDs, registry hashes — **not** claimed closed here; rollup/CI IDs remain execution-deferred per project decision records.

## Related

- Prior tertiary **2.1.1**: [[Phase-2-1-1-Stage-Family-Bodies-and-Boundary-Hooks-Roadmap-2026-04-12-1830]]
- Parent secondary (spine): [[Phase-2-1-Pipeline-Stages-Seed-to-World-Roadmap-2026-04-12-1616]]
- Next conceptual sibling: [[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-3-Staged-Delta-Bundles-Merge-Seams-and-Apply-Ordering-Roadmap-2026-03-30-1041]] — execution cursor will deepen **2.1.3** next.
