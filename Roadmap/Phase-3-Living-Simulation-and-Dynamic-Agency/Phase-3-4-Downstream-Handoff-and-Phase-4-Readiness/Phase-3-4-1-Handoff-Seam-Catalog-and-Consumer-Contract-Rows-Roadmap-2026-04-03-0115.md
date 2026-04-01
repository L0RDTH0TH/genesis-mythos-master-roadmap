---
title: Phase 3.4.1 — Handoff seam catalog and consumer contract rows
roadmap-level: tertiary
phase-number: 3
subphase-index: "3.4.1"
project-id: genesis-mythos-master
status: active
priority: high
progress: 52
handoff_readiness: 85
created: 2026-04-03
tags:
  - roadmap
  - genesis-mythos-master
  - phase-3
para-type: Project
links:
  - "[[Phase-3-4-Downstream-Handoff-and-Phase-4-Readiness-Roadmap-2026-04-03-0100]]"
  - "[[Phase-3-1-4-Persistence-Checkpoint-Boundaries-Roadmap-2026-04-02-2240]]"
  - "[[Phase-3-2-1-Observation-Channel-Taxonomy-Roadmap-2026-03-30-2310]]"
  - "[[Phase-3-3-2-Consequence-Durability-Matrix-and-Persistence-Invariants-Roadmap-2026-04-03-0020]]"
  - "[[decisions-log]]"
---

