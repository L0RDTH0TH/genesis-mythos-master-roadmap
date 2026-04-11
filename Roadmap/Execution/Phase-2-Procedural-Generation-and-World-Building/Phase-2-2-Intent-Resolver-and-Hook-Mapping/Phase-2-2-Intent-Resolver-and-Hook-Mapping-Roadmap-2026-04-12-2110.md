---
title: Phase 2.2 (Execution) — Intent Resolver and Hook Mapping
created: 2026-04-12
tags:
  - roadmap
  - execution
  - godot
  - sandbox-comparand
project-id: godot-genesis-mythos-master
roadmap_track: execution
phase: 2
subphase: "2.2"
roadmap-level: secondary
status: in-progress
handoff_readiness: 86
handoff_gaps:
  - "Rollup / registry / CI / HR-style proof rows (`missing_roll_up_gates`, `GMM-2.4.5-*`) remain execution-deferred per D-Exec-rollup-deferral — no fabricated `ci_run_id` or closed rollup verdicts in this mint."
handoff_audit_last: "2026-04-12T21:10:00Z"
conceptual_counterpart: "[[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-2-Intent-Resolver-and-Hook-Mapping/Phase-2-2-Intent-Resolver-and-Hook-Mapping-Roadmap-2026-03-30-2310]]"
---

# Phase 2.2 (Execution) — Intent resolver and hook mapping

Execution remint for **Phase 2 secondary 2.2** on the parallel spine. Mirrors conceptual NL scope from [[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-2-Intent-Resolver-and-Hook-Mapping/Phase-2-2-Intent-Resolver-and-Hook-Mapping-Roadmap-2026-03-30-2310]]; binds **normalize → classify → resolve conflicts → emit hook payloads** to `IIntentResolver` + frozen **hook namespace table** consumed by [[../Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-Pipeline-Stages-Seed-to-World-Roadmap-2026-04-12-1616]] stage spine and [[../Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-04-12-1515|Phase 2 execution primary]].

## Intent mapping

| Intent target | Inspiration anchors | Execution mechanism | Validation signal |
| --- | --- | --- | --- |
| Canonical intent envelope (actor, scope, metadata) | Conceptual **Behavior** + **Ordering** | `IIntentResolver.resolve(intents, hook_table)` → frozen `Dictionary` keyed by **StringName** | Resolver decision log + collision matrix |
| Hook namespace stability | Conceptual **hook namespaces** + typed envelopes | Hook table as **StringName** → payload outline; no silent mutation | Diff of hook keys across replay |
| Conflict classes (replace / merge / defer / reject) | Conceptual **conflict** rows | Deterministic ordering + explicit branch outcomes | `ConflictDecisionLog` stub (tertiary **2.2.3** refines) |
| Godot vs Sandbox parity | Dual-lane policy | **Dictionary** / **Callable** metaphors (A) vs C++ maps + ordered dispatch (B) | Hostile validator + **D-Exec-rollup-deferral** |

## Scope

- Define execution-facing **resolver pass** that sits **after** seed expansion and **before** body stages: consumes normalized intents + current hook table snapshot; produces **frozen hook bindings** for one pipeline run.
- Specify **fail-closed** behavior for unknown intents (diagnostics only; no world mutation) aligned to conceptual **Edge cases**.
- Keep **registry / CI / rollup / HR** closure **explicitly open**; do not claim `missing_roll_up_gates` closed.

## Resolver seam (execution binding)

| Step | Role | Reads | Produces |
| --- | --- | --- | --- |
| Normalize | Shape + identity | Raw intent envelope stream | Normalized intent list |
| Classify | Schema gate | Allowed hook catalog revision | Classified intents + rejects |
| Resolve | Priority + conflicts | Classified intents + policy snapshot | Single winner / merge / defer decision per hook key |
| Emit | Handoff to pipeline | Resolution outcomes | Frozen hook table + diagnostics |

Upstream **hook table** seed may be empty at first resolve; downstream stages read **only** the frozen table emitted here for the active run.

## Runner sketch (non-authoritative; text only)

```text
function resolve_intents_for_run(raw_intents, hook_catalog, policy):
  normalized = normalize_envelopes(raw_intents)
  classified = classify_against_schema(normalized, hook_catalog)
  decisions = apply_conflict_policy(classified, policy)
  frozen_hook_table = emit_hook_table(decisions)
  return ResolverResult(hooks=frozen_hook_table, diagnostics=collect_diagnostics(decisions))
```

## Godot stable citations (lane A)

Use only allowlisted stable-doc prefixes. These ground **resolver map / keying** metaphors without claiming closed CI IDs:

- Associative container for **StringName**-keyed hook table — [Dictionary](https://docs.godotengine.org/en/stable/classes/class_dictionary.html) (`get`, `has`, `merge`, `keys`).
- Symbolic hook keys — [StringName](https://docs.godotengine.org/en/stable/classes/class_stringname.html) (interned names; cheap compare for resolver hot path).
- Indirect dispatch for policy hooks / staged listeners — [Callable](https://docs.godotengine.org/en/stable/classes/class_callable.html) (`bind`, `call`, `is_valid`).
- Optional: ordered iteration for deterministic conflict tie-break — [Array](https://docs.godotengine.org/en/stable/classes/class_array.html) (`sort_custom` pattern documented; policy defines comparator).

## Acceptance criteria (execution-first)

| ID | Criterion | Evidence target | Status |
| --- | --- | --- | --- |
| AC-2.2-A | Same inputs + same policy snapshot ⇒ same frozen hook table | Hash-stable hook table + diagnostics | Planned |
| AC-2.2-B | Unknown / invalid intents never mutate staged world; surface as diagnostics | Reject/defer trace | Planned |
| AC-2.2-C | Conflict outcomes are total (no silent merge) | Collision matrix row coverage | Planned |
| AC-2.2-D | Replay uses intent snapshot + catalog revision; outputs match | Replay diff empty on golden case | Planned |

## Lane comparand rows

| Row | Lane A (Godot) | Lane B (Sandbox) | Common contract |
| --- | --- | --- | --- |
| Keyed map | Dictionary + StringName keys | `unordered_map` + interned keys | Stable key compare |
| Dispatch | Callable policy hooks | `std::function` / vtable | Deterministic ordering |
| Diagnostics | push_error / structured log seam | Typed error channel | Fail-closed surfacing |

## Explicit deferrals (D-Exec-rollup-deferral)

- **`GMM-2.4.5-*`**, manifest-hash CI, registry IDs, and rollup **HR** closures remain **open** — **do not** fabricate IDs in this note.
- **Tertiary 2.2.x** notes refine taxonomy, merge envelopes, and replay contracts; this secondary defines resolver seam + hook-table contract only.

## Related

- Phase 2 execution primary (interfaces): [[../Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-04-12-1515]]
- Phase 2.1 execution secondary (stage spine feeding resolver): [[../Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-Pipeline-Stages-Seed-to-World-Roadmap-2026-04-12-1616]]
- Conceptual Phase 2.2 (design authority): [[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-2-Intent-Resolver-and-Hook-Mapping/Phase-2-2-Intent-Resolver-and-Hook-Mapping-Roadmap-2026-03-30-2310]]
- Tertiary **2.2.1** minted — [[Phase-2-2-1-Intent-Envelope-Normalization-and-Identity-Binding-Roadmap-2026-04-12-2115]]; next structural target: **2.2.2** (validate/classify schema per conceptual tree).
