---
title: Phase 2.3 — Validate co-authored world emergence (test seeds)
roadmap-level: secondary
phase-number: 2
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-21
tags: [roadmap, genesis-mythos-master, phase, world-emergence, test-seeds]
para-type: Project
subphase-index: "2.3"
handoff_readiness: 82
handoff_gaps:
  - "EMG-1..3 field bindings to normative schema (TBD until 2.3.x tertiaries freeze paths)"
links:
  - "[[phase-2-procedural-generation-and-world-building-roadmap-2026-03-19-1101]]"
  - "[[phase-2-2-4-phase-2-2-secondary-closure-rollup-and-advance-readiness-roadmap-2026-03-21-2000]]"
  - "[[distilled-core]]"
---

## Phase 2.3 — Validate co-authored world emergence through test seeds

Close the loop from **frozen intent + replay harness** (Phase 2.2) to **observable world outcomes**: given deterministic seeds and authored intent/command streams, prove that **emergent simulation state** and **authoritative lore constraints** stay aligned within measurable bands — without relaxing fail-closed semantics.

### Objectives

- Define **emergence metrics (EMG-1..3)** as extensions of `ReplayAndVerify` / golden registry — not a parallel harness family.
- Specify a **seed matrix**: `(seed_envelope, fixture_id, tick_horizon)` rows with expected **emergence bands** (hashes, scores, denial closure).
- Document **float / GPU fence** policy for any non-bit-exact path before hashing derived emergence state.
- Keep **denial taxonomy** from [[phase-2-2-1-intent-canonicalization-and-denial-taxonomy-roadmap-2026-03-20-0901]] as the allow-list for unexpected denial codes on the emergence path.

### Non-goals (this secondary)

- Land VCS JSON fixtures + CI workflow (tracked as implementation debt elsewhere).
- Replace Phase 2.2 **G-P2.2-\*** closure — this slice **builds on** it.

### Contract sketch (v0)

- **EMG-1 `replay_emergence_hash`:** Derived hash after tick **N** from stable ledger fields (bind to schema in 2.3.1+).
- **EMG-2 `lore_sim_alignment_score`:** Int **0..100** comparing authoritative lore flags vs sim counters (floor **F** TBD).
- **EMG-3 `denial_invariant_closed`:** Count of unexpected open denials vs frozen taxonomy — **Pass** = zero unexpected.

### Tasks

- [x] Bind each **EMG-\*** to a wiki-linked pseudo-code row or table cell in a tertiary note — see [[phase-2-3-1-emg-normative-schema-bindings-and-seed-matrix-v0-roadmap-2026-03-21-2205]] and [[#emg-binding-table-v0-stub]].
- [x] Add one **seed matrix** example row (seed + fixture + thresholds) in a tertiary — see [[phase-2-3-1-emg-normative-schema-bindings-and-seed-matrix-v0-roadmap-2026-03-21-2205]] (Seed matrix section).
- [x] List finite **PBT command alphabet** (author tick vs sim tick) for property templates — see [[phase-2-3-1-emg-normative-schema-bindings-and-seed-matrix-v0-roadmap-2026-03-21-2205]] (PBT alphabet section).

### EMG binding table (v0 stub)

> **Caption:** **TBD** cells mean **not frozen** in state/decisions until Phase 2.3.x promotion; draft bindings and pseudo-code live in [[phase-2-3-1-emg-normative-schema-bindings-and-seed-matrix-v0-roadmap-2026-03-21-2205]].

| Metric | Normative field / pseudo-code row (TBD) | Status |
| --- | --- | --- |
| EMG-1 `replay_emergence_hash` | Ledger paths after `SpawnCommit` + tick **N** (bind in 2.3.1+) | TBD |
| EMG-2 `lore_sim_alignment_score` | `authoritative_lore_flags` vs `sim_observed_counters` (bind in 2.3.1+); floor **F** TBD | TBD |
| EMG-3 `denial_invariant_closed` | Denial taxonomy allow-list vs emitted codes (reuse 2.2.1) | TBD |

## Research integration

### Key takeaways

- **PCG Benchmark** (quality / diversity / controllability) is a useful *external* framing for extending **golden** thinking from **intent replay** to **generator + emergence** scenarios — not a replacement for your harness IDs.
- **Deterministic replay** stays **input + initial conditions → trace**; fence **float/GPU-soft** paths or tier-compare them (see Isaac-style drift warnings in vault raw).
- **Stateful PBT** fits **author commands + sim ticks**; pair with **Hypothesis-style** minimal failing case capture for CI.
- **Emergence** here means **documented invariants** (EMG metrics), not novelty for its own sake.

### Decisions / constraints

- **Adopted pattern:** three placeholder metrics **EMG-1** (replay emergence hash), **EMG-2** (lore/sim alignment), **EMG-3** (denial-invariant closure) — must be bound to real schema fields in Phase 2.3 spec.
- **Constraint:** LLM narrative papers (StoryVerse, PlayWrite) are **analogy only** unless the project explicitly adds such components.
- **Pending:** Set numeric floors for EMG-2 and wire field paths when Phase 2.3 contracts are written.

### Links

- [[Ingest/Agent-Research/phase-2-3-validate-co-authored-world-emergence-research-2026-03-21-2230]]
- [[Ingest/Agent-Research/Raw/phase-2-3-world-emergence-raw-2026-03-21-2230]]

### Sources

- See `## Sources` in the synthesis note for the full URL list and the **External source traceability** table (raw vs synthesis-only).

## Tertiary notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building"
WHERE contains(subphase-index, "2.3.") AND roadmap-level = "tertiary"
SORT subphase-index ASC, file.name ASC
```
