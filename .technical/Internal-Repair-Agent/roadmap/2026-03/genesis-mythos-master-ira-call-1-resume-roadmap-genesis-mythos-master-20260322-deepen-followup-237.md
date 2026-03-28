---
created: 2026-03-22
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: resume-roadmap-genesis-mythos-master-20260322-deepen-followup-237
ira_call_index: 1
parent_run_id: pr-20260322-eatq-genesis-237
status: repair_plan
risk_summary:
  low: 2
  medium: 3
  high: 1
validator_report_path: .technical/Validator/roadmap-auto-validation-genesis-mythos-master-20260322T004500Z.md
reason_codes:
  - safety_unknown_gap
  - missing_task_decomposition
---

# IRA call 1 — genesis-mythos-master — queue resume-roadmap-genesis-mythos-master-20260322-deepen-followup-237

## Context

Post–`RESUME_ROADMAP` deepen for **Phase 3.1.5**, nested **`roadmap_handoff_auto`** first pass returned **medium / needs_work** with **primary_code `safety_unknown_gap`** and **`missing_task_decomposition`**. Workflow cursor, roadmap-state macro summary, **D-035**, and the new phase note are mutually consistent on **3.1.5** as the live target. Contaminated-report rule applied: treat the validator’s list as a **floor**—structural and traceability debt is likely **worse** than stated (e.g. grep-only hygiene, MOC backlinks, phase-output sync) unless the parent re-runs full little val.

## Structural discrepancies (expanded beyond minimum)

1. **`roadmap-state.md`** consistency block **2026-03-22 00:45** leaves **`IRA / validator trace: (pending this run)`** — stale observability vs adjacent blocks that already link first/final validator + IRA paths.
2. **`distilled-core.md`** **`core_decisions`** and body **## Core decisions** stop at **3.1.4** while **`decisions-log`** already records **D-035** for **3.1.5** — roll-up drift.
3. **Phase 3.1.5 note** **`## Tasks`** has **three naked `- [ ]` items** — **`missing_task_decomposition`** unless closed, deferred with a decision id, or replaced by explicit deferral prose.
4. **Research wikilink** filename suffix **`2315`** vs workflow log **`2026-03-22 00:45`** — ordering/audit hazard unless the vault states artifact-time vs log-time semantics (parallel to **`roadmap-state` § Notes** for pause research).
5. **`handoff_readiness: 91`** / **`execution_handoff_readiness: 70`** and merge-matrix / golden checksum **TBD** are honest sub-threshold metrics — not dual-truth; vault edits cannot substitute for replay/CI closure.

## Proposed fixes (for parent application)

Apply in **risk order**: **low → medium → high**. Snapshot **`roadmap-state`**, **`distilled-core`**, **`decisions-log`**, and the **phase 3.1.5** note before edits per roadmap MCP rules.

| # | risk | action_type | target_path | description |
|---|------|-------------|-------------|-------------|
| 1 | low | rewrite_log_entry | `1-Projects/genesis-mythos-master/Roadmap/roadmap-state.md` | In **### 2026-03-22 00:45**, replace **`IRA / validator trace: (pending this run)`** with wikilinks: first pass `[[.technical/Validator/roadmap-auto-validation-genesis-mythos-master-20260322T004500Z]]`; IRA call 1 `[[.technical/Internal-Repair-Agent/roadmap/2026-03/genesis-mythos-master-ira-call-1-resume-roadmap-genesis-mythos-master-20260322-deepen-followup-237]]`; compare-final = TBD line until second nested validator writes `…T004500Z-final.md`, then patch in that path. |
| 2 | low | write_log_entry | `1-Projects/genesis-mythos-master/Roadmap/decisions-log.md` | Under **D-035**, add **traceability footnote**: research note filename **`…-2315`** = synthesis artifact timestamp; **`workflow_state`** row **`2026-03-22 00:45`** = run log time — **do not** infer causal ordering from filename suffix alone (cf. **`roadmap-state` § Notes** on pause research filenames). |
| 3 | medium | recompute_phase_metadata | `1-Projects/genesis-mythos-master/Roadmap/distilled-core.md` | Add **Phase 3.1.5** to **`core_decisions`** (frontmatter) **and** **## Core decisions (🔵)** — align to **D-035**: `MutationIntent_v0`, `AgencySliceApplyLedger_v0`, idempotent `mutation_id`, last-writer vs `SLICE_STATE_CONFLICT`, **D-031** / **3.1.3** coupling; **TBD** merge matrix + **`mutation_batch_checksum`** until **D-032** + **3.1.1** `replay_row_version`. Link phase note. |
| 4 | medium | write_log_entry | `1-Projects/genesis-mythos-master/Roadmap/decisions-log.md` | Add **D-036** (or sub-bullets under **D-035**) registering **deferred acceptance** for: (a) **`MutationIntent_v0` preimage + hash-domain freeze**, (b) **two-slice worked example**, (c) **`mutation_batch_checksum` stub** — each with **unblock conditions** (**D-032** A/B, **3.1.1** row version; no CI assertion until stated). |
| 5 | medium | adjust_frontmatter | `1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/phase-3-1-5-deterministic-agency-slice-outcomes-mutation-ledger-replay-roadmap-2026-03-22-0045.md` | Replace naked **Tasks** checkboxes with **(A)** real completions or **(B)** **`[x] Documented deferral`** rows wikilinked to **`decisions-log#D-036`** (or chosen id) + one-line scope — no silent TODOs. |
| 6 | high | recompute_phase_metadata | `1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/phase-3-1-5-deterministic-agency-slice-outcomes-mutation-ledger-replay-roadmap-2026-03-22-0045.md` | **Optional:** fully execute the three outcomes (preimage freeze list, two-slice example with ledger rows, **`mutation_batch_checksum`** column stub spec). Coordinate **D-035**, **distilled-core**, possibly **3.1.1** — only when gates allow. |

### Constraints

- **Fix 1:** Touch only the **2026-03-22 00:45** subsection.
- **Fixes 3–5:** **distilled-core** and phase note must not contradict **D-036** deferral vs done.
- **Fix 6:** Skip when this run’s intent is deferral + honesty; prefer **4+5**.

## Notes for future tuning

- **distilled-core** often lags **decisions-log** by one subphase after deepen — add a post-deepen checklist in RoadmapSubagent.
- **`(pending this run)`** in **roadmap-state** during mid-cycle validator work — consider a safer default template.
- Standard **research filename vs log time** footnote whenever linking **`Ingest/Agent-Research/`** from roadmap consistency rows.
