---
title: "Research — Phase 2.3.3 EMG-2 alignment ↔ CI golden registry (G1–G3 / F wiring)"
research_query: "EMG-2 alignment checks wired to Phase 2.2.3 golden registry pattern; registry schema; fixture matrix for emg2_alignment_floor_F"
linked_phase: "Phase-2-3-3"
project_id: genesis-mythos-master
created: 2026-03-21
tags: [research, agent-research, EMG-2, alignment, CI, golden-files, genesis-mythos-master]
agent-generated: true
research_tools_used: [web_search, vault_context]
---

## Purpose

Bridge **Phase 2.3.2** (`AlignmentFn_v0`, RFC 6901 pointers, provisional `emg2_alignment_floor_F`) to **Phase 2.2.3**’s **CI golden registry + boundary regression gates** so the next tertiary (**2.3.3**) can specify *where* EMG-2 vectors live, *how* CI runs them, and *how* `F` is calibrated from a **bounded worst-acceptable** matrix before `emg2_floor_F_status: frozen`.

**Do not duplicate:** Phase 2.2.3 already defines `fixtures/intent_replay/v0/`, G1–G3 / F1–F2, `DETERMINISTIC_GATE_V1`, promotion policy, and CODEOWNERS. Phase 2.3.2 already defines pointer registry, `AlignmentFn_v0` pseudo-code, and provisional **F** policy. This note adds **wiring**, **schema**, **ID conventions**, and **matrix calibration** only.

### Vault excerpts (normative facts carried forward)

**Index vs excerpts:** Bullets below **restate** normative strings/paths from the linked notes (not wikilink-only stubs). For full prose, open the linked phase notes.

From [[phase-2-2-3-ci-golden-registry-and-boundary-regression-gates-roadmap-2026-03-21-1205]]:

- Registry files include `G1.json`, `G2.json`, `G3.json` (happy) and `F1.json`, `F2.json` (denial) under `fixtures/intent_replay/v0/`.
- Each record includes `deterministic_gate_version_id` := `DETERMINISTIC_GATE_V1` (must match harness).
- CI contract: `for vector in RegistryList(glob="fixtures/intent_replay/v0/*.json")` then `ReplayAndVerify` — **mismatch fails the build**; **no auto-refresh in CI**.
- Promotion: local `RECORD_GOLDEN=1` only after intentional semantic change; PR bundles updated goldens + gate bump or waiver tied to decisions-log; **CODEOWNERS** on `fixtures/intent_replay/**`.

From [[phase-2-3-2-emg-2-floor-frozen-json-pointers-and-alignmentfn-v0-roadmap-2026-03-21-2245]] frontmatter / body:

- `emg2_alignment_floor_F: 85` (provisional), `emg2_floor_F_status: "provisional — calibrate from worst-acceptable fixture set before CI promotion"`.
- Handoff gap (explicit): registry row for EMG-2 alignment in the 2.2.3 note remains **absent until fixture IDs land in VCS**.
- Outcomes: `OK` | `INVALID_EMG2_SLICE` | `BELOW_FLOOR`; fail-closed on pointer/shape errors.

**Loader contract (v0, single):** `lore_json` and `sim_json` are **inline JSON objects** in each vector file. No `fixture_path` indirection in v0 — add a `v1` registry if external file refs are needed.

## Vault alignment (normative pointers)

| Source | Role |
| --- | --- |
| [[phase-2-2-3-ci-golden-registry-and-boundary-regression-gates-roadmap-2026-03-21-1205]] | G1–G3 / F1–F2 layout, CI job contract, promotion policy, triggers |
| [[phase-2-3-2-emg-2-floor-frozen-json-pointers-and-alignmentfn-v0-roadmap-2026-03-21-2245]] | EMG-2 pointers, `AlignmentFn_v0`, `INVALID_EMG2_SLICE` / `BELOW_FLOOR`, fixture calibration steps |

## 1. Registry layout (parallel root — avoid collision with intent replay)

Use a **separate registry root** so triggers and CODEOWNERS can be scoped without overloading `intent_replay`:

