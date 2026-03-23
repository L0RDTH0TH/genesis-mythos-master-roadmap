---
title: Phase 2.3.1 — EMG normative schema bindings + seed matrix v0
roadmap-level: tertiary
phase-number: 2
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-21
tags: [roadmap, genesis-mythos-master, phase, EMG, test-seeds, determinism]
para-type: Project
subphase-index: "2.3.1"
handoff_readiness: 94
handoff_readiness_scope: "structural/spec-draft completeness for EMG bindings + PBT alphabet + matrix shape — not executable golden closure"
handoff_gaps:
  - "EMG-2 numeric floor F remains TBD until authoritative_lore_flags and sim_observed_counters paths are frozen in implementation schema"
  - "EXAMPLE JSON paths and placeholder expected_emergence_hash are non-normative until wiki-linked freeze (D-023 promotion)"
  - "Delegation / CI execution remains blocked until F, frozen paths, and real golden hash replace placeholders"
links:
  - "[[phase-2-3-validate-co-authored-world-emergence-through-test-seeds-roadmap-2026-03-21-2025]]"
  - "[[phase-2-2-3-ci-golden-registry-and-boundary-regression-gates-roadmap-2026-03-21-1205]]"
  - "[[phase-2-2-1-intent-canonicalization-and-denial-taxonomy-roadmap-2026-03-20-0901]]"
  - "[[decisions-log]]"
---

## Phase 2.3.1 — EMG normative schema bindings and seed matrix v0

This tertiary **binds** **EMG-1..3** from the Phase 2.3 secondary to **named JSON paths**, **canonicalization profiles**, and **golden-matrix columns** so `ReplayAndVerify` extensions do not fork into a second harness family. It also freezes a **finite PBT command alphabet** for author/sim interleaving (reified commands before execution).

**Mid-technical (depth 3):** interfaces + algorithm sketches; exact repo field names stay **EXAMPLE** until schema freeze — every EXAMPLE row must wiki-link to a pseudo-code row on promotion.

### Deterministic pseudo-code (v0)

#### EMG slice extraction + JCS profile
```pseudo
constants:
  jcs_profile_id := "JCS-RFC8785@v1"
  emg1_allow_list_version := "emg1-v0"   // bump when paths change

type EmergenceMatrixRow:
  fixture_id: string
  seed_envelope_ref: string              // path or content-hash to frozen JSON
  tick_n: uint64
  expected_emergence_hash: bytes32       // EMG-1 output
  tolerance_tier: enum { A, B, C }       // float/GPU posture per research §1a

function LoadAllowListedJsonSubtrees(ledger_json, allow_list: JsonPath[]):
  // Returns ordered list of logical JSON values (I-JSON safe) for canonicalization
  values := []
  for path in SORT_LEX(allow_list):
    values.append(EXTRACT_JSON_PATH(ledger_json, path))
  return values

function EMG1_ReplayEmergenceHash(ledger_at_tick_N, matrix_row: EmergenceMatrixRow):
  tier := matrix_row.tolerance_tier
  if tier == C and not HasGpuDeterminismContract():
    return Error("EMG-1 non-applicable: Tier C without GPU determinism contract")
  allow_list := LoadAllowList("EMG1", emg1_allow_list_version)  // wiki-linked table in this note
  subtrees := LoadAllowListedJsonSubtrees(ledger_at_tick_N, allow_list)
  envelope := RESOLVE_REF(matrix_row.seed_envelope_ref)
  preimage_object := {
    "schema_id": SCHEMA_ID,
    "schema_version": SCHEMA_VERSION,
    "jcs_profile": jcs_profile_id,
    "allow_list": emg1_allow_list_version,
    "tier": tier,
    "seed_envelope": envelope,
    "subtrees": subtrees
  }
  canonical_utf8 := JCS_CANONICALIZE(preimage_object)   // RFC 8785
  return SHA256(canonical_utf8)

function EMG2_LoreSimAlignmentScore(ledger_slice):
  // **Non-normative sketch:** normative `AlignmentFn_v0`, RFC 6901 pointers, `AlignmentOutcome`, and floor **F** live **only** in [[phase-2-3-2-emg-2-floor-frozen-json-pointers-and-alignmentfn-v0-roadmap-2026-03-21-2245]].
  // Do not implement a second `AlignmentFn_v0` API here; delegate reads to that tertiary’s frozen pointer table + pseudo-code.
  return DELEGATE_TO_PHASE_2_3_2_EMG2(ledger_slice)

function EMG3_DenialInvariantClosed(denial_events, frozen_taxonomy_ref):
  // frozen_taxonomy_ref -> Phase 2.2.1 note
  for ev in denial_events:
    if ev.code NOT_IN frozen_taxonomy_ref.allow_list:
      return (closed: false, unexpected: ev.code)
  return (closed: true, unexpected: null)
```

