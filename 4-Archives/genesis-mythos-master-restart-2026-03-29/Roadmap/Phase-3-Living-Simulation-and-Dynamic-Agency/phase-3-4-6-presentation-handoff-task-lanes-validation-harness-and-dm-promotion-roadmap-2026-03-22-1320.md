---
title: Phase 3.4.6 — Presentation handoff task lanes, validation harness, DM promotion
roadmap-level: tertiary
phase-number: 3
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-22
tags: [roadmap, genesis-mythos-master, phase, living-world, phase-4, presentation, testing, handoff]
para-type: Project
subphase-index: "3.4.6"
handoff_readiness: 86
handoff_readiness_scope: "Vault-normative execution decomposition after 3.4.5 bridge — separates projection vs live vs golden lanes, sketches PresentationProjectionHarness, and sequences ToolActionQueue_v0 promotion tasks; still < min_handoff_conf 93 until repo goldens + D-032/D-043/D-044 gates clear"
execution_handoff_readiness: 38
lane_a_fixture_id_stub: "GMM-PVS-LANE-A-FIX-STUB-20260322"
handoff_gaps:
  - "Lane-C / ReplayAndVerify rows remain @skipUntil(D-032) / D-043 per 3.4.5 DEFERRED ledger"
  - "DM promotion idempotency + regen same-tick story stays dual-track until D-044 A/B logged"
links:
  - "[[phase-3-4-living-world-operations-and-consequence-fan-out-roadmap-2026-03-23-1210]]"
  - "[[phase-3-4-5-living-world-to-perspective-handoff-bridge-roadmap-2026-03-22-1205]]"
  - "[[phase-3-1-6-tick-scoped-observable-bundle-post-apply-replay-bridge-roadmap-2026-03-22-0047]]"
  - "[[phase-4-perspective-split-and-control-systems-roadmap-2026-03-19-1101]]"
  - "[[decisions-log]]"
  - "[[distilled-core]]"
---

## Phase 3.4.6 — Presentation handoff task lanes, validation harness, DM promotion

**TL;DR:** Close the validator gap **`missing_task_decomposition`** after **3.4.5** by minting a **vault task-ID + DEFERRED-ledger** tertiary: **three test lanes** (read-model projection, live/interactive smoke, golden/replay placeholder), a **`PresentationProjectionHarness`** sketch, and **`ToolActionQueue_v0` → `MutationIntent_v0`** promotion tasks (**T-DM-P01–P05**). **Does not** relax **D-032** / **D-043** / **D-044** gates.

### Objectives

1. Bind every future presentation test to **lane A / B / C** so “looks right” is never confused with **replay preimage**.
2. Provide a **harness outline** that consumes **committed** observables / tick fixtures and asserts **`PresentationViewState_v0`** only where policy allows.
3. Sequence **DM editor** promotion as explicit **staged → validated → promoted_to_intent → ordered** with telemetry hooks.

### Test matrix — lanes (normative for this tertiary)

| Lane | Proves | Hash / preimage | Vault coupling |
| --- | --- | --- | --- |
| **A — Read-model / projection** | `committed_observables → PresentationViewState_v0` deterministic | Lane A may snapshot **canonical JSON** of view state; **must not** mix wall-clock-only fields into replay preimage structs | **3.4.5** field tables + **3.1.6** post-apply bundle |
| **B — Live / interactive** | Render pump does not append **AgencySliceApplyLedger_v0** | **No** `TickCommitRecord_v0` asserts for presentation-only paths | **D-027** (UX vs commit split) |
| **C — Golden / ReplayAndVerify** | End-to-end tick ledger stability | **DEFERRED** until **D-032** / **D-043**; stub **`@skipUntil(D-032)`** | **3.4.5** DEFERRED ledger |

### Task seeds (checklist IDs)

| ID | Intent | Lane | Blocked by |
| --- | --- | --- | --- |
| **T-PR-H01** | Document matrix: observable family × lane × “allowed to assert hash?” | A/B/C | **Satisfied in-vault** — see § Test matrix — lanes + this table |
| **T-PR-H02** | Minimal lane-A test: fixture → read model → expected view (exclude wall-clock fields) | A | fixture policy |
| **T-PR-H03** | Lane-B smoke: no ledger append from render-only code paths | B | dev guard flag |
| **T-PR-H04** | Lane-C placeholder: empty or `@skipUntil(D-032)` | C | **D-032**, **D-043** |
| **T-DM-P01** | State machine: `staged` → `validated` → `promoted_to_intent` → `ordered` | — | **3.1.5** patterns |
| **T-DM-P02** | Idempotency: duplicate `tool_action_idempotency_key` → no second intent | — | registry |
| **T-DM-P03** | Promotion gate checklist: facet scope, DM flag, **D-044** lane note | — | **D-044** |
| **T-DM-P04** | UX: Apply vs Preview — preview never enqueues promotion | — | **3.4.5** classes |
| **T-DM-P05** | Telemetry: queue depth, promotion latency (ticks), rejected reasons | — | observability policy |

