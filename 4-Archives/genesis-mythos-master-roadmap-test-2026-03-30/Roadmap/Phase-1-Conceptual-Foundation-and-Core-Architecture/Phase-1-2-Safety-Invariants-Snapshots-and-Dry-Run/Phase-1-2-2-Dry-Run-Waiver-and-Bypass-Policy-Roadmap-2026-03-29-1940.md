---
title: Phase 1.2.2 — Dry-run waiver and bypass policy
roadmap-level: tertiary
phase-number: 1
subphase-index: "1.2.2"
project-id: genesis-mythos-master
status: active
priority: high
progress: 38
created: 2026-03-29
tags: [roadmap, genesis-mythos-master, phase]
para-type: Project
links:
  - "[[Phase-1-2-Safety-Invariants-Snapshots-and-Dry-Run-Roadmap-2026-03-29-1731]]"
  - "[[Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-03-29-1730]]"
  - "[[Phase-1-2-Safety-Invariants-Snapshots-and-Dry-Run/Phase-1-2-1-Snapshot-Preimage-Binding-and-Audit-Trail-Roadmap-2026-03-29-1935]]"
handoff_readiness: 80
handoff_gaps:
  - "Execution track: waiver RBAC, ticket integration, automated enforcement of cooldowns"
---

## Phase 1.2.2 — Dry-run waiver and bypass policy

This slice defines **when** dry-run may be **skipped** or **waived**, **who** may authorize it, and what **audit fields** must appear so commits remain traceable. It extends parent **1.2** mermaid path `B -->|skip allowed| D[Explicit waiver logged]` and **1.2.1** `dry_run_skipped` / emergency bypass language. **D-027:** policy is stack-agnostic; enforcement UX and storage are **execution-deferred**.

### Scope

Covers **policy dimensions**: roles, reasons, time-bounds, pairing with preimage completeness, and conflict with “dry-run required” tickets from **1.2.1**. Does **not** define RBAC implementation, ticketing system APIs, or rate-limit storage.

### Behavior

1. **Waiver record:** Any commit that omits a dry-run when policy would normally run one must carry **`dry_run_skipped: { reason_code, approver_role, optional_ticket_ref }`** in the conceptual audit contract (mirrors **1.2.1** post-commit audit row).
2. **Bypass ladder:** (a) **Standard** — dry-run executed; `dry_run_artifact_ref` populated when required. (b) **Expedited** — dry-run skipped for latency with **two-person rule** or **break-glass role** (conceptual labels only). (c) **Emergency** — aligns with **1.2.1** hotfix path: **`bypass: reason + approver`** mandatory; preimage may be partial only if explicitly allowed by policy tier (**TBD** prod vs dev).
3. **Cooldown / abuse guard:** Repeated waivers on the same **stage_manifest_ref** family should trigger **escalation review** (conceptual); execution implements counters and alerts.
4. **Validator interaction:** If **1.2.1** `ManifestTicket.requires_dry_run` is true, a waiver **does not** silence the ticket — either run dry-run or **reject commit** until ticket is updated by an authorized **policy exception** recorded in audit.

### Interfaces

**Inward:** **1.2** dry-run gate diagram; **1.2.1** `ValidatePreimageForCommit`, boundary tickets, audit row. **Outward:** Operators and execution can implement `EvaluateDryRunPolicy(manifest, ticket, waiverRequest) -> Run | SkipWithWaiver | Reject` without redefining preimage fields.

### Edge cases

**False expedite:** Declaring “expedited” to skip cost without role approval → **fail closed** at execution. **CI vs local:** Local iteration may allow broader skip policy than CI — **deferred** to execution environments table. **Nondeterministic dry-run:** If dry-run is flaky, waiver may be paired with **stability ticket** rather than silent skip (**TBD**).

### Open questions

- Whether **two-person rule** is always required for expedited skip in production (**TBD**).
- Maximum **rolling waiver** window per project (**deferred** to ops).

### Pseudo-code readiness

Reader can sketch policy checks without inventing storage.

```text
function EvaluateDryRunPolicy(manifest: StageManifest, ticket: ManifestTicket, req: WaiverRequest | Skip) -> RunDryRun | SkipLogged | Reject
  if ticket.requires_dry_run and req is Skip and not req.has_authorized_waiver
    return Reject("dry-run required by ticket")
  if req is WaiverRequest
    if not req.approver_role in AllowedRoles(req.tier)
      return Reject("approver not authorized")
    return SkipLogged(req.to_audit_fields())
  return RunDryRun()

function AppendWaiverToAudit(auditRow: AuditRow, waiver: WaiverFields)
  // merges dry_run_skipped + bypass metadata into conceptual audit minimum from 1.2.1
```

### Tasks

- [ ] Execution: map `reason_code` enum and approver roles to concrete IAM.
- [ ] Execution: wire waiver UI / CLI flags to audit row writer.
- [x] Conceptual: waiver ladder + validator coupling + cooldown intent.

## Related

- [[Phase-1-2-Safety-Invariants-Snapshots-and-Dry-Run-Roadmap-2026-03-29-1731]] — dry-run vs commit gate.
- [[Phase-1-2-Safety-Invariants-Snapshots-and-Dry-Run/Phase-1-2-1-Snapshot-Preimage-Binding-and-Audit-Trail-Roadmap-2026-03-29-1935]] — preimage + ticket + audit.