- Suggested root: `fixtures/emg2_alignment/v0/` (mirror the `v0` versioning style from 2.2.3).

**Rationale:** EMG-2 gates touch `AlignmentFn_v0`, JSON pointer evaluation, and optional JCS projection — different trigger paths than `CanonicalizeIntentBytes` / `IntentPlan`. A distinct root keeps CI `paths:` filters precise.

## 2. Row schema (machine record per vector)

Each file is one vector (same *shape* as 2.2.3’s one-record-per-file style). Minimum fields:

| Field | Type | Notes |
| --- | --- | --- |
| `emg2_gate_version_id` | string | e.g. `EMG2_ALIGNMENT_GATE_V0`; must match harness |
| `emg2_alignment_floor_version` | string | Echo from [[phase-2-3-2-emg-2-floor-frozen-json-pointers-and-alignmentfn-v0-roadmap-2026-03-21-2245]] frontmatter (`emg2_alignment_floor_version` / `emg2-F-v0`) |
| `emg2_alignment_floor_F` | uint8 | **Pinned integer** for this vector (CI must match project `emg2_alignment_floor_F` in [[phase-2-3-2-emg-2-floor-frozen-json-pointers-and-alignmentfn-v0-roadmap-2026-03-21-2245]] when promoting to frozen) |
| `canonicalization_version` | string | If JCS projection used for audit compares; else `"none"` |
| `tier` | enum | `A` \| `B` \| `C` — aligns with 2.3.2 Tier C fail-closed rule |
| `lore_json` | object | **Inline** authoritative lore JSON (v0 — no path indirection) |
| `sim_json` | object | **Inline** sim-observed JSON |
| `pointers` | object | `{ "authoritative_lore_flags": "/lore/flags", "sim_observed_counters": "/sim/counters" }` per frozen registry |
| `golden_expectations` | object | See below |

**`golden_expectations` (discriminated):**

- **Pass path:** `{ "outcome": "OK", "score_min": <uint8>, "score_max": <uint8> }` — use a band, not a single integer, if structured score has intentional wiggle before freeze.
- **Below floor:** `{ "outcome": "BELOW_FLOOR", "score_max": <uint8> }` with `score_max < emg2_alignment_floor_F`.
- **Invalid slice:** `{ "outcome": "INVALID_EMG2_SLICE", "reason_code": "..." }` — align with harness vocabulary (pointer error, type mismatch, duplicate keys).

Harness compares **only** normalized outputs (mask volatile fields if any exist in future; today ticks are in-record — pin them in fixtures).

### Minimal canonical example (`fixtures/emg2_alignment/v0/G1.json`)

```json
{
  "emg2_gate_version_id": "EMG2_ALIGNMENT_GATE_V0",
  "emg2_alignment_floor_version": "emg2-F-v0",
  "emg2_alignment_floor_F": 85,
  "canonicalization_version": "none",
  "tier": "A",
  "pointers": {
    "authoritative_lore_flags": "/lore/flags",
    "sim_observed_counters": "/sim/counters"
  },
  "lore_json": {
    "lore": {
      "flags": {
        "alpha": { "value": true, "source_tick": 1 }
      }
    }
  },
  "sim_json": {
    "sim": {
      "counters": {
        "alpha": { "count": 1, "last_tick": 1 }
      }
    }
  },
  "golden_expectations": {
    "outcome": "OK",
    "score_min": 90,
    "score_max": 100
  }
}
```

### Minimal failure-path examples (F1 / F2)

**F1 — `INVALID_EMG2_SLICE` (type mismatch at resolved pointer):**

```json
{
  "emg2_gate_version_id": "EMG2_ALIGNMENT_GATE_V0",
  "emg2_alignment_floor_version": "emg2-F-v0",
  "emg2_alignment_floor_F": 85,
  "canonicalization_version": "none",
  "tier": "A",
  "pointers": {
    "authoritative_lore_flags": "/lore/flags",
    "sim_observed_counters": "/sim/counters"
  },
  "lore_json": { "lore": { "flags": { "alpha": { "value": true, "source_tick": 1 } } } },
  "sim_json": { "sim": { "counters": { "alpha": { "count": "not-a-number", "last_tick": 1 } } } },
  "golden_expectations": {
    "outcome": "INVALID_EMG2_SLICE",
    "reason_code": "TYPE_MISMATCH"
  }
}
```

