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
handoff_readiness_scope: "IsAuditablePath_v0 + AppendWitness_v0 + WitnessRefHash_v0 JSON preimage shape + witness_appended/witness_skipped ledger literals (H_canonical TBD); vault-only EXAMPLE EvidenceWitnessRow_v0; does not clear rollup HR<93, REGISTRY-CI HOLD, or instantiate repo harness"
execution_handoff_readiness: 31
handoff_gaps:
  - "**G-P*.*-REGISTRY-CI HOLD** remains until 2.2.3 / D-020 execution evidence."
  - "EXAMPLE witness row is **non-normative** until operator promotes to golden / closure table row with auditable path."
  - "Path checks are vault-relative string ops only — no substitute for Lane-C **ReplayAndVerify** (**@skipUntil(D-032)**)."
  - "`WitnessRefHash_v0`: **JSON preimage field-order v0** + **ledger event name literals** are now sketched in-body; **`H_canonical` (SHA-256 vs JCS) + registry row + repo emission** remain **TBD** — still no rollup PASS."
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

### IsAuditablePath_v0 (checkable sketch)

**Inputs:** `proposed_target: string` (Obsidian wikilink target or vault-relative `.md` path after normalizing `[[` `]]`).

**Output:** `AuditablePathVerdict_v0` enum:

- `OK` — path resolves to an existing note under allowed PARA roots (`1-Projects/`, `2-Areas/`, `3-Resources/`, `4-Archives/`, `Ingest/`, `5-Attachments/` as linked target only).
- `MISSING` — normalized path has no file in vault.
- `MOVED_OR_AMBIGUOUS` — path fragment matches multiple candidates or alias collision (operator resolution required).
- `OUT_OF_SCOPE` — path points outside PARA / Ingest / Attachments allow-list (e.g. raw URL-only with no vault note).

> [!note] Non-normative sketch — `NormalizeVaultPath` is **not** fully specified here; the placeholder below is intentional (**vault-honest uninstantiated**) until a follow-on deepen defines bracket-stripping, alias resolution, and case rules.

```text
function NormalizeVaultPath(proposed_target: string) -> string:
  // strip [[ ]], resolve to vault-relative if possible
  // TBD: uninstantiated — explicit algorithm required before normative use
  return proposed_target // stub only; not production semantics
  // See "### NormalizeVaultPath_v0 (bounded deterministic rules)" for v0 strip/bracket steps.

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

### NormalizeVaultPath_v0 (bounded deterministic rules — alias/case still TBD)

These rules are **narrower** than full Obsidian resolution; they let juniors exercise **`IsAuditablePath_v0`** **without** claiming alias, case-folding, or multi-hop wikilink policy is frozen (**D-027** stack remains non-binding).

1. Trim leading/trailing Unicode whitespace on `proposed_target`.
2. If the string starts with `[[` **and** ends with `]]`, strip those **outermost** brackets **once** (do **not** recurse nested `[[` in v0).
3. Trim again after bracket strip.
4. If the result is empty → treat as **`""`** (downstream maps to **MISSING** after normalize).
5. If, after one outer strip, inner `[[` or `]]` remain → treat input as **non-canonical** — return the post-trim string **unchanged**; **`FileExistsInVault`** will likely yield **MISSING** until the operator rewrites the wikilink.
6. **Alias tables, basename collision, symlinks, case sensitivity:** **explicitly uninstantiated** — remain **`MOVED_OR_AMBIGUOUS`** until a dedicated note pins policy (this quaternary does **not** close that gap).

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
  // Bind: witness_ref ← WitnessRefHash_v0(witness)  // TBD: canonical JSON + hash registry
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

1. **[[workflow_state]]** — terminal machine-advancing **`deepen`** **`queue_entry_id` `eatq-antispin-obs-test-gmm-20260325T180000Z`** (**WitnessRefHash** / ledger literals — **ctx-tracking** **88%**); **historical** same-subphase **`resume-deepen-post-recal-0245-followup-gmm-20260325T031800Z`**; **historical** **`resume-deepen-post-second-pass-needs-work-gmm-20260325T020600Z`**; **historical** pass2 mint **`resume-deepen-post-pass2-41110-auditable-path-gmm-20260325T000321Z`**.
2. **This note** — `IsAuditablePath_v0`, `AppendWitness_v0`, **`WitnessRefHash_v0` JSON preimage v0**, ledger event literals, **EXAMPLE** `EvidenceWitnessRow_v0` JSON.
3. **[[phase-4-1-1-9-bundle-verification-witness-and-rollback-runbook-roadmap-2026-03-24-2304]]** — rollback §1 when path check fails.
4. **[[phase-4-1-1-7-adapter-registry-rollup-handoff-bundle-and-closure-map-roadmap-2026-03-24-0926]]** — bundle / closure map for valid **`bundle_id`** (vault scope only).

### WitnessRefHash_v0 (canonical JSON preimage sketch — `H_canonical` TBD)

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

**Hash step (explicitly uninstantiated):** `WitnessRefHash_v0(w) := H_canonical(UTF8_bytes(JSON_SER_ORDERED(w)))` — choose **`H_canonical`** (e.g. SHA-256 over UTF-8 vs **JCS** profile) in a **registry row**; this quaternary **does not** pick the algorithm.

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
7. **`NormalizeVaultPath_v0`** lists bounded v0 steps; alias/case remain **TBD**.
8. Witness ↔ rollback vocabulary table maps outcomes to **4.1.1.9** §1 without PASS inflation.
9. At least **three** **Given/When/Then** drills cover **OK**, **MISSING**, and **TABLE_KEY_MISSING**.
10. **`WitnessRefHash_v0`** documents **ordered JSON preimage** + states **`H_canonical` / registry / repo emission TBD** without PASS inflation.

### Non-goals

- No **ReplayAndVerify** or registry row materialization.
- No automatic **`recal`** queue line from this note alone (**D-060** applies when context tracking shows util ≥ threshold).

### Edges

- **Symlinks / case sensitivity:** treat as **MOVED_OR_AMBIGUOUS** until operator normalizes canonical vault path policy (**D-027** stack TBD does not block this vault-only contract).

### Handoff audit trace (2026-03-25 — `repair-l1-postlv-distilled-cursor-gmm-20260325T193300Z`)

- **Cited validator:** `[[3-Resources/Second-Brain/Validator-Reports/roadmap_handoff_auto/genesis-mythos-master-20260325T193200Z-layer1-post-recal.md]]` — **`state_hygiene_failure`** on [[distilled-core]] self-contradictory **`last_auto_iteration`** strings.
- **Repair:** [[distilled-core]] YAML + body + **Canonical cursor parity** aligned to [[workflow_state]] **`eatq-antispin-obs-test-gmm-20260325T180000Z`** @ **`4.1.1.10`**; **D-073** + **`#handoff-review`** on [[decisions-log]]; [[workflow_state]] **`## Log`** row **2026-03-25 20:05**.
- **Still open:** **`H_canonical`**, registry row, repo harness, **G-P4-1-*** **FAIL (stub)**, rollup **HR 92 < 93**, **REGISTRY-CI HOLD** — unchanged (honest).
