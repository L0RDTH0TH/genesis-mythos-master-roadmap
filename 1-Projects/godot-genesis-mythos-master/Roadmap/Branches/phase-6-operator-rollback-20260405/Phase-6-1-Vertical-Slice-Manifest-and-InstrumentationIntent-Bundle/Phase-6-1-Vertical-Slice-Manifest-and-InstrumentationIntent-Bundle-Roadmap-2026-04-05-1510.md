---
title: Phase 6.1 — Vertical slice manifest and InstrumentationIntent bundle
roadmap-level: secondary
phase-number: 6
subphase-index: "6.1"
project-id: godot-genesis-mythos-master
status: complete
priority: high
progress: 88
handoff_readiness: 86
created: 2026-04-05
tags:
  - roadmap
  - godot-genesis-mythos-master
  - phase-6
para-type: Project
links:
  - "[[Phase-6-Prototype-Assembly-Testing-and-Iteration-Roadmap-2026-03-30-0430]]"
  - "[[Phase-6-1-1-Manifest-Field-Registry-FeedbackRecord-Taxonomy-and-Instrumentation-Envelope-Roadmap-2026-04-05-2342]]"
  - "[[decisions-log]]"
  - "[[distilled-core]]"
  - "[[workflow_state]]"
  - "[[Conceptual-Decision-Records/deepen-phase-6-1-secondary-rollup-nl-gwt-2026-04-06-0130]]"
---

> [!note] #handoff-review
> `handoff_readiness: 86` — **Rollup (2026-04-06):** **NL checklist** + **GWT-6.1-A–K** parity vs tertiary **6.1.1** on [[Phase-6-1-1-Manifest-Field-Registry-FeedbackRecord-Taxonomy-and-Instrumentation-Envelope-Roadmap-2026-04-05-2342]]; CDR [[Conceptual-Decision-Records/deepen-phase-6-1-secondary-rollup-nl-gwt-2026-04-06-0130]]. Instrumentation wire formats, CI perf gates, dashboards, and marketplace packaging remain **execution-deferred** per conceptual waiver + queue `user_guidance`. **Honors** primary **GWT-6** delegation: Evidence **A/D/F/G/H** still cite this secondary until Phase **6 primary rollup** refreshes primary **GWT-6** Evidence rows. **No** `Roadmap/Execution/**` unless execution track is bootstrapped.
>
> **Mint queue (historical):** `followup-deepen-phase6-61-mint-slice-manifest-godot-gmm-20260405T151000Z` · `parallel_track: godot`. **Rollup queue:** `followup-deepen-phase61-rollup-post-611-godot-gmm-20260406T000000Z` · `parent_run_id: eat-queue-godot-20260405-layer1`.

## Phase 6.1 — Vertical slice manifest + InstrumentationIntent bundle

This secondary **names and binds** the **Horizon-Q3** slice as a **manifest-level** contract: which upstream secondaries are **pinned references**, how **InstrumentationIntent** rows attach to **NL probe loci**, and how **FeedbackRecord** routes without rewriting **2.x** / **3.x** / **5.x** authority.

## Scope

**In scope:**

- **VerticalSliceManifest (NL)** — stable **`slice_id: Horizon-Q3`**, **pinned phase references** (secondary/tertiary wikilinks only—no new consumer rows), **session story spine** (`admit → ticks → rules → perspective → operator readout`) aligned to Phase **6** primary **Behavior**.
- **InstrumentationIntent bundle** — **four** named intents (below) with **attach locus**, **metric class** (name only), **upstream gate** citation, and **execution-deferred** wire-format stub.
- **GWT-6.1-A–K** table narrowed vs primary **GWT-6-A–K** and **GWT-6** **Evidence** delegation rows (**A/D/F/G/H**).

**Out of scope:**

- Concrete profilers, dashboards, CI perf gates, soak harnesses, or marketplace packaging (**execution-deferred** per conceptual waiver).
- Redefining **3.4.1** **SeamId** rows, **5.1** evaluation order, or **2.x** commit envelopes—**6.1** **consumes** them by reference only.

