---
title: Phase 5.1.2 - Kernel Evaluation Schedule and Rule Ordering
roadmap-level: tertiary
phase-number: 5
subphase-index: "5.1.2"
project-id: godot-genesis-mythos-master
status: in-progress
priority: high
progress: 88
handoff_readiness: 85
created: 2026-04-04
tags:
  - roadmap
  - godot-genesis-mythos-master
  - phase-5
para-type: Project
links:
  - "[[Phase-5-1-1-Ruleset-Manifest-Seam-Admission-and-Deterministic-Evaluation-Order-Roadmap-2026-04-04-0010]]"
  - "[[Phase-5-1-3-Precedence-Conflict-Matrix-and-Cross-Seam-Resolution-Roadmap-2026-04-04-1209]]"
  - "[[Phase-5-1-Rule-Primitives-Plugin-Host-and-Conflict-Precedence-Roadmap-2026-04-03-2330]]"
  - "[[Phase-3-1-2-Tick-Scheduling-Defer-Merge-and-Work-Queue-Policy-Roadmap-2026-04-02-0020]]"
  - "[[Phase-4-1-3-Consumer-Surface-Framing-and-Presentation-Time-Validation-Roadmap-2026-04-03-2110]]"
  - "[[Phase-5-Rule-System-Integration-and-Extensibility-Roadmap-2026-03-30-0430]]"
  - "[[Conceptual-Decision-Records/deepen-phase-5-1-2-kernel-eval-schedule-rule-ordering-2026-04-04-0715]]"
  - "[[decisions-log]]"
---

> [!note] #handoff-review
> `handoff_readiness: 85` — Tertiary **5.1.2** binds a **kernel evaluation schedule** (when sorted **RuleCandidate** rows are considered per frame) and **rule ordering after tuple sort** — application of **precedence_class** and host policy in a **deterministic pass order** that stays replay-stable with **5.1.1** lexicographic ordering. **5.1.3** owns the explicit **conflict matrix** + cross-seam resolution — [[Phase-5-1-3-Precedence-Conflict-Matrix-and-Cross-Seam-Resolution-Roadmap-2026-04-04-1209]].

## Scope

In scope:
- **EvaluationFrame** NL contract: committed snapshot + ruleset pin + trigger stream slice defines one schedulable frame; admission failures from **5.1.1** short-circuit before schedule construction.
- **Schedule slots**: ordered phases within a frame — e.g. *admit → build eligible set → tuple sort (**5.1.1**) → precedence resolution pass → emit RuleOutcome-shaped records* — expressed only at NL + algorithm sketch depth.
- **Precedence application order**: when multiple rules share a **precedence_class** bucket, deterministic tie-break uses the **5.1** digest tuple first; **within-class** ordering uses manifest-declared **precedence_ordinal** (illustrative name) when present, else stable fallback (ruleset_pin_id, rule_stable_id) — no silent merges.
- Binding to **3.1.2** tick / defer semantics: rule evaluation slots are **downstream** of tick-scoped work admission; rules do not invent new merge gates.
- Operator legibility: schedule and pass names are **4.1.3**-readable (presentation envelope consumes named pass boundaries, not raw internals).

Out of scope:
- Full **precedence_class** matrix catalog and cross-seam winner payloads — **5.1.3+**.
- WASM / sandbox scheduling, wall-clock SLAs — execution-deferred.

## Behavior (natural language)

1. **Frame construction:** Given a valid admitted manifest (**5.1.1**), the kernel constructs an **EvaluationFrame** identity (snapshot id, pin id, trigger ordinal window) for audit replay.
2. **Eligible set:** Rule instances eligible in the frame are collected; empty set is valid — emit no outcomes for that frame.
3. **Tuple ordering:** Eligible rows are sorted by `(ruleset_pin_id, seam_id, rule_stable_id, trigger_ordinal)` per **5.1.1**; this order defines **evaluation pass 1** (ordered scan before precedence collapse).
4. **Precedence passes:** Rules are partitioned by **precedence_class** (from manifest / host policy). Within each class, **pass 2** applies: winner selection uses tuple order as primary key, then **precedence_ordinal** when defined for that class, then deterministic host fallback — single winner per **(seam_id, conflict_class)** group at NL.
5. **Emission:** **RuleOutcome** records reference frame id + pass identifiers + explanation handles suitable for **4.1.3** (execution payload deferred).
6. **Interaction with defer:** If **3.1.2** marks the frame as deferred, kernel schedule does not emit authoritative outcomes for that slice; deterministic **defer_marker** path only (names illustrative).

