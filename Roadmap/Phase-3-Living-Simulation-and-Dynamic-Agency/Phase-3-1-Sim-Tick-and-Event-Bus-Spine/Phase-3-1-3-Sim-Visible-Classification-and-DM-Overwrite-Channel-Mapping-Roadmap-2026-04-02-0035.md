---
title: Phase 3.1.3 — Sim-visible classification and DM overwrite channel mapping
roadmap-level: tertiary
phase-number: 3
subphase-index: "3.1.3"
project-id: godot-genesis-mythos-master
status: active
priority: high
progress: 46
progress_note: slice-local depth estimate vs siblings 3.1.1–3.1.2 (not Phase 3 rollup %)
handoff_readiness: 85
created: 2026-04-02
tags:
  - roadmap
  - godot-genesis-mythos-master
  - phase-3
para-type: Project
links:
  - "[[Phase-3-1-Sim-Tick-and-Event-Bus-Spine-Roadmap-2026-03-30-2213]]"
  - "[[Phase-3-1-2-Tick-Scheduling-Defer-Merge-and-Work-Queue-Policy-Roadmap-2026-04-02-0020]]"
  - "[[Phase-3-1-1-Event-Bus-Ordering-and-Pub-Sub-Lanes-Roadmap-2026-03-30-1830]]"
  - "[[Phase-3-Living-Simulation-and-Dynamic-Agency-Roadmap-2026-03-30-0430]]"
  - "[[decisions-log]]"
---

> [!note] #handoff-review
> `handoff_readiness: 85` — tertiary **3.1.3** — **sim-visible classification** tags on facts/events + **DM overwrite channel mapping** (which lanes may inject overwrite-class intents vs replay-only observation); extends **3.1** Behavior (DM overwrite classes), **3.1.1** (lanes/subscriptions), and **3.1.2** (queue/defer/merge closure); `GMM-2.4.5-*` remain **reference-only**. **`pattern_only` on the CDR** means **no external research synthesis**, not weaker NL depth. Next structural cursor **3.1.4** (persistence checkpoint boundaries under **3.1**).

## Phase 3.1.3 — Sim-visible classification and DM overwrite channel mapping

This **tertiary** makes **overwrite semantics** operational at the **bus + tick** seam: every **sim-visible fact** carries a **classification** that downstream subscribers (render, forge, operator tools, audit projections) can filter on **without** parsing world internals. It also maps **DM overwrite** work to **named channels** so **3.1.2** merge/defer decisions and **3.1.1** lane history stay coherent when a DM (or delegated tool) injects **live tweak** vs **structural regen** class work.

## Scope

**In scope:**

- **Sim-visible classification (NL):** a small **closed vocabulary** of tags on **SimEvent** / **observation facts** (e.g. `authoritative_tick`, `preview_shadow`, `dm_live_tweak`, `structural_regen_request`, `replay_only`) — enough for subscribers to enforce **Phase 3 primary** “live vs structural” contract without execution API names.
- **DM overwrite channel mapping:** which **intent lanes** / **subscription cohorts** may emit **overwrite-class** payloads; how those map to **3.1.1** pub/sub lanes and **3.1.2** **WorkItem** admission so **incompatible** overwrite attempts surface as **defer/block closure** rather than silent merge.
- **Continuity:** **FirstCommittedTickTrace** (**2.7.3**) remains the **first authoritative** sim boundary; classifications on tick `T≥1` must remain **replay-visible** alongside **3.1** acceptance **B**.

**Out of scope:**

- Concrete RBAC, net roles, or encryption (execution-deferred).
- Persistence file formats and checkpoint fsync (deferred to **3.1.4+** / execution).

## Behavior (natural language)

1. **Tag at publish:** Producers attach **sim_visible_class** when publishing **SimEvent** or observation facts; **default** is **authoritative_tick** when the publish path is post-commit and on the live sim spine.
2. **DM lanes:** **DM overwrite** intents enter through **named channels** (e.g. `dm_scene_edit`, `dm_npc_override`) that **pre-map** to **merge compatibility classes** from **3.1.2** — **live tweak** classes may merge with compatible world edits; **structural regen** classes **must not** silently combine with unrelated authoritative merges in the same tick without **escalation** (aligns with **3.1.2** G/H).
3. **Preview / shadow:** **Preview_shadow** classification **must not** produce **authoritative_tick** merge outcomes; aligns with **3.1.1** preview exclusion and **3.1** multi-session edge case.

