---
title: Phase 3.4.3 — Living-world facet manifest, catch-up failure closure, regen vs ambient (research)
created: 2026-03-23
tags: [research, agent-research, genesis-mythos-master, phase-3-4-3, living-world, observables, catch-up, D-037, D-031, D-044]
project-id: genesis-mythos-master
linked_phase: Phase-3-4-3
research_query: "Facet manifest + serialization_profile ↔ post_apply_observable_root; failure-closed catch-up when ambient fan-out exceeds CatchUpPolicy_v0 budget; regen vs ambient ordering (D-044 provisional)"
research_tools_used: [vault_context, web_search]
research_escalations_used: 0
agent-generated: true
source: vault-first synthesis for roadmap deepen (nested Research helper)
para-type: Resource
status: draft
parent_context:
  queue_entry_id: resume-roadmap-genesis-mythos-master-20260323-deepen-suggested-252
  parent_run_id: pr-qeat-20260323-resume-gmm-252
links:
  - "[[phase-3-4-2-living-world-consequence-fan-out-and-ordered-projection-roadmap-2026-03-23-1805]]"
  - "[[phase-3-1-6-tick-scoped-observable-bundle-post-apply-replay-bridge-roadmap-2026-03-22-0047]]"
  - "[[phase-3-1-2-deterministic-catch-up-caps-multirate-fairness-roadmap-2026-03-22-0016]]"
  - "[[phase-3-2-3-regen-ledger-replay-rows-and-tick-commit-coupling-roadmap-2026-03-22-1748]]"
  - "[[decisions-log]]"
  - "[[distilled-core]]"
---

# Phase 3.4.3 — Facet manifest coupling, catch-up failure closure, regen vs ambient

**Scope:** Tertiary **3.4.3** (after **3.4.2** ordered projection) — close three deferred threads from [[phase-3-4-2-living-world-consequence-fan-out-and-ordered-projection-roadmap-2026-03-23-1805]]: (1) **facet allow-list** ↔ **`serialization_profile_id`** ↔ **`post_apply_observable_root`** (**D-037**), (2) **failure-closed** behavior when **ambient fan-out** would exceed **3.1.2** catch-up budget (**D-031**), (3) **regen vs ambient** ordering reminders with **D-044** explicitly **provisional** only.

**Do not duplicate:** The binding chain ledger → observable barrier → `TickCommitRecord_v0`, `SimObservableBundleTelemetry_v0` field table (**4b** in prior research), and **3.4.2** pseudocode loop are already in vault; this note adds **manifest/catch-up/deferral** mechanics and **cross-links**, not a second definition of total order.

---

## 1. Facet manifest + `serialization_profile_id` ↔ `post_apply_observable_root` (D-037)

**Vault anchors:** **D-037** adopts **3.1.6** as normative draft for **`post_apply_observable_root`** alignment with **`TickCommitRecord_v0.committed_sim_observable_hash`**, with **`serialization_profile_id`**, **`facet-manifest-v0.md`**, and harness hash **TBD** until repo policy (**D-027**). Provisional path intent: `1-Projects/genesis-mythos-master/Roadmap/facet-manifest-v0.md` — **do not mint** until operator confirms (per decisions-log).

**Design coupling for 3.4.3 (living world):**

| Concern | Role |
|--------|------|
| **`facet_manifest_id`** (telemetry) | Names the **closed set** of observable facets that may appear in the tick’s post-apply preimage (NPC crowd summaries, weather scalars, faction posture bits, etc.). Ambient slices that emit **`MutationIntent_v0`** must declare which **facet ids** their successful apply can touch. |
| **`serialization_profile_id`** | Pins **endianness, fixed widths, map key order, string encoding** for every facet row in the Merkle / sorted preimage (**3.1.6** research §3–4b). **Living-world** facets that are **not** in the manifest must **not** influence `post_apply_observable_root` (fail closed or route through explicit manifest bump). |
| **Deterministic replay** | Replay rebuilds the **same** partial ledger (**D-031** parity), applies in **same** order, then hashes **only** manifest-listed facets with **same** profile — otherwise `committed_sim_observable_hash` diverges. |

**Acceptance-style checks (vault-normative, not CI until D-032/D-043):**

1. Every **ambient** `MutationIntent_v0` row carries **`affected_facet_ids: []`** (or equivalent) ⊆ manifest allow-list for the active **`facet_manifest_id`**.
2. **`observable_bundle_schema_version`** bumps when the allow-list or encoding rules change; **`replay_row_version`** coordinated on **3.1.1** per **D-037** / **3.1.6** bump rules.
3. **`partial_tick_ledger: true`** (when exposed) implies the observable root is still **post-apply for that truncated ledger** — manifest must be consistent with **partial** apply, not a hypothetical full fan-out.

---

## 2. Failure-closed catch-up when ambient fan-out exceeds budget (D-031, 3.1.2)

**Vault anchors:** **`CatchUpPolicy_v0`** (`max_steps_per_frame`, `frame_dt_clamp_max_ms`, `on_budget_exceeded`: `SLOW_SIMULATION` | `DROP_SUBSTEPS` | `COALESCE_INPUTS`) — live and replay must implement **identical** semantics (**D-031**). **3.4.2** task: defer via **idempotent ledger row**; **never reorder** schedule.

**Problem:** Ambient consequence fan-out can aspire to **more** `MutationIntent_v0` rows in one `tick_epoch` than **3.1.2** allows **substeps** or **slice budget** to execute. **Failure-closed** means: do **not** silently drop unordered work or fork hidden threads; **record** deferral in the **authoritative** stream.

**Event-sourcing style pattern (map to vault types):**

