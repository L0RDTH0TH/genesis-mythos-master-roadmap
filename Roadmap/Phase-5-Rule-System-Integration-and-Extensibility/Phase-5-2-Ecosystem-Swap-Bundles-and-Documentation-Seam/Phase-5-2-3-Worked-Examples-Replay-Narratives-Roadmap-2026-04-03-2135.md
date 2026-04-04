---
title: Phase 5.2.3 — Worked examples and replay narratives (documentation layer)
roadmap-level: tertiary
phase-number: 5
subphase-index: "5.2.3"
project-id: genesis-mythos-master
status: in-progress
priority: high
progress: 92
handoff_readiness: 88
created: 2026-04-03
tags:
  - roadmap
  - genesis-mythos-master
  - phase-5
para-type: Project
links:
  - "[[Phase-5-2-Ecosystem-Generator-Event-Style-Swap-Documentation-Seam-Roadmap-2026-04-04-2100]]"
  - "[[Phase-5-2-2-Cross-Bundle-Compatibility-Matrix-and-Multi-Bundle-Session-Outcomes-Roadmap-2026-04-04-2335]]"
  - "[[Phase-5-2-1-Slot-Bundle-Identity-Taxonomy-and-RulesetManifest-Seam-Vocabulary-Roadmap-2026-04-04-2208]]"
  - "[[Phase-4-2-3-Replay-Closure-Orchestration-Repair-and-Operator-Escalation-Readout-Roadmap-2026-03-31-1500]]"
  - "[[Phase-5-Rule-System-Integration-and-Extensibility-Roadmap-2026-03-30-0430]]"
  - "[[Conceptual-Decision-Records/deepen-phase-5-2-3-worked-examples-replay-narratives-2026-04-03-2135]]"
  - "[[decisions-log]]"
---

> [!note] #handoff-review
> `handoff_readiness: 88` — Tertiary **5.2.3** is the **documentation-layer** **worked example + replay narrative** slice: **fictional but typed** bundle-doc stories that **bind** **`swap_outcome_class`** cells from **5.2.2** to operator-visible timelines (aligned with **4.2.3** closure vocabulary **without** duplicating orchestration). Examples are **NL-only**; executable fixtures and CI replay harnesses remain **execution-deferred**.

## Scope

**In scope:**

- **Worked example set (minimum NL contract):** At least **three** end-to-end **documentation narratives**, each with:
  - **`example_id`** — stable doc label (e.g. `WE-5.2.3-A`).
  - **Bundle doc list** — ordered per **5.2.2** multi-bundle session (**generator → event → style** default).
  - **Matrix trace** — explicit **(A, B)** pairs with the **`swap_outcome_class`** that the story demonstrates (must match **5.2.2** naming).
  - **Replay anchor sentence** — cites **Phase 2** lineage discipline (“same pin + same ordered doc list + same matrix revision ⇒ same documented outcome class story”) without inventing hash algorithms.
  - **4.2.3 readout hook** — when the story touches session repair / escalation, it names **`ReplayClosureBundle`** / **`OperatorEscalationReadout`** as **documentation labels** only (no new orchestration fields).
- **Negative / reject examples:** At least **one** narrative for **`DOC_COMPAT_REJECT_PIN_MISMATCH`** and **one** for **`DOC_COMPAT_REJECT_SEAM_NOT_IN_MANIFEST`** (or **`DOC_COMPAT_REJECT_SLOT_KIND_CONFLICT`**) so **GWT-5.2.3** “Then” columns have concrete homes.
- **Tension example:** At least **one** narrative using **`DOC_COMPAT_DEFER_AUTHORITY_TENSION`** with explicit pointer to **5.1.3** **`explanation_handle`** vocabulary (still **non-closing** for **D-5.1.3**).

**Out of scope:**

- Shipping example repos, golden JSONL, or automated replay binaries — **execution-deferred** per conceptual waiver.
- Changing **5.1** evaluation order or **5.2.2** matrix skeleton — this slice **instantiates** only.

## Behavior (natural language)

1. **Example composition:** Author picks **illustrative** `bundle_doc_id` / `bundle_doc_revision` values that remain **consistent within the example** and reference **5.2.1** field names (no registry IDs).
2. **Matrix back-link:** Each example’s “Outcome” section lists the **5.2.2** cell pattern it exercises (e.g. “same slot kind, disjoint seams → `DOC_COMPAT_OK`”).
3. **Replay narrative:** The **chronological** operator story states what documentation artifacts must exist **before** and **after** the swap sequence so an external auditor (human) could reconstruct the **documented** class — aligns with **4.2.3** “replay-safe closure” **wording** only.
4. **Partial application:** If an example stops mid-sequence (operator cancels), documentation states **`swap_outcome_class`** as **deferred** or **rejected** per **5.2.2** edge cases — no silent OK.

## Interfaces

**Upstream:**

- [[Phase-5-2-2-Cross-Bundle-Compatibility-Matrix-and-Multi-Bundle-Session-Outcomes-Roadmap-2026-04-04-2335]] — matrix cells + session ordering.
- [[Phase-5-2-1-Slot-Bundle-Identity-Taxonomy-and-RulesetManifest-Seam-Vocabulary-Roadmap-2026-04-04-2208]] — identity fields + seam subset story.
- [[Phase-4-2-3-Replay-Closure-Orchestration-Repair-and-Operator-Escalation-Readout-Roadmap-2026-03-31-1500]] — replay closure **vocabulary** for narrative alignment.

**Parent:**

