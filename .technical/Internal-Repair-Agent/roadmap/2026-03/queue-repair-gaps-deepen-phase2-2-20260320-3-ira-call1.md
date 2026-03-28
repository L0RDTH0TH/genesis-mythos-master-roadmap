---
created: 2026-03-20
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: queue-repair-gaps-deepen-phase2-2-20260320-3
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 2
  medium: 1
  high: 0
---

## Context
IRA is invoked during `RESUME_ROADMAP` (`action: deepen`, focus: `handoff-readiness`) for project `genesis-mythos-master` to repair structural gaps flagged by the hostile validator:
`missing_decision_log_sync`, `missing_test_plan`, and `safety_unknown_gap`.

The current Phase 2.2.2 note contains executable pseudo-code assertions but lacks (a) concrete golden-vector fixture values, (b) an explicit stable-subset allowlist/denylist for deterministic hashing, and (c) `distilled-core.md`’s dependency graph still stops at Phase 1.1.10.

## Structural discrepancies detected
1. `phase-2-2-2-intentplan-consumption-boundary-and-deterministic-verification-harness-roadmap-2026-03-20-0605.md` has golden-vector assertions referencing `golden_vectors.*`, but no populated G1/G2/G3 fixture table exists.
2. The Phase 2.2.2 note describes stable-subset exclusions conceptually, but does not enumerate the transient/non-semantic fields excluded from deterministic hashing, nor the exact stable-subset allowlist and mapping into `stable_field_digest`.
3. `distilled-core.md` `## Dependency graph` mermaid flowchart ends at Phase 1.1.10 and does not include any Phase 2 / Phase 2.2.2 nodes.

## Proposed fixes (advisory)
### 1) Populate golden-vector fixture table + denial fixtures in Phase 2.2.2 note
- id: `phase2-2-2-fill-golden-vectors-and-denials`
- risk_level: low
- target_file: `1-Projects/genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building/phase-2-2-2-intentplan-consumption-boundary-and-deterministic-verification-harness-roadmap-2026-03-20-0605.md`
- description: Replace the “Minimal test matrix” placeholder bullets with concrete G1/G2/G3 golden vectors and explicit F1/F2 fail-closed denial fixtures, including ledger/idempotency expected outcomes.
- definition_of_done:
  - A reader can find a filled golden-vector table containing at minimum these fields (with the exact hex values below): `canonical_intent_bytes_hex`, `intent_hash_hex`, `manifest_hash_hex`, and `spawn_event_id_ordering` for G1/G2/G3 (no placeholders).
  - The note includes at least one explicit denial fixture per denial reason-code:
    - `INTENT_SCHEMA_MISMATCH` (F1) with expected `intent_id`
    - `INTENT_CANONICALIZATION_ERROR` (F2) with expected `error_fingerprint`
  - For each golden vector, the note explicitly states the double-apply/idempotency expected outcomes: first apply `applied`, second apply `ledger-hit` (or equivalent wording matching the pseudo-code ledger assertions).
- minimal patch instructions (high level):
  - Insert a new subsection under `### Deterministic replay harness (v1) — executable-grade assertions` named `### Golden vectors (G1/G2/G3) — fixture table`.
  - Add a new subsection named `### Fail-closed denial fixtures (F1/F2) — expected denial payloads + stop-consumption`.
  - Update or replace the existing `### Minimal test matrix (handoff verification)` section so it references the filled tables instead of using placeholder bullets.
- concrete fixture values to paste:
  - G1: raw `Move to Sector A`
    - `canonical_intent_bytes_hex`: `4d6f766520746f20536563746f7220410a496e74656e74506c616e5f7630`
    - `intent_hash_hex`: `5b2f6d3fd7c64a7525222fbd7583b11cd6ba71326c9b6b9c314368ba01d4e3a6`
    - `manifest_hash_hex`: `b5755f84fbfe43a67b8c8b0af6d378f2a529278cbe1388e26b4447f2e2f7a19a`
    - `spawn_event_id_ordering`: `[1b4c2abb8961c17ea5ad331578495cd49fc9c33e3e31ffacd11940fe58844b99]`
    - `expected_double_apply`: `ledger_result_1 = applied`, `ledger_result_2 = ledger-hit`
  - G2: raw `  Move   to   Sector   A  `
    - Same `canonical_intent_bytes_hex`, `intent_hash_hex`, `manifest_hash_hex`, and `spawn_event_id_ordering` as G1
    - `expected_double_apply`: `ledger_result_1 = applied`, `ledger_result_2 = ledger-hit`
  - G3: raw `Rest at Sector A`
    - `canonical_intent_bytes_hex`: `5265737420617420536563746f7220410a496e74656e74506c616e5f7630`
    - `intent_hash_hex`: `933778468e12f75dacae727638f1edff8eb8a6216d2b7a89cee1312eeec30360`
    - `manifest_hash_hex`: `fe980e32ed7c84197b9567d2bccc7746194a667a720d8ccdc0e72ad477b73471`
    - `spawn_event_id_ordering`: `[313f06099e5c205731afa9e3d7074f4e6a27371f3638f0c5efbec6d7d7cd3a38]`
    - `expected_double_apply`: `ledger_result_1 = applied`, `ledger_result_2 = ledger-hit`
  - F1 (`INTENT_SCHEMA_MISMATCH`):
    - Use canonical-intent bytes from G1:
      - `canonical_intent_bytes_hex`: `4d6f766520746f20536563746f7220410a496e74656e74506c616e5f7630`
    - `expected_intent_id`: `4754625a0be8e38fbec7adc5297a4ad622a0f5fd8397d0d143d7546176413388`
    - Expected denial payload fields:
      - `reason_code`: `INTENT_SCHEMA_MISMATCH`
      - `intent_id`: (value above)
      - `canonicalization_version`: `CanonicalizeIntentBytes_v1`
      - `intent_schema_version`: `IntentPlan_v0`
    - Expected fail-closed outcomes:
      - exactly one denial event for the denied `intent_id`
      - downstream stage hooks stop consuming for that `intent_id`
      - no manifest emission for that denied `intent_id`
  - F2 (`INTENT_CANONICALIZATION_ERROR`):
    - Fixture raw_input_bytes_hex: `fffeff`
    - `expected_error_fingerprint`: `b88c193009c22360a2a1e815905a7ea5f0b091647e5eaaff56a0cd90e22598b7`
    - Expected denial payload fields:
      - `reason_code`: `INTENT_CANONICALIZATION_ERROR`
      - `error_fingerprint`: (value above)
      - `canonicalization_version`: `CanonicalizeIntentBytes_v1`
    - Expected fail-closed outcomes:
      - exactly one denial event
      - downstream stage hooks stop consuming the denied intent (use the stable identifier consistently with the note’s schema wiring)
      - no manifest emission occurs for the denied intent

