---
title: Roadmap auto-validation — genesis-mythos-master (Phase 2.2.2 re-check)
validation_type: roadmap_handoff_auto
project_id: genesis-mythos-master
queue_entry_id: "-"
parent_run_id: "-"
generated_at: 2026-03-20T10:32:55Z
roadmap_level: tertiary
roadmap_level_source: phase note frontmatter `roadmap-level: tertiary`
severity: medium
recommended_action: needs_work
reason_codes:
  - missing_decision_log_sync
  - missing_test_plan
  - safety_unknown_gap
gap_citations:
  missing_decision_log_sync: |
    decisions-log ends its Phase 2 canonical decision entries at Phase 2.1.7 and never records a Phase 2.2.2 handoff decision/acceptance criteria:
    `- [D-020] Phase 2.1.7 secondary closure rollup: adopt [[phase-2-1-7-phase-2-1-secondary-closure-rollup-and-advance-readiness-roadmap-2026-03-19-2110]] as the **authoritative G-P2.1-* pass/fail rollup** for Phase 2.1 secondary closure; **\`handoff_readiness: 94\`** ...`
    followed by `## Handoff notes` (no Phase 2.2 canonical decision block exists).
  missing_test_plan: |
    Harness denial-path assertions do not validate the fixture-level denial payload fields or denial-path ledger idempotency, despite the fixture table claiming these checks:
    - Harness denial branch (no `error_fingerprint`, no `TryApplyToLedger` calls on denial):
      `if result is denial:`
      `assert denial_event_payload.intent_id == result.intent_id`
      `assert exactly_one_denial_event_emitted_for(intent_id=result.intent_id)`
      `assert downstream_stage_hooks_stop_consuming(intent_id=result.intent_id)`
      `assert no manifest emission occurs for denied intent_id`
      `return`
    - Fixture expectations (explicit `error_fingerprint` + expected ledger double-apply for F2 / idempotency for F1):
      `- F2 ... expected \`error_fingerprint\`: \`b88c193009c22360a2a1e815905a7ea5f0b091647e5eaaff56a0cd90e22598b7\``
      `- expected idempotency: \`ledger_result_1=applied\`, \`ledger_result_2=ledger-hit\``
      and
      `- F1 ... expected idempotency: \`ledger_result_1=applied\`, \`ledger_result_2=ledger-hit\``
  safety_unknown_gap: |
    Stable-subset hashing is described, but the deterministic extraction/serialization contract for stable_json inputs is underspecified:
    - stable_field_digest depends on `stable_json` / `intent_constraints` ordering, but stable_json serialization semantics do not define string normalization / nested structure encoding beyond "keys sorted" + "no insignificant whitespace":
      `- stable_json = UTF-8 JSON with keys sorted lexicographically and no insignificant whitespace.`
      `- stable_field_digest := SHA-256(stable_json_bytes)`
    - intent_constraints is only stated as "sorted lexicographically" without defining deterministic representation (array-vs-set, element canonicalization, unicode normalization) before hashing:
      `- intent_constraints (sorted lexicographically)`
potential_sycophancy_check: false
actor: validator
---

# Roadmap auto-validation — hostile re-check

## (1) Summary
This re-validation shows progress: the Phase 2.2.2 tertiary note now materializes golden-vector fixtures (G1/G2/G3) and enumerates a stable-subset hashing allowlist/denylist. However, it still fails hostile delegatability hygiene because (1) the denial-path pseudo-code does not actually assert the fixture-level denial payload fields and denial-path ledger idempotency that the fixtures claim, (2) the project `decisions-log.md` stops canonical decision recording at Phase 2.1.7 (no Phase 2.2.2 handoff decision/acceptance criteria entry), and (3) the stable-subset hashing determinism is not pinned down enough for replay-proof hashing of nested/encoded fields.

Go/no-go (auto): needs a non-destructive reconciliation of harness assertions, decisions-log traceability, and the stable_json determinism contract.

## (2) Per-phase findings (Phase 2.2.2 tertiary)
### What is now fixed (vs initial report)
- Golden-vector table is populated and exhibits canonicalization drift collapse (G1 vs G2 canonical bytes and hashes match).
- Stable-subset hashing has an explicit transient denylist and semantic allowlist with a stated `stable_json`/digest formula.

### What still blocks hostile delegation
1. Denial fixtures specify `error_fingerprint` and denial-path ledger idempotency, but the harness denial branch never computes/compares `error_fingerprint` and never performs ledger double-apply assertions on denial.
2. The project `decisions-log.md` contains no Phase 2.2.2 canonical decision/acceptance-criteria entry; handoff readiness is therefore not anchored in the canonical decision ledger for delegatable review.
3. Replay-proof hashing still has determinism holes for how stable_json is derived/encoded from `validated_intent_view` for `intent_constraints` (and, by extension, `canonical_target`), beyond a high-level "sorted lexicographically" statement.

## (3) `next_artifacts` (definition of done)
- [ ] **Update Phase 2.2.2 harness pseudo-code to validate denial fixtures.**
  - Definition-of-done: denial branch asserts `error_fingerprint` equality to the F2 expected value and performs ledger double-apply/idempotency checks for denial identities matching the fixture `ledger_result_1/ledger_result_2` expectations for both F1 and F2 (or explicitly refactors to a shared ledger/idempotency block that denial paths call).
- [ ] **Add Phase 2.2.2 canonical decision + acceptance anchoring in `decisions-log.md`.**
  - Definition-of-done: decisions-log includes a Phase 2.2.2 handoff decision entry (new `D-02x`) and acceptance criteria (or explicit pointer to acceptance criteria blocks) that cite this note’s deterministic verification harness and the denial/handoff gating semantics.
- [ ] **Tighten stable_json extraction/serialization determinism.**
  - Definition-of-done: define a `stable_json(validated_intent_view)` construction contract that (a) extracts only the allowlist fields, (b) specifies deterministic encoding for `intent_constraints` (array vs set, element ordering, string canonicalization/unicode normalization), and (c) uses that exact stable_json byte encoding in both happy-path and denial-path computations.

---

## Machine verdict (for parsers)

```yaml
severity: medium
recommended_action: needs_work
reason_codes:
  - missing_decision_log_sync
  - missing_test_plan
  - safety_unknown_gap
potential_sycophancy_check: false
```

