---
title: Phase 3.1.6 — Tick-scoped observable bundle after ordered apply (replay bridge)
roadmap-level: tertiary
phase-number: 3
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-22
tags: [roadmap, genesis-mythos-master, phase, simulation, determinism, observability, replay]
para-type: Project
subphase-index: "3.1.6"
handoff_readiness: 92
handoff_readiness_scope: "SimObservableBundleTelemetry_v0 + post_apply_observable_root alignment with TickCommitRecord_v0; HR 92 until serialization_profile_id + golden observable hash land"
handoff_gaps:
  - "**`serialization_profile_id`** and facet manifest promotion to **`facet-manifest-v0.md`** still **TBD** — link when **3.1.6** execution row exists in CI policy"
  - "**Appendix A toy hash** in synthesis remains **`TODO`** until repo pins profile + harness — validator **needs_work** residual"
  - "**Merkle vs flat** facet encoding choice deferred to scale review — document chosen sort keys before golden"
execution_handoff_readiness: 69
links:
  - "[[phase-3-1-5-deterministic-agency-slice-outcomes-mutation-ledger-replay-roadmap-2026-03-22-0045]]"
  - "[[phase-3-1-4-deterministic-agency-tick-slices-starvation-guards-roadmap-2026-03-22-0030]]"
  - "[[phase-3-1-1-deterministic-tick-epoch-and-hash-preimage-boundaries-roadmap-2026-03-22-0015]]"
  - "[[phase-3-1-2-deterministic-catch-up-caps-multirate-fairness-roadmap-2026-03-22-0016]]"
  - "[[phase-3-1-3-deterministic-pause-time-scale-sim-clock-coupling-roadmap-2026-03-22-0022]]"
  - "[[phase-3-1-simulation-tick-scheduler-and-time-quanta-roadmap-2026-03-21-2346]]"
  - "[[phase-3-living-simulation-and-dynamic-agency-roadmap-2026-03-19-1101]]"
---

## Phase 3.1.6 — Tick-scoped observable bundle after ordered apply (replay bridge)

**Deliverables:** Vault-normative **post-apply observable barrier**: after **`AgencySliceApplyLedger_v0`** apply completes for a `tick_epoch`, define how **`committed_sim_observable_hash`** (and companion telemetry) is taken so **live/replay** match **3.1.4–3.1.5** order, **CatchUpPolicy_v0** (**D-031**), and **pause** (**3.1.3**) without wall/thread leakage (**D-027**).

> [!warning] Authoritative handoff rule
> **Do not** treat **`handoff_readiness: 92`** as execution green. Use **`execution_handoff_readiness`** and **Tasks** until golden rows assert identical **`post_apply_observable_root`** + **`apply_ledger_checksum`** across drivers.

**Interfaces**

- **`SimObservableBundleTelemetry_v0` (draft):** tick-scoped telemetry pairing `apply_ledger_checksum`, `post_apply_observable_root`, `facet_manifest_id`, `observable_bundle_schema_version`; bumps coordinate with **`replay_row_version`** (**3.1.1**).
- **Barrier rule:** No `TickCommitRecord_v0` emission until **ordered** mutation apply finishes (or explicit carry-forward path for advanced tick + empty ledger per synthesis §7).
- **Facet model:** Allow-listed facets only; **one** authoritative story for RNG counters vs **`rng_counters_slice`** (**3.1.1**).
- **Partial ticks:** Observable bundle must match **truncated** ledger under **3.1.2**; optional `partial_tick_ledger` exposure when diagnostics require it.

### Algorithm sketch (mid-technical)

```text
function commit_tick_observable(world, ledger, control, tick_epoch):
  if control.paused and no_advance:
    return NoCommit  // 3.1.3
  apply_ledger_in_vault_order(world, ledger)  // 3.1.5 + idempotent mutation_id
  bundle = build_allowlisted_facets(world, facet_manifest_id)
  post_root = hash_canonical_bytes(bundle, serialization_profile_id)
  assert post_root == preimage.committed_sim_observable_hash  // TickCommitRecord_v0
  emit SimObservableBundleTelemetry_v0(tick_epoch, ledger_checksum(ledger), post_root, ...)
```

### Desync taxonomy (v0) — observable bundle

