---
title: Research — Phase 2.3 validate co-authored world emergence (test seeds)
created: 2026-03-21
tags: [research, agent-research, genesis-mythos-master, phase-2-3, world-emergence]
para-type: Project
project-id: genesis-mythos-master
linked_phase: Phase-2-3-Validate-Co-authored-World-Emergence
research_query: "procedural world generation test harness golden seeds; simulation emergence validation deterministic replay; property-based testing world state co-authoring"
research_tools_used: [web_search, mcp_web_fetch]
research_escalations_used: 0
research_synthesis_rubric: "coverage: pass (three query themes addressed). traceability: pass after IRA patch (see External source traceability). actionability: pass (metrics + backlog sections). No numeric self-grade."
agent-generated: true
---

# Phase 2.3 — Co-authored world emergence & test seeds (external synthesis)

**Scope:** Bridge **Phase 2** primary intent — *validate co-authored world emergence through test seeds* — with industry and research patterns for **deterministic replay**, **golden / seeded fixtures**, **PCG evaluation**, and **property-based validation** of evolving world state. This note extends (without repeating) vault work on **IntentPlan**, **ReplayAndVerify**, and **CI golden registry** (Phase 2.2.x).

**Do-not-duplicate (vault):** Phase 2.2 already freezes canonical intent bytes, harness vectors G1–G3/F1–F2, and CI promotion policy; this note focuses on **emergent outcomes** when **lore/intent** and **simulation** co-produce world state.

---

## Phase 2.3 emergence metrics (executable)

Named metrics for **ReplayAndVerify** / golden extensions (IDs align to existing harness vocabulary **G1–G3**, **F1–F2**; field names below are **placeholders** until bound to the normative schema in [[phase-2-2-2-intentplan-consumption-boundary-and-deterministic-verification-harness-roadmap-2026-03-20-0605]] — use **TBD** where the repo does not yet name columns).

| Symbol | Inputs (ledger / manifest) | Units | Pass / fail | Harness bridge |
|--------|------------------------------|-------|-------------|------------------|
| **EMG-1 `replay_emergence_hash`** | `seed_envelope`, `intent_ledger_tail` through tick **N**, `manifest_hash` after `SpawnCommit` (TBD: exact paths from phase notes) | 256-bit hex string | **Pass:** bitwise match to golden for fixed (seed, fixture id). **Fail:** any divergence. | Extends **G1–G3** vector idea with an extra **derived** hash column (new row in golden registry when Phase 2.3 lands). |
| **EMG-2 `lore_sim_alignment_score`** | `authoritative_lore_flags` (TBD) vs `sim_observed_counters` (TBD) after N ticks | Int in [0, 100] | **Pass:** score ≥ floor **F** (set in Phase 2.3 spec). **Fail:** below floor or undefined flags. | Maps to **F1–F2** “boundary” spirit: cross-check author vs sim; exact floor **TBD**. |
| **EMG-3 `denial_invariant_closed`** | `denial_taxonomy` codes emitted during run | Count of unexpected open denials | **Pass:** zero unexpected codes vs allow-list. **Fail:** any code not in frozen set from [[phase-2-2-1-intent-canonicalization-and-denial-taxonomy-roadmap-2026-03-20-0901]]. | Same closure class as **ReplayAndVerify** denials — reuse taxonomy, new assertion on emergence path. |

---

## Genesis coupling — verified vs hypothetical

| Claim in this note | Status | Evidence / next step |
|--------------------|--------|----------------------|
| Stage pipeline, manifests, `SpawnCommit`, hierarchical RNG | **Verified (vault)** | [[phase-2-1-stage-pipeline-skeleton-seed-to-entity-contracts-roadmap-2026-03-19-1912]], [[distilled-core]] Phase 2.1.x decisions |
| IntentPlan + `ReplayAndVerify` + G1–G3 / F1–F2 | **Verified (vault)** | [[phase-2-2-2-intentplan-consumption-boundary-and-deterministic-verification-harness-roadmap-2026-03-20-0605]], [[phase-2-2-3-ci-golden-registry-and-boundary-regression-gates-roadmap-2026-03-21-1205]] |
| “Quality ↔ playability, manifests, denial reasons” as PCG analogy | **Hypothesis** | External PCG axes mapped to project vocabulary; **verify:** add one-line footnote in Phase 2.3 spec when metrics EMG-* are frozen |
| Roguelike harness / ECS ordering | **Hypothesis** | Pattern only; **verify:** optional cross-read with repo stage graph implementation when Phase 2.3 deepens |

---

## External source traceability

