---
title: Phase 4.1.1 — Adapter preimage, stable column layout, CQRS, replay deferrals (research)
research_query: "T-P4-01 adapter row layout; TickCommitRecord_v0 post_apply_observable_root serialization_profile_id; CQRS vs AgencySliceApplyLedger_v0; skipUntil D-032 D-043; HR 92 vs min_handoff_conf 93 REGISTRY-CI HOLD"
linked_phase: Phase-4-1-1-adapter-preimage-stable-column-layout
project_id: genesis-mythos-master
created: 2026-03-23
tags: [research, agent-research, genesis-mythos-master, phase-4-1-1, adapter, cqrs, replay]
para-type: Resource
agent-generated: true
research_tools_used: [vault_context, web_search_skipped]
research_escalations_used: 0
parent_handoff: "Roadmap RESUME_ROADMAP pre-deepen nested research — phase 4.1.1 T-P4-01"
queue_entry_id: resume-deepen-post-recal-p4-1-1-gmm-20260324T021500Z
---

# Phase 4.1.1 — Adapter preimage, stable columns, CQRS, and vault-honest rollup wording

**Scope:** Non-normative synthesis for tertiary **[[phase-4-1-1-adapter-preimage-and-stable-column-layout-roadmap-2026-03-24-0018]]** (T-P4-01). **Authoritative** contracts remain **3.1.x** phase notes and **[[decisions-log]]** (especially **D-032**, **D-037**, **D-043**, **D-044**, **D-045**, **D-059**).

## Vault anchor (do not duplicate)

- Phase 4.1.1 already defines **preimage authority table**, **BuildPresentationAdapterRow** sketch, **adapter_row_layout_id**, and **Lane-C `@skipUntil(D-032)`** for presentation-only columns.
- **Prior synthesis:** [[Ingest/Agent-Research/phase-4-primary-perspective-control-research-2026-03-24]] (CQRS split, committed observables, G-P4-REGISTRY-CI HOLD).
- **Decisions-log** binds **D-037** (`serialization_profile_id`, facet manifest) **TBD**; **D-032** replay header / **`replay_row_version`** coordination with **3.1.1**; **D-043** canonical preimage deferral; **D-044** regen lane **Option A** with literal **TickCommitRecord_v0** alignment still **TBD**.

## 1. Stable adapter row layout and versioning (read-model over committed preimage)

**Intent:** Presentation adapter rows are **projections** of **tick-committed** simulation artifacts, not a parallel write ledger. Stability requires three coupled ideas:

1. **Layout identity:** A versioned **`adapter_row_layout_id`** (or equivalent) documents the **ordered column set** and **semantic names** exposed to golden / rollup tables. When columns are added, renamed, or reordered, bump layout id and coordinate with **3.1.1** **`replay_row_version`** / stub row — **no silent rename** vs rollup tables (phase 4.1.1 task list).

2. **Serialization profile:** **`serialization_profile_id`** (per **D-037** intent) selects which facets and canonicalization rules feed **hash-stable** preimage for **`post_apply_observable_root`** and related hashes. Until the profile registry and manifest file are operator-frozen, treat profile id as **intent** in vault text; hashes in CI must not claim stability across profile changes.

3. **Tick commit alignment:** **`TickCommitRecord_v0`** is the narrative anchor for **tick_id** and committed-bundle linkage; **`post_apply_observable_root`** (3.1.6) aligns with **`TickCommitRecord_v0.committed_sim_observable_hash`** per **D-037** draft. Adapter build should **assert** `committed_bundle.phase == post_apply` (already in 4.1.1 sketch) so presentation never consumes pre-barrier or speculative bundles.

**Pattern (industry-agnostic):** Read models that must match replay hashes typically version **both** the **logical schema** (column names / order) and the **serialization rules** used to build preimage bytes — same spirit as **schema evolution** for event projections in CQRS, without implying a specific framework.

## 2. CQRS boundary — presentation adapters must not write **AgencySliceApplyLedger_v0**

**Command side (simulation write path):** **3.1.5** / **D-035** — **`AgencySliceApplyLedger_v0`** records ordered apply outcomes and mutation intent; it participates in **tick commit** and replay coupling with **3.1.6** (`apply_ledger_checksum` narrative).

**Query side (presentation):** **`PresentationViewState_v0`**, **`CameraBinding_v0`**, and adapter rows are **pure functions** of **committed** observables + stable ids (**camera_binding_id**, allow-listed **`presentation_stable_inputs`**). **No** write-back from UI, camera rig, or adapter into **`AgencySliceApplyLedger_v0`** — any world mutation goes through **sanctioned intent / command** paths (player-first scope per **ARCH-FORK-02** / **D-059**; DM tooling deferred).

