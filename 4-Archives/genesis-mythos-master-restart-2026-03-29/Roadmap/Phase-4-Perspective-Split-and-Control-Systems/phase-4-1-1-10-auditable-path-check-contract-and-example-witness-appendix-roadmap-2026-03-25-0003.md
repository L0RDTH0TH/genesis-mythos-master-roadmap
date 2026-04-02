---
title: Phase 4.1.1.10 - Auditable path check contract and example witness appendix
roadmap-level: task
phase-number: 4
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-25
tags: [roadmap, genesis-mythos-master, phase-4, perspective, adapter, task, t-p4-01]
para-type: Project
subphase-index: "4.1.1.10"
handoff_readiness: 91
handoff_readiness_scope: "IsAuditablePath_v0 + AppendWitness_v0 + WitnessRefHash_v0 JSON preimage shape + witness_appended/witness_skipped ledger literals; vault **stub** row for H_canonical registry slot (algorithm DEFERRED) + repo-side acceptance envelope per compare-final next_artifacts — still **no** rollup HR≥93, REGISTRY-CI PASS, or checked-in harness; 2026-03-25 23:45Z RESUME_ROADMAP deepen queue followup-deepen-post-recal-distilled-parity-gmm-20260325T213400Z after `.technical/Validator/roadmap-auto-validation-genesis-mythos-master-20260325T213200Z-recal-post-distilled-parity-compare-final.md`"
execution_handoff_readiness: 31
handoff_gaps:
  - "**G-P*.*-REGISTRY-CI HOLD** remains until 2.2.3 / D-020 execution evidence."
  - "EXAMPLE witness row is **non-normative** until operator promotes to golden / closure table row with auditable path."
  - "Path checks are vault-relative string ops only — no substitute for Lane-C **ReplayAndVerify** (**@skipUntil(D-032)**)."
  - "`WitnessRefHash_v0`: **JSON preimage field-order v0** + **ledger event name literals** are now sketched in-body; `H_canonical` is fixed **by v0 policy exception** (**SHA256(UTF8(JSON_SER_ORDERED(w)))**) for determinism tests only — **registry row + repo emission + CI remain deferred** (still no rollup PASS)."
links:
  - "[[distilled-core]]"
  - "[[workflow_state]]"
  - "[[roadmap-state]]"
  - "[[phase-4-1-1-9-bundle-verification-witness-and-rollback-runbook-roadmap-2026-03-24-2304]]"
  - "[[phase-4-1-1-7-adapter-registry-rollup-handoff-bundle-and-closure-map-roadmap-2026-03-24-0926]]"
  - "[[phase-4-1-1-adapter-preimage-and-stable-column-layout-roadmap-2026-03-24-0018]]"
  - "[[decisions-log]]"
  - "[[genesis-mythos-master-roadmap-moc]]"
---

## Phase 4.1.1.10 - Auditable path check contract and example witness appendix

**Parent chain:** [[phase-4-1-1-9-bundle-verification-witness-and-rollback-runbook-roadmap-2026-03-24-2304]] → [[phase-4-1-1-7-adapter-registry-rollup-handoff-bundle-and-closure-map-roadmap-2026-03-24-0926]] → [[phase-4-1-1-adapter-preimage-and-stable-column-layout-roadmap-2026-03-24-0018]]

**Queue / validator trace:** Follow-up to nested **`roadmap_handoff_auto`** pass2 **`.technical/Validator/validator-roadmap_handoff_auto-genesis-mythos-master-20260325T013000Z-pass2-post-ira.md`** — tightens **`safety_unknown_gap`** on prose-only **`IsAuditablePath`** and uninstantiated witness machinery (**`missing_roll_up_gates`** / rollup honesty unchanged).

### TL;DR

- Defines **`IsAuditablePath_v0`** as a **checkable** vault-relative contract (inputs, outputs, failure classes) consumable by **4.1.1.9** rollback runbook step 1.
- Defines **`AppendWitness_v0`** + **closure_table** binding vocabulary (events ↔ cells) — **no** rollup PASS implication.
- Adds **Witness appendix** (ordered artifacts) + **one** **EXAMPLE** **`EvidenceWitnessRow_v0`** (vault-honest: labeled example, not CI PASS).
- **Does not** assert **rollup HR ≥ 93**, **REGISTRY-CI PASS**, or green harness.

> [!important] Machine authority (as-of 2026-03-26 19:05Z — post forward-map deepen)
> - **Canonical machine cursor:** `last_auto_iteration` **`resume-forward-map-phase-41110-gmm-20260326T180000Z`**, **`current_subphase_index` `4.1.1.10`** — authoritative source is [[workflow_state]] YAML + first physical **`deepen`** row in **`## Log`** (not narrative repair rows below it).
> - **Historical prior terminal deepen:** **`resume-deepen-post-recal-distilled-yaml-gmm-20260326T041500Z-followup`** (**2026-03-26 12:30Z**, Layer-1 vs mirrors parity deepen) — **superseded** by **19:05Z** forward-map deepen above.
> - **Historical prior deepen:** **`followup-deepen-post-recal-distilled-parity-gmm-20260325T213400Z`** (**23:45 UTC**, **`H_canonical` stub + repo envelope**) — **superseded** by **04:08Z** **`040820Z`** mapping; **then** superseded by **12:30Z** follow-up above.
> - **Historical shallow deepen:** **`resume-deepen-post-recal-antispin-followup-gmm-20260325T193000Z`** (**04:55 UTC**, **RollUpGateChecklist_v0** / **D-072**) remains **audit / narrative** context — **not** the live terminal id after **12:30Z** follow-up.
> - **Archival skimmer rule:** older threads citing **D-073** / **`eatq-antispin-obs-test-gmm-20260325T180000Z`** as *present-tense terminal* without **193000Z** / **213400Z** / **040820Z** / **041500Z-followup** supersession labels are **historical audit context** only.

### Task decomposition (execution) — open WBS (vault-honest)

