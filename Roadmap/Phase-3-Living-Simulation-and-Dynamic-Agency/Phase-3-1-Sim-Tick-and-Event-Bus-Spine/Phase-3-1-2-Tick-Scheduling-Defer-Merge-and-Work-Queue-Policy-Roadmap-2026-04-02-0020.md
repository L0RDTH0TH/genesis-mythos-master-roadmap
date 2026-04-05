---
title: Phase 3.1.2 — Tick scheduling, defer-merge, and work queue policy
roadmap-level: tertiary
phase-number: 3
subphase-index: "3.1.2"
project-id: sandbox-genesis-mythos-master
status: active
priority: high
progress: 48
progress_note: slice-local depth estimate vs sibling 3.1.1 (not Phase 3 rollup %)
handoff_readiness: 85
created: 2026-04-02
tags:
  - roadmap
  - sandbox-genesis-mythos-master
  - phase-3
para-type: Project
links:
  - "[[Phase-3-1-Sim-Tick-and-Event-Bus-Spine-Roadmap-2026-03-30-2213]]"
  - "[[Phase-3-1-1-Event-Bus-Ordering-and-Pub-Sub-Lanes-Roadmap-2026-03-30-1830]]"
  - "[[Phase-3-Living-Simulation-and-Dynamic-Agency-Roadmap-2026-03-30-0430]]"
  - "[[decisions-log]]"
---

> [!note] #handoff-review
> `handoff_readiness: 85` — tertiary **3.1.2** — **tick work queue** + **deferral ledger** + **deterministic merge policy** when closing tick `T` (extends **3.1** Behavior + **3.1.1** ordering/subscription contracts); `GMM-2.4.5-*` remain **reference-only**. **`pattern_only` on the CDR** means **no external research synthesis**, not weaker NL depth — this slice still meets conceptual **Scope / Behavior / Interfaces / Edge / Open Q / Pseudo-code readiness** + **GWT G–I**. Next structural cursor **3.1.3** (continue **3.1** chain — DM overwrite channel mapping / sim-visible classification).

## Phase 3.1.2 — Tick scheduling, defer-merge, and work queue policy

This **tertiary** closes the loop between **secondary 3.1**’s tick monotonicity promise and **3.1.1**’s ordered bus streams: it names **what work is admitted into tick `T`**, how **overflow** becomes **explicit deferral** (not silent merge), and how **merge outcomes** remain **replay-deterministic**—without naming thread pools, job systems, or persistence formats (execution-deferred).

## Scope

**In scope:**

- **Work queue (NL):** prioritized **WorkItem** records scheduled against **tick id** + **subsystem lane**; **admission** rules (what may enter the queue for `T` vs forced defer).
- **Deferral ledger:** append-only **DeferRecord** semantics — *why* deferred, *target tick* or *explicit barrier*, **no silent cross-tick merge** of incompatible writes (extends **3.1** Edge cases).
- **Merge policy matrix (sketch):** when two **compatible** writes target the same logical cell, **deterministic combine**; when **incompatible**, **deny closure** of `T` until policy chooses **defer** vs **escalate** (operator-visible; execution formats deferred).

**Out of scope:**

- Concrete scheduler implementation, QoS classes, or wall-clock timing (execution-deferred).
- Bus transport, async delivery, or consumer offset storage (see **3.1.1** deferrals).

## Behavior (natural language)

1. **Queue + tick closure:** The kernel **drains** eligible `WorkItem`s for tick `T` in **stable priority order** (subsystem order declared in policy table — execution assigns numbers). **Closure** of `T` is **invalid** if any admitted item remains **unresolved** without a **DeferRecord** or **merge outcome**.
2. **Deferral:** When capacity/backpressure triggers defer, the kernel **appends** a **DeferRecord** with **reason class**, **source item ids**, and **next eligibility** (tick `T+k` or **barrier** id). Deferred items **do not** participate in **merge** for `T`.
3. **Merge:** **Compatible** writes produce one **merged fact** + **merge provenance id** (for replay). **Incompatible** writes block closure unless **escalation** path is taken (named operator/DM lane — execution-deferred UI).

