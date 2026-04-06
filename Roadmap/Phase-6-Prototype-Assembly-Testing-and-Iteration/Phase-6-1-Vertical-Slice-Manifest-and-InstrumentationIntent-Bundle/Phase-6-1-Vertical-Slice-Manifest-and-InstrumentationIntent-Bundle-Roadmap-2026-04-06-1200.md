---
title: Phase 6.1 — Vertical slice manifest + InstrumentationIntent bundle (NL)
roadmap-level: secondary
phase-number: 6
subphase-index: "6.1"
project-id: sandbox-genesis-mythos-master
status: active
priority: high
progress: 45
handoff_readiness: 82
created: 2026-04-06
tags:
  - roadmap
  - sandbox-genesis-mythos-master
  - phase-6
para-type: Project
links:
  - "[[Phase-6-Prototype-Assembly-Testing-and-Iteration-Roadmap-2026-03-30-0430]]"
  - "[[Conceptual-Decision-Records/deepen-phase-6-1-bundle-remint-post-rollback-2026-04-06-1200]]"
  - "[[decisions-log]]"
  - "[[workflow_state]]"
  - "[[Branches/phase-6-operator-rollback-20260405/Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle/Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle-Roadmap-2026-04-05-1615]]"
---

> [!note] Post-rollback remint (active tree)
> This note **re-mints** secondary **6.1** after operator subtree rollback ([[Branches/phase-6-operator-rollback-20260405/ROLLBACK-MANIFEST-20260405]]). Prior rolled-up copy (with tertiaries **6.1.1–6.1.3**) remains **audit-only** under the branch folder — do not treat archived wikilinks as live children on this tree.
> **Queue scope:** `pool-remint-611-sandbox-gmm-20260406120000Z` — next structural mint targets **tertiary 6.1.1** as **Manifest Field Registry** + **FeedbackRecord taxonomy** + **instrumentation envelope** (sandbox vertical slice), replacing the pre-rollback **admission-row / ticket-vocabulary** emphasis for **6.1.1**.

## Phase 6.1 — Vertical slice manifest + InstrumentationIntent bundle

First **secondary** under Phase **6** (post-rollback): a **named vertical slice manifest** (**Horizon-Q3**) as an NL authority bundle—**pinned phase references**, **session story ordering**, and a consolidated **InstrumentationIntent** catalog—so **GWT-6-A–K** evidence can narrow here and in **6.1.x** tertiaries without duplicating Phase **2–5** truth.

## Scope

**In scope (conceptual):**

- **Slice manifest (NL):** stable **`slice_id`** (`horizon_q3_v1`), **human label**, **pinned upstream anchors** (wikilinks to **2.7.x**, **3.x**, **4.x**, **5.x** as consumed by this slice), and **admission story** (first committed tick → bounded tick window) in one place.
- **InstrumentationIntent bundle:** **table of named probe loci** (worldgen stage family, tick closure boundary, rules **EvaluationFrame**, presentation envelope assembly)—each row: **intent_id**, **locus**, **consumer** (operator / lab / roadmap), **non-bypass citations** (upstream phase row forbids reinterpretation).
- **FeedbackRecord routing stub:** what qualifies as slice-local **FeedbackRecord** vs **decisions-log** promotion—**NL only**; wire formats **execution-deferred**.

**Out of scope:** concrete metric backends, dashboards, soak harnesses, perf SLAs, CI jobs, or **Roadmap/Execution/** mirrors until execution track is bootstrapped.

## Planned tertiary decomposition (not yet minted on this tree)

| Index | Intent | Notes |
| --- | --- | --- |
| **6.1.1** | **Manifest Field Registry** + **FeedbackRecord** taxonomy + **instrumentation envelope** | Operator-directed remint; binds manifest rows to **RulesetManifest** / **5.1.1** seam vocabulary and **FeedbackRecord** shape without reopening **2.x** commit authority. |
| **6.1.2** | Bounded tick-window scenarios + sim-visible × checkpoint matrix | TBD after **6.1.1**. |
| **6.1.3** | ObservationChannel lane readout + **4.1.3** co-display | TBD after **6.1.2**. |

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
- **Tertiary 6.1.1 (planned):** Manifest **field registry** rows + **FeedbackRecord** typing + **instrumentation envelope** hooks—**NL** binding to **5.1.1** seam admission vocabulary (**no** alternate admission authority vs **2.7.x**).

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

## Phase-level **GWT-6 → 6.1** delegation (pending tertiary chain)

| GWT-6 row | Delegates into **6.1** (evidence status) |
| --- | --- |
| A–C | **Pending** — filled after **6.1.1–6.1.3** mint + rollup |
| D–K | **Pending** — same |

## Secondary rollup closure

**Not started** — requires tertiaries **6.1.1–6.1.3** on the **active** tree and NL + **GWT-6.1** parity pass.

## Related

- Rollback archive (read-only diff): [[Branches/phase-6-operator-rollback-20260405/Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle/Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle-Roadmap-2026-04-05-1615]]
