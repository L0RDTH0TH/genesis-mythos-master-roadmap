---
title: Phase 6.1 — Vertical slice manifest + InstrumentationIntent bundle (NL)
roadmap-level: secondary
phase-number: 6
subphase-index: "6.1"
project-id: sandbox-genesis-mythos-master
status: in-progress
priority: high
progress: 55
handoff_readiness: 85
created: 2026-04-05
tags:
  - roadmap
  - sandbox-genesis-mythos-master
  - phase-6
para-type: Project
links:
  - "[[Phase-6-1-2-Bounded-Tick-Window-Scenarios-and-Sim-Visible-Classification-Matrix-Roadmap-2026-04-06-0800]]"
  - "[[Phase-6-1-1-Manifest-Admission-Row-Bindings-and-Admission-Ticket-Vocabulary-Roadmap-2026-04-05-1918]]"
  - "[[Phase-6-Prototype-Assembly-Testing-and-Iteration-Roadmap-2026-03-30-0430]]"
  - "[[Conceptual-Decision-Records/deepen-phase-6-1-vertical-slice-manifest-instrumentation-2026-04-05-1615]]"
  - "[[decisions-log]]"
  - "[[workflow_state]]"
---

## Phase 6.1 — Vertical slice manifest + InstrumentationIntent bundle

First **secondary** under Phase **6**: a **named vertical slice manifest** (**Horizon-Q3**) as an NL authority bundle—**pinned phase references**, **session story ordering**, and a consolidated **InstrumentationIntent** catalog—so **GWT-6-A–K** evidence can narrow here and in **6.1.x** tertiaries without duplicating Phase **2–5** truth.

## Scope

**In scope (conceptual):**

- **Slice manifest (NL):** stable **`slice_id`** (e.g. `horizon_q3_v1`), **human label**, **pinned upstream anchors** (wikilinks to **2.7.x**, **3.x**, **4.x**, **5.x** secondaries/tertiaries as consumed by this slice—not exhaustive PMG scope), and **admission story** (first committed tick → bounded tick window) in one place.
- **InstrumentationIntent bundle:** a **table of named probe loci** (worldgen stage family, tick closure boundary, rules **EvaluationFrame**, presentation envelope assembly)—each row: **intent_id**, **locus**, **consumer** (operator / lab / roadmap), **non-bypass citations** (which upstream phase row forbids reinterpretation).
- **FeedbackRecord routing stub:** what qualifies as slice-local **FeedbackRecord** vs **decisions-log** promotion—**NL only**; ticketing wire formats **execution-deferred**.