| Id | Work unit | Observable pass (does **not** clear rollup HR<93 or REGISTRY-CI HOLD) | Owner / queue id |
| --- | --- | --- | --- |
| **WBS-41110-01** | Finalize **`NormalizeVaultPath_v0`** vs stub pseudo block | Deterministic strip/bracket rules written; alias/case explicitly **not resolved in v0** (handled elsewhere; no implied closure) | **Owner:** `ROLE:path-normalization` · **Proposed queue_entry_id:** `wbs-41110-01-normalizevaultpath-v0-gmm-20260326T000000Z` |
| **WBS-41110-02** | **`H_canonical`** registry row + fixture path | Row names hash profile + links to **checked-in** or **vault-stub** fixture path (no PASS claim) | **Owner:** `ROLE:registry-ci` · **Proposed queue_entry_id:** `wbs-41110-02-h-canonical-registry-row-fixture-path-gmm-20260326T000000Z` |
| **WBS-41110-03** | Lane-C **`ReplayAndVerify`** or **`@skipUntil(D-032)`** unblock plan | Named owner + dependency steps + queue id; no green CI assertion | **Owner:** `ROLE:lane-c-harness` · **Proposed queue_entry_id:** `wbs-41110-03-lane-c-replayandverify-unblock-gmm-20260326T000000Z` |

**Why these placeholders exist (and what they bind to):** This is a **structure-only** deepen requested by queue `followup-deepen-post-handoff-audit-antispin-missing-rollup-gmm-20260325T232500Z` to satisfy the Validator’s **`next_artifacts`** instruction “replace `TBD / queue placeholder` in WBS rows.”  
**Cited validator (next_artifacts anchor):** `.technical/Validator/roadmap-auto-validation-genesis-mythos-master-20260325T214500Z-handoff-audit-post-antispin-layer2-compare-final-vs-live-yaml-fix.md` (see **`next_artifacts`** item **6**).

#### RollUpGateChecklist_v0 mapping (WBS → OPEN/HOLD rows)

- **WBS-41110-01 → `missing_acceptance_criteria` (OPEN)**: ensure `NormalizeVaultPath_v0` is a bounded, checkable v0 algorithm (alias/case remain intentionally out-of-scope; no implied closure).
- **WBS-41110-02 → `H_canonical + registry row + fixture path` (OPEN)**: advance from “vault stub slot definition” to a concrete **registry-row** plan + **fixture path** plan (still **no** claim of repo existence / PASS).
- **WBS-41110-03 → `REGISTRY-CI HOLD` / Lane‑C harness (HOLD / OPEN)**: explicitly name an owner lane and a queue id for the **ReplayAndVerify** unblock plan or a scoped **`@skipUntil(D-032)`** bridge (still **no** green CI assertion).

### IsAuditablePath_v0 (checkable sketch)

**Inputs:** `proposed_target: string` (Obsidian wikilink target or vault-relative `.md` path after normalizing `[[` `]]`).

**Output:** `AuditablePathVerdict_v0` enum:

- `OK` — path resolves to an existing note under allowed PARA roots (`1-Projects/`, `2-Areas/`, `3-Resources/`, `4-Archives/`, `Ingest/`, `5-Attachments/` as linked target only).
- `MISSING` — normalized path has no file in vault.
- `MOVED_OR_AMBIGUOUS` — path fragment matches multiple candidates or alias collision (operator resolution required).
- `OUT_OF_SCOPE` — path points outside PARA / Ingest / Attachments allow-list (e.g. raw URL-only with no vault note).

> [!note] Scope note — `NormalizeVaultPath_v0` is **only** bounded string normalization (trim + one outer `[[ ]]` strip). Alias resolution and case policy remain out-of-scope for v0; this note does not claim repo-side resolution or CI closure.

```text
function NormalizeVaultPath(proposed_target: string) -> string:
  // v0 = deterministic string normalization only (no alias/case resolution)
  s = TrimUnicodeWhitespace(proposed_target)
  if s startsWith "[[" and s endsWith "]]":
    s = s.substring(2, len(s)-2)  // strip outermost once
  s = TrimUnicodeWhitespace(s)
  if s == "":
    return ""
  // If nested brackets remain after one strip, treat as non-canonical input.
  // v0 does not attempt recursive parsing; downstream existence check will likely fail.
  return s

function IsAuditablePath_v0(proposed_target: string) -> AuditablePathVerdict_v0:
  p = NormalizeVaultPath(proposed_target)
  if p == "":
    return MISSING
  if not FileExistsInVault(p):
    return MISSING
  if not UnderAllowedRoots(p):
    return OUT_OF_SCOPE
  return OK
```

**Coupling to 4.1.1.9:** When **`AppendWitness`** is invoked, **`proposed_target`** must satisfy **`IsAuditablePath_v0 == OK`** or the operator runbook downgrades the closure cell per **4.1.1.9** rollback §1.

### NormalizeVaultPath_v0 (bounded deterministic rules — alias/case intentionally not resolved in v0)

These rules are **narrower** than full Obsidian resolution; they let juniors exercise **`IsAuditablePath_v0`** **without** claiming alias, case-folding, or multi-hop wikilink policy is frozen (**D-027** stack remains non-binding).

1. Trim leading/trailing Unicode whitespace on `proposed_target`.
2. If the string starts with `[[` **and** ends with `]]`, strip those **outermost** brackets **once** (do **not** recurse nested `[[` in v0).
3. Trim again after bracket strip.
4. If the result is empty → treat as **`""`** (downstream maps to **MISSING** after normalize).
5. If, after one outer strip, inner `[[` or `]]` remain → treat input as **non-canonical** — return the post-trim string **unchanged**; **`FileExistsInVault`** will likely yield **MISSING** until the operator rewrites the wikilink.
6. **Alias tables, basename collision, symlinks, case sensitivity:** **not resolved in v0** — `NormalizeVaultPath_v0` is a string normalization only. These concerns remain **`MOVED_OR_AMBIGUOUS`** until a dedicated policy note pins resolution rules (this quaternary does **not** close that gap).

