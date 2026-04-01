---
title: Phase 2.5.2 - Cross-sink correlation and deterministic timeline ordering
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.5.2"
project-id: genesis-mythos-master
status: active
priority: high
progress: 38
handoff_readiness: 86
created: 2026-03-31
tags:
  - roadmap
  - genesis-mythos-master
  - phase-2
para-type: Project
links:
  - "[[Phase-2-5-Deterministic-Decision-Telemetry-and-Post-Commit-Audit-Bridge-Roadmap-2026-03-31-1307]]"
  - "[[Phase-2-5-1-Telemetry-Envelope-Segmentation-and-Audit-Sink-Binding-Roadmap-2026-03-31-1320]]"
  - "[[Phase-2-4-5-Commit-Decision-Finalization-Replay-Safety-and-Audit-Handoff-Roadmap-2026-03-31-0345]]"
  - "[[decisions-log]]"
---

## Phase 2.5.2 - Cross-sink correlation and deterministic timeline ordering

This tertiary defines how sink-bound telemetry segments from **2.5.1** are stitched into a single operator-auditable **timeline** using stable **correlation keys** and **deterministic ordering** rules, without collapsing branch semantics or implying execution closure for `GMM-2.4.5-*` artifacts.

> [!info] Metrics rubric (frontmatter)
> **`progress`** — density of checklist / AC rows filled for this slice (implementation-agnostic narrative completeness). **`handoff_readiness`** — delegatability score (hand-off-audit semantics: traceability, interfaces, acceptance criteria); orthogonal to **`progress`** and may read higher when narrative is thin but delegate-ready.

## Scope

**In scope:**

- **Cross-sink correlation identity** — a minimal set of fields (e.g. `decision_correlation_id`, `frame_anchor_id`, `lineage_trace_id`) that deterministically tie segments emitted to different sink classes back to one finalized decision lineage from **2.4.5**.
- **Deterministic timeline ordering** — total ordering rules for audit-visible events when the same logical decision fans out to multiple sinks (authority_audit before operator_review when both apply; validator_compare events ordered after mandatory lineage segments).
- **Replay-stable ordering** — identical authority inputs yield the same ordered sequence of timeline rows across replays; no sink-specific reordering that could invert branch meaning.
- **Reference-only** pointers to execution-deferred anchors `GMM-2.4.5-SCHEMA`, `GMM-2.4.5-RETENTION`, `GMM-2.4.5-VALIDATOR-COMPARE-TABLE` — cited as **authority links**, not satisfied gates.

**Out of scope:**

- Physical clock synchronization, wall-clock skew compensation, or distributed tracing infrastructure.
- Storage retention policies and compaction (defer to execution + `GMM-2.4.5-RETENTION`).
- Role-based redaction of canonical lineage fields (may appear in **2.5.3+** as optional overlays).

## Behavior (natural language)

Inputs: segmented telemetry envelopes and sink binding descriptors from **2.5.1**, plus finalized decision identity from **2.4.5** (replay hash references, branch outcome, reason-code lineage).

Flow:

1. Assign a **decision_correlation_id** deterministically from stable finalization inputs (same inputs → same id).
2. For each sink-bound segment, attach the correlation id + ordering **epoch** (monotonic within one finalization) + **sink_lane** (authoritative_audit | operator_review | validator_compare).
3. Apply **timeline merge** rules to produce a single ordered list of audit-visible rows; conflicts resolve by fixed lane priority matrix (documented in Interfaces).
4. Emit a **timeline contract** summary block that lists ordered lanes and forbidden reorderings (e.g. never interleave deny escalation before commit lineage when both present).

## Interfaces

Upstream:

- **2.5.1** — segmented envelopes + sink binding ([[Phase-2-5-1-Telemetry-Envelope-Segmentation-and-Audit-Sink-Binding-Roadmap-2026-03-31-1320]]).
- **2.4.5** — finalization + replay-safety + audit handoff authority ([[Phase-2-4-5-Commit-Decision-Finalization-Replay-Safety-and-Audit-Handoff-Roadmap-2026-03-31-0345]]).

Downstream:

- Later **2.5.x** tertiaries may refine parity checks across sinks, compare-table row shapes, or operator redaction overlays.

Outward guarantees:

- Same finalized inputs → same `decision_correlation_id` and same canonical timeline ordering.
- Branch outcome (`commit` | `defer` | `deny_commit`) remains unambiguous after merge; no sink reordering may imply a different branch.
- `GMM-2.4.5-*` anchors remain **reference-only**; narrative does not claim schema/retention/compare-table implementation completeness.

## Acceptance criteria

- Given one multi-sink emission, all segments share one `decision_correlation_id` and appear in the deterministic order prescribed by the lane priority matrix.
- Given replay with identical inputs, timeline row count, lane sequence, and correlation id are unchanged.
- Given `deny_commit`, escalation trace segments appear in positions that preserve deny authority after lineage segments per fixed rules.
- Given missing optional sink segment, timeline still validates with explicit **absent_sink** marker (non-commit-safe for closure claims).

## Edge cases

- Partial sink failure after segmentation: timeline records emitted vs failed lanes without mutating correlation id.
- Duplicate sink delivery retries: idempotent row keys prevent double-counting in canonical ordering.
- Validator_compare lane only: still requires correlation id + lineage segments before compare rows.

## Open questions

- Whether operator_review rows may be omitted entirely when a feature flag disables human review (conceptual TBD; execution binds policy).
- Whether global monotonic **epoch** should be scoped per project, per world shard, or per session (execution-deferred).

## Pseudo-code readiness

Depth-3 NL contract is sufficient for implementation teams to derive correlation key generation, lane enum, and sort comparator without re-deriving branch semantics from **2.4.x**.

## Parent

- Secondary: [[Phase-2-5-Deterministic-Decision-Telemetry-and-Post-Commit-Audit-Bridge-Roadmap-2026-03-31-1307]]
