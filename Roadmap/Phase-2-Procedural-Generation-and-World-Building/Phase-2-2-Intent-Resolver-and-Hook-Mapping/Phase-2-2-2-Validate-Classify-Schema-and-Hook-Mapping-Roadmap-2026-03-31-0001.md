---
title: Phase 2.2.2 — Validate / classify schema and hook mapping
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.2.2"
project-id: genesis-mythos-master
status: active
priority: high
progress: 32
handoff_readiness: 78
created: 2026-03-31
tags:
  - roadmap
  - genesis-mythos-master
  - phase-2
para-type: Project
links:
  - "[[Phase-2-2-Intent-Resolver-and-Hook-Mapping-Roadmap-2026-03-30-2310]]"
  - "[[Phase-2-2-1-Intent-Envelope-Normalization-and-Identity-Binding-Roadmap-2026-03-30-2338]]"
---

## Phase 2.2.2 — Validate / classify schema and hook mapping

This tertiary defines the **second resolver stage** after normalization: every **canonical intent envelope** is **validated** against a versioned **hook schema catalog**, **classified** into a stable **hook family + operation**, and **mapped** to a deterministic **hook payload skeleton** that downstream pipeline stages consume. No hook emission occurs here—that is reserved for later resolver stages—so invalid or ambiguous intents are rejected or deferred with structured diagnostics before any merge or priority logic runs.

## Scope

**In scope:**
- Structural validation of `CanonicalIntentEnvelope` (required fields, revision compatibility, frame/channel consistency with **2.2.1**).
- **HookSchemaCatalog** versioning: schema id, breaking-change rules, and “unknown field” policy (strip vs reject).
- **Classification**: map validated envelopes to `(hookNamespace, hookId, operationKind)` where `operationKind` is one of a closed set (e.g. `apply`, `replace`, `defer`, `cancel`) aligned with parent **2.2** spine.
- **Hook mapping**: deterministic projection from classified intent to **typed hook payload outline** (field names, optional vs required blocks) without executing pipeline side effects.
- Diagnostic surface for **validation_failed** vs **classification_ambiguous** vs **schema_revision_mismatch**.

**Out of scope:**
- Conflict resolution, merge policy, and priority ordering (**2.2.3+**).
- Emitting hook payloads into the live pipeline graph (later stage).
- Execution-track registry of hook IDs or CI proof rows.

## Behavior (natural language)

Ordering (within this slice):
1. **Validate** each normalized envelope against the active **HookSchemaCatalog** for `normalizationRevision` + client compatibility flags carried from **2.2.1**.
2. **Classify** valid envelopes: choose `hookNamespace` / `hookId` / `operationKind` using deterministic rules (no heuristic “best guess” that changes under replay).
3. **Map** to **HookPayloadOutline**: a skeleton object that lists required typed slots the emitter stage will fill; includes explicit **empty** markers where optional data is absent.
4. **Route failures**: validation errors → structured reject; ambiguous classification (multiple equally scored targets) → **defer** token with reason code; schema too new → **reject** with upgrade hint.
5. **Hand off** classified + mapped artifacts to the **resolve / conflict** stage (**2.2.3**), preserving ordering guarantees from **2.2.1**.

Determinism contract:
- Same validated catalog version + same normalized envelope bytes ⇒ same classification + same payload outline (including diagnostic branches).

## Interfaces

Natural-language type sketches (not APIs):

- **HookSchemaCatalog:** `{ catalogRevision, hooks: HookSchema[] }` where each **HookSchema** defines allowed `hookNamespace`, `hookId`, payload shape, and compatible `normalizationRevision` ranges.
- **ValidatedIntent:** `{ envelope: CanonicalIntentEnvelope, catalogRevisionUsed, validationLabels[] }`
- **ClassifiedIntent:** `{ validated: ValidatedIntent, hookNamespace, hookId, operationKind, classificationConfidence: explicit | rule_id }`
- **HookPayloadOutline:** `{ classified: ClassifiedIntent, slots: Record<string, slotDescriptor>, empty: string[] }`

Adjacent slices:
- **[[Phase-2-2-1-Intent-Envelope-Normalization-and-Identity-Binding-Roadmap-2026-03-30-2338]]** supplies canonical envelopes; this slice consumes them and must never widen envelopes silently.
- Parent **[[Phase-2-2-Intent-Resolver-and-Hook-Mapping-Roadmap-2026-03-30-2310]]** defines the normalize → classify → resolve → emit spine; this note instantiates **validate + classify + map-to-outline**.

## Edge cases

- **Unknown hookId** in catalog: reject with catalog revision hint (no fallback hook).
- **Multi-match classification** (two schemas fit): defer with `classification_ambiguous` unless a disambiguation rule table is exhaustive—table must be versioned with the catalog.
- **Partial payload** that satisfies schema but contradicts `operationKind`: validation error, not silent coercion.
- **Replay** with older catalog: migration path must be explicit (bump catalog revision or pinned replay mode)—tracked as open question **D-2.2.2-catalog-replay**.

## Open questions

- **D-2.2.2-catalog-replay:** Whether replay pins `HookSchemaCatalog` revision per frame or always uses latest—**execution-deferred**; see [[decisions-log]].
- **D-2.2.2-ambiguous-default:** Default policy when disambiguation table is incomplete (strict defer vs last-writer on rule id)—**execution-deferred**; see [[decisions-log]].

## Pseudo-code readiness

At depth 3, mid-technical: validation/classification/mapping interfaces + ordering + determinism; algorithm-level pseudocode optional. No depth-4 pseudo-code required for conceptual completion of this slice.

## Research integration

> [!note] External grounding
> No `Ingest/Agent-Research/` notes were bound this run; alignment is pattern-only from schema-validation + deterministic classification patterns common in typed pipeline routers.