| Code | Detect | Surface | Replay outcome |
|------|--------|---------|----------------|
| `OBSERVABLE_PREMATURE_HASH` | hash taken before last intent applied | Audit | Fail-closed |
| `LEDGER_CHECKSUM_MISMATCH` | live vs replay intent serialization differs | CI golden | Fail-closed |
| `FACET_MANIFEST_DRIFT` | facet set differs without schema bump | Validator | Fail-closed |

**Acceptance criteria**

- **`post_apply_observable_root`** equals the bytes wired into **`TickCommitRecord_v0`** preimage for the same `tick_epoch` (**3.1.1** versioning).
- **Empty ledger + advanced tick:** carry-forward re-hash semantics documented and replay-identical (**synthesis §7**).
- **Cross-links:** **3.1.5** (apply order), **3.1.1** (commit record), **D-031** (catch-up parity), **D-032** (header bits when frozen).

## Research integration

### Key takeaways

- Commit **`committed_sim_observable_hash`** only after **ordered** `MutationIntent_v0` apply for the `tick_epoch` (barrier), with live/replay using the same **3.1.4–3.1.5** order and **CatchUpPolicy_v0** (**D-031**).
- Use **`SimObservableBundleTelemetry_v0`** for tick-scoped diagnostics; bump **`observable_bundle_schema_version`** with any facet/serialization/Merkle change; coordinate **`replay_row_version`** (**3.1.1**).
- **Pause (3.1.3):** no advance ⇒ no `TickCommitRecord_v0`. **Advanced tick, empty ledger:** carry-forward observable re-hash (see synthesis §7).
- **Facet manifest** defaults to `1-Projects/genesis-mythos-master/Roadmap/facet-manifest-v0.md` only; link from **3.1.6** when authored.
- **D-027:** no wall/thread/pointer leakage in preimage; web sources in the note are labeled **non-normative**.

### Decisions / constraints

- **Constraint:** Parallel record allowed; **playback** order is **only** vault-visible intent order (**3.1.5** + **D-027**).
- **Constraint:** One authoritative RNG story vs **`rng_counters_slice`** (**3.1.1**).
- **Pending:** Replace Appendix A **`TODO`** hash with harness output when **`serialization_profile_id`** is pinned in repo.

### Links

- [[Ingest/Agent-Research/tick-scoped-observable-bundle-after-mutation-apply-research-2026-03-22-2330|tick-scoped-observable-bundle-after-mutation-apply-research-2026-03-22-2330]]

## Roll-up linkage

Parent secondary **3.1** holds the **### Tertiary roll-up (≥93 closure)** table — this tertiary (**3.1.6**) contributes **HR 92** / **EHR 69** until `post_apply_observable_root` + `apply_ledger_checksum` goldens exist; **no** execution green until those artifacts land per **D-037** and **D-032**.

## apply_ledger_checksum (vault normative v0)

**Input bytes (draft):** canonical serialization of the ordered `MutationIntent_v0` list for one `tick_epoch` after **3.1.5** apply order (include `mutation_id`, `tick_epoch`, `slice_id`, `op_index`, `target_key`, stable `payload_ref` bytes as defined in **3.1.5** — align merge matrix when **D-036** promotes). **Hash:** domain-separated digest (algorithm TBD with **`serialization_profile_id`**); bump **`replay_row_version`** when serialization changes.

**Toy sensitivity (symbolic):** intents `A` then `B` vs `B` then `A` over the same `target_key` must yield **different** `apply_ledger_checksum` unless merge table proves commutativity (**3.1.5**).

> [!warning] Golden row stub (NON-NORMATIVE / WAIVED)
> Field names `post_apply_observable_root` and `apply_ledger_checksum` are **wired for CI** only after **`serialization_profile_id`** + **D-032** header freeze. **TBD** hex values; **do not** treat as green until harness output replaces this callout.

## Tasks

- [ ] **Facet manifest path**
  - [ ] Confirm `Roadmap/facet-manifest-v0.md` with operator per **D-037**
  - [ ] When approved: create stub (allow-list + sort keys); link from this note
- [ ] **`apply_ledger_checksum`**
  - [ ] Lock canonical batch serialization paragraph with **3.1.5** / **D-036**
  - [ ] Replace toy symbolic example with harness hex when repo exists
- [ ] **Golden row**
  - [ ] Add registry row stub under **2.2.3** pattern after **D-032** A/B
  - [ ] Remove waiver callout above when values are non-TBD
- [ ] **Merkle vs flat facets**
  - [ ] Document chosen encoding + sort keys in facet manifest
  - [ ] Bump `observable_bundle_schema_version` when switching shapes
