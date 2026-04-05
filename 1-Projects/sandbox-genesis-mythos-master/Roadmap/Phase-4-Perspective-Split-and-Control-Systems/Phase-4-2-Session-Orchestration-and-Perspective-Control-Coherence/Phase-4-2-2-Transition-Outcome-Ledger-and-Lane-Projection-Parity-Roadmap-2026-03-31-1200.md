---
title: Phase 4.2.2 — Transition outcome ledger and lane projection parity
roadmap-level: tertiary
phase-number: 4
subphase-index: "4.2.2"
project-id: sandbox-genesis-mythos-master
status: active
priority: high
progress: 55
progress_semantics: slice_narrative_depth_not_percent_complete
handoff_readiness: 86
created: 2026-03-31
tags:
  - roadmap
  - sandbox-genesis-mythos-master
  - phase-4
para-type: Project
links:
  - "[[Phase-4-2-Session-Orchestration-and-Perspective-Control-Coherence-Roadmap-2026-04-03-2120]]"
  - "[[Phase-4-2-1-Session-Scoped-Orchestration-Hooks-and-Perspective-Transition-Graph-Roadmap-2026-04-03-2125]]"
  - "[[Phase-4-Perspective-Split-and-Control-Systems-Roadmap-2026-03-30-0430]]"
  - "[[Phase-4-1-3-Consumer-Surface-Framing-and-Presentation-Time-Validation-Roadmap-2026-04-03-2110]]"
  - "[[decisions-log]]"
---

> [!note] #handoff-review
> `handoff_readiness: 86` — tertiary **4.2.2** — **TransitionOutcomeLedger** (append-only **transition_id** + **commit_seq** + **orchestration_hash** after **4.2.1** `apply_control_commit`) + **lane projection parity** predicates so **narrative** vs **rendering** lane snapshots both match the **canonical** post-orchestration projection (**4.1** adapters + **SessionOrchestrationEnvelope**). Binds **4.1.3** **presentation-time validation** to ledger rows (legibility vs subscription truth — not Phase **2.3** gates). **GWT-4.2.2-A–K** narrow **GWT-4.2-A–K**. **Next structural cursor:** **4.2.3** (continue **4.2** chain). **Queue / state reconcile:** deepen executed with live pre-mint cursor **`4.2.2`**; post-mint **`workflow_state.current_subphase_index: "4.2.3"`**; stale queue **`user_guidance`** referencing **4.1 rollup** ignored per Layer 2 instruction — authoritative slice **4.2.2** vs **4.1** (`followup-deepen-phase4-41-rollup-gmm-20260403T211500Z`).

## Phase 4.2.2 — Transition outcome ledger and lane projection parity

This **tertiary** closes the loop after **4.2.1** commits a control transition: the system must record a **replay-stable audit spine** (**TransitionOutcomeLedger**) and prove **both** consumer lanes see the **same** committed projection (**lane projection parity**) before **4.1.3** presentation surfaces may style or emphasize differently.

## Scope

**In scope:**

- **TransitionOutcomeLedger (NL)** — append-only rows keyed by **`commit_seq`** (monotonic per session), **`transition_id`** (from **4.2.1** graph edge), **`orchestration_hash`** (canonical digest of **SessionOrchestrationEnvelope** at commit), **`checkpoint_barrier_token`** (when **3.1.4** participated), **`lane_projection_digest_narrative`** / **`lane_projection_digest_rendering`** — must be **equal** when parity class is **strict**; when **emphasis-only** skew is allowed, digest inequality must still map to a **declared** **4.1.2** reconciliation class (no silent fork).
- **LaneProjectionParityPredicate** — deterministic boolean + reason code: `parity_ok | emphasis_skew_allowed | parity_violation` — **`parity_violation`** blocks further transitions until reconciled (single-writer path via **4.2.1** hooks).

**Out of scope:**

- Cryptographic hash algorithms, Merkle batching, or external audit export (**execution-deferred**).
- Forge-specific UI panels (**D-3.1.5-*** execution binding).

## Behavior (natural language)

