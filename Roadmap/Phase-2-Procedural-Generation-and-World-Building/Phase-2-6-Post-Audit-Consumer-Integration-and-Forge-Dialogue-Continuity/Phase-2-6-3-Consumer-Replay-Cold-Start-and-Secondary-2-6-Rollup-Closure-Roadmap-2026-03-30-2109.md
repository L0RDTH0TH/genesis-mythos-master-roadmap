---
title: Phase 2.6.3 - Consumer replay anchors, cold-start binding, and secondary 2.6 rollup closure
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.6.3"
project-id: genesis-mythos-master
status: active
priority: high
progress: 48
handoff_readiness: 86
created: 2026-03-30
tags:
  - roadmap
  - genesis-mythos-master
  - phase-2
para-type: Project
links:
  - "[[Phase-2-6-Post-Audit-Consumer-Integration-and-Forge-Dialogue-Continuity-Roadmap-2026-03-30-2145]]"
  - "[[Phase-2-6-2-Operator-Session-Escalation-Surfaces-and-Forge-Continuity-Roadmap-2026-03-30-1200]]"
  - "[[Phase-2-6-1-Post-Audit-Consumer-Bindings-and-Forge-Dialogue-Citation-Roadmap-2026-04-01-2225]]"
  - "[[Phase-2-5-2-Cross-Sink-Correlation-and-Deterministic-Timeline-Ordering-Roadmap-2026-03-31-2200]]"
  - "[[decisions-log]]"
---

## Phase 2.6.3 - Consumer replay anchors, cold-start binding, and secondary 2.6 rollup closure

This tertiary closes the **2.6** tertiary chain (**2.6.1–2.6.3**) by binding **replay** and **cold-start** read contracts to the same deterministic anchors used in **2.6.2** session orchestration, then emitting a **rollup closure** row mirroring **2.5.5** so Phase 2 can advance to the next structural secondary (**2.7**) without implying any `GMM-2.4.5-*` execution completion.

## Scope

**In scope:**

- **Replay anchor** — a stable, replayable **consumer read cursor** that concatenates: (1) `decision_correlation_id` / segment identity from **2.5.2**, (2) binding-matrix lane from **2.6.1**, (3) **2.6.2** session phase ordinal — so a consumer can resume or diff sessions without re-executing validation gates.
- **Cold-start minimum** — the smallest named contract set required before any **2.5.3** parity or **2.5.4** sealed-head check may run (ordered: timeline identity → matrix lane → session phase list); explicit **blocked** state when any prerequisite is absent (no synthetic rows).
- **Cross-session forge continuity** — forge dialogue may cite **replay anchor** + wikilinks; citations remain **read-only** and **non-authoritative** for branch outcomes (rollup panel stays non-authoritative per **2.6.2**).
- **Secondary 2.6 rollup closure** — one checklist-style rollup mirroring **2.5.5**: tertiaries **2.6.1** (bindings + citation), **2.6.2** (session + escalation + forge drill-down), **2.6.3** (replay + cold-start + closure); **2.6 chain complete**.

**Out of scope:**

- Storage format for replay tokens, session persistence, or forge UI.
- Compare-table synthesis, retention jobs, or validator registry rows (`GMM-2.4.5-*` remain reference-only).

## Behavior (natural language)

1. **Replay:** Given the same upstream inputs from **2.5.1–2.5.4** surfaces, the **replay anchor** deterministically names the ordered read path; consumers may **diff** two anchors to detect stale role exports or missing sealed heads without re-validating **2.3** gates.
2. **Cold-start:** On first open with no session state, the consumer loads **cold-start minimum** only; forge and operator panels refuse parity/sealed claims until the minimum is satisfied (explicit **deferred** markers).
3. **Closure:** Rollup row states **2.6 chain complete (2.6.1–2.6.3)**; next structural target is **secondary 2.7** (mint) under Phase 2 per MOC / operator priority.

## Interfaces

Upstream:

- Session + escalation + forge defaults: [[Phase-2-6-2-Operator-Session-Escalation-Surfaces-and-Forge-Continuity-Roadmap-2026-03-30-1200]].
- Binding matrix + citation: [[Phase-2-6-1-Post-Audit-Consumer-Bindings-and-Forge-Dialogue-Citation-Roadmap-2026-04-01-2225]].
- Timeline identity: [[Phase-2-5-2-Cross-Sink-Correlation-and-Deterministic-Timeline-Ordering-Roadmap-2026-03-31-2200]].

Downstream:

- **Secondary 2.7** — next Phase 2 secondary mint (scope named on first deepen pass at **2.7**).

Outward guarantees:

- Same upstream contract inputs → same replay anchor string class (deterministic at NL).
- No closure row implies execution completion for deferred anchors.

## Edge cases

- **Partial matrix bind:** Replay anchor may be recorded as **incomplete** with explicit lane missing — cold-start still blocks downstream parity until **2.6.1** matrix row exists.
- **Forge cite without session:** Allowed for timeline-only claims; sealed or parity claims require session phase list from **2.6.2**.

## Open questions

- None blocking at conceptual depth — **2.6** secondary open items are satisfied by **2.6.1–2.6.3** decomposition; naming and scope for **2.7** remain for the next mint.

## Pseudo-code readiness

Depth 3 — replay/cold-start/closure are explicit enough for implementation checklists; no executable pseudo-code required for conceptual completion.

## Parent

- Secondary: [[Phase-2-6-Post-Audit-Consumer-Integration-and-Forge-Dialogue-Continuity-Roadmap-2026-03-30-2145]]

## Research integration

> [!note] External grounding
> No `Ingest/Agent-Research/` notes bound this mint; continuity is from **2.6.1**/**2.6.2** plus **2.5.2** timeline contracts and **2.5.5** rollup pattern reference.
