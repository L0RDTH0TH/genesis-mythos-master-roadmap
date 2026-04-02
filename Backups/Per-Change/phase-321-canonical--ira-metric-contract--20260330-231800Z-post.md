---
title: Phase 3.2.1 — Observation channel taxonomy
roadmap-level: tertiary
phase-number: 3
subphase-index: "3.2.1"
project-id: genesis-mythos-master
status: active
priority: high
progress: 52
handoff_readiness: 85
created: 2026-03-30
tags:
  - roadmap
  - genesis-mythos-master
  - phase-3
para-type: Project
links:
  - "[[Phase-3-2-Simulation-Rendering-Decoupling-and-Observation-Channels-Roadmap-2026-04-02-2300]]"
  - "[[Phase-3-1-1-Event-Bus-Ordering-and-Pub-Sub-Lanes-Roadmap-2026-03-30-1830]]"
  - "[[Phase-3-1-3-Sim-Visible-Classification-and-DM-Overwrite-Channel-Mapping-Roadmap-2026-04-02-0035]]"
  - "[[Phase-3-1-4-Persistence-Checkpoint-Boundaries-Roadmap-2026-04-02-2240]]"
  - "[[decisions-log]]"
---

> [!note] #handoff-review
> `handoff_readiness: 85` — tertiary **3.2.1** — **observation channel taxonomy** aligned to **3.1.1** **lane + subscription** model and **3.1.3** **`preview_shadow`** vs **committed** session boundary (re-affirmed with **3.1.4** checkpoint gates). **D-3.1.5-*** remain **execution-deferred** with binding loci unchanged. Next structural cursor **3.2.2**.

### Metric contract (progress vs handoff_readiness)

- **`progress` (52%):** slice **checklist breadth** — core NL, interfaces, GWT table, and pseudo-code sketch are in place; **open questions** and **execution-deferred** **D-3.1.5-*** hooks remain, so the slice is not at full “all closure artifacts shipped.”
- **`handoff_readiness` (85):** **delegation quality** — a junior engineer can implement from this note without inventing a second bus or violating **3.1** ordering; conceptual authority is clear even though rollup/CI proof rows stay **execution-deferred** per the conceptual track waiver.

## Phase 3.2.1 — Observation channel taxonomy

This **tertiary** names a **stable vocabulary** for **observation channels**: what renderers, operators, and narrative tools **may subscribe to**, how those channels **map onto** **3.1.1** **bus lanes** and **subscription registrations**, and how each channel declares **authority class** — **preview / shadow** vs **committed session** — without introducing a second bus or reordering **3.1** ordering rules.

## Scope

**In scope:**

- **Channel taxonomy (NL):** each **ObservationChannel** binds **(lane_id, subscription_pattern, authority_class)** where **lane_id** and **subscription_pattern** are **compatible** with **3.1.1** pub/sub sketches (same partition story; observation is **downstream filter**, not a publisher).
- **Alignment to 3.1.1 lanes:** **one primary bus lane** (or declared **lane set**) per channel for **replay-stable** ordering; cross-lane observation **merges** only via explicit **barrier** semantics deferred to execution — NL states **single-lane default** for conceptual closure.
- **preview_shadow vs committed:** channels carrying **`preview_shadow`** class (from **3.1.3**) **cannot** present as **checkpoint-eligible** or **authoritative SimEvent** export per **3.1.1** GWT **F** and **3.1.4** checkpoint boundary; **committed session** channels **only** surface facts that passed **tick closure** + **persistence** gates in **3.1.4** NL.

**Out of scope:**

- UI binding, frame pacing, or net-sync (execution-deferred).
- Changing **3.1.2** merge matrix or **3.1.5** WorkItem admission (upstream references only).

## Behavior (natural language)

1. **Channel registration (read path):** An **ObservationChannel** record names **which** `(lane, subscription_pattern)` slice of the bus log **feeds** this channel; **materialization** reuses **3.1.1** ordered iterators — **no** duplicate sort keys.
2. **Authority class:** **`preview_shadow`** channels **may** include **forge suggestion**, **dry-run shadow**, or **spectate** streams tagged **preview** in **3.1.1** sense; they **do not** advance **checkpoint sequence** or **authoritative export** cursor. **Committed** channels **only** attach to **post-tick** **checkpoint-visible** facts per **3.1.4**.
3. **DM / agency:** Observation channels **do not** grant **DM overwrite** or **agency** mutation — those remain **kernel-side** per **3.1.3** / **3.1.5**; misclassified UI traffic is **routing error**, not observation taxonomy.