1. **Budget probe (deterministic):** Before or during ordered apply, if the **remaining** catch-up / within-tick budget cannot apply the **next** scheduled ambient row, **do not** apply it this tick.
2. **Idempotent deferral record:** Append a **`MutationIntent_v0`** (or dedicated **`AmbientDeferralIntent_v0`** row folded into the same ledger ordering rules) that:
   - References **`deferred_from_slice_id`**, **`mutation_id`** (or stable **`deferral_key`**) idempotent on replay,
   - Carries **`reason_code: CATCHUP_BUDGET_DEFERRAL`** (or reuse taxonomy extension under **3.1.2** desync table),
   - **Does not** mutate gameplay state except **enqueue** the same logical work as a **future** `AgencySliceSchedule_v0` row (next tick or explicit **carry** structure).
3. **Schedule immutability:** The **original** `AgencySliceSchedule_v0` total order for the tick is **not** re-sorted; deferred work appears as **new** rows in a **later** tick, keyed so replay reproduces the **same** deferral decision given the same policy bits (**D-031**).
4. **Observable barrier:** `post_apply_observable_root` runs **after** only the intents that **actually** applied this tick — including deferral records that **commit** to observable/audit facets if those facets are manifest-listed.

**Pseudocode sketch (normative direction, not golden):**

```text
on_tick_apply(tick_epoch, policy: CatchUpPolicy_v0, schedule, budget):
  ledger = empty_ordered_intents()
  for row in schedule.rows_in_total_order():
    if budget.exhausted():
      ledger.append(deferral_intent(row, reason=CATCHUP_BUDGET_DEFERRAL, idempotent_key=stable(row)))
      continue
    if row.is_ambient_fan_out() and not budget.fits(row.estimated_substeps):
      ledger.append(deferral_intent(row, ...))
      schedule.enqueue_carry_forward(row, next_tick_epoch + carry_rule)
      continue
    ledger.append(row.to_mutation_intents()...)
    budget.consume(row.estimated_substeps)
  apply_ordered(ledger)  // 3.1.5
  bundle = build_SimObservableBundleTelemetry_v0(..., partial_tick_ledger=budget.truncated)
  assert post_apply_observable_root(bundle) aligns TickCommitRecord_v0...
```

**Replay obligation:** The **same** `CatchUpPolicy_v0` bits and **same** budget accounting must run on replay; otherwise **CATCHUP_POLICY_DIVERGENCE** (**3.1.2** table) applies.

[Source: Stack Overflow — aggregate versioning / idempotent command handling in event-sourced flows](https://stackoverflow.com/questions/37247231/using-aggregate-version-numbers-to-be-idempotent-when-using-event-sourcing) — **non-normative** analogy for **idempotent deferral** under retries/replay.

[Source: Stack Overflow — deterministic replay ordering in CQRS / event sourcing](https://stackoverflow.com/questions/60050722/how-to-replay-in-a-deterministic-way-in-cqrs-event-sourcing) — **non-normative** reinforcement of **single authoritative order**.

---

## 3. Regen vs ambient ordering — **provisional only** (D-044)

**Vault state:** **D-044** **RegenLaneTotalOrder_v0** Option **A** (multi-regen tuple order) vs **B** (≤1 regen/tick) is **not** logged in [[decisions-log]] as of **D-044** traceability note (**2026-03-23**). **3.4.1** / **3.4.2** allow **provisional** narrative: topology-dependent ambient scalars **after** `regen_apply_sequence` **until** A/B is pinned.

**Reminders for 3.4.3 authoring:**

- **Do not** assert a **single** normative same-tick interleaving in new text; label alternatives **Provisional A** / **Provisional B** and point to **D-044**.
- **`StableMergeKey_v0`** remains **post-regen** for player/DM merge buffers — **not** a substitute for regen lane (**3.2.3**).
- **`TickCommitRecord_v0`** preimage must include **final** regen digest when regen ran (**3.2.3**); ambient scalars that assume regen layout must not **commit** ahead of that sequence under the **provisional** ordering story.

---

## 4. Cross-phase checklist (for the new 3.4.3 roadmap note)

1. [ ] Define **facet-manifest** rows for **ambient-observable** fields (link **`facet_manifest_id`** + **`serialization_profile_id`** to **D-037** / **D-032** / **D-043** gates).
2. [ ] Document **CATCHUP_BUDGET_DEFERRAL** (or chosen code) + **idempotent** `mutation_id` / `deferral_key` pattern; explicit **no schedule reorder** rule.
3. [ ] Cross-link **partial_tick_ledger** + **CatchUpPolicy_v0** parity (**D-031**) in acceptance language.
4. [ ] **Regen ↔ ambient** section: **two** labeled provisional narratives only; **HOLD** normative merge until **D-044** A/B logged.

---

## Sources

- Vault: [[decisions-log]] (**D-031**, **D-037**, **D-044**, **D-053**), [[phase-3-4-2-living-world-consequence-fan-out-and-ordered-projection-roadmap-2026-03-23-1805]], [[phase-3-1-6-tick-scoped-observable-bundle-post-apply-replay-bridge-roadmap-2026-03-22-0047]], [[Ingest/Agent-Research/tick-scoped-observable-bundle-after-mutation-apply-research-2026-03-22-2330]], [[phase-3-1-2-deterministic-catch-up-caps-multirate-fairness-roadmap-2026-03-22-0016]]
- External (non-normative): [Stack Overflow — idempotent commands / aggregate replay](https://stackoverflow.com/questions/37247231/using-aggregate-version-numbers-to-be-idempotent-when-using-event-sourcing), [Stack Overflow — deterministic CQRS replay](https://stackoverflow.com/questions/60050722/how-to-replay-in-a-deterministic-way-in-cqrs-event-sourcing)

## Raw sources (vault)

- No separate raw note; synthesis is vault-grounded with light external citations above.
