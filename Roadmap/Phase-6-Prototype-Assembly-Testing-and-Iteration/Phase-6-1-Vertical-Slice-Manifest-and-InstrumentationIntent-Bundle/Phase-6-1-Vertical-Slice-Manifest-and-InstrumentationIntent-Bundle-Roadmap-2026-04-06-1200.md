---
title: Phase 6.1 — Vertical slice manifest + InstrumentationIntent bundle (NL)
roadmap-level: secondary
phase-number: 6
subphase-index: "6.1"
project-id: godot-genesis-mythos-master
status: complete
priority: high
progress: 100
handoff_readiness: 86
created: 2026-04-06
tags:
  - roadmap
  - godot-genesis-mythos-master
  - phase-6
para-type: Project
links:
  - "[[Phase-6-Prototype-Assembly-Testing-and-Iteration-Roadmap-2026-03-30-0430]]"
  - "[[Conceptual-Decision-Records/deepen-phase-6-1-bundle-remint-post-rollback-2026-04-06-1200]]"
  - "[[Phase-6-1-1-Manifest-Field-Registry-FeedbackRecord-and-Instrumentation-Envelope-Roadmap-2026-04-07-1245]]"
  - "[[decisions-log]]"
  - "[[workflow_state]]"
  - "[[Branches/phase-6-operator-rollback-20260405/Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle/Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle-Roadmap-2026-04-05-1615]]"
---

> [!note] Post-rollback remint (active tree)
> This note **re-mints** secondary **6.1** after operator subtree rollback ([[Branches/phase-6-operator-rollback-20260405/ROLLBACK-MANIFEST-20260405]]). Prior rolled-up copy (with tertiaries **6.1.1–6.1.3**) remains **audit-only** under the branch folder — do not treat archived wikilinks as live children on this tree.
> **Queue scope:** `pool-remint-611-godot-gmm-20260406120000Z` — next structural mint targets **tertiary 6.1.1** as **Manifest Field Registry** + **FeedbackRecord taxonomy** + **instrumentation envelope** (godot vertical slice), replacing the pre-rollback **admission-row / ticket-vocabulary** emphasis for **6.1.1**.

## Phase 6.1 — Vertical slice manifest + InstrumentationIntent bundle

First **secondary** under Phase **6** (post-rollback): a **named vertical slice manifest** (**Horizon-Q3**) as an NL authority bundle—**pinned phase references**, **session story ordering**, and a consolidated **InstrumentationIntent** catalog—so **GWT-6-A–K** evidence can narrow here and in **6.1.x** tertiaries without duplicating Phase **2–5** truth.

## Scope

**In scope (conceptual):**

- **Slice manifest (NL):** stable **`slice_id`** (`horizon_q3_v1`), **human label**, **pinned upstream anchors** (wikilinks to **2.7.x**, **3.x**, **4.x**, **5.x** as consumed by this slice), and **admission story** (first committed tick → bounded tick window) in one place.
- **InstrumentationIntent bundle:** **table of named probe loci** (worldgen stage family, tick closure boundary, rules **EvaluationFrame**, presentation envelope assembly)—each row: **intent_id**, **locus**, **consumer** (operator / lab / roadmap), **non-bypass citations** (upstream phase row forbids reinterpretation).
- **FeedbackRecord routing stub:** what qualifies as slice-local **FeedbackRecord** vs **decisions-log** promotion—**NL only**; wire formats **execution-deferred**.