**Out of scope:** concrete metric backends, dashboards, soak harnesses, perf SLAs, CI jobs, or **Roadmap/Execution/** mirror notes until execution track is bootstrapped.

## Behavior (natural language)

1. **Manifest as single glue:** Operators and future tertiaries treat this note as the **slice phonebook**—which Phase **6** primary rows (**GWT-6-***) delegate into **6.1+** without re-deriving **2.x** commit semantics or **3.x** sim truth.
2. **InstrumentationIntent lifecycle:** Intents are **declared** here; **6.1.x** tertiaries may **bind** each intent to finer acceptance language; execution track **attaches** tools later—conceptual track does not claim closure.
3. **Ordering echo:** The end-to-end ordering from Phase **6** primary (`admit → ticks → rules → perspective → presentation → feedback`) is **repeated with manifest-specific anchors** so junior readers need not jump across five phase folders for the slice story alone.

## Interfaces

**Upstream (Phase 6 primary):** Consumes **GWT-6-A–K** as the **parent checklist**; this secondary **does not** widen or contradict primary Scope/Behavior.

**Upstream (Phases 2–5):** Manifest **pins** wikilinks only—**2.7.3** admission / first committed tick, **3.1.x** bus + **3.1.4** checkpoints, **3.4.1** **SeamId** rows referenced by slice glue, **4.1.3** presentation-time validation, **4.2.x** tokens as **inputs**, **5.x** ruleset pin + **RuleOutcome** story.

**Downstream (6.1.x tertiaries):** May decompose manifest rows into **acceptance tables**, **scenario sketches**, or **rollup closure**—one tertiary chain expected before **secondary 6.1 rollup**.

**Rollup:** Secondary **6.1** NL+GWT rollup closure is explicitly deferred to the **6.1.x** tertiary chain per conceptual track policy (`missing_roll_up_gates` advisory on **conceptual_v1**, not a design-handoff blocker).

**Outward guarantees:**

- **No second truth:** Manifest cannot introduce alternate commit, checkpoint, or consumer-seam semantics; pins are **references**, not redefinitions.
- **Traceability:** Every **InstrumentationIntent** row cites at least one **non-bypass** upstream anchor as **`[[note]]` + explicit section heading** (or stable in-note anchor); coarse **2.x** / **3.x** family labels alone are **not** sufficient.

## Manifest (Horizon-Q3) — slice phonebook

Subsections below are the **structural homes** referenced by the **GWT-6 → 6.1** delegation table; content is **pins + NL glue** only—no new upstream semantics.

### Admission (manifest subsection)

- **Row-ID + ticket vocabulary binding:** [[Phase-6-1-1-Manifest-Admission-Row-Bindings-and-Admission-Ticket-Vocabulary-Roadmap-2026-04-05-1918]] — stable **`manifest_admission_row_id`** catalog ↔ **2.7.x** `admission_ticket_id` / **SimulationEntryBootstrap** / **FirstCommittedTickTrace** (NL); satisfies **GWT-6-A** evidence via **GWT-6.1.1-*** table.
- **`slice_id`:** `horizon_q3_v1` — human label: **Horizon-Q3 vertical slice (conceptual)**.
- **Pinned:** [[Phase-2-7-3-Shadow-to-Live-Parity-Admission-Ticket-Redemption-and-First-Committed-Tick-Trace-Roadmap-2026-03-30-1800]] (admission / first committed tick story); [[Phase-2-7-1-Simulation-Entry-Bootstrap-and-Deterministic-First-Tick-Contract-Roadmap-2026-04-01-0116]] (bootstrap + first-tick contract).

### Tick window + sim-visible classification (manifest subsection)

- **Bounded scenarios + matrix:** [[Phase-6-1-2-Bounded-Tick-Window-Scenarios-and-Sim-Visible-Classification-Matrix-Roadmap-2026-04-06-0800]] — **`slice_tick_window_scenario_id`** catalog + **sim-visible × checkpoint** matrix (**GWT-6.1.2-A–K**); satisfies **GWT-6-B** via narrowed evidence table.
- **Pinned:** [[Phase-3-1-3-Sim-Visible-Classification-and-DM-Overwrite-Channel-Mapping-Roadmap-2026-04-02-0035]]; [[Phase-3-1-4-Persistence-Checkpoint-Boundaries-Roadmap-2026-04-02-2240]]; [[Phase-3-1-2-Tick-Scheduling-Defer-Merge-and-Work-Queue-Policy-Roadmap-2026-04-02-0020]] (defer-merge / work-queue closure).

### Operator readout (ObservationChannel + 4.1.3 co-display)

- **Pinned:** [[Phase-3-2-1-Observation-Channel-Taxonomy-Roadmap-2026-03-30-2310]]; [[Phase-4-1-3-Consumer-Surface-Framing-and-Presentation-Time-Validation-Roadmap-2026-04-03-2110]].
- **Lane/readout matrix:** [[Phase-6-1-3-ObservationChannel-Lane-Readout-and-Presentation-Time-Co-Display-Roadmap-2026-04-06-2130]] — **`slice_operator_readout_id`** catalog + **channel → PresentationEnvelope** matrix (**GWT-6.1.3-A–K**); satisfies **GWT-6-C** via narrowed evidence table.

### Orchestration inputs (4.2.x tokens as inputs only)

| Input family | Wikilink pin (read-only) |
| --- | --- |
| Session / transition hooks | [[Phase-4-2-1-Session-Scoped-Orchestration-Hooks-and-Perspective-Transition-Graph-Roadmap-2026-04-03-2125]] |
| Transition outcome ledger | [[Phase-4-2-2-Transition-Outcome-Ledger-and-Lane-Projection-Parity-Roadmap-2026-03-31-1200]] |
| Replay closure / repair / escalation readout | [[Phase-4-2-3-Replay-Closure-Orchestration-Repair-and-Operator-Escalation-Readout-Roadmap-2026-03-31-1500]] |

### SeamId pin list (catalog seams only)

- **Catalog authority:** [[Phase-3-4-1-Handoff-Seam-Catalog-and-Consumer-Contract-Rows-Roadmap-2026-04-03-0115]] — slice glue references **only** seams present in that catalog; tertiaries **6.1.x** may enumerate concrete **SeamId** rows.

### DM acts (3.1.3 overwrite classes echo)

- **Pinned:** [[Phase-3-1-3-Sim-Visible-Classification-and-DM-Overwrite-Channel-Mapping-Roadmap-2026-04-02-0035]] — **live** vs **structural regen** labels persist through slice narrative without inventing alternate DM persistence.

### FeedbackRecord vs decisions-log routing (NL)

- **FeedbackRecord:** slice-local operator/lab annotations that do **not** reopen upstream phase authority.
- **decisions-log** promotion: only when a new **D-*** class row is required; otherwise follow **GWT-6-H** on [[Phase-6-Prototype-Assembly-Testing-and-Iteration-Roadmap-2026-03-30-0430]] (primary checklist table).

## Edge cases

- **Partial slice:** If the manifest lists a **minimal subgraph** (e.g. ticks + rules only), **explicit deferred legs** must appear in **Open questions**—no silent “full vertical” claim.
- **Pin drift:** Incompatible ruleset / bundle pins → **deterministic load failure** vocabulary inherited from **5.x**; manifest only names the **failure class**, not new error codes.
- **High context pressure:** Large pin lists should stay **tabular**; narrative depth moves to **6.1.x**, not unbounded appendix here.

## Open questions

- Minimum **manifest** field set for **lab ↔ roadmap** automation (beyond wikilinks)—**execution-deferred** schema.
- Whether **InstrumentationIntent** rows should carry a **priority tier** for lab burn-down (P0/P1) at **secondary** depth or only after **6.1.1** mint.

## Pseudo-code readiness

**Secondary conceptual depth:** **No pseudo-code** required. **Algorithm sketches** may begin in **6.1.1+** tertiaries when binding intents to measurable checks.

## GWT-6 → 6.1 delegation table (primary rows narrowed to this secondary)

> **Contract:** Phase **6** primary **GWT-6-A–K** **Evidence** column cites **this note + future 6.1.x** for slice-local proof; primary table remains NL-only anchors.
> **Delegation middle column** references the named subsections under **## Manifest (Horizon-Q3) — slice phonebook** above.

| Primary ID | Delegation to **6.1** (this note) | Tertiary follow-up (TBD) |
| --- | --- | --- |
| **GWT-6-A** | Manifest **admission** subsection pins **2.7.x** + first committed tick story | [[Phase-6-1-1-Manifest-Admission-Row-Bindings-and-Admission-Ticket-Vocabulary-Roadmap-2026-04-05-1918]] — `manifest_admission_row_id` ↔ **2.7.x** ticket vocabulary (**GWT-6.1.1-***) |
| **GWT-6-B** | Manifest **tick window** + **sim-visible** classification pins **3.x** | [[Phase-6-1-2-Bounded-Tick-Window-Scenarios-and-Sim-Visible-Classification-Matrix-Roadmap-2026-04-06-0800]] — **`slice_tick_window_scenario_id`** + matrix (**GWT-6.1.2-***) |
| **GWT-6-C** | **ObservationChannel** + **4.1.3** co-display pinned in manifest **operator readout** subsection | [[Phase-6-1-3-ObservationChannel-Lane-Readout-and-Presentation-Time-Co-Display-Roadmap-2026-04-06-2130]] — **`slice_operator_readout_id`** + envelope matrix (**GWT-6.1.3-***) |
| **GWT-6-D** | **4.2.x** tokens listed as **inputs** only in manifest **orchestration inputs** table | **6.1.x** — trigger vocabulary closure |
| **GWT-6-E** | **Ruleset pin** + **RuleOutcome** rows referenced; **SeamId** catalog pins **3.4.1** | **6.1.x** — outcome ↔ seam row binding |
| **GWT-6-F** | **Horizon-Q3** **slice_id** + end-to-end **story ordering** paragraph | Rollup narrative vs **6.1.x** chain |
| **GWT-6-G** | **InstrumentationIntent** bundle table (probe loci) | **6.1.x** — per-locus acceptance |
| **GWT-6-H** | **FeedbackRecord** vs **decisions-log** routing rules (NL) | **6.1.x** — example feedback cards |
| **GWT-6-I** | Manifest **SeamId** pin list — **catalog seams only** | **6.1.x** — seam coverage checklist |
| **GWT-6-J** | **3.1.3** DM overwrite classes echoed in manifest **DM acts** subsection | **6.1.x** — overwrite class scenario rows |
| **GWT-6-K** | Waiver restatement: execution benchmarks / CI / marketplace **out of scope** | Reference **roadmap-state** / **distilled-core** |

## InstrumentationIntent bundle (NL catalog)

| intent_id | locus (NL) | Non-bypass citation (wikilink + heading) | consumer |
| --- | --- | --- | --- |
| `ii.worldgen.stage_family` | Procedural graph **stage family** boundary before sim handoff | [[Phase-2-1-Pipeline-Stages-Seed-to-World-Roadmap-2026-03-30-2205]] § Scope / staged pipeline + [[Phase-2-7-3-Shadow-to-Live-Parity-Admission-Ticket-Redemption-and-First-Committed-Tick-Trace-Roadmap-2026-03-30-1800]] § Behavior (admission / first committed tick) | operator + lab |
| `ii.sim.tick_closure` | **Tick closure** record + **3.1.4** checkpoint alignment | [[Phase-3-1-3-Sim-Visible-Classification-and-DM-Overwrite-Channel-Mapping-Roadmap-2026-04-02-0035]] § Behavior + [[Phase-3-1-4-Persistence-Checkpoint-Boundaries-Roadmap-2026-04-02-2240]] § Behavior (checkpoints) | lab |
| `ii.rules.eval_frame` | **EvaluationFrame** admission vs **5.1.2** schedule story | [[Phase-5-1-2-Kernel-Evaluation-Schedule-and-Rule-Ordering-Roadmap-2026-04-04-0715]] § Behavior / schedule + [[Phase-4-1-3-Consumer-Surface-Framing-and-Presentation-Time-Validation-Roadmap-2026-04-03-2110]] § Behavior (presentation-time validation) | operator |
| `ii.presentation.envelope` | **4.1.3** presentation-time validation assembly | [[Phase-4-1-3-Consumer-Surface-Framing-and-Presentation-Time-Validation-Roadmap-2026-04-03-2110]] § Behavior + [[Phase-3-2-1-Observation-Channel-Taxonomy-Roadmap-2026-03-30-2310]] § Behavior (**preview_shadow** vs committed) | operator |
| `ii.feedback.promotion` | **FeedbackRecord** fields that may promote to **decisions-log** | [[Phase-6-Prototype-Assembly-Testing-and-Iteration-Roadmap-2026-03-30-0430]] § Phase-level **GWT-6-A–K** row **GWT-6-H** | roadmap |

## Research integration

- None (vault-first; external benchmarks execution-deferred).

## Tertiary notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/sandbox-genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle"
WHERE roadmap-level = "secondary" OR roadmap-level = "tertiary" OR roadmap-level = "task"
SORT subphase-index ASC, file.name ASC
```