### AppendWitness_v0 + closure_table binding (vault-normative sketch)

**Purpose:** Tighten **`safety_unknown_gap`** from nested **`roadmap_handoff_auto`** second pass (`.technical/Validator/validator-roadmap_handoff_auto-genesis-mythos-master-20260325T020500Z-post-deepen-41110-second-compare-first.md`) by **instantiating** how a witness row binds to a rollup **closure_table** cell — **without** claiming **G-P4-1-*** **PASS** or clearing **REGISTRY-CI HOLD**.

**Precondition:** `IsAuditablePath_v0(proposed_target) == OK`. On any other verdict, emit **`witness_append_skipped`** (runbook / ledger taxonomy **TBD**) and apply **4.1.1.9** rollback §1 downgrade — **no** silent closure cell promotion.

```text
type ClosureTableRowKey_v0 = tuple(gate_row_id: string, bundle_id: string, evidence_status_cell: string)

enum AppendWitnessOutcome_v0:
  WITNESS_BOUND_OK
  PATH_FAIL
  TABLE_KEY_MISSING
  APPEND_DUPLICATE_IDEMPOTENT

function AppendWitness_v0(
  closure_table: map<ClosureTableRowKey_v0, ClosureCellState_v0>,
  row_key: ClosureTableRowKey_v0,
  witness: EvidenceWitnessRow_v0
) -> AppendWitnessOutcome_v0:
  if not closure_table.contains(row_key):
    return TABLE_KEY_MISSING
  if IsAuditablePath_v0(witness.proposed_target) != OK:
    return PATH_FAIL
  if closure_table[row_key].witness_anchor == witness.workflow_log_anchor:
    return APPEND_DUPLICATE_IDEMPOTENT
  closure_table[row_key].witness_ref = WitnessRefHash_v0(witness)
  emit ledger: witness_appended.event { reason_code: WITNESS_BOUND_OK, row_key, witness.workflow_log_anchor }
  return WITNESS_BOUND_OK
```

**Closure binding table (vocabulary — vault)**

| Event / outcome | Closure cell fields touched | Implies rollup PASS? |
| --- | --- | --- |
| `witness_appended.event` + `WITNESS_BOUND_OK` | `witness_ref`, `evidence_bundle_ref` (from `bundle_id`) | **No** — **FAIL (stub)** until repo harness + registry row |
| `witness_append_skipped` (path verdict ≠ OK) | Downgrade per **4.1.1.9** | **No** |
| `APPEND_DUPLICATE_IDEMPOTENT` | None (replay-safe no-op) | **No** |

> [!warning] Honesty guard: This table **binds vocabulary** between **4.1.1.9** runbook steps and closure-table columns; it **does not** satisfy **missing_roll_up_gates** or clear **HR 92 < 93**.

### Witness outcome ↔ 4.1.1.9 rollback vocabulary (vault)

| `AppendWitnessOutcome_v0` / path verdict | Hook on [[phase-4-1-1-9-bundle-verification-witness-and-rollback-runbook-roadmap-2026-03-24-2304]] | Rollup / closure implication |
| --- | --- | --- |
| Path verdict ≠ **OK** (`PATH_FAIL` / `witness_append_skipped` intent) | **Rollback §1** — downgrade `evidence_status_cell` **without** deleting narrative history | **No** PASS |
| `TABLE_KEY_MISSING` | **Rollback §1** variant — operator records **missing_closure_key** token (**registry row TBD**) | **No** PASS |
| `WITNESS_BOUND_OK` | Advance closure fields per **`AppendWitness_v0`** sketch only | **No** PASS until repo harness |
| `APPEND_DUPLICATE_IDEMPOTENT` | No rollback — replay-safe no-op | **No** PASS change |

### Junior Given / When / Then (drill scenarios)

1. **OK path** — **Given** a vault-relative path to an existing note under `1-Projects/genesis-mythos-master/Roadmap/`, **When** `IsAuditablePath_v0` runs, **Then** verdict **OK** and **4.1.1.9** may proceed without rollback §1 downgrade.
2. **MISSING** — **Given** `proposed_target` that normalizes to a basename with **no** vault file, **When** checked, **Then** verdict **MISSING** and operator records `witness_append_skipped` intent (**taxonomy string TBD** — not a rollup PASS).
3. **TABLE_KEY_MISSING** — **Given** a syntactically valid **`EvidenceWitnessRow_v0`** whose `gate_row_id` is absent from the active closure table snapshot, **When** `AppendWitness_v0` runs, **Then** outcome **TABLE_KEY_MISSING** and **4.1.1.9** rollback §1 applies per table above — **no** stub → PASS flip.

### Witness appendix (ordered artifacts)

1. **[[workflow_state]]** — **terminal (live)** machine-advancing **`deepen`** **`queue_entry_id` `resume-deepen-post-recal-distilled-yaml-gmm-20260326T041500Z-followup`** (Layer-1 **`roadmap_handoff_auto`** vs **`.technical/Validator`** mirrors — **ctx-tracking** **89%**, **2026-03-26 12:30** row); **historical** **`resume-roadmap-deepen-gmm-20260326T040820Z`** (**RollUpGateChecklist_v0** witness-appendix OPEN-rows — **89%**, **2026-03-26 04:08** row); **historical** **`followup-deepen-post-recal-distilled-parity-gmm-20260325T213400Z`** (**H_canonical** registry stub + repo acceptance envelope — **90%**, **2026-03-25 23:45** row); **historical** **`resume-deepen-post-recal-antispin-followup-gmm-20260325T193000Z`** (**RollUpGateChecklist_v0** / **D-072** — **89%**, **04:55**); **historical** **`eatq-antispin-obs-test-gmm-20260325T180000Z`** (**WitnessRefHash** / ledger literals — **88%**); **historical** **`resume-deepen-post-recal-0245-followup-gmm-20260325T031800Z`**; **historical** **`resume-deepen-post-second-pass-needs-work-gmm-20260325T020600Z`**; **historical** pass2 mint **`resume-deepen-post-pass2-41110-auditable-path-gmm-20260325T000321Z`**.
2. **This note** — `IsAuditablePath_v0`, `AppendWitness_v0`, **`WitnessRefHash_v0` JSON preimage v0**, ledger event literals, **EXAMPLE** `EvidenceWitnessRow_v0` JSON.
3. **[[phase-4-1-1-9-bundle-verification-witness-and-rollback-runbook-roadmap-2026-03-24-2304]]** — rollback §1 when path check fails.
4. **[[phase-4-1-1-7-adapter-registry-rollup-handoff-bundle-and-closure-map-roadmap-2026-03-24-0926]]** — bundle / closure map for valid **`bundle_id`** (vault scope only).