| URL | raw_capture | Note |
|-----|-------------|------|
| https://arxiv.org/abs/2503.21474 | [[Ingest/Agent-Research/Raw/phase-2-3-world-emergence-raw-2026-03-21-2230]] | HTML mirror `arxiv.org/html/2503.21474v2` indexed same raw file |
| https://blog.aqd.is/2021/07/liar-pbt | same | Stateful PBT |
| https://bfnightly.bracketproductions.com/rustbook/chapter_24.html | **synthesis-only** | Search hit; not duplicated in Raw this run — pattern reference only |
| https://www.gamedeveloper.com/programming/developing-your-own-replay-system | [[Ingest/Agent-Research/Raw/phase-2-2-intent-parser-procedural-hooks-determinism-integration-research-2026-03-20-0233]] | Vault-first |
| https://isaac-sim.github.io/IsaacLab/main/source/features/reproducibility.html | [[Ingest/Agent-Research/Raw/phase-2-2-intent-parser-procedural-hooks-determinism-integration-research-2026-03-20-0233]] | Vault-first |
| https://ojs.aaai.org/index.php/AIIDE/article/view/12477/12336 | **synthesis-only** | Emergence framing; abstract-level only |
| https://arxiv.org/abs/2203.01075 | **synthesis-only** | Minimal traces analogy |
| https://hypothesis.readthedocs.io/en/latest/tutorial/replaying-failures.html | [[Ingest/Agent-Research/Raw/phase-2-2-intent-parser-procedural-hooks-determinism-integration-research-2026-03-20-0233]] | Vault-first |
| https://arxiv.org/abs/2405.13042 | **synthesis-only** | Narrative co-author analogy; not normative for core |
| https://arxiv.org/abs/2603.02366 | **synthesis-only** | Same |

---

## Phase 2.3 task decomposition (backlog)

1. **Bind EMG-1..3** to concrete field paths in `roadmap-state` / phase contracts — **done when** each metric names a wiki-linked pseudo-code row or table cell.
2. **Seed matrix column** “expected_emergence_band” — **done when** one example row appears in a Phase 2.3 note with seed + fixture id + EMG thresholds.
3. **PBT command alphabet** (author tick vs sim tick) — **done when** listed as finite set in spec; **acceptance:** property template sentence for one invariant.
4. **Float / GPU fence** — **done when** policy states hash-excluded vs epsilon tier per [[Ingest/Agent-Research/Raw/phase-2-2-intent-parser-procedural-hooks-determinism-integration-research-raw-2026-03-20-0233]] Isaac warning.

---

## 1. Procedural generation: benchmarks, seeds, and “golden” artifacts

The **Procedural Content Generation Benchmark (PCG Benchmark)** is an open framework (Gym-like API) with **12 game-related generative problems**, each with its own content representation and scoring on **quality**, **diversity**, and **controllability** — useful as an external analogue for thinking about **seeded regressions** on generators rather than only on replay logs.

