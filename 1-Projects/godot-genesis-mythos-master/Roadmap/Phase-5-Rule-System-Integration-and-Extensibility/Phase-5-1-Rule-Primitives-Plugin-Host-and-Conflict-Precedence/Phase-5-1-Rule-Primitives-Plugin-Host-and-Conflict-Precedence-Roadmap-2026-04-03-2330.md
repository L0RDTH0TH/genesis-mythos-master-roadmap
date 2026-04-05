---
title: Phase 5.1 - Rule Primitives, Plugin Host, Conflict Precedence
roadmap-level: secondary
phase-number: 5
subphase-index: "5.1"
project-id: godot-genesis-mythos-master
status: in-progress
priority: high
progress: 96
handoff_readiness: 86
created: 2026-04-03
restored_to_active_tree: 2026-04-04
tags:
  - roadmap
  - godot-genesis-mythos-master
  - phase-5
para-type: Project
links:
  - "[[Phase-5-Rule-System-Integration-and-Extensibility-Roadmap-2026-03-30-0430]]"
  - "[[Conceptual-Decision-Records/deepen-phase-5-1-secondary-rule-primitives-plugin-host-conflict-2026-04-03-2310]]"
  - "[[Conceptual-Decision-Records/deepen-phase-5-1-secondary-rollup-nl-gwt-2026-04-04-1815]]"
  - "[[decisions-log]]"
  - "[[1-Projects/godot-genesis-mythos-master/Roadmap/Branches/phase-5-1-secondary-rollback-2026-04-02/Phase-5-1-Rule-Primitives-Plugin-Host-and-Conflict-Precedence-Roadmap-2026-04-03-2310]]"
---

> [!note] #handoff-review
> `handoff_readiness: 86` — Phase 5 secondary **5.1** rollup complete: NL checklist + **GWT-5.1-A–K** parity vs tertiaries **5.1.1–5.1.3** (see **Secondary rollup closure** below). CDR [[Conceptual-Decision-Records/deepen-phase-5-1-secondary-rollup-nl-gwt-2026-04-04-1815]]; queue `followup-deepen-phase5-51-rollup-nl-gwt-gmm-20260404T181000Z`.
>
> **Active-tree restoration (2026-04-04):** Files under this slice were removed during a conceptual reset; this note was re-materialized from rollback archive + Phase 5 primary + CDR authority. Queue `followup-deepen-phase5-51-mint-gmm-20260403T231000Z` / `parent_run_id: eatq-remint-phase51-20260404`.
>
> Next structural cursor: **Phase 5 primary rollup** — [[workflow_state]] **`current_subphase_index: "5"`** after this rollup; optional **RECAL-ROAD** at high ctx util (~**94%**) before primary rollup deepen per operator note.
>
> **Tertiary folder:** `Phase-5-1-1*.md` **present** (2026-04-04 re-mint). Execution proof rows remain **conceptual-track deferred** per [[roadmap-state]] / [[distilled-core]].

## Phase 5.1 - Rule primitives, plugin host, conflict precedence

This secondary slice is the first structural home for the Phase 5 rule engine surface. It defines "what rules are allowed to decide" at the conceptual NL level (evaluate, schedule, and emit structured outcomes), while routing any world-change request through Phase 2's upstream validation and orchestration stories.

## Scope

In scope:
- Rule primitives NL design authority: RuleOutcome-shaped records and an evaluation schedule relative to tick/session boundaries (no new sim truth).
- Plugin host lifecycle: ruleset manifest admission, deterministic load validation, version pin enforcement, and deterministic error/failure classes (execution packaging deferred).
- Deterministic conflict precedence: when multiple rules target the same seam, select a single deterministic winner and produce an operator-visible explanation path.
- Integration constraints: explanations and operator readout must be legible via the Phase 4.1.3 presentation-time validation story.

Out of scope:
- Concrete programming language, package registry details, crypto signing, sandbox OS isolation, or performance SLAs (execution-deferred).
- Any claim that rules "author commits" directly; rule decisions remain subject to the Phase 4 orchestration layer and Phase 2 commit/deny/defer semantics.

