---
name: researcher-layer-migration
overview: Allow the Research subagent to be a sanctioned nested helper alongside IRA and Validator, while preserving the subagent layering and safety contracts.
todos:
  - id: add-research-nested-exception
    content: Add a Research nested-call exception to Subagent-Safety-Contract alongside IRA and Validator.
    status: completed
  - id: align-research-subagent-rule
    content: Tighten .cursor/agents/research.md to match the new nested exception (who may call it, what it may write, and how it returns research_consumables).
    status: completed
  - id: wire-roadmap-express-usage
    content: Document how roadmap (and express, if applicable) use nested Research and must consume injection_block_markdown correctly.
    status: completed
  - id: refresh-dispatcher-queue-docs
    content: Update dispatcher and queue rules (and sync copies) to note the three sanctioned nested helpers without changing core layering.
    status: completed
  - id: update-backbone-overview
    content: Update high-level backbone docs to list IRA, Validator, and Research as the three helper exceptions.
    status: completed
isProject: false
---

### Goal

Add the Research subagent as a **third, explicitly whitelisted nested helper** (like IRA and Validator) so pipelines can call it from within a run, without breaking the existing layering, safety, and queue-orchestration contracts.

### 1. Update Subagent-Safety-Contract to include Research as a nested exception

- **File**: `[3-Resources/Second-Brain/Subagent-Safety-Contract.md](3-Resources/Second-Brain/Subagent-Safety-Contract.md)`
- **Changes**:
  - In the section that currently defines the **Internal Repair Agent exception** and **Validator nested-call exception**, introduce a **new subsection** (e.g. "Research nested-call exception").
  - Specify that **allowed callers** are the relevant pipeline subagents (at minimum `roadmap`, and optionally `ingest`, `express`, maybe `distill`) and that **forbidden callers** remain Queue/Dispatcher and Validator (to avoid meta‑nesting).
  - Define **per-run limits** for research nested calls (e.g. at most 1–2 research calls per pipeline run) to keep stacks shallow:
    - Shape: `main → queue → pipeline → research` only; research itself must not call any other subagent.
  - Clarify **permissions**: Research is allowed to write only to `Ingest/Agent-Research/`** and `.technical/Run-Telemetry/` (plus any explicit research logs), and is **read-only** on roadmap-state, PMG, phase notes, etc., mirroring the read-only constraints you already have for Validator and IRA.
  - Add a short note about **chain vs nested**: when Research is used as a nested helper, it must not enqueue further pipelines directly; cross-pipeline orchestration still happens through the queue via `chain_request` when needed.

### 2. Align the Research subagent rule with the new nesting semantics

- **File**: `[.cursor/agents/research.md](.cursor/agents/research.md)`
- **Changes**:
  - Update the intro lines that currently say *"You are callable by any subagent (Queue or any pipeline)."* to align with the new layering:
    - Emphasize that **Queue** calls Research when mode is `RESEARCH_AGENT` / `RESEARCH_GAPS` (top‑level pipeline), while **pipeline subagents** may call Research only under the new "Research nested-call exception" conditions.
  - Add a small **"Subagent nesting"** subsection referencing the Subagent-Safety-Contract section, explicitly stating:
    - Research must not call other subagents.
    - Research must not read/write queue files or Watcher-Result.
    - When called as a nested helper, it returns structured `research_consumables` only; the caller is responsible for any queue entries or roadmap/state changes.
  - Ensure the nested **ValidatorSubagent** call for `research_synthesis` (already described in this file) is explicitly framed as a **per-run nested validator** that doesn’t violate the new caps (i.e. still only one validator layer under research, no further subagents beneath it).

### 3. Document how roadmap/express use nested Research

- **Files** (depending on where usage is defined):
  - Roadmap: `[.cursor/rules/agents/roadmap.mdc](.cursor/rules/agents/roadmap.mdc)`
  - Express / PMG scoping, if they call research directly: `[.cursor/rules/agents/express.mdc](.cursor/rules/agents/express.mdc)` and/or `[.cursor/skills/research-scope/SKILL.md](.cursor/skills/research-scope/SKILL.md)`
- **Changes**:
  - In each pipeline that will use nested research (starting with Roadmap pre‑deepen):
    - Add a short **"Subagent nesting"** bullet noting that the pipeline **may call ResearchSubagent as a nested helper** for pre‑deepen or scoped research, under the new contract.
    - Describe at a high level when it’s allowed (e.g. `params.enable_research === true` or phase marked as research-heavy) and confirm that the pipeline:
      - Integrates the returned `injection_block_markdown` into its artifacts or stores it as a pending injection per the research skill’s consumption contract.
      - Still runs little‑val (and then Validator, if applicable) on the final artifact before claiming Success.
  - Make clear that **queue-based RESEARCH-AGENT** remains the canonical long‑horizon path for heavy research (no change to existing queue modes), while nested research is a **lightweight, bounded helper** inside a single pipeline run.

### 4. Keep dispatcher/queue layering docs consistent

- **Files**:
  - `[.cursor/rules/always/dispatcher.mdc](.cursor/rules/always/dispatcher.mdc)`
  - `[.cursor/rules/agents/queue.mdc](.cursor/rules/agents/queue.mdc)` and its sync copy `[.cursor/sync/rules/agents/queue.md](.cursor/sync/rules/agents/queue.md)`
- **Changes**:
  - Confirm that the existing description of layering (`main → queue → pipeline (ingest/roadmap/distill/express/archive/organize/research/validator)`) stays **unchanged** for queue dispatch.
  - Add a brief note in the "Subagent nesting" paragraphs that there are now **three sanctioned nested helpers pipelines may call**: IRA, Validator, and Research, all bounded by the Subagent-Safety-Contract.
  - Make sure these docs still say that **only the queue** launches pipeline subagents via `Task` and that **no subagent ever calls queue** (so the layering violation is limited to helper calls, not orchestration).

### 5. Update backbone docs / sync copies

- **Backbone docs**:
  - Update any high-level reference that lists nested subagent exceptions, such as:
    - `[3-Resources/Second-Brain/Docs/Subagents-Overview.md]` (or equivalent, if present)
    - `[3-Resources/Second-Brain/Queue-Sources.md](3-Resources/Second-Brain/Queue-Sources.md)` where RESEARCH-AGENT modes and validator contracts are described.
  - Explicitly document the new trio of nested helpers: **IRA**, **Validator**, **Research**.
- **Sync folder**:
  - For any changed rule under `.cursor/rules/`**, update the corresponding copy under `.cursor/sync/rules/`** to keep the backbone docs synchronized, per `backbone-docs-sync.mdc`.

### 6. Sanity-check against safety invariants (no code changes yet)

- Walk through a couple of scenarios on paper:
  - **Roadmap deepen with pre‑deepen research**:
    - Expected stack: `main → queue → roadmap → research → (validator under research)`. Verify that:
      - Only research writes Ingest/Agent-Research.
      - Roadmap owns integrating `injection_block_markdown` into phase notes or state.
      - Final Success is still gated by roadmap’s little‑val + validator.
  - **Queue RESEARCH-AGENT mode**:
    - Expected stack: `main → queue → research → validator`. Confirm that this still conforms to the contract and that nested usage does not change the existing mode semantics.
- Ensure no doc suggests that research can call IRA or other subagents (it must remain a leaf apart from its own validator call), and that there’s no path that would introduce an additional layer beyond the helpers already specified.

