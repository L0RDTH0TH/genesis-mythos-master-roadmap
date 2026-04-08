---
title: Phase 2.2.1 — Execution intent envelope normalization and identity binding (Godot lane)
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.2.1"
project-id: godot-genesis-mythos-master
roadmap_track: execution
status: complete
priority: high
progress: 100
handoff_readiness: 86
handoff_gaps: []
created: 2026-04-08
tags:
  - roadmap
  - execution
  - godot-genesis-mythos-master
  - phase-2
para-type: Project
conceptual_counterpart: "[[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-2-Intent-Resolver-and-Hook-Mapping/Phase-2-2-1-Intent-Envelope-Normalization-and-Identity-Binding-Roadmap-2026-03-30-2338]]"
links:
  - "[[Phase-2-2-Execution-Intent-Resolver-and-Hook-Mapping-Roadmap-2026-04-10-1900]]"
  - "[[../Phase-2-Execution-Procedural-Generation-and-World-Building-Roadmap-2026-04-08-1227]]"
  - "[[../Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-Execution-Pipeline-Stages-Seed-to-World-Roadmap-2026-04-08-1805]]"
---

## Phase 2.2.1 — Execution intent envelope normalization and identity binding

Execution tertiary mirror for conceptual **2.2.1**. This slice is the **first resolver stage** on the parallel spine: heterogeneous inputs → **canonical `IntentEnvelope`** with stable **identity binding**, composing the **S1 — Intent resolve** seam from Phase **2.1** into concrete dry-run vs execute evidence rows (`G-2.2.1-*`). Lane **godot (A)** vs **sandbox (B)** comparand parity preserved.

