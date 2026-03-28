---
created: 2026-03-28
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: validator-roadmap-handoff-auto-gmm-20260328T210530Z
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 3
  medium: 1
  high: 1
validator_report_path: .technical/Validator/roadmap-handoff-auto-genesis-mythos-master-20260328T210530Z-post-d129-compare-201500Z.md
---

# IRA report — genesis-mythos-master (validator-driven, post–D-129 compare)

## Context

Roadmap handoff auto-validator (`conceptual_v1`) compared against the prior 201500Z report after D-129 handoff-audit. **Primary `missing_roll_up_gates`** remains correctly **OPEN** (vault-honest rollup HR 92 < 93, REGISTRY-CI HOLD). **Secondary `safety_unknown_gap`** targets three older `workflow_state` ## Log deepen rows (**d116** / **d113** / **d112**) whose Status narrative still leads with bare **`machine cursor advance`**, so regex-only consumers can mis-read them as live cursor despite the global [!important] D-128 block. This IRA call is **ira_after_first_pass: true**; no little-val failure preceded it.

## Structural discrepancies

1. **Table vs prepend parity:** `roadmap-state.md` deepen notes use **`Machine cursor advance (historical note; live cursor = [[workflow_state]] frontmatter + [!important] callout)`** for the same era; `workflow_state.md` rows for queues `followup-deepen-post-d116-skimmer-repair-gmm-20260328T030000Z`, `resume-deepen-post-d113-compare-final-gmm-20260328T024500Z`, and `followup-deepen-post-d112-bounded-415-gmm-20260327T191500Z` lack that per-row prefix (**validator rows ~49–51**).
2. **Execution debt (intentional):** `missing_roll_up_gates` is **not** a conceptual coherence bug; closing it requires **REGISTRY-CI** + **handoff_readiness ≥ 93** evidence (or documented policy exception), not rewording conceptual tables alone.

## Proposed fixes (for RoadmapSubagent / operator)

| # | Risk | Action | Target |
|---|------|--------|--------|
| 1 | low | Prepend historical skimmer prefix to Status cell for **12:00 d116** deepen row | `workflow_state.md` |
| 2 | low | Same for **02:45 d113** deepen row | `workflow_state.md` |
| 3 | low | Same for **22:00 d112** deepen row | `workflow_state.md` |
| 4 | medium | After external truth: add **Execution** track note (or extend existing) with **CI run link**, **REGISTRY-CI outcome**, and **HR metric** source; cross-link from rollup-facing lines if closure is real | `Roadmap/Execution/**`, optional cross-refs |
| 5 | high | **Obtain** REGISTRY-CI PASS and HR ≥ 93 in repo/CI (or formal exception) before vault claims gate closure | repository / CI |

**Canonical prefix text** (match `roadmap-state` skimmer contract):

`**Machine cursor advance (historical note; live cursor = [[workflow_state]] frontmatter + [!important] callout)** — `

Then keep the existing **`machine cursor advance`** clause and queue id tail unchanged (forensic chronology preserved).

**Constraints**

- Do **not** edit the **20:05 d125** deepen row’s live-terminal **`machine cursor advance`** wording or the D-128/D-129 repair rows except as separately authorized.
- Apply fixes **after** per-change snapshot of `workflow_state.md` per dual-track / MCP guardrails.
- Do **not** remove or soften **`vault-honest unchanged` — rollup HR 92 < 93, REGISTRY-CI HOLD** prose to fake-clear `missing_roll_up_gates`.

## Notes for future tuning

- Align **workflow_state** deepen Status cells with **roadmap-state** historical phrasing whenever D-128-style supersession rewrites frontmatter terminal.
- Consider a one-line **grep CI** in roadmap-deepen or handoff-audit: flag bare `machine cursor advance` in ## Log body outside the live terminal row.
