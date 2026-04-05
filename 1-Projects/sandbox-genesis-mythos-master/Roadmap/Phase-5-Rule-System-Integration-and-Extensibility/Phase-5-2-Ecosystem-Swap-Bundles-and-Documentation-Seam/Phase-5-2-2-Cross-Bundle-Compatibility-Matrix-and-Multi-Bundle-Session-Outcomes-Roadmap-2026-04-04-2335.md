---
title: Phase 5.2.2 — Cross-bundle compatibility matrix and multi-bundle session outcomes (doc-level)
roadmap-level: tertiary
phase-number: 5
subphase-index: "5.2.2"
project-id: sandbox-genesis-mythos-master
status: in-progress
priority: high
progress: 90
handoff_readiness: 87
created: 2026-04-04
tags:
  - roadmap
  - sandbox-genesis-mythos-master
  - phase-5
para-type: Project
links:
  - "[[Phase-5-2-Ecosystem-Generator-Event-Style-Swap-Documentation-Seam-Roadmap-2026-04-04-2100]]"
  - "[[Phase-5-2-1-Slot-Bundle-Identity-Taxonomy-and-RulesetManifest-Seam-Vocabulary-Roadmap-2026-04-04-2208]]"
  - "[[Phase-5-1-3-Precedence-Conflict-Matrix-and-Cross-Seam-Resolution-Roadmap-2026-04-04-1209]]"
  - "[[Phase-5-Rule-System-Integration-and-Extensibility-Roadmap-2026-03-30-0430]]"
  - "[[Conceptual-Decision-Records/deepen-phase-5-2-2-cross-bundle-compatibility-matrix-2026-04-04-2335]]"
  - "[[decisions-log]]"
---

> [!note] #handoff-review
> `handoff_readiness: 87` — Tertiary **5.2.2** is the **documentation-layer** **compatibility matrix** for **two or more** bundle docs (per **5.2.1** identity fields) under **one ruleset pin** or **explicit multi-doc session** narrative. Cells are **named outcome classes** only; wire enums and host algorithms remain **execution-deferred**. **GWT-5.2.2** binds each row to § Matrix / § Session ordering / § Edge cases.

## Scope

**In scope:**

- **Matrix axes (NL):** bundle instances identified by **`bundle_doc_id` + `bundle_doc_revision`** + **`ruleset_pin_binding`** (must agree with **5.1.1** pin story for the active pin). Matrix is **symmetric** at documentation level: row/column order is **lexicographic by `bundle_doc_id`** then **`bundle_doc_revision`** (illustrative sort key; execution may differ).
- **Cell contract:** each **(A, B)** pair (A ≤ B to avoid duplicate prose; diagonal allowed for self-compatibility) carries:
  - **`swap_outcome_class`** — named class such as **`DOC_COMPAT_OK`**, **`DOC_COMPAT_REJECT_PIN_MISMATCH`**, **`DOC_COMPAT_REJECT_SEAM_NOT_IN_MANIFEST`**, **`DOC_COMPAT_REJECT_SLOT_KIND_CONFLICT`**, **`DOC_COMPAT_DEFER_AUTHORITY_TENSION`** (when **D-5.1.3** default vs matrix row text could disagree).
  - **`seam_overlap_summary`** — NL list of **SeamId** intersections (must ⊆ **3.4.1** and ⊆ manifest `declared_seams` story per **5.2.1**).
  - **`operator_legibility_hook`** — pointer to **4.1.3** readout shape (label family only).
- **Multi-bundle session:** documentation for applying **N≥2** bundle docs in one operator story — **deterministic ordering** assumption (align **5.2** § Behavior cross-family ordering): default narrative **generator → event → style** unless **5.2** parent documents an override for a specific campaign class (still NL; no new execution gates).
- **Cross-family pairs:** **generator×event**, **generator×style**, **event×style** rows must cite **both** **`declared_slot_kinds`** from **5.2.1** without implying a second **SeamId** truth.

