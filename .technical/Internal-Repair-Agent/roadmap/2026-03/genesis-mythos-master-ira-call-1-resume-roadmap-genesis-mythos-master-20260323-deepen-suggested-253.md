---
created: 2026-03-23
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: resume-roadmap-genesis-mythos-master-20260323-deepen-suggested-253
ira_call_index: 1
status: repair_plan
risk_summary: { low: 3, medium: 3, high: 0 }
validator_report_path: .technical/Validator/roadmap-auto-validation-genesis-mythos-master-20260323-193500Z-first.md
parent_run_id: l1-7f2a9c41-eatq-253
---

# IRA call 1 — genesis-mythos-master — queue 253 (validator-driven)

## Context

Post–first-pass **`roadmap_handoff_auto`** for **RESUME_ROADMAP** deepen **3.4.4** returned **`needs_work`**, **`primary_code: missing_task_decomposition`**, plus **`safety_unknown_gap`**. Vault **state hygiene** is already aligned (validator §1): `workflow_state` frontmatter **72 / 82** matches the last **`## Log`** row for queue **253**. Residuals are **decomposition / traceability shape** (unchecked acceptance sketch, lone open optional task) and **honest HOLD** artifacts (**D-044** A/B, registry/CI) that must **not** be “fixed” by fabricated closure.

## Structural discrepancies

1. **Phase 3.4 secondary** — `### Acceptance sketch` lists three **unchecked** boxes that duplicate obligations already **adopted** under **D-052 / D-053 / D-054** with execution debt called out elsewhere; hostile review reads this as **missing decomposition** even though tertiaries exist.
2. **Phase 3.4.4 rollup** — Tasks include a **single unchecked** “Optional — handoff-audit” line while the body already **restates** a numbered closure trace; stale optional checkboxes read as **open work** without a DEFERRED ledger pattern (unlike sibling checked DEFERRED rows).
3. **`safety_unknown_gap`** — **D-044** sub-bullet correctly states A/B **not** logged; **G-P3.4-REGISTRY-CI** correctly points at **2.2.3** / **D-020**. Gap is **evidence path visibility**: mixed ambient+replay golden rows are not named as **explicit TBD stubs** on the registry anchor note (wikilink-only “PASS” risk per validator).
4. **Traceability** — Pre-deepen research path **`…-2215.md`** vs **`workflow_state`** log time **19:35** is the same **artifact clock vs run log** class called out in **`roadmap-state`** Notes for other notes; queue **253** should carry the same hygiene **once** in machine-adjacent Notes.

## Proposed fixes (for RoadmapSubagent apply order: low → medium → high)

See structured `suggested_fixes` in parent return payload; summary here mirrors that list.

## Notes for future tuning

- **Pattern:** Secondary **Acceptance sketch** sections left as raw `- [ ]` after tertiaries land trigger **`missing_task_decomposition`** even when **decisions-log** adoption rows exist — template should default to **DEFERRED / traceability** tables for “sketch” vs “execution closure.”
- **Pattern:** Optional **handoff-audit** bullets should use the same **`[x] DEFERRED (...)`** idiom as other non-completed-but-honest tasks on rollup notes.
- **D-044** remains the **single lever** for multiple **HOLD** rows; IRA cannot shorten that path without **operator** A/B — vault edits should **amplify** deferral visibility, not imply closure.
