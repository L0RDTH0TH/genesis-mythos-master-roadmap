---
title: Phase 2.2.1 — Intent canonicalization + denial taxonomy
roadmap-level: tertiary
phase-number: 2
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-20
tags: [roadmap, genesis-mythos-master, phase, intent-parser, determinism]
para-type: Project
subphase-index: "2.2.1"
handoff_readiness: 95
links:
  - "[[phase-2-2-intent-parser-integration-generation-hooks-roadmap-2026-03-20-0624]]"
  - "[[decisions-log]]"
---

## Phase 2.2.1 — Intent canonicalization + fail-closed denial reason-code taxonomy

This tertiary note turns the Phase 2.2 integration contract into delegatable, executable-grade pseudo-code and a fixed denial reason-code taxonomy (v0), so handoff readiness can be validated without hidden assumptions.

### Deterministic pseudo-code (v0)

#### Canonicalization + validation pipeline
```pseudo
constants:
  canonicalization_version := "CanonicalizeIntentBytes_v1"
  intent_schema_version_as_ascii := "IntentPlan_v0"
  domain_tag_v0 := "GENESIS_MYTHOS_INTENT_HASH_DOMAIN_V0"

function CanonicalizeIntentBytes_v1(raw_intent_text):
  s := UTF8_DECODE(raw_intent_text)              // decode boundary is explicit; if decode fails -> denial path
  s := UNICODE_NFC(s)
  s := NormalizeLineEndingsToLF(s)
  s := Trim(s)
  s := CollapseWhitespaceRunsToSingleSpace(s)   // whitespace chars: space/tab/LF
  s := RemoveZeroWidthCodepoints(s)
  canonical_string := s + LF + intent_schema_version_as_ascii
  return UTF8_ENCODE(canonical_string)

function StableIntentView_SerializedSubset(validated_intent_view):
  // stable subset only (no transient wall-clock fields, ids, etc.)
  return {
    "intent_kind": validated_intent_view.intent_kind,
    "canonical_target": validated_intent_view.canonical_target,
    "intent_constraints": SORT_LEX(validated_intent_view.intent_constraints),
    "intent_schema_version": "IntentPlan_v0"
  }

function stable_field_digest(validated_intent_view):
  stable_subset := StableIntentView_SerializedSubset(validated_intent_view)
  stable_json_bytes := CANONICAL_JSON_UTF8(stable_subset) // sorted keys + no insignificant whitespace
  return SHA256(stable_json_bytes) // raw 32-byte digest

function IntentHash_v0(raw_intent_text, validated_intent_view):
  canonical_bytes := CanonicalizeIntentBytes_v1(raw_intent_text)
  digest := stable_field_digest(validated_intent_view)
  preimage :=
    domain_tag_v0 ||
    len64(canonical_bytes) || canonical_bytes ||
    len64(intent_schema_version_as_ascii) || intent_schema_version_as_ascii ||
    len64(digest) || digest
  return SHA256(preimage) // raw 32-byte digest

function CanonicalizeThenValidate(raw_intent_text):
  try:
    canonical_bytes := CanonicalizeIntentBytes_v1(raw_intent_text)
  except decode/canonicalization error:
    return Denial(INTENT_CANONICALIZATION_ERROR, error_fingerprint=SHA256(raw_input_bytes))

  validated_intent_view_or_error := ValidateFrozenIntentPlanSchema(canonical_bytes)
  if schema validation fails:
    // fail-closed: canonical bytes exist; map denial deterministically
    intent_id := SHA256(domain_tag_v0 || len64(canonical_bytes) || canonical_bytes)
    return Denial(INTENT_SCHEMA_MISMATCH, intent_id=intent_id)

  return validated_intent_view
```

#### Denial reason-code taxonomy (fixed strings)
```text
INTENT_SCHEMA_MISMATCH            // stable schema field list mismatch
INTENT_CANONICALIZATION_ERROR     // contains disallowed characters/un-decodable bytes after canonicalization rules
```

### Denial event mapping (v0) — stable fields + determinism

The denial event must be *fail-closed*: no silent defaults; stage hooks must deterministically stop consuming the intent for that `intent_id`.

