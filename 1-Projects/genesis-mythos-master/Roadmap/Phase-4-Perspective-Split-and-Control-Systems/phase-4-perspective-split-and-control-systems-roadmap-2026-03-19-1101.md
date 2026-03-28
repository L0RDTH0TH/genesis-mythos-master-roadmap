---
title: Phase 4 — Perspective Split and Control Systems
roadmap-level: primary
phase-number: 4
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-19
tags: [roadmap, genesis-mythos-master, phase]
para-type: Project
subphase-index: "4"
handoff_readiness: 92
handoff_readiness_scope: "Macro Phase 4 primary: gate table G-P4-* + Phase 3 rollup anchors + REGISTRY-CI junior sketch + operator GMM-P4-PRIMARY-DEEPEN traceability"
execution_handoff_readiness: 40
handoff_gaps:
  - "Phase **4.1** secondary vault work ([[phase-4-1-player-first-perspective-read-model-and-rig-contracts-roadmap-2026-03-24-1201]]) — including **G-P4-1-*** **FAIL (stub)** roll-up rows and **2026-03-24** state-hygiene repair — **does not** clear **G-P4-PLAYER** **OPEN**, **G-P4-REGISTRY-CI** **HOLD**, or Phase **3.* rollup HR 92 < 93** (**D-062**)."
  - "Macro Phase 4 rollup HR not assertable ≥ min_handoff_conf 93 while G-P4-REGISTRY-CI HOLD and Phase 3 secondary rollups remain HR 92 < 93 (D-062 honesty)."
  - "Presentation / camera ReplayAndVerify rows remain @skipUntil(D-032/D-043) for literal replay columns."
  - "Automation cursor authority: use [[workflow_state]] **`last_auto_iteration`** + physical last **`## Log`** data row (**`workflow_log_authority: last_table_row`**) — not Timestamp column sort alone (e.g. **2026-03-24 01:08** Phase **4.1** secondary **`resume-deepen-phase4-1-player-first-gmm-20260324T010800Z`** vs earlier **00:18** **4.1.1** tertiary mint **`resume-deepen-phase4-primary-post-advance-idempotent-gmm-20260324T001800Z`**)."
links:
  - "[[genesis-mythos-master-roadmap-2026-03-19-1101]]"
  - "[[phase-4-2-dm-perspective-read-model-and-rig-contracts-roadmap-2026-03-28-1200]]"
---

## Phase 4 — Perspective Split and Control Systems

### Macro Phase 4 closure / roll-up gate (vault sketch — deferred)

| Gate id | Scope | Status | Authority |
| --- | --- | --- | --- |
| **G-P4-PLAYER** | Player-first read-model + rig (**4.1** / **ARCH-FORK-02**) | **OPEN** — first secondary minted **2026-03-24** | [[phase-4-1-player-first-perspective-read-model-and-rig-contracts-roadmap-2026-03-24-1201]] |
| **G-P4-DM-SHELL** | DM free-cam + orthographic + shared control shell | **OPEN** — conceptual **4.2** authorized **2026-03-28** per **D-131** (parallel with **4.1**; does not fold DM into **4.1** MVP) | [[phase-4-2-dm-perspective-read-model-and-rig-contracts-roadmap-2026-03-28-1200]] · [[decisions-log]] **D-131** |
| **G-P4-REGISTRY-CI** | Presentation / camera golden rows + **ReplayAndVerify** | **HOLD** until **D-032** / **D-043** literal replay fields | Same pattern as **G-P3.*-REGISTRY-CI** — **does not** clear because macro Phase 4 opened (**D-062**) |

**`handoff_readiness` (macro Phase 4):** frontmatter **`handoff_readiness: 92`** (&lt; **`min_handoff_conf` 93**) — vault-honest while **G-P4-REGISTRY-CI** + Phase **3.2.4** / **3.3.4** / **3.4.4** rollup **HR 92** debt remain; **operator `wrapper_approved` Phase 3→4 advance** is **provenance only** — see **D-062** on [[decisions-log]]. **Operator deepen (primary container):** queue **`operator-deepen-phase4-primary-gmm-20260324T003000Z`** (**GMM-P4-PRIMARY-DEEPEN**) — macro gate table + CQRS/replay literacy; **does not** clear **G-P4-REGISTRY-CI** or imply rollup **HR ≥ 93**. **Machine cursor:** authoritative id = **`[[workflow_state]]` `last_auto_iteration`** + last populated **`## Log`** data row (**`workflow_log_authority: last_table_row`**) — currently **`resume-forward-map-phase-41110-gmm-20260326T180000Z`** at **`4.1.1.10`** (forward-map deepen, **2026-03-26 19:05** row). **Historical cursor milestones:** **`resume-deepen-post-recal-distilled-yaml-gmm-20260326T041500Z-followup`** (**12:30 parity deepen**), **`resume-deepen-phase4-1-player-first-gmm-20260324T010800Z`** (early **4.1** widening), and **`resume-deepen-phase4-primary-post-advance-idempotent-gmm-20260324T001800Z`** (non-terminal tertiary mint on [[phase-4-1-1-adapter-preimage-and-stable-column-layout-roadmap-2026-03-24-0018]]) — **do not** treat historical ids as the live automation cursor.

### Operator batch traceability (GMM-P4-PRIMARY-DEEPEN)

