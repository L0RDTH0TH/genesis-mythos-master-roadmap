---
title: Phase 2.2.1 (Execution) — Intent envelope normalization and identity binding
created: 2026-04-12
tags:
  - roadmap
  - execution
  - sandbox
  - procedural-generation
  - phase-2-2-1
project-id: sandbox-genesis-mythos-master
roadmap_track: execution
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.2.1"
status: in-progress
handoff_readiness: 72
handoff_readiness_basis: "structural_scaffold_ac_planned"
priority: high
progress: 35
conceptual_counterpart: "[[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-2-Intent-Resolver-and-Hook-Mapping/Phase-2-2-1-Intent-Envelope-Normalization-and-Identity-Binding-Roadmap-2026-03-30-2338]]"
para-type: Project
links:
  - "[[Phase-2-2-Intent-Resolver-and-Hook-Mapping-Roadmap-2026-04-11-2335]]"
---

# Phase 2.2.1 (Execution) — Intent envelope normalization and identity binding

Execution tertiary **2.2.1** on the parallel spine under `Phase-2-2-Intent-Resolver-and-Hook-Mapping/`, mirroring conceptual **2.2.1** ([[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-2-Intent-Resolver-and-Hook-Mapping/Phase-2-2-1-Intent-Envelope-Normalization-and-Identity-Binding-Roadmap-2026-03-30-2338]]). Binds parent secondary **2.2** ([[Phase-2-2-Intent-Resolver-and-Hook-Mapping-Roadmap-2026-04-11-2335]]) to the **first resolver stage**: canonical **intent envelopes** + stable **identity binding** before classify / merge / emit. **Text-only** interface seams this pass; **sandbox_code_precision** (verbatim C++ + allowlisted Research) deferred unless evidenced.

Upstream: replay / diff / restore semantics from **2.1.5** ([[../Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-5-Replay-Ledger-Canonical-Diff-Surface-and-Restore-Cursor-Roadmap-2026-04-11-0625]]) — normalized envelopes must carry **joinable** snapshot metadata for ledger rows and restore cursor without smuggling nondeterministic fields into replay compares.

## Scope (execution)

**In scope:**

- **Normalization queue** per pipeline frame: ingest raw intent records → canonical **`CanonicalIntentEnvelope`** shape (required fields, optional blocks, **`normalizationRevision`**).
- **Actor binding**: stable **`ActorBinding`** + logical **`IntentRecordId`** keys aligned to DM / player / system surfaces (no silent guess that changes replay).
- **Dedupe / fold** policy hooks: window + idempotency rules as **deterministic** inputs to downstream merge policy (**2.2.3**).
- **Emit** handoff to **validate / classify** (**2.2.2**) — never skip validation on “fast paths.”

**Out of scope:**

- Verbatim C++ / stdlib quotes (**sandbox_code_precision** — future slice with nested Research under sandbox allowlist).
- Full hook taxonomy, merge policy precedence tables, or emit-stage payload shapes (**2.2.2+**).
- **GMM-2.4.5** / registry–CI closure (execution-deferred unless evidenced).

## Behavior (execution contract)

Ordering (within this slice):

1. **Ingest** `RawIntentRecord` batches into a per-frame **normalization queue** (single writer discipline; deterministic ordering rules for ties).
2. **Normalize** to **`CanonicalIntentEnvelope`**: defaults, enum coercion, attach **resolver metadata** (hints only — not final precedence).
3. **Bind identity**: allocate stable **`IntentRecordId`** + **`ActorBinding`**; reject or diagnostic-only when identity cannot be bound per policy.
4. **Dedupe / fold** within **`NormalizationPolicy.dedupeWindow`**: merge or reject duplicates per **`IntentRecordId` + targetScope** rules.
5. **Emit** normalized envelopes to **validation / classify** (**2.2.2**) with **no** skip of validation.

Determinism: same raw bytes + same normalization config + same **frameId** ⇒ same normalized set (including tie ordering).

## Interfaces (text — depth-3 tertiary)

- **`RawIntentRecord`:** `{ surface, payload, optionalActorHint, clientVersion }`
- **`CanonicalIntentEnvelope`:** `{ intentRecordId, actorBinding, channelId, frameId, targetScope, payloadNormalized, normalizationRevision }`
- **`NormalizationPolicy`:** `{ dedupeWindow, idempotencyRules, defaultActorResolution }`

## Edge cases (execution)

- **Missing actor hint:** policy default or invalid diagnostic — no silent guess affecting replay.
- **Client version skew:** incompatible payloads tagged for explicit defer/reject via **`normalizationRevision`**.
- **Conflicting duplicates** in-frame: **last-writer vs merge** must be **policy-defined** (referenced from **2.2.3** merge classes — not ad hoc here).

## Pseudocode readiness (text — no verbatim C++)

```text
seam normalize_intent_envelopes(raw_batch, policy, frame_id, mode):
  queue = stable_sort(raw_batch, policy.tie_break)
  out = []
  for r in queue:
    env = normalize_one(r, policy, frame_id)
    if not env.ok:
      out.append(diagnostic_only(env))
      continue
    bound = bind_identity(env, policy)
    folded = dedupe_or_fold(bound, policy, out)
    out.append(folded)
  return emit_to_classify(out, require_validation=true)
```

## Acceptance criteria (execution-first)

| ID | Criterion | Evidence target | Status |
| --- | --- | --- | --- |
| AC-2.2.1.E1 | Same raw + policy + frame ⇒ same normalized envelope set | `normalization_digest` (stub: ## Pseudocode readiness seam `normalize_intent_envelopes`) | Scaffolded |
| AC-2.2.1.E2 | Invalid identity / actor ⇒ diagnostic or reject — no silent mutation | `mutation_blocked=true` | Planned |
| AC-2.2.1.E3 | Dedupe/fold rules are policy-bound and deterministic | `dedupe_trace_id` | Planned |
| AC-2.2.1.E4 | Emitted envelopes join **2.1.5** ledger + restore cursor metadata | `intent_snapshot_id` | Planned |

## Intent Mapping

| Conceptual intent | Execution seam | Notes |
| --- | --- | --- |
| Canonical envelope shape | `CanonicalIntentEnvelope` + revision tagging | Aligns conceptual NL § Interfaces |
| Identity binding | `IntentRecordId` + `ActorBinding` | Ties to **2.1.x** staged snapshots |
| Dedupe window | `NormalizationPolicy` | Deterministic fold — feeds **2.2.3** |
| Replay safety | Strip / tag nondeterministic fields before ledger compare | Upstream **2.1.5** |

## Related

- Parent secondary **[[Phase-2-2-Intent-Resolver-and-Hook-Mapping-Roadmap-2026-04-11-2335]]**
- Next tertiary **2.2.2** (validate / classify / schema — not minted this run)
- Upstream **2.1.5** [[../Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-5-Replay-Ledger-Canonical-Diff-Surface-and-Restore-Cursor-Roadmap-2026-04-11-0625]]

## Research integration

> [!note] External grounding
> No nested **`Task(research)`** this run; **sandbox_code_precision** citations deferred. Design intent aligned to conceptual **2.2.1**; no non-allowlisted URLs introduced in this note.