## Interfaces

**Upstream:**

- Parent secondary: [[Phase-3-1-Sim-Tick-and-Event-Bus-Spine-Roadmap-2026-03-30-2213]] — tick monotonicity, stall/backpressure risk register.
- **3.1.1:** [[Phase-3-1-1-Event-Bus-Ordering-and-Pub-Sub-Lanes-Roadmap-2026-03-30-1830]] — lane order + subscriptions; deferral does not reorder committed lane history for `T`.

**Downstream:**

- **3.1.3+** — DM overwrite channel mapping, agency drivers, persistence checkpoint boundaries (named in Phase 3 primary / **3.1** Interfaces).

**Outward guarantees:**

- **Replay:** For each tick `T`, the sequence **queue drain → merge outcomes → deferrals → bus publish (per 3.1 ordering)** is reconstructible from logged ids (NL).
- **No silent merge:** Any **combine** requires **compatibility class** pre-declared in policy sketch; otherwise **defer** or **block closure**.

## Edge cases

- **Starvation:** If deferrals accumulate, **stall** surfaces as **operator-visible** (extends **3.1** bus overload risk); no silent drop.
- **Cross-subsystem dependency:** Dependent work may require **barrier tick** — default: **defer to `T+1`** unless policy pins explicit **barrier** (execution format).
- **Preview sessions:** Preview **WorkItem** streams **must not** author **merge outcomes** that advance authoritative tick state (aligns with **3.1.1** preview tagging).

## Open questions

- **Default priority order** across environment vs agency vs systems — **execution-deferred** tuning; this note requires **declared** order, not numeric weights.
- Whether **merge provenance** ids feed **2.5-style** audit sinks on execution track — **execution-deferred**; conceptual slice names **linkage** only.

## Pseudo-code readiness

**Mid-technical (depth 3):** algorithm sketches below; no production API.

### Work queue drain (per tick)

```
eligible(T) = filter(work_queue, admitted_for_tick == T and not deferred)
for item in sort_by(eligible(T), policy_order):
  outcome = resolve_or_merge(item)
  if outcome == incompatible:
     block_tick_closure(T) unless escalation_path(item)
```

### Deferral record (minimal fields)

```
DeferRecord { source_ids, reason_class, resume_tick_or_barrier, merge_blocked: bool }
```

## Risk register (delta vs 3.1.1)

| Risk | Mitigation | Decision locus |
| --- | --- | --- |
| **Silent merge under load** | Explicit compatibility matrix + block closure | This note + execution policy tables |
| **Deferral explosion** | Stall visibility + operator escalation path | **3.1** acceptance + Phase 3 primary DM lanes |

## Testable acceptance (GWT) — tertiary

Aligns with secondary **3.1** acceptance **A–C** and **3.1.1** **D–F**; adds **queue/defer/merge** coverage.

| # | Given | When | Then |
| --- | --- | --- | --- |
| G | **Incompatible** writes in same tick **T** | Kernel attempts closure | Tick **does not** advance; **DeferRecord** or **escalation** required |
| H | **Compatible** writes | Merge policy applies | Single **merged** outcome + **provenance id**; replay matches |
| I | **Backpressure** defers work | Deferral recorded | No silent merge into unrelated cells; **next eligibility** stated |

## Research integration

> [!note] External grounding
> No new `Ingest/Agent-Research/` notes; continuity from **3.1** / **3.1.1** + Phase 3 primary ordering.

## Related

- Parent: [[Phase-3-1-Sim-Tick-and-Event-Bus-Spine-Roadmap-2026-03-30-2213]]
- Prior tertiary: [[Phase-3-1-1-Event-Bus-Ordering-and-Pub-Sub-Lanes-Roadmap-2026-03-30-1830]]
