---
title: Phase 3.4.9 — Post-recal task decomposition and junior handoff bundle
roadmap-level: tertiary
phase-number: 3
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-22
tags: [roadmap, genesis-mythos-master, phase, living-world, task-decomposition, junior-handoff, validator-ladder, post-recal]
para-type: Project
subphase-index: "3.4.9"
handoff_readiness: 85
handoff_readiness_scope: "WBS-style leaves + traceability artifacts aligned to 3.4.8 validator ladder and L1 missing_task_decomposition (ladder PASS still on 3.4.8 until checkboxes + evidence) — vault-normative only; does not log D-044/D-059 picks"
execution_handoff_readiness: 33
handoff_gaps:
  - "Executable evidence (repo paths, green CI, golden rows) for ladder rows remains @skipUntil(D-032)/D-043/D-045 — same as 3.4.8"
  - "Phase 4.1 tertiary tree still blocked until D-059 logs ARCH-FORK-01 or ARCH-FORK-02"
links:
  - "[[phase-3-4-living-world-operations-and-consequence-fan-out-roadmap-2026-03-23-1210]]"
  - "[[phase-3-4-8-high-context-util-policy-and-phase-4-stub-readiness-roadmap-2026-03-22-1205]]"
  - "[[phase-3-4-7-perspective-entry-wbs-and-phase-4-1-task-bridge-roadmap-2026-03-22-0748]]"
  - "[[decisions-log]]"
  - "[[distilled-core]]"
---

## Phase 3.4.9 — Post-recal task decomposition and junior handoff bundle

**TL;DR:** After **RECAL** (**recal-gmm-post-348-deepen-high-util-20260322T120501Z**) and **3.4.8** (**D-060**), this tertiary turns the **Structural audit — task ladder (validator)** on [[phase-3-4-8-high-context-util-policy-and-phase-4-stub-readiness-roadmap-2026-03-22-1205]] into **checkable WBS leaves** with **interfaces (vault paths)**, **pseudo-code procedures**, **Given/When/Then** acceptance lines, and a **traceability matrix** — **delivering decomposition/traceability artifacts** for the post-recal hygiene slice and **L1 `missing_task_decomposition` alignment** (not a claim that **3.4.8** ladder rows are **PASS** until those checkboxes flip with cited evidence) **without** fabricating **D-044** or **D-059** outcomes.

## Research integration

**Scope:** Pre-deepen consumables for tertiary **3.4.9** — task decomposition and junior-developer handoff structure for the **validator task ladder** / **`missing_task_decomposition`** **artifact alignment** after **3.4.8 (D-060)** and **RECAL**. Does **not** pick **D-044** (**RegenLaneTotalOrder_v0**) or **D-059** (**ARCH-FORK-01** vs **ARCH-FORK-02**). **3.4.8** ladder **PASS** remains defined only when that note’s checklists meet their **Definition of done**.

### Key takeaways

- Decompose ladder work as **WBS-style leaves**: each checkbox = one verifiable artifact (path, `queue_entry_id`, or decisions-log sub-bullet pattern).
- Minimum **handoff pack**: scope one-pager, **interface** (which vault paths / table columns), **pseudo-code** procedure, **Given/When/Then** acceptance lines, **traceability** matrix (task → evidence → owner).
- **Hygiene pattern:** compare frontmatter **`last_ctx_util_pct`**, **`last_conf`**, **`current_subphase_index`**, **`last_auto_iteration`** on `1-Projects/genesis-mythos-master/Roadmap/workflow_state.md` to the **physical last** `## Log` data row — mismatch → hygiene repair or re-queue **`recal`**.
- Use **full vault paths** in machine-facing tables for juniors (`1-Projects/genesis-mythos-master/Roadmap/...`), not wikilinks alone.
- **Dual-track** boilerplate for regen/ambient/DM ordering until **D-044** operator sub-bullet exists.
- **Tree guard:** no Phase **4.1** tertiary **tree** until **D-059** logs **ARCH-FORK-01** or **ARCH-FORK-02**.

### Links

- [[Ingest/Agent-Research/phase-3-4-9-task-decomposition-junior-handoff-research-2026-03-22-1245]]
- Nested research synthesis validators: `.technical/Validator/research-synthesis-genesis-mythos-master-20260322T130800Z-first.md` → compare-final `.technical/Validator/research-synthesis-genesis-mythos-master-20260322T131500Z-compare-final.md`
- **A.1b deepen (2026-03-22 20:16 UTC):** [[Ingest/Agent-Research/phase-3-4-9-a1b-promptcraft-roll-up-gaps-synthesis-2026-03-22-2145]] — nested **research_synthesis** first `.technical/Validator/research-synthesis-genesis-mythos-master-20260322T214500Z-nested-pdeepen-first.md` → compare-final `.technical/Validator/research-synthesis-genesis-mythos-master-20260322T220500Z-nested-pdeepen-compare-final.md` (**low** / **`needs_work`**, residual **`safety_unknown_gap`** on excerpt anchoring only).