- On `INTENT_SCHEMA_MISMATCH`:
  - `reason_code`: `INTENT_SCHEMA_MISMATCH`
  - `intent_id`: `SHA256(domain_tag_v0 || len64(canonical_intent_bytes) || canonical_intent_bytes)` (canonicalization already succeeded)
  - `canonicalization_version`: `CanonicalizeIntentBytes_v1`
  - `intent_schema_version`: `IntentPlan_v0`
- On `INTENT_CANONICALIZATION_ERROR`:
  - `reason_code`: `INTENT_CANONICALIZATION_ERROR`
  - `error_fingerprint`: `SHA256(raw_input_bytes)` (precondition: raw bytes are the exact bytes at the player/DM boundary)
  - `canonicalization_version`: `CanonicalizeIntentBytes_v1`

### Hash-chain mapping (intent -> Phase 2.1 manifest hashing inputs)

To make golden vectors computable and testable in this integration hook slice, Phase 2.2 defines the deterministic mapping from `intent_hash` into manifest hashing inputs:

- `policy_hash := SHA256("intent_policy_v0" || intent_hash_bytes)`
- `lattice_hash := SHA256("intent_lattice_v0" || intent_hash_bytes)`
- `canonical_serialized_rows* := UTF8("INTENT_TARGET=" || canonical_target)`
- `manifest_hash := SHA256(lattice_hash_bytes || policy_hash_bytes || canonical_serialized_rows_bytes)`
- `spawn_event_id_0 := SHA256("spawn_event_v0" || intent_hash_bytes || 0x00)`
- `spawn_event_id ordering := [spawn_event_id_0]` for this v0 slice

### Golden vectors (computed) for handoff verification

Definitions assumed for all vectors:
- `intent_schema_version_as_ascii = "IntentPlan_v0"`
- `canonicalization_version = "CanonicalizeIntentBytes_v1"`
- `domain_tag_v0 = "GENESIS_MYTHOS_INTENT_HASH_DOMAIN_V0"`
- `stable_field_digest` computed as SHA-256 of canonical JSON stable subset (see pseudo-code)

| Vector | raw intent text | canonical_intent_bytes_hex | intent_hash_hex | manifest_hash_hex | spawn_event_id ordering |
| --- | --- | --- | --- | --- | --- |
| G1 | `Move to Sector A` | `4d6f766520746f20536563746f7220410a496e74656e74506c616e5f7630` | `5b2f6d3fd7c64a7525222fbd7583b11cd6ba71326c9b6b9c314368ba01d4e3a6` | `b5755f84fbfe43a67b8c8b0af6d378f2a529278cbe1388e26b4447f2e2f7a19a` | `[1b4c2abb8961c17ea5ad331578495cd49fc9c33e3e31ffacd11940fe58844b99]` |
| G2 | `  Move   to   Sector   A  ` | `4d6f766520746f20536563746f7220410a496e74656e74506c616e5f7630` | `5b2f6d3fd7c64a7525222fbd7583b11cd6ba71326c9b6b9c314368ba01d4e3a6` | `b5755f84fbfe43a67b8c8b0af6d378f2a529278cbe1388e26b4447f2e2f7a19a` | `[1b4c2abb8961c17ea5ad331578495cd49fc9c33e3e31ffacd11940fe58844b99]` |
| G3 | `Rest at Sector A` | `5265737420617420536563746f7220410a496e74656e74506c616e5f7630` | `933778468e12f75dacae727638f1edff8eb8a6216d2b7a89cee1312eeec30360` | `fe980e32ed7c84197b9567d2bccc7746194a667a720d8ccdc0e72ad477b73471` | `[313f06099e5c205731afa9e3d7074f4e6a27371f3638f0c5efbec6d7d7cd3a38]` |

### v0 Risk register (handoff)

| Risk | Impact | Mitigation |
| --- | --- | --- |
| R1: Canonicalization drift (whitespace/zero-width handling mismatch) | Intent hashes diverge across replay | Canonicalization rules are frozen + vectors (G1/G2) assert equality |
| R2: stable_field_digest serialization mismatch | Hash-chain changes unpredictably | stable_json definition is explicit (sorted keys + no insignificant whitespace) |
| R3: denial mapping ambiguity | Fail-open behavior / inconsistent denial | Denial mapping table + stable reason_code strings are fixed and used in fail-closed gate |

