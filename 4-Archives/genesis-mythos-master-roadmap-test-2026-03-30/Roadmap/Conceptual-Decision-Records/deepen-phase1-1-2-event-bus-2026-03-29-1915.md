---
title: "CDR — Phase 1.1.2 event bus topology and mod-load order"
created: 2026-03-29
tags: [roadmap, conceptual-decision-record, genesis-mythos-master]
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-1-1-Layer-Boundaries-and-Modularity-Seams/Phase-1-1-2-Event-Bus-Topology-and-Mod-Load-Order-Roadmap-2026-03-29-1915]]"
decision_kind: deepen
queue_entry_id: resume-deepen-gmm-after-1-1-1-20260329T190500Z
master_goal: "[[Genesis-mythos-master-goal]]"
validation_status: pattern_only
related_research: []
---

## Summary

Minted tertiary **1.1.2** describing **partitioned-by-default** event domains, **bridge** rules aligned to Phase 1.1 layer edges, **registration bands** (core → world observation → player/operator → extension) so mods cannot pre-empt core validators, and a **sequencing / replay** hook at the conceptual layer. **D-027** preserved (no concrete broker or mod manifest).

## PMG alignment

Supports **Technical Integration** themes: clear **modularity** and **replaceability** between simulation, presentation, and extension without fixing a stack—implementation teams get a **topology + order contract** to implement against.

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
| --- | --- | --- | --- |
| Single global bus | Simple mental model | Cross-talk and accidental coupling | Conflicts with seam isolation from **1.1.1** |
| Fully decentralized (no global sequencing) | Minimal central coordination | Hard replay story | Product requires deterministic narrative for audit/replay |
| Fix mod-load order in one flat priority list | Easy to implement | Does not scale across domains | **Bands** preserve core safety while allowing extensions |

## Validation evidence

- Pattern: common **domain-separated** event models in sims and engines; no external synth notes this run.
- Parent alignment: [[Phase-1-1-Layer-Boundaries-and-Modularity-Seams/Phase-1-1-1-Replaceability-Seams-and-Hook-Surface-Roadmap-2026-03-29-1905]] **S-H** / **S-G** seam table.

## Links

- **Workflow log anchor:** `2026-03-29 19:15` — Target `Phase-1-1-2-event-bus-topology` (deepen pass 4, phase 1).
- [[Phase-1-1-Layer-Boundaries-and-Modularity-Seams/Phase-1-1-2-Event-Bus-Topology-and-Mod-Load-Order-Roadmap-2026-03-29-1915]]
- [[decisions-log]]
