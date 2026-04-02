---
created: 2026-03-29
pipeline: roadmap
project_id: genesis-mythos-master
queue_entry_id: resume-deepen-gmm-phase11-followup-20260329T183600Z
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 4
  medium: 0
  high: 0
validator_report_path: .technical/Validator/roadmap-auto-validation-20260329T184530Z.md
parent_run_id: eatq-gmm-20260329-layer1-8f2a
---

# IRA call 1 — genesis-mythos-master (validator-driven)

## Context

Post–first-pass `roadmap_handoff_auto` returned **medium** / **needs_work** with `missing_task_decomposition` and `safety_unknown_gap`. Workflow shows **Phase 1** active at subphase **1.1** with iterations on phase 1 &gt; 0, but `roadmap-state.md` still summarizes Phase 1 as **pending**. Phase 1.1 secondary is strong conceptually but lacks a **risk register v0**, has no **1.1.x** tertiaries, and the validator bundle omitted the **Phase 1 primary** path despite the workflow log referencing primary NL work. Fixes below are **append-only or summary-line sync** — no frozen-body overwrites.

## Structural discrepancies

1. **Rollup vs cursor:** `roadmap-state.md` “Phase summaries” lists Phase 1 as pending while `workflow_state.md` has `current_subphase_index: "1.1"` and deepen log rows through 18:36.
2. **Recursion / decomposition:** No `1.1.x` tertiary files; validator treats this as `missing_task_decomposition` unless an explicit intentional deferral is recorded on the 1.1 note.
3. **Secondary quality bar:** Phase 1.1 has edge cases and stub table but no dedicated **top risks + mitigations** section.
4. **Validation hygiene:** Next nested `roadmap_handoff_auto` must include the **Phase 1 primary** note in `state_paths` (and a consistent bundle list).

## Proposed fixes

Apply in order **low → medium → high** when gates pass. All items below are **low** blast radius.

| id | risk | target | action | summary |
|----|------|--------|--------|---------|
| ira-gmm-20260329-001 | low | roadmap-state.md | state_summary_sync | Phase 1 bullet: pending → in-progress aligned with cursor 1.1 |
| ira-gmm-20260329-002 | low | Phase 1.1 secondary note | append_section | Add `## Risk register v0` (3–5 risks + mitigations) |
| ira-gmm-20260329-003 | low | Phase 1.1 secondary note | append_section | Add dated waiver callout for deferred `1.1.x` tertiaries |
| ira-gmm-20260329-004 | low | workflow_state.md | append_section | Add nested-validator `state_paths` bundle incl. Phase 1 **primary** |

## Notes for future tuning

- When conceptual track deepens **secondary** before tertiaries exist, **roadmap-deepen** or hand-off builder should default-append **primary + secondary** to validator `state_paths` if primary was touched in the same log window.
- Consider auto-syncing **Phase summaries** in `roadmap-state.md` from `workflow_state` cursor on each deepen return to prevent stale “pending” lines.

## suggested_fixes (YAML — machine-readable)

```yaml
suggested_fixes:
  - id: ira-gmm-20260329-001
    risk_level: low
    target_path: 1-Projects/genesis-mythos-master/Roadmap/roadmap-state.md
    action: state_summary_sync
    patch_description: >-
      In "## Phase summaries", replace the Phase 1 line
      `- Phase 1: pending — conceptual foundation and core architecture`
      with in-progress wording that matches workflow_state, e.g.
      `- Phase 1: in progress — conceptual foundation and core architecture (workflow cursor 1.1; primary NL refined per 2026-03-29 log)`.
      Do not change other phase lines or frontmatter except if a separate explicit sync step is required.
    rationale: >-
      Removes stale rollup vs `current_subphase_index: "1.1"` and iterations_per_phase["1"] ≥ 1; addresses safety_unknown_gap hygiene without implying phase completion.

  - id: ira-gmm-20260329-002
    risk_level: low
    target_path: 1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layer-Boundaries-and-Modularity-Seams-Roadmap-2026-03-29-1731.md
    action: append_section
    patch_description: >-
      Append at end (after existing checklist) a new section `## Risk register v0` with a short table or bullet list of 3–5 risks drawn from this note's layers, generation graph, and intent path — each with mitigation/owner posture (conceptual only; execution typing deferred). Example risk classes: presentation mutating authoritative state; generation stage partial writes without rollback; intent bypass of validation; schema/version mismatch at stage boundaries; unbounded graph cycles without termination story.
    rationale: >-
      Validator secondary checklist expects explicit risk posture beyond "Edge cases"; satisfies needs_work bar without rewriting frozen conceptual core sections.

  - id: ira-gmm-20260329-003
    risk_level: low
    target_path: 1-Projects/genesis-mythos-master/Roadmap/Phase-1-Conceptual-Foundation-and-Core-Architecture/Phase-1-1-Layer-Boundaries-and-Modularity-Seams-Roadmap-2026-03-29-1731.md
    action: append_section
    patch_description: >-
      After the risk register (or immediately after it in the same edit pass), append `## Structural waiver — tertiaries 1.1.x (deferred)` containing a callout such as
      `> [!warning] #review-needed — Intentional partial tree` explaining that atomic `1.1.x` tertiary notes are **explicitly deferred** to the next deepen that mints children under 1.1, and naming which checklist recursion rows are waived until then. Optionally mirror one line in frontmatter `handoff_gaps` only if merge is non-destructive; prefer body callout first.
    rationale: >-
      Converts missing_task_decomposition into an auditable intentional partial per conceptual_v1 gate catalog (tertiaries or waiver).

  - id: ira-gmm-20260329-004
    risk_level: low
    target_path: 1-Projects/genesis-mythos-master/Roadmap/workflow_state.md
    action: append_section
    patch_description: >-
      Append `## Nested validator — state_paths bundle (next roadmap_handoff_auto)` listing vault-relative paths the RoadmapSubagent **must** pass on the next nested validator invocation, including at minimum:
      roadmap-state.md, workflow_state.md, decisions-log.md, distilled-core.md, roadmap MOC if used,
      `Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-03-29-1730.md` (**Phase 1 primary — required**),
      and `Phase-1-1-Layer-Boundaries-and-Modularity-Seams-Roadmap-2026-03-29-1731.md`.
      Note: RoadmapSubagent should map this list into the actual validator `state_paths` / hand-off field names; this section is the durable vault reminder.
    rationale: >-
      Closes safety_unknown_gap from primary path omission in the validation bundle; next pass can certify primary NL completeness from inputs.
```
