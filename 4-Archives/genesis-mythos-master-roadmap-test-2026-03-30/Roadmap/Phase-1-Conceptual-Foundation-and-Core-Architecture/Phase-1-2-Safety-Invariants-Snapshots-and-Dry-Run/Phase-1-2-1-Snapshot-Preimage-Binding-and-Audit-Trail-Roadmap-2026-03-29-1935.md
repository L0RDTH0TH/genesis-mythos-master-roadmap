---
title: Phase 1.2.1 — Snapshot preimage binding and audit trail
roadmap-level: tertiary
phase-number: 1
subphase-index: "1.2.1"
project-id: genesis-mythos-master
status: active
priority: high
progress: 40
created: 2026-03-29
tags: [roadmap, genesis-mythos-master, phase]
para-type: Project
links:
  - "[[Phase-1-2-Safety-Invariants-Snapshots-and-Dry-Run-Roadmap-2026-03-29-1731]]"
  - "[[Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-03-29-1730]]"
handoff_readiness: 82
handoff_gaps:
  - "Execution track: concrete audit store, tamper-evident hashes, retention jobs"
---

## Phase 1.2.1 — Snapshot preimage binding and audit trail

This slice **binds** the Phase **1.2** snapshot preimage table to **commit-time validation** and an **audit trail** expectation: what must be true before `CommitIfValid` succeeds, and what record must exist afterward. **D-027:** field names are conceptual; execution chooses encodings.

### Scope

Covers **binding rules** (which preimage fields are required vs optional per commit class), **cross-checks** against stage manifest references, and **audit trail minimum content** (who/when/what snapshot). Does **not** specify databases, Merkle trees, or CI YAML.

### Behavior

1. **Pre-commit binding:** Before an authoritative transition, the runner holds a **SnapshotPreimage** value (see parent **1.2** table). **Required for any commit:** `seed_identity`, `schema_generation`, `stage_manifest_ref`. **Conditional:** `dry_run_artifact_ref` when policy ran dry-run; `override_fingerprint` when non-empty overrides were active; `intent_boundary_cursor` when the pipeline tracks intent ticks at the boundary.
2. **Validator coupling:** A stage-local validator may emit a **boundary ticket** (conceptual) that lists stage ids and output refs; `stage_manifest_ref` must **close** that ticket—i.e. cite the same boundary the validators last approved.
3. **Post-commit audit row:** After success, an **audit trail entry** (conceptual) records `snapshot_ref` (opaque id), preimage **subset** logged for humans, `operator_attestation` when available, and `dry_run_skipped` reason when applicable.

### Interfaces

**Inward:** Parent **1.2** preimage vocabulary; **1.1** stage/manifest language. **Outward:** Guarantees that execution can implement `ValidatePreimageForCommit(preimage, manifestTicket) -> OK | Reject` and `AppendAudit(snapshotRef, preimageSummary)` without redefining field names here.

### Edge cases

**Emergency bypass:** If human policy allows commit without full preimage (e.g. hotfix), the audit trail **must** record **`bypass: reason + approver`** — **TBD** whether bypass is ever allowed in production (**deferred**). **Replay:** Re-opening a snapshot for forensic replay is **out of scope**; only **forward commit binding** is defined here.

### Open questions

- Whether `intent_boundary_cursor` is mandatory for all commit classes or only simulation-heavy paths (**TBD**).
- Standard shape for **boundary ticket** vs free-form manifest rows (**deferred** to execution schema work).

### Pseudo-code readiness

Reader can sketch ordering without inventing storage.

```text
function ValidatePreimageForCommit(preimage: SnapshotPreimage, ticket: ManifestTicket) -> OK | Reject
  if missing preimage.seed_identity or preimage.schema_generation or preimage.stage_manifest_ref
    return Reject("incomplete preimage")
  if ticket.requires_dry_run and preimage.dry_run_artifact_ref is empty
    return Reject("dry-run required")
  if preimage.stage_manifest_ref does not close ticket.boundary_ids
    return Reject("manifest drift")
  return OK

function AppendAudit(snapshotRef: SnapshotRef, summary: PreimageSummary, attestation: OpAttestation | Skip)
  // execution: durable append-only log; conceptual: must exist per commit
```

### Tasks

- [ ] Execution: map preimage fields to concrete manifest columns.
- [ ] Execution: define `ManifestTicket` wire shape at a validated boundary.
- [x] Conceptual: commit-time binding rules + audit minimum.

## Related

- [[Phase-1-2-Safety-Invariants-Snapshots-and-Dry-Run-Roadmap-2026-03-29-1731]] — preimage table and dry-run gate.
- [[Phase-1-1-Layer-Boundaries-and-Modularity-Seams-Roadmap-2026-03-29-1731]] — stage validators referenced by `stage_manifest_ref`.