## Interfaces

**Upstream (3.1.x):**

- **3.1.1** — [[Phase-3-1-1-Event-Bus-Ordering-and-Pub-Sub-Lanes-Roadmap-2026-03-30-1830]] — lane order, pub/sub, preview exclusion from authoritative replay.
- **3.1.3** — [[Phase-3-1-3-Sim-Visible-Classification-and-DM-Overwrite-Channel-Mapping-Roadmap-2026-04-02-0035]] — **`preview_shadow`** classification vocabulary.
- **3.1.4** — [[Phase-3-1-4-Persistence-Checkpoint-Boundaries-Roadmap-2026-04-02-2240]] — **committed** durability boundary vs preview lanes.

**Parent:**

- **3.2** — [[Phase-3-2-Simulation-Rendering-Decoupling-and-Observation-Channels-Roadmap-2026-04-02-2300]] — observation + preview vs committed **secondary** contract.

**Downstream (3.2.2+):**

- **3.2.2** — (next tertiary) — freshness / drift policy classes (**tick-aligned** vs **frame-aligned**) referenced as **execution-deferred** in **3.2** open questions.

**Outward guarantees:**

- Every **ObservationChannel** can be traced to **at least one** **3.1.1**-compatible **(lane, subscription_pattern)** pair; **no orphan** observation path that bypasses bus semantics.
- **preview_shadow** channels are **explicitly non-authoritative** in rollup narratives — consistent with conceptual track waiver for execution closure artifacts.

## Edge cases

- **Multi-lane “overview” channel:** If a product needs **merged** view across lanes, taxonomy marks it **composite** and requires **declared merge order** (execution) — default **conceptual** position: **not** a new bus order; **UI-side** merge only.
- **Stale tick display:** **Committed** channel may lag **one tick** behind **kernel**; **preview** may diverge further — **not** a contradiction if **authority_class** is **honest**.

## Open questions

- **D-3.1.5-faction-cohort-lane-vs-shard** — still **execution-deferred**; when resolved, **ObservationChannel** **lane_id** bindings may **subdivide** — **3.2+** / [[decisions-log]].
- **D-3.1.5-forge-sourced-preview-default** — ties **forge** → **preview_shadow** default; **execution-deferred**; **3.2.1** only **references** **3.1.3** mapping.

## Pseudo-code readiness

**Mid-technical (depth 3):** interface sketches — **no** production API.

### Channel record sketch

```
ObservationChannel =
  { channel_id
  , lane_id                    // aligns to 3.1.1 lane partition
  , subscription_pattern       // filters SimEvent stream (3.1.1 pub/sub)
  , authority_class            // committed_session | preview_shadow
  , checkpoint_visibility      // none | tick_scoped  (NL: ties 3.1.4)
  }
```

### Mapping to 3.1.1 subscription

```
materialize_observation_channel(ch : ObservationChannel, tick T) =
  ordered_events(ch.lane_id, T) filtered by ch.subscription_pattern
  then tag_export_stream(authority_class = ch.authority_class)
```

## GWT (Given / When / Then) — tertiary

| ID | Given | When | Then |
| --- | --- | --- | --- |
| GWT-3.2.1-A | Channel **C** declares **committed_session** | Tick **T** closes with checkpoint | **C** surfaces only **checkpoint-visible** facts per **3.1.4** |
| GWT-3.2.1-B | Channel **P** declares **preview_shadow** | Authoritative export/replay runs | **P** is **excluded** from authoritative stream (extends **3.1.1** GWT **F**) |
| GWT-3.2.1-C | New observation consumer registers | Bus **3.1.1** registry | **(lane, pattern)** pair is **valid** under parent secondary **3.1** — or **reject** at registration |

## Risk register (delta vs 3.2 secondary)

| Risk | Mitigation | Decision locus |
| --- | --- | --- |
| **Shadow channel mistaken for live** | **authority_class** + **GWT-3.2.1-B** | **3.2.1** NL + **handoff_readiness** |
| **Taxonomy invents parallel bus** | **Mapping** section **forces** **3.1.1** `(lane, pattern)` | Validator **incoherence** guard — **not** here |

## Research integration

> [!note] External grounding
> No new `Ingest/Agent-Research/` notes; pattern continuity from **3.1.1**, **3.1.3**, **3.1.4**, and parent **3.2**.

## Related

- Parent secondary: [[Phase-3-2-Simulation-Rendering-Decoupling-and-Observation-Channels-Roadmap-2026-04-02-2300]]
