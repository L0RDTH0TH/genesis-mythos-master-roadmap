---
title: Roadmap auto-validation — genesis-mythos-master (post-little-val)
validation_type: roadmap_handoff_auto
project_id: genesis-mythos-master
queue_entry_id: queue-repair-gaps-deepen-phase2-2-20260320-3
parent_run_id: queue-roadmap-parent-20260320-060525
generated_at: 2026-03-20T10:43:57Z
roadmap_level: tertiary
roadmap_level_source: inferred from phase note frontmatter `roadmap-level: tertiary` on `phase-2-2-2-intentplan-consumption-boundary-and-deterministic-verification-harness-roadmap-2026-03-20-0605.md`
severity: high
recommended_action: block_destructive
reason_codes:
  - contradictions_detected
gap_citations:
  contradictions_detected: |
    Phase 2.2.1 defines the `intent_hash` preimage as:
    `preimage :=
      domain_tag_v0 ||
      len64(canonical_bytes) || canonical_bytes ||
      len64(intent_schema_version_as_ascii) || intent_schema_version_as_ascii ||
      len64(digest) || digest`

    Phase 2.2.2 claims the `intent_hash` preimage uses only:
    `Because \`intent_hash\` preimage uses only \`domain_tag_v0\` + length-prefixed canonical bytes + \`stable_field_digest(validated_intent_view)\``
potential_sycophancy_check: true
next_artifacts:
  - "Reconcile the `intent_hash` preimage contract across `phase-2-2-1-...-0901.md` and `phase-2-2-2-...-0605.md` so there is exactly one canonical concatenation rule (including whether `intent_schema_version_as_ascii` is embedded via canonical bytes vs included as a separate len64-prefixed segment)."
  - "Update `phase-2-2-2-...-0605.md` stable-subset hashing filter section to spell out the full `intent_hash` preimage concatenation (not an abbreviated ‘only uses ...’ claim) matching the canonical formula."
  - "Recompute and verify golden vectors (`G1/G2/G3` intent_hash_hex + derived manifest_hash/spawn ordering) against the reconciled preimage contract; ensure the replay harness assertions and fixture tables agree."
  - "After the edits, rerun `roadmap_handoff_auto` so the validator no longer reports `contradictions_detected` for this phase."
---

# Roadmap auto-validation — hostile auto-check

## (1) Summary
This post–little-val handoff is **not** safe to treat as delegatable/readiness-complete. The `intent_hash` preimage contract is internally inconsistent across Phase 2.2.1 and Phase 2.2.2: one note explicitly includes `len64(intent_schema_version_as_ascii) || intent_schema_version_as_ascii` in the preimage, while the other claims the preimage uses only `domain_tag_v0`, length-prefixed canonical bytes, and `stable_field_digest(validated_intent_view)`. That mismatch is safety-critical because the deterministic replay harness relies on the preimage being computed identically at replay time; you can’t hand off a contract with competing hashing definitions.

## (1b) Roadmap altitude
- `tertiary` (inferred from phase note frontmatter `roadmap-level: tertiary`)

## (1c–1e) reason_codes and verbatim gap citations
- `contradictions_detected`
  - Phase 2.2.1 preimage includes `len64(intent_schema_version_as_ascii) || intent_schema_version_as_ascii`
  - Phase 2.2.2 asserts an abbreviated ‘only uses ...’ preimage statement that omits that segment from the contract text

## (2) Per-phase findings
### Phase 2.2.2 (`phase-2-2-2-...-0605.md`)
- The note is rich in executable-grade assertions and includes a transient-field denylist, but it still leaves a **contract mismatch** with Phase 2.2.1 over how the `intent_hash` preimage is constructed.

## (3) Cross-phase / structural issues
- Cross-phase determinism contract break: two different articulations of the `intent_hash` preimage exist. This is exactly the kind of mismatch that causes replay verification to drift even when the “golden vectors” appear plausible.

## (4) Hostile recommendation
Block destructive/automated acceptance steps until the preimage contract is reconciled and the golden vectors are recomputed. Otherwise you’re relying on undocumented interpretation rather than a frozen, unambiguous hashing contract.
---