## Interfaces

Upstream:
- [[Phase-5-1-1-Ruleset-Manifest-Seam-Admission-and-Deterministic-Evaluation-Order-Roadmap-2026-04-04-0010]] — manifest, seam admission, tuple sort.
- [[Phase-5-1-Rule-Primitives-Plugin-Host-and-Conflict-Precedence-Roadmap-2026-04-03-2330]] — tie-break digest + RuleOutcome schedule intent.
- [[Phase-3-1-2-Tick-Scheduling-Defer-Merge-and-Work-Queue-Policy-Roadmap-2026-04-02-0020]] — tick closure / defer boundary.

Downstream:
- [[Phase-5-1-3-Precedence-Conflict-Matrix-and-Cross-Seam-Resolution-Roadmap-2026-04-04-1209]] — explicit conflict matrix, winner + explanation payloads.

Outward guarantees:
- **Replay-stable schedule:** same frame inputs → same pass order → same winner per conflict group at conceptual NL.
- **No precedence before tuple:** **precedence_class** never reorders before **5.1.1** sort completes.

## Edge cases

- **All candidates same precedence_class and tied on tuple and ordinal:** host fallback ordering must still pick one winner; document as **deterministic panic-class** name at NL (execution string deferred).
- **Dynamic rule graph mid-frame:** conceptual contract assumes frame boundary from **4.2** orchestration — mid-frame graph mutation is out of scope; treated as new frame.
- **Cross-seam conflicts:** deferred to **5.1.3** matrix — here only single-seam **conflict_class** groups.

## Open questions

- Whether **precedence_ordinal** is per-ruleset only or may be overridden by host **policy_pin** — **execution-deferred**.

## Pseudo-code readiness (algorithm sketches)

```text
function buildSchedule(frame):
  candidates = eligibleRules(frame)
  ordered = evaluationOrder(candidates)  # 5.1.1 tuple sort
  byClass = groupBy(ordered, λ r: r.precedence_class)
  winners = []
  for class in deterministicClassOrder(byClass):
    for group in seamConflictGroups(byClass[class]):
      winners.append(resolveWinner(group))  # tuple → ordinal → fallback
  return Schedule(frame_id=frame.id, passes=["tuple_sort","precedence_resolve"], winners=winners)
```

## Tertiary slice GWT (GWT-5.1.2-A–K) — narrowed vs GWT-5.1.1-A–K

| ID | Given | When | Then | Evidence (narrowed here) |
| --- | --- | --- | --- | --- |
| GWT-5.1.2-A | **5.1.1** admitted manifest + frame inputs | Frame starts | **EvaluationFrame** identity is stable for replay | § Behavior |
| GWT-5.1.2-B | Eligible **RuleCandidate** set | Tuple sort completes | Order matches **5.1.1** before any precedence pass | § Behavior |
| GWT-5.1.2-C | Same **precedence_class** bucket | Pass 2 runs | Exactly one winner per **(seam_id, conflict_class)** at NL | § Behavior |
| GWT-5.1.2-D | **GWT-5.1.1-D** ordering | Precedence applies | Tuple order is consumed before class-internal ordinal | § Interfaces |
| GWT-5.1.2-E | **3.1.2** defer marker | Frame deferred | No authoritative RuleOutcome for deferred slice | § Behavior |
| GWT-5.1.2-F | **4.1.3** envelope | Outcomes emitted | Pass names + frame id are legible fields | § Scope |
| GWT-5.1.2-G | **GWT-5.1-G** Phase 2 boundary | Rule requests world change | Routes through Phase 2 — schedule does not bypass | Parent **5.1** |
| GWT-5.1.2-H | Cross-seam conflict | Only single-seam groups in scope | **5.1.3** owns matrix | § Edge cases |
| GWT-5.1.2-I | **GWT-5.1.1-I** observation inputs | Rule reads sim | **3.2.1** authority_class respected | **5.1** + Phase 3 |
| GWT-5.1.2-J | Operator swaps pin mid-campaign | New pin | New admission (**5.1.1**) + new frame schedule | § Behavior |
| GWT-5.1.2-K | Conceptual waiver | Validator advisory | Execution marketplace / CI gaps deferred | [[roadmap-state]] / [[distilled-core]] |

## Related

- CDR: [[Conceptual-Decision-Records/deepen-phase-5-1-2-kernel-eval-schedule-rule-ordering-2026-04-04-0715]]
