---
created: 2026-03-29
pipeline: research
project_id: genesis-mythos-master
queue_entry_id: manual-invoke-research-synthesis
ira_call_index: 1
status: repair_plan
risk_summary: { low: 2, medium: 1, high: 0 }
validator_report_path: .technical/Validator/research-validation-genesis-mythos-master-20260329T140500Z-phase-4-1-5-d060-synthesis.md
synth_note_path: Ingest/Agent-Research/phase-4-1-5-d060-bounded-observability-cqrs-research-2026-03-29.md
---

# IRA — research synthesis post-validator (D-060 bounded observability)

## Context

Validator-driven invocation after first pass with `reason_codes`: `safety_unknown_gap`, `missing_evidence_anchors`. Parent already added: verbatim **Contract sketch** table (witness → advisory → digest), project-qualified `decisions-log` links, **STALE_SURFACE_v0** / projection-lag paragraph, and an explicit **delta vs junior handoff** blurb. This IRA re-reads the live synthesis against the hostile `next_artifacts` checklist and `decisions-log.md` (read-only).

## Structural discrepancies

1. **Rollup literal bind (partial):** The **Explicit non-claims** sentence asserts **rollup HR 92 < 93** and **REGISTRY-CI HOLD** while citing **D-141**. In `decisions-log.md`, **D-141** documents waiver scope and `@skipUntil(D-032)` / D-043 preimage and **no HR≥93 / no REGISTRY-CI PASS** language; the numeric **HR 92** and **REGISTRY-CI HOLD** phrasing is anchored in the **D-060** `#recal-review` row (and echoed in multiple deepen/handoff rows). A reader cannot verify those two literals from **D-141** alone — residual **`safety_unknown_gap`** traceability.

2. **Vault-first anchors (minor):** The contract excerpt is strong for **`missing_evidence_anchors`**. Remaining hygiene: **Related vault notes** still use **short wiki links** (`[[phase-4-1-4-...]]`, `[[phase-4-2-...]]`) without project path — same class of ambiguity the validator flagged for `[[decisions-log]]` before the patch.

3. **External depth:** Fowler CQRS + Event Sourcing + explicit **STALE_SURFACE_v0** mapping likely satisfies validator item 4; a second URL is optional polish, not required to clear the stated codes.

## Proposed fixes (for Research caller to apply under `Ingest/Agent-Research/` only)

See structured `suggested_fixes` in parent return payload; summary here matches that list.

## Notes for future tuning

- When synthesis cites **D-141** for execution-deferred replay language, **split** citations: **D-060** (or handoff rows) for **HR / REGISTRY-CI** literals, **D-141** for **@skipUntil(D-032)** / preimage scope — avoids overloading one decision id.
- Research validator `next_artifacts` item 2 ("each literal") is easier to auto-check if the note uses a small **fenced decisions-log excerpt** block per decision id.