> [!note] #handoff-review
> `handoff_readiness: 85` — tertiary **3.4.1** — **handoff seam catalog** + **consumer contract rows** (**GWT-3.4.1-A–K**) — maps upstream **3.1**/**3.2.1**/**3.3.2**/**3.1.4** seams to Phase 4–readable **contract rows** (markdown **Deliverable tables** below; repair `repair-l1postlv-contradictions-341-gmm-20260403T013000Z`). **Secondary 3.4 rollup** complete on parent [[Phase-3-4-Downstream-Handoff-and-Phase-4-Readiness-Roadmap-2026-04-03-0100]] — **GWT-3.4-A–K** reconciled vs this note; `workflow_state` **`current_subphase_index: "3"`** (Phase 3 primary rollup next). Queue: `followup-deepen-phase3-34-rollup-post-repair341-gmm-20260403T014500Z`.

### Metric contract (progress vs handoff_readiness)

- **`progress` (52%):** first **tertiary** under **3.4** — seam catalog vocabulary + **GWT-3.4.1** table + interface sketches; **secondary 3.4 rollup** carries full NL closure vs **GWT-3.4-A–K** on the parent.
- **`handoff_readiness` (85):** delegation-ready — junior can map **Phase 4** modules to **exact** upstream seams without inventing a second checkpoint or observation authority.

## Phase 3.4.1 — Handoff seam catalog and consumer contract rows

This **tertiary** materializes **secondary 3.4**’s promise into a **named seam catalog**: each row is a **consumer contract row** Phase 4 narrative/rendering/tooling can trace to **one** upstream anchor (**3.1.x**, **3.2.x**, or **3.3.x**) and to **authority_class** / **overwrite_class** labels—without importing execution wire formats.

## Scope

**In scope:**

- **Seam catalog table** — stable **SeamId** keys (NL) mapping: **upstream slice** → **minimum exported fields** Phase 4 may assume → **forbidden reinterpretations** (e.g. no preview-as-checkpoint).
- **Consumer contract rows** — one row per **major Phase 4 consumer class** (narrative scripting, rendering feature layer, operator panel) with **required** vs **optional** seam dependencies.
- **Cross-seam consistency rules** — when two rows disagree, **3.1.4** checkpoint ordering **wins**; **3.3.2** **I-3.3-*** invariants **constrain** consequence semantics only **through** that ordering.

**Out of scope:**

- Phase 4 phase notes, engine APIs, or asset pipelines (**Phase 4+**).
- Closing **D-3.4-*** rows in [[decisions-log]] — remain **execution-deferred** until operator picks land.
- **GMM-2.4.5-*** — **reference-only**.

## Behavior (natural language)

1. **Catalog authority:** The **seam catalog** is the **only** place Phase 4 may cite for “which upstream paragraph authorizes this read path”—prevents silent drift from **3.2.1** taxonomy re-labeling without updating **3.4.1**.
2. **Row consumption:** Each **consumer contract row** lists **SeamIds** it **must** bind before shipping Phase 4 design; optional seams are **performance/UX** only, not durability.
3. **Single checkpoint story:** Any row touching **persistence** **must** cite **Seam checkpoint_authority** pointing at **3.1.4** — **3.3.2** matrix cells reference **I-3.3-*** **only** as cross-checks, not alternate persist paths.

## Interfaces

**Upstream (bind targets in catalog):**

- **3.1** — [[Phase-3-1-Sim-Tick-and-Event-Bus-Spine-Roadmap-2026-03-30-2213]] — tick + SimEvent-visible facts.
- **3.1.4** — [[Phase-3-1-4-Persistence-Checkpoint-Boundaries-Roadmap-2026-04-02-2240]] — checkpoint ordering + preview non-authoritative durability.
- **3.2.1** — [[Phase-3-2-1-Observation-Channel-Taxonomy-Roadmap-2026-03-30-2310]] — **ObservationChannel** + **authority_class**.
- **3.3.2** — [[Phase-3-3-2-Consequence-Durability-Matrix-and-Persistence-Invariants-Roadmap-2026-04-03-0020]] — **I-3.3-*** invariants + matrix cells.

**Parent:**

- **3.4** — [[Phase-3-4-Downstream-Handoff-and-Phase-4-Readiness-Roadmap-2026-04-03-0100]] — Phase 3 → Phase 4 boundary package.

**Downstream:**

- **3.4 rollup** — secondary **3.4** NL + **GWT-3.4** parity vs **3.4.1** seam catalog (next deepen target **`3.4`**).

**Outward guarantees:**

- **No duplicate seam IDs** — each **SeamId** appears once in the catalog; aliases **forbidden** (use explicit “supersedes” note in [[decisions-log]] if ever needed).

## Deliverable tables (markdown)

These tables substantiate **GWT-3.4.1-A** and **GWT-3.4.1-F** so rollup claims in [[roadmap-state]] / [[distilled-core]] match in-note evidence (L1 post–little-val repair `repair-l1postlv-contradictions-341-gmm-20260403T013000Z`).

### Handoff seam catalog (≥ 4 rows)

| SeamId | upstream_anchor | minimum_export_fields | forbidden_reinterpretations |
|--------|-------------------|------------------------|----------------------------|
| P3-SEAM-SIM-SPINE | [[Phase-3-1-Sim-Tick-and-Event-Bus-Spine-Roadmap-2026-03-30-2213]] | tick_index, SimEvent_lane_facts, monotonic_tick_order | treating_preview_as_committed_tick |
| P3-SEAM-CKPT-314 | [[Phase-3-1-4-Persistence-Checkpoint-Boundaries-Roadmap-2026-04-02-2240]] | checkpoint_authority, preview_non_authoritative_durability | preview_shadow_as_checkpoint_authority |
| P3-SEAM-OBS-TAX | [[Phase-3-2-1-Observation-Channel-Taxonomy-Roadmap-2026-03-30-2310]] | ObservationChannel, authority_class, preview_shadow_vs_committed_session | reinterpreting_observation_as_sim_bus |
| P3-SEAM-MAT-332 | [[Phase-3-3-2-Consequence-Durability-Matrix-and-Persistence-Invariants-Roadmap-2026-04-03-0020]] | I-3.3-* matrix cells, cross_check_only_vs_checkpoint | alternate_persistence_path_bypassing_314 |

### Consumer contract rows

| consumer_class | required_seam_ids | optional_seam_ids | durability_dependency |
|----------------|-------------------|-------------------|----------------------|
| narrative_scripting | P3-SEAM-SIM-SPINE, P3-SEAM-OBS-TAX | P3-SEAM-MAT-332 | checkpoint_read |
| rendering_feature_layer | P3-SEAM-OBS-TAX, P3-SEAM-SIM-SPINE | P3-SEAM-CKPT-314 | none |
| operator_panel | P3-SEAM-OBS-TAX, P3-SEAM-CKPT-314 | P3-SEAM-MAT-332 | full_replay |

All **required_seam_ids** and **optional_seam_ids** reference **SeamId** values from the catalog table above.

## Edge cases

- **Partial Phase 4 adoption:** A consumer row may declare **optional** observation seams; if it **skips** **consequence** seams, it still **must** honor **authority_class** on any **ObservationChannel** it uses.
- **Hotfix to upstream slice:** If **3.2.1** taxonomy changes, **3.4.1** **SeamId** row **must** be updated in the **same** RESUME_ROADMAP pass or a **RECAL** notes the drift — catalog is **not** silently stale.

## Open questions

- Whether **SeamId** strings should be **globally unique across phases** vs **phase-scoped** — **execution-deferred** naming convention; NL uses **`P3-SEAM-*`** placeholders until locked.

## Pseudo-code readiness

**Mid-technical (depth 3):** interface sketches — **no** production API.

### Record sketches

```
SeamCatalogRow =
  { seam_id                    // NL stable key, e.g. P3-SEAM-OBS-AUTH
  , upstream_anchor            // wikilink + section anchor
  , minimum_export_fields[]    // NL field names Phase 4 may rely on
  , forbidden_reinterpretations[] // e.g. "preview_shadow → checkpoint"
  }

ConsumerContractRow =
  { consumer_class             // narrative | rendering | operator_panel | ...
  , required_seam_ids[]
  , optional_seam_ids[]
  , durability_dependency      // none | checkpoint_read | full_replay
  }
```

## GWT parity (tertiary 3.4.1 — seam catalog + consumer rows)

| ID | Check |
|----|--------|
| GWT-3.4.1-A | **Seam catalog** table exists with ≥ **4** rows covering **3.1**, **3.2.1**, **3.3.2**, **3.1.4**. |
| GWT-3.4.1-B | Each row names **upstream_anchor** as a wikilink to an existing Phase 3 note. |
| GWT-3.4.1-C | **checkpoint_authority** seam explicitly cites **3.1.4** (no duplicate path). |
| GWT-3.4.1-D | **ObservationChannel** seam cites **3.2.1** **authority_class** semantics. |
| GWT-3.4.1-E | **Consequence / matrix** seam cites **3.3.2** **I-3.3-*** as cross-check only. |
| GWT-3.4.1-F | **Consumer contract rows** list **required_seam_ids** ⊂ catalog. |
| GWT-3.4.1-G | **D-3.1.5-*** remain **execution-deferred** (no wire claims). |
| GWT-3.4.1-H | **GMM-2.4.5-*** **reference-only** restated in catalog intro. |
| GWT-3.4.1-I | **overwrite_class** / **live_tweak** vs **structural_regen_request** traced to **3.1.3** / Phase 3 primary. |
| GWT-3.4.1-J | **Open questions** list **or** explicit **none** for tertiary depth. |
| GWT-3.4.1-K | **Next step** names **secondary 3.4 rollup** as following structural action. |

## Tertiary notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-4-Downstream-Handoff-and-Phase-4-Readiness"
WHERE roadmap-level = "secondary" OR roadmap-level = "tertiary" OR roadmap-level = "task"
SORT subphase-index ASC, file.name ASC
```
