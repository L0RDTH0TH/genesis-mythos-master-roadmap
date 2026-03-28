---
title: Roadmap auto-validation — genesis-mythos-master (Phase 2.2.1)
validation_type: roadmap_handoff_auto
project_id: genesis-mythos-master
queue_entry_id: queue-repair-gaps-deepen-phase2-2-20260320-2
parent_run_id: 351c7701
generated_at: 2026-03-20T09:01:03.117Z
roadmap_level: tertiary
roadmap_level_source: inferred from phase note frontmatter `roadmap-level: tertiary` (Phase 2.2.1 note)
severity: high
recommended_action: block_destructive
reason_codes:
  - contradictions_detected
gap_citations:
  contradictions_detected: |
    Phase 2.2 intent_hash formula includes `len64(stable_field_digest(validated_intent_view)) || stable_field_digest(validated_intent_view)` only once:
    `intent_hash = H(domain_tag_v0 || len64(canonical_intent_bytes) || canonical_intent_bytes || len64(intent_schema_version) || intent_schema_version || len64(stable_field_digest(validated_intent_view)) || stable_field_digest(validated_intent_view))`
    
    Phase 2.2.1 pseudo-code IntentHash_v0 preimage includes the same `digest` three times (`len64(digest) || digest || digest`):
    `preimage := domain_tag_v0 || len64(canonical_bytes) || canonical_bytes || len64(intent_schema_version_as_ascii) || intent_schema_version_as_ascii || len64(digest) || digest || digest`
next_artifacts:
  - Resolve the intent_hash preimage contract to a single canonical definition across both notes (`Phase 2.2` and `Phase 2.2.1`), including whether `digest` appears once vs duplicated in the preimage.
  - Update one of: the `Phase 2.2` intent_hash formula or the `Phase 2.2.1` pseudo-code `IntentHash_v0` preimage so they match byte-for-byte.
  - Regenerate/verify golden vectors in `Phase 2.2.1` (G1/G2/G3) to match the reconciled contract, and ensure `manifest_hash_hex` and `spawn_event_id ordering` remain consistent with the same formula.
  - Confirm the stage-hook consumption boundary decision (“IntentPlan consumed at the manifest-emission boundary”) remains unchanged and still matches the denial-path semantics (no silent defaults).
potential_sycophancy_check: true
---

# Roadmap auto-validation — hostile auto-check (Phase 2.2.1 handoff trace)

## (1) Summary
Phase 2.2.1’s handoff trace is **not delegatable** because the determinism contract for `intent_hash` is internally contradictory across the Phase 2.2 integration contract and Phase 2.2.1’s executable-grade pseudo-code. Specifically, the Phase 2.2 intent_hash formula includes the `stable_field_digest(validated_intent_view)` only once in the hash preimage, while Phase 2.2.1’s `IntentHash_v0` preimage includes `digest` duplicated (effectively changing the preimage). This breaks replay-identity determinism: junior-dev implementation from either definition cannot produce the same `intent_hash_hex`/`manifest_hash_hex` vectors reliably. **Hard block** until the preimage contract is reconciled and vectors are regenerated from the single canonical formula.

## (1b) Roadmap altitude
- `tertiary` (from `phase-2-2-1...` frontmatter `roadmap-level: tertiary`).

## (1c–1e) reason_codes, gap citations, and delegated readiness
Reason code: `contradictions_detected`.
- Evidence: the explicit `intent_hash` preimage formula differs between the Phase 2.2 contract and the Phase 2.2.1 pseudo-code (see `gap_citations`).

## (2) Per-phase findings (Phase 2.2 → Phase 2.2.1)
### Phase 2.2 (integration contract)
- Contains an explicit intent_hash formula, and specifies deterministic intent_hash propagation into Phase 2.1 hash-chain seams.
- However, the intent_hash preimage includes `stable_field_digest(validated_intent_view)` only once.

### Phase 2.2.1 (tertiary executable pseudo-code + denial taxonomy)
- Provides deterministic pseudo-code, denial reason-code taxonomy, denial event mapping, and golden vectors.
- But its `IntentHash_v0` preimage includes the `digest` duplicated, which is inconsistent with the Phase 2.2 contract formula.

## (3) Hostile recommendation
Do **not** proceed with deeper integration work or treat this handoff trace as validated. The pipeline needs an explicit reconciliation of the hash preimage contract so replay determinism and golden-vector truth can be unambiguously enforced.

---
Machine verdict (for parsers):
severity: high
recommended_action: block_destructive
reason_codes:
  - contradictions_detected
potential_sycophancy_check: true
