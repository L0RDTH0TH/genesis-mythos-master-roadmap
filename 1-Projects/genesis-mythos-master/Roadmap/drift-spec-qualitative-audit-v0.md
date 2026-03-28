---
title: Drift Spec — qualitative_audit_v0
created: 2026-03-24
tags: [roadmap, drift, safety]
project-id: genesis-mythos-master
status: in-progress
---

# Drift spec — qualitative_audit_v0

## Purpose

Define the comparability contract for roadmap recal drift fields so qualitative judgments are not treated as numeric trend guarantees without shared inputs.

## Contract

- `drift_metric_kind: qualitative_audit_v0` means `drift_score_*` and `handoff_drift_*` are audit judgments, not strict cross-run metrics.
- Numeric values are only comparable when both this spec version and the input bundle hash match.
- Until comparability prerequisites are present, handoff and rollup gates remain source-of-truth in rollup artifacts, not scalar drift deltas.

## Input Hash Anchor

- Spec version: `qualitative_audit_v0`
- Input bundle hash: `pending`
- Required sources for hash materialization: `roadmap-state.md`, `workflow_state.md`, active phase note, validator compare-final report.

## Links

- [[roadmap-state]]
- [[phase-4-1-player-first-perspective-read-model-and-rig-contracts-roadmap-2026-03-24-1201]]
- [[phase-4-1-1-1-adapter-row-layout-registry-and-changelog-roadmap-2026-03-24-0228]]