**F2 — `BELOW_FLOOR` (valid slice, score under F):**

```json
{
  "emg2_gate_version_id": "EMG2_ALIGNMENT_GATE_V0",
  "emg2_alignment_floor_version": "emg2-F-v0",
  "emg2_alignment_floor_F": 85,
  "canonicalization_version": "none",
  "tier": "A",
  "pointers": {
    "authoritative_lore_flags": "/lore/flags",
    "sim_observed_counters": "/sim/counters"
  },
  "lore_json": { "lore": { "flags": { "x": { "value": true, "source_tick": 1 } } } },
  "sim_json": { "sim": { "counters": { "x": { "count": 0, "last_tick": 1 } } } },
  "golden_expectations": {
    "outcome": "BELOW_FLOOR",
    "score_max": 70
  }
}
```

## 3. Fixture ID conventions (G / F parity with 2.2.3)

Within `fixtures/emg2_alignment/v0/`:

| ID | Intent (parallel to 2.2.3) |
| --- | --- |
| **G1–G3** | Happy path: valid pointers, matching shapes, scores **≥ `F`** with documented margin (e.g. G1 well above F, G2 near F but still ≥ F, G3 stress on weighted agreement) |
| **F1–F2** (extend to **F3** if needed) | Boundary / denial: `INVALID_EMG2_SLICE` (bad pointer, type mismatch, forbidden duplicate keys), `BELOW_FLOOR` (valid slice but score `< F`) |

**Naming:** `G1.json` … `G3.json`, `F1.json` … under the EMG root — avoids renaming 2.2.3’s own G1–G3 while preserving **mental model** for reviewers.

Optional: prefix filenames with `emg2-` only if tooling requires global uniqueness; directory scoping usually suffices.

### Evidence / VCS boundary (decisions-log)

Per [[1-Projects/genesis-mythos-master/Roadmap/decisions-log]]:

- **D-020:** Fixture-root + CI gate for IntentPlan replay is **adopted** as policy; implementation timing is a **backlog** concern.
- **D-021:** **G-P2.2-CI** means policy + golden definitions are **normatively closed** in the Phase 2.2.3 note — **not** that CI has necessarily run in this repo’s VCS yet (fixtures/workflow backlog called out in rollup open risks).
- **D-022:** EMG metric adoption row stays **stub** until EMG-2 **F** and registry evidence are frozen; traceability until then is via phase notes.
- **D-024:** EMG-2 pointer + `AlignmentFn_v0` draft is **normative in vault**; **not frozen for CI** until registry row exists and `emg2_floor_F_status` → `frozen`.

This synthesis describes **target** harness + fixture shapes for **2.3.3**; it does **not** claim a specific `.github/workflows/*.yml` job already executes `AlignAndVerify` — wire-up is a follow-on engineering task once vectors land under VCS.

## 4. CI job contract (minimum pseudo)

**Names:** `CI_Emg2AlignmentSuite` and `AlignAndVerify` are **suggested** identifiers for Phase 2.3.3 documentation — they are **not** claimed to exist as symbols in application code until implemented.

```pseudo
procedure CI_Emg2AlignmentSuite():
  floor := LoadProjectFloor("emg2_alignment_floor_F")  // from locked config or vector pin
  for vector in RegistryList(glob="fixtures/emg2_alignment/v0/*.json"):
    out := AlignAndVerify(vector.lore_json, vector.sim_json, vector.pointers, vector.tier)
    assert out matches vector.golden_expectations
    assert vector.emg2_gate_version_id == harness.EMG2_ALIGNMENT_GATE_V0
```

**Triggers (suggested):** any change to `AlignmentFn_v0`, pointer registry, `emg2_alignment_floor_F` / version, lore/sim shape pseudo-code, or harness compare rules.

