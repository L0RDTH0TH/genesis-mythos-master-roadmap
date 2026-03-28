---
title: "Research — Phase 3.1.7 secondary closure rollup & advance readiness (pre-deepen)"
created: 2026-03-22
tags: [research, agent-research, genesis-mythos-master, phase-3-1-7, simulation, determinism, handoff-readiness]
project-id: genesis-mythos-master
linked_phase: Phase-3-1-7
agent-research: true
agent-generated: true
research_query: "Phase 3.1.7 secondary closure rollup; normative vs execution HR; DST golden rows"
research_tools_used: [web_search, mcp_web_fetch]
research_escalations_used: 0
ira_validator_repair_applied: true
---

# Phase 3.1.7 — Secondary closure rollup & advance readiness (external patterns + vault alignment)

**Audience:** Roadmap deepen for **genesis-mythos-master**, tertiary **3.1.7** after **3.1.6** (observable bundle + `TickCommitRecord` bridge). **Goal:** Stack-agnostic patterns for **rollup notes**, **handoff readiness tables**, **normative vs execution readiness**, and **deterministic simulation / CI golden rows**—without duplicating vault contracts already stated in **3.1.1–3.1.6**.

## Vault context (do not duplicate)

**Already in vault:**

- **Phase 3.1 parent** ([[phase-3-1-simulation-tick-scheduler-and-time-quanta-roadmap-2026-03-21-2346]]) defines **### Tertiary roll-up (≥93 closure)** with per-tertiary **Normative HR** vs **Execution HR**, **Blocking?**, and links through **3.1.6**; secondary `handoff_readiness: 88` with explicit gap until rollup satisfies the table.
- **3.1.6** closes the **post-apply observable barrier** and `SimObservableBundleTelemetry_v0` draft; **D-037** adoption in [[decisions-log]].
- **Rollup pattern precedents:** [[phase-2-1-7-phase-2-1-secondary-closure-rollup-and-advance-readiness-roadmap-2026-03-19-2110]] (**G-P2.1-\*** inventory, PASS + evidence, rollup authority, executable assertions) and [[phase-2-2-4-phase-2-2-secondary-closure-rollup-and-advance-readiness-roadmap-2026-03-21-2000]] (**contract/spec PASS** vs **VCS implementation debt** explicitly separated in **Open risks**).

**Do not duplicate:** The exact hash preimage fields, `CatchUpPolicy_v0`, pause semantics, slice schedule, mutation ledger, or observable bundle schema—those remain authoritative on their tertiary notes and decisions **D-031–D-037**.

## 1. Secondary closure rollups (what the note should *do*)

Mirror **2.1.7** / **2.2.4**:

1. **Declare rollup authority** — one tertiary (**3.1.7**) is the **authoritative** pass/fail table for **Phase 3.1 secondary closure**; per-tertiary `handoff_readiness` on **3.1.1–3.1.6** may stay mixed; **rollup** governs `advance-phase` when `handoff_gate: true` (same narrative as 2.1.7 § Rollup authority).
2. **Gate inventory table** — use **suggested draft** gate IDs only (e.g. **G-P3.1-TICK** → 3.1.1, **G-P3.1-CATCHUP** → 3.1.2, … **G-P3.1-OBS** → 3.1.6) with **Verdict** + **Evidence** wikilinks; **reconcile IDs with vault gate inventories and [[decisions-log]] before any freeze**—do not treat this research note as a registry.
3. **Rollup outcome line** — count PASS/HOLD; call out **non-blocking implementation debt** the way **2.2.4** separates **contract complete** from **repo fixtures landed**.
4. **Executable assertions** — traceability (each PASS → note with normative sections), decision sync (**D-030–D-037** + parent table), advance precondition (`handoff_readiness` on **3.1.7** vs `min_handoff_conf`).

Illustrative vocabulary for stage-gate / evidence-pack style rollups (not normative standards): see **Supplementary sources** below.

## 2. Handoff readiness tables (normative vs execution)

The vault already uses two columns (**Normative HR** / **Execution HR**) in the **3.1** parent rollup table. External framing that fits:

- **Verification vs validation (V&V):** *Verification* ≈ “building the system right” (specs, contracts, traceable criteria); *validation* ≈ “building the right system” (stakeholder / outcome fit). Your **normative** column maps cleanly to **contract + trace completeness**; **execution** maps to **artifacts in repo / CI / golden rows** that prove those contracts in a runtime.
- **Definition of Done vs acceptance criteria:** DoD is **shared universal** quality bars; acceptance criteria are **per item**. Rollup rows behave like **per-slice acceptance** backed by evidence links; the **3.1.7** note itself acts as a **DoD-like bundle** for the whole secondary.

**Practical constraint for 3.1.7:** When writing the rollup, **explicitly state** that **PASS (contract)** can coexist with **Execution HR &lt; 93** and **no golden row**—matching **2.2.4** and **D-031 / D-032 / D-036 / D-037** language (“no CI / golden claims until …”).

## 3. Deterministic simulation & CI “golden row” patterns (stack-agnostic)

