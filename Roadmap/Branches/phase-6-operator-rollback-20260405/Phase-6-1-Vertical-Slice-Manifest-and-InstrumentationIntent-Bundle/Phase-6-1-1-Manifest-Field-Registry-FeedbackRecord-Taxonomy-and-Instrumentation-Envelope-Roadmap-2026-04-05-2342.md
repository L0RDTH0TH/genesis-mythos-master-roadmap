---
title: Phase 6.1.1 — Manifest field registry, FeedbackRecord taxonomy, instrumentation envelope (NL)
roadmap-level: tertiary
phase-number: 6
subphase-index: "6.1.1"
project-id: godot-genesis-mythos-master
status: active
priority: high
progress: 55
handoff_readiness: 86
created: 2026-04-05
tags:
  - roadmap
  - godot-genesis-mythos-master
  - phase-6
para-type: Project
links:
  - "[[Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle-Roadmap-2026-04-05-1510]]"
  - "[[Phase-6-Prototype-Assembly-Testing-and-Iteration-Roadmap-2026-03-30-0430]]"
  - "[[decisions-log]]"
  - "[[distilled-core]]"
  - "[[workflow_state]]"
---

> [!note] #handoff-review
> `handoff_readiness: 86` — **Mint (2026-04-05):** Tertiary **6.1.1** materializes three NL contracts left open on secondary **6.1**: (1) **VerticalSliceManifest field registry** — minimum named columns for slice identity, pins, spine, and deferred-leg disclosure; (2) **FeedbackRecord taxonomy** — slice-local classification rows (no upstream rewrite); (3) **InstrumentationIntentEnvelope** — one NL envelope shape binding **II-6.1-*** rows to attach locus + metric class + upstream gate without profiler APIs. Honors **GWT-6.1** open questions. **No** `Roadmap/Execution/**` unless execution track bootstrapped.

## Phase 6.1.1 — Registry, taxonomy, envelope

This tertiary **refines** [[Phase-6-1-Vertical-Slice-Manifest-and-InstrumentationIntent-Bundle-Roadmap-2026-04-05-1510]] with **typed NL tables** (not host schemas): manifest columns operators must be able to read/compare across iterations; **FeedbackRecord** kinds that route to [[decisions-log]] / [[roadmap-state]]; and a single **envelope** pattern for instrumentation intents so execution can later split into per-subsystem cards without contradicting conceptual authority.

## Scope

**In scope:**

- **Manifest field registry** — required vs optional fields for **VerticalSliceManifest** rows keyed by **`slice_id: Horizon-Q3`**, including **deferred_leg** disclosure when a lab pass omits worldgen, presentation, or rules legs (**GWT-6.1-F** partial subgraph).
- **FeedbackRecord taxonomy** — named **record_kind** values (slice-local enums) with **severity_class**, **routing_target** (`decisions-log` | `roadmap-state` | `both`), and **non-mutation** guarantee vs upstream phase notes (**GWT-6.1-H**).
- **InstrumentationIntentEnvelope (NL)** — one envelope record shape: **`intent_id`** (matches **II-6.1-***), **`attach_locus_narrative`**, **`metric_class_name`**, **`upstream_gate_citation`**, **`execution_wire_stub`** (opaque placeholder), **`slice_id`** — binds the four secondary rows into a comparable set for operators and future execution packaging.

**Out of scope:**

- Profiler hooks, binary telemetry formats, CI thresholds, or Godot-specific APIs (**execution-deferred**).
- Changing **3.4.1** **SeamId** catalog, **5.1.3** matrix keys, or **2.x** commit vocabulary — **reference-only** consumption.

## Behavior (natural language)

