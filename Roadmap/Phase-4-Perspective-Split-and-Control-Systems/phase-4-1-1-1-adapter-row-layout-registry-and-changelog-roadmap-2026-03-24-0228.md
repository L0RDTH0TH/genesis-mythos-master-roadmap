---
title: Phase 4.1.1.1 — Adapter row layout registry and D-032 changelog hooks
roadmap-level: task
phase-number: 4
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-24
tags: [roadmap, genesis-mythos-master, phase-4, perspective, adapter, task, t-p4-01]
para-type: Project
subphase-index: "4.1.1.1"
handoff_readiness: 92
handoff_readiness_scope: "Quaternary task — versioned adapter_row_layout_id registry row + explicit D-032 clearance changelog fields; no CI golden until literals freeze"
execution_handoff_readiness: 30
handoff_gaps:
  - "**D-032 / D-043:** Literal replay columns still **TBD** — registry stores **intent-only** column ids until freeze."
  - "**G-P*.*-REGISTRY-CI HOLD** unchanged — presentation registry rows are **vault-normative** only."
links:
  - "[[phase-4-1-1-adapter-preimage-and-stable-column-layout-roadmap-2026-03-24-0018]]"
  - "[[phase-4-1-player-first-perspective-read-model-and-rig-contracts-roadmap-2026-03-24-1201]]"
  - "[[Ingest/Agent-Research/phase-4-1-1-adapter-preimage-stable-layout-cqrs-research-2026-03-23-2205]]"
  - "[[decisions-log]]"
---

## Phase 4.1.1.1 — Adapter row layout registry (task)

**Parent tertiary:** [[phase-4-1-1-adapter-preimage-and-stable-column-layout-roadmap-2026-03-24-0018]] (**T-P4-01** continuation).

**Mint:** queue **`resume-deepen-post-recal-p4-1-1-gmm-20260324T021500Z`** after post–**4.1.1** **recal** (`resume-recal-post-p4-1-1-deepen-gmm-20260324T002000Z`) and Layer-1 compare **`.technical/Validator/roadmap-handoff-auto-genesis-mythos-master-20260324T020000Z-layer1-post-deepen-001800Z.md`** (rollup **HR 92** vs **`min_handoff_conf` 93** + **REGISTRY-CI HOLD** vault-honest).

**Continuation (2026-03-24):** queue **`resume-deepen-post-handoff-audit-recal-gmm-20260324T021630Z`** after **`resume-recal-post-handoff-audit-cursor-repair-gmm-20260324T021600Z`** — deepen **4.1.1.1** adapter registry / **D-032** changelog spine only; **rollup HR 92 < 93** and **G-P*.*-REGISTRY-CI HOLD** unchanged unless repo evidence; **do not** re-open **D-044** / **D-059** operator picks (per queue `user_guidance`).

### TL;DR

- Introduce **`adapter_row_layout_id`** as a **versioned** selector over the normative adapter columns on **4.1.1**; bind breaking changes to **`replay_row_version`** (**3.1.1**) on operator freeze.
- **`D-032` clearance changelog** (vault table): list added/renamed columns, new golden **Lane-C** rows (**`@skipUntil` removal**), and **`TickCommitRecord_v0`** field alignment — **no** repo path assertions (**D-058 SCOPED_VAULT** pattern for package paths).

### Registry row sketch (vault-normative)

| Field | Type / role |
|-------|-------------|
| `adapter_row_layout_id` | Monotonic string id (e.g. `ADAPTER_ROW_LAYOUT_V0`) |
| `compatible_replay_row_version_min` | Ties to **3.1.1** stub when literals exist |
| `serialization_profile_allow_list` | Subset of **`serialization_profile_id`** values (**D-037** intent) |
| `normative_columns` | Ordered list matching **4.1.1** preimage table |
| `lane_c_skip_tags` | e.g. `fov_lod_parameters @skipUntil(D-032)` |

### Pseudo-code — register + validate layout

```text
// CANONICAL_ADAPTER_COLUMNS_V0 := ordered normative names from [[phase-4-1-1-adapter-preimage-and-stable-column-layout-roadmap-2026-03-24-0018]] § Preimage authority table:
//   tick_id | post_apply_observable_root | serialization_profile_id | presentation_stable_inputs | camera_binding_id | fov_lod_parameters
// Literal replay binding @skipUntil(D-032/D-043); table text is vault authority until freeze.

function RegisterAdapterRowLayout(layout: AdapterRowLayoutSpec_v0) -> layout_id:
  assert layout.normative_columns == CANONICAL_ADAPTER_COLUMNS_V0  // no silent rename vs 4.1.1 table
  assert layout.lane_c_skip_tags is subsetof AllowedSkipTags(D-032, D-043, D-045)
  commit vault registry row // not repo fixture until operator promotes
  return layout.adapter_row_layout_id

function ValidateAdapterRowAgainstLayout(row: AdapterRow_v0, layout_id: string) -> Result:
  layout = LookupLayout(layout_id)
  if row.replay_row_version < layout.compatible_replay_row_version_min:
    return Err(REPLAY_ROW_VERSION_MISMATCH)
  if row.serialization_profile_id not in layout.serialization_profile_allow_list:
    return Err(PROFILE_NOT_ALLOWED_FOR_LAYOUT)
  return Ok()
```

