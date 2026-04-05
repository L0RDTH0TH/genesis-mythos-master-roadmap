---
title: Phase 5.1 - Rule Primitives, Plugin Host, Conflict Precedence
roadmap-level: secondary
phase-number: 5
subphase-index: "5.1"
project-id: sandbox-genesis-mythos-master
status: complete
priority: high
progress: 100
handoff_readiness: 85
created: 2026-04-03
archived_from_active_tree: 2026-04-02
archive_reason: operator rollback — stabilize Second-Brain / regen cadence; next authoritative secondary 5.1 will be re-minted from clean RESUME_ROADMAP
tags:
  - roadmap
  - sandbox-genesis-mythos-master
  - phase-5
para-type: Project
links:
  - "[[Phase-5-Rule-System-Integration-and-Extensibility-Roadmap-2026-03-30-0430]]"
  - "[[Conceptual-Decision-Records/deepen-phase-5-1-secondary-rule-primitives-plugin-host-conflict-2026-04-03-2310]]"
  - "[[decisions-log]]"
---

> [!note] #handoff-review
> `handoff_readiness: 85` - Phase 5 secondary 5.1 minted. This container establishes the NL design authority for rule primitives (RuleOutcome-shaped records and evaluation schedule), the plugin host lifecycle (manifest admission and deterministic version pin / failure classes), and deterministic conflict precedence with operator-visible explanation paths.
> 
> Safety / authority constraints are preserved: no bypass of Phase 2 commit/deny/defer semantics, and no redefinition of Phase 3.1.4 checkpoint authority. Next structural cursor: **5.1.1** (mint tertiary under 5.1).

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

## Research integration

- None for this slice (vault-first pattern; external benchmarks deferred).

## Tertiary notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/sandbox-genesis-mythos-master/Roadmap/Phase-5-Rule-System-Integration-and-Extensibility/Phase-5-1-Rule-Primitives-Plugin-Host-and-Conflict-Precedence"
WHERE roadmap-level = "secondary" OR roadmap-level = "tertiary" OR roadmap-level = "task"
SORT subphase-index ASC, file.name ASC
```