1. **Manifest rows:** Every **Horizon-Q3** manifest row in operator-facing docs **includes** the registry fields below; missing optional fields must say **`explicit_none`** or **`deferred_execution`** with a one-line reason (ties **GWT-6.1-F**).
2. **FeedbackRecords:** When a contradiction or surprise is logged, authors **pick** a **record_kind** from the taxonomy table; promotion to [[decisions-log]] uses the **routing_target** column — **no** edits to **2.x**/**3.x**/**4.x**/**5.x** phase bodies for slice feedback alone.
3. **InstrumentationIntentEnvelope:** Each **II-6.1-*** intent from the secondary is **mirrored** as one envelope row — execution later may fan out to multiple cards, but **must** preserve **`intent_id`** + **`upstream_gate_citation`** parity (**GWT-6.1-G**).

## VerticalSliceManifest — field registry (minimum)

| Field id | Required | Meaning / contract |
| --- | --- | --- |
| **slice_id** | yes | Stable id; canonical **`Horizon-Q3`** for this slice until multi-slice policy note exists. |
| **manifest_revision** | yes | Monotonic doc-level revision string (NL); execution may bind to semver later. |
| **narrative_spine_ref** | yes | Pointer to the spine sentence in secondary **6.1** (no duplicate prose authority). |
| **pinned_phase_refs** | yes | Non-empty wikilink set; minimum set equals secondary **Pinned refs** table. |
| **deferred_legs** | yes | List of omitted legs (`worldgen` \| `tick_close` \| `rule_frame` \| `present`) when a partial subgraph run is intentional; empty = full spine claimed. |
| **seam_glue_policy** | yes | **`catalog_seams_only`** — only **3.4.1** **SeamId** keys in glue tables (**GWT-6.1-I**). |
| **d51_matrix_manifest_note** | optional | Free-text pointer to **D-5.1.3-matrix-vs-manifest** stance; **`explicit_none`** if unset. |

## FeedbackRecord taxonomy (slice-local)

| record_kind | severity_class | routing_target | When to use |
| --- | --- | --- | --- |
| **FR-6.1-SURPRISE** | `low` | `decisions-log` | Unexpected but non-blocking observation during slice pass (instrumentation noise, UX oddity). |
| **FR-6.1-CONTRADICTION** | `high` | `both` | Apparent conflict with pinned upstream note or **RuleOutcome** truth — requires [[roadmap-state]] visibility + [[decisions-log]] row. |
| **FR-6.1-SCOPE-DRIFT** | `medium` | `decisions-log` | Slice work trending into execution closure or redefining seams — stop + record; no upstream overwrite. |
| **FR-6.1-INSTRUMENTATION-GAP** | `low` | `decisions-log` | Named **II-6.1-*** locus cannot be observed with current lab harness — execution-deferred tooling. |
| **FR-6.1-PRESENTATION-BREAK** | `medium` | `both` | **4.1.3** envelope or **3.2.1** channel classification appears inconsistent with committed session facts. |

**Rule:** Taxonomy rows are **normative for Phase 6.1.x** feedback; free-text-only feedback is **allowed** only when tagged **`record_kind: FR-6.1-SURPRISE`** or escalated manually by operator.

## InstrumentationIntentEnvelope (NL shape)

| Envelope field | Source / binding |
| --- | --- |
| **intent_id** | **`II-6.1-WORLDGEN`**, **`II-6.1-TICKCLOSE`**, **`II-6.1-RULEFRAME`**, **`II-6.1-PRESENT`** (from secondary bundle table). |
| **slice_id** | **`Horizon-Q3`** |
| **attach_locus_narrative** | Copied from secondary **Attach locus (NL)** column for that intent. |
| **metric_class_name** | Copied from secondary **Metric class (name only)**. |
| **upstream_gate_citation** | Copied from secondary **Upstream gate / citation** — must cite **2.7.x**, **3.1.x**, **4.1.3**, **5.1.x** as appropriate (**no new gates**). |
| **execution_wire_stub** | Placeholder token **`EXEC_STUB:instrumentation_wire`** — execution track replaces; conceptual track **must not** claim wire format. |
| **envelope_revision** | Monotonic NL revision paired with **`manifest_revision`** when both change together. |

**Bundle rule:** Four envelope rows **must** exist for a complete **Horizon-Q3** instrumentation story in docs; partial labs list **`deferred_legs`** on the manifest row instead of deleting intents.

## Interfaces

**Upstream:** Secondary **6.1** manifest + **InstrumentationIntent** table + **GWT-6.1-A–K**.

**Sideways:** [[Phase-3-4-1-Handoff-Seam-Catalog-and-Consumer-Contract-Rows-Roadmap-2026-04-03-0115]] (**SeamId**), [[Phase-4-1-3-Consumer-Surface-Framing-and-Presentation-Time-Validation-Roadmap-2026-04-03-2110]], [[Phase-5-1-2-Kernel-Evaluation-Schedule-and-Rule-Ordering-Roadmap-2026-04-04-0715]] / [[Phase-5-1-3-Precedence-Conflict-Matrix-and-Cross-Seam-Resolution-Roadmap-2026-04-04-1209]] for rule-frame citations.

**Downstream:** Execution track may split **`InstrumentationIntentEnvelope`** into per-subsystem cards; **must** preserve **`intent_id`** and **upstream_gate_citation** parity.

## Edge cases

- **Partial subgraph:** **deferred_legs** non-empty → **FR-6.1-SCOPE-DRIFT** **disallowed** unless operator confirms intentional deferral (**GWT-6.1-F**).
- **Stale pin:** Use **FR-6.1-CONTRADICTION** + **5.x** load-failure vocabulary reference — do not patch **5.1**/**5.2** notes from this slice.
- **High ctx util:** Optional **RECAL-ROAD** does not invalidate registry/taxonomy/envelope rows already minted.