**Failure mode to avoid:** Treating a “convenience” update (e.g. tool adjusting sim state through a presentation hook) as harmless — that creates a **second write lane** that breaks determinism and replay parity.

## 3. **`@skipUntil(D-032/D-043)`** — how deferrals should read in specs

When **replay header literals** and **canonical preimage formulas** are still **TBD**:

- **Normative column names** may appear in tables (as in 4.1.1 preimage authority table).
- **Golden rows**, **ReplayAndVerify** literals, and **frozen field encodings** must be marked **`@skipUntil(D-032)`** and/or **`@skipUntil(D-043)`** (and any paired decision, e.g. **D-045** for regen rows) — matching **decisions-log** language: no CI assert until header + **`replay_row_version`** + preimage coordination land.
- **Lane-C** presentation-only columns (e.g. **`fov_lod_parameters`**) stay **`@skipUntil(D-032)`** until literal replay columns exist — consistent with **G-P\*.**\* registry **HOLD** narrative. **D-045** explicitly governs **3.2.3** regen **ReplayAndVerify** / golden deferrals; 4.1.1 Lane-C skips are anchored on **D-032** / **D-043** / **3.1.1** preimage freeze — not the regen-row deferral table.

**Spec hygiene:** In each skipped cell, prefer **one line**: dependency id, owner, and **“no PASS until …”** so operators are not misled by PASS elsewhere (e.g. **REPLAY-LANE** text PASS vs **REGISTRY-CI** HOLD).

## 4. Vault-honest wording — **HR 92** vs **`min_handoff_conf` 93** and **G-P\*.\*-REGISTRY-CI HOLD**

From **[[roadmap-state]]** and **[[3-Resources/Watcher-Result]]** (verbatim audit line):

```text
requestId: resume-roadmap-genesis-mythos-master-20260323-deepen-suggested-248 | segment: VALIDATE | status: success | message: "Post-pipeline roadmap_handoff_auto (Layer 1): medium/needs_work (non-blocking); primary_code missing_task_decomposition + safety_unknown_gap; HR below min_handoff_conf 93; no hard block; no A.5b repair." | trace: "report: .technical/Validator/roadmap-auto-validation-genesis-mythos-master-20260323T121500Z-queue-post-little-val-248.md" | completed: 2026-03-23T12:25:00.000Z
```

- **Rollup `handoff_readiness` 92** on **3.2.4 / 3.3.4 / 3.4.4** closure notes is **below** project **`min_handoff_conf: 93`** used for strict advance eligibility.
- **G-P\*.\*-REGISTRY-CI** remains **HOLD** until **2.2.3** / **D-020** execution evidence and related registry policy catch up — **do not** narrate **REGISTRY-CI PASS** or “advance-eligible” off rollup text alone.
- **Distinction:** Vault may record **PASS** on specific **normative gate rows** (e.g. **G-P3.2-REPLAY-LANE**) while **composite** advance gates (HR vs min conf, REGISTRY-CI HOLD) remain **unchanged** — **[[phase-4-1-1-adapter-preimage-and-stable-column-layout-roadmap-2026-03-24-0018]]** correctly states **G-P\*.\*-REGISTRY-CI HOLD** unchanged by this tertiary (**D-062**).

**Anti-pattern:** Fabricating **CI PASS** or implying **HR ≥ min_handoff_conf** without updating **roadmap-state** / rollup notes — violates vault-honest operator visibility.

## 5. Decision / doc candidates

- Add explicit **CQRS** sentence in 4.1.1 **TL;DR**: adapter = query projection; **forbidden** direct writes to **`AgencySliceApplyLedger_v0`** (cross-link **3.1.5**).
- When **D-032** clears: add **changelog row** linking **`adapter_row_layout_id`**, **`replay_row_version`**, and any new **TickCommitRecord_v0** fields.
- Keep **@skipUntil** tags in any new golden / Lane-C prose until **D-043** preimage + **3.1.1** row freeze.

## Sources

- Vault: [[1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems/phase-4-1-1-adapter-preimage-and-stable-column-layout-roadmap-2026-03-24-0018]], [[1-Projects/genesis-mythos-master/Roadmap/decisions-log]], [[1-Projects/genesis-mythos-master/Roadmap/roadmap-state]], [[Ingest/Agent-Research/phase-4-primary-perspective-control-research-2026-03-24]], [[1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/phase-3-1-6-tick-scoped-observable-bundle-post-apply-replay-bridge-roadmap-2026-03-22-0047]] (3.1.6 path per **D-037**).
- External: none required for this slice (vault-first).

## Raw sources (vault)

- No separate raw note; evidence is internal vault cross-references above.
