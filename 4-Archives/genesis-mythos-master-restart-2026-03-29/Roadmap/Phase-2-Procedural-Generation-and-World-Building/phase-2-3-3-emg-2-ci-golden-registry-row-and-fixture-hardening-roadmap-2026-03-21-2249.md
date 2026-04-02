---
title: Phase 2.3.3 — EMG-2 CI golden registry row + fixture hardening
roadmap-level: tertiary
phase-number: 2
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-21
tags: [roadmap, genesis-mythos-master, phase, EMG-2, CI, golden-registry, test-seeds]
para-type: Project
subphase-index: "2.3.3"
emg2_registry_wiring_status: "draft — row schema + CI pseudo + WA matrix; wiki registry row in Phase 2.2.3 note pending VCS"
handoff_readiness: 94
normative_handoff_readiness: 94
execution_handoff_readiness: 72
handoff_readiness_scope: "normative fixtures root + row schema + AlignAndVerify pseudo + worst-acceptable matrix — not live CI green until VCS"
handoff_gaps:
  - "Wiki-linked **G-EMG2-\*** row still absent in [[phase-2-2-3-ci-golden-registry-and-boundary-regression-gates-roadmap-2026-03-21-1205]] until fixture files land under `fixtures/emg2_alignment/v0/` in repo"
  - "Harness enum strings for `golden_expectations.reason_code` must match implementation before promotion"
links:
  - "[[phase-2-3-2-emg-2-floor-frozen-json-pointers-and-alignmentfn-v0-roadmap-2026-03-21-2245]]"
  - "[[phase-2-2-3-ci-golden-registry-and-boundary-regression-gates-roadmap-2026-03-21-1205]]"
  - "[[phase-2-3-1-emg-normative-schema-bindings-and-seed-matrix-v0-roadmap-2026-03-21-2205]]"
  - "[[decisions-log]]"
---

## Phase 2.3.3 — EMG-2 **CI golden registry row** + **fixture hardening**

> [!warning] Readiness split
> **`handoff_readiness` / `normative_handoff_readiness` (94)** = spec + vault wiring clarity only. **`execution_handoff_readiness` (72)** = VCS fixtures + CI job + closed WA runs — do **not** treat 94 as “ready to ship” until execution items close. See [[decisions-log]] **D-026**.

> **Normative scope:** Close the **implementation bridge** between **2.3.2** (`AlignmentFn_v0`, RFC 6901 pointers, provisional **F**) and **2.2.3** (G1–G3 / F1–F2 golden registry + `ReplayAndVerify` policy). This note defines **where** EMG-2 vectors live in-repo, **how** CI should run them, and **how** the **worst-acceptable** matrix calibrates **`emg2_alignment_floor_F`** before `emg2_floor_F_status: frozen`.

**Mid-technical (depth 3):** registry record shape, CI glob + verifier pseudo-code, bounded calibration matrix — no live workflow YAML until VCS owns paths.

### Parallel fixtures root (collision-safe)

- **Root:** `fixtures/emg2_alignment/v0/` (distinct from `fixtures/intent_replay/v0/`).
- **Rationale:** Different trigger paths (`AlignmentFn_v0` + pointer eval vs intent canonicalization); keeps `paths:` / CODEOWNERS scopes tight per D-020.

### Row schema (one JSON file per vector)

Minimum fields (aligns with research synthesis):

| Field | Role |
| --- | --- |
| `emg2_gate_version_id` | e.g. `EMG2_ALIGNMENT_GATE_V0` — must match harness |
| `emg2_alignment_floor_version` | Echo `emg2-F-v0` / floor version from 2.3.2 |
| `emg2_alignment_floor_F` | Pinned uint8 for this vector (must match project floor when frozen) |
| `tier` | `A` / `B` / `C` (Tier C float → fail-closed per 2.3.2) |
| `lore_json`, `sim_json` | **Inline** objects (v0 — no indirection) |
| `pointers` | `{ "authoritative_lore_flags": "/lore/flags", "sim_observed_counters": "/sim/counters" }` |
| `golden_expectations` | Discriminated: `OK` band, `BELOW_FLOOR`, or `INVALID_EMG2_SLICE` + reason |

### CI pseudo-code (`AlignAndVerify`)

```pseudo
for vector in RegistryGlob("fixtures/emg2_alignment/v0/*.json"):
  assert vector.emg2_gate_version_id == EMG2_ALIGNMENT_GATE_V0
  out := AlignmentFn_v0(vector.lore_json, vector.sim_json, vector.pointers, vector.tier)
  assert MatchesGolden(out, vector.golden_expectations)
  // mismatch => fail build; no auto-refresh in CI (RECORD_GOLDEN local only; PR review)
```

### Worst-acceptable calibration matrix (bounded)