> [!warning] EMG-2 contract split
> **EMG-2** alignment function contract (`AlignmentFn_v0`, `AlignmentOutcome`, RFC 6901 pointers, provisional **F**) is **normative only** in [[phase-2-3-2-emg-2-floor-frozen-json-pointers-and-alignmentfn-v0-roadmap-2026-03-21-2245]]. This note retains **EMG-1 / EMG-3** sketches, PBT alphabet, and seed-matrix **shape** only.

#### Seed matrix (illustrative example row — non-normative until freeze)

> [!note] Draft posture
> This row demonstrates **registry column shape** only. **`expected_emergence_hash`** is a **placeholder**; **`seed_envelope_ref`** uses an **EXAMPLE** path. Do not treat as CI-golden until D-023 promotion checklist completes.

| fixture_id | seed_envelope_ref | tick_n | tolerance_tier | expected_emergence_hash (EXAMPLE) | alignment_floor_F | notes |
| --- | --- | --- | --- | --- | --- | --- |
| `FX-EMG-SMOKE-001` | `goldens/seed_envelopes/smoke_001.json` (EXAMPLE path) | 64 | A | `0x…deadbeef…` (placeholder) | TBD | Row proves matrix shape; hash filled when ledger paths freeze |

### Finite PBT command alphabet (v0)

Reify commands **before** execution; generator may interleave in valid orders only.

| Command | Payload shape (sketch) | Preconditions | Postcondition (oracle hook) |
| --- | --- | --- | --- |
| `AuthorIntent` | `IntentPlan` bytes + metadata | canonicalization pipeline available | intent ledger append OR deterministic denial |
| `SimTick` | `{ delta_ticks: uint }` | stage graph idle barrier satisfied | manifest / counters advance OR deterministic denial |
| `QueryObservedCounters` | `{}` | none | read-only slice for EMG-2 oracle |
| `QueryLoreFlags` | `{}` | none | read-only slice for EMG-2 oracle |
| `ForceDenial` | `{ code: DenialCode }` | **only** codes enumerated in 2.2.1 taxonomy | EMG-3 expects allow-list closure |

**Property template (acceptance sentence):** For all command sequences generated under alphabet **v0**, `EMG3_DenialInvariantClosed` holds and `EMG1_ReplayEmergenceHash` matches golden row when `(fixture_id, tier)` is **A** and paths are allow-listed.

### EMG ↔ path ↔ profile (normative draft table)

| EMG-ID | JSON path(s) (EXAMPLE — replace on freeze) | canonicalization_profile | golden_registry_column |
| --- | --- | --- | --- |
| EMG-1 | `$.seed_envelope`, `$.intent_ledger_tail`, `$.manifest.post_tick` (subtree allow-list) | `JCS-RFC8785@v1` + `emg1-v0` | `expected_emergence_hash` |
| EMG-2 | `$.lore.flags`, `$.sim.counters` | *(value read; optional hash)* | `alignment_score_floor` |
| EMG-3 | `$.denials[*].code` | sorted code list → JCS | `unexpected_denial_count` |

## Research integration

### Key takeaways

- Bind **EMG-1** to **JCS (RFC 8785)** + versioned allow-list; matrix rows carry `tolerance_tier` **A/B/C** for float/GPU posture (Tier C defaults to **no EMG-1 hash** without a GPU determinism contract).
- **EMG-2** uses the finite **PBT command alphabet** above; oracle reads **only** frozen JSON paths.
- **EMG-3** reuses **Phase 2.2.1** denial taxonomy; property = zero unexpected codes.
- External synthesis with traceability: [[Ingest/Agent-Research/phase-2-3-1-emg-schema-bindings-research-2026-03-21-2310]].

### Decisions / constraints

- **Allow-list bumps** require `emg1_allow_list_version` increment and golden row review (same promotion rules as Phase 2.2.3 CI registry).
- **Do not** hash GPU-derived floats on EMG-1 until Tier C contract exists (see synthesis §1a).

### Links

- [[Ingest/Agent-Research/phase-2-3-1-emg-schema-bindings-research-2026-03-21-2310]]
- [[Ingest/Agent-Research/phase-2-3-validate-co-authored-world-emergence-research-2026-03-21-2230]]
- Raw: [[Ingest/Agent-Research/Raw/phase-2-3-1-emg-schema-bindings-raw-2026-03-21-2310]]

### Sources

- See `## Sources` in the synthesis note for URL list and external traceability.
