---
name: validator-enforcement-audit
overview: Audit and harden validator integration so every automation pipeline both performs a nested validator call and always triggers the queue-level validator pass on success.
todos:
  - id: audit-agents
    content: Audit and tighten validator wording/behavior in all pipeline agents (ingest, organize, archive, distill, express, roadmap, research).
    status: completed
  - id: update-safety-contract
    content: Strengthen Subagent-Safety-Contract and Queue-Sources to state hard invariants for nested and queue-level validator passes.
    status: completed
  - id: queue-rule-enforce
    content: Verify and, if needed, adjust queue.mdc so every successful pipeline run with little_val_ok true triggers a validator Task call using validator_context, without sampling or caps.
    status: completed
  - id: docs-sync-validator
    content: Update pipeline and validator documentation/diagrams to reflect mandatory two-layer validator integration and remove soft/ambiguous wording.
    status: completed
isProject: false
---

### Goals

- **Guarantee** that every pipeline run (ingest, organize, archive, distill, express, roadmap, research) both calls the Validator subagent once per run (nested) and is followed by a **mandatory** queue-level validator pass on Success.
- Remove or tighten any "soft" wording that could be interpreted as optional, and align all rules/docs with the hard invariants.

### 1. Map current validator touchpoints

- **Read** the following to confirm current contracts and where validator is mentioned:
  - `[.cursor/agents/ingest.md](.cursor/agents/ingest.md)`
  - `[.cursor/agents/organize.md](.cursor/agents/organize.md)`
  - `[.cursor/agents/archive.md](.cursor/agents/archive.md)`
  - `[.cursor/agents/distill.md](.cursor/agents/distill.md)`
  - `[.cursor/agents/express.md](.cursor/agents/express.md)`
  - `[.cursor/agents/roadmap.md](.cursor/agents/roadmap.md)`
  - `[.cursor/agents/research.md](.cursor/agents/research.md)`
  - `[.cursor/agents/queue.md](.cursor/agents/queue.md)`
  - `[.cursor/agents/validator.md](.cursor/agents/validator.md)`
  - `[3-Resources/Second-Brain/Subagent-Safety-Contract.md](3-Resources/Second-Brain/Subagent-Safety-Contract.md)`
  - `[3-Resources/Second-Brain/Queue-Sources.md](3-Resources/Second-Brain/Queue-Sources.md)`
- **Extract** for each pipeline:
  - Where the **nested** validator call is described and what conditions/gating language it uses.
  - What `validator_context` the pipeline promises to return on Success.
  - How the queue rule currently performs the **post-pipeline** validator pass using `validator_context`.
- **List gaps/softness**: any "may" / "when enabled" / sampling-condition text that could cause a pipeline run to skip validator entirely.

### 2. Harden the global validator contract

- In `Subagent-Safety-Contract.md`:
  - **Clarify invariants**:
    - Every pipeline subagent that returns **Success** and mutates notes/state **MUST** have either:
      - Run its **nested** ValidatorSubagent once and honored its verdict, and
      - Returned `little_val_ok: true` **and** a non-empty `validator_context` matching the validation type.
    - The queue **MUST** run ValidatorSubagent once per such Success, with **no sampling and no config gate**, before adding the entry id to `processed_success_ids`.
  - Replace any remaining "may call validator" phrasing for pipelines with "**MUST call**" and "**MUST NOT claim Success when validator recommends block_destructive/high severity**".
- In `Queue-Sources.md` under **Post-pipeline validator**:
  - Ensure wording is strictly mandatory ("queue MUST run ValidatorSubagent"; "pipelines MUST supply validator_context").
  - Confirm the `Mode → validation_type` mapping covers all target pipelines and update if any are missing.

### 3. Tighten each pipeline subagent spec

For each of `ingest`, `organize`, `archive`, `distill`, `express`, `roadmap`, and `research` agents:

- **Nested call requirement**:
  - Change the nested validator section to say the subagent **MUST call** `ValidatorSubagent` exactly once per run **after** little val reaches `ok: true` (or, for research, whenever synthesized notes exist).
  - Remove or narrow any config/sampling gates that would skip validator entirely; allow thresholds only for type-specific conditions (e.g. distill word-count) but not for the presence of the validator call itself.
