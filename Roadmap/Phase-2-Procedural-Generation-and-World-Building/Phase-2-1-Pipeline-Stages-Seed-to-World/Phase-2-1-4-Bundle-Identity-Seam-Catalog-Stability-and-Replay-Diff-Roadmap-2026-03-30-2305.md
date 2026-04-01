---
title: Phase 2.1.4 — Bundle identity, seam catalog stability, and replay/diff contracts
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.1.4"
project-id: genesis-mythos-master
status: active
priority: high
progress: 40
handoff_readiness: 76
created: 2026-03-30
tags:
  - roadmap
  - genesis-mythos-master
  - phase-2
para-type: Project
links:
  - "[[Phase-2-1-Pipeline-Stages-Seed-to-World-Roadmap-2026-03-30-2205]]"
---

## Phase 2.1.4 — Bundle identity, seam catalog stability, and replay/diff contracts

This tertiary **extends** [[Phase-2-1-3-Staged-Delta-Bundles-Merge-Seams-and-Apply-Ordering-Roadmap-2026-03-30-1041]] (composition, merge seams, apply ordering). Here the focus is **identity and evolution**: how a **StagedDeltaBundle** is **named and logically keyed** for replay, how the **merge seam catalog** stays stable across partial regeneration and pipeline graph tweaks, and what **deterministic diff** means between two bundles for tooling — without re-specifying Stage 4 ordering rules already fixed in 2.1.3.

## Scope

**In scope:**
- **BundleIdentity**: stable logical id derived from seed bundle identity + seam catalog revision + ordered apply fingerprint (conceptual fields only).
- **Seam catalog revisioning**: monotonic **SeamCatalogRevision** so Stage 4 can reject bundles built against an obsolete catalog when the spine adds/removes seams.
- **Replay contract**: two runs with the same inputs must yield **bundle identities** that compare equal under the replay equivalence relation (same seam resolution records, same apply op ids modulo explicit renames in catalog migration).
- **Deterministic bundle diff**: NL contract for what “changed” between bundle A and B (seam-level, op-level, label-level) for debug/regression — not a binary format.

**Out of scope:**
- **Cryptographic** hash functions, Merkle proofs, on-disk manifests, or concrete digest byte formats (execution chooses those).
- Execution-track CI proving catalog migrations.

**In scope (NL):** A **logical** stable **bundle identity** and **replay-equivalence** relation — expressed as named fields and canonical ordering — without picking a concrete digest algorithm.

## Behavior (natural language)

Actors: **pipeline runner**, **validation gate (Stage 4)**, **tooling** (diff/replay inspectors).

**Bundle identity composition:**
- Starts from **seed bundle identity** (Phase 2 spine) and incorporates **SeamCatalogRevision** + a **canonical serialization order** for apply ops (already spine-aligned in 2.1.3).
- **Partial regeneration** that only touches a subgraph still emits a bundle whose identity reflects **which seams participated**; unchanged subgraphs contribute stable sub-fingerprints.

**Seam catalog stability:**
- Adding a seam is a **breaking** change unless **SeamCatalogRevision** bumps and old bundles are rejected or migrated explicitly.
- Removing a seam requires **migration notes** at NL level (which ops move to which seam); execution supplies tooling later.

**Replay / diff:**
- **Replay equivalence**: two bundles are equivalent if their **validation labels**, **seam resolution records**, and **apply op sequence** match under the catalog revision in effect.
- **Diff** reports: seam-added / seam-removed / op reorder (only if allowed by partial order) / label drift.

Regeneration:
- Re-running after a **catalog bump** without changing intent must either **fail fast** with “catalog mismatch” or run through an explicit **migration path** (out of scope to implement; in scope to **name** the decision).

## Interfaces

- **BundleIdentity:** `{ seedBundleRef, seamCatalogRevision, applyFingerprint, participatingSeams[] }` (NL).
- **SeamCatalogRevision:** opaque monotonic token (string) maintained with the pipeline graph.
- **BundleDiffSummary:** `{ addedSeams[], removedSeams[], opChanges[], labelChanges[] }`.

Upstream (2.1.3):
- **StagedDeltaBundle** and merge semantics; this note adds **identity + catalog revision** overlays.

Downstream:
- Commit boundary (Stage 5) may log which **BundleIdentity** was consumed for audit.

## Edge cases

- **Catalog rollback (forbidden silently):** revision numbers never decrease; rollback is a new forward revision that restores seam definitions under a new id.
- **Same ops, different catalog revision:** not replay-equivalent until migration proves equivalence.

## Open questions

- Whether **migration adapters** between catalog revisions are always explicit code modules or may be data-driven tables on the execution track.

## Pseudo-code readiness

> [!abstract] Illustrative only — not a crypto or storage spec
> The sketch below uses **logical tuple keys** (`stable_logical_key`) for identity — *not* cryptographic hashes. Execution maps these to concrete digests or content IDs under the out-of-scope rules above.

```
bundle_identity(seed_id, catalog_rev, apply_ops_ordered, seam_records):
  return stable_logical_key(seed_id, catalog_rev, canonicalize(apply_ops_ordered), canonicalize(seam_records))

diff_bundle(a, b):
  if a.seamCatalogRevision != b.seamCatalogRevision: return DiffSummary(catalog_mismatch=true)
  return structural_diff(a.applyOpsOrdered, b.applyOpsOrdered, a.seamRecords, b.seamRecords)
```

## Research integration

> [!note] External grounding
> No `Ingest/Agent-Research/` notes were bound this run; alignment is **pattern-only** from content-addressed build artifacts, semver-ish interface revisioning, and deterministic replay testing practice.
