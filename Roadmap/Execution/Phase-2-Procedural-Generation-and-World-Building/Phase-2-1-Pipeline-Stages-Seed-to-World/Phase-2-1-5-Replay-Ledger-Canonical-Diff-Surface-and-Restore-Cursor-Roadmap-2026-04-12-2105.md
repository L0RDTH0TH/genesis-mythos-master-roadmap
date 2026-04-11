---
title: Phase 2.1.5 (Execution) — Replay ledger, canonical diff surface, restore cursor
created: 2026-04-12
tags:
  - roadmap
  - execution
  - godot
project-id: godot-genesis-mythos-master
roadmap_track: execution
phase: 2
subphase: "2.1.5"
roadmap-level: tertiary
status: in-progress
handoff_readiness: 86
handoff_gaps:
  - "Rollup / registry / CI proof rows remain execution-deferred per D-Exec-rollup-deferral."
handoff_audit_last: "2026-04-12T21:05:00Z"
conceptual_counterpart: "[[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-5-Replay-Ledger-Canonical-Diff-Surface-and-Restore-Cursor-Roadmap-2026-03-30-2310]]"
---

# Phase 2.1.5 (Execution) — Replay ledger, canonical diff surface, restore cursor

Execution remint for **Phase 2 tertiary 2.1.5** on the parallel spine. Binds conceptual NL from [[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-5-Replay-Ledger-Canonical-Diff-Surface-and-Restore-Cursor-Roadmap-2026-03-30-2310]] (replay ledger entry shape, canonical diff surface, restore cursor after validation stop) to Godot-shaped carriers consistent with [[Phase-2-1-4-Bundle-Identity-Seam-Catalog-Stability-and-Replay-Diff-Roadmap-2026-04-12-2005]] and [[Phase-2-1-Pipeline-Stages-Seed-to-World-Roadmap-2026-04-12-1616]].

## Intent mapping (execution)

| Conceptual contract | Execution mechanism | Godot metaphor |
| --- | --- | --- |
| **ReplayLedgerEntry** | Serializable record per staged attempt | [Dictionary](https://docs.godotengine.org/en/stable/classes/class_dictionary.html) with [StringName](https://docs.godotengine.org/en/stable/classes/class_stringname.html) keys: `bundle_identity`, `seam_catalog_revision`, `validation_labels`, `resume_cursor`, `stage_window`, `timestamp_logical` |
| **ResumeCursor** | Deterministic resume pointer after dry-run fail | Nested [Dictionary](https://docs.godotengine.org/en/stable/classes/class_dictionary.html): `resume_from_seam`, `resume_from_apply_ordinal`, `requires_catalog_migration` ([bool](https://docs.godotengine.org/en/stable/classes/class_bool.html)) |
| **CanonicalDiffSurface** | Tool-facing diff product (schema-level) | [Dictionary](https://docs.godotengine.org/en/stable/classes/class_dictionary.html) with [Array](https://docs.godotengine.org/en/stable/classes/class_array.html) slots for seam/op/label deltas + `cursor_delta`; optional [Callable](https://docs.godotengine.org/en/stable/classes/class_callable.html) for pluggable diff strategies |
| **Restore vs commit** | Cursor state machine | [String](https://docs.godotengine.org/en/stable/classes/class_string.html) or StringName enum-like tokens: `commit_ready` \| `restore_required` aligned to Stage 4/5 boundary from spine |

### Doc anchors (stable)

> Dictionaries preserve insertion order in Godot 4.x for deterministic iteration when keys are known.  
> — [Dictionary](https://docs.godotengine.org/en/stable/classes/class_dictionary.html)

## Ledger + diff + restore (sketch)

```text
# Pseudocode shape — not a committed engine API
func build_replay_ledger(bundle: Dictionary, validation_result: Dictionary) -> Dictionary:
  var cursor := derive_resume_cursor(bundle, validation_result)
  return {
    "bundle_identity": bundle.get("identity", {}),
    "seam_catalog_revision": bundle.get("seam_catalog_revision", ""),
    "validation_labels": validation_result.get("labels", {}),
    "resume_cursor": cursor,
    "stage_window": validation_result.get("stage_window", {}),
    "timestamp_logical": validation_result.get("timestamp_logical", 0),
  }

func canonical_diff_surface(a: Dictionary, b: Dictionary) -> Dictionary:
  return {
    "seam_delta": seam_delta(a, b),
    "op_delta": op_delta(a, b),
    "label_delta": label_delta(a, b),
    "cursor_delta": cursor_delta(a.get("resume_cursor", {}), b.get("resume_cursor", {})),
  }

func derive_resume_cursor(bundle: Dictionary, validation_result: Dictionary) -> Dictionary:
  if validation_result.get("passed", false):
    return { "state": "commit_ready", "boundary": validation_result.get("stage5_boundary_token", "") }
  return {
    "state": "restore_required",
    "resume_from_seam": validation_result.get("last_trusted_seam", ""),
    "resume_from_apply_ordinal": validation_result.get("last_trusted_apply_ordinal", -1),
    "requires_catalog_migration": validation_result.get("catalog_migration_required", false),
  }
```

- **Catalog mismatch on restore:** reject resume when `requires_catalog_migration` is true unless migration policy maps seams (execution-deferred runbook).
- **No persistent store:** ledger remains logical schema + in-memory shapes; file I/O / encryption out of scope per conceptual **2.1.5**.

## Acceptance criteria (execution-first)

| ID | Criterion | Evidence | Status |
| --- | --- | --- | --- |
| AC-2.1.5-A | Every Stage 4 attempt emits one **ReplayLedgerEntry**-shaped dict with identity + revision + labels + cursor | Schema check on minted bundle + validation outcome | Planned |
| AC-2.1.5-B | **canonical_diff_surface** separates catalog mismatch from seam/op/label drift | Golden diff vectors vs **2.1.4** `diff_bundle` | Planned |
| AC-2.1.5-C | Restore cursor rejects stale validation labels (fail-closed) | Label map compare before resume | Planned |

## Explicit deferrals (D-Exec-rollup-deferral)

- **`GMM-2.4.5-*`**, HR closure, CI run IDs, registry hashes — **not** claimed closed here; rollup/CI IDs remain execution-deferred per [[../../../decisions-log]].

## Related

- Prior tertiary **2.1.4**: [[Phase-2-1-4-Bundle-Identity-Seam-Catalog-Stability-and-Replay-Diff-Roadmap-2026-04-12-2005]]
- Parent secondary (spine): [[Phase-2-1-Pipeline-Stages-Seed-to-World-Roadmap-2026-04-12-1616]]
- **2.1** slice structurally complete on execution spine after this mint; next structural target: **Phase 2 secondary 2.2** — [[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-2-Intent-Resolver-and-Hook-Mapping/Phase-2-2-Intent-Resolver-and-Hook-Mapping-Roadmap-2026-03-30-2310]] (parallel-spine execution deepen).
