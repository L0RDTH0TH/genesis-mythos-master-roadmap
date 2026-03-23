---
title: Phase 3.4.7 — Perspective entry WBS and Phase 4.1 task bridge
roadmap-level: tertiary
phase-number: 3
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-22
tags: [roadmap, genesis-mythos-master, phase, living-world, phase-4, presentation, wbs, handoff]
para-type: Project
subphase-index: "3.4.7"
handoff_readiness: 84
handoff_readiness_scope: "Vault-normative WBS: every Phase 4.1-facing leaf carries lane (A|B|C), blocker DEC, owner, and given/when/then; binds read-model outputs to rig work without re-deriving sim truth — still < min_handoff_conf 93 until repo fixtures + D-032/D-043/D-044"
execution_handoff_readiness: 36
handoff_gaps:
  - "Architect fork **pinned as registry only** — **D-059** (**ARCH-FORK-01** shared control shell vs **ARCH-FORK-02** player-first): **no operator pick logged yet**; Phase 4.1 WBS stays fork-agnostic until **decisions-log** sub-bullet exists"
  - "Lane-C / ReplayAndVerify leaves remain @skipUntil(D-032) / D-043; D-044 dual-track for DM/regen/ambient unchanged per D-057 / D-056"
links:
  - "[[phase-3-4-living-world-operations-and-consequence-fan-out-roadmap-2026-03-23-1210]]"
  - "[[phase-3-4-6-presentation-handoff-task-lanes-validation-harness-and-dm-promotion-roadmap-2026-03-22-1320]]"
  - "[[phase-4-perspective-split-and-control-systems-roadmap-2026-03-19-1101]]"
  - "[[phase-3-4-5-living-world-to-perspective-handoff-bridge-roadmap-2026-03-22-1205]]"
  - "[[decisions-log]]"
  - "[[distilled-core]]"
---

## Phase 3.4.7 — Perspective entry WBS and Phase 4.1 task bridge

**TL;DR:** Close **L1 `missing_task_decomposition`** pressure (see `.technical/Validator/roadmap-handoff-auto-l1-postlv-resume-advance-gmm-20260322T000500Z.md`) by minting **checkable Phase 4.1 entry leaves** that **consume** `PresentationViewState_v0` / `CameraBinding_v0` as **read-model inputs**, inherit **3.4.6** lane matrix + **T-PR-H\*** / **T-DM-P\*** IDs, and split **adapter vs rig** so juniors do not mix **ledger append** into presentation paths (**D-027** / lane B).

## Research integration (external grounding)

**Scope:** Execution decomposition only — normative contracts remain on **3.4.5** / **3.4.6** / Phase 4 primary.

### Key takeaways

- Keep the **three-lane matrix** as the spine of every new task: **A** = committed observables → `PresentationViewState_v0` (deterministic projection; canonical JSON snapshot allowed); **B** = live/interactive (render pump; **no** `TickCommitRecord_v0` asserts); **C** = golden / `ReplayAndVerify` (**DEFERRED** — `@skipUntil(D-032)` until **D-032** / **D-043**).
- **Phase 4.1** leaves start from **read-model outputs**, not sim re-derivation: each rig task names **`PresentationViewState_v0` + `CameraBinding_v0`** (or explicit successor) as **read-only inputs**; sim mutation stays behind **`ToolActionQueue_v0` → `MutationIntent_v0`** promotion (**T-DM-P01–P05**), not camera code.
- Split **read-model → control** into **adapter** (projection → rig target state) then **rig implementation** (engine rig / interpolator). Forbid **ledger append** from presentation-only paths.
- **WBS leaf quality:** one concern per task; each leaf has **lane (A|B|C)**, **fixture id or `@skipUntil`**, **blocker DEC** (D-032, D-044, …), **owner**, **given / when / then**.

### Regen lane fork (D-044) — dual-track reference (**no operator pick**)

- **Option A — `RegenLaneTotalOrder_v0` multi-regen tuple order:** multiple accepted regen requests per `tick_epoch` ordered by a stable tuple (e.g. `regen_request_id`, subgraph hash) before player+DM merge — see [[phase-3-2-3-regen-ledger-replay-rows-and-tick-commit-coupling-roadmap-2026-03-22-1748]] + [[decisions-log]] **D-044**.
- **Option B — ≤1 accepted regen / `tick_epoch`:** at most one regen outcome row feeds merge; additional requests fail closed or defer — same authoritative note + **D-044**.
- **Vault rule:** do not assert **A** or **B** in pseudo-code, `handoff_readiness` narrative, or Phase 4.1 task **Given/When/Then** until the operator logs the pick per **D-044** operator template in [[decisions-log]].

### T-P4-03 — vault-scoped **repo-evidence** contract (lane B smoke)

