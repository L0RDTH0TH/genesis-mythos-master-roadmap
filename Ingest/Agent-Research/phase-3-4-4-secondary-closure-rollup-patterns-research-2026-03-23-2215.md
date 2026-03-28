---
title: Phase 3.4.4 secondary closure rollup — vault pattern mirror + advance readiness
created: 2026-03-23
tags: [agent-research, genesis-mythos-master, roadmap, phase-3-4, secondary-closure, gate-table]
source: nested ResearchSubagent (RESUME_ROADMAP pre-deepen) + vault corpus + external V&V framing
para-type: Resource
project-id: genesis-mythos-master
---

# Phase 3.4.4 — Secondary closure rollup patterns (research synthesis)

**Scope:** Opening **Phase 3.4.4** as the **single authoritative rollup** for **Phase 3.4 Living world**, mirroring **[[phase-3-2-4-phase-3-2-secondary-closure-rollup-and-advance-readiness-roadmap-2026-03-22-1810]]** and **[[phase-3-3-4-phase-3-3-secondary-closure-rollup-and-advance-readiness-roadmap-2026-03-23-1200]]**. Tertiaries **3.4.1–3.4.3** are treated as **draft-complete** on vault-normative text; rollup separates **normative PASS** from **execution / CI HOLD** rows.

## 1. Normative vs execution handoff split (conceptual anchor)