### A.1b PromptCraft deepen (queue `pcraft-gmm-deepen-a1b-20260322T201700Z-8e2c`)

- **Parent run:** `pr-eatq-20260322-pcraft-a1b-dispatch` — empty-queue bootstrap follow-up after **`pc-a1b-gmm-recal-20260322T123100Z`** and compare-final `.technical/Validator/roadmap-auto-validation-20260322T201545Z-gmm-pc-a1b-compare-final.md`.
- **Consumed research:** nested pre-deepen **`Task(research)`** → synthesis note above; integrates **rollup literacy** (**G-P3.2 / G-P3.3 / G-P3.4** paths + **D-046 / D-050 / D-055** excerpts), **PromptCraft** empty-queue bootstrap context, and **L1 `missing_task_decomposition`** row **GMM-L1-01** (below). **Does not** log **D-044** A/B or **D-059** **ARCH-FORK-0x**.

#### GMM-L1-01 — compare-final code → evidence contract

| Validator / L1 code | Vault artifact | PASS means |
| --- | --- | --- |
| `missing_roll_up_gates` | § **Validator compare-final alignment** + synthesis §2 rollup table | Stakeholder answers use **rollup note paths** + **HR 92 < 93** + **HOLD** ids — not **3.4.9** alone |
| `safety_unknown_gap` | **GMM-DLG-01** / **GMM-TREE-01** + drift methodology notes | No narrative **operator pick** without **decisions-log** sub-bullet; drift scalars labeled **qualitative** until versioned spec |
| `missing_task_decomposition` | Traceability matrix **GMM-**\* rows + this § | Each concern has **task id**, **evidence type**, **owner**; **3.4.8** ladder **`[x]`** only with cited **`queue_entry_id`** / repo path |

### Sources

- Consolidated in synthesis note **## Sources** (WBS, handoff patterns, INVEST heuristic, CQRS cross-links).

## Junior handoff pack (normative for this tertiary)

### Interfaces (read-only for this slice)

| Artifact | Path |
| --- | --- |
| Workflow cursor + metrics | `1-Projects/genesis-mythos-master/Roadmap/workflow_state.md` |
| Decisions | `1-Projects/genesis-mythos-master/Roadmap/decisions-log.md` |
| Roadmap narrative index | `1-Projects/genesis-mythos-master/Roadmap/roadmap-state.md` |
| Policy tertiary | `1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/phase-3-4-8-high-context-util-policy-and-phase-4-stub-readiness-roadmap-2026-03-22-1205.md` |

### Pseudo-code — `VerifyWorkflowHygieneAgainstLastLogRow()`

```
procedure VerifyWorkflowHygieneAgainstLastLogRow():
  ws = read("1-Projects/genesis-mythos-master/Roadmap/workflow_state.md")
  last_row = last_non_empty_table_row(ws, section="## Log")
  fm = frontmatter(ws)
  assert fm.last_ctx_util_pct == parse_ctx_util(last_row)
  assert fm.last_conf == parse_confidence(last_row)
  assert fm.current_subphase_index == parse_iter_phase(last_row)
  assert fm.last_auto_iteration == extract_queue_entry_id(last_row.StatusNext)
  # on mismatch: return HYGIENE_MISMATCH; do not claim deepen Success in automation
```

### Risk register v0 (3.4.9)

| Risk | Likelihood | Impact | Mitigation | Owner | Link |
| --- | --- | --- | --- | --- | --- |
| D-044 / RegenLaneTotalOrder_v0 undecided (dual-track until operator sub-bullet) | medium | high | Keep dual-track prose; run **GMM-DLG-01** before single-track ordering claims | Operator | [[decisions-log]] **D-044** |
| D-059 / Phase 4.1 tree guard (no tertiaries until ARCH-FORK logged) | medium | high | **GMM-TREE-01** + freeze `phase-4-1-*` minting | Architect | [[decisions-log]] **D-059** |
| D-032 / D-043 / D-045 execution evidence deferred (@skipUntil) | medium | high | Close tasks only with cited `queue_entry_id` / snapshots / repo paths | Automation + Operator | [[phase-3-4-8-high-context-util-policy-and-phase-4-stub-readiness-roadmap-2026-03-22-1205]] |

