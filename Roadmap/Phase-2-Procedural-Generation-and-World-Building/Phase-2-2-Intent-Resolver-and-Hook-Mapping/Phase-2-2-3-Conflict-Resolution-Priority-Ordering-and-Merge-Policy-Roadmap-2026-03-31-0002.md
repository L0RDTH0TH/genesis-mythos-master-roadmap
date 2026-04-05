---
title: Phase 2.2.3 — Conflict resolution, priority ordering, and merge policy
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.2.3"
project-id: godot-genesis-mythos-master
status: active
priority: high
progress: 34
handoff_readiness: 79
created: 2026-03-31
tags:
  - roadmap
  - godot-genesis-mythos-master
  - phase-2
para-type: Project
links:
  - "[[Phase-2-2-Intent-Resolver-and-Hook-Mapping-Roadmap-2026-03-30-2310]]"
  - "[[Phase-2-2-2-Validate-Classify-Schema-and-Hook-Mapping-Roadmap-2026-03-31-0001]]"
---

## Phase 2.2.3 — Conflict resolution, priority ordering, and merge policy

This tertiary defines the resolver stage that takes validated + classified hook payload outlines and decides which intents can co-exist, which must override, and which must defer. The output is an ordered merge-ready set of intents with explicit rationale codes, so later hook emission remains deterministic and replay-safe.

## Scope

**In scope:**
- Conflict detection across intents targeting the same domain/object/field region.
- Priority ordering contract across actor lanes (system, DM, player) and operation kinds.
- Merge policy matrix (`compose`, `override`, `defer`, `reject`) with deterministic tie-breaks.
- Reason-code surface for every conflict decision to support replay and post-run audit.
- Pre-emit handoff payload that preserves ordering and conflict outcomes for 2.2.4.

**Out of scope:**
- Actual hook emission into runtime pipeline slots (next tertiary).
- Runtime performance tuning and execution-track policy engines.
- Final authority on cross-session moderation policy (execution-deferred).

## Behavior (natural language)

Ordering:
1. Consume `ClassifiedIntent` + `HookPayloadOutline` from **2.2.2**.
2. Partition candidates by conflict domain (hook namespace/id + target region key).
3. Apply priority ladder and merge matrix:
   - no overlap -> compose
   - overlap + clear precedence -> override lower-priority candidate
   - overlap + unresolved precedence -> defer with reason code
   - invalid merge class pair -> reject with policy code
4. Produce a deterministic, stable order for surviving entries.
5. Emit `ResolvedIntentSet` and `ConflictDecisionLog` for pre-emit handoff.

Determinism contract:
- Same classified input set + same policy revision => same winners, same order, same reason codes.

## Interfaces

Natural-language type sketches:

- **ConflictCandidate:** `{ classifiedIntent, payloadOutline, conflictKey }`
- **MergePolicyMatrix:** rule table keyed by `(operationKindA, operationKindB, actorLaneA, actorLaneB)` -> decision class
- **ResolvedIntent:** `{ candidate, mergeDecision, precedenceRank, rationaleCode }`
- **ResolvedIntentSet:** ordered list of `ResolvedIntent` plus deferred/rejected buckets
- **ConflictDecisionLog:** append-only decision records with deterministic ids

Adjacent slices:
- **[[Phase-2-2-2-Validate-Classify-Schema-and-Hook-Mapping-Roadmap-2026-03-31-0001]]** provides valid classified candidates.
- Parent **[[Phase-2-2-Intent-Resolver-and-Hook-Mapping-Roadmap-2026-03-30-2310]]** requires deterministic normalize -> classify -> resolve -> emit flow.

## Edge cases

- Equal-priority conflicting intents in same lane: stable tie-break by deterministic tuple key; no random winner.
- Cascading conflicts (A blocks B, B blocks C): resolve by ordered pass with fixed precedence, then single normalization sweep.
- Mixed actor intents with stale frame token: reject/defer according to frame policy to avoid cross-frame bleed.
- Merge matrix missing row for pair: reject with `policy_row_missing` and surface for execution-track completion.

## Open questions

- **D-2.2.3-lane-precedence:** Final actor-lane precedence when DM and system both target same merge region in emergency events.
- **D-2.2.3-defer-window:** Whether deferred intents expire by frame count or explicit cancellation token.

## Pseudo-code readiness

At depth 3, this slice provides deterministic ordering and merge contracts with clear interface boundaries. Depth-4 pseudo-code for merge reducers and replay cursor reconciliation is execution-deferred.

## Research integration

> [!note] External grounding
> No `Ingest/Agent-Research/` notes were bound this run; alignment is pattern-only from deterministic policy-engine conflict resolution patterns used in rule-based intent routers.
