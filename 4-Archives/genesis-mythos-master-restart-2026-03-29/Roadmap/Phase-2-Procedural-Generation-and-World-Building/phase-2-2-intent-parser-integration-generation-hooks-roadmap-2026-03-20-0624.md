---
title: Phase 2.2 — Intent parser integration (generation hooks)
roadmap-level: secondary
phase-number: 2
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-20
tags: [roadmap, genesis-mythos-master, phase]
para-type: Project
subphase-index: "2.2"
handoff_readiness: 94
handoff_gaps:
  - "VCS materialization: fixtures/intent_replay/v0/*.json + CI workflow not yet landed (implementation debt; does not HOLD contract PASS per rollup open risks)"
links:
  - "[[phase-2-procedural-generation-and-world-building-roadmap-2026-03-19-1101]]"
  - "[[genesis-mythos-master-roadmap-2026-03-19-1101]]"
---

## Phase 2.2 — Intent parser integration (generation hooks)

Integrate a player/DM *intent parser* into the Phase 2 generation hook chain so co-authored intent deterministically influences world generation outcomes, while preserving replay safety, immutable published plan artifacts, and fail-closed semantics.

### Objectives

- Define the end-to-end **intent lifecycle**: capture co-authored intent text, canonicalize, parse, validate, and publish an immutable `IntentPlan`.
- Define **where** the intent plan is consumed by generation stages (stage hooks) without violating deterministic ordering or the async commit barrier semantics established in Phase 2.1.
- Define **failure surfaces** as deterministic replay events: invalid intent yields deterministic denials, not partial/implicit fallback behavior.

### Integration contract (v0)

- **Canonical intent bytes:** Require a stable canonicalization step that produces deterministic bytes used for hashing and replay identity.
- **Schema-bound plan:** Require a versioned `IntentPlan` schema (explicit field list, stable serialization rules) so changes are replay-disciplined and detectable.
- **Deterministic hash chain:** Wire `intent_hash` into downstream hash chain inputs that ultimately bind to `policy_bundle_hash` and `manifest_hash` (so intent affects manifest deterministically).
- **Hook consumption rule:** Stage hooks may *read* the published `IntentPlan`, but must not mutate it in-place. Stages must treat the plan as immutable input.
- **Fail-closed semantics:** If parse/validation fails, generation must deterministically stop for that `intent_id` and emit the corresponding denial event under the command/event schema.

### Lifecycle: from co-authored intent to replay-safe stage hooks

1. Co-authored intent text enters the pipeline at the intent entry point (player/DM input boundary).
2. Canonicalization converts intent text into canonical bytes used for identity (no “normalization drift” across runs).
3. Parser produces a structured representation that is validated against the versioned schema.
4. The system publishes an immutable `IntentPlan` plus a deterministic hash identity.
5. Generation stages consume the published plan and derive deterministic impacts via the hash chain into `manifest_hash` / spawn ordering.

### Command/Event contracts

- Ensure validation failures map to deterministic denial events with stable reason codes.
- Ensure stage consumption failures map to deterministic fail-closed events (no silent “use defaults” branches).
- Keep command/event outputs aligned with Phase 1 replay determinism guarantees (stable reason codes, stable replay identities).

### Open questions (for tertiary breakdown)

- **Resolved (v0):** `IntentPlan` consumption boundary is fixed at **manifest-emission** (see **Decision 1** in `### Pending decisions` and [[phase-2-2-2-intentplan-consumption-boundary-and-deterministic-verification-harness-roadmap-2026-03-20-0605]]); aligns with Acceptance criterion **#5**.
- **Residual (canonicalization polish):** Edge-case byte rules beyond golden vectors G1–G3 require an explicit `canonicalization_version` bump; baseline rules are frozen in work units below.
- **Resolved (hashing):** Transient-field exclusion for `IntentPlan` hashing is frozen per **Decision 3** in `### Pending decisions`; only stable semantic fields participate in `stable_field_digest`.

## Research integration

### Key takeaways (drafted without injected research block)

- Deterministic intent identity must be anchored to canonical bytes and a frozen serialization rule.
- Intent must affect `manifest_hash` through a deterministic hash chain, not narrative-only annotations.
- Invalid intent must fail closed with deterministic denial events and stable reason codes.

### Pending decisions

#### Delegatable task decomposition (v1)
Split canonicalization, schema validation, IntentPlan hashing (intent_hash), and denial-event mapping into delegatable work units.

