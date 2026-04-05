---
title: Phase 6 — Prototype Assembly, Testing, and Iteration
roadmap-level: primary
phase-number: 6
subphase-index: "1"
project-id: sandbox-genesis-mythos-master
status: active
priority: high
progress: 28
phase6_primary_checklist: complete
handoff_readiness: 86
created: 2026-03-30
tags:
  - roadmap
  - sandbox-genesis-mythos-master
  - phase
para-type: Project
links:
  - "[[sandbox-genesis-mythos-master-Roadmap-2026-03-30-0430]]"
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

- [x] Core implementation task — **Vertical slice integration** (end-to-end **NL** session path binding Phases **2.7 → 3 → 4 → 5**)
- [x] Core implementation task — **Performance dry-runs + instrumentation** for gen/sim hotspots (**NL** hooks + named metric classes; execution tooling deferred)
- [x] Glue / integration task — **Feedback loop** + iteration notes feeding [[roadmap-state]] / [[workflow_state]] **## Log** discipline

### Progress semantics (frontmatter)

`progress` is **0–100** for this note’s conceptual slice depth: **~25** = primary NL checklist complete enough to mint secondaries (**6.1+**); **~50+** = secondaries drafted; **100** = phase-ready for execution handoff (instrumentation closure still execution-deferred).

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

## Phase-level **GWT-6-A–K** (primary checklist — evidence delegated to **6.1+**)

> **Delegation:** Detailed **Evidence** rows + **InstrumentationIntent** binding live in secondary **6.1** — [[Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle-Roadmap-2026-04-05-1615]] (**GWT-6 → 6.1** table). This primary table stays the **NL** anchor; do not duplicate authoritative probe rows here.

| ID | Given | When | Then | Evidence |
| --- | --- | --- | --- | --- |
| **GWT-6-A** | **2.7.x** admission + first committed tick | Slice starts | World enters sim under **2.7** contracts—**no** ad hoc bypass of entry gates | Primary § Behavior; **6.1** manifest row — [[Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle-Roadmap-2026-04-05-1615]] |
| **GWT-6-B** | **3.x** tick + **sim-visible** facts | Slice runs ticks | Events stay **sim-visible**-classified; **3.1.4** checkpoint story **respected** | Primary § Interfaces; [[Phase-3-Living-Simulation-and-Dynamic-Agency-Roadmap-2026-03-30-0430]] |
| **GWT-6-C** | **4.x** lanes + **ObservationChannel** | Operator observes | Presentation respects **preview_shadow** vs **committed_session** + **4.1.3** legibility | Primary § Behavior; [[Phase-4-Perspective-Split-and-Control-Systems-Roadmap-2026-03-30-0430]] |
| **GWT-6-D** | **4.2.x** transition / repair tokens | Orchestration fires | Tokens are **inputs** to rules / UX—**not** alternate persistence writers | Primary § Behavior; **4.2.1–4.2.3** |
| **GWT-6-E** | **5.x** **RuleOutcome** + pinned ruleset | Rules evaluate | Outcomes **consume** **SeamId** rows—**no** second consumer truth; **no** **2.x** commit bypass | Primary § Interfaces; [[Phase-5-Rule-System-Integration-and-Extensibility-Roadmap-2026-03-30-0430]] |
| **GWT-6-F** | Phase **6** scope | Operator runs **Horizon-Q3** slice | One **named** vertical path is **documented** end-to-end at NL | Primary § Scope; **6.1** pinned path — [[Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle-Roadmap-2026-04-05-1615]] |
| **GWT-6-G** | Hotspot loci (gen / sim / rules) | Dry-run / lab pass | **InstrumentationIntent** names **probe attach points** (execution tools deferred) | **6.1** **InstrumentationIntent** table — [[Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle-Roadmap-2026-04-05-1615]] |
| **GWT-6-H** | **FeedbackRecord** | Iteration | Findings route to [[roadmap-state]] / [[decisions-log]] **without** rewriting upstream phase authority | **6.1** feedback routing row — [[Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle-Roadmap-2026-04-05-1615]] |
| **GWT-6-I** | **3.4.1** **SeamId** catalog | Slice references seams | Only **catalog** seams appear in slice glue—**forbidden** reinterpretation rows | [[Phase-3-4-1-Handoff-Seam-Catalog-and-Consumer-Contract-Rows-Roadmap-2026-04-03-0115]] |
| **GWT-6-J** | **3.1.3** DM overwrite classes | DM acts in slice | **Live** vs **structural regen** labels persist through slice narrative | Primary § Edge; Phase **3** primary |
| **GWT-6-K** | Conceptual waiver | Validator advisory codes | Execution-only gaps (perf SLAs, CI, marketplace) **deferred**—not blocking primary checklist | [[roadmap-state]], [[distilled-core]] |

**Primary checklist closure:** `phase6_primary_checklist: complete`; `handoff_readiness` **86** (CDR [[Conceptual-Decision-Records/deepen-phase-6-primary-checklist-prototype-assembly-2026-04-05-1510]]). **Secondary 6.1 on disk + rollup complete:** [[Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle-Roadmap-2026-04-05-1615]] (`handoff_readiness` **86** after NL + **GWT-6.1-A–K** vs **6.1.1–6.1.3**; mint CDR [[Conceptual-Decision-Records/deepen-phase-6-1-vertical-slice-manifest-instrumentation-2026-04-05-1615]]; rollup CDR [[Conceptual-Decision-Records/deepen-phase-6-1-secondary-rollup-nl-gwt-2026-04-06-2145]]). **Canonical cursor:** [[workflow_state]] **`current_subphase_index: "6"`** — next **Phase 6 primary rollup** (NL + **GWT-6-A–K** vs rolled-up **6.1**). **No** `Roadmap/Execution/**` edits on conceptual track unless execution bootstrapped.

## Subphases & notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/sandbox-genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration"
WHERE roadmap-level = "primary" OR roadmap-level = "secondary" OR roadmap-level = "tertiary"
SORT subphase-index ASC, file.name ASC
```
