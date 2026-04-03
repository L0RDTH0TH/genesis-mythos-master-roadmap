---
title: Phase 5 — Rule System Integration and Extensibility
roadmap-level: primary
phase-number: 5
subphase-index: "5"
project-id: genesis-mythos-master
status: active
priority: high
progress: 50
phase5_primary_checklist: complete
handoff_readiness: 85
created: 2026-03-30
tags:
  - roadmap
  - genesis-mythos-master
  - phase
para-type: Project
links:
  - "[[genesis-mythos-master-Roadmap-2026-03-30-0430]]"
  - "[[1-Projects/genesis-mythos-master/Roadmap/Branches/phase-5-1-secondary-rollback-2026-04-02/Phase-5-1-Rule-Primitives-Plugin-Host-and-Conflict-Precedence-Roadmap-2026-04-03-2310]]"
---

## Phase 5 — Rule System Integration and Extensibility

Integrate a **core rules engine** with **plugin rulesets**, demonstrate **deterministic swaps** (generators / events / styles), and document **ecosystem seams** for community remixing—while **consuming** Phase **4** **perspective / session orchestration** signals and Phase **3** **sim-visible** facts **without** re-deriving **3.1.4** checkpoint authority or **4.1.3** presentation-time validation semantics.

## Conceptual waiver & safety invariants

- **Conceptual track waiver (rollup / CI / HR):** Design authority on the **conceptual** track does **not** claim execution closure for a public plugin marketplace, signed-package CI, full sandboxing, or HR-style proof tables—those are **execution-deferred** per [[3-Resources/Second-Brain/Docs/Dual-Roadmap-Track|Dual-Roadmap-Track]].
- **Upstream continuity:** Phase 5 **reads** **ObservationChannel** / **authority_class** expectations via Phase **4** consumer surfaces; **session transition** and **orchestration repair** semantics bind to **4.2.x** without inventing a second **replay** truth; **presentation-time validation** legibility contracts remain anchored to **4.1.3**—rules may **label** outcomes for operators but do **not** replace Phase **2** commit gates.
- **`GMM-2.4.5-*`:** remain **reference-only** anchors for execution-track audit/compare artifacts.

- [x] Core implementation task — **Rule primitives + plugin registration + conflict hooks** (NL contract at primary; typed bodies under **5.1+**)
- [x] Core implementation task — **Initial ruleset plugin (one)** proving extensibility (NL contract; manifest + load order under secondaries)
- [x] Glue / integration task — **Docs + examples** for swapping generators/events/styles (ecosystem seam story—execution packaging deferred)

### Progress semantics (frontmatter)

`progress` is **0–100** for this note’s conceptual slice depth: **~25** = primary NL checklist complete enough to mint secondaries; **~50+** = secondaries drafted; **100** = phase-ready for execution handoff (still execution CI deferred).

## Scope

**In scope:** **rules engine kernel** (evaluate, schedule, emit structured outcomes); **plugin ruleset** lifecycle (register, activate, deactivate, version pin); **conflict policy** when two rules target the same seam (deterministic precedence + operator-visible explanation); **integration hooks** into Phase **4** mode/orchestration and Phase **3** sim-visible events; **ecosystem documentation** for swapping **generators**, **events**, and **styles** as pluggable bundles.

**Out of scope:** concrete programming language, package registry, cryptographic signing, remote marketplace, full sandbox OS isolation, and perf SLAs (execution-deferred).

## Behavior (natural language)

**Actors:** **Rules kernel** (loads rulesets, evaluates rule graphs, emits **RuleOutcome** records), **plugin host** (discovers manifests, validates declared seams), **orchestration layer** (Phase **4.2** transition / repair tokens may **trigger** rule evaluation—rules do not author commits), **operators** (see legible **explanations** tied to **4.1.3** presentation envelope), **simulation** (continues to emit **sim-visible** facts per Phase **3**—rules consume, do not mutate sim core directly).

**Inputs:** **sim-visible** event frames and **SeamId**-keyed consumer rows (via Phase **4** adaptation paths), **session orchestration** signals (**4.2.1** transition graph, **4.2.3** repair/escalation readouts as **inputs** to rule triggers), **ruleset manifests** (version, declared conflicts, generator/event/style slots).

**Outputs:** **deterministic rule decisions** (approve / deny / defer / reroute) as structured records suitable for **operator readout** and downstream **presentation**; **no** silent override of Phase **2** **commit** / **deny** / **defer** semantics—rules **propose** orchestration intents that remain subject to upstream orchestration + validation stories.

**Ordering (high level):** `ingest sim-visible + orchestration signals → select active rulesets → evaluate rule chain → emit RuleOutcome → (parallel) presentation/narrative surfaces render per 4.1.3 legibility contracts`.

## Interfaces

**Upstream (Phase 3–4):** consumes **ObservationChannel** taxonomy and **authority_class** discipline (**3.2.1**); **does not** weaken **3.1.4** checkpoint boundaries. Consumes **4.2** **orchestration** artifacts as **triggers**, not as persistence writers. **4.1.3** **presentation-time validation** defines how **rule explanations** surface to operators—rules do not redefine validation gates.

**Downstream (Phase 6+):** exposes stable **ruleset manifest** + **plugin slot** contracts for tooling and community packaging (NL only; wire formats execution-deferred).

**Outward guarantees:**