Industry **verification vs validation** language maps loosely onto this vault’s split: **verification**-style evidence = “contract text, pseudocode, decision rows, and traceability tables exist and cohere”; **validation**-style evidence = “fixtures, registry rows, green jobs, and literal golden encodings prove the story in a repo.” See [TechTarget — Verification vs validation](https://www.techtarget.com/searchsoftwarequality/tip/Verification-vs-validation-in-software-testing) for the generic distinction. **This project’s gate tables** operationalize that split as:

| Lane | What “done” means | Typical artifacts |
|------|-------------------|-------------------|
| **Vault-normative** | PASS / HOLD on **G-P3.x-\*** rows from phase notes + **decisions-log** | Pseudocode blocks, acceptance bullets, **D-05x** references, cross-links to **3.1.x / 3.2.x / 3.3.x** parents |
| **Execution handoff** | **`execution_handoff_readiness`** floor; registry / **ReplayAndVerify**; literal freezes | **D-032** replay header, **D-043** preimage, **2.2.3** policy, **D-045** golden deferral lift |

Do **not** conflate per-tertiary **`handoff_readiness`** (87 / 86 / 85 on **3.4.1–3.4.3**) with rollup **HR**; the rollup note must **inventory PASS/HOLD** explicitly, as **3.3.4** does for **G-P3.3-\***.

## 2. Proposed **G-P3.4-\*** gate inventory (draft labels for 3.4.4 table)

Align gate IDs to the three tertiaries + cross-cuts (same rhythm as **G-P3.2-\*** / **G-P3.3-\***):

| Gate ID | Scope | Evidence anchors | Expected verdict (2026-03-23 vault) |
|--------|--------|------------------|-------------------------------------|
| **G-P3.4-AMBIENT-SCHEDULE** | Ambient slice taxonomy, **`AgencySliceId_v0`** extension, RNG namespaces, regen/persistence predicates | **3.4.1** · **D-052** | **PASS** (normative draft) |
| **G-P3.4-ORDERED-PROJECTION** | Ledger → observable barrier → **`TickCommitRecord_v0`** chain; ambient **`MutationIntent_v0`** ordering | **3.4.2** · **D-053** | **PASS** (normative draft) |
| **G-P3.4-FACET-CATCHUP** | Facet manifest + **`serialization_profile_id`** coupling; idempotent catch-up deferral; replay parity narrative | **3.4.3** · **D-054** | **PASS** (normative draft) |
| **G-P3.4-REGEN-INTERLEAVE** | Single non-dual story for **same-tick** `regen_apply_sequence` vs dependent ambient scalars (**RegenLaneTotalOrder_v0**) | **3.2.3** · **D-044** | **HOLD** until operator logs **A** or **B** in [[decisions-log]] |
| **G-P3.4-REGISTRY-CI** | Golden / registry rows for living-world + ambient mixed ticks; volatile normalizer policy | **2.2.3** · **D-020** · **D-032** / **D-045** | **HOLD** — literal rows + job policy TBD |

**Machine rule (parallel to D-050 / 3.3.4):** Count **three** core living-world gates (**AMBIENT-SCHEDULE**, **ORDERED-PROJECTION**, **FACET-CATCHUP**) as the **3.4** spine **PASS** set. The two **HOLD** rows are **cross-cuts** (regen total order + CI), not “failed tertiaries.” Rollup **`handoff_readiness`** should stay **honest** vs **`min_handoff_conf: 93`** while any **HOLD** remains (expect **≤ 92** pattern matching **3.2.4** / **3.3.4** until **D-044** + registry materialize).

## 3. **D-044** and dual narrative (mandatory wording)

Until **RegenLaneTotalOrder_v0** **A/B** is logged, tertiary notes correctly allow **provisional dual narratives** for regen vs ambient interleaving (**3.4.2**, **3.4.3**). The **3.4.4** rollup must:

- Name **G-P3.4-REGEN-INTERLEAVE** (or explicit cross-link to **G-P3.2-REPLAY-LANE** / **G-P3.3-REGEN-DUAL**) as **HOLD**.
- Forbid claiming **macro advance** or “single interleaving story” in TL;DR while **HOLD** stands.

## 4. Advance readiness — what the rollup + next macro slice need

When **Phase 3** primary MOC lists only **3.1–3.4**, “next macro slice” after **3.4** is either a **new secondary** (e.g. **3.5** when minted) or **Phase 4** — either way, **advance readiness** rows should mirror **3.3.4**:

1. **Rollup closure trace** — one numbered list restating the spine (**3.4.1 → 3.4.2 → 3.4.3**) and dependencies on **3.1.x** schedule, **3.2.x** regen, **3.3.x** persistence (**D-047–D-049**).
2. **G-P3.4-\*** table — PASS/HOLD as above; rollup score arithmetic spelled out.
3. **`handoff_readiness` / `execution_handoff_readiness`** on the **3.4.4** note — composite EHR can floor from **3.4.1–3.4.3** EHR (**48 / 46 / 44**) plus rollup debt; cite **D-032**, **D-043**, **D-037** confirm, **CATCHUP_BUDGET_DEFERRAL** taxonomy registration (**3.4.3**).
4. **Advance eligibility** — explicit sentence: under **`handoff_gate: true`** and **`min_handoff_conf: 93`**, no **`advance-phase`** claim for **3.4 → next** until rollup **HR ≥ 93** or documented policy exception in [[roadmap-state]] / queue payload.
5. **Optional task** — **handoff-audit** bundle trace **3.4** secondary → **3.4.1 → 3.4.2 → 3.4.3 → 3.4.4** before first deepen of **3.5** (or Phase 4).

**External pattern (replay / determinism):** [Fix Your Timestep](https://gafferongames.com/post/fix_your_timestep/) and [Deterministic Lockstep](https://gafferongames.com/post/deterministic_lockstep/) remain valid metaphors for why **total order** and **D-044** are not cosmetic — already cited on **[[phase-3-4-living-world-operations-and-consequence-fan-out-roadmap-2026-03-23-1210]]**.

## 5. Sources

- Vault: **3.2.4**, **3.3.4**, **3.4** secondary, **3.4.1–3.4.3** tertiaries, **[[decisions-log]]**.
- Web: [TechTarget — Verification vs validation](https://www.techtarget.com/searchsoftwarequality/tip/Verification-vs-validation-in-software-testing); Gaffer on timestep / lockstep (links above).
