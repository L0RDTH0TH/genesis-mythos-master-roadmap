---
title: Phase 4.1.1.9 - Bundle verification witness row and rollback runbook
roadmap-level: task
phase-number: 4
project-id: genesis-mythos-master
status: active
priority: high
progress: 0
created: 2026-03-24
tags: [roadmap, genesis-mythos-master, phase-4, perspective, adapter, task, t-p4-01]
para-type: Project
subphase-index: "4.1.1.9"
handoff_readiness: 91
handoff_readiness_scope: "Quaternary runbook — deterministic witness rows for evidence cells after IngestEvidenceRef; rollback steps without HR≥93 or REGISTRY-CI PASS claims"
execution_handoff_readiness: 33
handoff_gaps:
  - "**G-P*.*-REGISTRY-CI HOLD** remains until 2.2.3 / D-020 execution evidence."
  - "Witness rows are vault-normative until repo harness exists; no green CI assertion."
links:
  - "[[distilled-core]]"
  - "[[workflow_state]]"
  - "[[roadmap-state]]"
  - "[[phase-4-1-1-8-operator-evidence-index-and-bundle-ingest-protocol-roadmap-2026-03-25-1200]]"
  - "[[phase-4-1-1-7-adapter-registry-rollup-handoff-bundle-and-closure-map-roadmap-2026-03-24-0926]]"
  - "[[decisions-log]]"
  - "[[genesis-mythos-master-roadmap-moc]]"
---

## Phase 4.1.1.9 - Bundle verification witness row and rollback runbook

**Parent chain:** [[phase-4-1-1-8-operator-evidence-index-and-bundle-ingest-protocol-roadmap-2026-03-25-1200]] → [[phase-4-1-1-7-adapter-registry-rollup-handoff-bundle-and-closure-map-roadmap-2026-03-24-0926]]

**Distilled-core ↔ phase spine:** [[distilled-core]] · [[workflow_state]] · [[roadmap-state]]

**Queue source:** `a1b-pc-resume-gmm-20260324T201830Z-7f3c` (empty-queue bootstrap continuation after post–little-val repair consumed)

### TL;DR

- Defines **witness rows** that record *who* approved an evidence target, *when*, and *which* bundle id was touched — without upgrading rollup **HR** or clearing **REGISTRY-CI HOLD**.
- **Rollback runbook** restores **TBD** when a proposed target fails auditable-path checks after the fact.

### Witness row schema (pseudo-code)

```text
type EvidenceWitnessRow_v0 = {
  gate_row_id: string,
  bundle_id: string,
  proposed_target: string,
  witness_actor: string,
  witness_utc: string,       // ISO-8601 Zulu
  workflow_log_anchor: string // queue_entry_id or last_auto_iteration id
}

function AppendWitness(row: EvidenceWitnessRow_v0, closure_table: Table) -> void:
  assert row.bundle_id in ["P4-1-1-BUNDLE-A", "P4-1-1-BUNDLE-B", "P4-1-1-BUNDLE-C"]
  assert not ClaimsPassWithoutCI(row.proposed_target)
  append closure_table.witness_appendix with row
```

### Rollback runbook

1. If **IngestEvidenceRef** returned a wikilink that later fails **`IsAuditablePath_v0`** (moved note, broken path), set cell back to **TBD** and append [[decisions-log]] row citing this note + witness **witness_utc**.
2. Do **not** delete historical **EvidenceWitnessRow_v0** rows — append a **superseded_by: rollback** marker row.
3. **registry_ci_hold_state** may only transition on **repo/CI evidence**, not rollback prose.

### Acceptance criteria

1. Every witness references a **gate_row_id** that exists on **4.1.1.7**.
2. No assertion that **rollup HR ≥ 93** or **REGISTRY-CI PASS** occurred.
3. Upward links to **4.1.1.8** and **4.1.1.7** present in body and `links`.

### Non-goals

- No substitute for **Lane-C** golden harness (**@skipUntil(D-032)**).
- No automatic **recal** queue line from this note alone (**D-060** matrix still applies on next high-util tracked run).

### Next quaternary (checkable path contract)

- **4.1.1.10** [[phase-4-1-1-10-auditable-path-check-contract-and-example-witness-appendix-roadmap-2026-03-25-0003]] — **`IsAuditablePath_v0`** + **EXAMPLE** witness appendix (post–pass2 validator **`next_artifacts`**).
