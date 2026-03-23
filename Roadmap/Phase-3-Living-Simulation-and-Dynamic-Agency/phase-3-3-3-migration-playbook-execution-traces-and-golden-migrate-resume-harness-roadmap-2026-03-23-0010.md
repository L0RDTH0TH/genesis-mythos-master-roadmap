---
title: Phase 3.3.3 — Migration playbook execution traces + golden migrate-and-resume harness
roadmap-level: tertiary
phase-number: 3
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-23
tags: [roadmap, genesis-mythos-master, phase, persistence, migration, golden, harness]
para-type: Project
subphase-index: "3.3.3"
blocked_on_decisions:
  - D-032
  - D-043
  - D-047
  - D-048
handoff_readiness: 88
handoff_readiness_scope: "Normative draft for migration_id registry rows, append-only execution traces, and golden migrate-and-resume loop (matrix → migrate → re-matrix → dual-hash); literal fixtures + CI rows remain vault-TBD until D-032/D-043/D-047"
execution_handoff_readiness: 54
handoff_gaps:
  - "`fixtures/migrate_resume/**` checked-in tree + normalizer for volatile fields — TBD (pairs D-048 / repo policy)"
  - "Negative fixture IDs: draft **G-NEG-*** → vault binding table in-note; literal repo rows + reason_code tables still **TBD** at implementation freeze (**D-032** / **D-043**)"
links:
  - "[[phase-3-3-2-persistence-bundle-versioning-and-compatibility-matrix-roadmap-2026-03-22-2355]]"
  - "[[phase-3-3-1-authoritative-resume-checkpoint-and-session-boundary-roadmap-2026-03-22-2340]]"
  - "[[phase-3-3-persistence-cross-session-consequence-propagation-roadmap-2026-03-21-2348]]"
  - "[[decisions-log]]"
  - "[[distilled-core]]"
---

## Phase 3.3.3 — Migration playbook execution traces + golden migrate-and-resume harness

**TL;DR:** Operationalize **3.3.2** Appendix B with an auditable **`migration_id` registry**, **append-only execution traces** (hash-linked, topologically valid), and a **golden harness** that exercises **preflight step 2 → migrate (when MIGRATE_REQUIRED) → re-run matrix on post-migration bundle → preflight step 3 dual-hash**, plus explicit **negative** cases for **INCOMPATIBLE**, regen-lane rejection, and trace mismatch.

### `MigrationRegistry_v0` row shape (draft)

Machine index over transforms permitted on **`PersistenceBundle_vN`** (columns align with synthesis; bind literals at repo freeze — **Tier A** = vault only):

| Field | Role |
|-------|------|
| `migration_id` | Stable primary key (e.g. `pbundle_3_3_2__v2_to_v3__202603`) |
| `from_bundle_schema_version` / `to_bundle_schema_version` | Step bounds |
| `replay_row_version_range` | Optional gate on **3.1.1** wire |
| `serialization_profile_id` | Profile under which row was validated (**D-037**) |
| `ordered_step_index` | Global order in composite chain |
| `transform_kind` | `tolerant_read` \| `upcast` \| `snapshot_rewrite` \| `noop_eligible` |
| `preconditions` / `postconditions` | Structured predicates + hash invariants |
| `audit_log_template` | Fields appended per trace line |

### Execution trace (append-only)

Minimum element per completed step:

```text
TraceRecord_v0 {
  migration_id
  ordered_step_index
  input_bundle_hash
  output_bundle_hash
  logical_seq            // monotonic session/tick seq — ignore wall clock for replay
  matrix_outcome_at_entry // COMPAT_OK | MIGRATE_REQUIRED | INCOMPATIBLE (names per 3.3.2)
  resume_preflight_step   // 2 | 3 | post_migrate_rematrix
}
```

**Rules:** topological order must match registry edges; **idempotent replay** — re-applying a step when bundle already at `to_*` is a **ledger-hit** (no hash change), analogous to **2.1.5** spawn idempotency spirit.

### Golden migrate-and-resume harness (sketch)

1. Load frozen `bundle_in.json` (stub until D-032/D-043/D-047).
2. Run **CompatibilityMatrix_v0** (preflight **step 2**).
3. If **MIGRATE_REQUIRED**, run ordered **`migration_id`** chain; write **expected_trace.jsonl** golden.
4. **Re-run matrix** on **post-migration** bundle; expect **COMPAT_OK** (or documented intermediate state for multi-hop chains).
5. Run **dual-hash preflight (step 3)** per **3.3.1**; assert alignment with **1.1.4** / **1.1.5** lineage semantics.
6. **Normalize** volatile fields before compare (same discipline as **2.2.3** golden registry).