> [!note] Queue reconcile
> Queue `followup-deepen-exec-p215-tertiary-godot-20260408T231500Z` cited **2.1.5** mint + parity gates; **2.1.5** is already on disk (**[[../Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-5-Execution-Replay-Ledger-Canonical-Diff-Surface-and-Restore-Cursor-Roadmap-2026-04-10-1830]]**) with `phase2_gate_validation_parity` / `phase2_gate_replay_traceability` **closed** in [[../../workflow_state-execution#Execution gate tracker]]. Authoritative pre-read cursor was **`2.2.1`** — this run mints **tertiary 2.2.1** (stale **2.1.5** target reconciled forward).

## Scope

**In scope:** canonical envelope fields, actor/channel/frame identity, normalization queue + dedupe policy hooks, determinism digest inputs for replay, junior stub pseudocode.

**Out of scope:** full classify/validate/merge envelopes (**2.2.2+**), CI/registry proof, `GMM-2.4.5-*` closure (explicit defer rows only).

## Lane comparand — godot (A) vs sandbox (B)

| Concern | **Lane godot (A)** | **Lane sandbox (B)** |
| --- | --- | --- |
| Normalization host | Resource `IntentNormalizationPipeline` + frame-scoped queue | In-memory queue with identical API |
| Identity binding | `IntentRecordId` + `ActorBinding` resources; session-stable when policy says so | Synthetic actors; same key namespace |
| Dedupe window | Policy-driven per `frameId` | Same policy table; harness clocks |
| Replay | Normalized envelope digest rows join **2.1.5** `ReplayLedgerEntry` | Harness ledger tuple; identical digest inputs |

## Canonical IntentEnvelope field table

Evidence for **`G-2.2.1-Envelope-Shape`** (PASS): enumerated canonical fields + **normalization revision** tag.

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `intentRecordId` | `IntentRecordId` (logical UUID) | yes | Stable across dry-run vs execute when raw bytes + policy match |
| `actorBinding` | `ActorBinding` | yes | Player vs DM vs system; optional party/role when policy allows |
| `channelId` | `ChannelId` | yes | Pipeline channel / adapter surface |
| `frameId` | `FrameId` | yes | Regen cycle / tick scope for ordering |
| `targetScope` | `TargetScope` | yes | World slice / entity set the intent applies to |
| `payloadNormalized` | `PayloadNormalized` | yes | Coerced payload after normalization rules |
| `normalizationRevision` | `int` | yes | Monotonic revision tag; incompatible clients defer/reject per policy |

**Revision tag:** `normalizationRevision` increments when normalization policy semver changes; echoed in digest rows for replay parity with [[../Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-5-Execution-Replay-Ledger-Canonical-Diff-Surface-and-Restore-Cursor-Roadmap-2026-04-10-1830]].

## Pipeline seam — 2.1 S1 → 2.2.1 normalization

| Seam | Upstream (Phase 2.1) | This slice (2.2.1) | Contract |
| --- | --- | --- | --- |
| Post–**S1** | `ResolvedHookBatch` / intent staging from [[../Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-Execution-Pipeline-Stages-Seed-to-World-Roadmap-2026-04-08-1805]] | Raw intents → **CanonicalIntentEnvelope** | Normalization revision + actor binding stable across dry-run vs execute |
| Pre–**2.2.2** | — | Emits envelopes to classify/validate stage | No skip of validation on “fast paths” |

## Pseudocode — normalization + identity (junior-dev stubs)

```pseudo
func normalize_intents(raw: RawIntentRecord[], policy: NormalizationPolicy, frame: FrameId) -> CanonicalIntentEnvelope[]:
  queue = ingest(raw, frame)
  out = []
  for r in queue:
    env = coerce_defaults(r, policy.normalizationRevision)
    env.intentRecordId = bind_identity(r, policy.defaultActorResolution)
    env.actorBinding = resolve_actor(r.optionalActorHint, policy)
    env.channelId, env.frameId = attach_channel_frame(r, frame)
    out.append(dedupe_fold(env, policy.dedupeWindow, out))
  return deterministic_sort(out, policy.tieBreak)
```

## Roll-up gates — `G-2.2.1-*` (execution_v1)

| Gate ID | Verdict | Evidence in this note | Owner signoff token |
| --- | --- | --- | --- |
| `G-2.2.1-Envelope-Shape` | **PASS** | Canonical field table + revision tag | `owner_signoff_G-2.2.1-Envelope-Shape_2026-04-08` |
| `G-2.2.1-Identity-Binding` | **PASS** | ActorBinding + IntentRecordId rows | `owner_signoff_G-2.2.1-Identity-Binding_2026-04-08` |
| `G-2.2.1-Dedupe-Policy` | **PASS** | Dedupe window + tie-break in pseudocode | `owner_signoff_G-2.2.1-Dedupe-Policy_2026-04-08` |
| `G-2.2.1-Lane-Comparand-Parity` | **PASS** | Comparand table | `owner_signoff_G-2.2.1-Lane-Comparand-Parity_2026-04-08` |
| `G-2.2.1-Registry-CI` | **FAIL (explicit, non-blocking)** | Registry/CI proof deferred | `owner_defer_G-2.2.1-Registry-CI_2026-04-08` |

## Deferred safety / CI seams (explicit)

| Seam | State | Notes |
| --- | --- | --- |
| `GMM-2.4.5-*` | open (execution-deferred) | Bind after lane CI bundle per [[../../workflow_state-execution#Deferred safety seam closure map]] |
| `CI-deferrals` | open (execution-deferred) | Proof promotion post–**1.2** rollup evidence |

## Acceptance criteria

1. **AC-2.2.1-1:** Mirrored path matches conceptual tertiary **2.2.1** under `Phase-2-2-Intent-Resolver-and-Hook-Mapping/` (parallel spine).
2. **AC-2.2.1-2:** `G-2.2.1-*` rows populated with PASS or explicit non-blocking FAIL + token.
3. **AC-2.2.1-3:** Seam table names **S1** upstream and routes to **2.2.2** explicitly.

## Related

- Parent secondary **2.2**: [[Phase-2-2-Execution-Intent-Resolver-and-Hook-Mapping-Roadmap-2026-04-10-1900]]
- Upstream **2.1.5** (replay/diff cursor): [[../Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-5-Execution-Replay-Ledger-Canonical-Diff-Surface-and-Restore-Cursor-Roadmap-2026-04-10-1830]]
- Execution state: [[../../workflow_state-execution]]
