---
title: Phase 3.4 — Downstream handoff and Phase 4 readiness
roadmap-level: secondary
phase-number: 3
subphase-index: "3.4"
project-id: genesis-mythos-master
status: active
priority: high
progress: 68
handoff_readiness: 86
created: 2026-04-03
tags:
  - roadmap
  - genesis-mythos-master
  - phase-3
para-type: Project
links:
  - "[[Phase-3-Living-Simulation-and-Dynamic-Agency-Roadmap-2026-03-30-0430]]"
  - "[[Phase-3-3-Vitality-Consequence-and-Persistence-Cohesion-Roadmap-2026-04-03-0005]]"
  - "[[Phase-3-1-4-Persistence-Checkpoint-Boundaries-Roadmap-2026-04-02-2240]]"
  - "[[Phase-3-2-Simulation-Rendering-Decoupling-and-Observation-Channels-Roadmap-2026-04-02-2300]]"
  - "[[decisions-log]]"
  - "[[Conceptual-Decision-Records/deepen-phase-3-4-secondary-rollup-nl-gwt-2026-04-03-0130]]"
---

> [!note] #handoff-review
> `handoff_readiness: 86` — **secondary 3.4 rollup** — **tertiary 3.4.1** complete (**seam catalog** + **consumer contract rows**; **GWT-3.4.1-A–K**); **NL checklist** + **GWT-3.4-A–K** parity vs **3.4.1** in-note evidence ([[Phase-3-4-1-Handoff-Seam-Catalog-and-Consumer-Contract-Rows-Roadmap-2026-04-03-0115]]). **D-3.4-*** Phase 4 consumer rows ([[decisions-log]]) remain **execution-deferred**; **GMM-2.4.5-*** **reference-only**. **Next structural cursor:** **Phase 3 primary rollup** — NL closure / **advance-phase** readiness on [[Phase-3-Living-Simulation-and-Dynamic-Agency-Roadmap-2026-03-30-0430]] (`workflow_state` **`current_subphase_index: "3"`**). Resolver: `gate_signature: structural-3-4-rollup-post-341` \| queue: `followup-deepen-phase3-34-rollup-post-repair341-gmm-20260403T014500Z`.

## Phase 3.4 — Downstream handoff and Phase 4 readiness

This **secondary 3.4** slice defines the **authoritative Phase 3 → Phase 4 boundary**: what **narrative, rendering, and operator tooling** layers may assume from **living simulation** outputs after **3.1** (tick + bus), **3.2** (observation), and **3.3** (vitality / consequence / persistence cohesion)—without importing Phase 2 commit internals or Phase 3 engine APIs.

## Scope

**In scope:**

- **Phase 4 consumer contract** — stable **sim-visible fact** shapes, **overwrite class** labels, and **checkpoint-eligible vs preview-only** authority that Phase 4 modules consume via **observation** and **audit** surfaces (NL only).
- **Handoff bundle semantics** — what is **in-variant** for Phase 4 design (references **3.2.1** `ObservationChannel`, **3.3.2** **I-3.3-***, **3.1.4** checkpoint ordering) vs **explicitly execution-deferred** (wire formats, CI, registry closure).
- **Phase boundary gate** — conceptual **readiness checklist** for “Phase 3 design authority sufficient to start Phase 4 narrative/rendering decomposition” (not execution HR proof).

**Out of scope:**

- Phase 4 phase notes, story tooling, or engine APIs (Phase 4+).
- Closing **D-3.1.5-*** or **D-3.3-*** rows — remain **execution-deferred** per [[decisions-log]].
- **GMM-2.4.5-*** compare-table / validator closure — **reference-only**.

## Behavior (natural language)

