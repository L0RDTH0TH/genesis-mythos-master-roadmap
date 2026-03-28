---
title: Research — Phase 3.3.3 migration playbook, migration_id registry, golden migrate-and-resume harness
research_query: "migration_id registry; ordered upcast chain traces; golden migrate-and-resume vs CompatibilityMatrix_v0 and resume preflight"
linked_phase: Phase-3-3-3-migration-playbook-execution-and-golden-harness
project_id: genesis-mythos-master
created: 2026-03-22
tags: [research, agent-research]
research_tools_used: [web_search, mcp_web_fetch]
agent-generated: true
research_escalations_used: 0
research_focus: junior_handoff
para-type: Resource
roadmap_anchor_pending: false
---

# Phase 3.3.3 — Migration playbook execution, registry shape, golden harness (external synthesis)

**Tier legend (throughout this note):** **Tier A** — vault-canonical / project roadmap or decisions text. **Tier B** — external evidence (docs, libraries). **Tier C** — analogy, orchestration guidance, or pending until roadmap/repo exists.

Synthesis for **next tertiary** after **3.3.2** (`PersistenceBundle_vN`, `CompatibilityMatrix_v0`, D-048). Goal: actionable patterns for **`migration_id` registry**, **ordered upcast-chain execution traces**, and a **golden migrate-and-resume** test harness that ties **matrix outcomes** to **resume preflight** (3.3.1).

**Tier A — Do-not-duplicate (vault):** 3.3.2 already defines COMPAT_OK / MIGRATE_REQUIRED / INCOMPATIBLE, tolerant reader → upcast → snapshot rewrite, dual-hash verify, and D-032/D-043/D-047 golden deferrals. This note adds **registry/trace/harness mechanics**, not a repeat of the playbook prose.

## 1. `migration_id` registry — recommended row shape (Tier A / Tier C)

**Tier A:** Row semantics must stay consistent with [[phase-3-3-2-persistence-bundle-versioning-and-compatibility-matrix-roadmap-2026-03-22-2355]] (matrix outcomes, playbook branches, no silent upcast of hashed observables).

Treat the registry as the **auditable index** of every transform that may run on a `PersistenceBundle_vN` (or checkpoint slice). Each row should be machine-actionable and stable across CI:

| Field | Purpose |
|--------|--------|
| `migration_id` | Stable string ID (e.g. `pbundle_3_3_2__v2_to_v3__2026_03`) — primary key. |
| `from_bundle_schema_version` / `to_bundle_schema_version` | Inclusive bounds for the step (or `from`/`to` pair). |
| `replay_row_version_range` | Optional — when migration is gated on replay wire version. |
| `serialization_profile_id` | Frozen profile the row was validated under (align D-037 / 3.1.6). |
| `ordered_step_index` | Integer position in the **global** ordered chain for this bundle lineage (not per-session ad hoc). |
| `transform_kind` | Enum: `tolerant_read` \| `upcast` \| `snapshot_rewrite` \| `noop_eligible` (mirror 3.3.2 branches). |
| `implementation_ref` | Repo pointer: crate/module + symbol or RFC section (for junior handoff). |
| `preconditions` | Structured predicates (e.g. matrix must have been `MIGRATE_REQUIRED` for column X). |
| `postconditions` | Hashes / invariants asserted after step (links to dual-hash preflight). |
| `audit_log_template` | Fields appended to execution trace (below). |

**Tier C:** Store as **versioned JSON** (or JSONL append-only) under repo policy when stack is chosen; the vault can mirror a **markdown table** for human review until the file lands in VCS.

