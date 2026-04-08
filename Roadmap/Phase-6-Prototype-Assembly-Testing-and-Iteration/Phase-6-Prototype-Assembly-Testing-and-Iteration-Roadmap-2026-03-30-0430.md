---
title: Phase 6 — Prototype Assembly, Testing, and Iteration
roadmap-level: primary
phase-number: 6
subphase-index: "6"
project-id: godot-genesis-mythos-master
status: complete
priority: high
progress: 100
handoff_readiness: 86
handoff_gaps: []
handoff_audit_last: 2026-04-08T17:37:56Z
phase6_primary_checklist: complete
phase6_primary_rollup_nl_gwt: complete
created: 2026-03-30
tags:
  - roadmap
  - godot-genesis-mythos-master
  - phase
para-type: Project
links:
  - "[[godot-genesis-mythos-master-Roadmap-2026-03-30-0430]]"
  - "[[Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle-Roadmap-2026-04-06-1200]]"
  - "[[Phase-6-2-Scenario-Matrix-and-Feedback-Closure-Bundle-Roadmap-2026-04-08-1605]]"
  - "[[Phase-5-Rule-System-Integration-and-Extensibility-Roadmap-2026-03-30-0430]]"
  - "[[Phase-4-Perspective-Split-and-Control-Systems-Roadmap-2026-03-30-0430]]"
  - "[[Phase-3-Living-Simulation-and-Dynamic-Agency-Roadmap-2026-03-30-0430]]"
  - "[[Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-03-30-0430]]"
---

## Phase 6 — Prototype Assembly, Testing, and Iteration

Assemble the **Q3 2026** **vertical slice**: one **replay-stable** path from **world admission** through **sim ticks**, **rules evaluation**, **perspective / orchestration** transitions, and **operator-visible outcomes**—with **instrumentation hooks** and **feedback capture** feeding [[roadmap-state]] / [[decisions-log]]—**without** claiming marketplace packaging, signed CI, perf SLAs, or full production hardening (**execution-deferred** per conceptual waiver).

## Conceptual waiver & safety invariants

- **Conceptual track waiver (rollup / CI / HR / perf):** Phase **6** **NL authority** does **not** close execution benchmarks, soak tests, A/B harnesses, or HR-style proof tables—those are **execution-deferred** per [[3-Resources/Second-Brain/Docs/Dual-Roadmap-Track|Dual-Roadmap-Track]].
- **Upstream non-bypass:** The slice **consumes** Phase **2** commit / deny / defer semantics (**2.4.x**), Phase **3** **sim-visible** facts + **3.1.4** checkpoint boundaries, Phase **4** **ObservationChannel** + **4.1.3** presentation-time validation legibility, and Phase **5** **RuleOutcome** records—**no** second truth for commits, checkpoints, or ledger rows.
- **`GMM-2.4.5-*`:** remain **reference-only** anchors for execution-track audit/compare artifacts.
- **`D-5.1.3-matrix-vs-manifest`:** remains **open** per [[decisions-log]]—**non-blocking** for Phase **6** primary checklist; resolution target **execution** / later secondaries.

- [ ] Core implementation task — **Vertical slice integration** (end-to-end **NL** session path binding Phases **2.7 → 3 → 4 → 5**)
- [ ] Core implementation task — **Performance dry-runs + instrumentation** for gen/sim hotspots (**NL** hooks + named metric classes; execution tooling deferred)
- [ ] Glue / integration task — **Feedback loop** + iteration notes feeding [[roadmap-state]] / [[workflow_state]] **## Log** discipline

### Progress semantics (frontmatter)

`progress` is **0–100** for this note’s conceptual slice depth: **~25** = primary NL checklist complete enough to mint secondaries (**6.1+**); **~50+** = secondaries drafted; **100** = phase-ready for execution handoff (instrumentation closure still execution-deferred).

