---
created: 2026-04-05
pipeline: roadmap
project_id: sandbox-genesis-mythos-master
queue_entry_id: followup-recal-post-611-high-ctx-sandbox-gmm-20260405T220000Z
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 3
  medium: 2
  high: 1
validator_report_path: .technical/Validator/roadmap-handoff-auto-recal-sandbox-gmm-20260406T002000Z-first-pass.md
reason_codes:
  - safety_unknown_gap
  - missing_roll_up_gates
---

# IRA — roadmap — sandbox-genesis-mythos-master (call 1)

## Context

Roadmap Layer 2 invoked IRA after nested `roadmap_handoff_auto` **first pass** (`ira_after_first_pass: true`). Validator verdict: **medium** / **needs_work**; **primary_code:** `safety_unknown_gap`; **secondary:** `missing_roll_up_gates`. Rollup surfaces (`roadmap-state`, `workflow_state`, `decisions-log`, `distilled-core`) agree on cursor **`6.1.2`** and drift **0.00**, but the **Conceptual autopilot** line for this queue id still claims nested **`Task(validator)`** / **`Task(internal-repair-agent)`** were unavailable — an attestation hole now that nested validation is running. Secondary **6.1** NL+GWT rollup is correctly **not** closed while **6.1.2** is unminted; on the conceptual track that should be explicitly framed as **advisory** (waiver-aligned) so validators do not over-read it as incoherence.

## Structural discrepancies

1. **Stale process narrative in `decisions-log.md`:** Autopilot bullet for `followup-recal-post-611-high-ctx-sandbox-gmm-20260405T220000Z` embeds **`#review-needed`** and “nested Task … not available” — contradicts current nested first-pass report on disk.
2. **Roll-up gate visibility:** `missing_roll_up_gates` is accurate structurally (no secondary **6.1** rollup row) but **expected** until the tertiary chain advances; rollup prose in Phase 6 should echo the existing conceptual waiver so consumers do not treat this as a hard hygiene failure.
3. **Definition of done (validator `next_artifacts`):** Mint **6.1.2**, reconcile autopilot, second validator pass with `compare_to_report_path` — IRA does not execute deepen; caller schedules pipeline work.

## Proposed fixes (for caller application)

| Order | Risk | Target | Action |
|------|------|--------|--------|
| 1 | low | `decisions-log.md` | Replace `#review-needed` / unavailable-host clause with attestation: nested `roadmap_handoff_auto` first pass → `.technical/Validator/roadmap-handoff-auto-recal-sandbox-gmm-20260406T002000Z-first-pass.md`; IRA → this report; second pass + `compare_to_report_path` per manifest. |
| 2 | low | `roadmap-state.md` | In Phase **6** summary (or **Consistency reports**), add one clause: **`missing_roll_up_gates`** for secondary **6.1** is **open** until tertiary **6.1.x** chain + secondary rollup; **advisory on conceptual track** per existing waiver in this file. |
| 3 | medium | `distilled-core.md` | In Phase **6** heading or canonical routing, add aligned sentence: secondary **6.1** rollup **deferred** until **6.1.2+** mint and rollup deepen — not execution/registry closure. |
| 4 | low | `workflow_state.md` | Optional single ## Log row: `handoff-audit` / `ledger-reconcile` class — documents IRA attestation + first-pass path (only if no duplicate row exists for same material). |
| 5 | medium | Nested validator | After edits + little val ok, run **second pass** with `compare_to_report_path: .technical/Validator/roadmap-handoff-auto-recal-sandbox-gmm-20260406T002000Z-first-pass.md`. |
| 6 | high | Roadmap deepen | **`RESUME_ROADMAP` `deepen`** tertiary **6.1.2** when queued — root closure for `missing_roll_up_gates` (snapshots + roadmap-deepen contract). |

## Notes for future tuning

- Autopilot lines should distinguish **historical host limitation** vs **current** nested ledger; prefer pointers to `.technical/Validator/*` and IRA reports over bare `#review-needed`.
- Conceptual projects should repeat **one-line advisory** next to any “in-progress secondary” when tertiaries remain — reduces false-positive `missing_roll_up_gates` severity inflation.
