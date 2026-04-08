---
title: Phase 2.2 — Execution intent resolver and hook mapping (Godot lane)
roadmap-level: secondary
phase-number: 2
subphase-index: "2.2"
project-id: godot-genesis-mythos-master
roadmap_track: execution
status: in-progress
priority: high
progress: 40
handoff_readiness: 85
handoff_gaps:
  - "Tertiary execution mirrors 2.2.3–2.2.5 not yet minted on parallel spine (2.2.1–2.2.2 on disk)."
created: 2026-04-10
tags:
  - roadmap
  - execution
  - godot-genesis-mythos-master
  - phase-2
para-type: Project
conceptual_counterpart: "[[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-2-Intent-Resolver-and-Hook-Mapping/Phase-2-2-Intent-Resolver-and-Hook-Mapping-Roadmap-2026-03-30-2310]]"
links:
  - "[[../Phase-2-Execution-Procedural-Generation-and-World-Building-Roadmap-2026-04-08-1227]]"
  - "[[../Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-Execution-Pipeline-Stages-Seed-to-World-Roadmap-2026-04-08-1805]]"
  - "[[Phase-2-2-1-Execution-Intent-Envelope-Normalization-and-Identity-Binding-Roadmap-2026-04-08-2315]]"
  - "[[Phase-2-2-2-Execution-Validate-Classify-Schema-and-Hook-Mapping-Roadmap-2026-04-08-2330]]"
---

## Phase 2.2 — Execution intent resolver and hook mapping (parallel spine)

Execution mirror for conceptual **2.2** under `Execution/Phase-2-Procedural-Generation-and-World-Building/Phase-2-2-Intent-Resolver-and-Hook-Mapping/` (no flat Execution-root heap). This slice binds **intent envelope normalization → classify/validate → conflict resolution → deterministic hook emission** with explicit `G-2.2-*` rows, lane **godot (A) vs sandbox (B)** comparands, and **pipeline seams** from Phase **2.1** **S1 — Intent resolve** into resolver stages.

> [!note] Queue reconcile
> Queue `followup-deepen-exec-p21-mint-godot-20260410T180500Z` requested a **secondary 2.1** mint; **2.1** was already on disk — authoritative pre-read cursor was **`2.2`** after **2.1.5** closure (**Iter 18** [[../../workflow_state-execution]]). This run mints **secondary 2.2** per resolver-forward policy.

## Scope

**In scope:** resolver stage ordering, hook namespace and schema catalog hooks, conflict classes (replace / merge / defer / reject), replay-safe intent snapshots, junior-dev stub pseudocode at seams.

**Out of scope:** full tertiary chain **2.2.1–2.2.5**, CI/registry proof bundles, `GMM-2.4.5-*` closure (explicit defer rows only).

## Lane comparand — godot (A) vs sandbox (B)

| Concern | **Lane godot (A)** | **Lane sandbox (B)** |
| --- | --- | --- |
| Resolver host | Resource-backed `IntentResolver` + stable catalog revision | In-memory harness with identical API |
| Schema catalog | `HookSchemaCatalog` revision pinned per session | Same revision namespace; synthetic fixtures |
| Conflict policy | Priority table + explicit merge policy token | Same policy table; diff-only diagnostics |
| Replay | `IntentReplaySnapshot` + digest rows | Harness-local snapshot with same digest inputs |

## Pipeline seam — seed→world (2.1) → intent→hooks (2.2)

| Seam | Upstream (Phase 2.1) | This slice (2.2) | Contract |
| --- | --- | --- | --- |
| Post–**S1** | `ResolvedHookBatch` from [[../Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-Execution-Pipeline-Stages-Seed-to-World-Roadmap-2026-04-08-1805]] | Normalized `IntentEnvelope` + classified hooks | IDs stable across dry-run vs execute |
| Pre–**S2** | Staged world evaluation | Deterministic hook payloads only after resolver PASS | No hidden world mutation on reject/defer |

## Pseudocode — resolver spine (junior-dev stubs)

```pseudo
func resolve_intents(envelopes: IntentEnvelope[], catalog_rev: CatalogRevision) -> ResolverResult:
  normalized = normalize(envelopes)           // identity + shape
  classified = classify(normalized, catalog_rev)
  conflicts = detect_conflicts(classified)
  resolved = apply_merge_policy(conflicts)   // replace|merge|defer|reject
  hooks = emit_hooks(resolved)
  return ResolverResult(hooks, diagnostics=replay_diagnostics(resolved))
```

## Roll-up gates — `G-2.2-*` (execution_v1)

| Gate ID | Verdict | Evidence in this note | Owner signoff token |
| --- | --- | --- | --- |
| `G-2.2-Resolver-Ordering` | **PASS** | Pseudocode + seam table S1→S2 | `owner_signoff_G-2.2-Resolver-Ordering_2026-04-10` |
| `G-2.2-Hook-Schema-Binding` | **PASS** | Lane A/B + catalog revision semantics | `owner_signoff_G-2.2-Hook-Schema-Binding_2026-04-10` |
| `G-2.2-Conflict-Policy` | **PASS** | Conflict classes + merge policy row | `owner_signoff_G-2.2-Conflict-Policy_2026-04-10` |
| `G-2.2-Lane-Comparand-Parity` | **PASS** | Comparand table | `owner_signoff_G-2.2-Lane-Comparand-Parity_2026-04-10` |
| `G-2.2-Tertiary-Chain-Deferred` | **FAIL (explicit, non-blocking)** | **2.2.1** minted [[Phase-2-2-1-Execution-Intent-Envelope-Normalization-and-Identity-Binding-Roadmap-2026-04-08-2315]]; **2.2.2–2.2.5** pending | `owner_defer_G-2.2-Tertiary-Chain-Deferred_2026-04-10` |

## Deferred safety / CI seams (explicit owner + timebox)

| Seam | State | Owner path | Review checkpoint |
| --- | --- | --- | --- |
| `GMM-2.4.5-*` | open (execution-deferred) | Bind after registry compare table in lane CI bundle | `2026-05-06` |
| `CI-deferrals` | open (execution-deferred) | Proof bundle under Phase 2 execution primary gate map | `2026-05-13` |

## Acceptance criteria

1. **AC-2.2-1:** Mirrored path matches conceptual subtree `Phase-2-2-Intent-Resolver-and-Hook-Mapping/` (parallel spine).
2. **AC-2.2-2:** Every `G-2.2-*` row has PASS or explicit non-blocking FAIL + token.
3. **AC-2.2-3:** Intent seam from **2.1** **S1** is named and traceable in the seam table.
4. **AC-2.2-4:** Phase 2 primary receives a propagation stub row for `rollup_2_primary_from_2_2` when tertiaries close (future deepen).

## Related

- Upstream secondary **2.1**: [[../Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-Execution-Pipeline-Stages-Seed-to-World-Roadmap-2026-04-08-1805]]
- Execution primary: [[../Phase-2-Execution-Procedural-Generation-and-World-Building-Roadmap-2026-04-08-1227]]
- Conceptual authority: [[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-2-Intent-Resolver-and-Hook-Mapping/Phase-2-2-Intent-Resolver-and-Hook-Mapping-Roadmap-2026-03-30-2310]]
- Execution state: [[../../workflow_state-execution]]
