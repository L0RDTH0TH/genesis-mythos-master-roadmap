---
title: "CDR — Phase 3.2.2 freshness / drift policy classes"
created: 2026-04-02
tags:
  - roadmap
  - conceptual-decision-record
  - genesis-mythos-master
para-type: Project
project-id: genesis-mythos-master
parent_roadmap_note: "[[Phase-3-2-2-Freshness-Drift-Policy-Classes-Roadmap-2026-04-02-2350]]"
decision_kind: deepen
queue_entry_id: followup-deepen-phase3-322-gmm-20260330T234600Z
master_goal: "[[Source-genesis-mythos-master-goal-2026-03-30-0430]]"
validation_status: pattern_only
related_research: []
---

# CDR — Phase 3.2.2 — Freshness / drift policy classes

## Summary

Chose **tick_aligned** vs **frame_aligned** **freshness** modes and **semantic_drift_bounded** vs **display_lag_disclosed** **drift** postures as **consumer-side** policy fields layered on **3.2.1** **ObservationChannel** records, aligned to **3.1.2** tick closure and **3.1.4** checkpoints without mutating **3.1.1** bus ordering.

## PMG alignment

Keeps **living simulation** **authoritative** on **tick** + **checkpoint** semantics while allowing **render** and **preview** UX to sample **between** ticks **only** under **preview_shadow** **authority**, preserving **Phase 2.7.3**-style **admission** stories into **Phase 3** **agency** (**3.1.5**).

## Alternatives and tradeoffs

| Alternative | Upside | Downside | Why not chosen |
| --- | --- | --- | --- |
| **Single freshness mode (tick only)** | Simpler mental model | Forces **all** UIs to **tick** cadence; **bad** for **responsive** **preview** | **Rejected** — **frame_aligned** **needed** for **spectate** / **forge** **UX** under **preview_shadow** |
| **Frame-first default** | **Smoother** **render** | **Risks** **authority** **leak** **without** **strict** **preview** **rules** | **Rejected** — **committed_session** **defaults** **tick_aligned** |

## Validation evidence

- **pattern_only** — **no** **Agent-Research** **synth** **this** **run**; **interfaces** **trace** **to** **3.1.x** **+** **3.2.1** **NL** **authority**.

## Links

- **Parent slice:** [[Phase-3-2-2-Freshness-Drift-Policy-Classes-Roadmap-2026-04-02-2350]]
- **Workflow anchor:** `workflow_state` **## Log** — **2026-04-02 23:50** — **Phase-3-2-2-Freshness-Drift-Policy-Classes** — `queue_entry_id: followup-deepen-phase3-322-gmm-20260330T234600Z`
