---
title: Phase 1 (Execution) — Conceptual Foundation and Core Architecture
created: 2026-04-10
tags:
  - roadmap
  - execution
  - godot
  - sandbox-comparand
project-id: godot-genesis-mythos-master
roadmap_track: execution
phase: 1
subphase: "1"
roadmap-level: primary
status: complete
handoff_readiness: 86
handoff_gaps:
  - "Rollup verdicts for GMM-2.4.5-* / CI-seam-expansion remain open until PENDING cells in Execution-Gates packets are filled with attested IDs (packets are structurally complete per handoff-audit-repair-godot-exec-rollup-20260410T105245Z) — execution-deferred; does not block Phase 1 **structural** closure on the execution track."
handoff_audit_last: "2026-04-11T13:05:00Z"
conceptual_counterpart: "[[../../Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-03-30-0430]]"
---

# Phase 1 (Execution) — Conceptual Foundation and Core Architecture

Execution remint anchor for Phase 1 on the parallel spine. Conceptual counterpart: [[../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-03-30-0430]].

## Intent mapping

| Intent target | Inspiration anchors | Execution mechanism | Validation signal |
| --- | --- | --- | --- |
| Runnable vertical foundation with deterministic tick | PMG modularity + layered-game patterns | `IGameLoopKernel` + `IWorldStateStore` seams from this note | AC table + lane comparand rows |
| Godot vs Sandbox parity | Dual-lane Second-Brain policy | Comparand table + deferrals | Hostile validator + execution gate packets |

## Scope

- Implement execution-facing interface seams for the first runnable vertical foundation.
- Define pseudocode skeleton for deterministic tick and handoff boundaries.
- Capture acceptance-criteria tables with lane comparand rows (Godot A vs Sandbox B).
- Keep GMM-2.4.5 and CI closure explicitly deferred to later execution slices.

## Interface seams (execution mint)

| Interface | Owner | Contract | Deferral |
| --- | --- | --- | --- |
| `IGameLoopKernel` | Runtime core | Owns fixed-step tick, pause/resume, and deterministic seed handoff | CI instrumentation coverage deferred |
| `IWorldStateStore` | State layer | Snapshot/apply immutable frame deltas by tick index | GMM-2.4.5 replay diff harness deferred |
| `IEventBus` | Orchestration | Publish ordered domain events with idempotency keys | CI concurrency stress suite deferred |
| `IRenderProjectionBridge` | Presentation seam | Convert sim-visible rows into presentation payloads | Consumer contract closure deferred |

## Pseudocode sketch

```text
function run_tick_window(seed_bundle, tick_budget):
  state = world_store.load(seed_bundle.root_state_id)
  for tick in 1..tick_budget:
    intents = event_bus.collect_intents(tick)
    state = game_loop_kernel.step(state, intents, seed_bundle)
    projection = render_bridge.project(state, tick)
    event_bus.publish_projection(projection, tick)
  world_store.persist(state, seed_bundle.session_id)
  return state
```

## Acceptance criteria (execution-first)

| ID | Criterion | Evidence target | Status |
| --- | --- | --- | --- |
| AC-1.1-A | Tick loop remains deterministic across two replay runs with same seed bundle | Matching state hash at final tick | Evidence-backed (provisional) |
| AC-1.1-B | World-state deltas persist and restore at checkpoint boundary | Restore succeeds without ordering drift | Planned |
| AC-1.1-C | Event bus preserves causal ordering through projection handoff | Ordered event trace with no inversion | Planned |
| AC-1.1-D | Presentation bridge emits schema-conformant rows for each tick | Row schema validation + sample replay | Planned |

## Lane comparand rows

| Row | Lane A (Godot) | Lane B (Sandbox) | Common contract |
| --- | --- | --- | --- |
| Runtime tick primitive | `_physics_process` bounded-step orchestration | C++ fixed-step scheduler loop | Stable tick budget and deterministic ordering |
| Event dispatch seam | Signal/event-channel envelope | Typed queue + dispatcher | Ordered publish/apply boundary |
| Projection surface | Node/scene-bound presentation payload | Renderer-agnostic data packet | Sim-visible projection schema |
| Replay verification | Seeded replay path + frame checkpoints | Seeded replay with state digest | Equivalent replay hash contract |

