---
title: Phase 2.1.5 (Execution) — Replay ledger, canonical diff surface, and restore cursor
created: 2026-04-11
tags:
  - roadmap
  - execution
  - sandbox
  - procedural-generation
  - phase-2-1-5
project-id: sandbox-genesis-mythos-master
roadmap_track: execution
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.1.5"
status: in-progress
handoff_readiness: 85
priority: high
progress: 42
conceptual_counterpart: "[[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-5-Replay-Ledger-Canonical-Diff-Surface-and-Restore-Cursor-Roadmap-2026-03-30-2310]]"
para-type: Project
links:
  - "[[Phase-2-1-Pipeline-Stages-Seed-to-World-Roadmap-2026-04-11-2359]]"
  - "[[Phase-2-1-4-Bundle-Identity-Seam-Catalog-Stability-and-Replay-Diff-Roadmap-2026-04-12-1517]]"
  - "[[Phase-2-1-3-Staged-Delta-Bundles-Merge-Seams-and-Apply-Ordering-Roadmap-2026-04-12-1516]]"
---

# Phase 2.1.5 (Execution) — Replay ledger, canonical diff surface, and restore cursor

Execution tertiary **2.1.5** on the parallel spine under `Phase-2-1-Pipeline-Stages-Seed-to-World/`, mirroring conceptual **2.1.5** ([[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-5-Replay-Ledger-Canonical-Diff-Surface-and-Restore-Cursor-Roadmap-2026-03-30-2310]]). This slice closes the **2.1** execution chain with **ReplayLedgerEntry**, **CanonicalDiffSurface**, and **ResumeCursor** contracts—**text-only** interface seams and `text` pseudocode (no verbatim C++; **sandbox_code_precision** / allowlisted **`Task(research)`** deferred). Aligns to **2.1.1–2.1.4** bundle / merge / identity / replay-diff seams; **GMM-2.4.5** / CI closure remains **execution-deferred** unless evidenced.

## Scope (execution)

**In scope:**

- **ReplayLedgerEntry (execution):** one logical row per staged-bundle attempt after Stage **4** validation — records **bundle identity** (from **2.1.4**), **seam catalog revision**, **validation label set**, **resume cursor**, **stage window**, and **logical timestamp** for ordering audits.
- **CanonicalDiffSurface:** deterministic comparison between two **ledger-linked** bundle identities — change classes: **seam delta**, **ordered op delta**, **label delta**, **cursor movement** (schema-level; no binary format).
- **ResumeCursor:** `restore-required` vs `commit-ready`, **resumeFromSeam**, **resumeFromApplyOrdinal**, **requiresCatalogMigration** — ties to **2.1.3** apply ordering and **2.1.2** label seams.
- Alignment to **2.1.1–2.1.4:** replay ledger consumes **BundleIdentity**, **BundleDiffSummary**, and merge/identity vocabulary; does not redefine stage spine (**2.1** secondary).

**Out of scope:**

- Verbatim C++, storage engines, encryption, event-stream implementation.
- **GMM-2.4.5** / registry–CI closure rows (**execution-deferred**).

## Behavior (execution contract)

Actors: **pipeline runner**, **Stage 4 validator**, **replay/diff tooling**, **operator**.

1. After Stage **4**, emit **at most one** replay-ledger entry per staged-bundle attempt (idempotent key = bundle identity + attempt ordinal).
2. On validation **pass:** cursor **`commit-ready`**; pointer to Stage **5** boundary token (NL reference to commit seam from **2.1** secondary).
3. On validation **fail:** cursor **`restore-required`**; **resume pointer** to last trusted seam / apply boundary per **2.1.3** ordering.
4. **diff_replay(a, b)** reads two ledger-linked identities; if **catalog revision** differs, surface **`catalog_mismatch`** (delegates to **2.1.4** semantics); else structural deltas on seams, ops, labels, cursor.

## Interfaces (text — depth-3 tertiary)

- **`ReplayLedgerEntry`:** `{ bundleIdentity, seamCatalogRevision, validationLabelSet, resumeCursor, stageWindow, timestampLogical }`
- **`ResumeCursor`:** `{ resumeFromSeam, resumeFromApplyOrdinal, requiresCatalogMigration, state: commit-ready | restore-required }`
- **`CanonicalDiffSurface`:** `{ seamDelta[], opDelta[], labelDelta[], cursorDelta }`

Upstream:

- **2.1.4** — **BundleIdentity**, **SeamCatalogRevision**, **BundleDiffSummary**, replay equivalence.
- **2.1.3** — **StagedDeltaBundle**, apply ordering, merge seams.
- **2.1.2** — validation labels and merge seam catalog inputs.
- **1.2.4** — determinism / seed / replay vocabulary.

Downstream:

- **2.2** (execution) — intent resolver + hook mapping; replay ledger feeds validation-label and bundle-chunk narratives without re-deriving **2.1** seam state.

## Edge cases (execution)

- **Catalog revision mismatch on restore:** cursor valid only when migration policy maps old seams to new seams (NL gate; no silent apply).
- **Stale validation labels on partial replay:** restore **rejects** stale labels (aligns conceptual open question).
- **Ordering-only noise:** canonical surface distinguishes harmless reorder vs semantic seam/op drift (**2.1.4** diff rules).

## Pseudocode readiness (text — no verbatim C++)

```text
append_replay_ledger(bundle, validation_result, stage_window):
  cursor = derive_resume_cursor(bundle, validation_result)
  return ReplayLedgerEntry(
    bundleIdentity=bundle.identity,
    seamCatalogRevision=bundle.seamCatalogRevision,
    validationLabelSet=validation_result.labels,
    resumeCursor=cursor,
    stageWindow=stage_window,
    timestampLogical=next_logical_timestamp()
  )

canonical_diff_surface(ledger_a, ledger_b):
  if ledger_a.bundleIdentity.seamCatalogRevision != ledger_b.bundleIdentity.seamCatalogRevision:
    return CanonicalDiffSurface(catalogMismatch=true)
  return CanonicalDiffSurface(
    seamDelta=diff_seams(ledger_a, ledger_b),
    opDelta=diff_ops(ledger_a, ledger_b),
    labelDelta=diff_labels(ledger_a, ledger_b),
    cursorDelta=diff_cursor(ledger_a.resumeCursor, ledger_b.resumeCursor)
  )
```

## Intent mapping (execution)

| Intent | Owner | Evidence |
| --- | --- | --- |
| IM-2.1.5-L1 | Pipeline runner | Replay ledger row emitted after Stage 4 for each bundle attempt |
| IM-2.1.5-L2 | Validator | Pass/fail drives `commit-ready` vs `restore-required` cursor |
| IM-2.1.5-L3 | Diff tooling | `canonical_diff_surface` returns deterministic change classes |

## Acceptance criteria (execution-first)

| ID | Criterion | Status |
| --- | --- | --- |
| AC-2.1.5-E1 | Replay ledger row schema matches NL **ReplayLedgerEntry** + upstream **BundleIdentity** | Planned |
| AC-2.1.5-E2 | Restore cursor semantics consistent with **2.1.3** apply ordinal + **2.1.4** catalog rules | Planned |
| AC-2.1.5-E3 | Canonical diff distinguishes catalog mismatch vs structural drift | Planned |

## Related

- Conceptual source: [[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-5-Replay-Ledger-Canonical-Diff-Surface-and-Restore-Cursor-Roadmap-2026-03-30-2310]]
- Prior execution tertiary: [[Phase-2-1-4-Bundle-Identity-Seam-Catalog-Stability-and-Replay-Diff-Roadmap-2026-04-12-1517]]