##### Work unit: Canonicalize intent bytes
- Inputs: co-authored intent text (raw), intent_schema_version_as_ascii.
- Outputs: canonical_intent_bytes (deterministic UTF-8 byte string) + canonicalization_version.
- Determinism: canonical_intent_bytes is computed via a fixed, versioned canonicalization function with no model/clock/time influence.
- Dependency: runs before any parse/validation; its output participates in intent_hash computation.

##### Work unit: Validate intent schema
- Inputs: canonical_intent_bytes.
- Outputs: validated_intent_view using a frozen IntentPlan field list (no implicit defaults).
- Fail-closed: on mismatch, emit exactly one deterministic denial event with stable reason_code.

##### Work unit: Compute intent_hash and annotated hash view
- Inputs: validated_intent_view, intent_schema_version_as_ascii.
- Outputs: intent_hash, annotated_intent_hash, intent_stream_id.
- intent_schema_version_as_ascii := "IntentPlan_v0" (fixed for v0 handoff).
- Domain_tag_v0 := GENESIS_MYTHOS_INTENT_HASH_DOMAIN_V0.
- Determinism: intent_hash = SHA256(domain_tag_v0 || len64(canonical_intent_bytes) || canonical_intent_bytes || len64(intent_schema_version_as_ascii) || intent_schema_version_as_ascii || len64(stable_field_digest(validated_intent_view)) || stable_field_digest(validated_intent_view))
- Dependency: intent_hash feeds the Phase-2.1 PolicyBind/ManifestEmit hash-chain seams and deterministically impacts manifest_hash and spawn ordering.

##### Work unit: Map validation/failure into denial events
- Inputs: validation error kind + intent_id + canonicalization_version.
- Outputs: denial_event payload (reason_code + stable fields) aligned to command/event schema v0.
- Ordering: denial publish occurs at the exact stage-hook boundary where IntentPlan would be consumed for that intent_id.

##### Integration dependency map
- Must not allow intent influence to bypass the Phase-2.1 async commit barrier.
- Must preserve replay ordering tuple invariants (spawn_event_id ordering) derived from intent_hash changes only.

#### Acceptance criteria (Phase 2 — handoff gates)
Executable invariants (must hold as pass/fail):
1. Canonical replay identity: canonical_intent_bytes built from the same input and intent_schema_version_as_ascii is bit-identical across runs (byte-for-byte).
2. Hash determinism: intent_hash computed with the formula above is identical for identical inputs and differs for semantic changes.
3. Propagation: any change in intent_hash deterministically changes manifest_hash and the spawn ordering tuple (spawn_event_id order) with no other implicit sources.
4. Fail-closed denial: invalid intent yields exactly one deterministic denial event with a stable reason_code taxonomy; generation halts for that intent_id (no silent fallbacks and no default policy usage).
5. Boundary is explicit: stage-hook boundary for IntentPlan consumption is fixed and used consistently by both the happy path and denial path.

#### Verification and test matrix closure (v1)
Golden vectors (minimum set):
- G1 (Move to Sector A):
  - canonical_intent_bytes_hex: `4d6f766520746f20536563746f7220410a496e74656e74506c616e5f7630`
  - intent_hash_hex: `5b2f6d3fd7c64a7525222fbd7583b11cd6ba71326c9b6b9c314368ba01d4e3a6`
  - manifest_hash_hex: `b5755f84fbfe43a67b8c8b0af6d378f2a529278cbe1388e26b4447f2e2f7a19a`
  - spawn_event_id ordering (v0): `[1b4c2abb8961c17ea5ad331578495cd49fc9c33e3e31ffacd11940fe58844b99]`
- G2 (whitespace/punctuation variants normalize to G1):
  - raw variants: `"  Move   to   Sector   A  "` (and any equivalent whitespace runs)
  - canonical_intent_bytes_hex: `4d6f766520746f20536563746f7220410a496e74656e74506c616e5f7630` (must match G1)
  - intent_hash_hex: `5b2f6d3fd7c64a7525222fbd7583b11cd6ba71326c9b6b9c314368ba01d4e3a6` (must match G1)
  - manifest_hash_hex: `b5755f84fbfe43a67b8c8b0af6d378f2a529278cbe1388e26b4447f2e2f7a19a` (must match G1)
  - spawn_event_id ordering (v0): `[1b4c2abb8961c17ea5ad331578495cd49fc9c33e3e31ffacd11940fe58844b99]` (must match G1)