**Out of scope:** concrete metric backends, dashboards, soak harnesses, perf SLAs, CI jobs, or **Roadmap/Execution/** mirrors until execution track is bootstrapped.

## Planned tertiary decomposition (active tree)

| Index | Intent | Notes |
| --- | --- | --- |
| **6.1.1** | **Manifest Field Registry** + **FeedbackRecord** taxonomy + **instrumentation envelope** | **Minted** — [[Phase-6-1-1-Manifest-Field-Registry-FeedbackRecord-and-Instrumentation-Envelope-Roadmap-2026-04-07-1245]] (`followup-deepen-phase611-after-pool-remint-613-20260407T123000Z`); **`mar.hq3.*`** stable IDs carried forward for **6.1.2**/**6.1.3** joins. |
| **6.1.2** | Bounded tick-window scenarios + sim-visible × checkpoint matrix | **Remint on active tree** — [[Phase-6-1-2-Bounded-Tick-Window-Scenarios-and-Sim-Visible-Classification-Matrix-Roadmap-2026-04-06-1215]] (`pool-remint-612-godot-gmm-20260406120001Z`). **`mar.*`** join keys — active **6.1.1** ([[Phase-6-1-1-Manifest-Field-Registry-FeedbackRecord-and-Instrumentation-Envelope-Roadmap-2026-04-07-1245]]). |
| **6.1.3** | ObservationChannel lane readout + **4.1.3** co-display | **Remint on active tree** — [[Phase-6-1-3-ObservationChannel-Lane-Readout-and-Presentation-Time-Co-Display-Roadmap-2026-04-07-1015]] (`pool-remint-613-godot-gmm-20260406120002Z`). **Out-of-order** vs **6.1.1** (operator queue). |

## Behavior (natural language)

1. **Manifest as single glue:** Operators and future tertiaries treat this note as the **slice phonebook**—which Phase **6** primary rows (**GWT-6-***) delegate into **6.1+** without re-deriving **2.x** commit semantics or **3.x** sim truth.
2. **InstrumentationIntent lifecycle:** Intents are **declared** here; **6.1.x** tertiaries **bind** acceptance language; execution **attaches** tools later.
3. **Ordering echo:** End-to-end ordering from Phase **6** primary (`admit → ticks → rules → perspective → presentation → feedback`) is **repeated with manifest-specific anchors**.

## Interfaces

**Upstream (Phase 6 primary):** Consumes **GWT-6-A–K** as parent checklist; this secondary does **not** widen primary Scope/Behavior.

**Upstream (Phases 2–5):** Manifest **pins** only—[[Phase-2-7-3-Shadow-to-Live-Parity-Admission-Ticket-Redemption-and-First-Committed-Tick-Trace-Roadmap-2026-03-30-1800]], [[Phase-2-7-1-Simulation-Entry-Bootstrap-and-Deterministic-First-Tick-Contract-Roadmap-2026-04-01-0116]], [[Phase-3-1-3-Sim-Visible-Classification-and-DM-Overwrite-Channel-Mapping-Roadmap-2026-04-02-0035]], [[Phase-3-1-4-Persistence-Checkpoint-Boundaries-Roadmap-2026-04-02-2240]], [[Phase-3-4-1-Handoff-Seam-Catalog-and-Consumer-Contract-Rows-Roadmap-2026-04-03-0115]], [[Phase-4-1-3-Consumer-Surface-Framing-and-Presentation-Time-Validation-Roadmap-2026-04-03-2110]], [[Phase-5-1-1-Ruleset-Manifest-Seam-Admission-and-Deterministic-Evaluation-Order-Roadmap-2026-04-04-0010]] (manifest field discipline).

**Downstream (6.1.x):** To be minted—see **Planned tertiary decomposition**.

## Manifest (Horizon-Q3) — slice phonebook (skeleton)

### Admission (manifest subsection)

- **Pinned:** [[Phase-2-7-3-Shadow-to-Live-Parity-Admission-Ticket-Redemption-and-First-Committed-Tick-Trace-Roadmap-2026-03-30-1800]]; [[Phase-2-7-1-Simulation-Entry-Bootstrap-and-Deterministic-First-Tick-Contract-Roadmap-2026-04-01-0116]].
- **Tertiary 6.1.1 (minted):** [[Phase-6-1-1-Manifest-Field-Registry-FeedbackRecord-and-Instrumentation-Envelope-Roadmap-2026-04-07-1245]] — manifest **field registry** rows + **FeedbackRecord** typing + **instrumentation envelope** hooks—**NL** binding to **5.1.1** seam admission vocabulary (**no** alternate admission authority vs **2.7.x**).