- **Success gating**:
  - Make explicit that the subagent **MUST NOT return Success** when validator reports `severity: high` or `recommended_action: "block_destructive"`; only `#review-needed` or `failure` are allowed in that case.
  - Confirm each spec states that Success is allowed only when final little val verdict is `ok: true` **and** nested validator did not block.
- **validator_context shape**:
  - Verify each agent’s **Return** section includes a precise `validator_context` object when `little_val_ok` is true, with keys matching the `Mode → validation_type` mapping in `Queue-Sources.md`.
  - Adjust any mismatched keys or missing fields so that queue can always construct a valid validator hand-off without guessing.

### 4. Enforce queue-level validator call in the queue rule

- In `[.cursor/rules/agents/queue.mdc](.cursor/rules/agents/queue.mdc)` A.5/A.6:
  - Confirm the logic that, on pipeline Success with `little_val_ok: true` and a `validator_context`, **always**:
    - Builds a validator hand-off from `validator_context` and telemetry.
    - Looks up the correct model from `Second-Brain-Config` for that `validation_type`.
    - Calls the Task tool with `subagent_type: validator` (this call **must not** be skipped by sampling or caps).
  - Ensure validator-global caps (`validator.global_max_per_run`) apply only to explicit `VALIDATE` / `ROADMAP_HANDOFF_VALIDATE` queue modes, **not** to these post-pipeline validator passes.
  - Strengthen any soft wording to say that if `validator_context` is missing for a pipeline that should have one, this is a **contract violation** to be logged in `Errors.md`, and the entry should **not** be silently treated as fully validated.

### 5. Align legacy/auxiliary paths and docs

- **Legacy agents** under `.cursor/rules/legacy-agents/*.mdc`:
  - Either update their descriptions to clearly mark them as deprecated and not used by the queue/dispatcher, or bring their text in line with the new hard validator invariants if they can still be run directly.
- **Validator subagent spec** (`.cursor/agents/validator.md` and `.cursor/rules/agents/validator.mdc`):
  - Document that it may be invoked in three ways:
    - Explicit queue modes (`VALIDATE`, `ROADMAP_HANDOFF_VALIDATE`).
    - Nested calls from pipelines.
    - Queue-level post-pipeline validator invocations.
  - Clarify that all are read-only on inputs except the report path and share the same verdict semantics.
- Update any high-level docs that describe pipeline behavior:
  - `3-Resources/Second-Brain/Cursor-Skill-Pipelines-Reference.md`.
  - Any dedicated `Validator-Reference` or validator section if present.

### 6. Sanity-check and examples

- Add **one short example** per pipeline in the relevant docs (or a central validator reference) showing:
  - A successful run (little val ok + nested validator ok + queue-level validator ok).
  - A blocked run (validator high severity / block_destructive) and how it appears in status, logs, and Watcher-Result.
- Verify the examples make it clear that **there is no path** where a pipeline mutates notes/state and returns Success without having passed through both validator layers.

### 7. Optional: configuration review

- Inspect `3-Resources/Second-Brain/Second-Brain-Config.md` for the `validator` block:
  - Ensure every `validation_type` in use has a configured `model`.
  - Remove or narrow any global sampling or enable/disable flags that could contradict the "always validate on Success" invariant for pipeline runs.

### Todos

- **audit-agents**: Systematically review and tighten validator language and return contracts in all pipeline agents (ingest/organize/archive/distill/express/roadmap/research).
- **update-safety-contract**: Harden `Subagent-Safety-Contract.md` and `Queue-Sources.md` around nested + post-pipeline validator invariants.
- **queue-rule-enforce**: Ensure `queue.mdc` always performs post-pipeline validator calls and treats missing `validator_context` as a contract error, not a soft skip.
- **docs-sync-validator**: Update high-level docs (Pipelines reference, Validator reference, any diagrams) to reflect the enforced two-layer validator model and de-emphasize any older soft language.

