---
title: Phase 2.1.4 (Execution) — Bundle identity, seam catalog stability, and replay/diff contracts
created: 2026-04-12
tags:
  - roadmap
  - execution
  - sandbox
  - procedural-generation
  - phase-2-1-4
project-id: sandbox-genesis-mythos-master
roadmap_track: execution
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.1.4"
status: in-progress
handoff_readiness: 85
priority: high
progress: 40
conceptual_counterpart: "[[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-4-Bundle-Identity-Seam-Catalog-Stability-and-Replay-Diff-Roadmap-2026-03-30-2305]]"
para-type: Project
links:
  - "[[Phase-2-1-Pipeline-Stages-Seed-to-World-Roadmap-2026-04-11-2359]]"
  - "[[Phase-2-1-3-Staged-Delta-Bundles-Merge-Seams-and-Apply-Ordering-Roadmap-2026-04-12-1516]]"
  - "[[Phase-2-1-2-Boundary-Hook-Labels-and-Staged-Delta-Merge-Seams-Roadmap-2026-04-11-2100]]"
---

# Phase 2.1.4 (Execution) — Bundle identity, seam catalog stability, and replay/diff contracts

Execution tertiary **2.1.4** on the parallel spine under `Phase-2-1-Pipeline-Stages-Seed-to-World/`, mirroring conceptual **2.1.4** ([[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-4-Bundle-Identity-Seam-Catalog-Stability-and-Replay-Diff-Roadmap-2026-03-30-2305]]). This slice specifies **BundleIdentity** composition, **SeamCatalogRevision** monotonicity, **replay-equivalence**, and **deterministic bundle diff** for execution—**text-only** interface contracts and `text` pseudocode only (no verbatim C++; **sandbox_code_precision** deferred). Aligns to Phase **2** primary + **1.2.x** seed/replay vocabulary + **2.1.1–2.1.3** bundle/merge/order seams.

## Scope (execution)

**In scope:**

- **BundleIdentity** logical tuple: `seedBundleRef`, `seamCatalogRevision`, `applyFingerprint`, `participatingSeams[]` — consistent with **2.1.3** `bundleIdentity` / `bundle_identity_digest` story and **1.2.4** replay contracts.
- **Seam catalog stability:** monotonic **SeamCatalogRevision** token; bundles built against an obsolete catalog are **rejected** at Stage **4** unless an explicit migration path is named (NL only here).
- **Replay equivalence:** two bundles equivalent when **validation labels**, **seam resolution records** (from **2.1.3**), and **apply op sequence** match under the active catalog revision.
- **BundleDiffSummary:** seam-added / seam-removed / op reorder (only if allowed by partial order from **2.1.3**) / label drift — for tooling and regression narratives.

**Out of scope:**

- Verbatim C++, `static_assert`, or allowlisted URL citations (**sandbox_code_precision** — future slice with nested **`Task(research)`**).
- **GMM-2.4.5** / registry–CI closure rows (**execution-deferred** unless evidenced).
- Cryptographic digest algorithms, on-disk manifests, Merkle proofs (conceptual defers; execution maps later).

## Behavior (execution contract)

Actors: **pipeline runner**, **Stage 4 validator**, **diff/replay tooling**.

**Identity composition (execution):**

1. Start from **seed bundle identity** (Phase **2** spine + **1.2.4** vocabulary).
2. Bind **seamCatalogRevision** from the live merge seam catalog (**2.1.2** / **2.1.3**).
3. Compute **applyFingerprint** from canonical serialization order of **applyOpsOrdered** + **seamRecords** (per **2.1.3**).
4. List **participatingSeams[]** so partial regeneration traces which seams contributed.

**Catalog bump:** adding/removing seams bumps revision; **no silent rollback** — rollback is a **new forward** revision that restores definitions under new ids (per conceptual).

**Replay / diff:**

- **Replay equivalence** matches conceptual NL: same labels, seam records, apply sequence under catalog revision.
- **diff_bundle(A, B)** returns **catalog_mismatch** when revisions differ; else structural diff on ops and seam records.

## Interfaces (text — depth-3 tertiary)

