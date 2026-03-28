---
title: Phase 3.4.8 prep — high Ctx Util policy, execution gates (D-044/D-059), CQRS-style presentation split
research_query: "phase-3-4-8 context util 80 policy recal handoff-audit deepen D-044 D-059 T-P4 CQRS presentation"
linked_phase: "Phase-3-4-8 (mint target — after 3.4.7 WBS / Phase 4.1 bridge)"
project_id: genesis-mythos-master
created: 2026-03-22
tags: [research, agent-research, genesis-mythos-master, roadmap, context-util, cqrs, presentation]
agent-generated: true
research_tools_used: [vault_grounded, pattern_synthesis]
---

# Research synthesis — tertiary **3.4.8** support (vault-first)

**Audience:** Roadmap deepen for **genesis-mythos-master** after **3.4.7** (`handoff_readiness` 84, `execution_handoff_readiness` 36). **Do not duplicate** the WBS table on [[phase-3-4-7-perspective-entry-wbs-and-phase-4-1-task-bridge-roadmap-2026-03-22-0748]] — this note adds **policy**, **gating**, and **architectural patterns** only.

## 1. High context utilization (~80%) — roadmap automation policy

**As-of (synthesis snapshot):** `2026-03-22T12:15:00Z` — numbers below are a **point-in-time copy** from [[1-Projects/genesis-mythos-master/Roadmap/workflow_state]]; automation must **re-read** that file before acting, not treat this paragraph as live truth.

**Vault facts:** Last `## Log` data row for queue `resume-gmm-deepen-followup-post-empty-bootstrap-20260322T074810Z` (**2026-03-22 08:05**, Phase **3.4.7**) records **Ctx Util 80%**, **Threshold 80%**, **Est. Tokens 102400 / 128000**, **Confidence 78**, with status text including *"at threshold — monitor RECAL policy on next deepen"* — see [[1-Projects/genesis-mythos-master/Roadmap/workflow_state]].

**Corroborated precedent (Phase 2.2, low util + HR gap):** Same table row **2026-03-20 07:50** — action **`handoff-audit`**, bundle **Phase-2-2-Intent-Parser-Integration-Generation-Hooks**, **Ctx Util 32%**, **handoff_readiness 78** below **min_handoff_conf 93** with `handoff_gaps` called out in the Status/Next column — [[1-Projects/genesis-mythos-master/Roadmap/workflow_state]].

**Recommended decision matrix (automation-facing):**

| Signal | Prefer | Rationale |
| --- | --- | --- |
| **estimated_tokens > 90% of context_window** (deepen overflow) | **`recal`** (RESUME_ROADMAP `action: recal`) then re-queue deepen | Matches global guardrail: context-overflow → RECAL-ROAD; do not stack another full-context deepen on a hot run. |
| **Ctx Util at/just above configured threshold (e.g. 80%)** and **last_conf mid (70–85)** | **Shallow deepen** *or* **`handoff-audit`** on the **current phase bundle** | You are bandwidth-limited; either narrow the next artifact (smaller `token_cap`, fewer inject_extra_state pulls) **or** machine-trace delegatability before burning another full pass. |
| **Ctx Util high** but **contradictions / stale frontmatter vs last log row** | **`recal`** or **IRA-hygiene fix** (not raw deepen) | Nested **roadmap_handoff_auto** passes on this project have raised **`state_hygiene_failure`** when `workflow_state` YAML (e.g. `last_ctx_util_pct` / `last_conf`) **drifted** from the authoritative last `## Log` row under `workflow_log_authority: last_table_row` — fix alignment before trusting util; example first-pass report: [[3-Resources/Second-Brain/Validator-Reports/roadmap_handoff_auto/genesis-mythos-master-20260323T163500Z-phase-3-4-1-deepen-250.md]]; cleared follow-up narrative: [[3-Resources/Second-Brain/Validator-Reports/roadmap_handoff_auto/genesis-mythos-master-20260323T180000Z-phase-3-4-1-deepen-250-ira-compare-final.md]]. |
| **Target phase HR unknown or stale** | **`handoff-audit`** | Produces trace + `handoff_gaps` consumable; same pattern as workflow rows at 61% util for Phase 3.2 bundle. |
| **Low util + low confidence** | **Pre-deepen research** (already wired) | Roadmap rule: util **below** `research_util_threshold` (default 30) triggers research enablement with veto — opposite end of the spectrum from the 80% case. |

**Operational takeaway for 3.4.8:** Treat **80% @ threshold** as a **yellow**: next deepen should assume **tighter budgets**, avoid **large distilled-core replay** unless needed, and **log** whether the run chose **audit vs narrow deepen vs recal** in the next workflow row’s Status/Next column for traceability.

### Deepen inject (paste-oriented checklist for phase 3.4.8)

