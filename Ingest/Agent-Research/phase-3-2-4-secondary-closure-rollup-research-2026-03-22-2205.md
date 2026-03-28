---
title: "Research — Phase 3.2.4 secondary closure rollup & advance readiness (pre-deepen)"
created: 2026-03-22
tags: [research, agent-research, genesis-mythos-master, phase-3-2-4, roadmap, handoff-readiness, determinism]
project-id: genesis-mythos-master
linked_phase: Phase-3-2-4-secondary-closure-rollup
agent-research: true
agent-generated: true
research_query: "Phase 3.2.4 secondary closure rollup; G-P3.2 inventory; advance readiness vs execution debt"
source: "Vault-first: phase-3-2-1..3, decisions-log, distilled-core; pattern parity with phase-3-1-7 research + G-P2.2/G-P3.1 rollups"
---

# Phase 3.2.4 — Secondary closure rollup & advance readiness (vault-aligned synthesis)

**Audience:** Roadmap deepen for **genesis-mythos-master** after tertiaries **3.2.1–3.2.3** (DM/regen taxonomy, `RegenRequest_v0` preconditions, regen replay lane + tick commit coupling). **Stack posture:** Cross-runtime contracts only (**D-027**); no engine or language picks.

## Vault context (authoritative elsewhere)

- **3.2.1** — `DmOverrideIntent_v0` vs `RegenRequest_v0`, `StableMergeKey_v0`, regen-before-merge delegation to 3.2.2 — [[phase-3-2-1-dm-override-intent-envelope-and-regeneration-gate-taxonomy-roadmap-2026-03-22-0210]]; **D-041**.
- **3.2.2** — P1–P6, 2.2.2 boundary, regen ledger idempotency sketch — [[phase-3-2-2-regen-request-preconditions-and-gated-subgraph-contract-roadmap-2026-03-22-1735]]; **D-042**, **D-043** (canonical preimage / sort order TBD).
- **3.2.3** — `regen_apply_sequence`, `RegenLaneTotalOrder_v0` A/B, `TickCommitRecord_v0` coupling, optional `regen_subgraph_outcome_row` — [[phase-3-2-3-regen-ledger-replay-rows-and-tick-commit-coupling-roadmap-2026-03-22-1748]]; **D-044**, **D-045** (golden / CI deferral).
- **Rollup precedents:** [[phase-2-2-4-phase-2-2-secondary-closure-rollup-and-advance-readiness-roadmap-2026-03-21-2000]] (G-P2.2 contract vs VCS debt); [[phase-3-1-7-phase-3-1-secondary-closure-rollup-and-advance-readiness-roadmap-2026-03-22-0122]] + research [[Ingest/Agent-Research/phase-3-1-7-secondary-closure-rollup-advance-readiness-research-2026-03-22-1430]] (G-P3.1-\*, normative vs execution HR, advance authority).
- **Decisions:** **D-038** / **D-039** (rollup governs `advance-phase` when `handoff_gate` + `min_handoff_conf`); **D-040** (draft golden row naming not frozen until reconciled with [[phase-2-2-3-ci-golden-registry-and-boundary-regression-gates-roadmap-2026-03-21-1205]]).

**Do not re-spec** field-level schemas for DM override, regen request, or tick rows here — remain on the tertiary notes above.

## 1. What the 3.2.4 rollup note should do

Mirror **2.2.4** and **3.1.7**:

1. **Declare rollup authority** — One tertiary (**3.2.4**) is the **authoritative** pass/fail table for **Phase 3.2 secondary closure** under the same narrative as **D-038**: per-tertiary `handoff_readiness` on **3.2.1–3.2.3** may stay in the low-90s / mixed execution HR; the **rollup** row decides whether **`advance-phase` (3.2 → next macro)** is eligible when `handoff_gate: true` and `min_handoff_conf` matches project policy (historically **93** for prior secondaries — confirm on parent **3.2** and [[roadmap-state]] before freezing text).
2. **Gate inventory table (draft IDs)** — Suggest **G-P3.2-\*** rows, e.g.:
   - **G-P3.2-DM-TAX** → 3.2.1 (channel split, `StableMergeKey_v0`, fail-closed codes vs 2.2.1 sketch).
   - **G-P3.2-REGEN-PRE** → 3.2.2 (P1–P6, 2.2.2 coupling, regen-before-merge).
   - **G-P3.2-REPLAY-LANE** → 3.2.3 (`regen_apply_sequence`, A/B fork documented, tick-close ordering vs post-regen merge).
   - Optional **G-P3.2-REGISTRY-CI** (draft only, **D-040**-style): contract/trace alignment with **2.2.3** + **D-020** PR policy — **PASS** may mean “normative closure in vault + named deferrals,” not green CI.