### WitnessRefHash_v0 (canonical JSON preimage sketch — `H_canonical` fixed by v0 policy exception)

**Purpose:** Satisfy the **in-note** hook from **`AppendWitness_v0`** (`witness_ref ← WitnessRefHash_v0(witness)`) with a **deterministic JSON shape** while remaining **vault-honest** about hash algorithm and registry freeze.

**Fixed field order (v0 — literals for junior serialization tests):**

```json
{
  "schema_id": "EvidenceWitnessRow_v0.1",
  "gate_row_id": "<string>",
  "bundle_id": "<string>",
  "proposed_target": "<normalized vault-relative string>",
  "witness_actor": "<string>",
  "witness_utc": "<RFC3339 Z>",
  "workflow_log_anchor": "<queue_entry_id or synthetic anchor>"
}
```

**Hash step (v0 policy exception):** `WitnessRefHash_v0(w) := SHA256(UTF8_bytes(JSON_SER_ORDERED(w)))` (policy exception: **D-078** + **D-020** allow a vault-local, non-claiming selection for determinism tests; **does not** imply checked-in registry row, repo emission, or CI PASS).

**Ledger events (vocabulary — names only until repo schema exists):**

```text
event witness_appended {
  reason_code: WITNESS_BOUND_OK | PATH_FAIL | TABLE_KEY_MISSING | APPEND_DUPLICATE_IDEMPOTENT
  row_key: ClosureTableRowKey_v0
  witness.workflow_log_anchor: string
  witness_ref: unset | bytes  // bytes only after H_canonical freezes
}

event witness_skipped {
  reason: witness_append_skipped
  path_verdict: AuditablePathVerdict_v0
  row_key: ClosureTableRowKey_v0 | null
}
```

> [!warning] **No PASS implication:** Emitting these event **shapes** in markdown **does not** satisfy **missing_roll_up_gates**, clear **REGISTRY-CI HOLD**, or substitute **Lane-C** **`ReplayAndVerify`** (**@skipUntil(D-032)**).

### EXAMPLE EvidenceWitnessRow_v0 (non-normative)

> [!warning] EXAMPLE ONLY — not evidence of CI closure or rollup PASS

```json
{
  "gate_row_id": "G-P4-1-ADAPTER-CORE",
  "bundle_id": "P4-1-1-BUNDLE-A",
  "proposed_target": "1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems/phase-4-1-1-7-adapter-registry-rollup-handoff-bundle-and-closure-map-roadmap-2026-03-24-0926.md",
  "witness_actor": "operator-example",
  "witness_utc": "2026-03-25T00:03:21Z",
  "workflow_log_anchor": "resume-deepen-post-pass2-41110-auditable-path-gmm-20260325T000321Z"
}
```

### Acceptance criteria

1. **`IsAuditablePath_v0`** documents **inputs**, **outputs**, and **enum** tied to **4.1.1.9** rollback wording.
2. **`AppendWitness_v0`** documents **preconditions**, **outcomes**, and **closure_table** row-key coupling + honesty table (**no** rollup PASS implication).
3. **Witness appendix** lists ordered artifacts (workflow log anchor → this note → 4.1.1.9 → 4.1.1.7).
4. **EXAMPLE** row is explicitly **non-normative** and does not flip **G-P4-1-*** stubs to PASS.
5. Upward links to **4.1.1.9**, **4.1.1.7**, and tertiary **4.1.1** present in body and `links`.
6. **Rollup HR 92 < 93** and **REGISTRY-CI HOLD** remain explicit in prose.
7. **`NormalizeVaultPath_v0`** lists bounded v0 steps; alias/case are **intentionally not resolved in v0**.
8. Witness ↔ rollback vocabulary table maps outcomes to **4.1.1.9** §1 without PASS inflation.
9. At least **three** **Given/When/Then** drills cover **OK**, **MISSING**, and **TABLE_KEY_MISSING**.
10. **`WitnessRefHash_v0`** documents **ordered JSON preimage** + fixes `H_canonical` **by v0 policy exception** while still stating **registry / repo emission / CI** are **not satisfied** (no PASS inflation).
11. **`WitnessRefHashRegistryRow_v0`** vault stub + **repo-side acceptance envelope** document **DEFERRED** execution without **HR≥93** or **REGISTRY-CI PASS** claims.

### Non-goals

- No **ReplayAndVerify** or registry row materialization.
- No automatic **`recal`** queue line from this note alone (**D-060** applies when context tracking shows util ≥ threshold).

### Edges

- **Symlinks / case sensitivity:** treat as **MOVED_OR_AMBIGUOUS** until operator normalizes canonical vault path policy (**D-027** stack TBD does not block this vault-only contract).

### Handoff audit trace (2026-03-25 — `repair-l1-postlv-distilled-cursor-gmm-20260325T193300Z`)