- **`BundleIdentity`:** `{ seedBundleRef, seamCatalogRevision, applyFingerprint, participatingSeams[] }`
- **`SeamCatalogRevision`:** opaque monotonic string (maintained with pipeline graph edits)
- **`BundleDiffSummary`:** `{ addedSeams[], removedSeams[], opChanges[], labelChanges[], catalogMismatch? }`

Upstream:

- **2.1.3** — **StagedDeltaBundle** assembly, merge seams, apply ordering (feeds fingerprints).
- **2.1.2** — **ValidationDecisionLabels** + merge seam catalog inputs.
- **1.2.4** — determinism / seed bundles / replay vocabulary.

Downstream:

- **2.1.5** — replay ledger / canonical diff surface / restore cursor: [[Phase-2-1-5-Replay-Ledger-Canonical-Diff-Surface-and-Restore-Cursor-Roadmap-2026-04-11-0625]] (execution mirror of conceptual **2.1.5**).

## Edge cases (execution)

- **Catalog rollback forbidden silently:** revision numbers never decrease; forward-only migrations.
- **Same ops, different catalog revision:** not replay-equivalent until migration proves equivalence.
- **Empty participating seam set:** valid only for no-op bundles (aligns **2.1.3** empty bundle story).

## Pseudocode readiness (text — no verbatim C++)

```text
bundle_identity(seed_id, catalog_rev, apply_ops_ordered, seam_records):
  return BundleIdentity(
    seedBundleRef=seed_id,
    seamCatalogRevision=catalog_rev,
    applyFingerprint=canonicalize(apply_ops_ordered),
    participatingSeams=unique_seams_from(seam_records)
  )

diff_bundle(a, b):
  if a.seamCatalogRevision != b.seamCatalogRevision:
    return BundleDiffSummary(catalogMismatch=true)
  return structural_diff(a.applyOpsOrdered, b.applyOpsOrdered, a.seamRecords, b.seamRecords)
```

Verbatim C++ / standard quotes → later slice with **Task(research)** + allowlisted citations per **sandbox_code_precision**.

## Acceptance criteria (execution-first)

| ID | Criterion | Evidence target | Status |
| --- | --- | --- | --- |
| AC-2.1.4.E1 | BundleIdentity tuple binds seed + catalog revision + apply fingerprint + participating seams | `bundle_identity_fields` | Scaffolded (inline) — receipt: [[../../../workflow_state-execution]] log row **2026-04-12 15:17** (`queue_entry_id: followup-deepen-exec-phase2-tertiary214-sandbox-20260412T151700Z`) |
| AC-2.1.4.E2 | SeamCatalogRevision monotonic; obsolete bundles rejected or migrated explicitly | `catalog_revision_audit` | Planned |
| AC-2.1.4.E3 | Replay equivalence defined over labels + seam records + apply sequence | `replay_equivalence_checklist` | Planned |
| AC-2.1.4.E4 | BundleDiffSummary covers seam/op/label drift; catalog mismatch surfaced | `diff_bundle_export` | Planned |

## Intent Mapping

| Design intent target | Inspiration anchors | Execution mechanism | Validation signal |
| --- | --- | --- | --- |
| Stable logical bundle id | Conceptual **2.1.4** NL + **1.2.4** replay | `BundleIdentity` + `SeamCatalogRevision` | AC-2.1.4.E1–E2 |
| Replay tooling | Deterministic testing practice (pattern-only) | `diff_bundle` + equivalence relation | AC-2.1.4.E3–E4 |
| No silent catalog drift | Semver-ish revisioning, fail-fast on mismatch | revision monotonicity + `catalogMismatch` | AC-2.1.4.E2 |

## Lane comparand

| Concern | Sandbox (this lane) | Godot (reference) | Shared contract |
| --- | --- | --- | --- |
| Bundle identity | Logical tuple + text pseudocode | Scene/resource identity patterns (reference only) | Same replay-equivalence semantics at NL |
| Diff surface | `BundleDiffSummary` fields | Editor diff metaphors (reference only) | Seam/op/label granularity |

## Related

- Parent secondary: [[Phase-2-1-Pipeline-Stages-Seed-to-World-Roadmap-2026-04-11-2359]]
- Prior tertiary: [[Phase-2-1-3-Staged-Delta-Bundles-Merge-Seams-and-Apply-Ordering-Roadmap-2026-04-12-1516]]
