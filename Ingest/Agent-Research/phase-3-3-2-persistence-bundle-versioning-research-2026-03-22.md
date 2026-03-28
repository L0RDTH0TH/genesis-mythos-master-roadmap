---
title: "Research — Phase 3.3.2 persistence bundle schema evolution + compatibility matrix + migrations"
research_query: "PersistenceBundle schema evolution; resume preflight compatibility matrix; tolerant reader upcast snapshot rewrite deterministic replay"
linked_phase: "Phase-3-3-2-Persistence-Bundle-Versioning-and-Compatibility-Matrix"
project_id: genesis-mythos-master
created: 2026-03-22
tags: [research, agent-research, genesis-mythos-master, persistence, schema-evolution, replay]
agent-generated: true
research_tools_used: [web_search, mcp_web_fetch]
research_escalations_used: 0
research_step1b_note: "research_escalations_used counts Step 1b query-sanity revisions only; nested Validator→IRA→repair is recorded in ira_repair_applied + validator reports."
research_focus: junior_handoff
origin: roadmap-deepen
ira_repair_applied: 2026-03-22
note_research_readiness: "draft_with_working_hypotheses_post_nested_validator_ira"
raw_sources:
  - "[[1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/phase-3-3-1-authoritative-resume-checkpoint-and-session-boundary-roadmap-2026-03-22-2340]]"
  - "[[Ingest/Agent-Research/phase-3-3-1-sim-persistence-cross-session-research-2026-03-22-1830]]"
  - "[[Ingest/Agent-Research/tick-scoped-observable-bundle-after-mutation-apply-research-2026-03-22-2330]]"
---

# Phase 3.3.2 — Persistence bundle versioning, compatibility matrix, and migrations (synthesis)

**Scope:** Deepen **Phase 3.3.2** after **[[phase-3-3-1-authoritative-resume-checkpoint-and-session-boundary-roadmap-2026-03-22-2340]]** (`ResumeCheckpoint_v0` draft, session vs tick boundary, dual-hash preflight, `PersistenceBundle` / `replay_row_version` / `serialization_profile_id` stubs). This note adds **reference-grade patterns** (vendor / official docs) plus **working hypotheses** for **schema evolution**, a **compatibility matrix** usable at **resume preflight step 2**, and **versioned migration** (tolerant reader, upcast chain, snapshot rewrite) aligned with **deterministic replay** (**1.1.4–1.1.5**, **3.1.1** tick commits).

**Do not duplicate:** Literal `ResumeCheckpoint_v0` field table (still draft in 3.3.1), full `TickCommitRecord_v0` preimage list, or `SimObservableBundleTelemetry_v0` facet table — those remain authoritative in vault phase notes and **[[Ingest/Agent-Research/tick-scoped-observable-bundle-after-mutation-apply-research-2026-03-22-2330]]**.

**Evidence tiers (for juniors):** **Tier A** = official vendor / protocol docs (protobuf.dev, Axon reference). **Tier B** = operational product docs (EventSourcingDB). **Tier C** = independent blog / opinion — use for intuition only, never as sole authority.

---

## 1. `PersistenceBundle` as the versioned “envelope”

Treat **`PersistenceBundle_vN`** (name TBD) as the **single persisted document** that pins everything CI and clients must agree on before mutating hashed observables:

| Concern | Suggested bundle fields (research-level) | Why it matters |
|--------|-------------------------------------------|----------------|
| **Logical stream** | `stream_id`, `bundle_schema_version` | One authoritative head per stream (3.3.1). |
| **Lineage** | `snapshot_lineage_head_id` | Anchors 1.1.4 DAG node. |
| **Tick cursor** | `last_committed_tick_epoch`, optional `ledger_tail_ref` | Aligns 3.1.1 journal tail vs snapshot baseline. |
| **Replay / row format** | `replay_row_version` | Routes tick rows + golden vectors through the correct deserializer/upcaster chain. |
| **Serialization** | `serialization_profile_id` | Binds observable preimage / facet graph (**3.1.6**) to a frozen profile (**D-037** theme). |
| **Async safety** | `barrier_publish_ref` | Ensures no half-published preimage (2.1.3). |
| **RNG / build** | `rng_namespace_map_version`, `build_id` slice | Cold-start parity with D-027 (no wall-clock in preimage). |