### Edge cases

- **Profile hash drift:** If **`serialization_profile_id`** changes without a new **`adapter_row_layout_id`**, replay hashes may diverge — treat as **breaking** and bump layout id.
- **Regen read path:** Adapter **read** order must not invent a second total order vs **RegenLaneTotalOrder_v0** (**D-044** Option A); presentation remains **downstream** of committed bundles only.

### D-032 clearance changelog (vault table stub)

Vault-normative rows only (**D-058 SCOPED_VAULT** — no package path assertions). Until **SimulationRunControl** / replay header literals freeze, keep cells as **intent ids** or **`@skipUntil(D-032)`**.

| Changelog field | Intent (until literal freeze) |
| --- | --- |
| `layout_id` | **`adapter_row_layout_id`** monotonic id |
| `normative_columns_delta` | Added / renamed column ids vs prior layout (empty if none) |
| `lane_c_delta` | New **Lane-C** golden row ids + **`@skipUntil` removals** |
| `tick_commit_record_delta` | **`TickCommitRecord_v0`** field ids added/renamed/removed |
| `replay_row_version_bump` | Link to **3.1.1** stub when **`compatible_replay_row_version_min`** advances |

### Acceptance criteria (junior handoff)

1. **Registry:** One vault row exists for **`ADAPTER_ROW_LAYOUT_V0`** (or next id) with **`normative_columns`** order **byte-identical** to [[phase-4-1-1-adapter-preimage-and-stable-column-layout-roadmap-2026-03-24-0018]] preimage table (no silent rename).
2. **Validation:** **`ValidateAdapterRowAgainstLayout`** returns **`Err(PROFILE_NOT_ALLOWED_FOR_LAYOUT)`** when profile ∉ allow-list; **`Err(REPLAY_ROW_VERSION_MISMATCH)`** when row version < min.
3. **Changelog:** **D-032** table section above filled or explicitly **`@skipUntil(D-032)`** with operator ticket id — **no** fabricated CI green.
4. **Fork safety:** Text does not assert **HR ≥ `min_handoff_conf` 93** or **REGISTRY-CI PASS**; rollup remains **92 < 93** until **2.2.3** / **D-020** evidence.

### Compare-final mirror — `missing_acceptance_criteria` ↔ open `normative_columns` task

**Target validator codes (post–`resume-recal-post-deepen-handoff-audit-gmm-20260324T021700Z`):** nested compare-final **`.technical/Validator/roadmap-handoff-auto-genesis-mythos-master-20260324T041500Z.md`** listed **`missing_acceptance_criteria`** alongside rollup / safety codes — this section **does not** clear **`missing_roll_up_gates`** or **REGISTRY-CI HOLD**; it only **binds** junior verification to the **first unchecked** task under **Tasks** (mirror **`normative_columns`** → **3.1.1** stub).

| Acceptance criterion (above) | Junior verifier action (vault-honest) | Blocked until |
| --- | --- | --- |
| **AC1** registry row + byte-identical column order vs [[phase-4-1-1-adapter-preimage-and-stable-column-layout-roadmap-2026-03-24-0018]] preimage table | Diff **ordered** `normative_columns` list vs **§ Preimage authority table** (five names); if **ADAPTER_ROW_LAYOUT_V0** row missing, document **`DEFER`** + **`@skipUntil(D-032/D-043)`** in registry status (already stated below). | Literal replay columns + operator freeze |
| **AC2** `ValidateAdapterRowAgainstLayout` error paths | Sketch **two** negative fixtures in vault prose only: (a) profile ∉ allow-list → **`Err(PROFILE_NOT_ALLOWED_FOR_LAYOUT)`**; (b) `replay_row_version` < min → **`Err(REPLAY_ROW_VERSION_MISMATCH)`** — **no** repo path or CI green claim. | Same |
| **AC3** D-032 changelog table | Either fill intent rows or keep cells **`@skipUntil(D-032)`** with operator ticket id; **no** fabricated Lane-C green. | **SimulationRunControl** / replay header freeze |
| **AC4** fork safety | Re-read **Roll-up literacy** + **Non-goals**; confirm no sentence implies **HR ≥ 93** or **REGISTRY-CI PASS** from vault alone. | **2.2.3** / **D-020** evidence |

**Mirror task checklist (maps to Tasks → first checkbox):**

1. Open [[phase-3-1-1-deterministic-tick-epoch-and-hash-preimage-boundaries-roadmap-2026-03-22-0015]] (or current **3.1.1** canonical path) replay-row / preimage note; copy **canonical column id list** into a **scratch alignment block** (vault-only) that lists the same five ids in the same order as **4.1.1** preimage table.
2. When **3.1.1** stub updates, re-diff ordered list; on any drift, **do not** check the mirror task — file a **single-line** decision note under [[decisions-log]] referencing **D-032** / **D-043** (no **D-044** / **D-059** operator pick churn per queue `user_guidance`).