## NL checklist (rollup closure)

- [x] **VerticalSliceManifest** row documents **slice_id**, narrative spine, pinned refs, **SeamId** discipline, and **D-5.1.3-matrix-vs-manifest** stance (**open**, non-blocking).
- [x] **Four** **InstrumentationIntent** rows name **II-6.1-*** loci with attach locus, metric class (name only), and upstream gate citations (**execution-deferred** wire stub).
- [x] **FeedbackRecord** routing defers taxonomy detail to tertiary **6.1.1** without upstream body overwrite.
- [x] **GWT-6.1-A–K** table present and mapped to **GWT-6.1.1-A–K** evidence (see § GWT parity).
- [x] **Conceptual waiver** explicit for perf/CI/dashboard/marketplace gaps (**not** authoritative open gates on conceptual track).

## Behavior (natural language)

1. **Manifest registration:** Operators treat **VerticalSliceManifest** as the **single named slice** under Phase **6** until a later note expands multi-slice policy. **Pin** references: **2.7.3** (entry), **3.1.x** bus + **3.1.4** checkpoints, **4.1.3** presentation legibility, **4.2.1–4.2.3** transition/repair **vocabulary as inputs**, **5.1**/**5.2** ruleset / bundle doc story.
2. **InstrumentationIntent usage:** Each intent is **advisory** for execution track: it states **what** to measure and **where** the hook conceptually sits in the NL spine—**not** a profiler API.
3. **FeedbackRecord routing:** Failures, surprises, and contradictions are **classified** using the **slice-local taxonomy** defined on [[Phase-6-1-1-Manifest-Field-Registry-FeedbackRecord-Taxonomy-and-Instrumentation-Envelope-Roadmap-2026-04-05-2342]] and **promote** to [[decisions-log]] / [[roadmap-state]] **without** mutating upstream phase notes.
4. **Non-bypass:** The manifest **never** introduces a shadow commit path, alternate **SeamId** catalog, or second **RuleOutcome** truth—**replays** remain **2.x** + **3.x** + **5.x** aligned.

## VerticalSliceManifest (NL record)

| Field | Value / contract |
| --- | --- |
| **slice_id** | `Horizon-Q3` |
| **narrative spine** | `SimulationEntryBootstrap (2.7) → bounded tick window (3.x) → pinned ruleset evaluation (5.x) on sim-visible + 4.2-shaped inputs → 4.1.3 operator surfaces → feedback + instrumentation capture` |
| **pinned refs (minimum)** | [[Phase-2-7-3-Shadow-to-Live-Parity-Admission-Ticket-Redemption-and-First-Committed-Tick-Trace-Roadmap-2026-03-30-1800]] · [[Phase-3-1-Sim-Tick-and-Event-Bus-Spine-Roadmap-2026-03-30-2213]] · [[Phase-3-1-4-Persistence-Checkpoint-Boundaries-Roadmap-2026-04-02-2240]] · [[Phase-4-1-3-Consumer-Surface-Framing-and-Presentation-Time-Validation-Roadmap-2026-04-03-2110]] · [[Phase-4-2-1-Session-Scoped-Orchestration-Hooks-and-Perspective-Transition-Graph-Roadmap-2026-04-03-2125]] · [[Phase-4-2-2-Transition-Outcome-Ledger-and-Lane-Projection-Parity-Roadmap-2026-03-31-1200]] · [[Phase-4-2-3-Replay-Closure-Orchestration-Repair-and-Operator-Escalation-Readout-Roadmap-2026-03-31-1500]] · [[Phase-5-1-Rule-Primitives-Plugin-Host-and-Conflict-Precedence-Roadmap-2026-04-03-2330]] · [[Phase-5-2-Ecosystem-Generator-Event-Style-Swap-Documentation-Seam-Roadmap-2026-04-04-2100]] |
| **SeamId discipline** | Only **3.4.1** catalog seams may appear in slice glue tables (**GWT-6-I**). |
| **D-5.1.3-matrix-vs-manifest** | **Open** per [[decisions-log]]—manifest **references** reader-default from **5.2** docs; **non-blocking** for **6.1**. |

## InstrumentationIntent bundle (four loci)

| Intent id | Attach locus (NL) | Metric class (name only) | Upstream gate / citation |
| --- | --- | --- | --- |
| **II-6.1-WORLDGEN** | World admission / graph stages before first committed tick | `HotspotWorldgenStages` | **2.7.1** / **2.7.3** admission + first-tick trace |
| **II-6.1-TICKCLOSE** | Tick scheduler closure + **3.1.4** checkpoint boundary | `TickClosureAndCheckpointBoundary` | **3.1.2** defer-merge + **3.1.4** persistence checkpoints |
| **II-6.1-RULEFRAME** | Rules evaluation frame consuming **sim-visible** + **4.2** inputs | `RuleEvaluationFrame` | **5.1.2** schedule + **5.1.3** matrix vocabulary |
| **II-6.1-PRESENT** | **4.1.3** presentation-time envelope assembly | `PresentationEnvelopeAssembly` | **4.1.3** legibility + **3.2.1** channel classification |

**Bundle rule:** Intents are **slice-scoped**; expanding to **per-subsystem cards** is a **6.1.x** tertiary decision (**Open questions**).

## Interfaces

**Upstream:** Phase **6** primary ([[Phase-6-Prototype-Assembly-Testing-and-Iteration-Roadmap-2026-03-30-0430]]) — **GWT-6** rows **A/D/F/G/H** delegate Evidence here.

**Sideways:** [[Phase-3-4-1-Handoff-Seam-Catalog-and-Consumer-Contract-Rows-Roadmap-2026-04-03-0115]] for **SeamId** keys; Phase **5** secondaries for pin + doc seams.

**Downstream:** Tertiary **6.1.1** minted — [[Phase-6-1-1-Manifest-Field-Registry-FeedbackRecord-Taxonomy-and-Instrumentation-Envelope-Roadmap-2026-04-05-2342]] (manifest **field registry**, **FeedbackRecord** taxonomy, **InstrumentationIntentEnvelope**). Further **6.1.x** packaging splits remain **execution-deferred** unless queued.

**Outward guarantees:**

- **One** named vertical slice manifest **on disk** for **Horizon-Q3**.
- **Four** **InstrumentationIntent** rows **named** and **traceable** to upstream phases.
- **Replay stance:** manifest text **never** weakens **2.x** commit / **3.x** tick / **5.x** outcome authority.

## Edge cases

- **Partial subgraph:** If execution lab only runs **ticks + rules**, manifest **must** list **deferred** legs explicitly (**GWT-6.1-F**).
- **Stale pin:** Incompatible ruleset / bundle doc → **deterministic load failure** vocabulary from **5.x**—manifest **names** the failure class, does not redefine host behavior.
- **High ctx util:** **RECAL-ROAD** remains available; **6.1** does not block on execution rollup codes (**conceptual waiver**).

## Open questions

- **Resolved (tertiary 6.1.1):** **FeedbackRecord** taxonomy rows + **InstrumentationIntentEnvelope** shape vs **II-6.1-*** — see [[Phase-6-1-1-Manifest-Field-Registry-FeedbackRecord-Taxonomy-and-Instrumentation-Envelope-Roadmap-2026-04-05-2342]] (**GWT-6.1.1-A–K**).
- **Resolved (secondary 6.1 rollup, 2026-04-06):** NL checklist + **GWT-6.1-A–K** parity vs **6.1.1** — CDR [[Conceptual-Decision-Records/deepen-phase-6-1-secondary-rollup-nl-gwt-2026-04-06-0130]]; queue `followup-deepen-phase61-rollup-post-611-godot-gmm-20260406T000000Z`.
- **Per-subsystem** instrumentation cards beyond the **single envelope** row-set — **execution-deferred** when packaging splits land.

## Pseudo-code readiness

At **secondary** conceptual depth, **no pseudo-code**. Typed manifests / enums start at **6.1.1+**.

## Secondary slice GWT (GWT-6.1-A–K) — narrowed vs primary **GWT-6**

| ID | Given | When | Then | Evidence (this slice) |
| --- | --- | --- | --- | --- |
| **GWT-6.1-A** | **2.7.x** admission story | Operator reads manifest | **Horizon-Q3** cites **2.7.3** as slice entry authority | § VerticalSliceManifest |
| **GWT-6.1-B** | **3.x** tick + sim-visible | Slice runs bounded ticks | Manifest pins **3.1** + **3.1.4** checkpoint boundary | § Pinned refs |
| **GWT-6.1-C** | **4.x** lanes | Operator observes | **4.1.3** + **3.2.1** classification cited in manifest spine | § Behavior |
| **GWT-6.1-D** | **4.2.x** tokens | Orchestration fires | Manifest states **inputs only**—no persistence author claims | § Behavior |
| **GWT-6.1-E** | **5.x** **RuleOutcome** | Rules evaluate | Pinned **5.1**/**5.2**—no second consumer truth | § Pinned refs |
| **GWT-6.1-F** | Phase **6** scope | Operator runs **Horizon-Q3** | **VerticalSliceManifest** row exists with **slice_id** + spine | § VerticalSliceManifest |
| **GWT-6.1-G** | Hotspot loci | Lab pass | **Four** **InstrumentationIntent** rows name attach points | § InstrumentationIntent bundle |
| **GWT-6.1-H** | **FeedbackRecord** | Iteration | Routing clause to [[decisions-log]] / [[roadmap-state]] without upstream overwrite | § Behavior |
| **GWT-6.1-I** | **3.4.1** **SeamId** | Slice references seams | Only catalog seams in glue | § VerticalSliceManifest |
| **GWT-6.1-J** | **3.1.3** DM classes | DM acts | Manifest spine preserves **live** vs **structural regen** labels | § Behavior; Phase **3** primary |
| **GWT-6.1-K** | Conceptual waiver | Validator advisory | Execution perf / CI / marketplace gaps **deferred** explicitly | [[roadmap-state]], [[distilled-core]] |

