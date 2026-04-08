---
title: Phase 4.2 - Session orchestration and perspective control coherence
roadmap-level: secondary
phase-number: 4
subphase-index: "4.2"
project-id: godot-genesis-mythos-master
status: complete
priority: high
progress: 100
handoff_readiness: 86
created: 2026-04-03
tags:
  - roadmap
  - godot-genesis-mythos-master
  - phase-4
para-type: Project
links:
  - "[[Phase-4-2-3-Replay-Closure-Orchestration-Repair-and-Operator-Escalation-Readout-Roadmap-2026-03-31-1500]]"
  - "[[Phase-4-2-2-Transition-Outcome-Ledger-and-Lane-Projection-Parity-Roadmap-2026-03-31-1200]]"
  - "[[Phase-4-2-1-Session-Scoped-Orchestration-Hooks-and-Perspective-Transition-Graph-Roadmap-2026-04-03-2125]]"
  - "[[Phase-4-Perspective-Split-and-Control-Systems-Roadmap-2026-03-30-0430]]"
  - "[[Phase-4-1-Narrative-Rendering-and-Consumer-Surface-Lanes-Roadmap-2026-04-03-2015]]"
  - "[[Phase-3-1-2-Tick-Scheduling-Defer-Merge-and-Work-Queue-Policy-Roadmap-2026-04-02-0020]]"
  - "[[Phase-3-1-4-Persistence-Checkpoint-Boundaries-Roadmap-2026-04-02-2240]]"
  - "[[decisions-log]]"
---

