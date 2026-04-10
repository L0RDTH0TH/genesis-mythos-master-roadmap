---
title: Phase 6.1.1 — Manifest field registry + FeedbackRecord taxonomy + instrumentation envelope (NL)
roadmap-level: tertiary
phase-number: 6
subphase-index: "6.1.1"
project-id: godot-genesis-mythos-master
status: complete
priority: high
progress: 100
handoff_readiness: 86
created: 2026-04-07
tags:
  - roadmap
  - godot-genesis-mythos-master
  - phase-6
para-type: Project
links:
  - "[[Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle-Roadmap-2026-04-06-1200]]"
  - "[[Phase-5-1-1-RulesetManifest-Seam-Admission-and-Deterministic-Evaluation-Order-Roadmap-2026-04-04-0010]]"
  - "[[Phase-6-Prototype-Assembly-Testing-and-Iteration-Roadmap-2026-03-30-0430]]"
  - "[[Phase-6-1-2-Bounded-Tick-Window-Scenarios-and-Sim-Visible-Classification-Matrix-Roadmap-2026-04-06-1215]]"
  - "[[decisions-log]]"
  - "[[workflow_state]]"
---

## Phase 6.1.1 — Manifest field registry + FeedbackRecord taxonomy + instrumentation envelope

> [!note] Active-tree mint (post-rollback remint chain)
> This note **mints** tertiary **6.1.1** on the **active** tree under [[Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle-Roadmap-2026-04-06-1200]], scoped to operator queue **`followup-deepen-phase611-after-pool-remint-613-20260407T123000Z`**. It **replaces** the audit-only carry-forward from [[Branches/phase-6-operator-rollback-20260405/Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle/Phase-6-1-1-Manifest-Admission-Row-Bindings-and-Admission-Ticket-Vocabulary-Roadmap-2026-04-05-1918]] for **join-key stability**: the **`mar.hq3.*`** identifiers below are **the same strings** as the branch catalog so **6.1.2**/**6.1.3** scenarios can bind without forked admission truth. **Semantic emphasis** here is **field registry + FeedbackRecord + instrumentation envelope** (not a second **2.7.x** vocabulary).

This tertiary **implements** [[Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle-Roadmap-2026-04-06-1200]] § **Planned tertiary — 6.1.1** for **Horizon-Q3** (`slice_id: horizon_q3_v1`): a **manifest field registry** aligned to **5.1.1** seam admission vocabulary, a **FeedbackRecord** taxonomy for slice-local annotations, and an **instrumentation envelope** contract that wires **InstrumentationIntent** rows on secondary **6.1** to typed feedback without execution backends.

## Scope

**In scope (conceptual):**

- **Manifest field registry** — stable **`manifest_field_id`** rows naming **columns** / **slots** manifest rows may populate, each mapped to ≥1 **5.1.1** seam / tuple concept (**seam_id**, **admission** language, **evaluation order** hooks) — **NL join keys only**.
- **Slice join keys (`mar.*`)** — canonical **`manifest_admission_row_id`** values **`mar.hq3.slice_identity`**, **`mar.hq3.pin.2_7_3`**, **`mar.hq3.pin.2_7_1`** (same IDs as branch **6.1.1** audit) so **6.1.2** **`stws.hq3.*`** and **6.1.3** readout rows keep stable joins.
- **FeedbackRecord taxonomy** — **`feedback_kind`** classes (observation, instrumentation, operator_escalation_stub) + **promotion rule** to **decisions-log** vs **stay slice-local** — **NL only**; no wire schema.
- **Instrumentation envelope** — how **`instr.*`** intent rows from secondary **6.1** bind **manifest_field_id** + **`mar.*`** + optional **FeedbackRecord** without adding new **2.x** commit authority.

**Out of scope:** JSON/YAML schemas, metrics backends, `Roadmap/Execution/**`, changing **5.1.1** authoritative tables, or re-deriving **2.7.x** redemption semantics.

## Behavior (natural language)

1. **Registry-first:** Operators extending the slice manifest cite **`manifest_field_id`** when adding columns; **5.1.1** seam keys remain **upstream** — registry **maps**, not **edits**, **5.1.1**.
2. **Stable `mar.*`:** **`mar.hq3.*`** rows are **not** renamed vs branch audit; downstream **6.1.2**/**6.1.3** matrices remain valid.
3. **FeedbackRecord vs decisions-log:** Slice-local **`FeedbackRecord`** annotations that do **not** assert new **D-*** obligations stay on this slice; promotion follows **GWT-6-H** on the Phase **6** primary.

## Interfaces

**Upstream (secondary 6.1):** Consumes **InstrumentationIntent** starter rows + **Manifest** skeleton; does not add new **`slice_id`**.

**Upstream (5.1.1):** Read-only — [[Phase-5-1-1-RulesetManifest-Seam-Admission-and-Deterministic-Evaluation-Order-Roadmap-2026-04-04-0010]] seam admission + tuple vocabulary.

**Upstream (2.7.x):** **`mar.hq3.*`** pins remain read-only references — **no** new admission ticket types.

**Downstream (6.1.2 / 6.1.3):** **Active** join authority for **`mar.*`** + manifest field columns used in **`stws.hq3.*`** / **`sor.hq3.*`** rows — cite **this** note instead of branch-only audit.

**Outward guarantees:**

- **No second seam vocabulary:** Registry **maps** manifest fields to **5.1.1** words; it does not introduce alternate **seam_id** spellings.
- **Traceability:** Every registry row lists a **non-bypass** wikilink + heading anchor (GWT-6.1.1-G).

## Manifest field registry (Horizon-Q3)

