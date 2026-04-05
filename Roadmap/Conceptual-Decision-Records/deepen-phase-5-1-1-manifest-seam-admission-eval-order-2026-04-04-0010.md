---
title: "CDR — Phase 5.1.1 tertiary (manifest, seam admission, evaluation order)"
created: 2026-04-04
tags:
  - roadmap
  - conceptual-decision-record
  - godot-genesis-mythos-master
para-type: Project
project-id: godot-genesis-mythos-master
parent_roadmap_note: "[[Phase-5-1-1-Ruleset-Manifest-Seam-Admission-and-Deterministic-Evaluation-Order-Roadmap-2026-04-04-0010]]"
queue_entry_id: followup-deepen-phase5-511-remint-gmm-20260404T060800Z
validation_status: evidence_on_disk
---

# Decision — Phase 5.1.1 tertiary (ruleset manifest + admission + order)

## Summary

Tertiary **5.1.1** commits **RulesetManifest** minimum fields, **seam admission** strictly against **3.4.1**, **deterministic evaluation order** via stable tuple sort **before** conflict winner logic (**5.1.2+**), and named load-time failure classes — preserving **Phase 2** non-bypass and **4.1.3** legibility for operator-visible errors.

## Alternatives considered

- **Implicit seam binding:** rejected — risks duplicate consumer truth vs **D-3.4-***.
- **Wall-clock tie-break:** rejected — breaks replay stability.

## PMG alignment

Supports **toolable, deterministic** rules authoring: manifests are **data**, ordering is **replay-stable**, failures are **named**.

## Validation evidence

[[Phase-5-1-1-Ruleset-Manifest-Seam-Admission-and-Deterministic-Evaluation-Order-Roadmap-2026-04-04-0010]] — **GWT-5.1.1-A–K**; parent [[Phase-5-1-Rule-Primitives-Plugin-Host-and-Conflict-Precedence-Roadmap-2026-04-03-2330]]. Queue **`followup-deepen-phase5-511-remint-gmm-20260404T060800Z`** — tertiary **5.1.1** re-mint under restored secondary **5.1**; `parent_run_id: eatq-e3dd8dca-gmm-5-1-1-deepen-20260404`.