### Roll-up literacy (post–handoff-audit recal)

- **Phase 3.* / Phase 4 rollups:** **`handoff_readiness` 92** vs **`min_handoff_conf` 93** remains **below bar** while **G-P*.*-REGISTRY-CI** is **HOLD** — consistent with [[decisions-log]] and [[roadmap-state]] **Operator decision visibility**.
- This note stays **tertiary spine** **4.1.1.1**; latest **`## Log`** deepen for **4.1** secondary WBS may differ — use [[workflow_state]] **`workflow_log_authority: last_table_row`** + **`current_subphase_index`**.

### Authoritative cursor pointer (state sync)

- **Authoritative subphase after handoff-audit repair:** **`4.1.1.1`** (not `4.1.1.5` / `4.1.1.6`), aligned to [[workflow_state]] frontmatter **`current_subphase_index`** and [[roadmap-state]] Phase 4 machine-cursor sentence.
- **Authoritative iteration id for this reconciliation:** **`resume-deepen-post-recal-d060-021700z-gmm-20260324T021800Z`**.
- This pointer resolves cursor ambiguity only; it does **not** clear **`missing_roll_up_gates`**, does **not** claim **HR >= 93**, and does **not** clear **REGISTRY-CI HOLD**.

### Tasks

- [ ] Mirror **`normative_columns`** to **3.1.1** stub row when **3.1.1** note updates (no orphan renames) — `@skipUntil(D-032/D-043, literal replay columns + replay_row_version freeze)`
- [ ] Draft **`D-032` clearance changelog** section on **4.1.1** parent when operator freezes header literals (empty stub OK until then) — `@skipUntil(D-032, SimulationRunControl/replay header operator freeze)`
- [ ] Link forward to **4.1.2** rig consume order when **T-P4-02** tertiary mints — `@skipUntil(4.1.1.x gate, roll-up gate row PASS on secondary 4.1)`
- [x] Link forward to follow-on quaternary consume-order contract: [[phase-4-1-1-2-adapter-registry-consumption-order-and-lane-c-delta-gates-roadmap-2026-03-24-0421]] (queue `resume-deepen-p4-1-1-1-post-handoff-hygiene-gmm-20260324T042100Z`)

### Validator traceability (first nested pass — 2026-03-24)

Nested **`roadmap_handoff_auto`**: `.technical/Validator/roadmap-handoff-auto-genesis-mythos-master-20260324T041500Z.md` — **`severity: medium`**, **`recommended_action: needs_work`**, **`primary_code: missing_roll_up_gates`**, **`reason_codes`**: `missing_roll_up_gates`, `missing_acceptance_criteria`, `safety_unknown_gap`. Prior **`repair-handoff-audit-layer1-post-lv-gmm-20260324T031600Z`** fixed **[[roadmap-state]]** Notes vs **YAML** vs terminal **`## Log`** **`021630Z`** dual-truth only — **macro rollup HR 92 < 93** and **G-P*.*-REGISTRY-CI HOLD** remain without repo evidence. **IRA:** `.technical/Internal-Repair-Agent/roadmap/2026-03/genesis-mythos-master-ira-call-1-validator-handoff-auto-20260324T041500Z.md`.

**Continuation (queue `resume-deepen-post-recal-d060-021700z-gmm-20260324T021800Z`, telemetry `pr-eatq-20260323-gmm-001`):** Added **§ Compare-final mirror — `missing_acceptance_criteria` ↔ open `normative_columns` task** so **`missing_acceptance_criteria`** has an explicit **AC1–AC4 → verifier** mapping and **3.1.1** mirror steps — **rollup / REGISTRY-CI machine codes unchanged** by design.

#### Drift scalar contract (read-only)

Per [[roadmap-state]] Notes **`qualitative_audit_v0`**: **`drift_score_last_recal`** / **`handoff_drift_last_recal`** are qualitative judgments — **not** numerically comparable across audits without a versioned drift spec + input hash ([[drift-spec-qualitative-audit-v0]]).

### Registry row status (vault-honest)

**`ADAPTER_ROW_LAYOUT_V0`** is **not** minted as a byte-identical vault row yet — **DEFER** until **D-032** / **D-043** literal replay freeze + **4.1.1** preimage column order lock with operator sign-off. **Do not** assert **REGISTRY-CI PASS** or rollup **HR ≥ 93** from vault prose alone.

### Non-goals (macro)

This quaternary slice **cannot** clear **`missing_roll_up_gates`** for Phase **3.* rollups** — authority remains on **3.2.4** / **3.3.4** / **3.4.4** rollup notes + [[decisions-log]] **D-046** / **D-050** / **D-055** + [[roadmap-state]] rollup index.

### Upward links

- **Tertiary:** [[phase-4-1-1-adapter-preimage-and-stable-column-layout-roadmap-2026-03-24-0018]]
- **Secondary:** [[phase-4-1-player-first-perspective-read-model-and-rig-contracts-roadmap-2026-03-24-1201]]

### Downstream continuation

- [[phase-4-1-1-2-adapter-registry-consumption-order-and-lane-c-delta-gates-roadmap-2026-03-24-0421]]
