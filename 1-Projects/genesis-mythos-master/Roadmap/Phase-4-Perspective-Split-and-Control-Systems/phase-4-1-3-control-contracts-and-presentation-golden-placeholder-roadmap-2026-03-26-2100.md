---
title: Phase 4.1.3 - Control contracts and presentation golden placeholder
roadmap-level: tertiary
phase-number: 4
project-id: genesis-mythos-master
status: in-progress
priority: high
progress: 27
created: 2026-03-26
tags: [roadmap, genesis-mythos-master, phase-4, perspective, controls, t-p4-04]
para-type: Project
subphase-index: "4.1.3"
handoff_readiness: 92
handoff_readiness_scope: "T-P4-04 control-shell and presentation golden placeholder contracts with explicit @skipUntil(D-032) boundaries and lane-C defer semantics"
execution_handoff_readiness: 45
handoff_gaps:
  - "**D-032 / D-043:** replay_row_version and literal golden columns are still unresolved."
  - "**Lane-C ReplayAndVerify:** remains deferred with explicit skip markers; no executable closure claims."
links:
  - "[[phase-4-1-player-first-perspective-read-model-and-rig-contracts-roadmap-2026-03-24-1201]]"
  - "[[phase-4-1-2-rig-consume-order-and-deterministic-binding-roadmap-2026-03-26-2100]]"
  - "[[phase-4-1-4-control-read-model-and-golden-row-selection-contract-roadmap-2026-03-27-0320]]"
  - "[[phase-3-4-6-presentation-handoff-task-lanes-validation-harness-and-dm-promotion-roadmap-2026-03-22-1320]]"
  - "[[decisions-log]]"
---

## Phase 4.1.3 - Control contracts and presentation golden placeholder (tertiary)

This branch captures the next conceptual lane after rig consume order: control-facing contract boundaries and a goldens placeholder table that is intentionally non-claiming until D-032 clears.

### Objectives

- Define control-facing read contracts that consume rig output without opening a write-back path.
- Add placeholder golden-row map with explicit lane-C defer semantics.
- Preserve vault-honest framing: this is structural progression, not execution closure.

### Control contract slices

| Slice | Inputs | Outputs | Current status |
| --- | --- | --- | --- |
| Control shell read adapter | `RigPose_v0`, `PresentationViewState_v0` | `ControlReadModel_v0` | Draft |
| Golden placeholder map | control + rig + tick keys | `GoldenPresentationRow_v0` | Stub (`@skipUntil(D-032)`) |
| Lane-C defer bridge | pending literal keys | queue anchor + owner role | Deferred |
| Tick / golden staleness | `tick_epoch`, rig outputs, `GoldenPresentationRow_v0.tick_key` | `ControlReadModel_v0` drops stale golden rows (no pre-tick carry-forward) | Draft (2026-03-26 shallow deepen) |
| D-060 matrix (advisory HOLD echo) | `missing_roll_up_gates`, `safety_unknown_gap`, macro rollup HR | Witness-vocabulary rows only — maps validator **advisory** codes to execution-deferred checklist language | Draft (2026-03-27 D-093 forward slice) |

### Placeholder policy

- Every candidate golden row in this note is non-authoritative while D-032 is open.
- All placeholders must include owner role and queue anchor text, not pass claims.
- Any mention of replay verification remains `@skipUntil(D-032)`.

### Example rows (non-claiming)

```text
row_id: G-P4.1.3-CTRL-001
state: OPEN_STUB
owner_role: ROLE:lane-c-harness
skip_marker: @skipUntil(D-032)
note: "Placeholder only; no replay_row_version literal lock yet"
```

### Acceptance checklist (conceptual)

- [x] Control read-model boundaries link back to 4.1.2 consume order.
- [x] Placeholder rows include owner + skip marker + non-claim language.
- [x] Cross-reference to 3.4.6 lane intent preserved for operator handoff.
- [x] Explicitly record that REGISTRY-CI/HR closure is still out of scope.

### 2026-03-26 deepen slice (queue-driven)

- Queue entry: `empty-bootstrap-20260326T192925Z`
- Action: one conceptual deepen slice for `4.1.3` control-shell and presentation-golden placeholder boundaries.
- Guardrails preserved: no REGISTRY-CI PASS claim, no HR>=93 claim, lane-C remains `@skipUntil(D-032)`.

### 2026-03-26 follow-up deepen slice (queue-driven)

- Queue entry: `resume-followup-post-empty-bootstrap-20260326T192940Z`
- Action: one additional bounded conceptual slice from the same `4.1.3` machine cursor.
- Added scope:
  - control-governance envelope for `ControlReadModel_v0` consumers (read-only contract, no write-back path),
  - explicit placeholder acceptance wording that keeps Lane-C replay fields deferred under `@skipUntil(D-032)`,
  - owner-role continuity note for future queue handoff into execution-facing artifact prep.
- Guardrails preserved: no REGISTRY-CI PASS claim, no HR>=93 claim, no execution closure claim.

### 2026-03-26 next bounded deepen slice (queue-driven)