| Field | Value |
| --- | --- |
| **Sequencing** | After **3.1.7** / **3.2.4** / **3.3.4** operator rollup deepens (`operator-deepen-phase3-3-3-rollup-gmm-20260323T233237Z` chain) |
| **REGISTRY-CI** | **HOLD** unchanged — same pattern as **G-P3.2-** / **G-P3.3-** / **G-P3.4-** rows until **2.2.3** / **D-020** + repo evidence |
| **Rollup HR 92 < 93** | Remains **vault-honest** on Phase **3.2.4** / **3.3.4** / **3.4.4** rollups — **not** overridden by Phase **4** vault work (**D-062**) |
| **First secondary** | [[phase-4-1-player-first-perspective-read-model-and-rig-contracts-roadmap-2026-03-24-1201]] (**resume-deepen-phase4-first-gmm-20260324T000001Z**) |

### Phase 3 secondary rollup anchors (read-only cross-links)

| Macro slice | Rollup note | Rollup HR vs **min_handoff_conf 93** | HOLD row |
| --- | --- | --- | --- |
| **3.1** | [[phase-3-1-7-phase-3-1-secondary-closure-rollup-and-advance-readiness-roadmap-2026-03-22-0122]] | **93** (meets gate for **3.1→3.2** per **D-038**) | **G-P3.1-GOLDEN** draft vs **2.2.3** |
| **3.2** | [[phase-3-2-4-phase-3-2-secondary-closure-rollup-and-advance-readiness-roadmap-2026-03-22-1810]] | **92** **<** **93** | **G-P3.2-REGISTRY-CI** |
| **3.3** | [[phase-3-3-4-phase-3-3-secondary-closure-rollup-and-advance-readiness-roadmap-2026-03-23-1200]] | **92** **<** **93** | **G-P3.3-REGISTRY-CI** |
| **3.4** | [[phase-3-4-4-phase-3-4-secondary-closure-rollup-and-advance-readiness-roadmap-2026-03-23-1935]] | **92** **<** **93** | **G-P3.4-REGISTRY-CI** |

### Junior CI / registry bundle sketch (macro Phase 4 — vault-normative only)

> [!note] REGISTRY-CI HOLD literacy
> **G-P4-REGISTRY-CI** tracks **presentation / camera** golden rows + **ReplayAndVerify** once **D-032** / **D-043** literal replay columns exist. Until then: **sketch** only — versioned fixture roots, path-scoped CI policy pseudo, **CODEOWNERS** split vs sim goldens (mirror **3.2.4** / **3.3.4** junior bundles). **No** vault assertion of green CI.

## Research integration

### Key takeaways

- Treat **player presentation** (`PresentationViewState_v0`, `CameraBinding_v0`) as **read models** over **post-commit** observables / tick ledger — **CQRS query side**, not a second write path into agency apply.
- **Deterministic replay** hinges on **fixed-step simulation**, controlled **time as input**, and **not feeding render-only data back into sim** unless it is explicitly part of preimage ([[Ingest/Agent-Research/phase-4-primary-perspective-control-research-2026-03-24#2-deterministic-tick-camera-rig-and-replay-coupling-to-observables|§2]] in synthesis).
- **First-person rigs** can compose **multiple presentation channels** (e.g. world vs view-model) from one logical player state — still **presentation composition**, not extra sim.
- **DM orthographic / editor viewports** align with **tooling** patterns; normative DM shell prose is **4.2** per **D-131** (synthesis §3 remains historical framing for pre-**D-131** deferral).
- **Golden / ReplayAndVerify** for presentation must be **hash-stable functions** of **sim-committed preimage** + **serialization profiles**; keep **Lane-C** `@skipUntil(D-032)` until literal replay columns exist ([[Ingest/Agent-Research/phase-4-primary-perspective-control-research-2026-03-24#4-golden-rows-replayandverify-vs-presentation-when-sim-tick-commits-are-authoritative|§4]]).

### Decisions / constraints

- **D-027:** Engine docs in synthesis are **examples only**; normative text stays stack-agnostic.
- **D-059 / D-131:** Do not expand **4.1** MVP to full **DM orthographic + shared shell** — that work is **4.2** [[phase-4-2-dm-perspective-read-model-and-rig-contracts-roadmap-2026-03-28-1200]] (**D-131** authorizes **4.2** in parallel with **4.1**).
- **REGISTRY-CI HOLD:** Do not claim presentation CI closure; anchor future presentation rows to **sim** goldens.

### Links

- [[Ingest/Agent-Research/phase-4-primary-perspective-control-research-2026-03-24|Phase 4 primary perspective/control synthesis]]
- [[Ingest/Agent-Research/phase-3-4-5-sim-presentation-camera-bridge-research-2026-03-22-1245|Earlier sim→presentation bridge research]]

Deliver role-specific control schemes: locked first-person immersion for players and fast free-cam plus orthographic precision tools for DMs. Ensure seamless transitions so viewpoint changes never break decision flow.

- [ ] Implement player first-person interaction rig
- [ ] Implement DM free-cam + orthographic toggle rig
- [ ] Add camera transition interpolator and validate UX continuity

## Subphases & notes

- **4.1 (secondary — player-first spine):** [[phase-4-1-player-first-perspective-read-model-and-rig-contracts-roadmap-2026-03-24-1201]] — **ARCH-FORK-02** per **D-059**; first Phase 4 deepen after operator advance (**D-062** traceability).
- **4.2 (secondary — DM perspective / shell):** [[phase-4-2-dm-perspective-read-model-and-rig-contracts-roadmap-2026-03-28-1200]] — **D-131**; sibling to **4.1**; does not widen **4.1** scope.

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems"
WHERE roadmap-level = "primary" OR roadmap-level = "secondary" OR roadmap-level = "tertiary"
SORT subphase-index ASC, file.name ASC
```