### Acceptance criteria (Given / When / Then)

1. **GMM-HYG-01 (hygiene row)**
   - **Given** a completed `RESUME_ROADMAP` run with context tracking **When** reading `workflow_state.md` **Then** YAML `last_ctx_util_pct`, `last_conf`, `current_subphase_index`, `last_auto_iteration` match the last `## Log` row (or document repair queue id in Notes).
2. **GMM-DLG-01 (decisions scan)**
   - **Given** `decisions-log.md` **When** scanning **D-044** **Then** PASS if no `Operator pick logged` sub-bullet implies A/B; FAIL if narrative asserts a pick without sub-bullet.
3. **GMM-TREE-01 (Phase 4.1 tree guard)**
   - **Given** roadmap tree under `Roadmap/` **When** listing new Phase 4.1 tertiaries **Then** none exist without **D-059** **ARCH-FORK-0x** label (stub secondary policy unchanged per **D-060**).

## Traceability matrix (task → evidence → owner)

| Task ID | Ladder origin (3.4.8) | Evidence type | Owner |
| --- | --- | --- | --- |
| GMM-HYG-01 | Post-`recal` hygiene | Log row + YAML parity | Automation |
| GMM-DLG-01 | Decisions-log verification | D-044 / D-059 scan notes | Operator + automation |
| GMM-TREE-01 | Phase 4.1 tree guard | Folder inventory + D-059 row | Architect |
| GMM-JHB-02 | Shallow deepen bundle (post-recal queue) | This note § Shallow deepen + `workflow_state` row citing `gmm-deepen-post-recal-20260322T1830Z` | Automation |
| GMM-VRF-01 | Validator compare-final `missing_roll_up_gates` | This note § Validator compare-final alignment — rollup HR matrix + literacy check | Junior + automation |
| GMM-L1-01 | L1 `missing_task_decomposition` + **pc-a1b** compare-final | This note § **A.1b** — code→evidence table + [[Ingest/Agent-Research/phase-3-4-9-a1b-promptcraft-roll-up-gaps-synthesis-2026-03-22-2145]] | Automation + junior |

## Validator compare-final alignment — `missing_roll_up_gates` (queue `gmm-deepen-post-recal-followup-20260322T1925Z`)

> **Architect:** Restates the compare-final hostile read `.technical/Validator/roadmap-auto-validation-20260322T195100Z-gmm-recal-followup-compare-final.md` for juniors — **vault-normative documentation only**; does **not** clear rollup **HOLD** rows, **D-044**, or **D-059**.

### What `missing_roll_up_gates` means here (distinct from **3.4.8** ladder rows)

| Macro slice | Authoritative rollup note (vault path) | Rollup `handoff_readiness` vs `min_handoff_conf` 93 | Advance under strict `handoff_gate` |
| --- | --- | --- | --- |
| Phase 3.2 secondary closure | `1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/phase-3-2-4-phase-3-2-secondary-closure-rollup-and-advance-readiness-roadmap-2026-03-22-1810.md` | **92 < 93** | **Not** eligible until **G-P3.2-REPLAY-LANE** clears (**D-044** A/B logged) |
| Phase 3.3 secondary closure | `1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/phase-3-3-4-phase-3-3-secondary-closure-rollup-and-advance-readiness-roadmap-2026-03-23-1200.md` | **92 < 93** | **Not** eligible until **HOLD** rows clear |
| Phase 3.4 secondary closure | `1-Projects/genesis-mythos-master/Roadmap/Phase-3-Living-Simulation-and-Dynamic-Agency/phase-3-4-4-phase-3-4-secondary-closure-rollup-and-advance-readiness-roadmap-2026-03-23-1935.md` | **92 < 93** | **Not** eligible until **G-P3.4-REGEN-INTERLEAVE** / **REGISTRY-CI** clear |

**Junior rule:** A tertiary (**3.4.9**) checklist **PASS** on **GMM-** tasks is **orthogonal** to rollup **HR ≥ 93**. Do **not** claim macro **advance-phase** eligibility from **3.4.9** prose alone.

### `safety_unknown_gap` (drift scalars + architect fork)

- **`drift_score_last_recal`** / **`handoff_drift_last_recal`** on [[roadmap-state]] remain **qualitative** roadmap-audit judgments until a **versioned drift spec** + input hash exists — see compare-final **regression_guard_vs_first_report** and [[workflow_state]] Notes **2026-03-22 19:20 UTC**.

### GMM-VRF-01 — rollup gate literacy check

