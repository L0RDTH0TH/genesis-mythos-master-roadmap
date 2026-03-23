---
title: Phase 3.3.2 — Persistence bundle versioning + compatibility matrix + migrations
roadmap-level: tertiary
phase-number: 3
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-22
tags: [roadmap, genesis-mythos-master, phase, persistence, bundle, migration, replay]
para-type: Project
subphase-index: "3.3.2"
blocked_on_decisions:
  - D-032
  - D-043
  - D-047
handoff_readiness: 89
handoff_readiness_scope: "Normative draft for PersistenceBundle envelope + CompatibilityMatrix_v0 outcomes; literal JSON matrix row + golden migration vectors still vault-TBD until D-032/D-043/D-047"
execution_handoff_readiness: 56
handoff_gaps:
  - "`CompatibilityMatrix_v0` checked-in row + CI eval hook — TBD (pairs D-048 adoption)"
  - "Ordered migration playbook execution traces (upcast chain IDs) — TBD until replay_row_version freeze"
links:
  - "[[phase-3-3-1-authoritative-resume-checkpoint-and-session-boundary-roadmap-2026-03-22-2340]]"
  - "[[phase-3-3-persistence-cross-session-consequence-propagation-roadmap-2026-03-21-2348]]"
  - "[[phase-1-1-4-state-snapshot-lineage-and-authoritative-rollback-ledger-roadmap-2026-03-19-1201]]"
  - "[[phase-1-1-5-idempotent-state-rehydration-contract-and-cold-start-consistency-roadmap-2026-03-19-1208]]"
  - "[[phase-3-1-1-deterministic-tick-epoch-and-hash-preimage-boundaries-roadmap-2026-03-22-0015]]"
  - "[[decisions-log]]"
  - "[[distilled-core]]"
---

## Phase 3.3.2 — Persistence bundle versioning + compatibility matrix + migrations

**TL;DR:** Operationalize **3.3.1** resume **preflight step 2** with a sparse **`CompatibilityMatrix_v0`** over **`PersistenceBundle_vN`** assertions; define **versioned migration** branches (tolerant reader → upcast chain → snapshot rewrite) without silent upcast of **hashed observables**.

### `PersistenceBundle_vN` (envelope, draft)

Single persisted document CI + clients agree on **before** live mutation:

| Field cluster | Role |
|---------------|------|
| Identity | `stream_id` (per **D-047**), `bundle_schema_version` |
| Lineage / tick | `snapshot_lineage_head_id`, `last_committed_tick_epoch`, optional `ledger_tail_ref` |
| Replay / wire | `replay_row_version`, `serialization_profile_id` (**3.1.6** / **D-037**) |
| Safety | `barrier_publish_ref` (**2.1.3**), `rng_namespace_map_version`, `build_id` slice (**D-027**) |

**Wire discipline:** If protobuf (or tag-based) storage is used: never reuse field tags; reserve deleted tags — persisted bundles obey same rules as RPC (Tier A).

### Compatibility matrix (preflight step 2)

**Row keys (consumer):** e.g. `engine_replay_capability.max_replay_row_version`, `serialization_profile_support`, `regen_lane_must_be_closed` (**3.2.x**).

**Column assertions (artifact):** `bundle_schema_version` range, `replay_row_version` migratable or in-range, `serialization_profile_id` frozen match, dual-hash families consistent with profile (**1.1.4** spirit).

**Outcomes:**

| Result | Next |
|--------|------|
| **COMPAT_OK** | Proceed to dual-hash preflight (**3.3.1** step 3). |
| **MIGRATE_REQUIRED** | Run **Appendix B** playbook; re-evaluate matrix; no live hash until pass. |
| **INCOMPATIBLE** | Fail closed (`RESUME_PROFILE_MISMATCH`, `RESUME_TICK_CURSOR_GAP`, etc. — reconcile with **3.3.1** draft codes). |

