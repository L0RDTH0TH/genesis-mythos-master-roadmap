---
title: Phase 2.1.3 (Execution) — Staged delta bundles, merge seams, apply ordering
created: 2026-04-12
tags:
  - roadmap
  - execution
  - godot
project-id: godot-genesis-mythos-master
roadmap_track: execution
phase: 2
subphase: "2.1.3"
roadmap-level: tertiary
status: in-progress
handoff_readiness: 86
handoff_gaps:
  - "Rollup / registry / CI proof rows remain execution-deferred per D-Exec-rollup-deferral."
handoff_audit_last: "2026-04-12T18:32:00Z"
conceptual_counterpart: "[[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-3-Staged-Delta-Bundles-Merge-Seams-and-Apply-Ordering-Roadmap-2026-03-30-1041]]"
---

# Phase 2.1.3 (Execution) — Staged delta bundles, merge seams, apply ordering

Execution remint for **Phase 2 tertiary 2.1.3** on the parallel spine. Binds conceptual NL from [[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-3-Staged-Delta-Bundles-Merge-Seams-and-Apply-Ordering-Roadmap-2026-03-30-1041]] (bundle assembly, merge seams, canonical apply ordering before Stage 4/5) to Godot-shaped carriers consistent with [[Phase-2-1-2-Validation-Labels-Typed-Deltas-Boundary-Hooks-Roadmap-2026-04-12-1831]] and [[Phase-2-1-Pipeline-Stages-Seed-to-World-Roadmap-2026-04-12-1616]].

## Intent mapping (execution)

| Conceptual contract | Execution mechanism | Godot metaphor |
| --- | --- | --- |
| **StagedDeltaBundle** single pre-commit artifact | One value object carried through Stage 4 → Stage 5 gate | [Dictionary](https://docs.godotengine.org/en/stable/classes/class_dictionary.html) or small [Resource](https://docs.godotengine.org/en/stable/classes/class_resource.html) subclass; keys as [StringName](https://docs.godotengine.org/en/stable/classes/class_stringname.html) for hot identifiers |
| **MergeSeamId** fan-in registry | Stable map seam → merge policy + inputs | Dictionary `seam_id` ([StringName](https://docs.godotengine.org/en/stable/classes/class_stringname.html)) → `{ policy, inputs: Array }` |
| **applyOpsOrdered** total / partial order | Deterministic ordering for replay + tooling | [Array](https://docs.godotengine.org/en/stable/classes/class_array.html) of op records; optional `sort_custom` via [Callable](https://docs.godotengine.org/en/stable/classes/class_callable.html) when partial order collapsed to linear view |
| Labels survive aggregation | Bundle-level + optional per-seam label slices | Reuse **2.1.2** label map pattern; [Variant](https://docs.godotengine.org/en/stable/classes/class_variant.html) leaves for tagged payloads |

### Doc anchors (stable)

> Dictionaries are passed by reference. … Arrays are referenced types. … Callable is a built-in Variant type.  
> — paraphrased from Godot class references: [Dictionary](https://docs.godotengine.org/en/stable/classes/class_dictionary.html), [Array](https://docs.godotengine.org/en/stable/classes/class_array.html), [Callable](https://docs.godotengine.org/en/stable/classes/class_callable.html).

## Bundle assembly (sketch)

```text
# Pseudocode shape — not a committed engine API
func assemble_staged_bundle(
  seam_catalog: Dictionary,          # MergeSeamId -> policy + fan-in refs
  fragments_by_stage: Dictionary    # stage_index -> Array of typed fragments (Variant)
) -> Dictionary:
  var bundle: Dictionary = {
    "bundle_identity": _make_bundle_id(),
    "seam_records": [],
    "apply_ops_ordered": [],
    "validation_labels": {},         # from 2.1.2 contract
    "source_stages": fragments_by_stage.keys()
  }
  for seam_id in _topological_seam_order(seam_catalog):
    var merged = _apply_merge_rule(seam_id, seam_catalog[seam_id], fragments_by_stage)
    bundle["seam_records"].append(merged)
  bundle["apply_ops_ordered"] = _total_order_ops(bundle["seam_records"], default = STAGE_SPINE_ORDER)
  return bundle
```

- **No silent last-writer-wins:** conflicting domain touches require explicit `resolution_record` on the seam row or Stage 4 deny (matches conceptual merge rules).
- **Determinism:** `bundle_identity` hashes seam catalog version + seed bundle id + intent hooks from **2.1.1** path.

## Acceptance criteria (execution-first)

| ID | Criterion | Evidence | Status |
| --- | --- | --- | --- |
| AC-2.1.3-A | Every merge seam declares a named policy family (no implicit merge) | Seam table + unit deny on missing policy | Planned |
| AC-2.1.3-B | `apply_ops_ordered` reconstructible from bundle + catalog alone (replay) | Round-trip diff harness | Planned |
| AC-2.1.3-C | Stage 4 evaluates **whole bundle** + labels; deny path yields **no** apply ops | Blocked-commit trace | Planned |

## Explicit deferrals (D-Exec-rollup-deferral)

- **`GMM-2.4.5-*`**, HR closure, CI run IDs, registry hashes — **not** claimed closed here; rollup/CI IDs remain execution-deferred per project decision records and [[../../../decisions-log]].

## Related

- Prior tertiary **2.1.2**: [[Phase-2-1-2-Validation-Labels-Typed-Deltas-Boundary-Hooks-Roadmap-2026-04-12-1831]]
- Parent secondary (spine): [[Phase-2-1-Pipeline-Stages-Seed-to-World-Roadmap-2026-04-12-1616]]
- Next execution tertiary **2.1.4**: [[Phase-2-1-4-Bundle-Identity-Seam-Catalog-Stability-and-Replay-Diff-Roadmap-2026-04-12-2005]] (minted **2026-04-12 20:05**). Conceptual sibling: [[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-4-Bundle-Identity-Seam-Catalog-Stability-and-Replay-Diff-Roadmap-2026-03-30-2305]].
