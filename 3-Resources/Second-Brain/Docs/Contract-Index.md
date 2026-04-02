# Contract Index (Subagents, Safety, Roadmap)

**Version: 2026-04**

Single-page index of the core contract, safety, and ledger docs the agents and validators rely on. Use this as the first stop for tooling or audits that need to discover the right files.

---

## Core safety and helper contracts

- **Subagent Safety Contract**  
  - Path in vault: `3-Resources/Second-Brain/Subagent-Safety-Contract.md`  
  - Export/Git path: `Docs/Core/Subagent-Safety-Contract.md`  
  - Purpose: Single source of truth for:
    - Task harden pass and capability probing.
    - Helper profiles (`fast` / `balance` / `extreme`) and helper graphs.
    - Mandatory vs optional nested helpers (Validator, IRA, Research).
    - Inline I/O fallback for roadmap when MCP is unavailable.
    - Honesty rules (no pretending helpers ran when they did not).

- **Safety Invariants**  
  - Path in vault: `3-Resources/Second-Brain/Docs/Safety-Invariants.md`  
  - Export/Git path: `Docs/Safety-Invariants.md`  
  - Purpose: Global safety rules for all pipelines:
    - Backups, per-change snapshots, confidence bands.
    - “No destructive action unless high band + snapshot”.
    - Nested subagent policy (orchestration boundaries).
    - Helper profile + honesty summary (mandatory helpers, no misrepresentation).

- **Nested Subagent Ledger Spec**  
  - Path in vault: `3-Resources/Second-Brain/Docs/Nested-Subagent-Ledger-Spec.md`  
  - Export/Git path: `Docs/Nested-Subagent-Ledger-Spec.md`  
  - Purpose: Schema and attestation rules for `nested_subagent_ledger`:
    - Step fields, stable step ids.
    - Forbidden combinations (e.g. `invoked_ok` + `task_tool_invoked: false` on mandated helpers).
    - Allowed `skipped` / `not_applicable` reason codes.
    - Run-Telemetry integration.

---

## Validator and profile contracts

- **Pipeline Validator Profiles**  
  - Path in vault: `3-Resources/Second-Brain/Docs/Pipeline-Validator-Profiles.md`  
  - Export/Git path: `Docs/Pipeline-Validator-Profiles.md`  
  - Purpose: Defines:
    - Validator behavior per pipeline mode/profile.
    - Tiered blocks (`log_only` / `needs_work` / `block_destructive`).
    - When post–little-val validator is mandatory at Layer 1.

- **Validator Tiered Blocks Spec**  
  - Path in vault: `3-Resources/Second-Brain/Docs/Validator-Tiered-Blocks-Spec.md`  
  - Export/Git path: `Docs/Validator-Tiered-Blocks-Spec.md`  
  - Purpose: Explains how severity + `recommended_action` map to:
    - Hard blocks vs advisory results.
    - Incoherence handling and retry budgets.

---

## Roadmap-specific contracts

- **Roadmapping System Overview**  
  - Path in vault: `3-Resources/Second-Brain/Docs/Roadmapping-System.md`  
  - Export/Git path: `Docs/Roadmapping-System.md`  
  - Purpose: High-level roadmap behavior (setup, resume, state authority, dual-track).

- **Roadmap Agent (Layer 2)**  
  - Path in vault: `.cursor/agents/roadmap.md`  
  - Export/Git path: `.cursor/agents/roadmap.md`  
  - Purpose: Operational contract for RESUME/ROADMAP:
    - MCP vs inline-edit fallback and `run_mode` classification.
    - Required nested helpers and honesty checklist.
    - Control-plane v2 observability and queue continuation rules.

- **Roadmap Gate Catalog by Track**  
  - Path in vault: `3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-By-Track.md`  
  - Export/Git path: `Docs/Roadmap-Gate-Catalog-By-Track.md`  
  - Purpose: Catalog of conceptual vs execution gates and their semantics.

---

## Queue, continuation, and task comms

- **Queue Sources**  
  - Path in vault: `3-Resources/Second-Brain/Queue-Sources.md`  
  - Export/Git path: `Docs/Queue-Sources.md`  
  - Purpose: Mode → file routing, RESUME_ROADMAP params, followup rules.

- **Queue Continuation Spec**  
  - Path in vault: `3-Resources/Second-Brain/Docs/Queue-Continuation-Spec.md`  
  - Export/Git path: `Docs/Queue-Continuation-Spec.md`  
  - Purpose: Schema for `queue_continuation` blocks and continuation logs.

- **Task Handoff Comms Spec**  
  - Path in vault: `3-Resources/Second-Brain/Docs/Task-Handoff-Comms-Spec.md`  
  - Export/Git path: `Docs/Task-Handoff-Comms-Spec.md`  
  - Purpose: JSONL shape for Task handoff logging (`handoff_out` / `return_in`).

---

## Where to start for audits/tools

If you are a secondary agent (Grok, validator, or tooling) trying to locate the contracts:

- Start here: `Docs/Contract-Index.md` (this file).
- Then follow:
  - `Docs/Safety-Invariants.md`
  - `Docs/Core/Subagent-Safety-Contract.md`
  - `Docs/Nested-Subagent-Ledger-Spec.md`
  - `Docs/Pipeline-Validator-Profiles.md`
  - `.cursor/agents/roadmap.md`

All of these paths exist on the `iteration-2-roadmap-rules` branch in the export repo.
