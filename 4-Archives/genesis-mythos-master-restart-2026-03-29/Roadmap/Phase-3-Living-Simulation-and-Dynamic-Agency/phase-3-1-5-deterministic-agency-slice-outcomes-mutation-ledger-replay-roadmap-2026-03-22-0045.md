---
title: Phase 3.1.5 — Deterministic agency slice outcomes, mutation ledger, and replay-stable apply
roadmap-level: tertiary
phase-number: 3
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-22
tags: [roadmap, genesis-mythos-master, phase, simulation, determinism, agency, mutation, replay]
para-type: Project
subphase-index: "3.1.5"
handoff_readiness: 91
handoff_readiness_scope: "MutationIntent_v0 + ordered apply stream per tick_epoch (normative draft); HR 91 until merge table for overlapping writes + golden intent checksum land"
handoff_gaps:
  - "Per-component **last-writer vs commutative merge** policy matrix still **TBD** (scalar vs structured state channels) — checklist **deferred** per [[decisions-log#D-036|D-036]]"
  - "Golden row for **`mutation_batch_checksum`** / per-slice intent stream waits **D-032** header + **3.1.1** `replay_row_version` coordination — **D-036**"
execution_handoff_readiness: 70
links:
  - "[[phase-3-1-4-deterministic-agency-tick-slices-starvation-guards-roadmap-2026-03-22-0030]]"
  - "[[phase-3-1-3-deterministic-pause-time-scale-sim-clock-coupling-roadmap-2026-03-22-0022]]"
  - "[[phase-3-1-2-deterministic-catch-up-caps-multirate-fairness-roadmap-2026-03-22-0016]]"
  - "[[phase-2-1-5-spawn-commit-idempotent-entity-apply-replay-harness-roadmap-2026-03-19-2035]]"
  - "[[phase-3-1-simulation-tick-scheduler-and-time-quanta-roadmap-2026-03-21-2346]]"
  - "[[phase-3-living-simulation-and-dynamic-agency-roadmap-2026-03-19-1101]]"
---

## Phase 3.1.5 — Deterministic agency slice outcomes, mutation ledger, and replay-stable apply

**Deliverables:** Vault-normative **ordered mutation stream** for one `tick_epoch`: slice outputs become **`MutationIntent_v0`** rows applied in **total order** derived from **3.1.4** `(tick_epoch, slice_index, tie_break_key, op_index)`, with **idempotent** `mutation_id`, explicit **overlap/conflict** policy, and parity with **3.1.2** catch-up truncation and **3.1.3** pause (no apply while paused).

> [!warning] Authoritative handoff rule
> **Do not** treat **`handoff_readiness: 91`** as execution green. Use **`execution_handoff_readiness`** and **Tasks** until replay artifacts assert identical intent streams and merge outcomes across live/replay drivers.

**Interfaces**

- `MutationIntent_v0` (draft): `{ tick_epoch, slice_id, op_index, mutation_id, target_key, payload_ref, expected_version? }` — `target_key` is a vault-defined stable addressing scheme (entity+facet or finer); **no** OS pointers or wall time.
- `AgencySliceApplyLedger_v0` (draft): ordered list of `MutationIntent_v0` for one `tick_epoch`, produced **only** for slices that ran under **3.1.2** substep budget after **3.1.4** schedule.
- **Pause coupling:** When **`SimulationRunControl_v0.paused`** (**3.1.3**), **no** slice execution ⇒ **empty** apply ledger for that instant; resume must not retroactively insert intents for skipped slices.
- **Conflict policy (default):** **stable sort by `mutation_id` then sequential apply**; scalar fields: **last intent in schedule order wins**; non-commutative overlaps emit **`SLICE_STATE_CONFLICT`** (fail-closed) unless a **vault merge table** names an allowed commutative merge.

### Algorithm sketch (mid-technical)

```text
function build_apply_ledger(world, schedule: AgencySliceSchedule_v0, control):
  if control.paused:
    return empty_ledger
  ledger = []
  for slice_id in schedule.slices_in_order:
    intents = produce_mutation_intents(world, slice_id)  // deterministic, bounded by 3.1.2
    for op_index, intent in enumerate(intents):
      ledger.append(MutationIntent_v0(..., op_index, mutation_id = hash(intent_preimage)))
  return AgencySliceApplyLedger_v0(schedule.tick_epoch, ledger)

function apply_ledger(world, ledger, mode):
  seen_ids = set()
  for intent in ledger.ordered_intents:
    if intent.mutation_id in seen_ids:
      continue  // idempotent replay
    if conflicts_with_committed(world, intent):
      return Err(SLICE_STATE_CONFLICT)  // or merge per policy table
    commit_intent(world, intent)
    seen_ids.add(intent.mutation_id)
```