- **Cursor authority:** For **RESUME_ROADMAP** / Layer 1 routing, **`[[workflow_state]]` frontmatter `current_subphase_index`** is authoritative. After rollback ([[Branches/phase-6-operator-rollback-20260405/ROLLBACK-MANIFEST-20260405]]), **secondary 6.1** was re-minted **2026-04-07** — [[Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle-Roadmap-2026-04-06-1200]]; **secondary 6.1 rollup** complete **2026-04-07** (CDR [[Conceptual-Decision-Records/deepen-phase-6-1-secondary-rollup-nl-gwt-active-tree-2026-04-07-1805]]); **`phase6_primary_rollup_nl_gwt: complete`** **2026-04-07** (CDR [[Conceptual-Decision-Records/deepen-phase-6-primary-rollup-nl-gwt-active-tree-2026-04-07-2105]]); **`current_subphase_index: "6"`** — next operator **`advance-phase`** / **`bootstrap-execution-track`** / **RECAL** per PMG (no Phase **7** spine in this vault unless added).
- **Post-6.2 conceptual checkpoint (2026-04-08):** Secondary [[Phase-6-2-Scenario-Matrix-and-Feedback-Closure-Bundle-Roadmap-2026-04-08-1605]] reached rollup-complete status (`6.2.1`-`6.2.3` complete with `handoff_readiness: 86`) and remains linked as conceptual authority extension of Phase 6 primary; this pass keeps **`subphase-index: "6"`** stable to avoid cursor forks between primary and secondary closure narratives.

## Scope

**In scope (conceptual):** one **named vertical slice** (“**Horizon-Q3**” narrative) that **threads** **SimulationEntryBootstrap** / first-tick admission (**2.7.x**), **tick closure** + **sim-visible** export (**3.x**), **perspective / lane** binding (**4.x**), **orchestration transition / repair vocabulary** as **trigger inputs** (**4.2.x**—not persistence authors), and **rules kernel** outcomes (**5.x**) into a **single operator story**; **slice-level** **instrumentation** vocabulary (what to measure, where to attach probes—**not** concrete profilers); **feedback** routing (what gets promoted to roadmap decisions vs stays in lab notes).

**Out of scope:** target frame rates, cloud deploy topology, full test automation matrices, marketplace distribution, cryptographic signing, and **multi-slice** product scope (second slice = new phase note or **6.x** secondary).

## Behavior (natural language)

**Actors:** **Operator** (runs the slice, reads **4.1.3**-legible explanations + **5.x** rule diffs), **Session orchestration** (emits **4.2.x**-shaped **transition / repair** tokens as **inputs** to rules + presentation—**does not** replace **2.x** commit writers), **Rules kernel** (**5.x**—consumes **sim-visible** + orchestration signals), **Simulation core** (**3.x**—authoritative ticks + checkpoints per **3.1.4**), **World admission path** (**2.7.x**—deterministic entry + first committed tick trace).

**Inputs:** **Committed** world snapshot + **seed/bundle** pin (**2.x** lineage story), **sim-visible** event frames (**3.1.x** bus), **ObservationChannel**-classified consumer rows (**3.2.1** / **3.4.1** **SeamId** discipline), **PerspectiveTransitionGraph** events (**4.2.1**), **TransitionOutcomeLedger** rows (**4.2.2**), **OrchestrationRepairToken** / **OperatorEscalationReadout** labels when repair paths fire (**4.2.3**—as **vocabulary**, not re-derived semantics), **active ruleset pin** (**5.1** manifest story).

**Outputs:** **End-to-end narrative** of one session: **admit → tick(s) → optional rule outcomes → perspective transition → operator readout**, with **explicit** **non-bypass** citations to upstream phases; **InstrumentationIntent** records (named probe loci: worldgen stage, tick closure, rule evaluation frame, presentation envelope); **FeedbackRecord** stubs (what failed, what surprised, what contradicts NL—**feeds** [[decisions-log]] / **Conceptual autopilot**).

**Ordering (high level):** `admit world (2.7) → run bounded tick window (3.x) → evaluate pinned ruleset (5.x) on sim-visible + orchestration triggers (4.2 as inputs) → render operator surfaces per 4.1.3 → capture feedback + instrumentation intents`.