- Queue entry: `resume-followup-post-413-20260326T193000Z`
- Action: one additional bounded conceptual deepen slice continuing the same `4.1.3` control-contract and presentation golden-placeholder boundaries.
- Added scope:
  - refined the control-shell read adapter contract wording while keeping it read-only (no write-back path),
  - expanded the golden placeholder map row sketch with explicit `@skipUntil(D-032)` guard (non-authoritative while D-032 is open),
  - preserved lane-C defer bridge semantics: all replay verification fields remain deferred (with owner-role continuity `ROLE:lane-c-harness`).
- Guardrails preserved: no REGISTRY-CI PASS claim, no HR>=93 claim, lane-C remains `@skipUntil(D-032)`, and no execution closure claim (no closure inflation).

### Conceptual execution handoff checklist (NL)

- **Scope:** Covers **T-P4-04** control-shell read surfaces and **presentation golden-row** placeholders that bridge rig output to UI-facing read models **without** write-back or CI closure. **Out of scope:** literal `replay_row_version` / column locks, **REGISTRY-CI PASS**, **HR ≥ 93** rollup closure, and **Lane-C** executable harness — all **execution-deferred** per `missing_roll_up_gates` / `safety_unknown_gap` (advisory on conceptual track).
- **Behavior:** **Actors:** control read adapter (consumer of `RigPose_v0` + `PresentationViewState_v0`), presentation golden stub registry (non-authoritative rows), operator/lane-C owner for deferred replay fields. **Ordering:** rig consume order (4.1.2) → control read model → presentation row selection; no mutation path back into rig or tick commit streams in this slice.
- **Interfaces:** **In:** rig outputs and tick keys per 4.1.2 binding note. **Out:** `ControlReadModel_v0` summary channels + `GoldenPresentationRow_v0` stub identifiers (placeholders only). **Guarantees:** read-only contract; golden rows carry `@skipUntil(D-032)` until D-032/D-043 literals exist.
- **Edge cases:** Missing rig pose → deterministic empty read model (no silent last-good pose). Pause / time-scale changes → control read model follows `PresentationViewState_v0` only; no sim mutation. D-032 still open → all golden cells remain **OPEN_STUB** language.
- **Open questions:** Exact `GoldenPresentationRow_v0` column set vs future `replay_row_version` row — **TBD**, tracked under D-032/D-043. Lane-C queue anchor strings for harness — **TBD** (owner `ROLE:lane-c-harness`).
- **Pseudo-code readiness:** Operators can sketch `SelectGoldenPresentationRows(read_model, tick_key)` as a pure filter over stub rows; no repo emission or CI binding until execution track + D-032 coordination.

### 2026-03-26 post–D-088 mirror bounded deepen (queue `followup-deepen-post-distilled-mirror-d088-gmm-20260326T232100Z`)

- **Source:** **RESUME_ROADMAP** **`deepen`** after **[[decisions-log]]** **D-088** Layer-1 mirror repair (**413**): **`contradictions_detected`** surfaces cleared; continue bounded conceptual work at **`4.1.3`** aligned to **`empty-bootstrap-eatq-20260326T231500Z`** historical chain + live YAML [[workflow_state]].
- **Resolver echo:** **`need_class: missing_structure`**, **`effective_action: deepen`**, **`effective_target: Phase 4.1.3 — post-mirror bounded deepen (413)`**, **`gate_signature: post-d088-distilled-mirror-413-bounded-deepen`**, **`gate_catalog_id: conceptual_v1`**, **`track_lock_explicit: true`**, **`effective_track: conceptual`**.
- **Added (narrow):**
  - **Registry rollup advisory paragraph:** explicitly frames **rollup HR 92 &lt; 93** and **G-P*.*-REGISTRY-CI HOLD** as **execution-deferred / advisory** on the conceptual track (not authoritative open gates blocking conceptual slice completion).
  - **Third placeholder sketch:** `G-P4.1.3-CTRL-003` — operator audit hook for cross-checking **distilled-core** ↔ **workflow_state** cursor strings after mirror repairs (**`OPEN_STUB`**, **`@skipUntil(D-032)`**, owner **`ROLE:lane-c-harness`**).
- **Guardrails preserved:** no REGISTRY-CI PASS claim; no HR≥93 claim; **`missing_roll_up_gates`** / **`safety_unknown_gap`** remain advisory; **`enable_context_tracking: true`** — **Ctx 89%** → next **`queue_followups`** prefers **`recal`** (**D-060**), not another heavy **`deepen`**.

```text
row_id: G-P4.1.3-CTRL-003
state: OPEN_STUB
owner_role: ROLE:lane-c-harness
skip_marker: @skipUntil(D-032)
note: "Post-mirror cursor audit hook; no replay_row_version literal; no CI closure"
```

### 2026-03-27 post–D-091 recal forward bounded deepen (queue `resume-deepen-post-d091-recal-413-gmm-20260326T234800Z`)