- **Determinism:** given the same **committed** world snapshot + same ruleset pin + same orchestration signal stream, rule outcomes are **replay-stable** (aligns Phase **2** lineage story).
- **Conflict transparency:** conflicting rules produce a **single** deterministic winner per declared **precedence class** + **operator-visible** diff (no silent merge).

## Edge cases

- **Rule asks for structural regen:** emit **regen request** intent consistent with Phase **3** **overwrite** vs **structural** story—rules do not bypass Phase **2** validation.
- **Plugin mismatch / bad manifest:** host **rejects load** with deterministic error surface (execution packaging deferred; NL requires **named failure class** at primary).
- **High churn operator toggles:** mode switches (**4.2**) may reorder **which** rules are eligible—kernel must not assume a static rule graph without **explicit** rebinding event (NL).

## Open questions

- Minimum **ruleset manifest** fields for community sharing (version pin, seam declarations, conflict class) before execution prototypes.
- Whether **generator** vs **event** vs **style** swaps share one **plugin envelope** or three (execution-deferred packaging).

## Pseudo-code readiness

At **primary** conceptual depth, **no pseudo-code** is required. **Interfaces + slot graph** for secondaries start at **5.1**.

## Phase-level **GWT-5-A–K** (primary checklist scaffold — evidence tightens after secondaries **5.1+**)

> **Primary checklist:** This table binds **phase-level** hooks to **upstream** Phase **3–4** contracts. Rows cite **planned** secondary **5.1** as the first structural home for engine/plugin NL unless otherwise noted.

| ID | Given | When | Then | Evidence (primary / planned) |
| --- | --- | --- | --- | --- |
| **GWT-5-A** | Phase **3** **sim-visible** facts on bus | Kernel evaluates rules | Rules consume **observation**-class inputs without inventing sim mutations | Primary § Behavior; archived secondary 5.1 slice § **GWT-5.1-A** ([[1-Projects/genesis-mythos-master/Roadmap/Branches/phase-5-1-secondary-rollback-2026-04-02/Phase-5-1-Rule-Primitives-Plugin-Host-and-Conflict-Precedence-Roadmap-2026-04-03-2310]]) |
| **GWT-5-B** | Phase **4.2.1** **PerspectiveTransitionGraph** | Mode/orchestration transition | Rule triggers may **attach** to transition events—do not author commits | **4.2.1**; primary § Interfaces |
| **GWT-5-C** | Phase **4.2.2** **TransitionOutcomeLedger** | Outcome recorded | Rule outcomes remain **consistent** with ledger rows (no duplicate truth) | **4.2.2**; archived secondary 5.1 slice § **GWT-5.1-C** ([[1-Projects/genesis-mythos-master/Roadmap/Branches/phase-5-1-secondary-rollback-2026-04-02/Phase-5-1-Rule-Primitives-Plugin-Host-and-Conflict-Precedence-Roadmap-2026-04-03-2310]]) |
| **GWT-5-D** | Phase **4.2.3** **OrchestrationRepairToken** | Repair path | Rules may **propose** repair-shaped intents—escalation readout remains authoritative | **4.2.3**; primary § Edge |
| **GWT-5-E** | Phase **4.1.3** **presentation envelope** | Operator reads outcome | Explanations are **legible** per presentation-time validation story | **4.1.3**; primary § Behavior |
| **GWT-5-F** | Plugin manifest declares **conflict class** | Two rules collide | Deterministic **precedence** + operator-visible explanation | Primary § Interfaces |
| **GWT-5-G** | Ruleset **version pin** | Load requested | Kernel **rejects** incompatible pins with deterministic error class | Primary § Edge |
| **GWT-5-H** | Phase **2** commit boundary | Rule proposes world change | Proposal routes through **structural regen** / validation story—no bypass | Primary § Behavior; **2.4.x** refs via decisions-log |
| **GWT-5-I** | **D-3.4-*** consumer granularity rows | Bundle policy applies | Rules respect **SeamId** rows—no second consumer truth | [[decisions-log]]; **3.4.1** |
| **GWT-5-J** | Community **ecosystem** seam | Operator swaps generator/event/style | Swap is **documented** and **replay-stable** under manifest pin (execution packaging deferred) | Primary § Scope |
| **GWT-5-K** | Conceptual waiver | Validator advisory codes | Execution-only gaps (marketplace, CI) **deferred**—not blocking primary checklist | [[roadmap-state]], [[distilled-core]] |

`handoff_readiness` **85** after primary NL checklist (CDR [[Conceptual-Decision-Records/deepen-phase-5-primary-checklist-rule-system-2026-03-31-1200]]). The deepen note for **secondary 5.1** ([[1-Projects/genesis-mythos-master/Roadmap/Branches/phase-5-1-secondary-rollback-2026-04-02/Phase-5-1-Rule-Primitives-Plugin-Host-and-Conflict-Precedence-Roadmap-2026-04-03-2310]]) was **removed from the active tree** on **2026-04-02** (manifest: [[1-Projects/genesis-mythos-master/Roadmap/Branches/phase-5-1-secondary-rollback-2026-04-02/ROLLBACK-MANIFEST-2026-04-02]]); next structural cursor is **re-mint secondary 5.1** per [[workflow_state]] **`current_subphase_index: "5.1"`**. Stale queue text on **`followup-deepen-phase4-41-rollup-gmm-20260403T211500Z`** remains historical only.

## Subphases & notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-5-Rule-System-Integration-and-Extensibility"
WHERE roadmap-level = "primary" OR roadmap-level = "secondary" OR roadmap-level = "tertiary"
SORT subphase-index ASC, file.name ASC
```