[Source: The Procedural Content Generation Benchmark (FDG ’25)](https://arxiv.org/abs/2503.21474)

**Pattern mapping (PCG → project vocabulary — not a repo assertion):**

- **Quality** ↔ playability / structural constraints (analogue to manifest + denial closure).
- **Diversity** ↔ multiple fixed seeds in a registry so outputs are not trivially identical.
- **Controllability** ↔ designer-facing knobs as stable inputs to replay runs.

Roguelike / ECS tutorials often isolate map generation in a **test harness** so the same API drives **runtime** and **headless tests**; hierarchical or path-based RNG is analogous to **stream isolation** described in [[phase-2-1-2-intent-stream-and-hierarchical-rng-ordering-roadmap-2026-03-19-1935]].

[Source: Map Building Test Harness — Roguelike Tutorial (Rust)](https://bfnightly.bracketproductions.com/rustbook/chapter_24.html)

---

## 2. Deterministic simulation, replay, and “emergence validation”

**Deterministic replay** for games is classically **input + initial conditions → identical state trace**, not full-state snapshots every tick; non-deterministic subsystems must be fenced so they cannot affect the hashed core.

[Source: Developing Your Own Replay System (Game Developer)](https://www.gamedeveloper.com/programming/developing-your-own-replay-system)

**Isaac Lab** (vault raw) stresses **global seed configuration** and warns that **GPU scheduling** and **runtime parameter changes** can introduce **small float drift** over long horizons.

[Source: Reproducibility and Determinism — Isaac Lab](https://isaac-sim.github.io/IsaacLab/main/source/features/reproducibility.html)  
*(Vault-first: [[Ingest/Agent-Research/Raw/phase-2-2-intent-parser-procedural-hooks-determinism-integration-research-raw-2026-03-20-0233]].)*

**Emergence in games** is often studied by **simulating mechanics** and measuring macro-level outcomes. For this project, “emergence validation” means **documented invariants**: given **seed S** and **intent stream I**, **EMG-*** metrics stay within envelopes and match **golden** derived state where specified.

[Source: Simulating Mechanics to Study Emergence in Games (AIIDE)](https://ojs.aaai.org/index.php/AIIDE/article/view/12477/12336)

**RL validation** literature uses **compressed traces** to re-simulate results — analogous to shipping **short seed + intent ledger** instead of huge blobs.

[Source: Reliable validation of Reinforcement Learning Benchmarks (arXiv:2203.01075)](https://arxiv.org/abs/2203.01075)

---

## 3. Property-based testing & co-authored narrative / state

**Stateful property-based testing (PBT)** generates **sequences of commands** against an **abstract state machine** and compares the model to the system under test — a strong pattern for **co-authored world state** where **human/author intents** and **simulation rules** interleave.

[Source: Stateful Property-Based Testing in Action (LIAR / EVE prototype)](https://blog.aqd.is/2021/07/liar-pbt)

**Hypothesis**-style replay of failures (vault raw): persist **minimal failing cases** as goldens for CI.

[Source: Hypothesis — Replaying failures](https://hypothesis.readthedocs.io/en/latest/tutorial/replaying-failures.html)  
*(Vault-first: [[Ingest/Agent-Research/Raw/phase-2-2-intent-parser-procedural-hooks-determinism-integration-research-raw-2026-03-20-0233]].)*

**Narrative co-authoring** research (StoryVerse, PlayWrite) is cited as **analogy** for layering authorial intent on **IntentPlan**; **not** normative for the deterministic core unless explicitly adopted.

[Source: StoryVerse — Co-authoring Dynamic Plot (arXiv:2405.13042)](https://arxiv.org/abs/2405.13042)  
[Source: PlayWrite — Narrative Co-Authoring Through Play in XR (arXiv:2603.02366)](https://arxiv.org/abs/2603.02366)

---

## 4. Concrete design hooks (for Phase 2.3 roadmap text)

> [!warning] Superseded for execution detail
> Use **Phase 2.3 emergence metrics**, **Genesis coupling**, **External source traceability**, and **Phase 2.3 task decomposition** above as the authoritative checklist. The table below remains a quick mnemonic only.

| Hook | Idea |
|------|------|
| **Emergence contract** | See **EMG-*** metrics. |
| **Seed matrix** | Pair **base seed** × **intent fixture** × **lore profile**; add **expected_emergence_band** when EMG thresholds are fixed. |
| **PBT / command model** | Author + sim command alphabet; properties per backlog §3. |
| **Fence drift** | Hash-exclude or epsilon tier for float/GPU-soft paths. |

---

## Raw sources (vault)

- [[Ingest/Agent-Research/Raw/phase-2-2-intent-parser-procedural-hooks-determinism-integration-research-raw-2026-03-20-0233]] — Isaac Lab, Game Developer replay, Hypothesis (reused).
- [[Ingest/Agent-Research/Raw/phase-2-3-world-emergence-raw-2026-03-21-2230]] — PCG Benchmark HTML, LIAR blog (this run).

---

## Sources

Canonical list matches **External source traceability** (synthesis-only URLs are labeled there).

- [Source: PCG Benchmark paper (arXiv:2503.21474)](https://arxiv.org/abs/2503.21474)
- [Source: Roguelike map test harness (Rust book)](https://bfnightly.bracketproductions.com/rustbook/chapter_24.html)
- [Source: Game Developer — replay system](https://www.gamedeveloper.com/programming/developing-your-own-replay-system)
- [Source: Isaac Lab — reproducibility](https://isaac-sim.github.io/IsaacLab/main/source/features/reproducibility.html)
- [Source: AIIDE — emergence in games](https://ojs.aaai.org/index.php/AIIDE/article/view/12477/12336)
- [Source: RL benchmark validation (arXiv:2203.01075)](https://arxiv.org/abs/2203.01075)
- [Source: Stateful PBT — LIAR blog](https://blog.aqd.is/2021/07/liar-pbt)
- [Source: StoryVerse (arXiv:2405.13042)](https://arxiv.org/abs/2405.13042)
- [Source: PlayWrite (arXiv:2603.02366)](https://arxiv.org/abs/2603.02366)
- [Source: Hypothesis replay](https://hypothesis.readthedocs.io/en/latest/tutorial/replaying-failures.html)
