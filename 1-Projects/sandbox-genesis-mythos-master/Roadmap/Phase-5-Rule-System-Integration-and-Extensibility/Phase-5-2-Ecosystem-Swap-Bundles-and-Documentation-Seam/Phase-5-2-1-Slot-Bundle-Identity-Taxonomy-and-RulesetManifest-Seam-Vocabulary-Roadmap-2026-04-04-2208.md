---
title: Phase 5.2.1 — Slot / bundle identity taxonomy vs RulesetManifest + 5.1.1 seam vocabulary
roadmap-level: tertiary
phase-number: 5
subphase-index: "5.2.1"
project-id: sandbox-genesis-mythos-master
status: in-progress
priority: high
progress: 88
handoff_readiness: 86
created: 2026-04-04
tags:
  - roadmap
  - sandbox-genesis-mythos-master
  - phase-5
para-type: Project
links:
  - "[[Phase-5-2-Ecosystem-Generator-Event-Style-Swap-Documentation-Seam-Roadmap-2026-04-04-2100]]"
  - "[[Phase-5-1-1-Ruleset-Manifest-Seam-Admission-and-Deterministic-Evaluation-Order-Roadmap-2026-04-04-0010]]"
  - "[[Phase-5-Rule-System-Integration-and-Extensibility-Roadmap-2026-03-30-0430]]"
  - "[[Conceptual-Decision-Records/deepen-phase-5-2-1-slot-bundle-identity-rulesetmanifest-seam-2026-04-04-2208]]"
  - "[[decisions-log]]"
---

> [!note] #handoff-review
> `handoff_readiness: 86` — Tertiary **5.2.1** names **documentation-layer** **slot kinds** and **bundle identity** fields that **must** align with **RulesetManifest** + **5.1.1** seam admission (**3.4.1** **SeamId** rows only). **GWT-5.2.1** table below binds each row to § Scope / § Mapping tables / § Edge cases. **Execution-deferred:** concrete manifest schema IDs, extension registries, signing.

## Scope

**In scope:**

- **Slot-kind taxonomy (NL)** for **5.2** swap families — **`generator_slot`**, **`event_slot`**, **`style_slot`** — each mapped to **which manifest-declared seams** and **which RulesetManifest-shaped fields** (names illustrative; wire formats deferred) may mention them without inventing consumer rows beyond **3.4.1**.
- **Bundle identity documentation contract:** minimum narrative fields **`bundle_doc_id`**, **`bundle_doc_revision`**, **`compatibility_class`** (named classes only), **`ruleset_pin_binding`** (must reference **5.1.1** **`ruleset_pin_id`** story), and **`declared_slot_kinds`** — sufficient for replay-stable **documentation** of “what was swapped” under a pin.
- **Seam vocabulary seam with 5.1.1:** every **bundle-declared seam** must cite an existing **3.4.1** row the same way **5.1.1** requires for **RulesetManifest** — **5.2.1** adds **no** parallel catalog.
- **Cross-family identity:** documentation states how **one** operator session may reference **multiple** bundle docs bound to **one** or **many** pins (defer resolution mechanics to **5.2.2**).

**Out of scope:**

- Package bytes, marketplace transport, sandbox, CI — execution-deferred per conceptual waiver.
- Closing **D-5.1.3-matrix-vs-manifest** — **5.2.1** only **references** the same non-authoritative default as secondary **5.2**.

## Behavior (natural language)

1. **Slot kind → manifest hook (documentation):** Each **`generator_slot` / `event_slot` / `style_slot`** entry in bundle docs lists **SeamId** references that **must** already appear in the **RulesetManifest** `declared_seams` set (or an explicitly named **documentation-only** superset that **5.1.1** rejects at admission — default **reject** unless operator extends **3.4.1**).
2. **Bundle doc identity:** Authors publish **`bundle_doc_id` + `bundle_doc_revision`**; hosts compare **pin** + **manifest hash** per **5.1**; **5.2.1** does not define hashing — only **that** doc identity is **stable across replay narratives**.
3. **Compatibility class:** Named classes (e.g. **`COMPAT_STRICT_PIN`**, **`COMPAT_SAME_MAJOR`**) are **documentation enums** until execution assigns wire values; they **must** appear in **GWT** tables when claimed.
4. **No second truth:** Bundle documentation **cannot** assert **SeamId** meanings that contradict **3.4.1** consumer rows — same rule chain as **5.1.1**.

## Interfaces

**Upstream:**

- [[Phase-5-1-1-Ruleset-Manifest-Seam-Admission-and-Deterministic-Evaluation-Order-Roadmap-2026-04-04-0010]] — **RulesetManifest**, **declared_seams**, **tuple** ordering authority.
- [[Phase-3-4-1-Handoff-Seam-Catalog-and-Consumer-Contract-Rows-Roadmap-2026-04-03-0115]] — **SeamId** + consumer rows (**sole** seam truth).

**Parent:**

- [[Phase-5-2-Ecosystem-Generator-Event-Style-Swap-Documentation-Seam-Roadmap-2026-04-04-2100]].

**Downstream:**

- **5.2.2** — cross-bundle compatibility matrix (doc-level).
- **5.2.3** — worked examples / replay narratives.

**Outward guarantees:**

- **Traceable bundle identity** in prose under a **ruleset pin**.
- **Slot vocabulary** that **composes** with **5.1.1** without widening **SeamId** authority.

