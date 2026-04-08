---
title: Phase 2.2.2 — Execution validate / classify schema and hook mapping (Godot lane)
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.2.2"
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
conceptual_counterpart: "[[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-2-Intent-Resolver-and-Hook-Mapping/Phase-2-2-2-Validate-Classify-Schema-and-Hook-Mapping-Roadmap-2026-03-31-0001]]"
links:
  - "[[Phase-2-2-Execution-Intent-Resolver-and-Hook-Mapping-Roadmap-2026-04-10-1900]]"
  - "[[../Phase-2-Execution-Procedural-Generation-and-World-Building-Roadmap-2026-04-08-1227]]"
  - "[[Phase-2-2-1-Execution-Intent-Envelope-Normalization-and-Identity-Binding-Roadmap-2026-04-08-2315]]"
---

## Phase 2.2.2 — Execution validate / classify schema and hook mapping

Execution tertiary mirror for conceptual **2.2.2**. Second resolver stage after **2.2.1** normalization: **validate** canonical envelopes against a versioned **HookSchemaCatalog**, **classify** into `(hookNamespace, hookId, operationKind)`, **map** to deterministic **HookPayloadOutline** for downstream emit stages. Composes **S1** seam continuity from [[../Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-Execution-Pipeline-Stages-Seed-to-World-Roadmap-2026-04-08-1805]] via **2.2.1** digest inputs. Lane **godot (A)** vs **sandbox (B)** comparand parity preserved.

> [!note] Queue reconcile
> Queue `followup-deepen-exec-p21-mint-godot-20260410T180500Z` requested **secondary 2.1** mint under the parallel spine; **2.1** + tertiaries **2.1.1–2.1.5** were already on disk (**[[../../workflow_state-execution]]** Iter **12–18**). Authoritative pre-read cursor was **`2.2.2`** after **2.2.1** (**Iter 20**). This run mints **tertiary 2.2.2** (stale **2.1** target reconciled forward per Layer 1 resolver).

## Scope

**In scope:** catalog revision binding to `normalizationRevision` from **2.2.1**, validation labels, classification disambiguation table versioning, payload outline slots, `G-2.2.2-*` dry-run vs execute parity rows, junior stub pseudocode.

**Out of scope:** conflict resolution / merge policy (**2.2.3+**), hook emission side effects, `GMM-2.4.5-*` / full CI registry proof (explicit defer rows only).

## Lane comparand — godot (A) vs sandbox (B)

| Concern | **Lane godot (A)** | **Lane sandbox (B)** |
| --- | --- | --- |
| Catalog host | Resource `HookSchemaCatalog` + revision pin per session | In-memory catalog clone; identical revision namespace |
| Validation | `catalog.validate(envelope)` returns typed `ValidationLabel[]` | Same API; harness fixtures |
| Classification | Deterministic rule engine keyed by `(catalogRevision, hookId)` | Same rule ids; synthetic envelopes |
| Replay | Digest joins **2.1.5** `ReplayLedgerEntry` + **2.2.1** normalization revision | Harness ledger tuple |

## Pipeline seam — 2.2.1 → 2.2.2 → 2.2.3

| Seam | Upstream | This slice (2.2.2) | Downstream |
| --- | --- | --- | --- |
| Envelopes in | [[Phase-2-2-1-Execution-Intent-Envelope-Normalization-and-Identity-Binding-Roadmap-2026-04-08-2315]] | Validate + classify + outline | **2.2.3** conflict resolution |
| Catalog | `HookSchemaCatalog` revision | Compatibility bounds for `normalizationRevision` | Staged merge inputs only after PASS |

## Pseudocode — validate / classify / map (junior-dev stubs)

```pseudo
func validate_classify_map(envelopes: CanonicalIntentEnvelope[], catalog: HookSchemaCatalog) -> ClassifiedIntent[]:
  out = []
  for e in envelopes:
    v = catalog.validate(e, catalog.revision)
    if not v.ok:
      out.append(reject(v.labels))
      continue
    c = catalog.classify(v.validated, disambiguationTable[catalog.revision])
    if c.ambiguous:
      out.append(defer("classification_ambiguous", c.candidates))
      continue
    outline = catalog.map_outline(c)
    out.append(ClassifiedIntent(validated=v.validated, classified=c, outline=outline))
  return deterministic_sort(out, tieBreak=catalog.tieBreak)
```

## Roll-up gates — `G-2.2.2-*` (execution_v1)

| Gate ID | Verdict | Evidence in this note | Owner signoff token |
| --- | --- | --- | --- |
| `G-2.2.2-Catalog-Revision-Bind` | **PASS** | Catalog revision + normalizationRevision compatibility | `owner_signoff_G-2.2.2-Catalog-Revision-Bind_2026-04-08` |
| `G-2.2.2-Validation-Labels` | **PASS** | Validation path + reject vs defer semantics | `owner_signoff_G-2.2.2-Validation-Labels_2026-04-08` |
| `G-2.2.2-Classification-Determinism` | **PASS** | Disambiguation table + no heuristic drift | `owner_signoff_G-2.2.2-Classification-Determinism_2026-04-08` |
| `G-2.2.2-Lane-Comparand-Parity` | **PASS** | Comparand table | `owner_signoff_G-2.2.2-Lane-Comparand-Parity_2026-04-08` |
| `G-2.2.2-GMM-CI-Deferred` | **FAIL (explicit, non-blocking)** | `GMM-2.4.5-*` / CI closure | `owner_defer_G-2.2.2-GMM-CI-Deferred_2026-04-08` |

## Deferred safety / CI seams (explicit)

| Seam | State | Notes |
| --- | --- | --- |
| `GMM-2.4.5-*` | deferred | Owner/timebox: see [[../../workflow_state-execution#Deferred safety seam closure map]] |
| Registry / CI proof | deferred | Non-blocking FAIL row; execution track evidence path TBD |

## Test plan

| Mode | Harness / fixture | Scope |
| --- | --- | --- |
| Dry-run | `fixtures/harness_intent_validate_classify_v1` (sandbox B) + `res://test/intent/validate_classify_dryrun.tres` (godot A) | Catalog revision bind + validation label paths (reject/defer) |
| Execute | Same harness with `execute=true`; digest joins **2.2.1** + **2.1.5** replay ledger | Parity: identical classification + outline bytes across modes |
| Failure injection | `fixture_ambiguous_multi_match`, `fixture_schema_too_new`, `fixture_unknown_hook_id` | Forces `classification_ambiguous`, schema revision reject, unknown hook reject |

## Executable acceptance criteria

| Gate ID | Observable evidence (must pass in harness) |
| --- | --- |
| `G-2.2.2-Catalog-Revision-Bind` | Catalog revision pinned; incompatible `normalizationRevision` yields structured reject with hint |
| `G-2.2.2-Validation-Labels` | Invalid envelope produces typed `ValidationLabel[]`; valid proceeds to classify |
| `G-2.2.2-Classification-Determinism` | Repeated run on same bytes → same `(hookNamespace, hookId, operationKind)` and outline |
| `G-2.2.2-Lane-Comparand-Parity` | Godot vs sandbox rows produce bit-identical classified outputs for shared fixtures |
| `G-2.2.2-GMM-CI-Deferred` | Explicit FAIL row remains; no silent promotion of registry/CI proof |

## Related

- Parent secondary: [[Phase-2-2-Execution-Intent-Resolver-and-Hook-Mapping-Roadmap-2026-04-10-1900]]
- Next tertiary: **2.2.3** — conflict resolution / merge policy (conceptual: Phase-2-2-3-…)