- **Cited validator:** `[[3-Resources/Second-Brain/Validator-Reports/roadmap_handoff_auto/genesis-mythos-master-20260325T193200Z-layer1-post-recal.md]]` — **`state_hygiene_failure`** on [[distilled-core]] self-contradictory **`last_auto_iteration`** strings.
- **Repair:** [[distilled-core]] YAML + body + **Canonical cursor parity** aligned to [[workflow_state]] **`eatq-antispin-obs-test-gmm-20260325T180000Z`** @ **`4.1.1.10`**; **D-073** + **`#handoff-review`** on [[decisions-log]]; [[workflow_state]] **`## Log`** row **2026-03-25 20:05**.
- **Still open:** **`H_canonical`**, registry row, repo harness, **G-P4-1-*** **FAIL (stub)**, rollup **HR 92 < 93**, **REGISTRY-CI HOLD** — unchanged (honest).

### Shallow deepen — D-072 trace + `RollUpGateChecklist_v0` (queue `resume-deepen-post-recal-antispin-followup-gmm-20260325T193000Z`)

> [!note] Vault-honest scope — **no** metric inflation
> This subsection answers resolver **`need_class: missing_structure`** with a **checklist-shaped** roll-up / safety articulation. It **does not** claim **rollup HR ≥ 93**, **REGISTRY-CI PASS**, or closure of **`missing_roll_up_gates`**. It cites **[[decisions-log]] D-072** as the audit anchor after the **18:15** high-context deepen and **D-060**-style **recal** row (**19:25**), where nested **`Task(validator)`** / IRA were **host-unavailable** and Layer-1 **`roadmap_handoff_auto`** remained the recommended hostile pass.

**Trace:** **D-072** documents **qualitative** `drift_score_last_recal` / `handoff_drift_last_recal` **unchanged** (**0.04 / 0.15**), **rollup HR 92 < 93**, **REGISTRY-CI HOLD**, **`missing_roll_up_gates`**, **`safety_unknown_gap`** **unchanged** after **`eatq-antispin-obs-test-gmm-20260325T180000Z`**. **D-074** / **D-075** subsequent nested passes **preserved** the same **HR / registry** honesty — still **no** PASS inflation.

#### `RollUpGateChecklist_v0` (stub — operator fills evidence cells)

| Gate row | Claim | Evidence hook | Status (honest) |
| --- | --- | --- | --- |
| **G-P4-1-rollup-HR** | Handoff rollup **HR** meets phase gate (**≥ 93** when policy requires) | Vault evidence bundle + validator report path | **OPEN** — **HR 92 < 93** (per **D-072** / **D-074**) |
| **G-P4-1-REGISTRY-CI** | **REGISTRY-CI** not in **HOLD** when claiming adapter closure | CI / registry run log + waiver | **HOLD** — unchanged |
| **`missing_roll_up_gates`** | Roll-up vocabulary maps to **closure_table** + witness | This note + **4.1.1.7** bundle | **PARTIAL** — structure sketched; **instantiation TBD** |
| **`safety_unknown_gap`** | **IsAuditablePath** / witness machinery not prose-only | **Given/When/Then** + **EXAMPLE** row | **NARROWED** per prior deepens; **Lane-C** still **@skipUntil(D-032)** |
| **`H_canonical` / repo harness** | **WitnessRefHash_v0** bytes + registry row + repo emission | Repo artifact + hash spec | **STUB** — vault registry-row skeleton + acceptance envelope (**23:45Z** deepen); **execution / bytes / CI still OPEN** |

**Next run hint (operator):** When **Ctx Util % ≥ 80%** after a deepen, **D-060** matrix: prefer **`RESUME_ROADMAP` `recal`** (drift refresh) or **`handoff-audit`** over another heavy **`deepen`** — see [[workflow_state]] **`## Log`** row **2026-03-25 23:45** (**`213400Z`**) and prior **04:55** **`193000Z`** row for contrast.

> [!info] DoD for **`missing_roll_up_gates`** (advisory)
> Checklist rows above are **not** instantiation: closure requires **closure_table** rows backed by **repo/registry evidence paths** (or a **documented waiver** tied to **D-020** / **2.2.3**). Markdown-only tables **do not** clear **REGISTRY-CI HOLD** or lift rollup **HR** to **≥ 93**.

### `WitnessRefHashRegistryRow_v0` (vault stub — execution DEFERRED)

**Purpose:** Satisfy validator **`next_artifacts`** direction to name a **registry row** for **`H_canonical`** **without** picking SHA-256-vs-JCS in prose as normative closure and **without** claiming **REGISTRY-CI PASS**.

**Stub row (vault-normative shape only — not checked-in registry):**

| Field | Value / constraint | Execution state |
| --- | --- | --- |
| `registry_key` | `witness_ref_hash_v0.genesis_mythos_master` | **DEFERRED** until wiki / `fixtures/**` owner assigns canonical key |
| `schema_id` | `EvidenceWitnessRow_v0.1` (must match **WitnessRefHash_v0** JSON preimage) | Frozen in this note only |
| `serialization_profile_id` | `JSON_UTF8_FIELD_ORDER_V0` (field order as fenced JSON in **WitnessRefHash_v0** §) | **DEFERRED** if JCS profile replaces literal order |
| `H_canonical` | `SHA256(UTF8(JSON_SER_ORDERED(w)))` (v0 policy exception only; no registry/CI claim) | **DEFERRED** — execution / wiki registry row still pending |
| `fixture_path` | `fixtures/witness_ref_hash/v0/example_row.json` (illustrative only) | **DEFERRED** — no repo path asserted |
| `registry_ci_gate` | **G-P*.*-REGISTRY-CI** | **HOLD** — unchanged |

> [!warning] Honesty guard
> This table is a **slot definition**, not evidence. It **does not** close **`missing_roll_up_gates`**, satisfy **`next_artifacts[1]`** phase-note acceptance rows, or substitute **Lane-C** **`ReplayAndVerify`**.

### Repo-side acceptance envelope (check-in criteria — **not satisfied**)

Maps validator compare-final **`.technical/Validator/roadmap-auto-validation-genesis-mythos-master-20260325T213200Z-recal-post-distilled-parity-compare-final.md`** **`next_artifacts[0]`** to **concrete repo artifacts** (none asserted present):

