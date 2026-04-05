---
title: Phase 6.1.1 — Manifest admission row IDs ↔ admission ticket vocabulary (NL)
roadmap-level: tertiary
phase-number: 6
subphase-index: "6.1.1"
project-id: sandbox-genesis-mythos-master
status: complete
priority: high
progress: 100
handoff_readiness: 86
created: 2026-04-05
tags:
  - roadmap
  - sandbox-genesis-mythos-master
  - phase-6
para-type: Project
links:
  - "[[Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle-Roadmap-2026-04-05-1615]]"
  - "[[Phase-6-Prototype-Assembly-Testing-and-Iteration-Roadmap-2026-03-30-0430]]"
  - "[[Phase-2-7-3-Shadow-to-Live-Parity-Admission-Ticket-Redemption-and-First-Committed-Tick-Trace-Roadmap-2026-03-30-1800]]"
  - "[[Phase-2-7-1-Simulation-Entry-Bootstrap-and-Deterministic-First-Tick-Contract-Roadmap-2026-04-01-0116]]"
  - "[[decisions-log]]"
  - "[[workflow_state]]"
---

## Phase 6.1.1 — Manifest admission row IDs ↔ admission ticket vocabulary

> [!note] Slice lifecycle vocabulary (state hygiene)
> Frontmatter **`status: complete`** + **`progress: 100`** mean this **tertiary slice is minted** (catalog + binding + GWT table on disk), consistent with [[roadmap-state]] “tertiary **6.1.1** minted” and **`handoff_readiness: 86`**. **`progress`** is **slice fill / mint completeness** (0–100), not context utilization. Secondary **6.1** NL+GWT rollup closure remains **explicitly deferred** to the **6.1.x** tertiary chain per conceptual track policy (`missing_roll_up_gates` advisory — not a blocker for this note’s mint-complete story). Repairs: queue `followup-l1-a5b-handoff-audit-611-sandbox-20260405T221600Z` (L1 post-LV `state_hygiene_failure`).

This tertiary **implements [[Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle-Roadmap-2026-04-05-1615]] § Manifest — Admission** for **Horizon-Q3** (`slice_id: horizon_q3_v1`): it assigns **stable manifest row IDs** to the NL admission story and **binds** each row to the **Phase 2.7.x admission ticket vocabulary** (`admission_ticket_id`, **SimulationEntryBootstrap**, **FirstCommittedTickTrace** redemption narrative) so **GWT-6-A** evidence can cite **one table** without re-deriving **2.7.3** semantics.

## Scope

**In scope (conceptual):**

- **Manifest admission row catalog** — named rows under the secondary’s **Admission (manifest subsection)** with immutable **`manifest_admission_row_id`** values used in slice MOCs, decisions-log references, and future lab cards.
- **Vocabulary binding table** — each row maps to **exactly one** primary ticket-field cluster from [[Phase-2-7-3-Shadow-to-Live-Parity-Admission-Ticket-Redemption-and-First-Committed-Tick-Trace-Roadmap-2026-03-30-1800]] (redemption / trace / parity) or [[Phase-2-7-1-Simulation-Entry-Bootstrap-and-Deterministic-First-Tick-Contract-Roadmap-2026-04-01-0116]] (bootstrap + first-tick contract), with **no new runtime fields** — labels and join keys only.
- **Delegation trace** — one column that states how the row supports **GWT-6-A** on [[Phase-6-Prototype-Assembly-Testing-and-Iteration-Roadmap-2026-03-30-0430]] (primary checklist) via the secondary delegation table.

**Out of scope:** execution schemas, JSON/YAML wire formats, `Roadmap/Execution/**` mirrors, perf or soak metrics, changing **2.7.x** authoritative definitions.

## Behavior (natural language)

1. **Row-first reading:** Operators and tertiaries cite **`manifest_admission_row_id`** when they mean a slice-local slice of the admission story; they cite **`admission_ticket_id`** only when referring to the **2.7.2 → 2.7.3** redemption artifact family.
2. **Single redeeming trace:** For this slice, **at most one** logical redemption path is active per **SimulationEntryBootstrap** identity per **2.7.2** tie-break; manifest rows **describe** that path, they do not fork new tie-break rules.
3. **Pinned NL only:** Wikilinks in the binding table point at **headings/sections** in **2.7.1** / **2.7.3**; manifest rows **do not** copy full Behavior blocks into Phase **6** notes.

## Interfaces

**Upstream (secondary 6.1):** Consumes **Manifest — Admission** bullets and **GWT-6 → 6.1** row **GWT-6-A**; does not widen manifest **slice_id** or pin list.

**Upstream (Phase 2.7.x):** Read-only — **2.7.3** redemption + **FirstCommittedTickTrace**; **2.7.1** admission gates + hook order preamble.

**Downstream (6.1.2+):** May attach **bounded tick window** / **ObservationChannel** matrices; must reference these **`manifest_admission_row_id`** values when extending admission-adjacent rows.

**Outward guarantees:**

- **No second redemption truth:** If a manifest row implies a ticket field, the **same** field name and semantics apply as in **2.7.3** § Behavior — no alternate spellings for `admission_ticket_id`.
- **Traceability:** Every row lists a **non-bypass** wikilink + heading anchor satisfying secondary **InstrumentationIntent** style citations (minimum one **2.7.x** cite per row).

