---
title: Phase 2.1.4 (Execution) — Bundle identity, seam catalog stability, replay diff
created: 2026-04-12
tags:
  - roadmap
  - execution
  - godot
project-id: godot-genesis-mythos-master
roadmap_track: execution
phase: 2
subphase: "2.1.4"
roadmap-level: tertiary
status: in-progress
handoff_readiness: 86
handoff_gaps:
  - "Rollup / registry / CI proof rows remain execution-deferred per D-Exec-rollup-deferral."
handoff_audit_last: "2026-04-12T20:05:00Z"
conceptual_counterpart: "[[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-4-Bundle-Identity-Seam-Catalog-Stability-and-Replay-Diff-Roadmap-2026-03-30-2305]]"
---

# Phase 2.1.4 (Execution) — Bundle identity, seam catalog stability, replay diff

Execution remint for **Phase 2 tertiary 2.1.4** on the parallel spine. Binds conceptual NL from [[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-4-Bundle-Identity-Seam-Catalog-Stability-and-Replay-Diff-Roadmap-2026-03-30-2305]] (bundle identity composition, **SeamCatalogRevision**, replay-equivalence, deterministic bundle diff) to Godot-shaped carriers consistent with [[Phase-2-1-3-Staged-Delta-Bundles-Merge-Seams-and-Apply-Ordering-Roadmap-2026-04-12-1832]] and [[Phase-2-1-Pipeline-Stages-Seed-to-World-Roadmap-2026-04-12-1616]].

## Intent mapping (execution)

| Conceptual contract | Execution mechanism | Godot metaphor |
| --- | --- | --- |
| **BundleIdentity** logical tuple | Serializable record carried with the staged bundle | [Dictionary](https://docs.godotengine.org/en/stable/classes/class_dictionary.html) with [StringName](https://docs.godotengine.org/en/stable/classes/class_stringname.html) keys for `seed_bundle_ref`, `seam_catalog_revision`, `apply_fingerprint`, `participating_seams` |
| **SeamCatalogRevision** monotonic token | Opaque string compared before Stage 4 accept | Store as [String](https://docs.godotengine.org/en/stable/classes/class_string.html) or StringName; reject on `<` never allowed (catalog rollback forbidden silently per conceptual note) |
| **Replay equivalence** | Bit-exact compare of normalized bundle dicts under same revision | Deep compare of [Dictionary](https://docs.godotengine.org/en/stable/classes/class_dictionary.html) / [Array](https://docs.godotengine.org/en/stable/classes/class_array.html) trees after `canonicalize()` ordering pass |
| **BundleDiffSummary** | Tooling surface for seam/op/label drift | [Dictionary](https://docs.godotengine.org/en/stable/classes/class_dictionary.html) with arrays for `added_seams`, `removed_seams`, `op_changes`, `label_changes`; optional [Callable](https://docs.godotengine.org/en/stable/classes/class_callable.html) for pluggable diff strategies |

### Doc anchors (stable)

> Dictionaries preserve insertion order in Godot 4.x for deterministic iteration when keys are known. … StringName is optimized for comparisons.  
> — paraphrased from Godot class references: [Dictionary](https://docs.godotengine.org/en/stable/classes/class_dictionary.html), [StringName](https://docs.godotengine.org/en/stable/classes/class_stringname.html), [String](https://docs.godotengine.org/en/stable/classes/class_string.html).

## Identity + catalog gate (sketch)

```text
# Pseudocode shape — not a committed engine API
func bundle_identity_matches_replay(a: Dictionary, b: Dictionary) -> bool:
  if a.get("seam_catalog_revision", "") != b.get("seam_catalog_revision", ""):
    return false
  return canonicalize(a.get("apply_ops_ordered", [])) == canonicalize(b.get("apply_ops_ordered", [])) \
    and canonicalize(a.get("seam_records", [])) == canonicalize(b.get("seam_records", [])) \
    and a.get("validation_labels", {}) == b.get("validation_labels", {})

func diff_bundle(a: Dictionary, b: Dictionary) -> Dictionary:
  if a.get("seam_catalog_revision", "") != b.get("seam_catalog_revision", ""):
    return { "catalog_mismatch": true, "diff": {} }
  return structural_diff(a, b)  # seam-level / op-level / label-level
```

- **Catalog bump:** Stage 4 rejects bundles whose `seam_catalog_revision` lags the live catalog unless an explicit migration path exists (execution-deferred).
- **No new crypto here:** logical keys and ordering only; byte digests stay out of scope per conceptual **2.1.4**.

## Acceptance criteria (execution-first)

| ID | Criterion | Evidence | Status |
| --- | --- | --- | --- |
| AC-2.1.4-A | `BundleIdentity` fields always populated on staged bundle mint | Schema check + deny on missing revision | Planned |
| AC-2.1.4-B | Replay equivalence matcher wired to **2.1.3** `apply_ops_ordered` + seam records | Round-trip test vectors | Planned |
| AC-2.1.4-C | `diff_bundle` reports catalog mismatch vs structural drift separately | Golden diff fixtures | Planned |

## Explicit deferrals (D-Exec-rollup-deferral)

- **`GMM-2.4.5-*`**, HR closure, CI run IDs, registry hashes — **not** claimed closed here; rollup/CI IDs remain execution-deferred per project decision records and [[../../../decisions-log]].

## Related

- Prior tertiary **2.1.3**: [[Phase-2-1-3-Staged-Delta-Bundles-Merge-Seams-and-Apply-Ordering-Roadmap-2026-04-12-1832]]
- Parent secondary (spine): [[Phase-2-1-Pipeline-Stages-Seed-to-World-Roadmap-2026-04-12-1616]]
- Next conceptual sibling **2.1.5**: [[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-5-Replay-Ledger-Canonical-Diff-Surface-and-Restore-Cursor-Roadmap-2026-03-30-2310]] — execution cursor advances **`2.1.4` → `2.1.5`** for next deepen.