## Behavior (natural language)

1. RuleOutcome emission contract: given committed world snapshot + ruleset pin + an orchestration/event trigger stream, the rules kernel evaluates rule graphs and emits deterministic RuleOutcome records suitable for downstream operator readout.
2. Plugin host admission contract: when a manifest is presented, the host validates declared seams and enforces the version pin; incompatible pins produce a deterministic, named failure class.
3. Conflict precedence contract: when two or more eligible rules target the same seam and conflict class, the kernel resolves to a single deterministic winner using a declared precedence class, and renders a legible operator explanation of "why this winner."
4. Non-bypass contract: any request that would imply world change or commit-like effect must route through Phase 2's structural regen / validation story (no bypass, no silent override).

## Deterministic tie-break digest (feeds 5.1.1+)

Before applying declared **precedence_class** (tertiary **5.1.2+**), the kernel uses a **canonical stable tuple** for ordering eligible rules so replay and audit traces agree:

1. `ruleset_pin_id` (lexicographic)
2. `seam_id` (must match **3.4.1** consumer / **SeamId** vocabulary)
3. `rule_stable_id` (manifest-declared stable id, not display name)
4. `trigger_ordinal` (monotonic within the evaluation frame)

If two candidates remain tied after the tuple, **precedence_class** from manifest + host policy selects the winner; **5.1.1** binds manifest fields that admit this tuple; **5.1.2+** binds schedule and explicit matrix rows.

## Interfaces

Upstream (Phase 3 - 4):
- Consumes ObservationChannel taxonomy and authority_class discipline from Phase 3.2.1.
- Consumes Phase 4 session orchestration artifacts as triggers (not persistence writers).
- Relies on Phase 4.1.3 presentation-time validation as the legibility envelope for operator explanations.

Parent (Phase 5 primary):
- [[Phase-5-Rule-System-Integration-and-Extensibility-Roadmap-2026-03-30-0430]].

Downstream (5.1.1+):
- Tertiary nodes refine rule primitives into concrete NL/structure: manifest + seam admission, deterministic ordering, and then operator-visible explanation payloads.

Outward guarantees:
- Determinism: same committed snapshot + same ruleset pin + same trigger stream yields replay-stable outcomes.
- Conflict transparency: precedence resolution produces one winner plus operator-visible diff/explanation (no silent merge).

## Edge cases

- Rules ask for structural regen: emit a regen request intent consistent with Phase 3 overwrite vs structural story; rules do not bypass Phase 2 validation.
- Plugin mismatch / bad manifest: host rejects load with deterministic named failure class (execution packaging deferred).
- High churn operator toggles: mode switches may reorder which rules are eligible, but the kernel must not assume a static rule graph without explicit rebinding at NL level.

## Open questions

- Minimum ruleset manifest fields required for community sharing (version pin, seam declarations, conflict class).
- Whether generator vs event vs style swaps share a single plugin envelope or require separate envelopes for conflict classes (execution-deferred).

## Pseudo-code readiness

At secondary conceptual depth, no pseudo-code is required. Algorithm sketches and operational pseudo-code may appear starting in tertiary 5.1.1+.

## Secondary slice GWT (GWT-5.1-A-K) - evidence narrows vs primary