## Manifest admission row catalog (Horizon-Q3)

| manifest_admission_row_id | Human label (NL) | Manifest subsection anchor |
| --- | --- | --- |
| `mar.hq3.slice_identity` | **slice_id** + human label for Horizon-Q3 | Secondary **Admission** — `slice_id` / human label |
| `mar.hq3.pin.2_7_3` | Pinned **2.7.3** admission / first committed tick story | Secondary **Admission** — pin **2.7.3** |
| `mar.hq3.pin.2_7_1` | Pinned **2.7.1** bootstrap + first-tick contract | Secondary **Admission** — pin **2.7.1** |

## Binding — manifest rows ↔ 2.7.x admission ticket vocabulary

| manifest_admission_row_id | 2.7.x vocabulary cluster (read-only) | Explicit heading anchor (GWT-6.1.1-G audit grep) | Binding sentence (NL) |
| --- | --- | --- | --- |
| `mar.hq3.slice_identity` | [[Phase-2-7-1-Simulation-Entry-Bootstrap-and-Deterministic-First-Tick-Contract-Roadmap-2026-04-01-0116]] — **SimulationEntryBootstrap** identity family | **2.7.1** — `## Behavior` + `## Interfaces` (simulation entry bootstrap + first-tick contract) | Manifest **slice_id** labels the **same** bootstrap envelope family **2.7.1** uses for admission gates — not a second identity scheme. |
| `mar.hq3.pin.2_7_3` | [[Phase-2-7-3-Shadow-to-Live-Parity-Admission-Ticket-Redemption-and-First-Committed-Tick-Trace-Roadmap-2026-03-30-1800]] — `admission_ticket_id` redemption + **FirstCommittedTickTrace** | **2.7.3** — `## Behavior` (redemption + first committed tick trace) | Pin row is the slice-local **index** into **2.7.3** redemption + trace invariants; operators cite **`mar.hq3.pin.2_7_3`** when claiming “ticket redeemed for this slice.” |
| `mar.hq3.pin.2_7_1` | [[Phase-2-7-1-Simulation-Entry-Bootstrap-and-Deterministic-First-Tick-Contract-Roadmap-2026-04-01-0116]] — Admission gates + hook-order contract | **2.7.1** — `## Behavior` (admission gates + hook-order preamble) | Pin row is the slice-local **index** into **2.7.1** “admit before live” gate story; does not relax **2.7.2** shadow prerequisites. |

## GWT-6.1.1-A–K (narrowed vs GWT-6-A / secondary delegation)

| ID | Then (evidence expectation) | Primary / secondary anchor |
| --- | --- | --- |
| **GWT-6.1.1-A** | Table **Manifest admission row catalog** lists ≥3 stable `manifest_admission_row_id` values | **GWT-6-A** delegation |
| **GWT-6.1.1-B** | Table **Binding** lists ≥3 rows with **2.7.x** vocabulary + wikilink | **2.7.3** / **2.7.1** |
| **GWT-6.1.1-C** | Each binding row includes explicit “no second truth” clause for ticket field names | **2.7.3** § Behavior |
| **GWT-6.1.1-D** | `mar.hq3.pin.2_7_3` row cites redemption + trace headings | **2.7.3** |
| **GWT-6.1.1-E** | `mar.hq3.pin.2_7_1` row cites admission gate / hook order | **2.7.1** |
| **GWT-6.1.1-F** | `mar.hq3.slice_identity` ties **slice_id** to bootstrap identity family | **2.7.1** |
| **GWT-6.1.1-G** | Outward guarantee **Traceability** satisfied (wikilink + heading per row) | Secondary **Interfaces** |
| **GWT-6.1.1-H** | Outward guarantee **No second redemption truth** explicit | **2.7.3** |
| **GWT-6.1.1-I** | Downstream **6.1.2+** contract states reuse of `manifest_admission_row_id` | This note § Interfaces |
| **GWT-6.1.1-J** | Execution-deferred: wire formats for row IDs in lab exports | **roadmap-state** waiver |
| **GWT-6.1.1-K** | Open questions list at least one execution-deferred item | Below |

## Edge cases

- **Stale pin:** If **2.7.x** note titles move, manifest rows remain valid by **`manifest_admission_row_id`**; humans repair wikilinks in a **handoff-audit** pass — no silent rename of IDs.
- **Multi-slice vault:** Other `slice_id` values must use a **different** `mar.*` prefix namespace to avoid cross-slice collision (e.g. `mar.hq4.*`).

## Open questions

- Whether **`manifest_admission_row_id`** should be mirrored in **distilled-core** `core_decisions` for operator search (deferred — **recal** candidate).
- Lab export: minimum JSON shape for row IDs (**execution-deferred**).

## Pseudo-code readiness

Depth **3** — tables + NL invariants only; no pseudo-code required on conceptual track for this slice.

## Parent

- Secondary: [[Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle-Roadmap-2026-04-05-1615]]

## Research integration

> [!note] External grounding
> Vault-first; continuity from **6.1** manifest + **2.7.1** / **2.7.3** only.
