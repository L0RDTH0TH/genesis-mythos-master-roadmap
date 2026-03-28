---
title: Hostile research synthesis validation — genesis-mythos-master
created: 2026-03-18
tags: [validator, research_synthesis, genesis-mythos-master, determinism, provenance, simulation-boundary]
validation_type: research_synthesis
project_id: genesis-mythos-master
input_notes:
  - Ingest/Agent-Research/phase-1-core-architecture-research-2026-03-18-1125.md
queue_entry_id: resume-roadmap-genesis-mythos-master-2026-03-18-113537-next
parent_run_id: "44f1e39519"
timestamp: 2026-03-18T19:56:54.440Z
---

## Verdict

| field | value |
|---|---|
| severity | medium |
| recommended_action | needs_work |
| status | #review-needed |

## One-paragraph summary
The synthesis note is coherent on the simulation boundary split (world-state vs simulation vs rendering vs input) and it proposes a provenance record shape aligned with the “software / parameters / environment” contract, including guidance to store a seed in `parameters`. However, it does not explicitly carry several deterministic replay / simulation invariants that the genesis-mythos Phase-1 research corpus treats as safety-critical (tick/system update ordering, explicit “no non-determinism in simulation” constraints like unseeded RNG / float/time/GPU scheduling effects, and a concrete dry-run replay comparison procedure). Provenance guidance is also underspecified for traceability completeness (e.g., no explicit `random_seed` vs `stage_seed` mapping example, and it omits the “CLI args as array” detail).

## Contract checks (hostile)

### 1) Determinism contract
Findings:
1. **Seed recording is mentioned**, but the note frames determinism as “provenance reproducibility” rather than as an explicit simulation constraint set (no unseeded RNG; no platform-dependent float/time behavior; fixed system order / tick boundary). This leaves room for downstream implementers to miss the critical determinism failure modes highlighted in `world-state-serialization-deterministic-replay-2026-03-15-1240.md`.
2. **Replay validation procedure is missing**: no instruction to run identical seed + identical input history and compare hashes/checksums as a determinism test, even though other Phase-1 research notes call this out as “standard determinism test”.
Reason this matters:
Determinism safety is not only about recording seeds; it also requires forbidding or controlling the common non-determinism sources during the simulation step.

### 2) Provenance / traceability contract
Findings:
1. The note correctly proposes the required provenance blocks (`software`, `parameters`, `environment`) and names `schema_version` / `software` shape / environment capture at a high level.
2. It explicitly mentions “Record random_seed even if auto-generated” and “CLI args as array”, but the **integration section** that defines the minimal stage JSON record does not concretely include `args` nor does it clearly map `random_seed` to `global_seed` and/or `stage_seed` in the minimal record.
Reason this matters:
If implementers copy the “minimal provenance record” template, they may omit the exact fields that the determinism replay and audit tooling expects.

### 3) Simulation boundary contract
Findings:
1. The boundary diagram bullets match the intended split: simulation reads world-state and produces deltas/events; rendering consumes a read-only projection; input produces intents/commands and does not mutate world-state directly.
2. Missing linkage: it does not explicitly mention the tick/event boundary contract (discrete steps; fixed timestep; “no render in simulation” as an enforced invariant) even though Phase-1 research treats this as a core determinism constraint.

## Reason codes
- missing_determinism_non_determinism_controls
- missing_tick_event_boundary_constraints
- missing_dry_run_replay_comparison_procedure
- provenance_integration_template_incomplete(random_seed_mapping_and_args)
- evidence_gap(determinism_sources_not_linked_in_synthesis_note)

## Recommended next artifacts (checklist)
1. Add a short section “Deterministic replay invariants” that explicitly lists the non-determinism sources to ban/control (unseeded RNG, platform-dependent float/time behavior, nondeterministic system scheduling), referencing the existing Phase-1 research note `world-state-serialization-deterministic-replay-2026-03-15-1240.md`.
2. Add a concrete “Replay test (dry-run)” procedure: same build + same seeds + same input/event log -> serialize/hashes -> compare checksums, and what gets recorded for provenance.
3. Update the “Minimal provenance record per stage” template to include (or explicitly map) `random_seed` and `args` (when applicable), or add a one-line statement explaining why `random_seed` is represented as `global_seed` / `stage_seed` in this project.
4. Extend the Sources list with at least one determinism/replay-specific reference source (not just ECS/provenance), so the note’s claims are defensible from citations alone.

