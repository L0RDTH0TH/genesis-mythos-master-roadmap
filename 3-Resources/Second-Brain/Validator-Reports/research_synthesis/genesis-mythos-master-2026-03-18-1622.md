---
title: Hostile research synthesis validation — genesis-mythos-master
created: 2026-03-18
tags: [validator, research_synthesis, genesis-mythos-master, determinism, provenance, simulation-boundary]
validation_type: research_synthesis
project_id: genesis-mythos-master
input_notes:
  - 1-Projects/genesis-mythos-master/Roadmap/Phase-1-conceptual-foundation-and-core-architecture/Phase-1-1-core-abstractions-and-boundaries-Roadmap-2026-03-18-1125.md
  - Ingest/Agent-Research/phase-1-1-1-core-abstractions-boundaries-research-2026-03-18-1622.md
queue_entry_id: resume-roadmap-genesis-mythos-master-2026-03-18-195659-next
parent_run_id: "pr-resume-roadmap-genesis-mythos-master-20260318-162212"
timestamp: 2026-03-18T16:22:12-04:00
---

## Verdict

| field | value |
|---|---|
| severity | medium |
| recommended_action | needs_work |
| status | #review-needed |

## One-paragraph summary
The synthesis note is directionally consistent with Phase 1.1’s “hard seams” goals (boundary split, deterministic simulation framing, RNG discipline, and general replay/checkpoint practices) and it cites appropriate determinism and event-sourcing references. However, it remains underspecified for the safety-critical details Phase 1.1 expects handoff-ready implementation to enforce: an explicit tick/system update ordering + replay/dry-run comparison procedure, a concrete serialization/canonical-float policy, and a complete provenance record mapping (stage_seed/random_seed naming, dt/intents_hash, and required output hashes + diff pointers). As a result, downstream implementers are likely to miss determinism failure modes or produce provenance that is not auditably complete.

## Contract checks (hostile)

### 1) Determinism contract (what must be controlled, not just described)

Findings:
1. The note defines determinism and recommends checksums, but it does not include an explicit, step-by-step “seed + intent/event log -> canonical serialization -> checksum compare” dry-run replay procedure that matches the Phase-1.1 replay comparison requirement.
2. Non-determinism controls (floating-point env/platform differences, time/entropy, scheduling/data-race sources) are discussed at a high level, but the synthesis does not translate them into a concrete “ban/control list” aligned to the Phase-1.1 contract (what to prohibit inside `SimulationStep`, and what serialization policy must be fixed).

Why this matters:
Determinism safety here is not only about “record a seed”; it is about forbidding or controlling known sources of replay divergence and providing a verifiable harness.

### 2) Provenance / traceability contract (schema completeness and mapping fidelity)

Findings:
1. The note proposes provenance fields and emphasizes reproducibility controls, but it does not fully map Phase-1.1’s expected provenance schema elements into a minimal record template: `random_seed` vs `stage_seed` aliasing, `dt_ms`, `intents_hash`, `from_snapshot_id`, and required output hashes (e.g. `events_hash`) + diff pointers for traceability/audits.
2. The synthesis suggests “lock floating-point policy” but does not name or specify a concrete canonical float policy (e.g. quantize/round scheme) that the Phase-1.1 template explicitly requires under `serialization_boundary`.

Why this matters:
If the provenance record is incomplete or ambiguously mapped, later verification steps (replay comparison, diffs, audits) cannot be executed reliably.

### 3) Simulation boundary contract (ordering + isolation invariants)

Findings:
1. Boundary split guidance is consistent, but tick/event ordering and “fixed system_graph order / stable update order” requirements are only implied via “stable ordering keys,” not stated as explicit invariants (e.g. events ordered by monotonic `event_id` / stable indices).
2. Rendering/simulation isolation is mentioned generically (“no side effects”), but the synthesis does not reinforce the strict “no gameplay writes in rendering / no render/projection state writes in simulation” rule as testable constraints.

Why this matters:
Handoff implementability depends on invariants being explicit and directly testable.

## Reason codes
- missing_dry_run_replay_procedure
- missing_determinism_ban_control_list
- missing_canonical_float_policy_concrete
- provenance_schema_incomplete(random_seed_stage_seed_mapping_output_hashes_diff_pointers)
- missing_tick_system_update_order_constraints

## Recommended next artifacts (checklist)
1. Add a “Deterministic replay invariants” section that explicitly lists the determinism failure modes to ban/control (unseeded RNG, float env/time entropy, nondeterministic iteration/scheduler effects) and ties each to the Phase-1.1 contract.
2. Add a concrete dry-run replay procedure that mirrors Phase-1.1: same seeds + intent/event log + `from_snapshot_id` -> canonical serialization -> compute checksums/hashes -> compare and record the divergence/provenance record.
3. Update the “Minimal replay/provenance record per stage” template so it includes (or explicitly maps) Phase-1.1 required fields: `random_seed`/`stage_seed` alias, `dt_ms`, `intents_hash`, input/output snapshot identifiers, at minimum `events_hash` (and the checksum/hash it corresponds to), and diff-pointer fields (`from_snapshot_id`, `to_snapshot_id`, `delta_summary_hash?`).
4. Reinforce ordering invariants as explicit bullets (e.g. event order by monotonic `event_id` or stable index; fixed deterministic system update ordering) so implementers can make ordering enforceable in code.