## Interfaces

**Upstream (Phase 2–5):** **2.7.3** **FirstCommittedTickTrace** / admission ticket story is the **slice entry** contract; **3.1.2**/**3.1.4** define **defer / checkpoint** boundaries the slice must **respect**; **3.4.1** **SeamId** rows are the **only** consumer seam keys the slice may **reference** for cross-phase glue; **4.1.3** defines how **rule explanations** and **orchestration readouts** **co-display** without merging authority; **5.1**/**5.2** define **manifest / bundle doc** identity the slice treats as **pinned inputs**.

**Downstream (execution track / tooling):** stable **slice manifest** descriptor (NL): slice id, pinned phase secondary refs, **instrumentation** hook list, **feedback** routing—**wire formats deferred**.

**Outward guarantees:**

- **Replay stance:** slice narrative is **consistent** with **2.x** deterministic lineage + **3.x** tick index monotonicity + **5.x** ruleset pin—**no** alternate “shadow commit” path inside the slice story.
- **Legibility:** every **deny / defer / repair** surfaced in the slice has a **traceable** upstream anchor (**2.4**, **3.1.2**, **4.2.3**, **5.x** conflict explanation)—**no** silent recovery.

## Edge cases

- **Rule outcome vs commit gate:** **RuleOutcome** may **propose** orchestration-shaped intents; **2.x** commit envelope remains **authoritative**—slice doc must show **hand-off**, not **merge**.
- **High ctx / partial slice:** if only **subsystem** depth is available, **name** the **minimal** subgraph (e.g. “ticks + rules only”) and **explicitly** list **deferred** legs—**do not** imply full vertical closure.
- **Stale pins:** incompatible **ruleset pin** or **bundle doc** revision → **deterministic load failure** class (**5.x** host story)—slice references that vocabulary **by name** only at primary depth.

## Open questions

- Minimum **slice manifest** fields for **lab ↔ roadmap** feedback (beyond free-text **FeedbackRecord**).
- Whether **instrumentation intents** are **one** envelope per slice or **per-subsystem** cards (**execution-deferred** packaging).

## Pseudo-code readiness

At **primary** conceptual depth, **no pseudo-code** is required. **Typed bodies** start at **6.1+** secondaries.

## Phase-level **GWT-6-A–K** (primary rollup — evidence bound to rolled-up secondary **6.1** + chain **6.1.1–6.1.3**)

> **Primary rollup (active tree):** NL checklist reaffirmed; **GWT-6-A–K** **Evidence** column cites **rolled-up** secondary **6.1** (rollup CDR [[Conceptual-Decision-Records/deepen-phase-6-1-secondary-rollup-nl-gwt-active-tree-2026-04-07-1805]]) and tertiaries **6.1.1–6.1.3** where rows delegate typed bodies. **Queue reconcile:** `followup-deepen-secondary-61-rollup-post-611-mint-20260407T133000Z` scoped **secondary 6.1 rollup** vs **`current_subphase_index: "6.1"`** — **superseded** by terminal ## Log **2026-04-07 18:05** (rollup already complete); this run executed **Phase 6 primary** rollup instead.

