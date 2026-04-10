---
title: Phase 1.1.1 (Execution) — Layer boundary and commit pipeline
created: 2026-04-10
tags:
  - roadmap
  - execution
  - sandbox
  - layering
  - commit-pipeline
project-id: sandbox-genesis-mythos-master
roadmap_track: execution
roadmap-level: tertiary
phase-number: 1
subphase-index: "1.1.1"
status: in-progress
handoff_readiness: 86
handoff_readiness_basis: design_traceability_pre_evidence
handoff_readiness_note: "Score reflects NL alignment, seams, and traceability to conceptual/parent execution notes; not evidence closure while all AC rows remain Planned."
conceptual_counterpart: "[[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layering-and-Interface-Contracts/Phase-1-1-1-Layer-Boundary-and-Commit-Pipeline-Roadmap-2026-03-30-0431]]"
---

# Phase 1.1.1 (Execution) — Layer boundary and commit pipeline

Execution tertiary **1.1.1** on the **parallel spine** under `Phase-1-1-Layering-and-Interface-Contracts/`, aligned to conceptual [[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layering-and-Interface-Contracts/Phase-1-1-1-Layer-Boundary-and-Commit-Pipeline-Roadmap-2026-03-30-0431]]. Focus: **single-committer semantics**, **tick-shaped staging** of mutations, and **render-after-commit** ordering — extending the secondary **1.1** boundary matrix with explicit **commit pipeline** mechanics and evidence hooks. **GMM-2.4.5** lineage/compare harnesses and **CI closure** remain **explicitly deferred** unless evidenced later.

Parent execution secondary: [[Phase-1-1-Layering-and-Interface-Contracts-Roadmap-2026-04-10-2205]] · Phase 1 execution primary: [[../Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-04-10-2100]]

## Handoff readiness vs evidence

**Handoff readiness** on this slice is **design- and traceability-first**: conceptual alignment, boundary/commit seams, and intent mapping. It does **not** claim execution evidence until at least one AC row advances beyond **Planned**. **`status: in-progress`** here means this tertiary’s spec and hooks are not closed out in-repo; it does **not** mean the automation cursor is still on `1.1.1` — see [[../../workflow_state-execution]] (`current_subphase_index` points at the **next** deepen target).

## Slice status vs execution cursor

- This note is the **1.1.1** execution spec slice (commit pipeline).
- **`workflow_state-execution`** **`current_subphase_index: 1.1.2`** is the **next** structural deepen step after this mint; the cursor has already advanced past 1.1.1 in automation state.

## Alignment to conceptual Phase-1-1-1

| Conceptual contract | Execution mechanism (this note) | Validation signal |
| --- | --- | --- |
| Single tick: intents → staged delta → world commit → render post-commit | `tick_commit_pipeline` pseudocode + seam ordering table | AC-1.1.1.E1–E4 |
| Simulation holds ephemeral state only until commit | `simulation_scratch` vs `committed_view` separation in seams | AC-1.1.1.E2 |
| Render reads from last committed snapshot + version token | `ReadViewModel` after `version` bump; no backdoor write | AC-1.1.1.E3 |
| Atomic batch rejection on invariant violation | `commit_batch` all-or-nothing default | AC-1.1.1.E1 |

## Commit pipeline (execution seam)

**Ordering (hard):** `ingress_validate_shape` → `simulation.stage(intents, world.read())` → `world.commit(staged, validate=hard)` → `dispatch.publish_projections(version)` → `presentation.consume(version)` — matches conceptual **single committer**; simulation **never** writes authoritative fields.

```text
pipeline tick_commit(tick_id):
  intents = ingress.drain_ordered(tick_id)
  pre_version = world.version_token()
  staged = simulation.propose_staged_delta(intents, world.read_consistent(pre_version))
  commit = world.commit_staged(staged, tick_id)   # sole authority
  if commit.status == rejected:
    simulation.discard_ephemeral()
    return CommitResult(rejected, commit.reason)
  dispatch.emit_after_commit(commit.projection_envelope, commit.version)
  presentation.attach_read_model(commit.version)
  return CommitResult(accepted, commit.version)
```

## Boundary matrix (tertiary tightening)

| Seam | Upstream | Downstream | Forbidden |
| --- | --- | --- | --- |
| Simulation → World | `StagedDelta` | `CommitReceipt` | Direct field mutation on world store |
| World → Dispatch | `post_commit` envelope + version | Scheduler tick merge | Dispatch reading pre-commit staging buffers |
| World → Presentation | `ReadViewModel(version)` | Render packet | Presentation calling `commit` |
| Ingress → Simulation | `IntentEnvelope` (shape-valid) | Staging only | Authorization bypass |

## Acceptance criteria — evidence hooks

| ID | Criterion | Evidence artifact (planned) | Status |
| --- | --- | --- | --- |
| AC-1.1.1.E1 | Commit rejects full batch on any invariant failure; version unchanged on reject | `commit_attempt.jsonl` (tick, pre_v, post_v, status) | Planned |
| AC-1.1.1.E2 | Ephemeral simulation buffers cleared or rolled back on reject | `ephemeral_rollback.log` | Planned |
| AC-1.1.1.E3 | Presentation packet schema id tied to `commit.version` | `render_packet_schema.tsv` | Planned |
| AC-1.1.1.E4 | Deterministic replay: same intents + same world read → same commit digest (sandbox) | `replay_digest_compare.txt` (deferred harness; same deferral as GMM-2.4.5) | Planned |

## Intent Mapping

| Design intent target | Inspiration anchors | Execution mechanism | Validation signal |
| --- | --- | --- | --- |
| Layer boundary + commit pipeline NL | Conceptual 1.1.1 behavior + secondary 1.1 matrix (**vault-only** — no external URL anchor in this slice) | `tick_commit` + seam table | AC-1.1.1.E1–E3 |
| Render cadence vs simulation | Conceptual “render faster than sim” | `presentation.attach_read_model(version)` only; stale detection via version | AC-1.1.1.E3 |
| Atomic batch semantics | Conceptual partial-failure default | `commit_staged` all-or-nothing | AC-1.1.1.E1 |

## Risks (v0)

| Risk | Mitigation | Linked AC |
| --- | --- | --- |
| Hidden world side-channel in replay | Document channel list; flag as **open** until depth-4 | AC-1.1.1.E4 |
| Soft vs hard validation policy | Default hard-only in pipeline; DM policy out of scope | AC-1.1.1.E1 |
| Scope creep into GMM-2.4.5 / CI | Explicit deferrals in note + ledger | Deferrals |

## Explicit deferrals

- **GMM-2.4.5-*** comparator / cross-lane harness: not claimed.
- **CI** gates (coverage, stress matrices): not claimed.
- **New** verbatim C/C++ standard API citations: deferred to a future run that invokes lane Research with allowlisted URLs; this slice uses **pseudocode** and **reuse-only** references to parent execution notes.

## Code precision (reuse-only)

No new C/C++ standard API surfaces in this slice. **Code precision authority** remains on the Phase 1 execution primary ([[../Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-04-10-2100]]) until a Research-backed pass adds allowlisted citations.

## Next structural intent

Deepen execution tertiary **1.1.2** (observation / cache / invalidation) on the mirrored spine — conceptual [[../../../Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layering-and-Interface-Contracts/Phase-1-1-2-Observation-Cache-and-Invalidation-Roadmap-2026-03-30-1325]].