1. **Re-read** [[1-Projects/genesis-mythos-master/Roadmap/workflow_state]] **before** copying any util/token numbers into the phase note; align **YAML** `last_ctx_util_pct` / `last_conf` with the **last** `## Log` row after the run (hygiene gate).
2. In the **next** workflow log row, state explicitly whether this run was **handoff-audit**, **narrow deepen** (reduced `token_cap` / fewer inject pulls), or **`recal`** / RECAL-ROAD — per the matrix above.
3. **Token budget:** Prefer a **lower** effective context budget when **Ctx Util** is at/above threshold and **last_conf** is mid-band; do not stack full-context deepen on overflow-risk without **recal** first.
4. **Do not assume closure** on **D-044** / **D-059** in narrative until decisions-log records the operator pick ([[1-Projects/genesis-mythos-master/Roadmap/decisions-log]]); keep **T-P4-05**-class work **DEFERRED** / dual-track per §2 below.
5. **CQRS vocabulary** here is **labeling only** for adapter→rig split; it does **not** override **D-027** engine choice or **D-044** ordering.

## 2. Execution gating after **T-P4-01…T-P4-05** with **D-044** and **D-059** open

**Vault authority:** [[1-Projects/genesis-mythos-master/Roadmap/decisions-log]] **D-044** — `RegenLaneTotalOrder_v0` **Option A vs B** not logged; **D-059** — **ARCH-FORK-01** vs **ARCH-FORK-02** pending. [[phase-3-4-7-perspective-entry-wbs-and-phase-4-1-task-bridge-roadmap-2026-03-22-0748]] DEFERRED ledger ties **T-P4-05** to **D-044** and architect fork registry.

**Gating rules (normative vs execution):**

1. **Vault-normative work** (spec text, Given/When/Then, package-boundary narrative, lane tags) on **T-P4-01…T-P4-04** may proceed **without** resolving **D-044/D-059** — consistent with **D-055** / **D-058** pattern: PASS on contract text, HOLD on cross-cutting literals.
2. **Any leaf that orders **DM/tool promotion** into **`MutationIntent_v0` / merge / regen lane** (**T-P4-05** class)** must stay **DEFERRED** or **dual-track** until **D-044** operator pick — matches **D-044** implementation guard and **3.4.7** pseudo-code comments.
3. **Minting the first **Phase 4.1** tertiary *tree*** (not just bridge text) should **not** assume **ARCH-FORK-01** or **ARCH-FORK-02** until **D-059** logs a pick — otherwise risk conflicting spine order under **D-058**.
4. **CI / golden / ReplayAndVerify** rows remain under **D-032**, **D-043**, **D-045** regardless of WBS progress — do not conflate WBS checkboxes with execution closure.

## 3. Industry patterns — read-model presentation vs simulation mutation

**Intent:** Give juniors a **named pattern** for the **adapter → rig** split and “no ledger append from presentation” without picking an engine (**D-027**).

**CQRS (Command Query Responsibility Segregation):** Separate **models that mutate authoritative state** (commands → domain invariants → events/state) from **models optimized for read/display**. Presentation consumes **read models**; it does not author **commands** except through explicit **application APIs** (here: **`ToolActionQueue_v0` → promotion → `MutationIntent_v0`**).

**Event sourcing alignment (selective):** Simulation tick processing resembles **folding an append-only ledger** (slices, mutations, commit record). **Projections** (observables, `PresentationViewState_v0`) are **derived views**; rewinding replay recomputes them from the same inputs — presentation code should depend on **committed view state**, not on re-running mutation paths ad hoc.

**Game/sim loop analogy:** Many engines separate **simulation step** (fixed tick, deterministic inputs) from **presentation interpolation** (frame-rate dependent). Your vault already encodes this as **lane A/B/C** — this research only **labels** the separation as CQRS-style **read side vs write side** for cross-team vocabulary.

**Anti-pattern:** **Fat view** that calls **spawn / mutate / regen** APIs directly — violates **T-P4-03** package-boundary intent and blurs **D-044** ordering surface.

## Raw sources (vault)

- [[1-Projects/genesis-mythos-master/Roadmap/workflow_state]]
- [[1-Projects/genesis-mythos-master/Roadmap/decisions-log]]
- [[1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/phase-3-4-7-perspective-entry-wbs-and-phase-4-1-task-bridge-roadmap-2026-03-22-0748]]
- [[1-Projects/genesis-mythos-master/Roadmap/distilled-core]]

## Sources (external pattern refs)

- [Source: CQRS (Martin Fowler)](https://martinfowler.com/bliki/CQRS.html)
- [Source: Event Sourcing (Martin Fowler)](https://martinfowler.com/eaaDev/EventSourcing.html)
