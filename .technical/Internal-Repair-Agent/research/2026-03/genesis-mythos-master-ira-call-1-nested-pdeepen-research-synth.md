---
created: 2026-03-22
pipeline: research
project_id: genesis-mythos-master
queue_entry_id: nested-pdeepen-research-synth
ira_call_index: 1
status: repair_plan
risk_summary: { low: 2, medium: 0, high: 0 }
validator_report: .technical/Validator/research-synthesis-genesis-mythos-master-20260322T221500Z-nested-pdeepen-first.md
synth_note: Ingest/Agent-Research/phase-3-4-9-bs-gmm-bootstrap-d060-junior-wbs-research-2026-03-22-2215.md
---

# IRA — research (validator-driven), call 1

## Context

Post–`research_synthesis` nested validator first pass reported **`needs_work`** / **`safety_unknown_gap`**: (1) A.1b eligibility narrative in the synthesis follows **Queue-Continuation-Spec** (four named `suppress_reason` exclusions) while **queue.mdc** A.1b step 4 only names two exclusions plus **`continuation_eligible === true`** — juniors may treat the synthesis as “the Layer-1 rule” without reconciling sources; (2) §2 operator matrix omits an explicit row for **`recal_util_high_threshold`** (default **~70%**) after **roadmap-deepen**, which phase **3.4.8** calls out separately from generic “~80%” context-util narratives.

## Structural discrepancies

1. **Spec-shaped vs queue-rule-shaped A.1b** — Table row “A.1b reader” (synthesis L26) lists four suppress_reason exclusions aligned with the Spec; validator notes queue.mdc step 4 does not enumerate `pipeline_failure` / `nested_attestation_failure` in that step, creating a **documentation triangulation gap** unless `continuation_eligible` always excludes those cases (not established in-note).
2. **Matrix gap** — §2 “Automation matrix” has ~90% overflow and “Ctx Util at/above threshold (often **80%**)” rows but **no** dedicated row for **post-deepen** auto-**`recal`** when **`context_util_pct ≥ recal_util_high_threshold`** (default **70%** per merged Config / **roadmap-deepen** / **3.4.8**).

## Proposed fixes

| # | Risk | Target | Action |
|---|------|--------|--------|
| 1 | low | Synthesis §1 | Add short **operator callout** after the A.1b table (or extend the “A.1b reader” cell): **audit A.1b by comparing** [[Queue-Continuation-Spec]] **durable-log reader** (four named exclusions) **vs** [[.cursor/sync/rules/agents/queue]] / **queue.mdc** A.1b step 4 (**`continuation_eligible`**, two named `suppress_reason` exclusions, TTL). State that **implementation truth** is the Layer-1 rule text + fields on the continuation record; the Spec’s four-name list is **authoritative for the log reader shape** until/unless queue.mdc step 4 is patched to match verbatim. |
| 2 | low | Synthesis §2 table | Insert one matrix row: **Signal:** `context_util_pct ≥ recal_util_high_threshold` (default **~70%**, verify merged **Second-Brain-Config** / **Parameters** / **roadmap-deepen** SKILL) **after roadmap-deepen** \| **Prefer:** **`RESUME_ROADMAP`** with **`params.action: "recal"`** \| **Notes:** distinct from mid-band / “often 80%” rows; cite **3.4.8** “Next actions” / queue follow-up narrative. Optionally one sentence in §2 heading clarifying **two different thresholds** (70% auto-recal gate vs ~80% examples elsewhere). |

**Constraints:** Apply only if synthesis file still matches validator-cited line anchors; if the note was edited concurrently, re-read before patch.

## Notes for future tuning

- **Research synthesis template** could require an “authority stack” line for any queue procedure: Spec vs synced rule vs Config keys.
- Repeated **recal_util_high_threshold** vs **context_util_threshold** confusion suggests Parameters.md cross-links in deepen handoffs.