### Validation harness sketch (`PresentationProjectionHarness`)

```text
Harness: PresentationProjectionHarness
  Input:  SimObservableBundleFixture (versioned id) OR TickCommitRecordFixture
  Step 1: Validate bundle against facet allow-list (3.4.3 / D-037) — fail closed
  Step 2: Build PresentationViewState_v0 via documented interpolate() / derive path
  Step 3: Serialize view_state to canonical JSON (stable key order) for snapshot compare (lane A only)
  Step 4: Assert excluded-from-preimage fields are NOT present in any replay hash input struct
  Optional: Property test — idempotent replay of same commit → same view (lane A only)
```

## Research integration (external grounding)

- **Full synthesis:** [[Ingest/Agent-Research/phase-3-4-6-presentation-handoff-engineering-harness-dm-research-2026-03-22-1530]]
- **Prior bridge context:** [[Ingest/Agent-Research/phase-3-4-5-sim-presentation-camera-bridge-research-2026-03-22-1245]]
- **Key takeaways:** Separate **projection / live / golden** lanes; treat presentation as **CQRS-style** read model over **post_apply** truth; **ToolActionQueue_v0** promotion mirrors editor **commit boundaries** (Godot `EditorUndoRedoManager` vs runtime `UndoRedo` pattern — **D-027** illustrative only).

### Dependencies

- **D-056** — **3.4.5** bridge contracts authoritative; this tertiary adds **tasks + harness** only.
- **D-044** — same-tick DM / regen / ambient remains **dual-track** until operator logs **RegenLaneTotalOrder_v0** A/B.
- **D-055** — **G-P3.4-*** rollup **PASS** rows **not** reopened.

## Execution / DEFERRED ledger

| Task ID | Status | Owner | Blocker | Unblock condition | Evidence / link |
| --- | --- | --- | --- | --- | --- |
| **T-PR-H01** | **DONE (vault)** | roadmap | — | — | § **Test matrix — lanes** + § **Task seeds** (observable family × lane × hash policy) |
| **T-PR-H02** | **DEFERRED** | eng | **D-032**, repo policy | Lane-A stub JSON + test harness interface in repo | Fixture id **`GMM-PVS-LANE-A-FIX-STUB-20260322`**; § **Lane A fixture anchor** |
| **T-PR-H03** | **DEFERRED** | eng | dev build flag, **D-027** | Runtime or static guard in repo proving render paths skip ledger append | — |
| **T-PR-H04** | **DEFERRED** | eng | **D-032**, **D-043** | `@skipUntil(D-032)` test landed in repo | — |
| **T-DM-P01** | **DEFERRED** | eng | **3.1.5** merge policy text | State machine doc + code | § **Pseudo-code — DM promotion**; **3.4.5** **ToolActionQueue_v0** bounds |
| **T-DM-P02** | **DEFERRED** | eng | **3.1.5**, **3.4.5** idempotency **TBD** | Align duplicate-key semantics with `mutation_id` | [[phase-3-4-5-living-world-to-perspective-handoff-bridge-roadmap-2026-03-22-1205]] bounds row |
| **T-DM-P03** | **DEFERRED** | eng + operator | **D-044** A/B | Operator logs pick in **decisions-log** **D-044** | **D-044** implementation guard sub-bullet (2026-03-22) |
| **T-DM-P04** | **DEFERRED** | eng | UX spec | Apply vs Preview commands in editor | **3.4.5** view-only vs intent classes |
| **T-DM-P05** | **DEFERRED** | eng | observability policy | Metrics schema in repo | — |
| **Goldens / ReplayAndVerify** | **DEFERRED** | eng | **D-032**, **D-043** | Replay header freeze + registry row | **3.4.5** DEFERRED ledger |

## Pseudo-code — DM promotion (staging only)

```text
on_dm_tool_apply(cmd):
  enqueue ToolActionQueue_v0(cmd, state=staged)
  if cmd.mode == preview:
    return  // never promote
  validate(cmd)  // facet scope, capability flags
  promote_to_intent(cmd)  // produces MutationIntent_v0 draft
  order_and_append_to_slice_ledger(intent)  // only after D-044 / 3.2 story satisfied
```