Until a game repo with a `presentation` / `render` package exists in VCS, **evidence for T-P4-03** is **vault-normative** only:

1. **Package boundary spec** — document forbidden edges: presentation-layer modules **must not** import or call APIs that append to **`AgencySliceApplyLedger_v0`** or emit **`MutationIntent_v0`** (lane B is render pump + profiling hooks only).
2. **Type / cfg wall checklist** — CI-ready when repo exists: build flag or analyzer rule listing **deny patterns** (e.g. `append_apply_ledger`, `MutationIntent` construction) from presentation package roots.
3. **Dev runtime guard (optional)** — debug-only assert hook on hot paths; **not** a substitute for static boundary enforcement.
4. **Lane-B smoke narrative** — “Given render pump tick; When profiling hooks run; Then zero ledger appends from presentation package” maps to grep-able spec text in-vault until green CI proves it.

**Honesty:** this run **does not** claim repo grep/CI proof — **SCOPED_VAULT** promotion only (see DEFERRED ledger).

### Links

- [[Ingest/Agent-Research/phase-3-2-3-replay-regen-ledger-tickcommit-serialization-research-2026-03-22-1830]]
- [[Ingest/Agent-Research/phase-3-4-6-presentation-handoff-engineering-harness-dm-research-2026-03-22-1530]]
- [[Ingest/Agent-Research/phase-3-4-5-sim-presentation-camera-bridge-research-2026-03-22-1245]]

## WBS — Phase 4.1 entry (vault-checkable)

| Task ID | Lane | Concern | Depends on (3.4.6+) | Blocker DEC | Given / When / Then (sketch) |
| --- | --- | --- | --- | --- | --- |
| **T-P4-01** | A | Read-model adapter contract | **T-PR-H01**, **3.4.5** field tables | D-043 preimage registry | **Given** a lane-A fixture id stub; **When** adapter maps bundle → view state; **Then** canonical JSON excludes wall-clock-only fields per **3.4.6** matrix. |
| **T-P4-02** | A | Rig target state envelope | **T-P4-01** | D-032 (header bits) | **Given** frozen `PresentationViewState_v0`; **When** adapter emits `RigTargetState_v0` (pose/mode/handoff tokens); **Then** no sim mutation APIs called. |
| **T-P4-03** | B | Render-only smoke guard | **T-PR-H03** | dev policy | **Given** render pump tick; **When** profiling hooks run; **Then** zero `AgencySliceApplyLedger_v0` appends from presentation package. |
| **T-P4-04** | C | Golden placeholder | **T-PR-H04** | D-032, D-043 | **Given** `@skipUntil(D-032)`; **When** CI policy allows; **Then** wire `ReplayAndVerify` row — **DEFERRED**. |
| **T-P4-05** | — | DM promotion trace into Phase 4 | **T-DM-P01–P05** | D-044 | **Given** staged tool action; **When** Apply (not Preview); **Then** promotion emits `MutationIntent_v0` draft only after **3.1.5** ordering story + **D-044** note satisfied. |

## DEFERRED ledger (execution)

| Task ID | Status | Owner | Blocker | Unblock condition |
| --- | --- | --- | --- | --- |
| **T-P4-01** | **DEFERRED** | eng | D-043, repo | Lane-A fixture + adapter interface in repo |
| **T-P4-02** | **DEFERRED** | eng | D-032 | Replay header freeze + `RigTargetState_v0` schema row |
| **T-P4-03** | **SCOPED_VAULT** | eng | D-027, build flags, **no game repo in vault** | Vault package-boundary + forbidden-import spec landed (**§ T-P4-03**); promote to **IN_PROGRESS** when repo path exists + CI/analyzer row green |
| **T-P4-04** | **DEFERRED** | eng | D-032, D-043 | Lane-C policy open |
| **T-P4-05** | **DEFERRED** | eng + operator | D-044 A/B | Operator logs pick in **decisions-log** **D-044** |

## Pseudo-code — adapter boundary (depth-4 sketch)

```text
interface PresentationToRigAdapter:
  fn adapt(view: PresentationViewState_v0, binding: CameraBinding_v0) -> RigTargetState_v0
  // MUST NOT: append MutationIntent_v0, touch TickCommitRecord_v0, or read wall-clock for preimage fields
```

## Dependencies

- **D-057** / **3.4.6** — upstream task IDs + harness sketch authoritative.
- **D-056** / **3.4.5** — `PresentationViewState_v0` / `CameraBinding_v0` draft authoritative.
- **D-055** — **G-P3.4-*** rollup **PASS** rows **not** reopened.
- **D-044** — regen / DM / ambient same-tick story stays **dual-track** until operator logs **A/B**.