## Mapping tables (documentation — not execution schema)

### A. Slot kind → typical seam families (illustrative)

| Slot kind | Typical seam role (NL) | Must map to 3.4.1 row | Deferred to execution |
| --- | --- | --- | --- |
| **generator_slot** | Graph / stage hooks that admit generator swaps | Yes — explicit **SeamId** list in bundle doc | Hook payload shapes |
| **event_slot** | Trigger / bus consumption surfaces for event bundles | Yes | Trigger ordinal wiring |
| **style_slot** | Presentation / legibility surfaces (**4.1.3**) | Yes | Theme resource IDs |

### B. Bundle doc identity fields (minimum)

| Field | Purpose | Evidence anchor |
| --- | --- | --- |
| **bundle_doc_id** | Stable author id for the bundle narrative | § Behavior |
| **bundle_doc_revision** | Monotonic doc revision under that id | § Behavior |
| **compatibility_class** | Named compatibility posture vs pin | § Edge cases |
| **ruleset_pin_binding** | Which pin(s) the doc targets | § Interfaces **5.1.1** |
| **declared_slot_kinds** | Subset of {generator, event, style} | § Scope |

### C. RulesetManifest ↔ bundle doc seam (5.1.1 seam)

| RulesetManifest concept (5.1.1) | Bundle doc obligation (5.2.1) |
| --- | --- |
| `declared_seams` ⊆ **3.4.1** | Bundle **SeamId** list ⊆ same **3.4.1** rows |
| `ruleset_pin_id` | **`ruleset_pin_binding`** must reference same pin story |
| Admission failure classes | Bundle doc **may** name **user-facing** mirror strings — execution mapping deferred |

## Edge cases

- **Bundle doc lists seam not in manifest:** documentation treated as **invalid relative to pin** until manifest updated — **non-authoritative** narrative may still describe intent, but **5.1.1** admission remains gate.
- **Multi-pin bundle narrative:** allowed at doc layer; host admission still **one pin at a time** per **5.1** — **5.2.2** will narrow conflict story.
- **Opaque extension buckets (5.1.1 open question):** if ignored by kernel, **5.2.1** bundle docs **must** label such sections **non-authoritative** for swap outcome class.

## Open questions

- Whether **`bundle_doc_revision`** must be **order-comparable** with **manifest version** fields — **execution-deferred** (requires schema IDs).

## Pseudo-code readiness

At **tertiary** conceptual depth, **optional** sketch only — execution types deferred.

```text
function docSeamsSubsetManifest(bundleDoc, manifest):
  return every bundleDoc.seam_id ∈ manifest.declared_seams
```

## Tertiary slice GWT (GWT-5.2.1-A–K) — narrowed vs **GWT-5.2-A–K** and **GWT-5.1.1-A–K**

| ID | Given | When | Then | Evidence (this slice) |
| --- | --- | --- | --- | --- |
| **GWT-5.2.1-A** | **5.1.1** admits seams only from **3.4.1** | Bundle doc lists seams | Every **SeamId** ⊆ **3.4.1** and ⊆ manifest declared set story | § Mapping C + § Behavior |
| **GWT-5.2.1-B** | **GWT-5.2-A** generator swap doc | Author fills **generator_slot** | Doc cites **SeamId** rows + manifest hook | § Mapping A + § Scope |
| **GWT-5.2.1-C** | **GWT-5.2-B** event swap doc | Author fills **event_slot** | Doc cites trigger/bus seams without sim mutation claims | § Mapping A |
| **GWT-5.2.1-D** | **GWT-5.2-C** style swap doc | Author fills **style_slot** | Doc ties to **4.1.3** legibility only | § Mapping A + parent **5.2** |
| **GWT-5.2.1-E** | **GWT-5.1.1-B** pin validated | Bundle claims **ruleset_pin_binding** | Binding references same pin id narrative as manifest | § Mapping B |
| **GWT-5.2.1-F** | **GWT-5.2.1-A** holds | Author adds orphan seam | Doc marked invalid / superseded until manifest aligns | § Edge cases |
| **GWT-5.2.1-G** | **GWT-5.2-D** overlapping bundles | Two bundle docs share seam | **5.2.2** owns matrix — **5.2.1** only requires **declared_slot_kinds** visible | § Scope cross-family |
| **GWT-5.2.1-H** | **D-5.1.3** open | Reader needs alignment story | Same **non-authoritative** default as secondary **5.2** | § Scope out of scope |
| **GWT-5.2.1-I** | **Phase 2** commit boundary | Bundle implies world change | Routes via **2.x** — doc does not bypass | § Behavior + **5.1.1** |
| **GWT-5.2.1-J** | **GWT-5.2-G** version skew | Author publishes revision | **bundle_doc_revision** recorded | § Mapping B |
| **GWT-5.2.1-K** | Conceptual waiver | Registry / CI | Execution-deferred explicit | [[roadmap-state]], [[distilled-core]] |

## Research integration

- None this run (`research_pre_deepen: skipped_high_ctx_budget`; prior **workflow_state** **last_ctx_util_pct** ~**97%**).

## Related

- CDR: [[Conceptual-Decision-Records/deepen-phase-5-2-1-slot-bundle-identity-rulesetmanifest-seam-2026-04-04-2208]]
