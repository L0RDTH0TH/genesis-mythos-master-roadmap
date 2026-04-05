---
title: Phase 2.5.4 - Sealed external audit bundles and compare-table row interchange
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.5.4"
project-id: sandbox-genesis-mythos-master
status: active
priority: high
progress: 42
handoff_readiness: 88
created: 2026-03-31
tags:
  - roadmap
  - sandbox-genesis-mythos-master
  - phase-2
para-type: Project
links:
  - "[[Phase-2-5-Deterministic-Decision-Telemetry-and-Post-Commit-Audit-Bridge-Roadmap-2026-03-31-1307]]"
  - "[[Phase-2-5-3-Operator-Redaction-Overlays-and-Deterministic-Parity-Verification-Roadmap-2026-03-31-2330]]"
  - "[[Phase-2-5-2-Cross-Sink-Correlation-and-Deterministic-Timeline-Ordering-Roadmap-2026-03-31-2200]]"
  - "[[Phase-2-4-5-Commit-Decision-Finalization-Replay-Safety-and-Audit-Handoff-Roadmap-2026-03-31-0345]]"
  - "[[decisions-log]]"
---

## Phase 2.5.4 - Sealed external audit bundles and compare-table row interchange

This tertiary defines how **sealed external audit bundles** package canonical timeline + redacted views (from **2.5.3**) into a **hash-chained interchange manifest** suitable for third-party verifier consumption, and how **conceptual row shapes** align to the execution-deferred `GMM-2.4.5-VALIDATOR-COMPARE-TABLE` contract without claiming implementation closure. Execution anchors `GMM-2.4.5-*` remain **reference-only** authority links.

> [!info] Metrics rubric (frontmatter)
> **`progress`** — density of checklist / AC rows filled for this slice (implementation-agnostic narrative completeness). **`handoff_readiness`** — delegatability score (traceability, interfaces, acceptance criteria); orthogonal to **`progress`**.

## Scope

**In scope:**

- **Sealed bundle manifest** — deterministic ordering of: (1) canonical `decision_correlation_id` + timeline row keys from **2.5.2**, (2) overlay class digest from **2.5.3** (`canonical` | `operator_summary` | `external_audit_bundle`), (3) hash-chain links per segment (previous-segment hash + segment body hash) so replay can verify integrity without operator UI.
- **External verifier handoff** — minimum consumer contract: which manifest fields a verifier must parse, how to reject bundles that omit mandatory deny lineage when `deny_commit`, and how to treat `absent_lane` markers from **2.5.3** as **non-closure** for validator-compare surfaces.
- **Compare-table row interchange** — conceptual mapping from **bundle row** columns to **expected** `GMM-2.4.5-VALIDATOR-COMPARE-TABLE` row shape (scenario id, branch outcome, reason-code path, parity predicates) as **schema alignment only**; narrative explicitly defers storage, retention, and live compare-table population to execution.
- **Reference-only** carry-forward of `GMM-2.4.5-SCHEMA`, `GMM-2.4.5-RETENTION`, `GMM-2.4.5-VALIDATOR-COMPARE-TABLE` — cited as deferment IDs, not satisfied gates.

**Out of scope:**

- Cryptographic suite selection, signing keys, or TSA profiles.
- Concrete compare-table storage, CI jobs, or validator binary interfaces.
- Legal hold / retention clock semantics (`GMM-2.4.5-RETENTION`).

## Behavior (natural language)

Inputs: **parity-verified** view bundle from **2.5.3** + canonical timeline from **2.5.2** + finalized closure references from **2.4.5**.

Flow:

1. Assemble **segment list** in deterministic order (same as **2.5.2** lane matrix traversal).
2. For each segment, compute **segment hash** over canonical bytes + overlay digest; chain to **manifest head hash**.
3. Emit **sealed external audit bundle** record with manifest hash, overlay class, explicit `non_authority` markers on redacted exports.
4. Map each bundle row to **compare-table conceptual columns** (alignment checklist for execution) — **no** claim that execution table rows exist.

## Interfaces

Upstream:

- **2.5.3** — redaction overlays + parity verification ([[Phase-2-5-3-Operator-Redaction-Overlays-and-Deterministic-Parity-Verification-Roadmap-2026-03-31-2330]]).
- **2.5.2** — cross-sink correlation + timeline ordering ([[Phase-2-5-2-Cross-Sink-Correlation-and-Deterministic-Timeline-Ordering-Roadmap-2026-03-31-2200]]).
- **2.4.5** — finalization + replay hashes + audit handoff ([[Phase-2-4-5-Commit-Decision-Finalization-Replay-Safety-and-Audit-Handoff-Roadmap-2026-03-31-0345]]).

Downstream:

- Optional **2.5.5** may close the **2.5** chain with rollup summary + handoff readiness for Phase 2.6 or Phase 3 bridge.

Outward guarantees:

- Same canonical inputs + overlay spec → same manifest head hash (deterministic sealing).
- Verifier can reject bundles that fail parity predicates from **2.5.3** before any compare-table join.
- `GMM-2.4.5-*` anchors remain reference-only; narrative does not claim schema/retention/compare implementation.

## Acceptance criteria

- Given a parity-passing export from **2.5.3**, sealing produces a deterministic manifest head hash and chain for all segments.
- Given `deny_commit`, sealed bundle still contains deny authority rows in positions compatible with **2.5.2** ordering; verifier rejects if deny rows missing.
- Given bundle row alignment checklist, **each** column maps to a named `GMM-2.4.5-VALIDATOR-COMPARE-TABLE` expectation or is marked `execution_deferred`.
- Given identical canonical inputs, sealing output is identical across replays.

## Edge cases

- Overlay requests a segment not present in canonical timeline: **reject seal** with deterministic error code.
- Verifier version skew: manifest includes **min verifier contract version** field (conceptual; execution assigns semver).
- Partial bundle without manifest head: **invalid** — cannot be joined to compare-table interchange.

## Open questions

- Whether **2.5.5** should be a **chain-complete** rollup (similar to **2.3.5** / **2.4.5**) or advance to **2.6** secondary under Phase 2.
- Whether sealed bundles should embed **replay hash** pointers from **2.4.5** verbatim or only hash-stable digests.

## Pseudo-code readiness

Depth-3 NL contract is sufficient for implementation teams to derive sealing manifests, verifier handoffs, and compare-table alignment checklists without re-deriving **2.4.5** branch semantics.

## Parent

- Secondary: [[Phase-2-5-Deterministic-Decision-Telemetry-and-Post-Commit-Audit-Bridge-Roadmap-2026-03-31-1307]]