- [[Phase-5-2-Ecosystem-Generator-Event-Style-Swap-Documentation-Seam-Roadmap-2026-04-04-2100]].

**Downstream:**

- **Secondary 5.2 rollup** — NL checklist + **GWT-5.2** parity vs **5.2.1–5.2.3** (next structural target after this mint).

**Outward guarantees:**

- **No orphan examples:** every **`example_id`** maps to at least one **GWT-5.2.3** row’s Evidence column.
- **No second seam truth:** all **SeamId** mentions remain subsets of **3.4.1** per **5.2.1**/**5.2.2**.

## Worked example table (illustrative — documentation only)

| `example_id` | Bundle sequence (ordered) | Matrix / outcome demonstrated | 4.2.3 touchpoint |
| --- | --- | --- | --- |
| **WE-5.2.3-A** | `gen_core@rev2` → `evt_hooks@rev1` → `style_ui@rev3` | Cross-family **`DOC_COMPAT_OK`** + default ordering | Optional **`ReplayClosureBundle`** mention when session restarts mid-swap |
| **WE-5.2.3-B** | `gen_alt@rev1` + `gen_core@rev2` (different pins) | **`DOC_COMPAT_REJECT_PIN_MISMATCH`** | **`OperatorEscalationReadout`** label if operator forces incompatible pin |
| **WE-5.2.3-C** | `evt_badseam@rev1` (declared seam ∉ manifest story) | **`DOC_COMPAT_REJECT_SEAM_NOT_IN_MANIFEST`** | Closure narrative only — no new repair token fields |
| **WE-5.2.3-D** | Overlapping write seams + **D-5.1.3** tension | **`DOC_COMPAT_DEFER_AUTHORITY_TENSION`** + **5.1.3** **`explanation_handle`** cite | Doc states operator waits for matrix/manifest alignment decision |

## Edge cases

- **Example vs live campaign:** Examples are **non-normative**; a live campaign may carry a **`campaign_doc_revision`** that overrides ordering only if **5.2** parent already documented that override class (still NL).
- **Three-or-more bundles:** Examples use **5.2.2** pairwise expansion rule — if an example uses **rollup doc**, it states the expansion explicitly.

## Open questions

- Minimum **count** of worked examples before **5.2 rollup** closes — default **four rows** above satisfies “≥3 positive-path slices + rejects”; operator may extend in **Conceptual-Amendments** without freezing **5.2.3** body.

## Pseudo-code readiness

Optional narrative pseudo-code only (not host API):

```text
function documentedSwapStory(bundleDocsOrdered, matrixRevision):
  assert each pair has swap_outcome_class from 5.2.2
  assert replay_anchor_text cites pin + ordered list + matrixRevision
  return example_id
```

## Tertiary slice GWT (GWT-5.2.3-A–K) — narrowed vs **GWT-5.2.2-A–K**

| ID | Given | When | Then | Evidence (this slice) |
| --- | --- | --- | --- | --- |
| **GWT-5.2.3-A** | **GWT-5.2.2-E** multi-bundle session | Author writes example | Ordered doc list + default **generator→event→style** | § Worked example table **WE-5.2.3-A** |
| **GWT-5.2.3-B** | **GWT-5.2.2-C** pin mismatch | Author writes negative example | Story ends in **`DOC_COMPAT_REJECT_PIN_MISMATCH`** | **WE-5.2.3-B** |
| **GWT-5.2.3-C** | **GWT-5.2.2-B** missing cell | Author adds defer/reject | Example cites explicit class | **§ Scope** — Negative / reject examples + **WE-5.2.3-C** |
| **GWT-5.2.3-D** | **4.2.3** vocabulary | Example mentions repair | Uses **ReplayClosureBundle** / **OperatorEscalationReadout** as **labels** only | § Interfaces |
| **GWT-5.2.3-E** | **Phase 2** replay discipline | Reader checks determinism | One-sentence **replay anchor** per example | § Behavior item 3 |
| **GWT-5.2.3-F** | **GWT-5.2.2-I** **SeamId** truth | Example lists seams | ⊆ **3.4.1** | § Interfaces outward guarantees |
| **GWT-5.2.3-G** | **GWT-5.2.2-D** tension | Example uses defer class | **`explanation_handle`** vocabulary only | **WE-5.2.3-D** |
| **GWT-5.2.3-H** | **4.1.3** legibility | Example shows operator readout | Cites **`operator_legibility_hook`** pattern from **5.2.2** | § Behavior item 2 (matrix back-link) + [[Phase-5-2-2-Cross-Bundle-Compatibility-Matrix-and-Multi-Bundle-Session-Outcomes-Roadmap-2026-04-04-2335]] § Scope cell contract |
| **GWT-5.2.3-I** | **GWT-5.2-F** Phase 2 boundary | Example implies world change | Routes via **2.x** / **5.1** — no bypass | § Behavior item 4 (partial application — no silent OK) |
| **GWT-5.2.3-J** | Conceptual waiver | CI / fixtures | Execution-deferred explicit | [[roadmap-state]], [[distilled-core]] |
| **GWT-5.2.3-K** | **5.2** tertiary chain | **5.2.3** minted | Downstream **5.2 rollup** has example evidence | § Interfaces — **Downstream** |

## Research integration

- None this run (`research_pre_deepen: skipped_high_ctx_budget`; operator **`user_guidance`** allowed optional **RECAL** at ~**99%** ctx util — not taken in this deepen).

## Related

- CDR: [[Conceptual-Decision-Records/deepen-phase-5-2-3-worked-examples-replay-narratives-2026-04-03-2135]]