- G3 (Rest at Sector A):
  - canonical_intent_bytes_hex: `5265737420617420536563746f7220410a496e74656e74506c616e5f7630`
  - intent_hash_hex: `933778468e12f75dacae727638f1edff8eb8a6216d2b7a89cee1312eeec30360`
  - manifest_hash_hex: `fe980e32ed7c84197b9567d2bccc7746194a667a720d8ccdc0e72ad477b73471`
  - spawn_event_id ordering (v0): `[313f06099e5c205731afa9e3d7074f4e6a27371f3638f0c5efbec6d7d7cd3a38]`

Fail-closed cases (minimum):
- F1 schema mismatch: violates the frozen IntentPlan field list -> denial reason_code INTENT_SCHEMA_MISMATCH; verify stage consumption halts.
- F2 canonicalization error: contains disallowed characters or un-decodable bytes -> denial reason_code INTENT_CANONICALIZATION_ERROR; verify stage consumption halts.

Test procedure checklist:
- Step 1: run canonicalization -> canonical_intent_bytes.
- Step 2: validate schema -> validated_intent_view or denial.
- Step 3: compute intent_hash -> annotated_intent_hash.
- Step 4: simulate Phase 2 stage-hook consumption at the fixed boundary; produce manifest_hash and spawn ordering.
- Step 5: assert determinism (bit-identical replay) and fail-closed behavior (no partial side-effects).

#### Pending decisions — closed contract (Phase 2.2 handoff)
Resolve the three pending decisions with fixed, deterministic answers.

##### Decision 1: IntentPlan consumption boundary
Chosen boundary: IntentPlan is consumed at the manifest-emission boundary, after PolicyBind completes deterministic policy derivation and immediately before ManifestEmit draft emission. Stage hooks must treat IntentPlan as immutable input and may only read, never mutate.

##### Decision 2: Canonical bytes rules
CanonicalizeIntentBytes_v1:
- Decode input as UTF-8.
- Normalize Unicode to NFC.
- Convert line endings to LF.
- Trim leading/trailing whitespace.
- Collapse runs of whitespace (space/tab/LF) into a single space.
- Remove zero-width codepoints.
- intent_schema_version_as_ascii := "IntentPlan_v0" (fixed for v0 handoff).
- Output: canonical_intent_bytes = utf8(trim_collapse(intent_text) + LF_SEP + intent_schema_version_as_ascii), where LF_SEP denotes a single LF byte.

Hash concatenation rules:
- All concatenations inside intent_hash use length-prefixed fields (len64) to prevent ambiguity.
- Use domain_tag_v0 = "GENESIS_MYTHOS_INTENT_HASH_DOMAIN_V0" as a fixed ASCII prefix.

##### Decision 3: Transient-field exclusion from IntentPlan hashing
Excluded from hashing (explicit set transient_intent_fields):
- processing timestamps and wall-clock fields (e.g. intent_processing_time_utc)
- run ids / session ids / trace ids (e.g. generation_run_id, ui_request_id)
- any free-form diagnostic strings that do not participate in deterministic semantics
- non-deterministic model outputs or sampling metadata

Only stable semantic fields that map to validated_intent_view participate in stable_field_digest(validated_intent_view).

stable_field_digest(validated_intent_view) — stable serialization + digest
- stable_subset fields (ordered by key name in stable JSON):
  - intent_kind
  - canonical_target
  - intent_constraints (array; sorted lexicographically)
  - intent_schema_version (fixed to intent_schema_version_as_ascii = "IntentPlan_v0" for this v0 handoff)
- stable_json(validated_intent_view_stable_subset) := UTF-8 JSON with:
  - keys sorted lexicographically
  - no insignificant whitespace (canonical separators)
- stable_field_digest(validated_intent_view) := SHA-256(stable_json_bytes)

Canonicalization + hashing are versioned: canonicalization_version := "CanonicalizeIntentBytes_v1".
If any version bump occurs, golden vectors and replay identity rules must be recomputed.

## Tertiary notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building"
WHERE roadmap-level = "secondary" OR roadmap-level = "tertiary" OR roadmap-level = "task"
SORT subphase-index ASC, file.name ASC
```

Explicit tertiary links (for handoff trace traversal):
- [[phase-2-2-1-intent-canonicalization-and-denial-taxonomy-roadmap-2026-03-20-0901]]
- [[phase-2-2-2-intentplan-consumption-boundary-and-deterministic-verification-harness-roadmap-2026-03-20-0605]]
- [[phase-2-2-3-ci-golden-registry-and-boundary-regression-gates-roadmap-2026-03-21-1205]]
- [[phase-2-2-4-phase-2-2-secondary-closure-rollup-and-advance-readiness-roadmap-2026-03-21-2000]]