**Wire-format discipline:** If you use **protobuf** (or similar tag-based encoding) for storage, treat **tag numbers** as the compatibility key: never reuse tags, reserve deleted tags, avoid type changes — the same rules that prevent silent binary misinterpretation apply to **persisted** bundles, not only RPC.

[Source (Tier A): Proto Best Practices — don’t re-use tag numbers; reserve deleted fields](https://protobuf.dev/best-practices/dos-donts/)

---

## 2. Compatibility matrix — resume preflight step 2

**Preflight step 2** in 3.3.1 is “verify **compatibility matrix** (row version, profile, player cardinality…).” Operationalize it as a **sparse decision table**: rows = **consumer capabilities**, columns = **artifact assertions**.

### 2.1 Row keys (examples)

- **`engine_replay_capability`**: max `replay_row_version` understood + registered upcasters.
- **`serialization_profile_support`**: set of allowed `serialization_profile_id` values (or hash of facet manifest).
- **`snapshot_schema_capability`**: max snapshot manifest schema / Merkle facet graph version.
- **`session_policy`**: player cardinality, shard policy, regen lane closure flags (**3.2.x**), if they affect preimage eligibility.

### 2.2 Column assertions (from bundle + checkpoint)

- **`bundle_schema_version`** ∈ supported range.
- **`replay_row_version`** ≤ `engine_replay_capability.max` **or** migratable via known upcast chain.
- **`serialization_profile_id`** matches frozen profile for this build (or explicit migration path).
- **`metadata_hash` / `state_hash`** families (1.1.4 spirit) — dual-hash gate remains **fail-closed** if profile or row version implies different preimage layout.

### 2.3 Outcomes

| Result | Behavior |
|--------|----------|
| **COMPAT_OK** | Proceed to dual-hash preflight (step 3). |
| **MIGRATE_REQUIRED** | Run **controlled migration** (Appendix B) before hashing / live apply. |
| **INCOMPATIBLE** | Fail closed with reason codes (e.g. `RESUME_PROFILE_MISMATCH`, `RESUME_TICK_CURSOR_GAP` — reconcile naming in decisions-log). |

### 2.4 Worked walk-through (illustrative IDs, non-normative)

**Consumer:** `engine_profile_id: "sim-ci-2026-03"` with `max_replay_row_version: 7`, `allowed_serialization_profile_ids: ["facet-manifest-v3"]`, `regen_lane_must_be_closed: true`.

**Bundle assertions from `ResumeCheckpoint_v0` + tail:** `replay_row_version: 7`, `serialization_profile_id: "facet-manifest-v3"`, `regen_lane_closed: true`, `bundle_schema_version: 2`.

**Evaluation:** All column predicates pass ⇒ **COMPAT_OK** → dual-hash preflight. If `replay_row_version` were `8` with no registered upcast to 7 ⇒ **INCOMPATIBLE** (or **MIGRATE_REQUIRED** if an offline migration tool exists).

[Source (Tier A): Event versioning — Axon Framework reference (version metadata + transformation concepts)](https://docs.axoniq.io/axon-framework-reference/5.0/events/event-versioning/)

[Source (Tier C, supplementary only): Schema evolution overview — tolerant reader vs upcasting](https://www.youngju.dev/blog/architecture/2026-03-07-architecture-event-sourcing-cqrs-production-patterns.en)

---

## 3. Deterministic replay linkage (1.1.4–1.1.5 + 3.1.1)

- **Replay order:** Baseline snapshot → ordered tick tail → **same** `replay_row_version` interpretation at every step. If a tick row deserializes under the wrong version, **hashes diverge** even when “mostly” right — treat as **hard failure** for CI.
- **Tolerant reader:** Safe only for **additive** changes (new optional fields). **Renames, removals, or type changes** require **upcasters** or **snapshot rewrite** (below).
- **Live vs replay:** Migration and upcast paths must be **pure** w.r.t. external side effects (already flagged in 3.3.1 research).

[Source (Tier B): Optimizing event replays — replay hygiene](https://docs.eventsourcingdb.io/best-practices/optimizing-event-replays/)

---

## 4. Migration strategies (choose explicitly per change type)

| Strategy | Mechanism | Determinism impact |
|----------|-----------|-------------------|
| **Tolerant reader** | Deserialize ignoring unknown fields; defaults for missing | OK for additive-only; **not** for renames/removals. |
| **Upcast on read** | Chain `vK → vK+1 → … → current` for tick rows / bundle fragments | Must be **total** for supported ranges; golden tests per version jump. |
| **Snapshot rewrite** | Offline or maintenance job writes new snapshot + bumps lineage | Must preserve **bijective** mapping vs replayed tail; record new `snapshot_lineage_head_id`. |
| **Parallel full rebuild** | Recompute state from genesis or last golden anchor | Expensive; use when Merkle facet graph changes invalidate old snapshots. |

**Protobuf-oriented rule of thumb:** prefer **new fields / reserved tags** over in-place mutation; never rely on **serialization stability across builds** for cache keys or hashes — align with explicit **`serialization_profile_id`** instead.

[Source (Tier A): Proto — never rely on serialization stability across builds](https://protobuf.dev/best-practices/dos-donts/)

---

## 5. Roadmap-owned follow-ups (after this synthesis)

The following remain **normative project work** in phase notes / CI, not fully closed by this research file:

1. **`PersistenceBundle_v0` → v1 diff policy** — table of allowed change classes (additive, upcast-required, breaking); use **Appendix A** as JSON stub input.
2. **Golden vectors** — one row per supported `(from_replay_row_version, to_replay_row_version)` jump — **blocked on D-032 / D-043** for literal CI rows; **unblocked** for drafting matrix semantics, migration playbook, and diff-policy prose in 3.3.2 roadmap text.
3. **Operator adoption** — copy any **“Proposed text for decisions-log”** blocks below into [[decisions-log]] when the project owner accepts the hypothesis.

---

## 6. Working hypotheses (research defaults; partial vault adoption)

> **Label:** **D-048** (2026-03-22) already adopts the **normative draft** (bundle envelope, matrix outcomes, migration playbook) in [[decisions-log]]. Bullets **below** remain **research defaults** for stack-specific knobs until explicitly merged into **D-048** or the tertiary note — not additional vault law by themselves.

### 6.1 On-disk bundle: JSON canonical, protobuf optional

**Hypothesis:** Ship **`PersistenceBundle_v0` as canonical JSON** (UTF-8, sorted keys for debuggability) in repo fixtures and human-editable operator bundles; use **protobuf** (or msgpack) only where bandwidth or storage compaction demands it, with an explicit **`serialization_profile_id`** that pins byte rules. **Tradeoff:** JSON is diff-friendly and junior-debuggable; protobuf is smaller on disk but pushes juniors toward hex dumps — keep JSON for “source of truth” docs and golden fixtures.

### 6.2 Compatibility matrix: static in-repo + optional overlay in bundle

**Hypothesis:** Maintain **`CompatibilityMatrix_v0` as versioned JSON under `1-Projects/<id>/Roadmap/` or `3-Resources/`** (static, reviewable in PRs). Allow an **optional small overlay** inside the live bundle for operator overrides (e.g. experimental profiles) that must still be **hash-covered** or **signed** so resume cannot silently widen compatibility.

### 6.3 Regen lane vs matrix

**Hypothesis:** Treat **regen lane closure** as **both**: (a) a **boolean assertion** on the bundle row evaluated by the matrix (`regen_lane_closed`), and (b) a **separate gate** in the regen pipeline (**3.2.x**) so a bug cannot fake the bit without the lane contract. Matrix answers “is this save logically eligible to resume?”; regen gate answers “did we actually finish regen work before persisting?”

### 6.4 Dependency clarity (D-032 / D-043)

**Blocked:** Literal **golden harness rows** and **frozen replay header preimage** for new `replay_row_version` jumps remain **blocked on D-032 / D-043**. **Not blocked:** compatibility-matrix JSON shape, migration playbook ordering, diff-policy tables, and roadmap prose for Phase 3.3.2.

### Proposed text for decisions-log (paste when approved)

**Block A — on-disk format**

> **Decision (proposed):** Canonical operator-facing `PersistenceBundle_v0` documents are **JSON** with sorted-key convention for fixtures; binary encodings are allowed only behind an explicit `serialization_profile_id` that pins field order and numeric rules.

**Block B — matrix placement**

> **Decision (proposed):** `CompatibilityMatrix_v0` ships as **static, versioned JSON in-repo**; optional per-save overrides may appear in-bundle only when covered by the same integrity mechanism as the checkpoint (hash- or signature-covered).

**Block C — regen seam**

> **Decision (proposed):** Regen lane closure is enforced by **pipeline gate + matrix assertion** (dual check); matrix alone is insufficient.

---

## Appendix A — `CompatibilityMatrix_v0` minimal stub (typed, provisional names)

```json
{
  "matrix_schema_version": "0.1.0",
  "project_id": "genesis-mythos-master",
  "consumers": [
    {
      "engine_profile_id": "sim-ci-2026-03",
      "max_replay_row_version": 7,
      "allowed_serialization_profile_ids": ["facet-manifest-v3"],
      "max_bundle_schema_version": 2,
      "requires_regen_lane_closed": true,
      "max_player_cardinality": 4
    },
    {
      "engine_profile_id": "headless-replay-worker",
      "max_replay_row_version": 7,
      "allowed_serialization_profile_ids": ["facet-manifest-v3", "facet-manifest-v2"],
      "max_bundle_schema_version": 2,
      "requires_regen_lane_closed": false,
      "max_player_cardinality": null
    }
  ],
  "assertions_evaluated": [
    "bundle_schema_version",
    "replay_row_version",
    "serialization_profile_id"
  ]
}
```

---

## Appendix B — Migration playbook v0 (ordered)

1. **Detect** persisted versions: read `bundle_schema_version`, `replay_row_version`, `serialization_profile_id`, snapshot manifest version from `PersistenceBundle` + checkpoint.
2. **Load** static `CompatibilityMatrix_v0` for this build; merge allowed operator overlay (if present and integrity-verified).
3. **Classify** outcome: **COMPAT_OK**, **MIGRATE_REQUIRED**, or **INCOMPATIBLE** (§2.3). Stop on **INCOMPATIBLE** with fail-closed reason code.
4. **Branch migration:**  
   - Additive-only delta ⇒ **tolerant reader** path (no upcast).  
   - Row format change with registered chain ⇒ **upcast on read** for each tick row / bundle fragment.  
   - Facet graph / Merkle shape breaking ⇒ **snapshot rewrite** or **parallel rebuild** (§4).
5. **Recompute** or **verify** dual-hash preflight (3.3.1 step 3) on baseline + tail using **post-migration** `serialization_profile_id`.
6. **Emit** new persisted metadata: bump `replay_row_version` and/or `serialization_profile_id` only through a **documented** migration note (no silent bump).
7. **Record** migration audit id (optional field) for support — must not enter hashed observable preimage unless already allow-listed.

---

## Raw sources (vault)

- [[1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/phase-3-3-1-authoritative-resume-checkpoint-and-session-boundary-roadmap-2026-03-22-2340]]
- [[Ingest/Agent-Research/phase-3-3-1-sim-persistence-cross-session-research-2026-03-22-1830]]
- [[Ingest/Agent-Research/tick-scoped-observable-bundle-after-mutation-apply-research-2026-03-22-2330]]

## Sources

- https://protobuf.dev/best-practices/dos-donts/ (Tier A)
- https://docs.axoniq.io/axon-framework-reference/5.0/events/event-versioning/ (Tier A)
- https://docs.eventsourcingdb.io/best-practices/optimizing-event-replays/ (Tier B)
- https://www.youngju.dev/blog/architecture/2026-03-07-architecture-event-sourcing-cqrs-production-patterns.en (Tier C — supplementary)