**Negative families (parametrize):** **INCOMPATIBLE** (no migrate), registry/matrix mismatch, **3.2.x** regen lane not closed, missing or out-of-order trace → **fail-closed** paths.

### Negative case ID binding (draft — D-049)

Maps harness **G-NEG-*** IDs to vault reason surfaces (no new codes; literals bind at repo freeze):

| Harness ID | Binds to (vault) | Notes |
|------------|------------------|--------|
| **G-NEG-INCOMPAT** | [[phase-3-3-2-persistence-bundle-versioning-and-compatibility-matrix-roadmap-2026-03-22-2355]] — matrix **INCOMPATIBLE** branch + fail-closed migrate refusal | No ordered steps run; trace may record single **matrix_outcome_at_entry** only |
| **G-NEG-REGEN** | [[phase-3-2-3-regen-ledger-replay-rows-and-tick-commit-coupling-roadmap-2026-03-22-1748]] + [[phase-3-3-2-persistence-bundle-versioning-and-compatibility-matrix-roadmap-2026-03-22-2355]] — regen-lane dual check | Migrate blocked until regen ledger closure per **3.2.x** |
| **G-NEG-TRACE** | [[phase-3-3-1-authoritative-resume-checkpoint-and-session-boundary-roadmap-2026-03-22-2340]] — resume preflight / ordering violations | Out-of-order `ordered_step_index` or hash mismatch vs registry |

### Interface table

| Partner | Contract |
|---------|----------|
| **3.3.2** | Supplies matrix outcomes + playbook branches; registry rows must not contradict matrix semantics |
| **3.3.1** | Preflight steps 2–3 + resume reason codes |
| **3.2.x** | Regen lane dual-check before treating migrate as safe |
| **2.2.3** | Golden refresh policy + volatile-field normalization |

### Tasks

- [x] Vault table stub for **`migration_id`** rows (markdown) → mirror to repo JSON/JSONL when **D-027** stack chosen — **done in-note** (`MigrationRegistry_v0` table above); repo mirror **DEFERRED** (**D-032** / **D-027**)
- [ ] Define **fixture case IDs** for positive + negative harness rows (link to **3.3.1** / **3.3.2** code tables by name, not invented literals)
- [ ] Document **trace hash linkage** (optional Merkle chunking) for large migrations — defer if YAGNI
- [ ] Golden: **migrate vN→vN+k + resume + M ticks** — blocked **D-032** / **D-043** / **D-047** / **D-048**

### Fixture case IDs (vault stub — D-049)

| Case ID | Class | Wikilink anchor |
|---------|--------|-----------------|
| **G-POS-MIGRATE-001** | Positive migrate + rematrix + dual-hash | § Golden migrate-and-resume harness |
| **G-NEG-INCOMPAT** | Matrix **INCOMPATIBLE** — no steps | § Negative case ID binding; [[phase-3-3-2-persistence-bundle-versioning-and-compatibility-matrix-roadmap-2026-03-22-2355]] |
| **G-NEG-REGEN** | Regen lane not closed | § Negative case ID binding; [[phase-3-2-3-regen-ledger-replay-rows-and-tick-commit-coupling-roadmap-2026-03-22-1748]] |
| **G-NEG-TRACE** | Trace order / hash vs registry | § Negative case ID binding; [[phase-3-3-1-authoritative-resume-checkpoint-and-session-boundary-roadmap-2026-03-22-2340]] |

### DEFERRED tasks ledger (open work)

| Task (unchecked above) | Blocked by | Decision |
|------------------------|------------|----------|
| Fixture case ID literals in repo + reason table rows | **D-032**, **D-043**, **D-047** | **D-049** |
| Trace hash linkage / Merkle (optional) | Operator YAGNI + repo | **D-049** |
| Golden migrate vN→vN+k + resume + M ticks | **D-032**, **D-043**, **D-047**, **D-048** | **D-049** |

## Research integration

**Synthesis:** [[Ingest/Agent-Research/phase-3-3-3-migration-playbook-golden-harness-research-2026-03-22-0815.md]]

**Key takeaways**

- Registry rows are the auditable index; **protobuf** or external docs are **Tier C** analogy only — do not import foreign column defs as normative.
- Golden harness **must** re-run matrix after migrate before claiming **COMPAT_OK** on live path.
- Explicit **goldenfile** / snapshot-update policy (**Tier B** refs in synthesis) forces intentional drift acceptance in CI.

**Nested research_synthesis validation:** first `.technical/Validator/research-synthesis-genesis-mythos-master-20260322T081500Z.md` → IRA → compare-final `.technical/Validator/research-synthesis-genesis-mythos-master-20260322T081500Z-final.md` (**medium** / **needs_work** — residual anchor/traceability until this note existed; **cleared** by creation of **3.3.3**).