1. **Checked-in hash profile:** one of: **SHA256+UTF8 ordered JSON** or **JCS** profile frozen under `fixtures/witness_ref_hash/v0/` + CI vector that fails on drift.
2. **Registry row materialization:** wiki or machine registry entry matching **`WitnessRefHashRegistryRow_v0`** stub above + **PR-reviewed** promotion (no auto-green).
3. **Policy exception (if any):** explicit **D-020** / **2.2.3** waiver doc path — **not** vault adjectives alone.

**Explicit defer:** Until (1)–(2) land, **G-P4-1-*** rows remain **FAIL (stub)** and rollup **HR 92 < 93** stays honest.

### Bounded deepen trace (2026-03-25 23:45Z — queue `followup-deepen-post-recal-distilled-parity-gmm-20260325T213400Z`)

- **Parent telemetry:** `pr-l1-eatq-followup-deepen-parity-gmm-20260325T234500Z` · `pipeline_task_correlation_id` **`a8e3f1c2-7b4d-4e9a-9c1f-2d6e8b0a4f73`**
- **Conceptual track lock:** `params.roadmap_track: conceptual` — **no** **`Roadmap/Execution/`** pivot (resolver **`track_lock_explicit: true`**).
- **Compare-final cite:** **`primary_code: missing_roll_up_gates`** — this deepen adds **structure** only; **severity / recommended_action** unchanged vs **213200Z** expectation.
- **Decision anchor:** [[decisions-log]] **D-078** (traceability for **213400Z** terminal cursor advance).
- **Pre-mutate backups:** [[Backups/Per-Change/20260325-234500Z-workflow-state-pre-deepen-followup-distilled-parity-gmm.md.bak]] · [[Backups/Per-Change/20260325-234500Z-roadmap-state-pre-deepen-followup-distilled-parity-gmm.md.bak]] · [[Backups/Per-Change/20260325-234500Z-phase-41110-pre-deepen-followup-distilled-parity-gmm.md.bak]] · [[Backups/Per-Change/20260325-234500Z-distilled-core-pre-deepen-followup-distilled-parity-gmm.md.bak]]

### Bounded deepen trace (2026-03-26T04:08Z — queue `resume-roadmap-deepen-gmm-20260326T040820Z`)

**Auditable path witness appendix — `RollUpGateChecklist_v0` OPEN rows (structure-only)**

| Checklist row (OPEN / HOLD / PARTIAL) | What an auditable witness would cite (vault paths / artifacts) | Explicitly **not** claiming |
| --- | --- | --- |
| **G-P4-1-rollup-HR (OPEN)** | [[workflow_state]] **## Log** row + validator compare-final path that records rollup HR (e.g. `.technical/Validator/...compare-final.md`) | HR ≥ 93 |
| **G-P4-1-REGISTRY-CI (HOLD)** | Repo CI log + registry waiver bundle (when paths exist) | REGISTRY-CI PASS |
| **`missing_roll_up_gates` (PARTIAL)** | [[phase-4-1-1-7-adapter-registry-rollup-handoff-bundle-and-closure-map-roadmap-2026-03-24-0926]] closure keys + this note `AppendWitness_v0` / closure binding table | Rollup PASS |
| **`safety_unknown_gap` (NARROWED)** | Given/When/Then drills + EXAMPLE `EvidenceWitnessRow_v0` + **Witness appendix** ordered list | Lane-C green |
| **`H_canonical` / repo harness (STUB)** | `WitnessRefHashRegistryRow_v0` stub § + **Repo-side acceptance envelope** § | Bytes checked into repo |

**Resolver alignment:** `need_class: missing_structure` · `effective_target: 4.1.1.10 / auditable path witness appendix (RollUpGateChecklist_v0 OPEN rows)` · `gate_signature: missing_roll_up_gates|safety_unknown_gap` · `gate_streak: 0` · `track_lock_explicit: true` · `gate_catalog_id: conceptual_v1`.

**Telemetry:** `parent_run_id` **`9b2a62ec-5d73-4639-9dfa-6ae328bd017b`** · `pipeline_task_correlation_id` **`557fec38-417f-415c-af2f-ae26ce63f73a`** · `queue_entry_id` **`resume-roadmap-deepen-gmm-20260326T040820Z`**.

> [!note] Honesty
> This appendix **names witness-shaped evidence hooks** for OPEN/HOLD rows; it does **not** close gates, lift rollup HR, or clear **REGISTRY-CI HOLD**.

### Bounded deepen trace (2026-03-26 — queue `resume-deepen-post-recal-distilled-yaml-gmm-20260326T041500Z-followup`)

- **Purpose:** Post-**D-080** / post–**D-060** **`distilled-core`** **`core_decisions`** parity (**040820Z** authoritative) — cite **Layer-1** **`roadmap_handoff_auto`** vs **RoadmapSubagent / `.technical/Validator`** mirrors **without** inflating **HR** / **REGISTRY-CI**.
- **Layer-1 (Validator-Reports mirror):** `[[3-Resources/Second-Brain/Validator-Reports/roadmap_handoff_auto/genesis-mythos-master-20260326T130500Z-roadmap-handoff-auto-conceptual-v1-post-d080.md]]` — second pass after **D-080** workflow **`## Log`** cell repair (**4.1.1.8** historical).
- **RoadmapSubagent / recal chain (mirror):** `.technical/Validator/roadmap-auto-validation-genesis-mythos-master-20260326T044500Z-roadmap-handoff-auto-conceptual-v1-rerun.md` — **D-060** **`recal`** after **04:08Z** deepen **`resume-roadmap-deepen-gmm-20260326T040820Z`**; **`distilled-core`** **`core_decisions`** live strings repaired (**`213400Z` → historical**; **`040820Z`** authoritative) per prior **`state_hygiene_failure`** closure.
- **Vault-honest machine verdict (unchanged):** **`missing_roll_up_gates`**, **`safety_unknown_gap`** remain **advisory OPEN**; **rollup HR 92 < 93**; **G-P*.*-REGISTRY-CI** **HOLD** — **no** **HR ≥ 93** / **REGISTRY-CI PASS** claims.
- **Canonical cursor parity (historical tranche):** this tranche had advanced **`last_auto_iteration`** to **`resume-deepen-post-recal-distilled-yaml-gmm-20260326T041500Z-followup`** at the time; it is now **superseded** by **`resume-forward-map-phase-41110-gmm-20260326T180000Z`** per current [[workflow_state]] YAML + first physical **`deepen`** row in **`## Log`**.