3. **Verdict + evidence** — Each row: **PASS / HOLD** with wikilink to the tertiary section that satisfies the criterion; **HOLD** must cite a specific decision or open task (e.g. **BLOCKED_ON_OPERATOR** for **RegenLaneTotalOrder_v0** A/B per **D-044**).
4. **Normative vs execution handoff** — Reuse the two-layer story from **3.1.7** / **D-039**: rollup **HR** can reflect **vault-normative** completeness while composite **execution_handoff_readiness** stays lower until **D-032** header, **D-043** preimage freeze, **D-045** golden rows land. State that explicitly in **Open risks**.
5. **Executable assertions** — Short checklist: every **PASS** maps to a wikilinked normative heading; [[decisions-log]] rows **D-041–D-045** are cited for deferrals; no claim of `ReplayAndVerify` coverage until **D-045** gates clear.

## 2. Advance readiness checklist (non-engine)

Stack-agnostic items appropriate for a **secondary closure** bundle:

| Theme | Rollup should confirm |
|--------|------------------------|
| Traceability | Each **G-P3.2-\*** row points at a single authoritative tertiary subsection + decision id where frozen. |
| Ordering story | Text-level closure that regen lane completes before player+DM merge and before tick commit digest — already split across 3.2.1–3.2.3; rollup restates the **whole-tick** narrative once. |
| Versioning | Any cited **gate_version** / **replay_row_version** / registry bump policy is consistent with **D-020** and **3.1.1** — without inventing numeric versions. |
| Operator forks | **RegenLaneTotalOrder_v0** A vs B is either **chosen and logged** or explicitly **HOLD** with pointer to **D-044** / **3.2.3** task. |
| CI honesty | Golden / registry rows deferred per **D-045** are listed under **Open risks**, not smuggled into **PASS** wording. |

External framing (illustrative, non-binding): secondary closure rollups in large programs often mirror **stage-gate** or **evidence pack** practice — a single table that aggregates **definition-of-done** per slice before a **phase transition**. Same idea as summarized in [[Ingest/Agent-Research/phase-3-1-7-secondary-closure-rollup-advance-readiness-research-2026-03-22-1430]] §1–2.

## 3. Suggested skeleton for the Phase 3.2.4 roadmap note

1. **Title** — “Phase 3.2.4 — Phase 3.2 secondary closure rollup & advance readiness”.
2. **TL;DR** — Authoritative **G-P3.2-\*** inventory; rollup `handoff_readiness` vs `min_handoff_conf`; explicit **normative / execution** split.
3. **Gate table** — Three core rows (3.2.1–3.2.3) + optional registry/CI row (**draft** naming until reconciled with **2.2.3** / **D-040**).
4. **Rollup outcome** — e.g. “3/3 PASS (contract)” or “2/3 PASS + 1 HOLD” with reasons.
5. **Open risks** — Operator A/B; **D-032** replay header; **D-043** canonical bytes; **D-045** golden deferral; alignment of `TickCommitRecord_v0` field names with **3.1.1**.
6. **Research integration** — Wikilink [[Ingest/Agent-Research/phase-3-2-4-secondary-closure-rollup-research-2026-03-22-2205]].

## Related vault synthesis

- [[Ingest/Agent-Research/phase-3-2-3-replay-regen-ledger-tickcommit-serialization-research-2026-03-22-1830]]
- [[Ingest/Agent-Research/regenrequest-v0-gated-subgraph-determinism-research-2026-03-22]]
- [[Ingest/Agent-Research/phase-3-1-7-secondary-closure-rollup-advance-readiness-research-2026-03-22-1430]]
