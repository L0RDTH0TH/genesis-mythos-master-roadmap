---
title: Phase 2.2.3 — CI golden registry + boundary regression gates
roadmap-level: tertiary
phase-number: 2
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-21
tags: [roadmap, genesis-mythos-master, phase, intent-parser, determinism, handoff-readiness, ci]
para-type: Project
subphase-index: "2.2.3"
handoff_readiness: 93
links:
  - "[[phase-2-2-2-intentplan-consumption-boundary-and-deterministic-verification-harness-roadmap-2026-03-20-0605]]"
  - "[[phase-2-2-intent-parser-integration-generation-hooks-roadmap-2026-03-20-0624]]"
  - "[[decisions-log]]"
---

## Phase 2.2.3 — CI golden registry + boundary regression gates

This tertiary closes the loop between **Phase 2.2.2**’s executable replay narrative and **operational proof**: where golden vectors live, how CI runs `ReplayAndVerify`, and how intentional semantic changes are promoted without silent drift.

### Golden artifact registry (normative layout)

All vectors from [[phase-2-2-2-intentplan-consumption-boundary-and-deterministic-verification-harness-roadmap-2026-03-20-0605]] are mirrored as **machine-consumable records** (JSON or canonical UTF-8 text) under a single registry root, e.g. `fixtures/intent_replay/v0/`:

- `G1.json`, `G2.json`, `G3.json` — happy path inputs + expected `manifest_hash_hex` + `spawn_event_id_ordering`
- `F1.json`, `F2.json` — denial path inputs + expected `reason_code` + `intent_id` / `error_fingerprint` + **no manifest** invariant

Each record includes:

- `deterministic_gate_version_id` := `DETERMINISTIC_GATE_V1` (must match harness)
- `canonicalization_version`, `intent_schema_version_as_ascii`
- `expected_ledger_outcomes` := `{ first: "applied", second: "ledger-hit" }`

### EMG-2 alignment registry row (parallel — **DEFERRED**)

Normative wiring for EMG-2 lives in [[phase-2-3-3-emg-2-ci-golden-registry-row-and-fixture-hardening-roadmap-2026-03-21-2249]]; this table tracks the **wiki/registry** row for Phase 2.2.3 until VCS fixtures land.

| Row ID | Status | Owner | Trigger to promote | Links |
| --- | --- | --- | --- | --- |
| G-EMG2-ALIGN | **DEFERRED** | Roadmap / implementer | First merged PR under `fixtures/emg2_alignment/**` + passing `AlignAndVerify` | [[decisions-log]] **D-025**, **D-026** |

### CI job contract (minimum)

```pseudo
procedure CI_IntentReplaySuite():
  for vector in RegistryList(glob="fixtures/intent_replay/v0/*.json"):
    outputs := ReplayAndVerify(vector.replay_inputs, vector.golden_expectations)
    assert outputs matches vector.golden_expectations exactly

  assert no additional emits beyond expected per vector (denials: exactly_one_denial_event)
```

**Triggers (required):** any change touching `CanonicalizeIntentBytes_*`, `IntentPlan` schema, `intent_hash` preimage, `ManifestEmit` boundary wiring, or ledger apply idempotency.

**Failure semantics:** mismatch fails the build; no auto-refresh in CI (refresh is a PR-authored golden update).

### Promotion policy (human gate)

1. Engineer runs harness locally with `RECORD_GOLDEN=1` (or equivalent) **only** after intentional semantic change.
2. PR must include: (a) updated golden files, (b) `DETERMINISTIC_GATE_V1` bump **or** explicit waiver note tied to decisions-log id, (c) diff summary of hash changes.
3. CODEOWNERS (or second reviewer) required for `fixtures/intent_replay/**`.

### Flake and nondeterminism controls

- Strip or normalize volatile fields **before** comparison (timestamps, run ids) per Phase 2.2.2 stable-subset rules.
- Pin toolchain versions for crypto + UTF-8 NFC in CI matrix.
- If harness reads workspace files, pin fixture encoding to UTF-8 without BOM.

### Handoff readiness evidence inventory

This note is handoff-ready when:

1. Registry paths exist and are linked from this note.
2. CI job name + trigger paths are documented (copy-pasteable for junior setup).
3. Promotion policy is explicit (no silent golden edits).
4. `handoff_readiness` is evidence-based (checklist above), not narrative-only.

### Phase 3.4 ambient + mixed-tick registry rows (**TBD** — **G-P3.4-REGISTRY-CI**)

Placeholder checklist for **living-world** golden / CI rows that must exist **before** clearing **G-P3.4-REGISTRY-CI** on [[phase-3-4-4-phase-3-4-secondary-closure-rollup-and-advance-readiness-roadmap-2026-03-23-1935]]. **No PASS / no green-CI claims** until checked-in fixtures + job policy land per **D-020** / **D-032** / **D-045**.

| Row / fixture ID | Scope | Status | Notes |
| --- | --- | --- | --- |
| `G-P3.4-AMBIENT-MIXED-TICK-v0` | Ambient slice + replay tick in one harness | **TBD** | Path under `fixtures/**` **not** specified until eng draft |
| `G-P3.4-MIGRATION-RESUME-v0` | **PersistenceBundle_vN** + migrate-and-resume vs **3.3.x** | **TBD** | Depends on **D-048** / **D-049** harness IDs |
| CI job / trigger paths | ReplayAndVerify (or successor) on above | **TBD** | Document job name here when wired |

## Research integration

### Key takeaways

- Golden-file testing treats reference outputs as versioned code; any change requires explicit review.
- Deterministic replay suites should mask nondeterministic fields before diff.
- Industry patterns (pytest-golden, Rust goldenfile, regression plugins) align with **fail-on-drift + PR-based golden updates**.

### Decisions / constraints

- No CI auto-update of goldens; refresh is always a deliberate PR action.
- Vectors G1–G3 and F1–F2 remain the **minimum** proving set until expanded by a future tertiary or task note.

### Links

- [[Ingest/Agent-Research/phase-2-2-3-ci-golden-registry-regression-gates-research-2026-03-21-1205.md]]
- [[phase-2-2-2-intentplan-consumption-boundary-and-deterministic-verification-harness-roadmap-2026-03-20-0605]]

### Sources

- [Golden File Testing: Output Comparison | Application Architect](https://www.application-architect.com/posts/golden-file-testing-output-comparison/)
- [pytest-golden · PyPI](https://pypi.org/project/pytest-golden/)
- [goldenfile · crates.io](https://crates.io/crates/goldenfile)
