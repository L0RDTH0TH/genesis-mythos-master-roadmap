---
created: 2026-03-28
pipeline: research
project_id: genesis-mythos-master
queue_entry_id: resume-deepen-phase4-2-dm-research-ctx-gmm-20260328T230000Z
ira_call_index: 1
status: repair_plan
risk_summary: { low: 5, medium: 1, high: 0 }
validator_primary_code: safety_unknown_gap
---

# IRA — research synthesis (validator pass 1)

## Context

Post–first-pass hostile `research_synthesis` validation on `Ingest/Agent-Research/phase-4-2-dm-perspective-read-model-research-2026-03-28-2330.md` returned **medium / needs_work** with **safety_unknown_gap**: traceability without a Raw bundle, **DmCameraBinding_v0** replay parity not closed against the phase 4.2 interface table, operator-discipline IDs (**D-060**, **D-027**, **D-044**) cited without decisions-log anchors, and weak external analogies (**deck.gl**, versioned Unity URL). Contaminated-report rule applied: treat validator gaps as minimum; expand coverage in the synthesis note only (parent must not edit frozen roadmap or decisions-log).

## Structural discrepancies

1. Synthesis admits **no Raw bundle** — web/CQRS claims are not independently auditable from the note body alone.
2. Phase roadmap table flags **DmCameraBinding_v0** replay-relevant fields **TBD** vs **CameraBinding_v0** parity; the note gestures at “derivable from ticks” and **D-027** carve-out but does not add a **stub table** or explicit **still-TBD** rows aligned to that WBS line.
3. **D-060** (checklist item 6), **D-027** (replay preimage), **D-044** (lanes) appear as shorthand without **[[1-Projects/genesis-mythos-master/Roadmap/decisions-log]]**-style pointer discipline in prose.
4. **deck.gl** citation risks **borrowed glitter** unless labeled non-stack analogy; Unity **/530/** path is version-fragile.

## Proposed fixes (for parent application)

See structured `suggested_fixes` in parent return JSON; apply in order **low → medium**, with snapshot/backup per project norms before editing the synthesis note.

## Notes for future tuning

- Research pipeline should default to a **minimal Raw stub** (even one screen of fetch titles + timestamps) in `Ingest/Agent-Research/Raw/` **or** an in-note **Fetch log** block on every `mcp_web_fetch` run to clear `safety_unknown_gap` early.
- Validator **next_artifacts** for 4.2 DM should explicitly require **interface-row closure** (strawman columns or explicit defer mirroring the phase table) whenever the source roadmap contains **TBD** rig rows.