### Tick window + sim-visible (manifest subsection)

- **Pinned:** [[Phase-3-1-2-Tick-Scheduling-Defer-Merge-and-Work-Queue-Policy-Roadmap-2026-04-02-0020]]; [[Phase-3-1-3-Sim-Visible-Classification-and-DM-Overwrite-Channel-Mapping-Roadmap-2026-04-02-0035]]; [[Phase-3-1-4-Persistence-Checkpoint-Boundaries-Roadmap-2026-04-02-2240]].

### Operator readout

- **Pinned:** [[Phase-3-2-1-Observation-Channel-Taxonomy-Roadmap-2026-03-30-2310]]; [[Phase-4-1-3-Consumer-Surface-Framing-and-Presentation-Time-Validation-Roadmap-2026-04-03-2110]].

### Orchestration inputs (4.2.x as inputs only)

| Input family | Wikilink pin |
| --- | --- |
| Session / transition hooks | [[Phase-4-2-1-Session-Scoped-Orchestration-Hooks-and-Perspective-Transition-Graph-Roadmap-2026-04-03-2125]] |
| Transition outcome ledger | [[Phase-4-2-2-Transition-Outcome-Ledger-and-Lane-Projection-Parity-Roadmap-2026-03-31-1200]] |
| Replay closure / repair / escalation | [[Phase-4-2-3-Replay-Closure-Orchestration-Repair-and-Operator-Escalation-Readout-Roadmap-2026-03-31-1500]] |

### InstrumentationIntent (starter rows)

| intent_id | locus | consumer | Non-bypass citation |
| --- | --- | --- | --- |
| `instr.worldgen_stage` | Worldgen stage family boundary | lab / roadmap | [[Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-03-30-0430]] (phase spine—no perf SLA) |
| `instr.tick_closure` | Tick closure + sim-visible export | operator / lab | [[Phase-3-1-3-Sim-Visible-Classification-and-DM-Overwrite-Channel-Mapping-Roadmap-2026-04-02-0035]] |
| `instr.rules_eval_frame` | Rules **EvaluationFrame** pin | lab | [[Phase-5-1-2-Kernel-Evaluation-Schedule-and-Rule-Ordering-Roadmap-2026-04-04-0715]] |
| `instr.presentation_envelope` | Presentation envelope assembly | operator | [[Phase-4-1-3-Consumer-Surface-Framing-and-Presentation-Time-Validation-Roadmap-2026-04-03-2110]] |

### FeedbackRecord vs decisions-log (NL)

- **FeedbackRecord:** slice-local annotations that do **not** reopen upstream authority.
- **decisions-log** promotion: only when a new **D-*** row is required; otherwise follow **GWT-6-H** on the Phase **6** primary.

## Edge cases

- **Partial slice:** Explicit **deferred legs** in Open questions—no silent full-vertical claim.
- **Pin drift:** Load failure vocabulary inherited from **5.x**; manifest names **failure class** only.

## Open questions

- Field-registry **minimum column set** for manifest rows vs **5.1.1** seam keys (to be closed in **6.1.1**).
- Whether **FeedbackRecord** carries a **severity / promotion** enum at conceptual depth or only on execution track.

## Pseudo-code readiness

Secondary depth: **interfaces + tables**; **no** pseudo-code required. **6.1.1+** may add mid-technical sketches.

## Phase-level **GWT-6 → 6.1** delegation (tertiary chain on active tree)