**Deterministic simulation testing (DST):** Per [Antithesis — deterministic simulation testing](https://antithesis.com/docs/resources/deterministic_simulation_testing/), DST places software in a **simulated, deterministic** environment, controlling **clocks, thread interleaving, RNG** so failures **replay**; it is often paired with **property-based testing, fuzzing, fault injection**. The same article states that **“practical adoption of this approach was pioneered at FoundationDB and Amazon Web Services around 2010”** and contrasts (a) **designing nondeterministic components as pluggable** (popularized via FoundationDB’s simulation docs) with (b) running non-deterministic software **inside a deterministic hypervisor**—two implementation patterns, both described on that page.

[Source: Antithesis — deterministic simulation testing](https://antithesis.com/docs/resources/deterministic_simulation_testing/)

**Golden / snapshot rows in CI:**

- **Golden master / snapshot testing** stores **expected outputs**; CI fails on diff—promotion is a **reviewed, intentional** update. For **sim ticks**, a **golden row** is a **pinned (seed, inputs, serialized replay header, expected commit / observable hash tuple)** versioned beside **`replay_row_version`** (already normative in 3.1.x notes).
- **Schema vs snapshot:** Schema-style checks give **reviewable, additive** evolution; raw snapshots catch **subtle regressions** but need **normalization** to avoid flaky CI. For **tick pipelines**, prefer **schema’d golden fixtures** + **deterministic harness** over opaque binary blobs where possible.

[Source: dev.tools — schema vs snapshot testing for APIs in CI](https://dev.tools/blog/schema-vs-snapshot-testing-for-apis-what-actually-works-in-ci/)

**Implication for 3.1.7 rollup (draft):** Consider a row or subsection **G-P3.1-GOLDEN** (name **not** frozen until reconciled) that states: **contract PASS** can require **named golden dimensions** (which checksums / rows / registry policy) even if **VCS row** is still **backlog**—parallel to **G-P2.2-CI** in **2.2.4**. **Reconcile gate naming with vault before freeze.**

## 4. Suggested content skeleton for the Phase 3.1.7 roadmap note

1. **Title** — “Phase 3.1.7 — Phase 3.1 secondary closure rollup & advance readiness”.
2. **TL;DR** — Normative rollup for **draft G-P3.1-\*** spine completeness; **advance** authority; align **parent ### Tertiary roll-up** to **≥93** when policy says so.
3. **Gate table** — six rows (3.1.1–3.1.6) minimum using **draft** IDs; optional seventh for **cross-cutting golden / registry** alignment with [[phase-2-2-3-ci-golden-registry-and-boundary-regression-gates-roadmap-2026-03-21-1205]] / EMG-2 rollup if still in scope—**reconcile IDs before freeze**.
4. **Executable assertions** — mirror 2.1.7 §46–48.
5. **Open risks** — implementation debt vs HOLD (2.2.4 pattern).
6. **Research integration** — inject block from parent Roadmap run + wikilink here.

## Raw sources (excerpts)

Access date **2026-03-22** for fetches below.

### Antithesis — deterministic simulation testing

> Practical adoption of this approach was pioneered at FoundationDB and Amazon Web Services around 2010, and seems to have been a case of simultaneous invention, or rather, implementation, since the idea itself predates both these instances.

> One approach, popularized by FoundationDB, is to design the system under test so that all nondeterministic components are pluggable.

> Another approach is to run regular non-deterministic software inside a deterministic hypervisor, using a system like Antithesis.

— From [Deterministic simulation testing](https://antithesis.com/docs/resources/deterministic_simulation_testing/) (retrieved 2026-03-22).

### dev.tools — schema vs snapshot testing

> Schema testing validates responses against a contract (JSON Schema/OpenAPI)… Snapshot testing stores exact response representations… The key principle: CI requires changes to be detectable, reviewable, and repeatable—making snapshot testing effective when properly controlled.

— Paraphrased / excerpted from [Schema vs Snapshot Testing for APIs: What Actually Works in CI](https://dev.tools/blog/schema-vs-snapshot-testing-for-apis-what-actually-works-in-ci/) (retrieved 2026-03-22).

## Supplementary sources (checklist / blog tier — not normative evidence)

These links are **illustrative vocabulary only** for phase gates, checklists, DoD vs acceptance, and V&V blog summaries—they are **not** standards bodies or primary technical evidence for simulation CI.

- [Fit Gap — completion criteria / evidence packs](https://us.fitgap.com/stack-guides/closing-the-gap-between-deployed-and-done-with-completion-criteria-and-evidence-packs)
- [Professional QA — phase-end audit checklist](https://www.professionalqa.com/phase-end-audit-checklist)
- [Seann Hicks — acceptance criteria vs definition of done](https://www.seannhicks.com/blog/acceptance-criteria-vs-definition-of-done/)
- [Easterbrook — verification vs validation (blog)](https://www.easterbrook.ca/steve/2010/11/the-difference-between-verification-and-validation/)

## Sources

### Primary

- [Antithesis — Deterministic simulation testing](https://antithesis.com/docs/resources/deterministic_simulation_testing/)
- [dev.tools — Schema vs snapshot testing for APIs in CI](https://dev.tools/blog/schema-vs-snapshot-testing-for-apis-what-actually-works-in-ci/)

### Supplementary

- [Fit Gap — evidence packs / completion criteria](https://us.fitgap.com/stack-guides/closing-the-gap-between-deployed-and-done-with-completion-criteria-and-evidence-packs)
- [Professional QA — Phase end audit checklist](https://www.professionalqa.com/phase-end-audit-checklist)
- [Seann Hicks — Acceptance criteria vs definition of done](https://www.seannhicks.com/blog/acceptance-criteria-vs-definition-of-done/)
- [Easterbrook — Verification vs validation](https://www.easterbrook.ca/steve/2010/11/the-difference-between-verification-and-validation/)