| manifest_field_id | Human label (NL) | 5.1.1 seam / concept anchor | Notes |
| --- | --- | --- | --- |
| `mfr.hq3.seam_id` | **SeamId** column for manifest rows | [[Phase-5-1-1-RulesetManifest-Seam-Admission-and-Deterministic-Evaluation-Order-Roadmap-2026-04-04-0010]] § Interfaces — seam admission | Must match **3.4.1** consumer seam vocabulary when exported |
| `mfr.hq3.ruleset_id` | Ruleset manifest identity pin | Same note — **RulesetManifest** tuple / identity | Joins **5.2.1** slot/bundle doc identity when ecosystem docs apply |
| `mfr.hq3.eval_order_key` | Lexicographic + **precedence_class** ordering | Same note — evaluation order | Does not override **5.1.3** matrix — **cross-check** row only |
| `mfr.hq3.instrumentation_intent_ref` | Pointer to **`instr.*`** row on secondary **6.1** | Secondary **6.1** — InstrumentationIntent table | Binds envelope § below |

## Slice join keys (`mar.*`) — carried forward (stable IDs)

| manifest_admission_row_id | Human label (NL) | Authority |
| --- | --- | --- |
| `mar.hq3.slice_identity` | **slice_id** + human label | Horizon-Q3 slice phonebook |
| `mar.hq3.pin.2_7_3` | Pinned **2.7.3** redemption / first committed tick | [[Phase-2-7-3-Shadow-to-Live-Parity-Admission-Ticket-Redemption-and-First-Committed-Tick-Trace-Roadmap-2026-03-30-1800]] |
| `mar.hq3.pin.2_7_1` | Pinned **2.7.1** bootstrap + first-tick contract | [[Phase-2-7-1-Simulation-Entry-Bootstrap-and-Deterministic-First-Tick-Contract-Roadmap-2026-04-01-0116]] |

## FeedbackRecord taxonomy (NL)

| feedback_kind | Meaning | Promotion rule |
| --- | --- | --- |
| `fb.slice.observation` | Operator/lab note tied to **`manifest_field_id`** + **`mar.*`** | Stay slice-local unless **D-*** required |
| `fb.slice.instrumentation` | Structured note tied to **`instr.*`** + registry field | Stay slice-local; **decisions-log** only for new **D-*** |
| `fb.slice.escalation_stub` | Placeholder for **4.2.3**-style escalation vocabulary | **Label-only** — execution-deferred |

## Instrumentation envelope (NL)

**Envelope fields (conceptual):** **`slice_id`** + **`manifest_field_id`** + optional **`mar.*`** + **`instr.*`** reference + **`feedback_kind`** — describes how an instrumentation probe **labels** evidence without claiming new commit or sim authority.

**Binding rule:** **`instr.*`** rows on secondary **6.1** **must** cite ≥1 **`manifest_field_id`** when describing **where** probe output lands in the manifest story.

## GWT-6.1.1-A–K (narrowed vs GWT-6-A / secondary delegation)

| ID | Then (evidence expectation) | Primary / secondary anchor |
| --- | --- | --- |
| **GWT-6.1.1-A** | Registry lists ≥4 stable **`manifest_field_id`** values | **GWT-6-A** delegation |
| **GWT-6.1.1-B** | **`mar.*`** table lists **3** stable IDs matching branch audit | **6.1.2**/**6.1.3** joins |
| **GWT-6.1.1-C** | Each registry row maps to **5.1.1** heading anchor | **5.1.1** |
| **GWT-6.1.1-D** | FeedbackRecord taxonomy lists ≥3 **`feedback_kind`** rows | This note |
| **GWT-6.1.1-E** | Instrumentation envelope **Binding rule** explicit | Secondary **6.1** |
| **GWT-6.1.1-F** | **No second seam vocabulary** in **Outward guarantees** | This note |
| **GWT-6.1.1-G** | Traceability — **5.1.1** heading column populated | This note § Registry |
| **GWT-6.1.1-H** | Promotion rule distinguishes **FeedbackRecord** vs **decisions-log** | **GWT-6-H** |
| **GWT-6.1.1-I** | Downstream **6.1.2** may cite **`mar.*`** from **this** active note | [[Phase-6-1-2-Bounded-Tick-Window-Scenarios-and-Sim-Visible-Classification-Matrix-Roadmap-2026-04-06-1215]] |
| **GWT-6.1.1-J** | InstrumentationIntent **`instr.*`** alignment cited without new intent IDs | Secondary **6.1** |
| **GWT-6.1.1-K** | Open questions include ≥1 execution-deferred item | Below |

## Edge cases

- **Partial registry:** Unlisted **`manifest_field_id`** values are **out of slice** until secondary manifest expands — no silent coverage claim.
- **5.1.1 drift:** If **5.1.1** seam vocabulary changes on **execution** track, **conceptual** registry rows remain **NL map** — operator **RECAL** to re-bind.

## Open questions

- Whether **`feedback_kind`** carries a **severity** enum at conceptual depth or **execution-only** — **execution-deferred**.
- Minimum **`manifest_field_id`** column set vs **5.1.1** **SeamId** rows when ecosystem **5.2.x** docs apply — close in **secondary 6.1 rollup** or execution.

## Pseudo-code readiness

Tertiary depth **3** — **interfaces + tables**; algorithm sketches optional; **no** pseudo-code required for conceptual completion.

## Related

- Branch audit (read-only diff): [[Branches/phase-6-operator-rollback-20260405/Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle/Phase-6-1-1-Manifest-Admission-Row-Bindings-and-Admission-Ticket-Vocabulary-Roadmap-2026-04-05-1918]]
