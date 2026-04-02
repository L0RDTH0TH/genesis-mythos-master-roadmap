---
title: Phase 3.4.3 — Living world facet manifest, catch-up deferral, and replay parity
roadmap-level: tertiary
phase-number: 3
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-23
tags: [roadmap, genesis-mythos-master, phase, living-world, facet-manifest, catch-up, replay-parity]
para-type: Project
subphase-index: "3.4.3"
handoff_readiness: 85
execution_handoff_readiness: 44
handoff_readiness_scope: vault-normative draft — facet allow-list + serialization_profile coupling to post_apply_observable_root; idempotent catch-up deferral; D-044 provisional only
handoff_gaps:
  - "`facet_manifest_id` + `serialization_profile_id` literal freeze blocked on D-037 operator confirm + D-032/D-043"
  - "`CATCHUP_BUDGET_DEFERRAL` (or chosen code) must be registered in 3.1.2 taxonomy before CI asserts"
  - "Normative single same-tick regen vs ambient interleaving remains HOLD until D-044 A/B logged"
links:
  - "[[phase-3-4-living-world-operations-and-consequence-fan-out-roadmap-2026-03-23-1210]]"
  - "[[phase-3-4-2-living-world-consequence-fan-out-and-ordered-projection-roadmap-2026-03-23-1805]]"
  - "[[phase-3-1-2-deterministic-catch-up-caps-multirate-fairness-roadmap-2026-03-22-0016]]"
  - "[[phase-3-1-6-tick-scoped-observable-bundle-post-apply-replay-bridge-roadmap-2026-03-22-0047]]"
  - "[[phase-3-2-3-regen-ledger-replay-rows-and-tick-commit-coupling-roadmap-2026-03-22-1748]]"
  - "[[Ingest/Agent-Research/phase-3-4-3-living-world-facet-catchup-research-2026-03-23.md]]"
  - "[[distilled-core]]"
  - "[[decisions-log]]"
---

## Phase 3.4.3 — Living world facet manifest, catch-up deferral, and replay parity

> **Architect:** **3.4.2** fixed the *ordered projection chain*; **3.4.3** pins *which hashed surfaces exist* and what happens when **catch-up budget** would force silent reorder — **never** reorder inside a tick; **defer idempotently** and **carry** via new schedule rows.

### TL;DR

- **Facet manifest:** Ambient **`MutationIntent_v0`** rows declare **`affected_facet_ids`** ⊆ closed **`facet_manifest_id`** allow-list paired with **`serialization_profile_id`** (**D-037**). Bump **`observable_bundle_schema_version`** + coordinate **`replay_row_version`** when manifest or encoding changes.
- **Catch-up failure closure:** When **`CatchUpPolicy_v0`** budget would be exceeded, append an **idempotent** deferral record (`mutation_id` / `deferral_key`, reason e.g. **`CATCHUP_BUDGET_DEFERRAL`**) and **schedule carry-forward** — **no** in-tick reorder of `AgencySliceApplyLedger_v0` (**D-031** live/replay parity).
- **`partial_tick_ledger`:** Observable root and tick commit digest reflect **only** intents that actually applied this tick (deferral audit facets optional if manifest-listed).
- **Regen vs ambient:** **Provisional dual narratives** until **D-044** **RegenLaneTotalOrder_v0** A/B is logged; **`StableMergeKey_v0`** remains **post-regen** (**3.2.3**).

## Algorithm sketch (pseudocode)

```text
on_tick_close(tick_epoch):
  ledger = AgencySliceApplyLedger_v0.for_tick(tick_epoch)
  budget = CatchUpPolicy_v0.remaining_budget(tick_epoch)
  for intent in ledger.ordered_mutation_intents():
    if not budget.allows(intent.estimated_cost):
      ledger.append_deferral_intent(
        deferral_key = stable_id(intent, tick_epoch),
        reason = CATCHUP_BUDGET_DEFERRAL,
        carry_forward_schedule_ref = next_tick_slice_ref(intent.slice_class)
      )
      continue
    assert intent.affected_facet_ids subset facet_manifest.allow_list
    apply_mutation_intent(intent)
    budget.consume(intent.estimated_cost)
  bundle = build_SimObservableBundleTelemetry_v0(post_apply_state, facet_manifest, serialization_profile_id)
  publish TickCommitRecord_v0(..., partial_tick_ledger_digest = ledger.commit_digest())
```

