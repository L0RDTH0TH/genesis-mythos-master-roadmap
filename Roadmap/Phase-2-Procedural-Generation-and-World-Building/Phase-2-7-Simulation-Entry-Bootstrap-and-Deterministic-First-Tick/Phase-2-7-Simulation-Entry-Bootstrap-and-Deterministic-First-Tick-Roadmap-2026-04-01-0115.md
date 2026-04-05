---
title: Phase 2.7 - Simulation-entry bootstrap and deterministic first-tick contract
roadmap-level: secondary
phase-number: 2
subphase-index: "2.7"
project-id: sandbox-genesis-mythos-master
status: active
priority: high
progress: 52
handoff_readiness: 84
created: 2026-04-01
tags:
  - roadmap
  - sandbox-genesis-mythos-master
  - phase-2
para-type: Project
links:
  - "[[Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-03-30-0430]]"
  - "[[Phase-2-6-3-Consumer-Replay-Cold-Start-and-Secondary-2-6-Rollup-Closure-Roadmap-2026-03-30-2109]]"
  - "[[Phase-2-6-Post-Audit-Consumer-Integration-and-Forge-Dialogue-Continuity-Roadmap-2026-03-30-2145]]"
  - "[[decisions-log]]"
---

> [!note] #handoff-review
> `handoff_readiness: 84` — tertiaries **2.7.1–2.7.3** minted — **SimulationEntryBootstrap** + first-tick order + **dry-run shadow** / **hook matrix** / **operator preview** + multi-op admission + **admission ticket redemption** / **shadow-to-live parity** / **FirstCommittedTickTrace**; **2.7 chain complete**; `GMM-2.4.5-*` remain **reference-only**. Next structural cursor **Phase 2 primary rollup** / **advance-phase** gate (workflow `current_subphase_index: "2"`).

## Phase 2.7 - Simulation-entry bootstrap and deterministic first-tick contract

This **secondary 2.7** slice closes the conceptual gap between **post-audit consumer replay** (**2.6.3**) and **running simulation**: it names the **bootstrap record** that must exist before tick `0 → 1`, how it binds to **replay anchors** and **cold-start minimum** from **2.6.3**, and what **deterministic ordering** means for the first observable simulation frame after commit. Anchors `GMM-2.4.5-*` remain **reference-only** deferment IDs.

## Scope

**In scope:**

- **Simulation-entry record** — a single named conceptual artifact (NL) that lists mandatory inputs: final **CommitDecisionEnvelope** identity (from **2.4.x** lineage), **telemetry timeline head** (**2.5.2**), and **replay anchor** (**2.6.3**) sufficient to admit the world into the sim loop.
- **First-tick contract** — what “tick boundary” means at NL: ordering of subsystem hooks (input → world application → observation) for the **first** tick after bootstrap; no engine API.
- **Determinism** — same bootstrap record + same seed lineage ⇒ same first-tick observable ordering (execution proof deferred).

**Out of scope:**

- Fixed timestep scheduling, physics integrator choice, or networking tick models (execution-deferred).
- Compare-table population, registry CI, or HR proof rows (`GMM-2.4.5-*` and related execution artifacts).

## Behavior (natural language)

1. **Bootstrap admission:** Before any simulation tick runs, the runtime (conceptual) **admits** a **SimulationEntryBootstrap** record that references **2.6.3** replay anchor fields and **2.5.2** correlation ordering — no silent bypass of prior commit/audit gates.
2. **First tick:** Subsystems consume **bootstrap** only in the documented order; **deny_commit** / **defer** semantics from **2.4.5** remain authoritative for what world mutations may appear; forge dialogue may **cite** bootstrap surfaces read-only (**2.6** consumer contract).
3. **Cold-start parity:** If `cold_start_minimum` from **2.6.3** is not satisfied, simulation entry is **blocked** until the minimum replay surface is present (NL failure mode, not a new validator).

## Interfaces

Upstream:

- Replay anchor + cold-start: [[Phase-2-6-3-Consumer-Replay-Cold-Start-and-Secondary-2-6-Rollup-Closure-Roadmap-2026-03-30-2109]].
- Secondary **2.6** parent: [[Phase-2-6-Post-Audit-Consumer-Integration-and-Forge-Dialogue-Continuity-Roadmap-2026-03-30-2145]].
- Commit-finalization floor: [[Phase-2-4-5-Commit-Decision-Finalization-Replay-Safety-and-Audit-Handoff-Roadmap-2026-03-31-0345]] (authority by reference only).

Downstream:

- **2.7.1** (minted): [[Phase-2-7-1-Simulation-Entry-Bootstrap-and-Deterministic-First-Tick-Contract-Roadmap-2026-04-01-0116]] — bootstrap field bindings + first-tick hook order.
- **2.7.2** (minted): [[Phase-2-7-2-First-Tick-Dry-Run-Shadow-Hook-Matrix-and-Operator-Bootstrap-Preview-Roadmap-2026-04-01-1200]] — dry-run shadow policy + hook matrix + operator bootstrap preview + multi-operator admission minimum.
- **2.7.3** (minted): [[Phase-2-7-3-Shadow-to-Live-Parity-Admission-Ticket-Redemption-and-First-Committed-Tick-Trace-Roadmap-2026-03-30-1800]] — admission ticket redemption + shadow-to-live parity + FirstCommittedTickTrace (**2.7 chain complete**).

## Edge cases

- **Stale bootstrap:** If replay anchor rotates between **2.6.3** closure and sim entry, **bootstrap** must carry explicit **lineage** pointer — no implicit “latest” without a documented transition (execution binding deferred).
- **Partial telemetry:** If **2.5.2** timeline is incomplete but **commit** is valid, entry may still be **deferred** with a named **defer** state consistent with **2.4** (no synthetic commit).

## Open questions

- Whether **first tick** should expose a **dry-run shadow** of subsystem order before observable tick (tertiary decision).
- Minimum **bootstrap** fields for **multi-operator** forge sessions vs single-DM — execution binding deferred.

## Pseudo-code readiness

At secondary depth, **no pseudo-code** required; interfaces are NL contracts referencing upstream phase notes and deferment IDs.

## Research integration

> [!note] External grounding
> No `Ingest/Agent-Research/` notes bound this mint; continuity is from **2.6.3** replay/cold-start + Phase 2 primary forge glue row ([[Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-03-30-0430]]).

## Tertiary notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/sandbox-genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building/Phase-2-7-Simulation-Entry-Bootstrap-and-Deterministic-First-Tick"
WHERE roadmap-level = "tertiary" OR roadmap-level = "task"
SORT subphase-index ASC, file.name ASC
```
