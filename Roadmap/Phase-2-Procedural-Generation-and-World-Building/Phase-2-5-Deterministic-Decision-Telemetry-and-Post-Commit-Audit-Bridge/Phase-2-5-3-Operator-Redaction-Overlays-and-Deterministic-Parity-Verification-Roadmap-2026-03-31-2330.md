---
title: Phase 2.5.3 - Operator redaction overlays and deterministic parity verification
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.5.3"
project-id: sandbox-genesis-mythos-master
status: active
priority: high
progress: 40
handoff_readiness: 87
created: 2026-03-31
tags:
  - roadmap
  - sandbox-genesis-mythos-master
  - phase-2
para-type: Project
links:
  - "[[Phase-2-5-Deterministic-Decision-Telemetry-and-Post-Commit-Audit-Bridge-Roadmap-2026-03-31-1307]]"
  - "[[Phase-2-5-4-Sealed-External-Audit-Bundles-and-Compare-Table-Row-Interchange-Roadmap-2026-03-31-2335]]"
  - "[[Phase-2-5-2-Cross-Sink-Correlation-and-Deterministic-Timeline-Ordering-Roadmap-2026-03-31-2200]]"
  - "[[Phase-2-5-1-Telemetry-Envelope-Segmentation-and-Audit-Sink-Binding-Roadmap-2026-03-31-1320]]"
  - "[[Phase-2-4-5-Commit-Decision-Finalization-Replay-Safety-and-Audit-Handoff-Roadmap-2026-03-31-0345]]"
  - "[[decisions-log]]"
---

## Phase 2.5.3 - Operator redaction overlays and deterministic parity verification

This tertiary defines how **role-scoped redaction overlays** may mask or bucket sensitive fields in audit-visible timelines while preserving a single **canonical** replay identity and **deterministic parity checks** between canonical and overlay-derived views. Execution anchors `GMM-2.4.5-*` remain **reference-only** authority links (schema, retention, validator-compare tables).

> [!info] Metrics rubric (frontmatter)
> **`progress`** — density of checklist / AC rows filled for this slice (implementation-agnostic narrative completeness). **`handoff_readiness`** — delegatability score (traceability, interfaces, acceptance criteria); orthogonal to **`progress`**.

## Scope

**In scope:**

- **Redaction overlay contract** — a deterministic mapping from `decision_correlation_id` + timeline row keys to **overlay class** (`canonical` | `operator_summary` | `external_audit_bundle`) with explicit **field mask rules** per class (which lineage subfields may be replaced by stable placeholders vs omitted).
- **Canonical preservation rule** — redaction never rewrites branch outcome (`commit` | `defer` | `deny_commit`), `decision_reason_code` lineage path, or ordering epoch semantics from **2.5.2**; overlays only affect *presentation* or *export* slices, not authoritative ordering comparators.
- **Deterministic parity verification** — a checklist of **parity predicates** that must hold when comparing canonical timeline rows to redacted exports (same row count per logical event; no new commits implied; deny escalation rows remain after commit lineage when both present per **2.5.2** lane matrix).
- **Reference-only** carry-forward of `GMM-2.4.5-SCHEMA`, `GMM-2.4.5-RETENTION`, `GMM-2.4.5-VALIDATOR-COMPARE-TABLE` — cited as deferment IDs, not satisfied gates.

**Out of scope:**

- Cryptographic redaction proofs, differential privacy budgets, or KMS integration.
- Concrete storage of retention windows (`GMM-2.4.5-RETENTION`) or compare-table row payloads (`GMM-2.4.5-VALIDATOR-COMPARE-TABLE`).
- UX for operator review consoles (execution-deferred).

## Behavior (natural language)

Inputs: merged **timeline contract** from **2.5.2** (ordered lanes + correlation ids) + finalized decision lineage from **2.4.5**.

Flow:

1. Classify each timeline row for **redaction eligibility** by sink lane and sensitivity tier (e.g. raw intent payload vs hashed id only).
2. Apply **overlay class** to produce a **view bundle** — deterministic given canonical inputs + role id (same role + same canonical → same redacted bytes).
3. Run **parity verification** predicates before any export leaves the trust boundary: no branch flip, no missing mandatory deny lineage when `deny_commit`, correlation id stable across views.
4. Emit explicit **non-authority** markers on redacted exports so validator compare surfaces cannot treat overlays as canonical closure artifacts.

## Interfaces

Upstream:

- **2.5.2** — cross-sink correlation + deterministic timeline ordering ([[Phase-2-5-2-Cross-Sink-Correlation-and-Deterministic-Timeline-Ordering-Roadmap-2026-03-31-2200]]).
- **2.5.1** — segmented envelopes + sink binding ([[Phase-2-5-1-Telemetry-Envelope-Segmentation-and-Audit-Sink-Binding-Roadmap-2026-03-31-1320]]).
- **2.4.5** — finalization + replay hashes + audit handoff ([[Phase-2-4-5-Commit-Decision-Finalization-Replay-Safety-and-Audit-Handoff-Roadmap-2026-03-31-0345]]).

Downstream:

- **2.5.4** — sealed external audit bundles + compare-table row interchange ([[Phase-2-5-4-Sealed-External-Audit-Bundles-and-Compare-Table-Row-Interchange-Roadmap-2026-03-31-2335]]).
- Optional **2.5.5** may rollup / close the **2.5** chain.

Outward guarantees:

- Redacted views are **derivable** from canonical rows + overlay spec only; no hidden state in redaction path.
- Parity predicates are **replay-stable** — same inputs → same pass/fail bit for verification suite.
- `GMM-2.4.5-*` anchors remain reference-only; narrative does not claim schema/retention/compare implementation.

## Acceptance criteria

- Given one canonical timeline, applying overlay class `operator_summary` yields deterministic redacted rows and passes all parity predicates.
- Given `deny_commit`, redacted export still contains deny authority rows in positions compatible with **2.5.2** lane ordering (no reorder that implies commit).
- Given role without access to validator_compare lane, export marks **absent_lane** explicitly (non-closure-safe for that export only).
- Given identical canonical inputs, parity verification bit is identical across replays.

## Edge cases

- Overlay requests removal of a field required for parity: **reject overlay** with deterministic error code (do not silently weaken branch semantics).
- Multi-tenant roles: overlay key includes tenant id in deterministic hash input to prevent cross-tenant collisions (execution may bind store).
- Partial replay with redacted export only: parity suite documents **minimum canonical fields** still required.

## Open questions

- Whether `external_audit_bundle` may legally omit operator_review lane entirely (policy; execution binds).
- Whether redaction versioning should be tied to telemetry envelope version from **2.5** secondary or global audit contract version.

## Pseudo-code readiness

Depth-3 NL contract is sufficient for implementation teams to derive overlay specs, parity predicate tables, and export gate behavior without re-deriving **2.4.5** branch semantics.

## Parent

- Secondary: [[Phase-2-5-Deterministic-Decision-Telemetry-and-Post-Commit-Audit-Bridge-Roadmap-2026-03-31-1307]]