## 5. PR-review golden refresh policy (inherit 2.2.3)

Mirror Phase 2.2.3 § Promotion policy (same mechanics as `intent_replay`; this repo’s normative wording is in the phase note, not in external blogs):

1. Local `RECORD_GOLDEN=1` (or EMG-specific flag) **only** for intentional semantic changes.
2. PR bundles: **code + golden JSON** + **version bump** (`EMG2_ALIGNMENT_GATE_V0` or `emg2_alignment_floor_version`) **or** waiver tied to [[decisions-log]] id.
3. CODEOWNERS on `fixtures/emg2_alignment/**` (second pair of eyes on score changes).
4. **No auto-refresh in CI** — failure is the default; drift is always a human-reviewed commit.

**Background reading (non-repo proof):** [Golden File Testing: Output Comparison](https://www.application-architect.com/posts/golden-file-testing-output-comparison/) — industry pattern for treating golden updates as reviewed behavioral changes.

## 6. Bounded worst-acceptable fixture matrix (for calibrating `F`)

**Goal:** Choose `emg2_alignment_floor_F` such that all **product-required** “still acceptable” alignment cases remain **≥ F**, while **F1–F2** vectors prove the harness rejects bad slices and sub-threshold scores.

**Dimensions (rows — cap for boundedness):** pick a small orthogonal set, e.g.:

| Row label | Stress |
| --- | --- |
| WA-1 | Max allowed key mismatch under product rules |
| WA-2 | Worst allowed counter lag / tick skew (still valid) |
| WA-3 | Minimal acceptable overlap (still not `INVALID`) |
| WA-4 | **At-threshold** acceptable score (defines **F**) |
| X-1 | Must be `BELOW_FLOOR` (score `< F`) |
| X-2 | Must be `INVALID_EMG2_SLICE` |

**Procedure:**

1. Author **WA-*** rows as **passing** golden vectors (expected `OK`, score in `[F, 100]`).
2. Author **X-*** rows as **failing** golden vectors (expected `BELOW_FLOOR` or `INVALID`).
3. Run oracle + harness; if any WA row fails while product says it should pass → **lower F** *or* **tighten shapes** (2.3.2 prefers shape tighten over lowering F).
4. Set `emg2_floor_F_status: frozen` only when matrix is stable and **registry row** is added to Phase 2.2.3 note (cross-link) or a 2.3.3 subsection lists the EMG rows explicitly.

**Hypothesis / PBT note:** Threshold-style properties can shrink to “barely past” examples; use **explicit** WA-4 at-threshold fixtures rather than relying on PBT alone for the numeric floor. See [Hypothesis — The Threshold Problem](https://hypothesis.works/articles/threshold-problem/).

## 7. Closing gap: registry row in Phase 2.2.3 note

When `fixture IDs land in VCS`, add a **table row** (or subsection) to Phase 2.2.3’s golden artifact registry pointing to `fixtures/emg2_alignment/v0/` and listing `EMG2_ALIGNMENT_GATE_V0` — satisfies 2.3.2 handoff gap *“Registry row … for EMG-2 alignment still absent”*.

## Raw sources (vault)

- [[phase-2-2-3-ci-golden-registry-and-boundary-regression-gates-roadmap-2026-03-21-1205]] — `DETERMINISTIC_GATE_V1`, `fixtures/intent_replay/v0/`, G1–G3 / F1–F2, `RECORD_GOLDEN`, CODEOWNERS path, CI failure semantics.
- [[phase-2-3-2-emg-2-floor-frozen-json-pointers-and-alignmentfn-v0-roadmap-2026-03-21-2245]] — `emg2_alignment_floor_F`, `AlignmentFn_v0`, pointer table, `INVALID_EMG2_SLICE` / `BELOW_FLOOR`, calibration steps.

## Sources (external, background)

- [Golden File Testing: Output Comparison | Application Architect](https://www.application-architect.com/posts/golden-file-testing-output-comparison/)
- [Hypothesis — The Threshold Problem](https://hypothesis.works/articles/threshold-problem/)