- **Source:** **RESUME_ROADMAP** **`deepen`** after **[[decisions-log]]** **D-091** / **`followup-recal-post-413-shallow-deepen-gmm-20260326T233500Z`** **`recal`** + Layer-1 validator advisory (**`missing_roll_up_gates`**); **user_guidance** + **D-060**: **Ctx ~89%** — **narrow** forward-only slice (no closure inflation).
- **Resolver echo:** **`need_class: missing_structure`**, **`effective_action: deepen`**, **`effective_target: Phase 4.1.3 — bounded conceptual deepen after D-091 recal + nested validator advisory (missing_roll_up_gates); narrow slice per D-060 matrix`**, **`gate_signature: post-d091-recal-bounded-deepen|D-060|4.1.3`**, **`gate_catalog_id: conceptual_v1`**, **`track_lock_explicit: true`**, **`effective_track: conceptual`**.
- **Added (narrow):**
  - **D-060 matrix row (advisory):** a **non-authoritative** mapping table that labels **`missing_roll_up_gates`**, **`safety_unknown_gap`**, **rollup HR 92 &lt; 93**, and **G-P*.*-REGISTRY-CI HOLD** as **execution-deferred / advisory** on the conceptual track (same contract as prior registry rollup advisory paragraphs — **no** **PASS** / **HR ≥ 93** claims).
  - **Fourth placeholder sketch:** **`G-P4.1.3-CTRL-004`** — **D-060** rollup-matrix witness-binding hook (vault-only vocabulary; **`OPEN_STUB`**, **`@skipUntil(D-032)`**, owner **`ROLE:lane-c-harness`**).
- **Guardrails preserved:** no REGISTRY-CI PASS claim; no HR≥93 claim; **`missing_roll_up_gates`** / **`safety_unknown_gap`** remain **advisory OPEN**; **`enable_context_tracking: true`** — **Ctx 89%** → next **`queue_followups`** prefers **`recal`** (**D-060**), not another heavy **`deepen`**.

```text
row_id: G-P4.1.3-CTRL-004
state: OPEN_STUB
owner_role: ROLE:lane-c-harness
skip_marker: @skipUntil(D-032)
note: "D-060 matrix binding vocabulary — witness hook only; no rollup HR closure"
```

### 2026-03-26 post–D-087 shallow deepen (queue `followup-deepen-post-recal-empty-bootstrap-413-gmm-20260326T231900Z`)

- **Source:** Optional shallow structural pass after **[[decisions-log]]** **D-087** **`recal`** on **4.1.3**; **user_guidance** + **D-060**: **Ctx 89%** — **narrow** deepen only (no heavy expansion).
- **Added (narrow):**
  - **Read-model staleness rule:** when **`tick_epoch`** advances per **4.1.2** rig consume order, consumers of **`ControlReadModel_v0` + `GoldenPresentationRow_v0`** must not treat golden rows as valid for presentation unless the row’s **`tick_key`** matches the current committed tick (no silent carry-forward of pre-tick golden selections).
  - **Second placeholder sketch:** `G-P4.1.3-CTRL-002` for camera/presentation binding preimage (**`OPEN_STUB`**, **`@skipUntil(D-032)`**, owner **`ROLE:lane-c-harness`**).
- **Guardrails preserved:** no REGISTRY-CI PASS claim; no HR≥93 claim; **`missing_roll_up_gates`** / **`safety_unknown_gap`** remain **execution-deferred / advisory** on conceptual track.

```text
row_id: G-P4.1.3-CTRL-002
state: OPEN_STUB
owner_role: ROLE:lane-c-harness
skip_marker: @skipUntil(D-032)
note: "Camera/presentation binding preimage deferred; no golden row lock"
```

### 2026-03-26 deepen slice (queue `empty-bootstrap-eatq-20260326T231500Z`)

- **Source:** Layer-1 empty-queue bootstrap (A.1b step 5) from queue-continuation record `d33a06bd-370b-497b-8629-10a50d47f90c` (completed `2026-03-26T22:05:00.000Z`); one **`RESUME_ROADMAP`** step at **`4.1.3`** with **`roadmap_track: conceptual`** lock.
- **Added:** NL checklist (above) + presentation-layer read-contract paragraph; clarified **execution-deferred** wording for rollup/registry advisory gates (no authoritative “open gate” framing for conceptual completion).
- **Guardrails preserved:** no REGISTRY-CI PASS claim; no HR≥93 claim; `@skipUntil(D-032)` intact; lane-C defer unchanged.

### Parent

- [[phase-4-1-player-first-perspective-read-model-and-rig-contracts-roadmap-2026-03-24-1201]]

### 2026-03-27 slice-exit handoff to 4.1.4 (forward-only conceptual deepen)

- Queue entry: `resume-roadmap-forward-only-gmm-20260327T010000Z`
- Slice-exit predicate passed on this note (`handoff_readiness: 92` + NL checklist complete for conceptual scope).
- Next structural node selected: [[phase-4-1-4-control-read-model-and-golden-row-selection-contract-roadmap-2026-03-27-0320]].
- Vault-honest unchanged: rollup `HR 92 < 93`, `REGISTRY-CI HOLD`, `missing_roll_up_gates`, and `safety_unknown_gap` stay advisory/execution-deferred.
