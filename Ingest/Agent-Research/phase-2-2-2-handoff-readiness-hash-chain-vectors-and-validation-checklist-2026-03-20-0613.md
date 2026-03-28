---
title: Phase 2.2.2 — Handoff readiness (hash-chain vectors + validation checklist)
created: 2026-03-20
tags: [research, agent-research, genesis-mythos-master, handoff-readiness, hash-chain, testing]
project-id: genesis-mythos-master
linked_phase: Phase-2-2-2
research_query: testing patterns for hash-chain integrations (golden vectors, whitespace/canonicalization drift checks) + handoff_readiness best practices
agent-generated: true
---

## Summary
This note consolidates the golden-vector test matrix and drift checks required to prove that the Phase 2.2 intent hash chain integrates deterministically into downstream manifest hashing, plus a checklist for computing/validating `handoff_readiness` for technical handoff between pipeline stages.

## Contract anchors (canonical bytes + hash chain)
Key source references:
- [[1-Projects/genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building/phase-2-2-intent-parser-integration-generation-hooks-roadmap-2026-03-20-0624.md]]
- [[1-Projects/genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building/phase-2-2-1-intent-canonicalization-and-denial-taxonomy-roadmap-2026-03-20-0901.md]]
- [[Ingest/Agent-Research/phase-2-2-intent-parser-procedural-hooks-determinism-integration-research-2026-03-20-0233.md]]

### Canonicalization rules (frozen)
Use `CanonicalizeIntentBytes_v1`:
- decode boundary is explicit UTF-8; decode failure -> denial path
- Unicode NFC
- normalize line endings to LF
- trim leading/trailing whitespace
- collapse whitespace runs (space/tab/LF) to a single space
- remove zero-width codepoints
- append `LF` + `intent_schema_version_as_ascii` where `intent_schema_version_as_ascii := "IntentPlan_v0"`

### Hash concatenation / stable JSON
- any concatenation inside `intent_hash` uses `len64(...)` length-prefixed fields
- stable_field_digest uses a stable JSON definition (sorted keys, no insignificant whitespace)
- excluded transient fields must not participate in hashing

## Golden vectors (must be computed and asserted)
Minimum golden vector set:

### G1 / G2: “Move to Sector A” whitespace/punctuation drift checks
- G1
  - raw intent text: `Move to Sector A`
  - canonical_intent_bytes_hex: `4d6f766520746f20536563746f7220410a496e74656e74506c616e5f7630`
  - intent_hash_hex: `5b2f6d3fd7c64a7525222fbd7583b11cd6ba71326c9b6b9c314368ba01d4e3a6`
  - manifest_hash_hex: `b5755f84fbfe43a67b8c8b0af6d378f2a529278cbe1388e26b4447f2e2f7a19a`
  - spawn_event_id ordering (v0): `[1b4c2abb8961c17ea5ad331578495cd49fc9c33e3e31ffacd11940fe58844b99]`
- G2
  - raw intent text: `  Move   to   Sector   A  `
  - canonical_intent_bytes_hex: (must equal G1)
  - intent_hash_hex: (must equal G1)
  - manifest_hash_hex: (must equal G1)
  - spawn_event_id ordering (v0): (must equal G1)

### G3: “Rest at Sector A”
- raw intent text: `Rest at Sector A`
- canonical_intent_bytes_hex: `5265737420617420536563746f7220410a496e74656e74506c616e5f7630`
- intent_hash_hex: `933778468e12f75dacae727638f1edff8eb8a6216d2b7a89cee1312eeec30360`
- manifest_hash_hex: `fe980e32ed7c84197b9567d2bccc7746194a667a720d8ccdc0e72ad477b73471`
- spawn_event_id ordering (v0): `[313f06099e5c205731afa9e3d7074f4e6a27371f3638f0c5efbec6d7d7cd3a38]`

## Fail-closed cases (minimum denial assertions)
Fail-closed denials (must halt downstream consumption):
- F1: `INTENT_SCHEMA_MISMATCH`
- F2: `INTENT_CANONICALIZATION_ERROR`

Assertions:
- emit exactly one deterministic denial event per denied `intent_id`
- no partial downstream publish artifacts for that `intent_id`

## Hash-chain mapping: intent_hash -> manifest_hash / spawn ordering
For the v0 integration slice:
- `policy_hash := SHA256("intent_policy_v0" || intent_hash_bytes)`
- `lattice_hash := SHA256("intent_lattice_v0" || intent_hash_bytes)`
- `manifest_hash := SHA256(lattice_hash_bytes || policy_hash_bytes || canonical_serialized_rows_bytes)`
- `spawn_event_id_0 := SHA256("spawn_event_v0" || intent_hash_bytes || 0x00)`
- spawn_event_id ordering is deterministic under this v0 slice (`[spawn_event_id_0]`)

## Testing patterns checklist (how to structure CI)
1. Byte-level asserts first
   - canonical_intent_bytes hex must match golden vectors
2. Hash asserts next
   - intent_hash_hex and manifest_hash_hex must match golden vectors
3. Ordering asserts last
   - spawn_event_id ordering must match golden vectors
4. Drift tests
   - run G1 input variants (whitespace/punctuation) and ensure they converge to the same canonical bytes + hashes
5. Negative tests
   - verify fail-closed for F1/F2: exactly one denial event, downstream stage consumption halts
6. Ledger/idempotency tests
   - re-run the same command/event trace twice and assert no additional ledger mutations

## Handoff_readiness computation + validation (best practices)
Phase handoff gating expects measurable, evidence-backed readiness, not narrative claims.

### Suggested readiness checklist for `handoff_readiness >= min_handoff_conf`
For the handoff boundary between pipeline stages, mark readiness based on whether all of the following are satisfied:

1. Contract freeze evidence is pinned
   - canonicalization_version + intent_schema_version_as_ascii + domain_tag_v0 are explicit and versioned
   - stage hook boundary is fixed (no “sometimes consumes earlier/later” ambiguity)
2. Deterministic replay proven by CI-style tasks
   - parser determinism (canonical bytes + IntentPlan stable serialization)
   - schema validation determinism (stable denial reasons/identifiers)
3. Hash-chain golden vectors pass
   - G1/G2/G3 vectors are asserted
4. Drift checks pass
   - whitespace/punctuation variants converge to identical canonical_intent_bytes and hence identical hashes
5. Fail-closed behavior pass
   - invalid intent yields exactly one deterministic denial event and prevents downstream publish artifacts
6. Evidence inventory is complete
   - each checklist item is linked via wiki links to the phase notes / research notes used as proof

### Practical rule for the handoff score
If any of the above CI-style assertions is missing or unverified (e.g., golden vectors not computed, stable subset serialization unspecified, denial mapping not fixed), treat the readiness as insufficient for advance-phase gating.

## Sources
- [[Ingest/Agent-Research/phase-2-2-2-handoff-readiness-deterministic-replay-ledger-idempotency-2026-03-20-0613.md]]
- [[Ingest/Agent-Research/phase-2-2-2-handoff-readiness-fail-closed-denial-schema-mapping-2026-03-20-0613.md]]
- [[1-Projects/genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building/phase-2-2-intent-parser-integration-generation-hooks-roadmap-2026-03-20-0624.md]]
- [[1-Projects/genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building/phase-2-2-1-intent-canonicalization-and-denial-taxonomy-roadmap-2026-03-20-0901.md]]
- https://json-schema.org/draft/2020-12