1. **Exports:** Phase 4 consumers receive **labeled** streams: **SimEvent**-visible facts (from **3.1**), **ObservationChannel**-scoped views (**3.2**), **ConsequenceRecord** / **vitality** semantics (**3.3**), each tagged with **authority_class** (**committed_session** vs **preview_shadow**) and **overwrite_class** (**live_tweak** vs **structural_regen_request**) per Phase 3 primary and **3.1.3** mapping.
2. **No second durability authority:** **3.1.4** checkpoint ordering remains **canonical**; Phase 4 **must not** invent a parallel persist path; **3.3.2** matrix cells **reference** **I-3.3-*** invariants only through **3.1.4** gates.
3. **Continuity:** Phase 2 **FirstCommittedTickTrace** / **2.7.3** admission semantics remain **upstream**; **3.4** only **packages** what Phase 4 needs to **read** without re-deriving **2.4**/**2.5** branch tables.

## Interfaces

**Upstream (Phase 3 chains):**

- **3.1** — [[Phase-3-1-Sim-Tick-and-Event-Bus-Spine-Roadmap-2026-03-30-2213]] — tick + bus spine.
- **3.2** — [[Phase-3-2-Simulation-Rendering-Decoupling-and-Observation-Channels-Roadmap-2026-04-02-2300]] — observation + preview vs committed.
- **3.3** — [[Phase-3-3-Vitality-Consequence-and-Persistence-Cohesion-Roadmap-2026-04-03-0005]] — vitality / consequence / persistence cohesion.

**Parent (Phase 3 primary):**

- [[Phase-3-Living-Simulation-and-Dynamic-Agency-Roadmap-2026-03-30-0430]] — **Downstream (Phase 4+)** exposes sim-visible facts + overwrite labels (primary § Interfaces).

**Downstream (Phase 4+):**

- Narrative systems, rendering feature layers, and operator panels that consume **observation contracts** only—detailed in Phase 4 roadmap (not minted here).

**Outward guarantees:**

- **Single source of truth** for **checkpoint vs preview** and **live vs regen** at the Phase 3 boundary; Phase 4 **does not** reinterpret **2.x** validation semantics.

## Edge cases

- **Partial Phase 4 adoption:** If a consumer only needs **observation** without **consequence** replay, it still **must** respect **authority_class**—cannot promote **preview_shadow** to **checkpoint-eligible** without **3.1.5** admission.
- **Drift between teams:** If Phase 4 drafts assume **extra** durability fields not in **3.3.2**, treat as **Phase 4 open question**—not a silent **3.x** patch.

## Open questions

- **D-3.4-phase4-consumer-granularity** — Minimum **consumer bundle** granularity (per-campaign vs per-session vs per-tick export) before execution prototypes — **execution-deferred**; authoritative row [[decisions-log]] when created.
- **D-3.4-narrative-rendering-split** — Whether **narrative** vs **rendering** Phase 4 tracks split **consumer contracts** or share one **handoff bundle** — **execution-deferred**.

## Pseudo-code readiness

At **secondary** conceptual depth, **no pseudo-code** is required. **GWT-3.4-** rows below are the **pre-rollup checklist**; **secondary 3.4 rollup** (after **3.4.1** mint) reconciles **GWT-3.4-A–K** against **3.4.1** seam catalog + consumer contract tables.

## GWT parity (secondary 3.4 — handoff readiness)

| ID | Check |
|----|--------|
| GWT-3.4-A | Phase 4 **consumer contract** paragraph exists (what layers may assume). |
| GWT-3.4-B | **authority_class** + **overwrite_class** labels traced to **3.1.3** / Phase 3 primary. |
| GWT-3.4-C | **3.1.4** checkpoint authority **not** duplicated or weakened. |
| GWT-3.4-D | **3.2.1** **ObservationChannel** referenced as **observation** export surface. |
| GWT-3.4-E | **3.3.2** **I-3.3-*** referenced for **consequence** / durability cross-check. |
| GWT-3.4-F | **Preview vs committed** boundary **re-stated** for Phase 4 readers. |
| GWT-3.4-G | **D-3.1.5-*** explicitly **execution-deferred** (no new wire claims). |
| GWT-3.4-H | **GMM-2.4.5-*** **reference-only** restated. |
| GWT-3.4-I | Phase 2 **simulation entry** continuity **one-liner** (no re-derive). |
| GWT-3.4-J | **Open questions** list **or** explicit **none** for secondary depth. |
| GWT-3.4-K | **Tertiary 3.4.1** minted — [[Phase-3-4-1-Handoff-Seam-Catalog-and-Consumer-Contract-Rows-Roadmap-2026-04-03-0115]] (**seam catalog** + **consumer contract rows**). |

## Secondary 3.4 rollup (NL checklist + GWT parity)

**NL checklist (secondary depth):**

- [x] Scope / Behavior / Interfaces / Edge cases / Open questions coherent with **3.1.x** / **3.2.x** / **3.3.x** upstream and Phase 3 primary glue row.
- [x] **Tertiary 3.4.1** complete — **handoff seam catalog** + **consumer contract rows** (**GWT-3.4.1-A–K**) with **Deliverable tables** in-note.
- [x] **GWT parity:** **GWT-3.4-A**–**K** trace **3.4.1** coverage on this secondary surface (rollup maps **A–C** to checkpoint + authority story, **D–F** to observation + preview/committed, **G–K** to execution deferrals + **3.4.1** seam / consumer evidence).
- [x] **D-3.1.5-*** and **D-3.4-*** — **execution-deferred** per [[decisions-log]]; prose does **not** treat them as conceptual hard gates.

**GWT parity mapping (tertiary → secondary rows):**

| Tertiary | GWT rows |
| --- | --- |
| 3.4.1 | GWT-3.4-A — GWT-3.4-K |

## GWT (Given / When / Then) — secondary prose

| ID | Given | When | Then |
| --- | --- | --- | --- |
| GWT-3.4-A | Phase 4 consumer reads the **handoff bundle** | Contract row is chosen | **SeamId** set ⊆ **3.4.1** catalog — no silent extra upstream seam |
| GWT-3.4-B | Labels **authority_class** / **overwrite_class** appear on exports | Consumer maps to Phase 4 UI | Trace lands on **3.1.3** mapping + Phase 3 primary — **no** invented label taxonomy |
| GWT-3.4-C | Durability is asserted | Checkpoint story is needed | **3.1.4** ordering remains sole checkpoint authority — **3.3.2** cells are cross-check only |
| GWT-3.4-D | **ObservationChannel** is consumed | Read path resolves | **3.2.1** taxonomy + **authority_class** honored — not a second bus API |
| GWT-3.4-E | **Consequence** / matrix semantics consulted | Consumer ties to persistence | **I-3.3-*** via **P3-SEAM-MAT-332** only — no alternate persist path |
| GWT-3.4-F | **Preview** lane is shown | UX compares to committed | **Preview vs committed** boundary explicit — **3.1.5** admission for promotion |
| GWT-3.4-G | **D-3.1.5-*** referenced | Wire format requested | **Execution-deferred** — NL loci only (**3.2.3**), no wire claims |
| GWT-3.4-H | Compare-table / registry invoked | Validator closure expected | **GMM-2.4.5-*** **reference-only** — execution track owns closure |
| GWT-3.4-I | Phase 2 **simulation entry** continuity | Phase 4 scopes bootstrap | One-liner upstream to **2.7.3** / **FirstCommittedTickTrace** — no re-derive of **2.4**/**2.5** tables |
| GWT-3.4-J | **D-3.4-*** open rows exist | Consumer bundles Phase 4 | Rows live in [[decisions-log]] — **not** silent **3.x** patches |
| GWT-3.4-K | **3.4.1** **SeamId** + **consumer_class** rows exist | Rollup claims design authority | **P3-SEAM-*** catalog + consumer **required_seam_ids** ⊂ catalog — matches **GWT-3.4.1-A–K** |

## Risk register v1

| Risk | Mitigation | Owner / defer |
| --- | --- | --- |
| Seam catalog drifts from upstream slice relabel | **3.4.1** hotfix rule + **RECAL** if taxonomy changes without catalog update | Closed at conceptual rollup |
| Phase 4 assumes extra durability fields | **3.3.2** matrix + **P3-SEAM-MAT-332** — **GWT-3.4-E** | [[decisions-log]] **D-3.4-*** |
| Duplicate checkpoint authority | **P3-SEAM-CKPT-314** + **3.1.4** — **GWT-3.4-C** | Execution-deferred wire proofs |

## Tertiary notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/Phase-3-4-Downstream-Handoff-and-Phase-4-Readiness"
WHERE roadmap-level = "secondary" OR roadmap-level = "tertiary" OR roadmap-level = "task"
SORT subphase-index ASC, file.name ASC
```
