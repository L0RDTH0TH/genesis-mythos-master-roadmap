---
name: roadmap-mcp-fallback-refactor
overview: Design changes to roadmap-related skills and contracts so that roadmap-deepen and helpers can gracefully fall back to inline file edits when Obsidian MCP is unavailable, while keeping safety guarantees intact.
todos:
  - id: analyze-contracts
    content: Re-read Subagent-Safety-Contract, roadmap agent, and core guardrails to restate current guarantees around MCP vs inline edits for roadmap.
    status: completed
  - id: design-fallback-semantics
    content: Define capability detection and two-path behavior (MCP vs inline) for roadmap-deepen, little-val, and validator helpers, including reporting flags.
    status: completed
  - id: spec-io-abstraction
    content: Specify a minimal I/O abstraction pattern that splits roadmap skill logic from the underlying MCP or inline-edit implementation.
    status: completed
  - id: document-contract-updates
    content: Update conceptual documentation (Subagent-Safety-Contract and core guardrails) to describe the new fallback semantics and result modes.
    status: completed
  - id: define-test-scenarios
    content: List concrete test scenarios and acceptance criteria to verify correct behavior for both MCP-available and MCP-unavailable Task environments.
    status: completed
isProject: false
---

## Roadmap MCP Fallback Refactor Plan

### 1. Clarify current behavior and contracts

- **Review Subagent contract**: Re-read `[3-Resources/Second-Brain/Subagent-Safety-Contract.md](3-Resources/Second-Brain/Subagent-Safety-Contract.md)` for the current guarantees around MCP vs inline edits, especially the section describing Task subagents, fallback modes, and the roadmap helper graph.
- **Inspect roadmap agent behavior**: Re-read `[.cursor/agents/roadmap.md](.cursor/agents/roadmap.md)` to understand how it currently calls `roadmap-deepen`, little-val, and Validator/IRA, and what it assumes about MCP availability.
- **Confirm global safety expectations**: Revisit `[.cursor/rules/always/core-guardrails.mdc](.cursor/rules/always/core-guardrails.mdc)` to ensure any fallback still respects backups/snapshots intent and confidence bands, even when implemented via inline edits.

### 2. Define capability-detection and fallback semantics

- **Capability probing model**: Specify a simple, reusable way for skills to detect whether Obsidian MCP tools are available/healthy vs absent/broken in the current environment (e.g. via a lightweight health flag or a dedicated probe step at the start of the agent/skill).
- **Two-path contract**: Write down a clear contract for skills:
  - MCP path: preferred, uses `obsidian_`* calls, snapshots, and backups exactly as today.
  - Inline-edit path: allowed when MCP is unavailable; uses Cursor file tools to read/write markdown while treating snapshot/backup as best-effort intent, not MCP calls.
- **Result reporting**: Decide how subagents should report which path was taken (e.g. explicit flags like `used_mcp: true/false`, `fallback_inline_edits: true/false`, and when they must mark `#review-needed`).

### 3. Target the roadmap skill stack for fallback

- **Map the dependency chain**: Identify exactly which skills in the roadmap pipeline must be made MCP-optional:
  - `roadmap-deepen` core logic and its file-touching pieces.
  - `little-val-structural` and any structural checks that currently assume MCP.
  - Any roadmap-related validator glue used from the roadmap subagent.
- **Separate pure logic from I/O**: For each of these skills, conceptually separate the reasoning/planning pieces (what to create/update) from the I/O layer (how to read/write notes), so the same logic can run on both MCP and inline-edit backends.
- **Design an I/O abstraction**: Define a minimal interface or pattern (even if only by convention) that encapsulates “read note”, “write note”, and “snapshot/backup intent”, so the skill can plug either the MCP or inline-edit implementation under it.

### 4. Specify MCP-path behavior (keep existing safety)

- **Preserve current safeguards**: Ensure the MCP implementation of the I/O abstraction still:
  - Calls `obsidian_ensure_backup` / `obsidian_create_backup` before destructive changes.
  - Uses `obsidian-snapshot` per-change snapshots around roadmap state and phase-note mutations.
  - Obeys confidence bands and dual-roadmap-track rules for conceptual vs execution tracks.
- **No behavioral regressions**: Enumerate key behaviors that must not change on MCP-capable runs (e.g. where roadmap notes are written, how `roadmap-state.md` is updated, how Decision Records are created).

### 5. Specify inline-edit fallback behavior

- **Read/write semantics**: Define how inline edits will read and write:
  - Use Cursor `Read`-equivalent to load markdown files by path.
  - Use `ApplyPatch`-style diffing to apply minimal, atomic edits to `roadmap-state.md`, phase notes, and decision logs.
- **Safety approximations**: Describe how to approximate backups/snapshots without MCP:
  - Log snapshot intent and optionally create lightweight in-vault copies using standard file tools when reasonable.
  - Continue to enforce confidence bands conceptually (e.g. do not perform large structural rewrites when confidence is low; prefer `#review-needed` callouts).
- **Error handling**: Define how skills should behave when inline edits fail (e.g. file missing, patch conflict): abort the destructive step, surface a clear error in the roadmap subagent result, and avoid pretending deepen succeeded.

### 6. Update subagent result and status semantics

- **Result shape**: Update the conceptual schema for the roadmap subagent’s return payload so it can distinguish:
  - `mode: full_run_mcp` (MCP path, full deepen + validators).
  - `mode: full_run_inline` (inline edits path, full deepen semantics but without MCP).
  - `mode: analysis_only` (neither path completed; no mutations, #review-needed).
- **Little-val and validator flags**: Clarify the conditions under which `little_val_ok`, `validator_context`, and `queue_followups` can be set to non-omitted values in fallback mode versus when they must remain omitted.
- **Honest reporting**: Make explicit that the subagent must never claim a deepen/validation ran when it only performed analysis; instead it should set appropriate flags and messages so Layer 1 and humans can distinguish partial from full runs.

### 7. Thread fallback semantics into the safety contract docs

- **Subagent-Safety-Contract updates**: Amend `[3-Resources/Second-Brain/Subagent-Safety-Contract.md](3-Resources/Second-Brain/Subagent-Safety-Contract.md)` to:
  - Document the MCP vs inline-edit behavior for roadmap subagent and helpers.
  - Describe how the Task harden pass should interpret fallback modes (still valid, but lower observability).
- **Core guardrails note**: Add a short note to `[.cursor/rules/always/core-guardrails.mdc](.cursor/rules/always/core-guardrails.mdc)` clarifying that, in MCP-less Task environments, roadmap pipelines are expected to obey the same intent (backups, snapshots, confidence bands) using inline edits rather than shell operations.

### 8. Plan verification and test scenarios (conceptual)

- **Scenario matrix**: Define a small matrix of scenarios to test once implemented:
  - Task/roadmap in MCP-healthy environment → MCP path.
  - Task/roadmap in MCP-broken environment → inline-edit path, successful deepen.
  - Task/roadmap in MCP-broken environment with unexpected file errors → analysis-only with clear `#review-needed` status.
- **Acceptance criteria**: For each scenario, specify expected flags, status fields, and observable side effects in the vault (e.g. phase 5.1 note actually created/updated vs not touched).
- **Observability**: Decide how to log which path was used (MCP vs inline) so debugging future runs is straightforward.

