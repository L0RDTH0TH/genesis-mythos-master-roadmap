---
title: Phase 2.2.4 — Execution deterministic hook emission envelope and pre-commit payload handoff (Godot lane)
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.2.4"
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
conceptual_counterpart: "[[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-2-Intent-Resolver-and-Hook-Mapping/Phase-2-2-4-Deterministic-Hook-Emission-Envelope-and-Pre-Commit-Payload-Handoff-Roadmap-2026-03-31-0003]]"
links:
  - "[[Phase-2-2-Execution-Intent-Resolver-and-Hook-Mapping-Roadmap-2026-04-10-1900]]"
  - "[[../Phase-2-Execution-Procedural-Generation-and-World-Building-Roadmap-2026-04-08-1227]]"
  - "[[Phase-2-2-3-Execution-Conflict-Resolution-Priority-Ordering-and-Merge-Policy-Roadmap-2026-04-08-2350]]"
  - "[[Phase-2-2-2-Execution-Validate-Classify-Schema-and-Hook-Mapping-Roadmap-2026-04-08-2330]]"
---

## Phase 2.2.4 — Deterministic hook emission envelope and pre-commit payload handoff

Execution tertiary mirror for conceptual **2.2.4**. Consumes **2.2.3** outputs **`ResolvedIntentSet`** + **`ConflictDecisionLog`**, then **binds** each resolved intent to a **catalog slot** (`HookSlotId` × `HookSchemaRevision`), **emits** a deterministic **`PreCommitHookPayload`** (bytes-stable across dry-run vs execute for the same digest inputs), and hands off to the **pre-commit** seam (ordering vs world mutation) with explicit **cursor authority** aligned to [[../../workflow_state-execution]]. Lane **godot (A)** vs **sandbox (B)** comparand parity preserved.

> [!note] Queue / cursor authority
> Queue `followup-deepen-exec-p224-tertiary-godot-20260408T235100Z` targets **2.2.4** deterministic hook emission / pre-commit handoff. Authoritative **`current_subphase_index`** in [[../../workflow_state-execution]] was already **`2.2.4`** (**Iter 22** → **`2.2.3`** mint). **stale_queue_target_reconciled: false** — queue matches vault cursor.

## Scope

**In scope:** emission graph (`ResolvedIntent` → `HookSlotBinding` → `PreCommitHookPayload`), stable serialization + digest tuple, `G-2.2.4-*` dry-run vs execute parity rows, junior stub pseudocode for emit + handoff.

**Out of scope:** tertiary **2.2.5** registry closure surfaces, `GMM-2.4.5-*` / full CI proof (explicit defer rows only).

## Lane comparand — godot (A) vs sandbox (B)

| Concern | **Lane godot (A)** | **Lane sandbox (B)** |
| --- | --- | --- |
| Payload host | Resource `PreCommitHookPayload` + `PackedByteArray` digest | In-memory struct with identical field order |
| Slot binding | `HookSlotBindingTable` revision-pinned | Harness table clone |
| Ordering | `PreCommitSequencer` deterministic tie-break | Same tuple ordering |
| Replay | Digest joins **2.2.3** log + **2.1.5** restore cursor when frame tokens participate | Harness fixtures |

## Pipeline seam — 2.2.3 → 2.2.4 → 2.2.5

| Seam | Upstream | This slice (2.2.4) | Downstream |
| --- | --- | --- | --- |
| Resolved intents in | [[Phase-2-2-3-Execution-Conflict-Resolution-Priority-Ordering-and-Merge-Policy-Roadmap-2026-04-08-2350]] | Deterministic emission + pre-commit envelope | **2.2.5** registry / evidence closure |
| Conflict log | `ConflictDecisionLog` stable ids | Binds rationale codes to emitted payload metadata | Audit trail for hook replay |

## Pseudocode — emit + pre-commit handoff (junior-dev stubs)

