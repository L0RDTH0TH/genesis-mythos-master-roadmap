---
title: Phase 2.2 (Execution) — Intent Resolver and Hook Mapping
created: 2026-04-11
tags:
  - roadmap
  - execution
  - sandbox
  - procedural-generation
  - phase-2-2
project-id: sandbox-genesis-mythos-master
roadmap_track: execution
roadmap-level: secondary
phase-number: 2
subphase-index: "2.2"
status: in-progress
handoff_readiness: 85
conceptual_counterpart: "[[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-2-Intent-Resolver-and-Hook-Mapping/Phase-2-2-Intent-Resolver-and-Hook-Mapping-Roadmap-2026-03-30-2310]]"
---

# Phase 2.2 (Execution) — Intent resolver and hook mapping

Execution secondary **2.2** on the parallel spine under `Phase-2-Procedural-Generation-and-World-Building/Phase-2-2-Intent-Resolver-and-Hook-Mapping/`, mirroring the conceptual tree. Binds Phase **2** execution primary ([[../Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-04-11-1432]]) to upstream Phase **2.1** seed-to-world spine — including **replay ledger**, **canonical diff surface**, and **restore cursor** contracts from tertiary **2.1.5** ([[../Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-5-Replay-Ledger-Canonical-Diff-Surface-and-Restore-Cursor-Roadmap-2026-04-11-0625]]) as the authoritative upstream closure for deterministic intent snapshots and audit trails (text-only seams this pass).

Conceptual authority: [[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-2-Intent-Resolver-and-Hook-Mapping/Phase-2-2-Intent-Resolver-and-Hook-Mapping-Roadmap-2026-03-30-2310]]

## Scope (execution)

- **Intent envelope normalization** and **identity binding** inputs that feed resolver ordering (aligns conceptual **2.2.1**).
- **Validate / classify / schema** and **hook mapping** surfaces that consume normalized envelopes (aligns conceptual **2.2.2**).
- **Conflict resolution**, **priority ordering**, and **merge policy** inputs for replace / merge / defer / reject classes (aligns conceptual **2.2.3**).
- **Deterministic hook emission**, **pre-commit payload handoff**, and **envelope validation labels** as execution-facing seams — **text-only** this pass; **sandbox_code_precision** (verbatim C++ / allowlisted Research citations) deferred to tertiary **2.2.x** mints unless evidenced.

**Explicitly deferred:** **GMM-2.4.5** / registry–CI / compare-table closure rows remain **execution-deferred** unless a later slice evidences them (per queue guidance).

## Upstream alignment (2.1 → 2.2)

| Upstream (2.1.x) | Carried constraint for 2.2 |
| --- | --- |
| **Replay ledger** + **canonical diff** + **restore cursor** (2.1.5) | Intent + hook snapshots must remain **replay-safe** and **diff-auditable** relative to staged pipeline state; resolver outcomes must not bypass ledger/diff/restore semantics. |
| Staged delta bundles + merge seams (2.1.3) | Resolver outputs feed **merge policy inputs** deterministically (digest-stable). |
| Bundle identity + seam catalog (2.1.4) | Hook namespaces must avoid collisions with **bundle identity** and **seam catalog** revision rules. |

## Resolver spine (execution contract — text)

| Stage | Role | Failure / empty-output semantics |
| --- | --- | --- |
| Ingest | Accept DM / player / system intents into canonical envelope | Invalid shape → diagnostic; no world mutation |
| Normalize | Bind identity + scope; strip nondeterministic fields for replay compare | Typed empty envelope when rejected |
| Classify | Map to hook schema + merge policy class | Unknown class → defer/reject path |
| Resolve | Apply priority + conflict rules | Deterministic ordering; diagnostics on conflict |
| Emit | Produce stable hook payloads + replay snapshot metadata | Same seed + intents + config → same outputs |

## Pseudocode seams (text — depth-2 secondary)

```text
seam resolve_intent_hooks(intent_envelopes, resolver_config, staged_context, mode):
  normalized = []
  for env in intent_envelopes:
    n = normalize_envelope(env, staged_context)
    if not n.ok:
      normalized.append(diagnostic_only(n))
      continue
    normalized.append(classify_and_bind(n, resolver_config))
  merged = apply_merge_policy(normalized, resolver_config.priority_table)
  hooks = emit_hook_payloads(merged, resolver_config.hook_schema)
  if mode == replay_compare:
    return hooks_with_snapshot_metadata(hooks, staged_context.cursor)
  return hooks
```

## Acceptance criteria (execution-first)

| ID | Criterion | Evidence target | Status |
| --- | --- | --- | --- |
| AC-2.2.E1 | Resolver ordering is stable for identical envelopes + config | `resolver_order_digest` | Planned |
| AC-2.2.E2 | Invalid / unknown intents never mutate staged state directly | `mutation_blocked=true` on reject path | Planned |
| AC-2.2.E3 | Hook payloads are schema-bound; collisions are explicit diagnostics | `hook_emit_diagnostics` | Planned |
| AC-2.2.E4 | Replay snapshot metadata aligns with **2.1.5** ledger + restore cursor | `intent_snapshot_id` joinable to ledger row | Planned |

## Intent Mapping

| Design intent target | Inspiration anchors | Execution mechanism | Validation signal |
| --- | --- | --- | --- |
| Deterministic resolver | Conceptual 2.2 ordering + Phase 2 primary `IIntentResolver` | `resolve_intent_hooks` + stage table | AC-2.2.E1 digest |
| Safe failure | 2.1 dry-run / commit boundary story | Normalize/classify rejects → diagnostics only | AC-2.2.E2 |
| Replay + audit | 2.1.5 replay ledger / diff / restore cursor | `replay_compare` branch + snapshot metadata | AC-2.2.E4 |
| Merge policy inputs | 2.1.3 staged deltas | `apply_merge_policy` inputs from classified envelopes | AC-2.2.E3 |

## Lane comparand

| Concern | Sandbox (this lane) | Godot (reference) | Shared contract |
| --- | --- | --- | --- |
| Resolver | C++-oriented seams | Signal / binding analog | Deterministic digest |
| Hook emit | Typed payload tables | Callable / signal payloads | Schema-bound emit |
| Replay | Ledger + cursor join | Scene state snapshot analog | Same-input same-output |

## Related

- Phase 2 execution primary: [[../Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-04-11-1432]]
- Upstream secondary **2.1**: [[../Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-Pipeline-Stages-Seed-to-World-Roadmap-2026-04-11-2359]]
- Upstream tertiary **2.1.5** (replay / diff / restore): [[../Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-5-Replay-Ledger-Canonical-Diff-Surface-and-Restore-Cursor-Roadmap-2026-04-11-0625]]
- Execution tertiary **2.2.1** (minted): [[./Phase-2-2-1-Intent-Envelope-Normalization-and-Identity-Binding-Roadmap-2026-04-12-2208]] — conceptual peer [[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-2-Intent-Resolver-and-Hook-Mapping/Phase-2-2-1-Intent-Envelope-Normalization-and-Identity-Binding-Roadmap-2026-03-30-2338]].
- **Next structural target:** tertiary **2.2.2** (validate / classify / schema) — per [[../../workflow_state-execution]] **`current_subphase_index: "2.2.2"`** (authoritative execution cursor).