| ID | Given | When | Then | Evidence (narrowed here) |
| --- | --- | --- | --- | --- |
| GWT-5.1-A | Phase 3 sim-visible facts on bus | Kernel evaluates rules | Rules consume observation-class inputs without inventing sim mutations | Primary § Behavior; CDR [[Conceptual-Decision-Records/deepen-phase-5-1-secondary-rule-primitives-plugin-host-conflict-2026-04-03-2310]] |
| GWT-5.1-B | Phase 4.2.1 PerspectiveTransitionGraph | Mode/orchestration transition triggers | Rule triggers may attach to transition events; rules do not author commits | Primary § Interfaces; Phase 4.2 trigger inputs |
| GWT-5.1-C | Phase 4.2.2 TransitionOutcomeLedger | Outcome recorded | Rule outcomes remain consistent with ledger rows; no duplicate truth | Primary § Interfaces; Primary conflict/consistency story |
| GWT-5.1-D | Phase 4.2.3 OrchestrationRepairToken | Repair path triggered | Rules may propose repair-shaped intents; escalation readout remains authoritative | Primary § Edge and Phase 4.2.x constraints |
| GWT-5.1-E | Phase 4.1.3 presentation envelope | Operator reads outcome | Explanations are legible per presentation-time validation story | Primary § Behavior; Phase 4.1.3 legibility contract |
| GWT-5.1-F | Plugin manifest declares conflict class | Two rules collide | Deterministic precedence winner plus operator-visible explanation | This slice: deterministic conflict precedence + explanation |
| GWT-5.1-G | Ruleset version pin | Load requested | Kernel rejects incompatible pins with deterministic named failure class | This slice: plugin host enforcement |
| GWT-5.1-H | Phase 2 commit boundary | Rule proposes world change | Proposal routes through structural regen / validation story; no bypass | CDR constraints + Phase 2 non-bypass principle |
| GWT-5.1-I | D-3.4-* consumer granularity rows | Bundle policy applies | Rules respect SeamId rows and do not invent a second consumer truth | Primary § Interfaces; decisions-log D-3.4-* rows |
| GWT-5.1-J | Community ecosystem seam | Operator swaps generator/event/style | Swap is documented and replay-stable under manifest pin (execution packaging deferred) | Primary § Scope + this slice's host lifecycle |
| GWT-5.1-K | Conceptual waiver | Validator advisory codes surface | Execution-only gaps (marketplace, CI) are deferred and not blocking | [[roadmap-state]] + [[distilled-core]] waiver rows |

## Secondary rollup closure (NL checklist + GWT parity)

**NL checklist (rollup):** Scope, authority, seams, operator legibility, replay/determinism, deferral boundaries, pseudo-code / structural anchors — each maps to tertiary evidence below; **no** `Roadmap/Execution/**` authority claimed on conceptual track.

**GWT-5.1 ↔ tertiary parity (evidence loci):**

| GWT-5.1 row | Primary tertiary evidence | Notes |
| --- | --- | --- |
| A–D (manifest / admission / failure classes) | [[Phase-5-1-1-Ruleset-Manifest-Seam-Admission-and-Deterministic-Evaluation-Order-Roadmap-2026-04-04-0010]] | RulesetManifest + **3.4.1** seam admission + tuple-first order |
| E–H (evaluation schedule / tuple vs precedence / defer / legibility) | [[Phase-5-1-2-Kernel-Evaluation-Schedule-and-Rule-Ordering-Roadmap-2026-04-04-0715]] | **EvaluationFrame**, **precedence_class** after **5.1.1** sort; **3.1.2** / **4.1.3** bindings |
| I–J (conflict matrix / cross-seam / explanation handles) | [[Phase-5-1-3-Precedence-Conflict-Matrix-and-Cross-Seam-Resolution-Roadmap-2026-04-04-1209]] | **matrix_row_id** / **explanation_handle** for **4.1.3** |
| K (waiver) | [[roadmap-state]], [[distilled-core]] | Execution rollup / CI / HR deferred |

**Open fork (logged, not blocking conceptual rollup):** [[decisions-log]] **D-5.1.3-matrix-vs-manifest** — matrix vs manifest ordinal tension at NL; default story documented on **5.1.3** note.

CDR: [[Conceptual-Decision-Records/deepen-phase-5-1-secondary-rollup-nl-gwt-2026-04-04-1815]] · queue `followup-deepen-phase5-51-rollup-nl-gwt-gmm-20260404T181000Z`.

## Research integration

- None for this slice (vault-first pattern; external benchmarks deferred).

## Tertiary notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/godot-genesis-mythos-master/Roadmap/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-1-Rule-Primitives-Plugin-Host-and-Conflict-Precedence"
WHERE roadmap-level = "secondary" OR roadmap-level = "tertiary" OR roadmap-level = "task"
SORT subphase-index ASC, file.name ASC
```
