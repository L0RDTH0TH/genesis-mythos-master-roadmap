---
title: Phase 2.3.4 — EMG-2 execution closure (VCS promotion + floor freeze)
roadmap-level: tertiary
phase-number: 2
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-21
tags: [roadmap, genesis-mythos-master, phase, EMG-2, CI, execution-closure, golden-fixtures]
para-type: Project
subphase-index: "2.3.4"
emg2_execution_closure_status: "open — PR tranche + WA log + registry row co-materialization"
handoff_readiness: 93
normative_handoff_readiness: 93
execution_handoff_readiness: 66
handoff_readiness_scope: "single-tranche checklist tying fixtures PR, workflow paths/CODEOWNERS, WA-1..4 log closure, wiki G-EMG2 row, and D-024 freeze flip"
handoff_gaps:
  - "No green CI proof until `AlignAndVerify` runs on merged vectors under `fixtures/emg2_alignment/v0/`"
  - "WA matrix execution log in [[phase-2-3-3-emg-2-ci-golden-registry-row-and-fixture-hardening-roadmap-2026-03-21-2249]] must transition NOT RUN → PASS/FAIL with evidence before `emg2_floor_F_status: frozen`"
links:
  - "[[phase-2-procedural-generation-and-world-building-roadmap-2026-03-19-1101]]"
  - "[[phase-2-3-3-emg-2-ci-golden-registry-row-and-fixture-hardening-roadmap-2026-03-21-2249]]"
  - "[[phase-2-3-2-emg-2-floor-frozen-json-pointers-and-alignmentfn-v0-roadmap-2026-03-21-2245]]"
  - "[[phase-2-2-3-ci-golden-registry-and-boundary-regression-gates-roadmap-2026-03-21-1205]]"
  - "[[decisions-log]]"
---

## Phase 2.3.4 — EMG-2 **execution closure** (VCS promotion + **F** freeze)

> [!warning] Normative vs execution
> This tertiary is the **execution bridge** for everything **2.3.3** drafted: registry row shape, `AlignAndVerify`, and WA matrix **exist in vault**; **execution_handoff_readiness** stays **below normative** until a merged PR carries fixtures + workflow + populated WA log rows.

**Mid-technical (depth 3):** PR tranche boundaries, CI `paths` / optional `dorny/paths-filter`, CODEOWNERS split, and a **single merge policy** so wiki **G-EMG2-*** rows never ship without repo paths.

### Single-tranche merge policy (v0)

1. **Branch** adds `fixtures/emg2_alignment/v0/{G1,F1,F2}.json` (or agreed stems) validating against the row schema in **2.3.3**.
2. **Workflow** job scoped with `on.push.paths` / `paths-ignore` covering `fixtures/emg2_alignment/**`, shared verifier paths, and (when needed) gate-version constants so cross-cutting edits still run **both** EMG-2 and intent-replay lanes where required.
3. **CODEOWNERS** assigns disjoint owners for `fixtures/emg2_alignment/` vs `fixtures/intent_replay/` plus an owner line for `.github/CODEOWNERS` itself.
4. **WA matrix** rows in **2.3.3** are filled with **expected vs actual** for WA-1…WA-4; failures block `emg2_floor_F_status: frozen` on **2.3.2**.
5. **Wiki registry** ([[phase-2-2-3-ci-golden-registry-and-boundary-regression-gates-roadmap-2026-03-21-1205]]) gains **G-EMG2-ALIGN** (or agreed id) **in the same PR** as fixture files (no orphan wiki row).
6. **Decisions** — update **D-024** / **D-025** / **D-026** status lines when **F** is frozen and wiki row is non-TBD.

### CI wiring pseudo-code (repo-local)

```pseudo
on:
  push:
    paths:
      - "fixtures/emg2_alignment/**"
      - "tools/align_verify/**"        # example shared harness root
      - ".github/workflows/emg2-alignment.yml"
jobs:
  align_and_verify:
    steps:
      - run: AlignAndVerify --glob "fixtures/emg2_alignment/v0/*.json"
```

### Promotion gate (maps to research checklist)

| Gate | Evidence |
| --- | --- |
| Schema + enum parity | JSON validates; `golden_expectations` / `reason_code` match harness table in **2.3.3** |
| Determinism | Tier-C policy explicit; normalized `AlignmentOutcome` compared in harness |
| WA closure | WA-1…WA-4 logged with PASS/FAIL + notes |
| Version pins | `emg2_gate_version_id`, `emg2_alignment_floor_version`, numeric **F** consistent across fixtures + **2.3.2** frontmatter |
| Status flip | `emg2_floor_F_status: frozen` only after WA + pins + green CI |

## Research integration

### Key takeaways

- Treat **`fixtures/emg2_alignment/v0/`** as its own CODEOWNERS + `on.<event>.paths` scope beside **`fixtures/intent_replay/v0/`**, and include shared verifier/schema paths so cross-cutting gate bumps still run both lanes when needed.
- Anchor CI path behavior on **GitHub Actions workflow syntax** (`paths` / `paths-ignore`); use **`dorny/paths-filter`** when you need named filters and conditional jobs; third-party blog posts are illustrative only.
- **Promotion to frozen floor F:** close schema + enum parity, run and log **WA-1…WA-4**, align `emg2_gate_version_id` / `emg2_alignment_floor_version` / numeric **F** across fixtures and [[phase-2-3-2-emg-2-floor-frozen-json-pointers-and-alignmentfn-v0-roadmap-2026-03-21-2245]], then flip `emg2_floor_F_status: frozen` and fill the **G-EMG2-*** wiki row with real repo paths in the same tranche as the first merged fixture PR.

### Decisions / constraints

- **CODEOWNERS:** last matching pattern wins; file is case-sensitive; put `.github/CODEOWNERS` and assign an owner to that file; owners need write access (GitHub Docs).
- **Fixture layout framing:** the **two-root split** is **vault-defined** (2.3.3); external docs do not redefine the split.
- **Registry parity:** each wiki row should carry immutable vector id, repo-relative path, phase wiki-links (2.3.3 implementation + 2.2.3 rollup), and CI job proof when available.

### Links

- Synthesis: [[Ingest/Agent-Research/phase-2-3-4-emg2-execution-closure-genesis-mythos-master-2026-03-21-2230]]
- Upstream wiring note: [[phase-2-3-3-emg-2-ci-golden-registry-row-and-fixture-hardening-roadmap-2026-03-21-2249]]

## Tasks

**PR / VCS (evidence required)**

- [ ] Land `fixtures/emg2_alignment/v0/*.json` + `AlignAndVerify` entrypoint per **2.3.3** pseudo-code.
- [ ] Add workflow YAML with path filters + optional `dorny/paths-filter` for monorepo fan-out.
- [ ] Update CODEOWNERS for EMG-2 vs intent-replay roots + `.github/CODEOWNERS` owner line.
- [ ] Execute WA-1…WA-4; mirror results into **2.3.3** WA log table.
- [ ] Append **G-EMG2-*** row in Phase **2.2.3** note with concrete repo paths.
- [ ] Flip `emg2_floor_F_status` to **frozen** on **2.3.2** when gates close; patch [[decisions-log]] **D-024**/**D-025**/**D-026**.

**Vault-follow (no VCS)**

- [x] Linked from [[distilled-core]] (`core_decisions` + Phase 2.3 body) and [[roadmap-state]] **Notes** / **Consistency reports** lineage for this deepen run (`version: 14`).
