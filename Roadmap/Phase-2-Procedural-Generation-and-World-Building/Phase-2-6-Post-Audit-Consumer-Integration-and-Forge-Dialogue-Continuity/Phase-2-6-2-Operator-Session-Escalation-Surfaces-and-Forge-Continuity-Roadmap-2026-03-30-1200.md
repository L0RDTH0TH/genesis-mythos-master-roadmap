---
title: Phase 2.6.2 - Operator session escalation surfaces and forge continuity
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.6.2"
project-id: genesis-mythos-master
status: active
priority: high
progress: 42
handoff_readiness: 85
created: 2026-03-30
tags:
  - roadmap
  - genesis-mythos-master
  - phase-2
para-type: Project
links:
  - "[[Phase-2-6-Post-Audit-Consumer-Integration-and-Forge-Dialogue-Continuity-Roadmap-2026-03-30-2145]]"
  - "[[Phase-2-6-1-Post-Audit-Consumer-Bindings-and-Forge-Dialogue-Citation-Roadmap-2026-04-01-2225]]"
  - "[[Phase-2-5-5-Rollup-Chain-Closure-and-Secondary-2-6-Handoff-Roadmap-2026-03-31-2345]]"
  - "[[decisions-log]]"
---

## Phase 2.6.2 - Operator session escalation surfaces and forge continuity

This tertiary closes the **session-level** contract left open by **2.6.1**: how a single operator session **orders** reads across **2.5.1**–**2.5.4** surfaces, when to surface **escalation** (parity breach, missing sealed head, incomplete bind), and how **forge dialogue** chooses between **one rollup narrative** vs **per-sink drill-down** without re-validating **2.3** gates or implying `GMM-2.4.5-*` execution closure.

## Scope

**In scope:**

- **Session orchestration (NL)** — deterministic **read order** inside one session: timeline identity (**2.5.2**) before redaction-sensitive exports (**2.5.3**) before sealed external head checks (**2.5.4**), with explicit **refresh** and **stale** markers when role-scoped views lag canonical timeline.
- **Escalation read paths** — named escalation classes when: parity predicates fail, sealed manifest head is absent, or binding matrix from **2.6.1** is incomplete; each maps to **read-only** operator copy (no compare-table synthesis).
- **Forge continuity mode** — default **per-sink drill-down** as authoritative for evidence quotes; optional **rollup summary** panel is a **non-authoritative** index that must link to sink-specific notes (does not replace drill-down).
- **Role overlap (DM vs auditor)** — when both need audit context: **auditor** path uses canonical timeline + full correlation; **DM-adjacent** path uses **redacted** export lane from **2.6.1** matrix; **overlap** is modeled as **two bound lanes** with the same `decision_correlation_id` anchor, not merged vocabulary.

**Out of scope:**

- UI layout, theming, accessibility.
- Implementing sinks, signing, compare-table rows, or retention jobs (`GMM-2.4.5-*` remain reference-only).

## Behavior (natural language)

1. **Session phases:** (a) establish segment order and correlation keys, (b) verify parity predicates or mark **deferred**, (c) verify sealed head expectation or mark **execution-deferred**, (d) only then allow forge citations that span multiple sinks.
2. **Escalation:** On parity failure → escalation surface lists **which** **2.5.x** contract failed and **preserves** branch vocabulary from **2.4.5** via **2.5** rollup (no collapsed outcomes). On missing sealed head → explicit **deferred** marker; no synthetic validator rows.
3. **Forge turns:** Citation targets remain wikilinks to phase notes + deferment IDs; rollup summary may shorten labels but cannot replace drill-down for claims about branch outcomes.

## Interfaces

Upstream:

- Binding matrix + citation rules: [[Phase-2-6-1-Post-Audit-Consumer-Bindings-and-Forge-Dialogue-Citation-Roadmap-2026-04-01-2225]].
- Timeline + correlation: [[Phase-2-5-2-Cross-Sink-Correlation-and-Deterministic-Timeline-Ordering-Roadmap-2026-03-31-2200]].
- Sealed bundles: [[Phase-2-5-4-Sealed-External-Audit-Bundles-and-Compare-Table-Row-Interchange-Roadmap-2026-03-31-2335]].

Downstream:

- Tertiary **2.6.3** closes **2.6** chain with rollup handoff — see [[Phase-2-6-3-Consumer-Replay-Cold-Start-and-Secondary-2-6-Rollup-Closure-Roadmap-2026-03-30-2109]]; next structural cursor **2.7** (secondary mint).

Outward guarantees:

- Same inputs from **2.6.1** matrix → same session phase ordering and escalation class set (deterministic at NL).
- No forge or session contract implies `GMM-2.4.5-*` completion.

## Edge cases

- **Half-bound session:** If correlation keys exist but sealed head is missing, session stops at **deferred** boundary — forge may cite timeline but not sealed export claims.
- **Stale role export:** **2.5.3** parity predicates still apply; dialogue shows **stale** flag until refresh contract from **2.6.1** is satisfied.

## Open questions

- None blocking at conceptual depth — **2.6.1** open items resolved here: narrative default = **per-sink drill-down** + optional rollup; DM/auditor overlap = **two lanes** with shared correlation anchor.

## Pseudo-code readiness

Depth 3 — interfaces and session ordering are explicit enough to derive implementation checks; no executable pseudo-code required for conceptual completion.

## Parent

- Secondary: [[Phase-2-6-Post-Audit-Consumer-Integration-and-Forge-Dialogue-Continuity-Roadmap-2026-03-30-2145]]

## Research integration

> [!note] External grounding
> No `Ingest/Agent-Research/` notes bound this mint; continuity is from **2.6.1** binding matrix + **2.5.2**/**2.5.3**/**2.5.4** contracts and **2.6** secondary scope.
