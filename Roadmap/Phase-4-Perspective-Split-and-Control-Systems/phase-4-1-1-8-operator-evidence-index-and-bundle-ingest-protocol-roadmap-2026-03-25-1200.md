---
title: Phase 4.1.1.8 - Operator evidence index and bundle ingest protocol
roadmap-level: task
phase-number: 4
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-25
tags: [roadmap, genesis-mythos-master, phase-4, perspective, adapter, task, t-p4-01]
para-type: Project
subphase-index: "4.1.1.8"
handoff_readiness: 90
handoff_readiness_scope: "Quaternary protocol — replace TBD evidence cells from 4.1.1.7 with auditable targets or explicit DEFERRED tokens; no HR≥93 or REGISTRY-CI PASS claims"
execution_handoff_readiness: 34
handoff_gaps:
  - "**G-P*.*-REGISTRY-CI HOLD** remains until 2.2.3 / D-020 execution evidence."
  - "Closure cells remain TBD until operator attaches resolvable wiki or VCS targets."
links:
  - "[[distilled-core]]"
  - "[[workflow_state]]"
  - "[[roadmap-state]]"
  - "[[phase-4-1-1-7-adapter-registry-rollup-handoff-bundle-and-closure-map-roadmap-2026-03-24-0926]]"
  - "[[phase-4-1-1-adapter-preimage-and-stable-column-layout-roadmap-2026-03-24-0018]]"
  - "[[decisions-log]]"
  - "[[genesis-mythos-master-roadmap-moc]]"
---

## Phase 4.1.1.8 - Operator evidence index and bundle ingest protocol

**Parent task:** [[phase-4-1-1-7-adapter-registry-rollup-handoff-bundle-and-closure-map-roadmap-2026-03-24-0926]]

**Distilled-core ↔ phase spine:** [[distilled-core]] (project-wide core decisions + dependency graph) · [[workflow_state]] (authoritative machine cursor / `## Log`) · [[roadmap-state]] (Phase summaries + consistency notes)

**Queue source:** `gmm-conceptual-deepen-one-step-20260325T120002Z` · cross-link pass `gmm-conceptual-crosslink-core-20260325T120003Z`

### TL;DR

- Describes how operators move **`pending-vault-evidence-bundle-4.1.1.7`** toward **auditable** links without claiming rollup closure or registry CI pass-through.
- Bundles **P4-1-1-BUNDLE-A/B/C** stay in their recorded states until evidence exists; this note adds **ingest rules**, not outcomes.

### Bundle-to-evidence ingest (pseudo-code)

```text
function IngestEvidenceRef(bundle_id, gate_row_id, proposed_target) -> EvidenceCell:
  assert bundle_id in ["P4-1-1-BUNDLE-A", "P4-1-1-BUNDLE-B", "P4-1-1-BUNDLE-C"]
  if proposed_target == "" or proposed_target == "TBD":
    return "TBD"
  if not IsAuditablePath(proposed_target):
    return "TBD"
  if ClaimsPassWithoutCI(proposed_target):
    FailClosed("no PASS inflation vs REGISTRY-CI HOLD")
  return WikilinkOrUri(proposed_target)
```

### Operator checklist

1. Walk **G-P4.1-ROLLUP-GATE-0x** rows on **4.1.1.7**; for each **TBD**, either attach a **real** target or leave **TBD** and log rationale on [[decisions-log]].
2. Never mark **`registry_ci_hold_state`** **cleared** from vault prose alone.
3. Prefer one evidence row per gate; split only when bundle boundaries require it.

### Staging table (copy-forward until 4.1.1.7 table updated)

| Gate id | Proposed target | Owner | State |
| --- | --- | --- | --- |
| G-P4.1-ROLLUP-GATE-02 | TBD | infra-ci | pending |
| G-P4.1-ROLLUP-GATE-03 | TBD | infra-ci | pending |

### Acceptance criteria

1. Protocol references **4.1.1.7** bundle ids and gate ids without renaming them.
2. No assertion that **rollup HR ≥ 93** or **REGISTRY-CI PASS** occurred.
3. Upward link to **4.1.1.7** is present in body and `links`.

### Next quaternary

- **4.1.1.9** witness + rollback runbook: [[phase-4-1-1-9-bundle-verification-witness-and-rollback-runbook-roadmap-2026-03-24-2304]]

### Non-goals

- No automatic **RECAL** queue line from this note.
- No clearing **D-032** / **D-044** / **D-059** deferrals by narrative.