| GWT-6 row | Delegates into **6.1** (evidence status) |
| --- | --- |
| A (admission / manifest rows / field registry) | **Closed** — [[Phase-6-1-1-Manifest-Field-Registry-FeedbackRecord-and-Instrumentation-Envelope-Roadmap-2026-04-07-1245]] (`handoff_readiness` **86**; mint queue `followup-deepen-phase611-after-pool-remint-613-20260407T123000Z`) |
| B (tick window / sim-visible classification) | **Closed** — [[Phase-6-1-2-Bounded-Tick-Window-Scenarios-and-Sim-Visible-Classification-Matrix-Roadmap-2026-04-06-1215]] (`handoff_readiness` **87**; queue `pool-remint-612-godot-gmm-20260406120001Z`); **out-of-order** mint before **6.1.1** resolved by active **6.1.1** mint **2026-04-07** |
| C–K (observation / presentation / operator readout) | **Closed** — [[Phase-6-1-3-ObservationChannel-Lane-Readout-and-Presentation-Time-Co-Display-Roadmap-2026-04-07-1015]] (`handoff_readiness` **88**; queue `pool-remint-613-godot-gmm-20260406120002Z`) |

## Secondary rollup closure

**Complete (2026-04-07)** — **NL checklist** + **GWT-6.1-A–K** parity vs tertiaries **6.1.1–6.1.3** on the **active** remint tree; **GWT-6 → 6.1** delegation rows **A–K** bound to evidence notes above; **InstrumentationIntent** starter rows aligned to tertiary **instr.*** / **ii.*** citations; rollup CDR [[Conceptual-Decision-Records/deepen-phase-6-1-secondary-rollup-nl-gwt-active-tree-2026-04-07-1805]]. **Queue reconcile:** stale `user_guidance` on `followup-deepen-phase611-after-pool-remint-613-20260407T123000Z` described **mint 6.1.1** — **superseded** by **2026-04-07 12:45** mint; this deepen executed **secondary 6.1 rollup** per authoritative [[workflow_state]] **`current_subphase_index: "6.1"`** + terminal ## Log.

### NL handoff checklist (secondary rollup — closure)

| Checklist row | Status |
| --- | --- |
| **Scope** | **Pass** — manifest phonebook + InstrumentationIntent + FeedbackRecord routing (see § Scope / manifest subsections). |
| **Behavior** | **Pass** — actors/ordering echo **6.1.x** tertiary bindings without second sim truth. |
| **Interfaces** | **Pass** — upstream pins + downstream tertiary wikilinks + **6.1.3** readout matrix joins **6.1.2**/**4.1.3**. |
| **Edge cases** | **Pass** — partial slice + pin drift called out; execution-deferred legs labeled. |
| **Open questions** | **Pass** — remainder explicitly execution-deferred or listed in tertiaries. |
| **Pseudo-code readiness** | **N/A at secondary** — mid-technical sketches live in **6.1.1–6.1.3** per depth contract. |

### **GWT-6.1-A–K** (secondary rollup parity vs **6.1.1 / 6.1.2 / 6.1.3**)

| GWT-6.1 | Parity statement | Tertiary evidence |
| --- | --- | --- |
| **A** | Manifest field registry + **5.1.1** seam vocabulary + **`mar.hq3.*`** stable IDs | **6.1.1** **GWT-6.1.1-A–D** |
| **B** | Tick-window scenarios + sim-visible × checkpoint matrix + **`stws.*`** joins | **6.1.2** **GWT-6.1.2-A–D** |
| **C** | ObservationChannel readout + presentation-time co-display + **`sor.*`** joins | **6.1.3** **GWT-6.1.3-A–D** |
| **D–K** | Delegation coverage + traceability columns + InstrumentationIntent alignment rows | **6.1.1**/**6.1.2**/**6.1.3** respective **GWT-6.1.x-E–K** tables |

### InstrumentationIntent — tertiary chain closure (active tree)

| intent_id | Tertiary bind | Closure |
| --- | --- | --- |
| `instr.worldgen_stage` | **6.1.x** stage-family pins | Named in manifest + **6.1.2** scenario catalog |
| `instr.tick_closure` | **6.1.2** | `stws.hq3.*` alignment row |
| `instr.rules_eval_frame` | **5.1.2** pin (upstream) | Non-bypass cite preserved |
| `instr.presentation_envelope` | **6.1.3** | `sor.hq3.*` matrix + **4.1.3** |

## Related

- Rollback archive (read-only diff): [[Branches/phase-6-operator-rollback-20260405/Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle/Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle-Roadmap-2026-04-05-1615]]