| ID | Given | When | Then | Evidence (primary / secondary **6.1** rollup) |
| --- | --- | --- | --- | --- |
| **GWT-6-A** | **2.7.x** admission + **6.1** manifest phonebook | Slice admits world | First committed tick + manifest rows bind **without** second admission truth | Primary § Behavior; **6.1** rollup § **GWT-6 → 6.1** row **A** + **6.1.1** registry ([[Phase-6-1-1-Manifest-Field-Registry-FeedbackRecord-and-Instrumentation-Envelope-Roadmap-2026-04-07-1245]]); secondary rollup CDR [[Conceptual-Decision-Records/deepen-phase-6-1-secondary-rollup-nl-gwt-active-tree-2026-04-07-1805]] |
| **GWT-6-B** | **3.x** tick + sim-visible classification | Bounded tick window runs | Sim-visible × checkpoint matrix stays consistent with **3.1.4** | **6.1** rollup § **GWT-6.1-B** + **6.1.2** `stws.*` ([[Phase-6-1-2-Bounded-Tick-Window-Scenarios-and-Sim-Visible-Classification-Matrix-Roadmap-2026-04-06-1215]]); rollup CDR [[Conceptual-Decision-Records/deepen-phase-6-1-secondary-rollup-nl-gwt-active-tree-2026-04-07-1805]] |
| **GWT-6-C** | **4.x** ObservationChannel + **4.1.3** presentation | Operator reads slice | Readout + presentation-time co-display stay **non-bypass** vs **2.x** commits | **6.1** rollup § **GWT-6.1-C** + **6.1.3** `sor.*` ([[Phase-6-1-3-ObservationChannel-Lane-Readout-and-Presentation-Time-Co-Display-Roadmap-2026-04-07-1015]]); primary § Interfaces |
| **GWT-6-D** | **4.2.x** orchestration tokens | Transition / repair fires | Tokens remain **inputs** to rules + presentation—**not** commit authors | Primary § Behavior; **4.2.1–4.2.3** pins in **6.1** manifest |
| **GWT-6-E** | **5.x** **RuleOutcome** + pinned ruleset | Rules evaluate | Outcomes consume **sim-visible** + orchestration **without** alternate sim truth | Primary § Scope; **5.1.1–5.1.3** seam refs via **6.1** manifest |
| **GWT-6-F** | **InstrumentationIntent** rows declared on **6.1** | Lab attaches probes | Named loci map to **6.1.x** binds—**no** concrete profilers at conceptual depth | **6.1** InstrumentationIntent closure table; secondary [[Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle-Roadmap-2026-04-06-1200]] |
| **GWT-6-G** | **FeedbackRecord** vs **decisions-log** routing | Operator annotates slice | Promotion rules stay NL-only; **D-*** rows only when new register entry required | Primary § Behavior; **6.1** FeedbackRecord stub |
| **GWT-6-H** | **2.x** commit / deny / defer | Slice proposes world change | Hand-off to **2.4.x** semantics—**no** shadow commit path | Primary § Edge; **2.7.3** trace refs |
| **GWT-6-I** | **D-5.1.3-matrix-vs-manifest** open | Operator loads bundle | Failure class vocabulary only—**not** closed here | [[decisions-log]]; conceptual waiver |
| **GWT-6-J** | **Horizon-Q3** slice id pinned | Session story told | End-to-end ordering matches manifest + **6.1** rollup NL closure | **6.1** secondary rollup § NL checklist; rollup CDR [[Conceptual-Decision-Records/deepen-phase-6-1-secondary-rollup-nl-gwt-active-tree-2026-04-07-1805]] |
| **GWT-6-K** | Conceptual waiver | Validator advisory (execution-only) | Benchmarks / CI / HR tables **deferred**—not blocking primary rollup | [[roadmap-state]], [[distilled-core]] dual-track lines |

**Primary rollup closure:** `phase6_primary_rollup_nl_gwt: complete`; `handoff_readiness` **86** (checklist CDR [[Conceptual-Decision-Records/deepen-phase-6-primary-checklist-prototype-assembly-2026-04-05-1510]]; rollup CDR [[Conceptual-Decision-Records/deepen-phase-6-primary-rollup-nl-gwt-active-tree-2026-04-07-2105]]). **Secondary 6.1 (rolled up, active tree):** [[Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle-Roadmap-2026-04-06-1200]] — **GWT-6.1-A–K** vs **6.1.1–6.1.3**; rollup CDR [[Conceptual-Decision-Records/deepen-phase-6-1-secondary-rollup-nl-gwt-active-tree-2026-04-07-1805]]. **Archive / branch diff:** prior **6.x** under [[Branches/phase-6-operator-rollback-20260405]] — audit-only.

## Subphases & notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/godot-genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration"
WHERE roadmap-level = "primary" OR roadmap-level = "secondary" OR roadmap-level = "tertiary"
SORT subphase-index ASC, file.name ASC
```