**Telemetry:** `parent_run_id` **`l1-eatq-resume-deepen-followup-gmm-20260326T123000Z`** · `pipeline_task_correlation_id` **`a3f7c2e1-9d4b-4f6a-8c2e-1b5d7f9a0e4c`** · `queue_entry_id` **`resume-deepen-post-recal-distilled-yaml-gmm-20260326T041500Z-followup`**.

### Research integration + bounded deepen (2026-03-26 — queue `resume-roadmap-research-true-gmm-20260326T000000Z`)

- **Pre-deepen research consumed (nested task):** vault-first synthesis confirmed that canonical cursor and target remain `4.1.1.10` with the same conceptual scope: auditable witness mapping, no execution closure claims.
- **Evidence continuity retained:** validator trajectory is still centered on `missing_roll_up_gates` and `safety_unknown_gap`; earlier state-hygiene cursor drift is treated as repaired history, not a live blocker.
- **Bounded deepen objective:** tighten the conceptual witness-index contract so each OPEN/HOLD row can point to one current validator citation and one workflow/decision anchor.
- **Non-claim guard (unchanged):** rollup **HR 92 < 93** and **REGISTRY-CI HOLD** remain explicit; this section does not imply HR>=93, CI PASS, or repo-side closure.

#### Research integration

- Canonical cursor at deepen start: `last_auto_iteration` **`resume-deepen-post-recal-distilled-yaml-gmm-20260326T041500Z-followup`** and `current_subphase_index` **`4.1.1.10`** ([[workflow_state]]).
- Existing witness machinery already in scope here: `IsAuditablePath_v0`, `AppendWitness_v0`, rollback coupling to **4.1.1.9**, and `RollUpGateChecklist_v0` OPEN/HOLD/PARTIAL mapping.
- Follow-up implication from research: prioritize per-row evidence indexing and wording consistency across [[workflow_state]], [[roadmap-state]], and [[distilled-core]] rather than adding closure language.
- Keep DoD language conceptual-only: traceability quality, witness linkage quality, and consistency; no execution-gate closure semantics.

**Research sources consumed:** [[workflow_state]], [[roadmap-state]], [[distilled-core]], `3-Resources/Second-Brain/Validator-Reports/roadmap_handoff_auto/genesis-mythos-master-20260326T130500Z-roadmap-handoff-auto-conceptual-v1-post-d080.md`, `3-Resources/Second-Brain/Validator-Reports/roadmap_handoff_auto/genesis-mythos-master-20260326T140000Z-roadmap-handoff-auto-conceptual-v1-second-pass-post-d080-ira.md`.

**Telemetry:** `parent_run_id` **`queue-eat-queue-20260326T064229Z`** · `queue_entry_id` **`resume-roadmap-research-true-gmm-20260326T000000Z`**.

### Forward map deepen (2026-03-26 19:05 UTC — queue `resume-forward-map-phase-41110-gmm-20260326T180000Z`)

- **Intent:** map the remaining concrete structure/work for this quaternary so later runs can convert directly to executable artifacts, while preserving conceptual-track honesty (**rollup HR 92 < 93**, **REGISTRY-CI HOLD**).
- **Decisions reviewed before mapping:** [[decisions-log]] **D-079**, **D-080**, **D-081**, **D-082** and recent `roadmap_handoff_auto` compare-final notes.
- **No closure inflation:** this deepen adds task scaffolding and artifact contracts only; it does not claim CI closure, registry PASS, or HR>=93.

#### Remaining structure map (concrete next artifacts)

| Id | Artifact (planned) | Purpose | Acceptance check (conceptual) |
| --- | --- | --- | --- |
| **A-41110-01** | `Roadmap/Phase-4-Perspective-Split-and-Control-Systems/Artifacts/rollup-gatechecklist-v0-evidence-index-2026-03-26.md` | One canonical index from each `RollUpGateChecklist_v0` row to exactly one validator citation and one workflow/decision anchor. | Every OPEN/HOLD/PARTIAL row has `validator_ref` + `workflow_ref` + `decision_ref`; no PASS language. |
| **A-41110-02** | `Roadmap/Phase-4-Perspective-Split-and-Control-Systems/Artifacts/appendwitness-v0-outcome-matrix-2026-03-26.md` | Normalize `AppendWitnessOutcome_v0` handling into conversion-ready tasks for closure-table updates and rollback hooks. | Matrix covers `WITNESS_BOUND_OK`, `PATH_FAIL`, `TABLE_KEY_MISSING`, `APPEND_DUPLICATE_IDEMPOTENT` with explicit non-goals. |
| **A-41110-03** | `Roadmap/Phase-4-Perspective-Split-and-Control-Systems/Artifacts/witnessrefhash-v0-registry-promotion-plan-2026-03-26.md` | Stage `H_canonical` promotion path (vault -> registry row -> repo acceptance) without asserting completion. | Plan enumerates owner lane, prerequisite evidence, and hold condition text that keeps REGISTRY-CI in HOLD until external proof exists. |

#### Concrete task list for next runs

1. **T-41110-01 (Evidence index harden):** create `A-41110-01` and bind every checklist row to one current source of truth (validator report path + workflow log row + decision id).
2. **T-41110-02 (Outcome matrix extraction):** split the current `AppendWitness_v0` prose into a conversion-ready matrix note (`A-41110-02`) with deterministic field names for juniors.
3. **T-41110-03 (Registry promotion plan):** write `A-41110-03` with explicit preconditions for moving `H_canonical` from policy exception text to registry-backed execution evidence.
4. **T-41110-04 (Acceptance rows):** add one acceptance row under this phase note for each artifact above, marked OPEN until each artifact note exists and is linked.

