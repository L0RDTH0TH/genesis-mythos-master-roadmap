---
title: Phase 3.2 — DM overwrite and regeneration gates
roadmap-level: secondary
phase-number: 3
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-21
tags: [roadmap, genesis-mythos-master, phase, dm, regeneration, intent]
para-type: Project
subphase-index: "3.2"
handoff_readiness: 92
handoff_readiness_scope: "Tertiary **3.2.1–3.2.4** + authoritative **G-P3.2-\*** rollup on **3.2.4**; **2/3** gate PASS + **HOLD** on **RegenLaneTotalOrder_v0** A/B until **D-044** logged; golden vectors + registry still TBD (**D-041** / **D-042** / **D-044** / **D-045**)"
execution_handoff_readiness: 61
handoff_gaps:
  - "Golden replay vectors for override-before-manifest vs regen-subgraph ordering — TBD until repo + **D-032** header freeze"
  - "Closed `reason_code` strings must reconcile with **2.2.1** registry before CI asserts"
links:
  - "[[phase-3-living-simulation-and-dynamic-agency-roadmap-2026-03-19-1101]]"
  - "[[phase-2-2-2-intentplan-consumption-boundary-and-deterministic-verification-harness-roadmap-2026-03-20-0605]]"
  - "[[phase-2-2-1-intent-canonicalization-and-denial-taxonomy-roadmap-2026-03-20-0901]]"
  - "[[phase-3-2-1-dm-override-intent-envelope-and-regeneration-gate-taxonomy-roadmap-2026-03-22-0210]]"
  - "[[phase-3-2-2-regen-request-preconditions-and-gated-subgraph-contract-roadmap-2026-03-22-1735]]"
  - "[[phase-3-2-3-regen-ledger-replay-rows-and-tick-commit-coupling-roadmap-2026-03-22-1748]]"
  - "[[phase-3-2-4-phase-3-2-secondary-closure-rollup-and-advance-readiness-roadmap-2026-03-22-1810]]"
---

## Phase 3.2 — DM overwrite and regeneration gates

**Deliverables (draft):** Explicit DM override channel vs structural regeneration; denial / reason-code alignment with Phase 2.2.1 taxonomy; seams to `IntentPlan` consumption boundary and Phase 3.1 apply ledger / tick commit.

**Interfaces:** Generation hooks from Phase 2.2; replay harness — overrides must not break manifest hash preimage without documented gate bump; DM overrides ordered with player intents per **3.1.5** / **3.1.6**.

**Acceptance sketch:** Override events are logged in deterministic order; regen paths re-run golden-safe subsets or emit fail-closed denials — **normative regen precondition / `reason_code` surface:** [[phase-3-2-2-regen-request-preconditions-and-gated-subgraph-contract-roadmap-2026-03-22-1735]] (**D-042**); envelope + merge ordering context in **3.2.1**.

### Tertiary spine

- **3.2.1** — [[phase-3-2-1-dm-override-intent-envelope-and-regeneration-gate-taxonomy-roadmap-2026-03-22-0210]] — `DmOverrideIntent_v0` vs `RegenRequest_v0`, regen gate version, fail-closed codes — **D-041**.
- **3.2.2** — [[phase-3-2-2-regen-request-preconditions-and-gated-subgraph-contract-roadmap-2026-03-22-1735]] — `RegenRequest_v0` field row, P1–P6 preconditions, **regen-before-merge** ordering, **2.2.2** coupling — **D-042**.
- **3.2.3** — [[phase-3-2-3-regen-ledger-replay-rows-and-tick-commit-coupling-roadmap-2026-03-22-1748]] — `regen_apply_sequence`, **RegenLaneTotalOrder_v0** (A/B), **`TickCommitRecord_v0`** coupling, optional `regen_subgraph_outcome_row` — **D-044**.
- **3.2.4** — [[phase-3-2-4-phase-3-2-secondary-closure-rollup-and-advance-readiness-roadmap-2026-03-22-1810]] — **G-P3.2-\*** secondary closure rollup + advance readiness (**D-046**).

## Tertiary notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, handoff_readiness AS "Handoff"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency"
WHERE roadmap-level = "tertiary" AND contains(subphase-index, "3.2")
SORT subphase-index ASC
```