## Open questions

- Whether **manifest_revision** and **envelope_revision** must **lock-step** bump on every intent edit vs manifest-only bumps (**execution-deferred** policy).
- Whether **FR-6.1-*** enums need a **stable machine slug** column at execution handoff (**out of scope** here).

## Pseudo-code readiness

**Depth 3 (tertiary):** interface sketches only — no executable pseudo-code; typed tables above satisfy **mid-technical** checklist for **6.1.1**.

## Tertiary slice GWT (GWT-6.1.1-A–K) — narrowed vs **GWT-6.1**

| ID | Given | When | Then | Evidence (this slice) |
| --- | --- | --- | --- | --- |
| **GWT-6.1.1-A** | Secondary **VerticalSliceManifest** | Operator audits slice doc | Registry columns exist and are filled or **`explicit_none`** / **`deferred_execution`** | § Manifest field registry |
| **GWT-6.1.1-B** | Partial lab pass | **deferred_legs** used | Listed legs match omitted instrumentation/envelope rows | § Behavior; § Manifest field registry |
| **GWT-6.1.1-C** | Feedback arrives | Author classifies | **record_kind** is one of taxonomy rows | § FeedbackRecord taxonomy |
| **GWT-6.1.1-D** | **FR-6.1-CONTRADICTION** | Routed | [[roadmap-state]] + [[decisions-log]] both receive a reference path (no upstream body edit) | § Behavior |
| **GWT-6.1.1-E** | Four **II-6.1-*** intents | Envelope pass | Four **InstrumentationIntentEnvelope** rows exist with matching **intent_id** | § InstrumentationIntentEnvelope |
| **GWT-6.1.1-F** | **upstream_gate_citation** | Reviewer checks | Each citation resolves to an existing upstream phase note clause | § Envelope table |
| **GWT-6.1.1-G** | Execution stub | Conceptual read | **`EXEC_STUB:instrumentation_wire`** present; no fake API names | § InstrumentationIntentEnvelope |
| **GWT-6.1.1-H** | **3.4.1** seams | Glue tables | Only catalog **SeamId** keys appear | § Manifest field registry |
| **GWT-6.1.1-I** | **4.1.3** / **3.2.1** | Presentation leg | **II-6.1-PRESENT** envelope cites both where spine demands | § Envelope table |
| **GWT-6.1.1-J** | **5.1.2** / **5.1.3** | Rules leg | **II-6.1-RULEFRAME** envelope cites schedule + matrix vocabulary | § Envelope table |
| **GWT-6.1.1-K** | Conceptual waiver | Validator advisory | Perf/CI/dashboard gaps remain **execution-deferred** with explicit deferral language | [[roadmap-state]], [[distilled-core]] |

## Research integration

- None this run (**research_pre_deepen** not enabled on queue entry; vault-first **pattern_only**).