### Desync taxonomy (v0) — slice apply

| Code | Detect | Surface | Replay outcome |
|------|--------|---------|----------------|
| `SLICE_APPLY_ORDER_DIVERGENCE` | intent stream order differs at same `tick_epoch` | CI golden | Fail-closed |
| `CATCHUP_TRUNCATION_MISMATCH` | live truncated slices ≠ replay under **CatchUpPolicy_v0** | Harness | Fail-closed |
| `PAUSE_APPLY_LEAK` | intents committed while `paused` | Audit | Fail-closed |

**Acceptance criteria**

- Every committed state change in a `tick_epoch` is **reachable** by **replaying** the same `AgencySliceApplyLedger_v0` from vault-visible inputs (**D-027**).
- **Cross-links:** **3.1.4** (schedule order), **3.1.2** (budget/truncation), **3.1.3** (pause), **2.1.5** (idempotent spawn/apply harness vocabulary).

## Research integration

### Key takeaways

- **Single commit stream per `tick_epoch`:** Treat slice outputs as **ordered mutation intents**; merge into one stream ordered by `(tick_epoch, slice_index, tie_break_key, op_index)` so live/replay never depend on thread or wall-clock order.
- **Overlapping writes:** Default **stable sort then sequential apply** (last in schedule order wins on scalars); non-commutative read-modify-write conflicts need **vault-defined merge** or **fail-closed** codes (e.g. `SLICE_STATE_CONFLICT`).
- **Idempotent replay:** Attach **`mutation_id`** (or row id) per intent; apply phase ignores duplicates; optional **expected version / preimage** per entity facet to catch divergence early (CQRS/event-sourcing pattern).
- **`CatchUpPolicy_v0`:** Truncation / coalescing must cut the **same** slice set in live and replay; partial ticks only commit intents for slices that **actually ran** under the substep ledger.
- **Pause (`SimulationRunControl_v0`):** No slice run ⇒ no apply ⇒ no `tick_epoch` advance; resume/pause sequencing must match **3.1.3** input latch story.
- **Implementation freedom (D-027):** Parallel **recording** is allowed if **playback** order is **only** the vault total order (analogous to deferred command buffers with explicit sort keys).
- **Replay artifacts:** Extend **D-034** trajectory: golden rows should assert not only **`agency_slice_sequence`** but **per-slice mutation batch / intent checksum** feeding apply.

### Decisions / constraints

- **Adopt** a named apply record (`AgencySliceApplyLedger_v0` / `MutationIntent_v0`) in vault prose before implementation details.
- **Require** deterministic conflict policy: sorted last-writer **or** commutative merge **or** explicit operator/CI failure — no silent merges.
- **Pair** apply semantics with **`replay_row_version`** when mutation envelope or id scheme changes (align with 3.1.1 / D-032 freeze cadence).
- **Pending:** Exact state key granularity (entity+component vs finer channels), and whether multi-slice merges use **functional merge** vs **ordered overwrite** per component family.

### Links

- [[Ingest/Agent-Research/agency-slice-outcomes-deterministic-state-apply-research-2026-03-22-2315|agency-slice-outcomes-deterministic-state-apply-research-2026-03-22-2315]]
- Prior spine: [[phase-3-1-4-deterministic-agency-tick-slices-starvation-guards-roadmap-2026-03-22-0030]], [[phase-3-1-2-deterministic-catch-up-caps-multirate-fairness-roadmap-2026-03-22-0016]], [[phase-3-1-3-deterministic-pause-time-scale-sim-clock-coupling-roadmap-2026-03-22-0022]]

## Tasks

- [x] **Deferred (D-036):** Freeze **`MutationIntent_v0`** preimage fields (including `mutation_id` hash domain) — unblock: **D-032** header + **`replay_row_version`** on **3.1.1**; track in [[decisions-log#D-036|D-036]].
- [x] **Deferred (D-036):** Worked example (**two** slices / overlap) — unblock: merge policy table adoption or operator A/B on conflict semantics.
- [x] **Deferred (D-036):** Stub replay log column **`mutation_batch_checksum`** — unblock: **D-032** A/B header choice; no CI until **3.1.1** `replay_row_version` bump.