## Tasks

- [ ] Draft **`facet_manifest_v0`** row table (facet id, preimage field list, commutative vs ordered-merge) — **do not** mint vault file until operator confirms (**D-037**).
- [ ] Cross-link **`CATCHUP_BUDGET_DEFERRAL`** to **3.1.2** reason taxonomy + **D-031** replay-driver parity checklist.
- [ ] Maintain **two** labeled provisional paragraphs for **regen_apply_sequence** vs dependent ambient scalars (**D-044**); delete dual narrative when A/B logged.

### Task ledger (DEFERRED / BLOCKED)

| Task | WAITING_ON | Notes |
| --- | --- | --- |
| Manifest file path | **D-037** / operator | Provisional path intent only until confirm |
| Golden deferral row | **D-032** / **D-043** | Pseudocode-only in vault |
| Single interleaving story | **D-044** A/B | HOLD — normative text forbidden until logged |

## Research integration

- **Facet manifest ↔ `post_apply_observable_root` (D-037):** Bind **`facet_manifest_id`** to a closed allow-list of observable facets ambient slices may affect; pair with **`serialization_profile_id`** for canonical bytes (width, map order, encoding). Bump **`observable_bundle_schema_version`** + coordinate **`replay_row_version`** when the allow-list or encoding changes. Ambient **`MutationIntent_v0`** rows should declare **`affected_facet_ids`** ⊆ manifest.
- **Catch-up failure closure (D-031 / 3.1.2):** When ambient fan-out would exceed **`CatchUpPolicy_v0`** budget, **fail closed** by appending an **idempotent** deferral record (stable **`mutation_id`** / **`deferral_key`**, reason e.g. **`CATCHUP_BUDGET_DEFERRAL`**) and **carrying** work via **new** schedule rows — **never** reorder the current tick’s total order. **`post_apply_observable_root`** reflects **only** intents that actually applied (including deferral audit facets if listed).
- **Replay parity:** Live and replay must share **identical** policy bits and budget accounting (**D-031**); **`partial_tick_ledger`** stays consistent with truncated apply + observable root.
- **Regen vs ambient (D-044):** **Provisional only** — do **not** assert one normative same-tick interleaving until **RegenLaneTotalOrder_v0** A/B is logged in [[decisions-log]]; keep **two** labeled provisional narratives. **`StableMergeKey_v0`** remains **post-regen**; tick commit digests must include **final** regen sequence when regen ran (**3.2.3**).

**Decisions / constraints**

- Mint **`facet-manifest-v0.md`** only after operator confirmation (**D-037**).
- Literal golden / registry rows remain blocked per **D-032** / **D-043** until header + `replay_row_version` freeze.
- Normative single interleaving for regen vs dependent ambient scalars **HOLD** until **D-044** A/B.

**Links**

- Synthesis: [[Ingest/Agent-Research/phase-3-4-3-living-world-facet-catchup-research-2026-03-23.md]]
- Prior chain: [[phase-3-4-2-living-world-consequence-fan-out-and-ordered-projection-roadmap-2026-03-23-1805]], [[Ingest/Agent-Research/phase-3-4-2-living-world-consequence-fan-out-research-2026-03-23.md]]

### Cited takeaways

1. **Manifest enforcement** prevents “surprise” observable preimage drift when ambient slices add fields.
2. **Deferral intents** preserve total order while avoiding catch-up wall violations.
3. **Replay** must budget-account the same way as live — no hidden catch-up paths.

## Risk register (v0)

| Risk | Signal | Mitigation | Owner |
| --- | --- | --- | --- |
| Silent facet growth | New ambient field without manifest bump | CI / review gate on `affected_facet_ids` | Eng |
| Deferral spam | Infinite carry-forward loops | Cap deferral depth + starvation credit (**3.1.4**) | Eng |
| Regen ambiguity | Single story before D-044 | Keep dual provisional + decisions-log HOLD | Operator |