#### Acceptance criteria for this forward map deepen

1. Three concrete artifact notes are named with paths and non-overlapping purpose.
2. Four conversion-ready tasks are listed with unique IDs and direct tie to artifacts.
3. Mapping explicitly preserves conceptual honesty gates (**HR 92 < 93**, **REGISTRY-CI HOLD**, `missing_roll_up_gates`, `safety_unknown_gap`).
4. No task language claims closure of execution-only holds; all closure language is deferred to future execution evidence.

### Bounded deepen (2026-03-26 19:19 UTC — queue `followup-deepen-post-forward-map-recal-gmm-20260326T191900Z`)

- **Resolver echo:** `need_class: missing_structure` · `effective_action: deepen` · `effective_target: 4.1.1.10 / auditable path witness appendix` · `track_lock_explicit: true` · `effective_track: conceptual` · `gate_catalog_id: conceptual_v1`.
- **Pre-deepen research consumed (nested task):** focused synthesis retained the same conceptual scope and recommended one concrete roll-up artifact closure + one `@skipUntil(D-032)` dependency bridge.
- **Honesty invariant preserved:** this deepen does **not** claim **HR >= 93** and does **not** claim **REGISTRY-CI PASS**.

#### Concrete roll-up gate artifact closure (single-row, no-pass inflation)

- Added artifact anchor: `Roadmap/Phase-4-Perspective-Split-and-Control-Systems/Artifacts/rollup-gatechecklist-v0-evidence-index-2026-03-26.md`.
- Closed one concrete evidence-index row for **`G-P4.1-ROLLUP-GATE-02`** by pinning:
  - `validator_ref`: `3-Resources/Second-Brain/Validator-Reports/roadmap_handoff_auto/genesis-mythos-master-20260326T130500Z-roadmap-handoff-auto-conceptual-v1-post-d080.md`
  - `workflow_ref`: [[workflow_state]] row for queue `resume-forward-map-phase-41110-gmm-20260326T180000Z`
  - `decision_ref`: [[decisions-log]] (`D-082` continuity + `D-083` row for this deepen)
- **Acceptance check (conceptual only):** all three refs are present and link-resolvable; no `TBD` text remains on this row.

#### `@skipUntil(D-032)` conversion to execution-bridge artifact (owner + check)

- Added execution-bridge anchor: `Roadmap/Phase-4-Perspective-Split-and-Control-Systems/Artifacts/d032-lane-c-execution-bridge-2026-03-26.md`.
- Converted one dependency path from prose-only hold to an owner-bound bridge entry:
  - `dependency_anchor`: `@skipUntil(D-032)` (Lane-C `ReplayAndVerify`)
  - `owner`: `ROLE:lane-c-harness`
  - `queue_anchor`: `wbs-41110-03-lane-c-replayandverify-unblock-gmm-20260326T000000Z`
  - `preconditions`: `D-032` literal replay columns + `replay_row_version` coordination
- **Acceptance check (bridge only):** owner named, queue anchor present, preconditions listed, and verification step defined as checklist item; no CI/registry closure claim.

#### Roll-up gate closure rows (OPEN)

| Artifact | artifact_path | validator_ref | workflow_ref | decision_ref | status |
| --- | --- | --- | --- | --- | --- |
| A-41110-01 | `Roadmap/Phase-4-Perspective-Split-and-Control-Systems/Artifacts/rollup-gatechecklist-v0-evidence-index-2026-03-26.md` | `3-Resources/Second-Brain/Validator-Reports/roadmap_handoff_auto/genesis-mythos-master-20260326T130500Z-roadmap-handoff-auto-conceptual-v1-post-d080.md` | [[workflow_state]] (`resume-forward-map-phase-41110-gmm-20260326T180000Z`) | [[decisions-log]] `D-083` | OPEN |
| A-41110-02 | `Roadmap/Phase-4-Perspective-Split-and-Control-Systems/Artifacts/appendwitness-v0-outcome-matrix-2026-03-26.md` | `3-Resources/Second-Brain/Validator-Reports/roadmap_handoff_auto/genesis-mythos-master-20260326T191900Z-roadmap-handoff-auto-conceptual-v3-post-forward-map-recal.md` | [[workflow_state]] (`followup-deepen-post-forward-map-recal-gmm-20260326T191900Z`) | [[decisions-log]] `D-084` | OPEN |
| A-41110-03 | `Roadmap/Phase-4-Perspective-Split-and-Control-Systems/Artifacts/witnessrefhash-v0-registry-promotion-plan-2026-03-26.md` | `3-Resources/Second-Brain/Validator-Reports/roadmap_handoff_auto/genesis-mythos-master-20260326T191900Z-roadmap-handoff-auto-conceptual-v3-post-forward-map-recal.md` | [[workflow_state]] (`followup-deepen-post-forward-map-recal-gmm-20260326T191900Z`) | [[decisions-log]] `D-084` | HOLD |

> [!warning] Open-gate honesty
> These rows are structure/evidence indexing only. They do **not** claim **HR >= 93**, do **not** claim **REGISTRY-CI PASS**, and do **not** assert execution closure.

#### D-032 bridge contract (OPEN)

- [ ] **owner:** `ROLE:lane-c-harness`
- [ ] **queue_anchor:** `wbs-41110-03-lane-c-replayandverify-unblock-gmm-20260326T000000Z`
- [ ] **preconditions:** `D-032` literal replay columns frozen; `replay_row_version` coordination recorded
- [ ] **verification_step:** contract-level replay bridge checklist exists and is link-resolvable
- [ ] **failure_mode:** keep `@skipUntil(D-032)` and retain conceptual hold language

> [!note]
> This contract does **not** imply Lane-C green, CI pass, or registry closure.