**Out of scope:**

- Runtime merge, package signing, download, CI matrix automation — **execution-deferred** per conceptual waiver.
- Closing **D-5.1.3-matrix-vs-manifest** — matrix cites **non-authoritative** default from secondary **5.2** / **5.2.1**; authoritative closure remains **decisions-log** / execution.

## Behavior (natural language)

1. **Cell evaluation (documentation):** Before claiming **`DOC_COMPAT_OK`**, author checks **pin equality** (same **`ruleset_pin_binding`** target), **5.2.1** **`docSeamsSubsetManifest`** sketch, and **compatibility_class** pair-wise rules (e.g. two **`COMPAT_STRICT_PIN`** docs on different pins ⇒ **`DOC_COMPAT_REJECT_PIN_MISMATCH`** without host invocation).
2. **Overlapping seams:** If **SeamId** sets intersect, documentation **must** state whether overlap is **read-only disjoint**, **write-serializable under 5.1 schedule**, or **rejected** — if unknown, use **`DOC_COMPAT_DEFER_AUTHORITY_TENSION`** and cite **5.1.3** **`explanation_handle`** vocabulary where applicable.
3. **Session apply order:** Multi-bundle docs append an **ordered doc list** to the session narrative; **style** after **generator**/**event** visibility is the **default** doc story (matches **5.2** § Behavior item 3).
4. **Single-pin invariant:** Host admission remains **one pin at a time** per **5.1**; multi-pin **storytelling** is labeled **non-host-authoritative** unless operator extends **5.1** (out of scope here).

## Interfaces

**Upstream:**

- [[Phase-5-2-1-Slot-Bundle-Identity-Taxonomy-and-RulesetManifest-Seam-Vocabulary-Roadmap-2026-04-04-2208]] — identity fields + seam subset rule.
- [[Phase-5-1-3-Precedence-Conflict-Matrix-and-Cross-Seam-Resolution-Roadmap-2026-04-04-1209]] — **`matrix_row_id` / `explanation_handle`** for tension rows (**references**, not closure).
- [[Phase-3-4-1-Handoff-Seam-Catalog-and-Consumer-Contract-Rows-Roadmap-2026-04-03-0115]] — **SeamId** sole catalog truth.

**Parent:**

- [[Phase-5-2-Ecosystem-Generator-Event-Style-Swap-Documentation-Seam-Roadmap-2026-04-04-2100]].

**Downstream:**

- [[Phase-5-2-3-Worked-Examples-Replay-Narratives-Roadmap-2026-04-03-2135]] — worked examples / replay narratives that **instantiate** matrix rows (**minted**).

**Outward guarantees:**

- **No silent compat:** every advertised **pair** in a published doc set either has a matrix cell or an explicit **deferred** row.
- **Replay-stable class names:** same pin + same ordered bundle doc list + same matrix revision ⇒ same documented **`swap_outcome_class`** story.

## Matrix skeleton (documentation — illustrative rows)

| Pair pattern | Typical `swap_outcome_class` | When |
| --- | --- | --- |
| Same slot kind, disjoint seams | `DOC_COMPAT_OK` | Overlap empty; both ⊆ manifest |
| Same slot kind, overlapping write seams | `DOC_COMPAT_DEFER_AUTHORITY_TENSION` or `DOC_COMPAT_REJECT_SLOT_KIND_CONFLICT` | Author must pick one class per campaign; cite **5.1.3** if tension |
| Cross-family (generator×event) | `DOC_COMPAT_OK` or `DOC_COMPAT_DEFER_AUTHORITY_TENSION` | Depends on seam overlap + ordering |
| Pin mismatch | `DOC_COMPAT_REJECT_PIN_MISMATCH` | Always when **`ruleset_pin_binding`** targets differ |
| Seam not in manifest | `DOC_COMPAT_REJECT_SEAM_NOT_IN_MANIFEST` | **5.1.1** gate story |

## Edge cases

- **Diagonal (A, A):** self-row documents **revision monotonicity** only — same id + newer revision should not **narrow** declared seams without explicit breaking-change callout (NL).
- **Three-or-more bundles:** documentation composes **pairwise** matrix **or** a stated **rollup doc** that expands to pairwise — must not hide a rejected pair.
- **Opaque extension buckets:** same labeling rule as **5.2.1** — matrix rows touching opaque buckets carry **`non_authoritative_for_swap_outcome`** flag in prose.

## Open questions

- Whether **`swap_outcome_class`** should be **globally unique** vs **scoped by `bundle_doc_id` namespace** — **execution-deferred** (registry IDs).

## Pseudo-code readiness

Optional sketch only:

```text
function docLevelCompatClass(bundleA, bundleB, manifestStory):
  if bundleA.ruleset_pin_binding != bundleB.ruleset_pin_binding:
    return DOC_COMPAT_REJECT_PIN_MISMATCH
  if not seamsSubsetManifest(bundleA, manifestStory): return DOC_COMPAT_REJECT_SEAM_NOT_IN_MANIFEST
  if not seamsSubsetManifest(bundleB, manifestStory): return DOC_COMPAT_REJECT_SEAM_NOT_IN_MANIFEST
  if disjoint(bundleA.seams, bundleB.seams): return DOC_COMPAT_OK
  return DOC_COMPAT_DEFER_AUTHORITY_TENSION
```

## Tertiary slice GWT (GWT-5.2.2-A–K) — narrowed vs **GWT-5.2.1-A–K** and **GWT-5.2-D**

| ID | Given | When | Then | Evidence (this slice) |
| --- | --- | --- | --- | --- |
| **GWT-5.2.2-A** | **GWT-5.2.1-A** holds for both bundles | Author fills matrix cell | **`swap_outcome_class`** named + **SeamId** overlap summary | § Matrix skeleton + § Behavior |
| **GWT-5.2.2-B** | **GWT-5.2-D** overlapping bundles | Author documents pair | Cell exists **or** explicit defer row | § Scope + § Edge cases |
| **GWT-5.2.2-C** | Different pins | Session lists two bundle docs | **`DOC_COMPAT_REJECT_PIN_MISMATCH`** (or reject narrative) | § Behavior item 1 |
| **GWT-5.2.2-D** | **5.1.3** row cited | Tension row | Uses **`explanation_handle`** vocabulary only | § Interfaces |
| **GWT-5.2.2-E** | Multi-bundle session | N≥2 docs | Ordered list + default **generator→event→style** | § Scope session |
| **GWT-5.2.2-F** | **GWT-5.2-F** Phase 2 boundary | Doc implies world change | Routes via **2.x** / **5.1** — no bypass | § Behavior + parent **5.2** |
| **GWT-5.2.2-G** | **D-5.1.3** open | Reader needs story | **Non-authoritative** default repeated | § Scope out of scope |
| **GWT-5.2.2-H** | **4.1.3** legibility | Outcome shown to operator | **`operator_legibility_hook`** present | § Scope cell contract |
| **GWT-5.2.2-I** | **3.4.1** seam truth | Matrix lists seam | Every **SeamId** ⊆ **3.4.1** | § Scope |
| **GWT-5.2.2-J** | **GWT-5.2.2-B** cross-family | generator×style pair | Slot kinds visible from **5.2.1** | § Scope cross-family |
| **GWT-5.2.2-K** | Conceptual waiver | Registry / CI | Execution-deferred explicit | [[roadmap-state]], [[distilled-core]] |

## Research integration

- None this run (`research_pre_deepen: skipped_high_ctx_budget`; **workflow_state** **last_ctx_util_pct** **98%**; operator may **RECAL-ROAD** before next deepen per queue `user_guidance`).

## Related

- CDR: [[Conceptual-Decision-Records/deepen-phase-5-2-2-cross-bundle-compatibility-matrix-2026-04-04-2335]]