## Explicit deferrals

- `GMM-2.4.5-*` comparator and lineage closure rows are execution-deferred in this mint.
- CI seam expansion (cross-lane stress, long-run replay matrix, report automation) is deferred.
- These deferrals are intentional and tracked for downstream execution slices, not conceptual rewrites.

## Roll-up closure map (execution gate reconciliation)

| Gate ID | Owner | Artifact target | Completion check | Current state |
| --- | --- | --- | --- | --- |
| `GMM-2.4.5-replay-diff` | Runtime + state | `3-Resources/Second-Brain/Validator-Reports/Execution-Gates/godot-phase1-gmm-245-replay-diff.md` | Two-run final hash equivalence with seed lineage annotation | Open — **structured packet** (`evidence_packet_status: structured_open`); verdict rows `PENDING` until CI hashes |
| `GMM-2.4.5-lineage-closure` | Architecture | `3-Resources/Second-Brain/Validator-Reports/Execution-Gates/godot-phase1-gmm-245-lineage-closure.md` | Comparator rows resolved with explicit pass/fail marks | Open — **structured packet**; statuses `PENDING` until registry milestones |
| `CI-seam-expansion` | CI + runtime | `3-Resources/Second-Brain/Validator-Reports/Execution-Gates/godot-phase1-ci-seam-expansion.md` | Cross-lane stress, long-run replay, and report automation run IDs recorded | Open — **structured packet**; `ci_run_id` cells `PENDING` (no fabrication) |

Execution gate deferment remains active until the listed completion checks are met and linked.

## Handoff-audit reconciliation (2026-04-10)

Repair queue `repair-handoff-audit-godot-exec-phase1-rollup-20260410T210700Z` **does not close** L1 `missing_roll_up_gates`; it binds the closure map to **on-disk stub packets** (see `3-Resources/Second-Brain/Validator-Reports/Execution-Gates/`) plus owner accountability until real verdict rows exist.

**2026-04-11 — `handoff-audit-repair-godot-exec-rollup-20260410T105245Z`:** Upgraded **replay-diff**, **lineage-closure**, and **CI-seam-expansion** packets from bare stubs to **structured_open** evidence (protocol, matrices, hostile-validation checklists; `PENDING` where IDs are not yet attested). **`missing_roll_up_gates`** remains an advisory open code until real CI/registry rows populate — this pass closes **packet-shape** gaps for hostile replay, not rollup verdict.

| Gate ID | Evidence packet status | Blocking condition before rollup verdict closure | Owner note |
| --- | --- | --- | --- |
| `GMM-2.4.5-replay-diff` | Structured packet (`structured_open`); matrix cells `PENDING` until CI hashes | Populate Run A/B `final_state_hash` + `ci_run_id` per packet protocol | Runtime + state |
| `GMM-2.4.5-lineage-closure` | Structured packet; verdict rows `PENDING` | Fill `engine_build_id` / `parent_commit` when attested | Architecture |
| `CI-seam-expansion` | Structured stress matrix; all `ci_run_id` cells `PENDING` | Attach real stress / long-run / report-automation run IDs | CI + runtime |

Execution deepen along [[../../workflow_state-execution]] — **primary glue slice (this note)**: safety invariants + dry-run hooks are bound to **1.2.5** manifest/versioning interfaces; rollup **`missing_roll_up_gates`** / CI / registry IDs remain **execution-deferred** per **D-Exec-rollup-deferral** (no fabricated `ci_run_id`).

### AC-1.1-A evidence

Canonical record (including placeholder digests pending CI attestation): [[3-Resources/Second-Brain/Validator-Reports/Execution-Gates/godot-phase1-ac-1-1-a-determinism-check|godot-phase1-ac-1-1-a-determinism-check]]. Evidence-backed scope is **provisional** stub parity only; CI seam expansion remains open per roll-up closure map.