1. **Commit then ledger:** Every successful `apply_control_commit` emits exactly one **TransitionOutcomeLedger** row before either lane may publish a new **presentation envelope** revision.
2. **Parity before emphasis:** **LaneProjectionParityPredicate** runs on the **canonical** projection; **4.1** lane adapters may only apply **emphasis** / **framing** deltas that preserve **`parity_ok`** or **`emphasis_skew_allowed`** per **4.1.2** matrix.
3. **Presentation-time validation:** **4.1.3** checks bind **operator-visible** framing to the **same** ledger row the lanes attest — no “UI-only” control truth.

## Interfaces

**Parent:**

- [[Phase-4-2-Session-Orchestration-and-Perspective-Control-Coherence-Roadmap-2026-04-03-2120]] — secondary **4.2** + **GWT-4.2-A–K**.

**Upstream:**

- [[Phase-4-2-1-Session-Scoped-Orchestration-Hooks-and-Perspective-Transition-Graph-Roadmap-2026-04-03-2125]] — hooks + graph + `apply_control_commit`.
- [[Phase-4-1-3-Consumer-Surface-Framing-and-Presentation-Time-Validation-Roadmap-2026-04-03-2110]] — presentation envelope vs ledger.

**Cross-lane:**

- [[Phase-4-1-2-Cross-Lane-Coherence-and-Emphasis-Reconciliation-Roadmap-2026-03-30-1200]] — allowed emphasis skew classes.

## Edge cases

- **Partial lane failure after commit:** If one lane fails to project, ledger row exists but **parity_violation** — freeze transitions until rollback/repair path (conceptual: **orchestration rollback token**; execution-deferred).
- **Replay audit:** Replaying **commit_seq** order must reproduce **lane_projection_digest** equality outcomes — **transition_id** alone is insufficient without **orchestration_hash**.

## Open questions

- Whether **emphasis_skew_allowed** should carry a **cap** count per session (**execution-deferred** policy).
- Minimum **ledger row** field set for **cross-session** audit bundles (**execution-deferred**).

## Pseudo-code readiness

**Mid-technical:** field lists for **TransitionOutcomeLedger** + parity predicate inputs; executable pseudo-code optional next tier (**4.2.3**) if stress-path closure requires it.

## Tertiary slice GWT — narrowed vs **GWT-4.2-A–K**

| Narrow ID | Parent GWT | Given | When | Then | Evidence (this slice) |
| --- | --- | --- | --- | --- | --- |
| **GWT-4.2.2-A** | **GWT-4.2-A** | Transition committed | Ledger row | Row exists before lane publish | § TransitionOutcomeLedger |
| **GWT-4.2.2-B** | **GWT-4.2-B** | **4.1** lanes | Post-commit projection | Digests match or declared skew | § LaneProjectionParityPredicate |
| **GWT-4.2.2-C** | **GWT-4.2-C** | Deferred work | Commit | Ordering visible in ledger | § Behavior (1) |
| **GWT-4.2.2-D** | **GWT-4.2-D** | Checkpoint token | Row | Barrier recorded | § Scope |
| **GWT-4.2.2-E** | **GWT-4.2-E** | Preview vs committed | Compare | Parity ties to ledger | § Behavior (2) |
| **GWT-4.2.2-F** | **GWT-4.2-F** | Handoff | Commit | Ledger preserves lineage | § Edge cases |
| **GWT-4.2.2-G** | **GWT-4.2-G** | Advisory gaps | Validator | Waiver explicit | [[roadmap-state]] |
| **GWT-4.2.2-H** | **GWT-4.2-H** | Coherence conflict | Parity | `parity_violation` blocks | § LaneProjectionParityPredicate |
| **GWT-4.2.2-I** | **GWT-4.2-I** | Operator legibility | Presentation | **4.1.3** binds ledger | § Behavior (3) |
| **GWT-4.2.2-J** | **GWT-4.2-J** | Stress path | Ledger growth | Disclosure without reinterpretation | § Open questions |
| **GWT-4.2.2-K** | **GWT-4.2-K** | **4.2** tertiaries | Next deepen | Evidence narrows in **4.2.3+** | this note |

## Research integration

- None for this slice (vault-first pattern).