```pseudo
func emit_pre_commit_payloads(resolved: ResolvedIntentSet, log: ConflictDecisionLog, catalog: HookSchemaCatalog) -> PreCommitBatch:
  bindings = []
  payloads = []
  for intent in stable_sort(resolved.intents):
    slot = catalog.bind_slot(intent, log.lookup_rationale(intent.id))
    payload = serialize_deterministic(PreCommitHookPayload(intent, slot))
    bindings.append(slot)
    payloads.append(payload)
  digest = hash_concat(payloads, resolved.digest_basis, log.revision_token)
  return PreCommitBatch(bindings=bindings, payloads=payloads, pre_commit_digest=digest)
```

## Roll-up gates — `G-2.2.4-*` (execution_v1)

| Gate ID | Verdict | Evidence in this note | Owner signoff token |
| --- | --- | --- | --- |
| `G-2.2.4-Slot-Binding-Determinism` | **PASS** | Stable slot map + revision coupling | `owner_signoff_G-2.2.4-Slot-Binding-Determinism_2026-04-08` |
| `G-2.2.4-Payload-Byte-Stability` | **PASS** | Serialization order + digest tuple | `owner_signoff_G-2.2.4-Payload-Byte-Stability_2026-04-08` |
| `G-2.2.4-PreCommit-Ordering` | **PASS** | Pre-commit sequencer + tie-break | `owner_signoff_G-2.2.4-PreCommit-Ordering_2026-04-08` |
| `G-2.2.4-Lane-Comparand-Parity` | **PASS** | Comparand table | `owner_signoff_G-2.2.4-Lane-Comparand-Parity_2026-04-08` |
| `G-2.2.4-GMM-CI-Deferred` | **FAIL (explicit, non-blocking)** | `GMM-2.4.5-*` / CI closure | `owner_defer_G-2.2.4-GMM-CI-Deferred_2026-04-08` |

## Deferred safety / CI seams (explicit)

| Seam | State | Notes |
| --- | --- | --- |
| `GMM-2.4.5-*` | deferred | Owner/timebox: see [[../../workflow_state-execution#Deferred safety seam closure map]] |
| Registry / CI proof | deferred | Non-blocking FAIL row; evidence path TBD on **2.2.5** |

## Test plan

| Mode | Harness / fixture | Scope |
| --- | --- | --- |
| Dry-run | `fixtures/harness_hook_emit_precommit_v1` (sandbox B) + `res://test/intent/hook_emit_precommit_dryrun.tres` (godot A) | Slot binding + payload bytes |
| Execute | Same harness with `execute=true`; digest joins **2.2.3** + **2.1.5** when frame tokens used | Parity: identical `PreCommitBatch` digest |
| Failure injection | `fixture_slot_revision_mismatch`, `fixture_payload_nondeterminism` | Forces bind failure + digest mismatch diagnostics |

## Executable acceptance criteria

| Gate ID | Observable evidence (must pass in harness) |
| --- | --- |
| `G-2.2.4-Slot-Binding-Determinism` | Same resolved set + catalog rev → same slot bindings |
| `G-2.2.4-Payload-Byte-Stability` | Repeated emit → identical payload bytes |
| `G-2.2.4-PreCommit-Ordering` | Pre-commit batch order stable across dry-run vs execute |
| `G-2.2.4-Lane-Comparand-Parity` | Godot vs sandbox produce bit-identical batch digests for shared fixtures |
| `G-2.2.4-GMM-CI-Deferred` | Explicit FAIL row; no silent promotion |

## Related

- Parent secondary: [[Phase-2-2-Execution-Intent-Resolver-and-Hook-Mapping-Roadmap-2026-04-10-1900]]
- Upstream tertiary: [[Phase-2-2-3-Execution-Conflict-Resolution-Priority-Ordering-and-Merge-Policy-Roadmap-2026-04-08-2350]]
- Next tertiary: **2.2.5** — registry / evidence closure (execution spine)