1. **Given** the three rollup paths above **When** a stakeholder asks whether Phase **3.2 / 3.3 / 3.4** can **advance** **Then** answer with rollup **HR**, **`min_handoff_conf`**, and the **HOLD** row id — cite the **rollup note path**, not **3.4.9** alone.
2. **D-044** (**RegenLaneTotalOrder_v0** A/B) and **D-059** (**ARCH-FORK-01** vs **ARCH-FORK-02**) remain **open** in [[decisions-log]] — **no** operator picks added in this deepen run.

**Bootstrap `recal` trace (2026-03-22 21:05 UTC):** Layer-1 queue UUID **`2b8a47f4-f18e-44c0-9c08-2aa7a07fb02e`** · nested **`roadmap_handoff_auto`** first **`.technical/Validator/roadmap-auto-validation-20260322T210500Z-gmm-bootstrap-recal-2b8a-first.md`** — open **GMM-*** checkboxes remain **L1 `missing_task_decomposition`** debt until executed with cited evidence; **not** rollup **HR ≥ 93**.

### Queue / Layer-1 follow-up (policy)

Per **D-060** with **Ctx Util** still **>** threshold **80** after this sharpen pass, the **preferred** next queue entry remains **`RESUME_ROADMAP`** with **`params.action: "recal"`** unless **`user_guidance`** overrides (for example **`handoff-audit`** on the **3.4.8** / **3.4.9** bundle).

## Shallow deepen continuation (queue `gmm-deepen-post-recal-20260322T1830Z`)

> Architect: Post-**recal** operator queued an explicit **deepen** with **ctx already &gt; 80** — expand **junior pack** in-vault only; still emit **recal** follow-up per **D-060**.

### Machine-facing queue template (next preferred automation step)

After this row lands in `workflow_state`, Layer 1 should prefer **`RESUME_ROADMAP`** with **`params.action: "recal"`** (drift refresh) before another high-context **deepen**, unless **`user_guidance`** requests **`handoff-audit`** on **3.4.9** / **3.4.8** bundle.

```json
{
  "mode": "RESUME_ROADMAP",
  "params": {
    "action": "recal",
    "project_id": "genesis-mythos-master",
    "source_file": "1-Projects/genesis-mythos-master/Roadmap/workflow_state.md",
    "enable_context_tracking": true,
    "queue_next": true,
    "user_guidance": "D-060 follow-up after gmm-deepen-post-recal-20260322T1830Z shallow 3.4.9; ctx 83% > 80; D-044/D-059 still open."
  }
}
```

### Junior copy-paste checklist (this run)

1. Confirm **`workflow_state.md`** frontmatter **`last_auto_iteration`** = **`gmm-deepen-post-recal-20260322T1830Z`** and matches last **`## Log`** **`queue_entry_id`** substring.
2. Do **not** mark **3.4.8** ladder rows **`[x]`** without repo path / `queue_entry_id` evidence.
3. **Dual-track** regen narrative remains until **D-044** operator sub-bullet exists.

## Tasks

### Checklist (vault-normative — unchecked until evidence)

- [ ] Run **GMM-HYG-01** after next deepen/recal; record `queue_entry_id` in `workflow_state` Notes when repairing.
- [ ] Run **GMM-DLG-01** before claiming any regen interleaving story in new tertiaries.
- [ ] Run **GMM-TREE-01** before minting any `phase-4-1-*` tertiary roadmap file.

### Deferred execution (honest)

- [ ] CI / `ReplayAndVerify` / registry rows: **@skipUntil(D-032, D-043, D-045)** — unchanged from **3.4.8**.

## Dependencies

- **D-060** / **3.4.8** — upstream policy and ladder wording.
- **D-061** (this slice) — see [[decisions-log]].
- **D-044** / **D-059** — remain **open**; dual-track and tree-guard language is **mandatory** in any downstream spec.

## Automation notes (queue)

- **Ctx Util** estimated **87%** after **A.1b** deepen **`pcraft-gmm-deepen-a1b-20260322T201700Z-8e2c`** (**>** threshold **80%**): per **D-060**, **next automation-preferred follow-up** remains **`RESUME_ROADMAP`** **`action: recal`** before another full-context **deepen**; operator may override with **`handoff-audit`** on **3.4.9** / **3.4.8** if readiness review is the intent.
- Prior **84%** row: **`gmm-deepen-post-recal-followup-20260322T1925Z`** (shallow **3.4.9** without `enable_research`).
- Prior row (**82%**) from **`gmm-a1b-bootstrap-deepen-20260322T122045Z`**; this continuation adds **GMM-JHB-02** + § **Shallow deepen continuation** only (no new tertiary index).