### 2) Enumerate stable-subset exclusion rule in Phase 2.2.2 note
- id: `phase2-2-2-stable-subset-allowlist-denylist`
- risk_level: low
- target_file: `1-Projects/genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building/phase-2-2-2-intentplan-consumption-boundary-and-deterministic-verification-harness-roadmap-2026-03-20-0605.md`
- description: Add the explicit transient/non-semantic field exclusion set and the stable-subset allowlist, plus a short mapping showing how these fields feed the deterministic `stable_json` / `stable_field_digest` filter used inside `intent_hash` and downstream hashes.
- definition_of_done:
  - The note contains an explicit `transient_intent_fields` list (denylist) with the same items/meaning as upstream canonicalization + hashing notes.
  - The note contains an explicit stable-subset allowlist (`stable_subset` fields) used for `stable_field_digest`.
  - The note states how `stable_field_digest(validated_intent_view)` is computed from the stable subset (stable_json rules + SHA-256), and that transient fields do not participate.
  - No remaining “conceptual-only” mention without the explicit allow/deny enumeration.
- minimal patch instructions (high level):
  - Insert a subsection named `### Stable-subset hashing filter (allowlist/denylist, v1)` under `### Research integration` → `### Decisions / constraints`.
  - Paste:
    - Excluded transient fields from hashing:
      - processing timestamps and wall-clock fields (e.g. `intent_processing_time_utc`)
      - run ids / session ids / trace ids (e.g. `generation_run_id`, `ui_request_id`)
      - free-form diagnostic strings that do not participate in deterministic semantics
      - non-deterministic model outputs or sampling metadata
    - Stable subset allowlist fields used for `stable_json` / `stable_field_digest`:
      - `intent_kind`
      - `canonical_target`
      - `intent_constraints` (array; sorted lexicographically)
      - `intent_schema_version` (fixed to `IntentPlan_v0` for this v0 handoff)
    - Deterministic stable serialization + digest:
      - `stable_json`: UTF-8 JSON with keys sorted lexicographically and no insignificant whitespace
      - `stable_field_digest := SHA-256(stable_json_bytes)`
  - Add one explicit sentence tying this to the intent-hash wiring (that `intent_hash` preimage uses only `stable_field_digest`, so transient fields cannot drift hashes).

### 3) Roll forward `distilled-core.md` dependency graph to include Phase 2.2.2
- id: `distilled-core-extend-dependency-graph-phase2-2-2`
- risk_level: medium
- target_file: `1-Projects/genesis-mythos-master/Roadmap/distilled-core.md`
- description: Extend the mermaid flowchart under `## Dependency graph` so it includes Phase 2 and at minimum Phase 2.2.2 nodes/edges.
- definition_of_done:
  - The mermaid graph contains a node representing `Phase 2.2.2 — IntentPlan consumption boundary + deterministic verification harness` and has at least one edge from an earlier Phase 2 node to that node.
  - The graph no longer ends solely at Phase 1.1.10.
- minimal patch instructions (high level):
  - Append to the existing `flowchart TD` block nodes/edges:
    - `Phase1 --> Phase2[Phase2]`
    - `Phase2 --> Phase2_2[Phase 2.2 Intent parser integration (generation hooks)]`
    - `Phase2_2 --> Phase2_2_1[Phase 2.2.1 Intent canonicalization + denial taxonomy]`
    - `Phase2_2_1 --> Phase2_2_2[Phase 2.2.2 IntentPlan consumption boundary + deterministic verification harness]`
  - Preserve existing indentation and node naming style.

## Notes for future tuning
1. When executable-grade pseudo-code exists but fixture values are missing, hostile validation stops at delegatability hygiene (not algorithmic correctness).
2. Stable hashing “stable subset” needs explicit enumeration; conceptual descriptions are insufficient.
3. `distilled-core.md` dependency graph must track roadmap-state phase boundaries continuously (Phase 1 → Phase 2 transitions must be represented).
