---
title: Phase 5.1 — Rule primitives, plugin host, and deterministic conflict precedence
roadmap-level: secondary
phase-number: 5
subphase-index: "5.1"
project-id: genesis-mythos-master
status: active
priority: high
progress: 40
handoff_readiness: 86
created: 2026-04-04
tags:
  - roadmap
  - genesis-mythos-master
  - phase
para-type: Project
links:
  - "[[genesis-mythos-master-Roadmap-2026-03-30-0430]]"
  - "[[Phase-5-Rule-System-Integration-and-Extensibility-Roadmap-2026-03-30-0430]]"
---

## Phase 5.1 — Rule primitives, plugin host, and deterministic conflict precedence

**Post-reset re-mint (2026-04-04):** This note re-establishes authoritative **secondary 5.1** design after manual removal of the prior 5.1 roadmap chain. Historical rationale remains in [[Conceptual-Decision-Records/deepen-phase-5-1-secondary-rule-primitives-plugin-host-conflict-2026-04-03-2310]] and related pre-reset CDRs; **this file** is the live contract for tertiaries **5.1.1+**.

## Scope

**In scope:** **Rule primitive** vocabulary (**RuleOutcome** shapes, evaluation **epoch** relative to sim tick vs session transition, idempotent **re-evaluation** boundaries); **plugin host** surface (manifest **admission**, **version pin**, **activation scope**, deterministic **load/reject** error classes); **conflict precedence** (declared **precedence_class**, **tie-break** keys, **single winner** per collision scope, **operator-visible** explanation payloads routed through **4.1.3** presentation envelope).

**Out of scope:** concrete bytecode sandbox, marketplace signing, remote fetch, perf SLOs — **execution-deferred** per primary waiver.

## Behavior (natural language)

**Kernel** consumes **sim-visible** facts (**3.2.1** **ObservationChannel** + **authority_class**) and **4.2** orchestration signals (**PerspectiveTransitionGraph**, **TransitionOutcomeLedger**, **OrchestrationRepairToken**) as **read-only triggers**. It **never** authors Phase **2** commit envelopes or mutates **3.1.4** checkpoint authority.

**Plugin host** validates **RulesetManifest** against declared **SeamId** rows (**3.4.1** consumer contract discipline). Incompatible **version_pin** → deterministic **reject** with stable **failure_class** (named at NL; wire format deferred).

**Conflict flow:** when two active rules target the same **precedence_class** + **collision_key**, kernel applies **declared ordering** (manifest **precedence_rank** + **ruleset_pin** lexicographic tie-break) and emits **one** **RuleOutcome** plus **ConflictResolutionTrace** suitable for **4.1.3**-style operator readout (no silent merge).

## Interfaces

| Surface | Responsibility |
| --- | --- |
| **RuleOutcome** | Approve / deny / defer / propose_orchestration_intent — **proposal only** upstream of Phase **2** / **4.2** writers |
| **RulesetManifest** | Version, seams, **precedence_class** declarations, optional **generator/event/style** slot hooks |
| **PluginHostAdmission** | Validate manifest → load graph slice → bind triggers; **reject** path is replay-stable |
| **ConflictResolutionTrace** | Winner id, loser set, **reason_code**, **presentation_labels** for operator UI |

**Upstream:** [[Phase-3-2-1-Observation-Channel-Taxonomy-Roadmap-2026-04-02-2310]], [[Phase-4-2-1-Session-Scoped-Orchestration-Hooks-and-Perspective-Transition-Graph-Roadmap-2026-04-03-2125]], [[Phase-4-2-2-Transition-Outcome-Ledger-and-Lane-Projection-Parity-Roadmap-2026-03-31-1200]], [[Phase-4-1-3-Consumer-Surface-Framing-and-Presentation-Time-Validation-Roadmap-2026-04-03-2110]].

**Downstream:** tertiaries **5.1.1** (manifest + **SeamId** binding), **5.1.2** (evaluation schedule / ordering), **5.1.3** (precedence matrix + winner resolution) — names follow prior chain for continuity; content is re-derived from this note.

## Edge cases

- **Repair storm:** multiple **OrchestrationRepairToken** instances in one tick — kernel **batches** triggers with deterministic **trigger_total_order**; does not fork ledger truth.
- **Stale manifest pin** after world drift — **reject_eval** outcome with **reason_code**; no partial apply.
- **Rule proposes structural regen** — emits intent only; Phase **3** overwrite / structural paths remain authoritative.

## Open questions

- Minimum **collision_key** granularity (per **SeamId** vs per **ObservationChannel** family) before execution prototypes.
- Whether **defer** outcomes from rules participate in the same **TransitionOutcomeLedger** rows as **4.2.2** or a **shadow companion** ledger (**execution-deferred**).

## Pseudo-code readiness

**Secondary depth:** interface sketches and **ordering narrative** only; **no** full pseudo-code block required until **5.1.2+** (mid-technical escalation per roadmap-deepen).

## Secondary **GWT-5.1-A–K** (narrowed vs primary **GWT-5-A–K**)

| ID | Given | When | Then | Evidence (this note) |
| --- | --- | --- | --- | --- |
| **GWT-5.1-A** | Sim-visible bus payload | Kernel evaluates | Consumption respects **authority_class**; no sim mutation | § Behavior |
| **GWT-5.1-B** | **4.2.1** transition event | Trigger fires | Attachment is **read-only** side-effect on rule graph | § Behavior |
| **GWT-5.1-C** | **4.2.2** ledger row | Outcome emitted | **RuleOutcome** does not duplicate ledger as second truth | § Behavior |
| **GWT-5.1-D** | **4.2.3** repair token | Repair path | Rule may **propose** repair-shaped intent; escalation readout wins | § Edge |
| **GWT-5.1-E** | **4.1.3** envelope | Operator reads | **ConflictResolutionTrace** maps to presentation-time validation story | § Behavior |
| **GWT-5.1-F** | Conflicting rules same class | Collision | **Single winner** + visible trace | § Behavior |
| **GWT-5.1-G** | Bad **version_pin** | Load | Deterministic **reject** + **failure_class** | § Behavior |
| **GWT-5.1-H** | Phase **2** commit boundary | Rule proposes mutation | Routes through structural regen / validation — **no bypass** | § Scope |
| **GWT-5.1-I** | **D-3.4-*** rows | Bundle policy | Rules respect **SeamId** discipline | § Interfaces |
| **GWT-5.1-J** | Ecosystem swap story | Operator swaps bundle | **Documented** + replay-stable under pin (packaging deferred) | § Scope |
| **GWT-5.1-K** | Conceptual waiver | Validator advisory | Execution marketplace / CI codes **non-blocking** | Primary § waiver |

## Related

- [[Phase-5-Rule-System-Integration-and-Extensibility-Roadmap-2026-03-30-0430]]
- [[Conceptual-Decision-Records/deepen-phase-5-1-secondary-remint-post-reset-2026-04-04-0015]]