> [!note] #handoff-review
> `handoff_readiness: 86` — secondary **4.2 rollup complete** — **session orchestration** + **perspective-control coherence** over **one** canonical authority lane; **GWT-4.2-A–K** parity checked against **4.2.1–4.2.3** and upstream **3.1.2** / **3.1.4** / **4.1** lane semantics. Queue **`user_guidance`** that named **secondary 4.1 rollup** / **`current_subphase_index: 4.1`** was **stale**; authoritative live cursor was **4.2 rollup** per [[workflow_state]] + Layer 1 `effective_target`. **Tertiary 4.2.1** — [[Phase-4-2-1-Session-Scoped-Orchestration-Hooks-and-Perspective-Transition-Graph-Roadmap-2026-04-03-2125]]; **4.2.2** — [[Phase-4-2-2-Transition-Outcome-Ledger-and-Lane-Projection-Parity-Roadmap-2026-03-31-1200]]; **4.2.3** — [[Phase-4-2-3-Replay-Closure-Orchestration-Repair-and-Operator-Escalation-Readout-Roadmap-2026-03-31-1500]].
> **Historical (rollup-time routing):** “Next structural cursor: **4** (Phase **4 primary rollup** …)” described the **post-4.2** queue at **rollup completion** — **superseded** by later global progression (Phase **4** primary rollup through Phase **6**; see [[roadmap-state]] / [[workflow_state]] ## Log). **Live next-step:** use [[workflow_state]] + [[roadmap-state]] (**`roadmap_track: execution`** post **2026-04-08 parity sync**) + [[Execution/workflow_state-execution]] (e.g. forward registry **`exec-forward-p42-ux-20260408`** for Phase **4.2** UX → execution mirror).

## Phase 4.2 - Session orchestration and perspective control coherence

This secondary slice defines how perspective control modes coordinate with session lifecycle and input scheduling without creating a second authority lane. It carries forward 4.1 lane semantics while binding to 3.1 scheduling/checkpoint constraints.

## Scope

**In scope:**

- Session lifecycle hooks for perspective-control transitions.
- Control coherence rules across narrative and rendering-facing lanes.
- Deterministic interaction boundaries for operator-visible perspective changes.

**Out of scope:**

- Renderer-specific camera implementation details.
- Input-device driver mappings.
- Execution-time performance tuning.

## Behavior (natural language)

1. Perspective control updates are accepted only through session-scoped orchestration hooks.
2. Lane-specific presentation rules may differ, but control state transitions remain singular and replay-safe.
3. Session transitions preserve ordering and checkpoint legality inherited from Phase 3 scheduling/durability rules.

### Player-facing UX authority (sandbox-canonical comparand)

**Canonical operator source (sandbox):** [[1-Projects/sandbox-genesis-mythos-master/Roadmap/Conceptual-Amendments/amend-frontend-player-ux-pc-swap-scheduling-lore-surface-2026-04-08-1400]] — decisions anchor **D-2026-04-08-frontend-player-ux-authority** in [[1-Projects/sandbox-genesis-mythos-master/Roadmap/decisions-log|sandbox decisions-log]]. The following bindings apply **in parallel** to this godot Phase **4.2** slice (same design intent as the sandbox lane; godot-specific execution evidence will land under `Roadmap/Execution/` when Phase **4** execution mirrors are minted on the parallel spine).

- **(A) Multi-PC swap (GTA V–class):** Active-character changes use a **zoom-out → traverse → possess** sequence; the prior body becomes NPC / off-camera per orchestration rules without a hard session reload. The **PerspectiveTransitionGraph** ([[Phase-4-2-1-Session-Scoped-Orchestration-Hooks-and-Perspective-Transition-Graph-Roadmap-2026-04-03-2125]]) must admit this transition **class** as a first-class **PerspectiveTransition** (labels + ordering vs session hooks).
- **(B) Schedules — propose / approve / override:** Players may **propose** in-world schedules; the **DM** has **exclusive approval** — schedules commit only after **DM approve** or **DM override** (including veto or rewrite). No player-unilateral hard commitment that bypasses the single authority lane; aligns with Phase **3** scheduling / checkpoint seams.
- **(C) Non-goals:** **Mobile / tablet spectator** client — **explicitly deprioritized** until a future product decision elevates it.
- **(D) Lore / history surface:** Markdown- or Obsidian-shaped trees are **product serialization, chronicle, and audit** — not an instruction to ship the vault’s **automation spine** (queues, MCP, PARA pipelines) inside the runtime.

**Execution track:** When `Roadmap/Execution/Phase-4-Perspective-Split-and-Control-Systems/Phase-4-2-…` execution notes exist, **`deepen`** there with AC/interface rows citing this block; pending registry: [[Execution/workflow_state-execution#Conceptual counterpart forward registry]].

## Interfaces

- Upstream lane semantics: [[Phase-4-1-Narrative-Rendering-and-Consumer-Surface-Lanes-Roadmap-2026-04-03-2015]].
- Tick scheduling and merge boundaries: [[Phase-3-1-2-Tick-Scheduling-Defer-Merge-and-Work-Queue-Policy-Roadmap-2026-04-02-0020]].
- Durability/checkpoint authority: [[Phase-3-1-4-Persistence-Checkpoint-Boundaries-Roadmap-2026-04-02-2240]].

## Edge cases

- Mid-transition perspective switch while deferred tasks are pending.
- Narrative lane and rendering lane receiving control updates at different cadences.
- Session handoff where preview surfaces lag behind committed control state.

## Open questions

- Should perspective transitions expose a standardized "operator override intent" marker at conceptual level, or remain execution-local?
- Which transition states require explicit "defer until checkpoint-safe" wording versus direct apply?

## Pseudo-code readiness

At secondary depth, this note captures interfaces and ordering constraints only. Pseudo-code belongs to tertiary decomposition.

## Secondary slice GWT (**GWT-4.2-A–K**) — evidence narrows at tertiaries

| ID | Given | When | Then | Evidence (tertiary / upstream) |
| --- | --- | --- | --- | --- |
| **GWT-4.2-A** | Session has active perspective mode | Mode transition requested | Transition enters orchestration path, not direct mutation | [[Phase-4-2-1-Session-Scoped-Orchestration-Hooks-and-Perspective-Transition-Graph-Roadmap-2026-04-03-2125]] + **3.1.2** |
| **GWT-4.2-B** | Lane adapters active from **4.1** | Control state changes | Both lanes reflect one canonical state transition | [[Phase-4-1-Narrative-Rendering-and-Consumer-Surface-Lanes-Roadmap-2026-04-03-2015]] rollup + **4.2.2** ledger parity |
| **GWT-4.2-C** | Deferred tasks pending | Perspective switch occurs | Ordering contract remains deterministic | **3.1.2** + **4.2.1** transition graph |
| **GWT-4.2-D** | Checkpoint boundary unresolved | Control transition requests persistence-sensitive action | Transition is constrained by durability boundary | **3.1.4** + **4.2.1** hooks |
| **GWT-4.2-E** | Preview and committed surfaces differ | Operator inspects state | No authority inversion between preview and committed lanes | **4.1** + **3.2.x** + **4.2.2** lane projection |
| **GWT-4.2-F** | Session handoff in progress | Control input arrives | Handoff policy preserves replay-safe lineage | **4.2.1** + **4.2.3** replay closure |
| **GWT-4.2-G** | Execution-only closure gates missing | Validator reports advisory rollup gaps | Conceptual progress remains valid with explicit deferral | [[roadmap-state]] conceptual waiver |
| **GWT-4.2-H** | Control coherence conflict detected | Reconciliation policy runs | Conflict class documented without second-truth lane | **4.2.2** ledger + **4.1.2** coherence |
| **GWT-4.2-I** | Operator legibility requirements apply | Transition shown in UI lane | Legibility retained while respecting control authority | **4.1.3** + **4.2.2** presentation binding |
| **GWT-4.2-J** | Perspective control enters stress path | Cadence drops | Disclosure policy applies without state reinterpretation | **3.2.2** + **4.2.3** escalation readout |
| **GWT-4.2-K** | Tertiary chain **4.2.1–4.2.3** complete | Secondary rollup asserts parity | **GWT-4.2-*** rows satisfied without silent gaps | **4.2.1**, **4.2.2**, **4.2.3** + this rollup section |

## Rollup closure (NL checklist + GWT parity)

- [x] **Scope / Behavior / Interfaces / Edge cases** — stated at secondary depth; tertiaries **4.2.1–4.2.3** carry hook graph, ledger parity, replay/repair/escalation closure.
- [x] **No second authority lane** — perspective/control transitions remain **session-scoped** and **replay-safe** vs **4.1** dual **consumption** lanes (one sim truth).
- [x] **GWT-4.2-A–K** — evidence column aligned to **4.2.1–4.2.3** + upstream **3.1.2**/**3.1.4**/**3.2.2**/**4.1**; execution wire formats and perf remain **execution-deferred** per [[decisions-log]].
- [x] **Stale queue reconcile** — same `queue_entry_id` previously carried **4.1 rollup** text while vault cursor was **4.2**; this rollup run matches **workflow_state** **`current_subphase_index: "4.2"`** pre-completion, then advances cursor to **4** (Phase 4 primary rollup gate) in [[workflow_state]].

## Research integration

- None for this slice (vault-first pattern).