## Safety invariants (primary glue — execution)

Cross-walk to the conceptual Phase 1 primary checklist: invariants are **lane-neutral**; Godot/Sandbox rows below cite **where** each invariant is enforced without claiming rollup closure.

| Invariant ID | Statement | Primary enforcement surface | Godot lane anchor | Sandbox lane anchor |
| --- | --- | --- | --- | --- |
| SI-P1-01 | **No silent graph load** — interchange bytes must pass schema/version gate before host mutation | Pre-run validation seam ahead of world/store commit | Same ordering as **1.2.5** pre-run validation + `JSON` parse failure surface ([docs](https://docs.godotengine.org/en/stable/classes/class_json.html)) | Parse/validate failure → no C++ graph host mutation |
| SI-P1-02 | **Deterministic identity** — `graph_schema_version` + interchange manifest hash must agree with [[../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-5-Graph-Versioning-Interchange-Manifests-and-Pre-Run-Validation-Roadmap-2026-04-12-0215|1.2.5 execution]] tables before `ResourceLoader` load path is honored | Version tuple + manifest record in workflow tick ledger | Load path gated after validation ([ResourceLoader](https://docs.godotengine.org/en/stable/classes/class_resourceloader.html)) | Resource-equivalent load seam after validation |
| SI-P1-03 | **Dry-run supremacy** — when `dry_run=true`, host must not publish tick `n` state commits or side effects; may emit validation transcript only | Kernel + store + bus (see hooks) | Editor/tooling detection stays advisory only; no new GDScript API shapes committed here without Research | Compile-time / mock store dry path |
| SI-P1-04 | **Failure taxonomy** — validation vs load vs replay failures stay in distinct buckets (aligns with 1.1.4 error boundaries) | `push_error` / `push_warning` policy from [[../Phase-1-1-Layering-and-Interface-Contracts/Phase-1-1-4-Error-Boundaries-and-Failure-Propagation-Roadmap-2026-04-11-2105|1.1.4 execution]] | Godot signal/error surface | Sandbox exception / log surface |

> Rollup / HR / registry **closure IDs** remain **out of scope** for this slice (**D-Exec-rollup-deferral-missing-roll-up-gates-20260411**).

## Dry-run validation hooks (bound to 1.2.5 manifest/versioning)

**Binding:** Canonical manifest + schema/version fields are defined on [[../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-2-Procedural-Generation-Graph-Skeleton/Phase-1-2-5-Graph-Versioning-Interchange-Manifests-and-Pre-Run-Validation-Roadmap-2026-04-12-0215|Phase 1.2.5 execution (graph versioning / interchange / pre-run validation)]]. This primary slice **does not duplicate** that note; it wires **hook contracts** into Phase 1 primary seams.

| Hook ID | Trigger | Inputs (from 1.2.5) | Output transcript | Must not (dry-run) |
| --- | --- | --- | --- | --- |
| DH-P1-01 | Pre-load | Interchange manifest JSON + declared `graph_schema_version` | Parsed manifest record + semver compatibility verdict | Mutate `IWorldStateStore` |
| DH-P1-02 | Pre-tick | Seed bundle + manifest hash from 1.2.4/1.2.5 linkage | Deterministic replay fingerprint (tick 0 snapshot) | Publish `event_bus` side effects |
| DH-P1-03 | Host selection | `ResourceLoader` load path candidate | Success/failure + loader error bucket | Commit presentation projection rows |

**Interface IDs (glue-only):** `IGraphInterchangeManifest` (parse/validate), `IGraphSchemaCompatibility` (semver tuple check vs kernel), `IDryRunTranscriptSink` (append-only validation record) — names are **contracts** for downstream mints; no new GDScript signatures are asserted here.

## Next structural intent

> Primary **glue** slice for Phase 1 execution is recorded above. Authoritative automation cursor: [[../../workflow_state-execution]] — after this run, execution track advances to **Phase 2 / `"2"`** for the next parallel-spine mint. Rollup **`missing_roll_up_gates`** remains advisory until attested CI/registry IDs exist.