**Tier C — illustrative analogy (non-normative):** Public protobuf migration/release notes discuss **breaking runtime and API changes** staged across library versions — useful as a **mental model** that wire and interpretation drift need explicit versioning, not as a definition of your `migration_id` columns. See [Migration Guide | Protocol Buffers Documentation](https://protobuf.dev/support/migration/). Do **not** treat that page as specifying `migration_id`, audit templates, or Genesis Mythos registry rows.

## 2. Ordered upcast chain — execution traces (Tier A / Tier C)

An **execution trace** is a append-only list of **completed** migration steps for one bundle instance:

- **Trace element (minimum):** `{ migration_id, ordered_step_index, input_bundle_hash, output_bundle_hash, wall_clock_ts_ignored?, logical_tick_or_seq, matrix_outcome_at_entry, resume_preflight_step }`
- **Ordering:** Steps must match the **topological order** implied by `from_*` → `to_*` edges in the registry; reject if a step’s `from` does not equal current bundle version after prior steps.
- **Idempotency:** Re-running the same `migration_id` on an already-at-`to` bundle should be a **ledger hit** (no hash change), analogous to spawn idempotency patterns in Phase 2.1.x distilled-core.

Log traces where operators can diff CI: same structure as **golden** vectors (below).

## 3. Golden migrate-and-resume harness (ties `CompatibilityMatrix_v0` to preflight) (Tier A / Tier B / Tier C)

**Objective:** One test (or parametrized family) that:

1. Loads a **frozen golden bundle** at version *N* (stub until D-032/D-043/D-047 allow literals).
2. Runs **matrix evaluation** (resume preflight **step 2** per [[phase-3-3-1-authoritative-resume-checkpoint-and-session-boundary-roadmap-2026-03-22-2340]] sketch) → expects `COMPAT_OK` \| `MIGRATE_REQUIRED` \| `INCOMPATIBLE` per fixture metadata — names per 3.3.2 outcome table, not invented enums.
3. On `MIGRATE_REQUIRED`, runs the **ordered chain** from the registry; records **execution trace**; asserts **post-bundle hash** matches golden *N+k*.
4. **Post-migration acceptance (not redundant with step 2):** After the bundle’s version/hash changed, **re-run matrix classification (preflight step 2 again)** on the migrated artifact, then **dual-hash verification (preflight step 3)** and any idempotency / rehydrate guards 3.3.1 ties to 1.1.4 / 1.1.5. Expect **pass** only when matrix + migration + preflight align.

**Fixture layout (suggested):**

- `fixtures/migrate_resume/<case_id>/bundle_in.json` — input bundle.
- `fixtures/migrate_resume/<case_id>/expected_matrix_outcome.json` — expected classification.
- `fixtures/migrate_resume/<case_id>/expected_trace.jsonl` — ordered `migration_id` list + hashes (normalized: strip volatile fields per golden rules).
- `fixtures/migrate_resume/<case_id>/bundle_out.json` — post-migration golden.

**Golden file mechanics (Tier B):** Use a library that **fails CI on drift** and requires an explicit env flag to refresh goldens.

[Source: goldenfile — Mint compares outputs to checked-in golden files; intentional updates via env flag](https://docs.rs/goldenfile/latest/goldenfile/)

[Source: Jest — Snapshot testing; updates require explicit `-u` / interactive consent](https://jestjs.io/docs/snapshot-testing)

**Normalization (Tier A):** Strip or canonicalize timestamps, UUIDs, and nondeterministic ordering before hash/compare — same discipline as Phase 2.2.3 golden registry notes.

### 3.1 Negative and regen-lane fixtures (required) (Tier A)

Parametrize at least these **failure / ordering** cases; expected codes must be reconciled with the **3.3.1** reason_code / preflight table and **3.3.2** matrix + regen-lane text (use those tables by name when implementing — do not mint new failure enums here):

| Case | Setup | Expected behavior |
|------|--------|-------------------|
| (a) | Matrix returns **INCOMPATIBLE** for fixture | **No** migration steps run; fail-closed; no partial apply. |
| (b) | Matrix says **MIGRATE_REQUIRED** but registry chain or preconditions disagree with matrix column | Abort migration with explicit mismatch code; no hash bump. |
| (c) | **Regen lane not closed** (3.2.x ordering / 3.3.2 dual check) | Matrix or preflight rejects before live hashed observables — align with 3.3.2 regen-lane bullets. |
| (d) | Post-migration bundle claims version without **trace tail** / trace inconsistent with claimed `to_*` | Same fail-closed family as §4 checklist (**INCOMPATIBLE** / mismatch codes per merged 3.3.1 table). |

## 4. Interface checklist (3.3.2 ↔ 3.3.1 ↔ CI) (Tier A)

- **Matrix stub row** in CI must reference **`migration_id`(s)** that are the only legal transforms for `MIGRATE_REQUIRED` for that column.
- **Resume preflight** should consume **last trace tail** (or bundle metadata embedding last `migration_id`) so “migrate then resume” is one story, not two silos.
- **Fail-closed:** If trace is missing for a bundle claiming post-migration version, preflight returns the same family as `INCOMPATIBLE` / mismatch codes (align with 3.3.1 reason_code table when merged).

## 5. Open decisions (explicit) (Tier C)

- JSON vs JSONL for registry (query: single-file version vs append-only audit).
- Whether `ordered_step_index` is global per `stream_id` family or per `bundle_schema_version` major — pick one and document.
- Where golden bundles live until D-047 pins literal checkpoint rows (vault-first stubs vs repo).

## 6. Hand-off traceability (Tier C)

**Anchored (2026-03-23):** Canonical tertiary [[phase-3-3-3-migration-playbook-execution-traces-and-golden-migrate-resume-harness-roadmap-2026-03-23-0010]] exists; `linked_phase` aligns with **3.3.3** deepen. Frontmatter **`roadmap_anchor_pending: false`**.

## Raw sources (vault)

- [[phase-3-3-2-persistence-bundle-versioning-and-compatibility-matrix-roadmap-2026-03-22-2355]]
- [[phase-3-3-1-authoritative-resume-checkpoint-and-session-boundary-roadmap-2026-03-22-2340]]
- [[distilled-core]]

## Sources

- [Migration Guide | Protocol Buffers Documentation](https://protobuf.dev/support/migration/)
- [Crate goldenfile — docs.rs](https://docs.rs/goldenfile/latest/goldenfile/)
- [Jest — Snapshot testing](https://jestjs.io/docs/snapshot-testing)