## Interfaces

**Upstream:**

- **3.1:** [[Phase-3-1-Sim-Tick-and-Event-Bus-Spine-Roadmap-2026-03-30-2213]] — DM overwrite classes at secondary depth.
- **3.1.1:** [[Phase-3-1-1-Event-Bus-Ordering-and-Pub-Sub-Lanes-Roadmap-2026-03-30-1830]] — lane order + subscriptions; classification does not bypass **total order per lane**.
- **3.1.2:** [[Phase-3-1-2-Tick-Scheduling-Defer-Merge-and-Work-Queue-Policy-Roadmap-2026-04-02-0020]] — queue/defer/merge; overwrite channels declare **admission** into **WorkItem** streams per tick.

**Downstream:**

- **3.1.4+** — persistence checkpoint boundaries, agency drivers (named in **3.1** Interfaces).

**Outward guarantees:**

- **Filterability:** subscribers can drop **preview_shadow** or **replay_only** streams without touching sim core.
- **Traceability:** classification tags appear in **replay** story with **tick id** + **lane id** (NL).

## Edge cases

- **Conflicting class on same lane:** if two publishers attach **incompatible** classes to overlapping facts, **3.1.2** **incompatible** path blocks tick closure (extends **G**).
- **DM escalation:** when **structural_regen_request** collides with **live tweak** on same cell — **escalation** path required (operator-visible); no silent downgrade of class.
- **Forge read-only:** forge subscribers may receive **replay_only** exports — must not **re-publish** as **authoritative_tick**.

## Open questions

- **Granularity:** per-event vs per-bundle classification — **execution-deferred**; this note requires **at least** per-event for overwrite-class facts.
- Whether **weather** vs **faction** namespaces share **classification namespace** or orthogonal tags — **execution-deferred** (aligns with **3.1** Open questions).

## Pseudo-code readiness

**Mid-technical (depth 3):** sketches only.

### Classification attachment (publish path)

```
publish(sim_fact, lane_id, tick_id):
  assert sim_visible_class in ClosedVocabulary
  assert lane_id registered in 3.1.1 subscription catalog
  emit SimEvent(sim_fact, class=sim_visible_class, tick_id, lane_id)
```

### DM channel → merge class (sketch)

```
DM_CHANNEL_MAP = {
  "dm_live_tweak": compatible_with(world_edit_cell),
  "structural_regen_request": requires_escalation_or_defer
}
```

## Risk register (delta vs 3.1.2)

| Risk | Mitigation | Decision locus |
| --- | --- | --- |
| **Mis-tagged preview as authoritative** | Closed vocabulary + admission gate on WorkItem | This note + **3.1.2** |
| **DM lane bypasses merge matrix** | Channel→compatibility pre-map | This note + execution policy tables |

## Testable acceptance (GWT) — tertiary

Extends **3.1** A–C, **3.1.1** D–F, **3.1.2** G–I.

| # | Given | When | Then |
| --- | --- | --- | --- |
| J | A **sim-visible** fact on **authoritative** path | Published to bus | **Classification** is one of the closed vocabulary; subscribers can filter without world parse |
| K | A **DM overwrite** intent on mapped channel | Admitted to tick `T` | **Merge compatibility** follows **3.1.2** matrix; **structural** vs **live** conflicts **block** or **escalate**, no silent merge |
| L | **Preview_shadow** producer | Publishes during preview session | **No authoritative merge outcome**; does not advance authoritative tick state |

## Research integration

> [!note] External grounding
> No new `Ingest/Agent-Research/` notes; continuity from **3.1** / **3.1.1** / **3.1.2** + Phase 3 primary DM overwrite semantics.

## Related

- Parent: [[Phase-3-1-Sim-Tick-and-Event-Bus-Spine-Roadmap-2026-03-30-2213]]
- Prior tertiaries: [[Phase-3-1-1-Event-Bus-Ordering-and-Pub-Sub-Lanes-Roadmap-2026-03-30-1830]], [[Phase-3-1-2-Tick-Scheduling-Defer-Merge-and-Work-Queue-Policy-Roadmap-2026-04-02-0020]]