| ID | Intent |
| --- | --- |
| WA-1 | Max drift lore vs sim still ≥ **F** |
| WA-2 | Borderline shape mismatch → `INVALID_EMG2_SLICE` |
| WA-3 | Score just below **F** → `BELOW_FLOOR` |
| WA-4 | Tier C GPU-float path → `INVALID_EMG2_SLICE` when hash-binding required |

Run matrix before setting `emg2_floor_F_status: frozen`; prefer **shape tighten** over lowering **F**.

### Registry row in Phase 2.2.3 note (target)

Add wiki table row **G-EMG2-ALIGN** linking `fixtures/emg2_alignment/v0/G1.json` (pass), `F1.json` / `F2.json` (denials), and policy parity with G-P2.2-CI — **vault edit in** [[phase-2-2-3-ci-golden-registry-and-boundary-regression-gates-roadmap-2026-03-21-1205]] when fixtures exist; until then **TBD (non-HOLD)** per D-021/D-024.

## Risk register (v0)

| Risk | Owner | Mitigation | Review trigger |
| --- | --- | --- | --- |
| `handoff_readiness` misread as CI-green | Roadmap architect | Dual frontmatter + warning callout | Any raise of `handoff_readiness` without VCS proof |
| Fixture PR blocked on enum mismatch | Implementer | Harness enum contract table below | First failing `AlignAndVerify` in CI |
| **F** drift vs bounded matrix | QA / sim | WA log + bump `emg2_alignment_floor_version` | Any score band violation |

## Harness enum contract (v0)

| `golden_expectations` / `reason_code` (vault) | Implementation hook (target) |
| --- | --- |
| `POINTER_RESOLUTION_ERROR` | JSON Pointer eval failure |
| `TYPE_MISMATCH_LORE_SIM` | Shape mismatch at resolved nodes |
| `DUPLICATE_KEY_AT_NODE` | Forbidden duplicate keys at resolved object |
| `BELOW_FLOOR` | `AlignmentOutcome.outcome == BELOW_FLOOR` |
| `INVALID_EMG2_SLICE` | Catch-all invalid / Tier-C fail-closed |

## WA matrix execution log

| Run | Status | Outcome | F-freeze decision |
| --- | --- | --- | --- |
| WA-1 | **NOT RUN** | — | pending |
| WA-2 | **NOT RUN** | — | pending |
| WA-3 | **NOT RUN** | — | pending |
| WA-4 | **NOT RUN** | — | pending |

## Research integration

### Key takeaways

- Separate **`fixtures/emg2_alignment/v0/`** root; mirror G1–G3 / F naming; **`EMG2_ALIGNMENT_GATE_V0`** parallels `DETERMINISTIC_GATE_V1`.
- Row schema pins floor version + inline JSON + discriminated expectations; harness compares normalized `AlignmentOutcome` only.
- PR policy inherits 2.2.3: no CI auto-refresh; CODEOWNERS on fixtures; decisions-log waiver on gate bump.
- Bounded WA matrix drives **F** freeze; then promote wiki registry row + set `emg2_floor_F_status: frozen` on 2.3.2 when calibration closes.

### Links

- Synthesis: [[Ingest/Agent-Research/phase-2-3-3-emg2-alignment-golden-gate-wiring-research-2026-03-21-2315]]
- Upstream EMG-2 contract: [[phase-2-3-2-emg-2-floor-frozen-json-pointers-and-alignmentfn-v0-roadmap-2026-03-21-2245]]
- Golden registry pattern: [[phase-2-2-3-ci-golden-registry-and-boundary-regression-gates-roadmap-2026-03-21-1205]]

### Tasks

**Vault-now (no VCS)**

- [ ] Copy **G1 / F1 / F2** JSON skeletons from [[Ingest/Agent-Research/phase-2-3-3-emg2-alignment-golden-gate-wiring-research-2026-03-21-2315]] into a working note (or `Ingest/Agent-Output/`) as **draft** stand-ins until **D-026** promotion path is chosen.
- [x] Split **normative vs execution** readiness in frontmatter + warning callout (this note).
- [x] Add **risk register**, **harness enum contract**, **WA log** scaffold (this note).

**VCS / PR (evidence required)**

- [ ] Add `fixtures/emg2_alignment/v0/`, `G1.json`, `F1.json`, `F2.json` (from research synthesis) in repo.
- [ ] Open PR: CI job `paths: fixtures/emg2_alignment/**` + harness `AlignAndVerify` stub.
- [ ] Execute WA matrix; fill **WA matrix execution log**; bump `emg2_alignment_floor_version` if **F** moves.
- [ ] When frozen: append **G-EMG2-\*** row in Phase 2.2.3 note + update **D-024** / **D-025** status in [[decisions-log]].