## GWT-6.1 ↔ GWT-6.1.1 parity (rollup)

| **GWT-6.1** | Parity claim (secondary NL) | **GWT-6.1.1** evidence row (tertiary) |
| --- | --- | --- |
| **A** | **Horizon-Q3** cites **2.7.3** as slice entry | **A** — registry columns for manifest doc |
| **B** | Pins **3.1** + **3.1.4** checkpoint boundary | **B** — **deferred_legs** vs omitted rows |
| **C** | **4.1.3** + **3.2.1** in spine | **I** — **II-6.1-PRESENT** cites **4.1.3** / **3.2.1** |
| **D** | **4.2.x** inputs only (no persistence authority) | **F** — **upstream_gate_citation** resolves |
| **E** | Pinned **5.1**/**5.2** — no second truth | **J** — **II-6.1-RULEFRAME** cites **5.1.2** / **5.1.3** |
| **F** | Manifest row + spine exists | **A** + **B** (manifest + partial pass) |
| **G** | Four **InstrumentationIntent** rows | **E** — four **InstrumentationIntentEnvelope** rows |
| **H** | **FeedbackRecord** routing without upstream overwrite | **C** + **D** — taxonomy + **FR-6.1-CONTRADICTION** routing |
| **I** | Only **3.4.1** catalog seams | **H** — glue **SeamId** keys only |
| **J** | **3.1.3** live vs structural regen labels | **F** / spine alignment via upstream citations |
| **K** | Conceptual waiver explicit | **K** — perf/CI/dashboard **execution-deferred** |

## Research integration

- None this run (**research_pre_deepen** not enabled on queue entry; vault-first **pattern_only**).

## Tertiary notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/godot-genesis-mythos-master/Roadmap/Phase-6-Prototype-Assembly-Testing-and-Iteration/Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle"
WHERE roadmap-level = "secondary" OR roadmap-level = "tertiary" OR roadmap-level = "task"
SORT subphase-index ASC, file.name ASC
```
