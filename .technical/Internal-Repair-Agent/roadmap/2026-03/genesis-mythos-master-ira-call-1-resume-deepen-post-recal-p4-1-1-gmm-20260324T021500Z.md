---
created: 2026-03-24
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: resume-deepen-post-recal-p4-1-1-gmm-20260324T021500Z
ira_call_index: 1
status: repair_plan
parent_task_correlation_id: b9a65ab5-70f5-4c65-9a48-1b5247f4b4fa
validator_report_path: .technical/Validator/roadmap-auto-validation-genesis-mythos-master-20260324T022500Z-post-p4-1-1-continuation-first.md
risk_summary:
  low: 4
  medium: 0
  high: 0
---

# IRA — roadmap / RESUME_ROADMAP deepen (post roadmap_handoff_auto first pass)

## Context

Validator first pass (`roadmap_handoff_auto`) returned **medium** / **needs_work** with **primary_code** `missing_task_decomposition`, plus `safety_unknown_gap` and `missing_roll_up_gates`. Invoked with **`ira_after_first_pass: true`**. Gaps: undefined **`CANONICAL_ADAPTER_COLUMNS_V0`** in **4.1.1.1** pseudo-code; open checklists without explicit deferral ownership; secondary **4.1** lacks a concrete **4.1.1.x → 4.1.2** roll-up gate row. **Do not** fabricate **REGISTRY-CI PASS** or **HR ≥ 93** — vault honesty stays as-is.

## Structural discrepancies

1. **Floating symbol:** `phase-4-1-1-1-...0228.md` asserts `layout.normative_columns == CANONICAL_ADAPTER_COLUMNS_V0` without defining the constant or linking to the **4.1.1** preimage table order.
2. **Task decomposition signal:** Multiple **4.1.1.1** and **4.1.1** tasks remain bare `- [ ]` without **`@skipUntil`** / decision anchors — reads as “not started” rather than “blocked on D-032 / 3.1.1 / T-P4-02”.
3. **Roll-up:** **4.1** “Next (tertiary spine)” prose mentions **4.1.2** after **4.1.1.x** closure but has no one-row **gate stub** with testable preconditions (validator **missing_roll_up_gates**).

## Proposed fixes (caller applies under snapshot/backup rules)

All items below are **low** risk (doc-only, localized). Full snippets are in the structured return `suggested_fixes` below.

## Notes for future tuning

- Prefer **inline alias comments** next to the first pseudo-code use of a constant rather than a distant glossary — reduces `missing_task_decomposition` on quaternary notes.
- Standardize **`@skipUntil(tag, reason)`** on any task that is blocked by decisions **D-0xx** so validators do not read “all open” as “no decomposition”.

## IRA-only writes

This file + Run-Telemetry under `.technical/Run-Telemetry/` — **no** edits to `1-Projects/**` by IRA (read-only contract on user artifacts).

## Appendix — verbatim insertion snippets

### A — 4.1.1.1 pseudo-code preamble (before `function RegisterAdapterRowLayout`)

```text
// CANONICAL_ADAPTER_COLUMNS_V0 — vault alias: ordered normative column ids matching parent 4.1.1
// "Preimage authority table (v0)" in [[phase-4-1-1-adapter-preimage-and-stable-column-layout-roadmap-2026-03-24-0018]] (table row order, top → bottom):
//   tick_id, post_apply_observable_root (hash field), serialization_profile_id, presentation_stable_inputs, camera_binding_id, fov_lod_parameters
// Semantics: layout.normative_columns must match this order/names unless 4.1.1 table is explicitly revised (no silent renames).
```

### B — 4.1.1.1 Tasks (replace three open lines)

```markdown
- [ ] Mirror **`normative_columns`** to **3.1.1** stub row when **3.1.1** note updates (no orphan renames). @skipUntil(D-032, 3.1.1 replay_row_version / stub freeze)
- [ ] Draft **`D-032` clearance changelog** section on **4.1.1** parent when operator freezes header literals (empty stub OK until then). @skipUntil(D-032 operator freeze)
- [ ] Link forward to **4.1.2** rig consume order when **T-P4-02** tertiary mints. @skipUntil(T-P4-02 tertiary mint + roll-up gate row satisfied)
```

### C — 4.1.1 Tasks (replace four open lines; keep completed line as-is)

```markdown
- [ ] Align adapter column names with **3.1.1** stub row (no silent rename vs rollup tables). @skipUntil(3.1.1 stub coordination + D-043 as needed)
- [ ] Document **@skipUntil(D-032)** for any presentation-only golden column. @skipUntil(D-032 literal contract for Lane-C / golden rows)
- [ ] Cross-check **RegenLaneTotalOrder_v0** (**D-044** Option A) — adapter read order does not introduce a second ordering lane. @skipUntil(D-044 read-order invariant locked or 4.1.2 rig consume draft)
- [ ] Close **4.1.1.1** task checklist when **`adapter_row_layout_id`** registry sketch is accepted. @skipUntil(4.1.1.1 acceptance + optional operator sign-off)
```

### D — 4.1 secondary: new section before `### Next (tertiary spine)`

```markdown
### Roll-up gate (4.1.1.x → 4.1.2) — stub

| Gate | Precondition (vault-testable) | Explicit non-claims |
|------|-------------------------------|---------------------|
| **G-4.1.1→4.1.2** | **4.1.1.1** registry sketch accepted: `adapter_row_layout_id` row + `normative_columns` aligned to **4.1.1** preimage table; **4.1.1** links a **D-032 changelog** stub (may be empty until freeze). | Does **not** assert **REGISTRY-CI PASS**, **HR ≥ 93**, or clearance of **G-P*.*-REGISTRY-CI HOLD** — **D-062** still applies. |
| **Mint 4.1.2** | Above row satisfied **and** operator or queue explicitly mints **T-P4-02** / **4.1.2** tertiary (per “Next (tertiary spine)” ordering). | **4.1.2** remains **draft** until rig consume order is written; no golden lane claims. |
```
