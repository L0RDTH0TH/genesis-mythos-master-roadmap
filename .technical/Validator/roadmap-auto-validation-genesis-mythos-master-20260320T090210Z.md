---
title: Roadmap auto-validation — genesis-mythos-master (Phase 2.2 → 2.2.1 intent_hash contract)
created: 2026-03-20
validation_type: roadmap_handoff_auto
project_id: genesis-mythos-master
queue_entry_id: queue-repair-gaps-deepen-phase2-2-20260320-2
parent_run_id: "351c7701"
generated_at: 2026-03-20T09:02:10Z
roadmap_level: secondary
severity: high
recommended_action: block_destructive
reason_codes:
  - safety_unknown_gap
gap_citations:
  safety_unknown_gap: |
    Phase 2.2 (intent_hash operator/variable naming is ambiguous):
    "intent_hash = H(domain_tag_v0 || len64(canonical_intent_bytes) || canonical_intent_bytes || len64(intent_schema_version) || intent_schema_version || len64(stable_field_digest(validated_intent_view)) || stable_field_digest(validated_intent_view))"

    Phase 2.2.1 (explicitly pins SHA256 + intent_schema_version_as_ascii + digest):
    "preimage := domain_tag_v0 || len64(canonical_bytes) || canonical_bytes || len64(intent_schema_version_as_ascii) || intent_schema_version_as_ascii || len64(digest) || digest"
    "return SHA256(preimage) // raw 32-byte digest"
next_artifacts:
  - "In `phase-2-2-intent-parser-integration-generation-hooks-roadmap-2026-03-20-0624.md`, define `H(...)` to exactly equal `SHA256(...)` (and confirm digest byte semantics match `len64(digest)`); DOD: a reader can compute `intent_hash` from inputs without interpretation gaps."
  - "In the same Phase 2.2 file, pin `intent_schema_version` to the exact same constant/string used in Phase 2.2.1 (`intent_schema_version_as_ascii = \"IntentPlan_v0\"`) and/or rename the variable in the formula; DOD: preimage field names and encodings match Phase 2.2.1 verbatim."
  - "Cross-check that the Phase 2.2 intent_hash preimage definition reproduces the Phase 2.2.1 golden vectors (G1/G2/G3) for both `intent_hash_hex` and downstream `manifest_hash_hex`; DOD: explicit note/proof ties computed vectors to the preimage definition."
potential_sycophancy_check: true
---

# Roadmap auto-validation — hostile auto-check

## (1) Summary
Phase 2.2 and Phase 2.2.1 agree on the *structure* of the intent_hash preimage (domain tag, length-prefixed canonical bytes, stable digest component, and feed into manifest_hash/spawn ordering), but they do not reconcile the preimage *notation* required for deterministic replay: Phase 2.2 leaves the hash operator as `H(...)` and uses `intent_schema_version` in the preimage formula, while Phase 2.2.1 explicitly pins `SHA256(preimage)` and uses `intent_schema_version_as_ascii` plus a `digest` binding. This is safety-critical ambiguity in the cross-phase contract, so the handoff is not delegatable yet.

## (1b) Roadmap altitude
- `secondary` (roadmap_level from hand-off / validated phase note frontmatter).

## (1c–1e) reason_codes, gap citations, and delegated readiness
### reason_codes
| reason_code | What’s missing / wrong |
|---|---|
| `safety_unknown_gap` | The cross-phase intent_hash preimage contract is not expressed identically: `H(...)` vs explicit `SHA256(...)` plus `intent_schema_version` vs `intent_schema_version_as_ascii`. |

### Verbatim gap citations
- Phase 2.2: `intent_hash = H(domain_tag_v0 || len64(canonical_intent_bytes) || canonical_intent_bytes || len64(intent_schema_version) || intent_schema_version || len64(stable_field_digest(validated_intent_view)) || stable_field_digest(validated_intent_view))`
- Phase 2.2.1: `preimage := domain_tag_v0 || len64(canonical_bytes) || canonical_bytes || len64(intent_schema_version_as_ascii) || intent_schema_version_as_ascii || len64(digest) || digest`
- Phase 2.2.1: `return SHA256(preimage) // raw 32-byte digest`

## (1f) Potential sycophancy check
true. I was tempted to treat `H(...)` as “obviously SHA256” because Phase 2.2.1 contains golden vectors, but that assumption is exactly the kind of silent interpretation this contract forbids.

## (2) Per-phase findings
### Phase 2.2 (secondary note)
- The lifecycle, deterministic intent hashing *intent*, golden vectors, and fail-closed denial semantics are present.
- However, the intent_hash preimage formula is not reconciled with Phase 2.2.1 at the determinism-notation level (`H(...)` and `intent_schema_version` are not pinned to Phase 2.2.1’s explicit `SHA256(...)` and `intent_schema_version_as_ascii`).

### Phase 2.2.1 (tertiary note)
- Executable-grade pseudo-code pins canonicalization, the intent_hash preimage, and `return SHA256(preimage)`.
- It also pins the constant used for the preimage string: `intent_schema_version_as_ascii = "IntentPlan_v0"` and defines `digest` as the stable_field_digest output.

## (3) Cross-phase / structural issues
- Cross-phase determinism contract violation (documentation-level): Phase 2.2 notation does not state equivalence to Phase 2.2.1 notation, which risks future replay mismatches or repeated recalibration thrash.

---
# Machine verdict (parsers)
severity: high
recommended_action: block_destructive
reason_codes: [safety_unknown_gap]
next_artifacts:
  - "In Phase 2.2, define `H(...) := SHA256(...)` and align the intent_schema_version binding to Phase 2.2.1."
  - "Verify that Phase 2.2’s formula reproduces Phase 2.2.1 golden vectors (intent_hash_hex + manifest_hash_hex)."
potential_sycophancy_check: true
---
