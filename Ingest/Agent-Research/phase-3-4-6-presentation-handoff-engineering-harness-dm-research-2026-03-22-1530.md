---
title: Phase 3.4.6 prep — presentation handoff tasks, validation harness, DM tool promotion
research_query: "engineering task breakdown presentation read-model vs golden replay; projection testing; editor tool promotion"
linked_phase: Phase-3-4-6 (pre-mint — follow 3.4.5 bridge)
project_id: genesis-mythos-master
created: 2026-03-22
tags: [research, agent-research, genesis-mythos-master, phase-3-4, phase-4, testing, handoff]
para-type: Resource
agent-generated: true
research_tools_used: [web_search]
research_escalations_used: 0
research_focus: junior_handoff
parent_handoff: "RESUME_ROADMAP pre-deepen nested research; queue_entry_id resume-gmm-deepen-followup-post-a1b-20260322T132000Z; parent_run_id pr-eatq-resume-gmm-deepen-20260322T1400Z"
---

# Phase 3.4.6 research — task decomposition, harness sketch, DM promotion workflow

**Scope:** Non-normative engineering patterns to close the validator gap **`missing_task_decomposition`** after **3.4.5** (contracts + DEFERRED ledger). Targets the **next tertiary (3.4.6)**: explicit work breakdown for **presentation handoff vs golden/replay**, a **validation harness sketch** tying **sim observables** to **presentation read-model**, and **DM tool promotion** tasks aligned with **`ToolActionQueue_v0`**.

## Vault anchor (do not duplicate)

- **3.4.5** already defines **`PresentationViewState_v0`**, **`CameraBinding_v0`**, **`ToolActionQueue_v0`** bounds, preimage exclusions, and **DEFERRED** rows for goldens (**D-032** / **D-043**) and **D-044**. Do not re-litigate contract tables here; add **execution** and **test** scaffolding only.

- Prior synthesis: [[phase-3-4-5-sim-presentation-camera-bridge-research-2026-03-22-1245]] (sim vs presentation industry split; DM A/B/C roles).

## 1. Engineering task breakdown — presentation handoff vs golden / replay

**Intent:** Separate **three lanes** so juniors do not conflate “looks right in editor” with “replay-authoritative.”

| Lane | What it proves | Typical artifacts | Vault coupling |
|------|----------------|-------------------|----------------|
| **A — Read-model / projection** | Given a fixed **committed** observable snapshot (or tick commit), **`PresentationViewState_v0`** (and derived camera pose) updates **deterministically** and **never** mutates preimage fields | Unit/integration tests on pure functions: `committed_observables → view_state` | Maps to **3.4.5** acceptance observables (doc checks) extended with **automated** assertions |
| **B — Live / interactive** | Frame-rate variability only affects **interpolation_alpha** / UX paths per **D-027** | Play-mode or headless “pump N sim steps, M render frames” smoke tests | Explicitly **not** compared to **TickCommitRecord_v0** hashes for presentation-only fields |
| **C — Golden / ReplayAndVerify** | End-to-end **tick ledger** + **header version** stability (**D-032** / **D-043**) | Frozen fixtures, `ReplayAndVerify` CI rows | **DEFERRED** in 3.4.5 until header freeze; 3.4.6 should **stub** harness interfaces and **document** which lane each test belongs to |

**Task seeds (for 3.4.6 checklist):**

1. **T-PR-H01** — Document **test matrix**: row per observable family × lane (A/B/C) × “allowed to assert hash?”
2. **T-PR-H02** — Implement **lane-A** minimal test: load fixture `TickCommitRecord_v0` (or markdown stand-in), build read model, assert `PresentationViewState_v0` fields match expected **excluding** wall-clock-only fields when run twice with different fake `dt_real`.
3. **T-PR-H03** — Implement **lane-B** smoke: assert **no** `AgencySliceApplyLedger_v0` append from render-only code paths (static analysis or runtime guard flag in dev builds).
4. **T-PR-H04** — **Lane-C** placeholder: empty or `@skipUntil(D-032)` test that will assert **presentation is absent** from replay preimage until policy allows.

[Source: Golden Master testing overview](https://stevenschwenke.de/whatIsTheGoldenMasterTechnique)

[Source: Deterministic replay survey (ACM)](https://dl.acm.org/doi/10.1145/2790077)

[Source: Game replay — input replay vs state snapshot (Stack Exchange / industry summaries)](https://gamedev.stackexchange.com/questions/19624/deterministic-replay-in-a-modern-game)

## 2. Validation harness sketch — observables → presentation read-model

**Pattern (CQRS / event-sourced projections):** Treat **post_apply** observables as the **write-side truth** for tests; **presentation** is a **projection**. Tests should **given → when → then**: given a sequence of commits (or one frozen bundle), when the projection runs, then the read model matches expected documents.

[Source: Testing event-driven projections](https://event-driven.io/en/testing_event_driven_projections/)

[Source: Marten — testing projections](https://martendb.io/events/projections/testing)

**Concrete sketch for Genesis Mythos (markdown-first / future repo):**

```text
Harness: PresentationProjectionHarness
  Input:  SimObservableBundleFixture (versioned id) OR TickCommitRecordFixture
  Step 1: Validate bundle against facet allow-list (3.4.3 / D-037) — fail closed
  Step 2: Build PresentationViewState_v0 via documented interpolate() / derive path
  Step 3: Serialize view_state to canonical JSON (stable key order) for snapshot compare
  Step 4: Assert excluded-from-preimage fields are NOT present in any replay hash input struct
  Optional: Property test — idempotent replay of same commit → same view (lane A only)
```

**Observability hooks:** Log **binding_id**, **subscribed_facet_ids**, and **presentation_tick_seq** per render frame in **dev** only; correlate with **tick_epoch** in structured logs to catch ordering bugs (presentation advancing without new commit).

## 3. DM tool promotion workflow — tasks

**Pattern:** Engines separate **editor** undo stacks from **runtime** mutation paths; “promotion” is an explicit **commit boundary**, not an accidental flush.

[Source: Godot — EditorUndoRedoManager vs runtime UndoRedo](https://docs.godotengine.org/en/stable/classes/class_editorundoredomanager.html)

**Workflow tasks aligned with `ToolActionQueue_v0`:**

1. **T-DM-P01** — Define **states** for a queued tool action: `staged` → `validated` → `promoted_to_intent` → `ordered` (append to **AgencySliceApplyLedger_v0** only in last state).
2. **T-DM-P02** — Specify **idempotency**: duplicate `tool_action_idempotency_key` → ledger hit / no second intent (mirror **3.1.5** patterns).
3. **T-DM-P03** — **Promotion gate** checklist: facet scope, DM capability flag, **D-044** lane (document “cannot promote same-tick with regen until operator A/B”).
4. **T-DM-P04** — UX / tooling: “Apply” vs “Preview” commands; preview **never** enqueues promotion (maps to 3.4.5 classes **view-only** vs **intent producers**).
5. **T-DM-P05** — Telemetry: metric for **queue depth**, **promotion latency** (ticks), **rejected promotions** with reason enum.

## Raw sources (vault)

- (none — web_search snippets only this run)

## Sources

- https://stevenschwenke.de/whatIsTheGoldenMasterTechnique
- https://dl.acm.org/doi/10.1145/2790077
- https://gamedev.stackexchange.com/questions/19624/deterministic-replay-in-a-modern-game
- https://event-driven.io/en/testing_event_driven_projections/
- https://martendb.io/events/projections/testing
- https://docs.godotengine.org/en/stable/classes/class_editorundoredomanager.html
- https://docs.godotengine.org/cs/latest/classes/class_undoredo.html