**Harness parametrization (3.3.3 / D-049):** Golden negative **G-NEG-INCOMPAT** parametrizes this **INCOMPATIBLE** branch (no ordered `migration_id` steps); trace records **matrix_outcome_at_entry** only — see [[phase-3-3-3-migration-playbook-execution-traces-and-golden-migrate-resume-harness-roadmap-2026-03-23-0010]] § Negative case ID binding.

**Regen lane:** Matrix must assert regen closure; **also** enforce **3.2.x** ordering gates (**dual check** per synthesis).

### Algorithm sketch — migration playbook (ordered)

1. **Detect** `bundle_schema_version` + `replay_row_version` + profile from bundle + checkpoint tail.
2. **Classify** matrix outcome; if **INCOMPATIBLE**, stop (no partial apply).
3. **Branch:**
   - **Tolerant reader:** forward-only fields; unknown fields ignored only when explicitly allowed in profile doc.
   - **Upcast chain:** ordered transforms `vK → vK+1` with logged `migration_id` + new bundle hash.
   - **Snapshot rewrite:** baseline + tail materialized to new lineage node (**1.1.4**) when upcast unsafe.
4. **Verify** dual-hash + tick cursor alignment post-migration.
5. **Bump** only via documented migration notes + version fields (no silent bump).

### Interface table

| Partner | Contract |
|---------|----------|
| **3.3.1** | `ResumeCheckpoint_v0` references bundle slice; preflight step 2 calls matrix. |
| **1.1.4 / 1.1.5** | Lineage + rehydrate after migration completes. |
| **3.1.1** | `TickCommitRecord_v0` + `replay_row_version` routing for tail replay. |
| **3.2.x** | Regen lane boolean + pipeline ordering (not only matrix text). |

### Tasks

- [ ] Check in **stub** `CompatibilityMatrix_v0` JSON (Appendix A of synthesis) under repo policy when stack chosen (**D-027**).
- [ ] Reconcile fail-closed **reason_code** strings with **3.3.1** table + **2.2.x** regen codes.
- [ ] Define **`migration_id`** registry row shape (vault table) before first implementation PR.
- [ ] Golden: “migrate bundle vN→vN+1 + resume + N ticks” — **blocked** **D-032** / **D-043** / checkpoint literal row (**D-047**).

## Research integration

### Key takeaways

- Version **`PersistenceBundle_vN`** as the envelope pinning `replay_row_version`, `serialization_profile_id`, lineage head, last committed tick, and barrier ref before mutating hashed observables.
- Resume **preflight step 2** evaluates **`CompatibilityMatrix_v0`** with outcomes **COMPAT_OK / MIGRATE_REQUIRED / INCOMPATIBLE**.
- Use **Tier A/B/C** source labeling in synthesis; protobuf tag hygiene is **Tier A**.
- **Appendix B** migration playbook: detect → classify → branch (tolerant reader / upcast / snapshot rewrite) → dual-hash verify → bump ids only via documented migration.
- **D-032 / D-043** still gate literal **golden replay rows**; matrix + playbook prose can land before goldens.

### Decisions / constraints

- **Constraint:** No silent upcast of hashed observables — mismatches fail closed per **3.3.1**.
- **Constraint:** Do not use protobuf cross-build serialization stability as hash input — bind **`serialization_profile_id`**.
- **Adopted:** **D-048** (2026-03-22) in [[decisions-log]] records the normative draft for **`PersistenceBundle_vN`**, **`CompatibilityMatrix_v0`**, and the ordered migration playbook. Optional: merge additional synthesis **§6** hypothesis blocks into the **D-048** row when the operator signs stack-specific defaults.

### Links

- [[Ingest/Agent-Research/phase-3-3-2-persistence-bundle-versioning-research-2026-03-22.md]]
- [[Ingest/Agent-Research/phase-3-3-1-sim-persistence-cross-session-research-2026-03-22-1830.md]]

### Sources

- See synthesis note **## Sources** (Tier A/B/C list).
