---
name: rule-funnel-doc-cleaning-v2
overview: Upgrade Cursor rule funnels, docs, and safety shielding so that prompt-crafter is the primary entry door, manual mode triggers are explicitly advanced/manual, and all pipelines are protected by global guardrails and clear documentation.
todos:
  - id: inventory-rules-and-docs-v2
    content: Inventory all rules (always/context and Starter-Kit) and key docs, and classify them by layer (core guardrail, funnel, pipeline, helper, template).
    status: completed
  - id: design-core-guardrails-funnel
    content: Design the exact structure and content of always/core-guardrails.mdc as the single safety contract, based on existing always rules.
    status: completed
  - id: design-system-funnels-funnel
    content: Design the exact structure and content of always/system-funnels.mdc, clearly distinguishing Prompt-Crafter entry vs manual/advanced mode triggers and mapping them to context rules.
    status: completed
  - id: canonicalize-and-archive-rules
    content: Select canonical rule implementations and plan the archival/renaming of Starter-Kit rule files into a non-active templates/legacy location.
    status: completed
  - id: prompt-crafter-primary-door-docs
    content: Update prompt-crafter and queue docs conceptually so Prompt-Crafter is clearly the primary entry door and manual modes are marked as advanced, with their behavior documented.
    status: completed
  - id: backbone-readme-funnel-docs
    content: Plan specific README and Backbone edits so they explain the funnel layers (core-guardrails, system-funnels, pipelines) and how Prompt-Crafter and manual triggers flow through them.
    status: completed
  - id: queue-docs-dedup-v2
    content: Refine Queue-Sources and Queue-Alias-Table roles, adding origin (Prompt-Crafter vs manual) and updating other docs to point to these instead of re-describing modes.
    status: completed
  - id: link-path-cleanup-v2
    content: Identify and plan corrections for outdated or ambiguous links/paths (especially Second-Brain-Config and archived notes) across backbone docs.
    status: completed
  - id: hub-context-integration-v2
    content: Plan hub sections and context headers so key specs (prompt-crafter, queues, funnels, ingest/mobile, PARA) are reachable and labeled from README and Backbone.
    status: completed
  - id: level-naming-consistency-v2
    content: Define and apply consistent High/Mid/Detailed semantics and H1 naming for backbone and user-flow docs so invariants live in Detailed only.
    status: completed
  - id: safety-integration-docs-v2
    content: Plan a concise safety overview that references always/core-guardrails and a Watcher/Commander narrative that references Queue-Sources and pipeline docs.
    status: completed
  - id: hardening-search-pass
    content: Specify and later run a read-only search over rules/skills for triggers, thresholds, destructive MCP calls, and queue/watcher writes to ensure they align with core-guardrails and system-funnels.
    status: completed
  - id: post-refactor-validation
    content: Define and use a validation checklist (per-trigger flows, queue behavior, doc navigation, link sanity) after implementing rule funnels and doc changes.
    status: completed
isProject: false
---

# Rule Funnel, Prompt-Crafter, and Doc Cleaning v2

## Goals

- **Funnel & shielding**: Introduce two minimal always-on rule funnels (`core-guardrails` and `system-funnels`) that define global safety and routing, explicitly distinguishing **prompt-crafter entry** from **manual/advanced mode triggers**.
- **Prompt-crafter as primary door**: Make the question-led Prompt-Crafter the canonical way to generate queue entries and pipeline runs; treat direct mode phrases (INGEST MODE, DISTILL MODE, etc.) as **manual/advanced** operations with clarified behavior.
- **Docs alignment**: De-duplicate and harden backbone, prompt-crafter, and queue documentation so they reflect the new funnels, shielding, and manual-mode semantics.
- **Safety**: Ensure that any changes to rules/pipelines are compensated by doc updates and validated with targeted searches (triggers, thresholds, destructive ops, queues, watcher).

---

## 1. Inventory & classification (rules + docs)

1. **Rules inventory** (read-only):
  - Enumerate all rules under `.cursor/rules/always/` and `.cursor/rules/context/`, plus `Second-Brain-Starter-Kit/.cursor/rules/`**.
  - For each rule, record: filename, location, and role:
    - `global-guardrail` (core invariants),
    - `routing/funnel` (triggers → pipelines),
    - `pipeline-specific` (ingest, organize, distill, express, archive, roadmap, queue, restore, garden/cluster),
    - `helper` (e.g. highlight-perspective, distill-lens),
    - `legacy/template` (Starter-Kit copies, older contracts).
2. **Docs inventory** (read-only):
  - Backbone hub docs: `README.md`, `Backbone.md`, `Pipelines.md`, `Parameters.md`, `Queue-Sources.md`, `Queue-Alias-Table.md`, `Logs.md`, `MCP-Tools.md`, `Skills.md`, `Vault-Layout.md`, `Responsibilities-Breakdown.md`, `Second-Brain-Config.md`.
  - Prompt-crafter docs: `Second-Brain-User-Flows/Prompt-Crafter-Structure-Detailed.md`, `Prompt-Crafter-Param-Table.md`, `Prompt-Crafter-Examples.md`, user-flow prompt-crafter variants, `Chat-Prompts.md`.
  - Queue docs: `Queue-Sources.md`, `Queue-Alias-Table.md`, Mode-Success-Contracts.md, queue sections in `Backbone.md`, `Pipelines.md`, `Chat-Prompts.md`.
3. **Record mapping** in `3-Resources/Second-Brain/Rules.md` or a small internal index: rule/doc → type → layer (core, funnel, pipeline, helper, template).

---

## 2. Design v2 always-on structure (funnels + shielding)

### 2.1 `always/core-guardrails.mdc` (global safety contract)

Design a new always rule that is **behaviorally equivalent** to the current combination of `00-always-core`, `second-brain-standards`, `mcp-obsidian-integration` (generic parts), and `confidence-loops`, but with a clearer API:

- **Persona & PARA**:
  - Thoth-AI persona and Markdown/Obsidian conventions.
  - PARA-only folders and naming standards (no `00 Inbox`, `10 Zettelkasten`, etc.).
- **Confidence bands & loops** (canonical):
  - Define high/mid/low bands once, including:
    - Exact thresholds.
    - One non-destructive loop per note per pipeline run.
    - Requirements for moving from mid-band to executing destructive actions.
  - Forbid destructive actions in mid/low bands.
- **MCP & filesystem safety** (vault-agnostic):
  - Backups must exist (`obsidian_create_backup`/`obsidian_ensure_backup`) before any destructive change.
  - Per-change snapshots (`obsidian-snapshot`) required before move/rename/delete/large rewrite.
  - Never use shell `cp/mv/rm` for the vault (only allowed in specific, user-invoked skills).
  - Backups and snapshots in `Backups/` + `BACKUP_DIR` are append-only and never edited.
  - Respect `watcher-protected: true` and other exclusions (Ingest/watched-file.md, Watcher-Signal/Result, Backups/).
- **Cross-pipeline invariants**:
  - "No destructive action unless (1) high band, (2) snapshot success".
  - Error Handling Protocol reference (Errors.md + pipeline logs) without re-implementing pipeline-specific steps.
  - Multi-run/roadmap state invariants are referenced, but details live in roadmap docs and `auto-roadmap`.

### 2.2 `always/system-funnels.mdc` (routing + entry semantics)

Design a second always rule that defines **how instructions and prompts enter the system**, distinguishing:

- **Primary entry: Prompt-Crafter**
  - Clearly state: the **question-led Prompt-Crafter** (triggered by "We are making a prompt" / code/roadmap prompt-crafter flows) is the **preferred and safest entry door** for creating queue entries and automation runs.
  - Pipelines triggered via Prompt-Crafter:
    - Always run with fully-specified, validated `mode` + `params` objects that obey Prompt-Crafter-Structure.
    - Are considered **standard/normal** operation.
- **Secondary entry: Manual/advanced mode triggers**
  - Explicitly mark raw mode phrases such as:
    - `INGEST MODE – safe batch autopilot` / `INGEST MODE`.
    - `DISTILL MODE – safe batch autopilot`.
    - `EXPRESS MODE – safe batch autopilot`.
    - `ARCHIVE MODE – safe batch autopilot`.
    - `EAT-QUEUE` / `EAT-CACHE`.
    - `PROCESS TASK QUEUE`.
    - `ROADMAP MODE`, `RESUME-ROADMAP`, `RECAL-ROAD`, `REVERT-PHASE`, `SYNC-PHASE-OUTPUTS`, `HANDOFF-AUDIT`, `EXPAND-ROAD`, `RESUME-FROM-LAST-SAFE`.
  - Declare these as **manual/advanced operations**:
    - Intended for laptop use with higher trust.
    - Behave differently from Prompt-Crafter flows (e.g. may assume more context, may not collect certain parameters via Q&A).
    - Must still obey `core-guardrails` (backups, snapshots, confidence bands) and queue/roadmap invariants.
- **Routing table** (declarative, no steps):
  - For each manual mode phrase, define:
    - Which **context rule** handles it,
    - Whether it is **standard/prompt-crafter-driven** or **manual/advanced**.
    Examples (document-only):
  - `INGEST MODE` (manual/advanced trigger)
    - → `context/ingest-processing.mdc` + `context/para-zettel-autopilot.mdc`.
  - `DISTILL MODE` (manual/advanced trigger)
    - → `context/auto-distill.mdc`.
  - `EXPRESS MODE` (manual/advanced trigger)
    - → `context/auto-express.mdc`.
  - `ARCHIVE MODE` (manual/advanced trigger)
    - → `context/auto-archive.mdc`.
  - `EAT-QUEUE`/`EAT-CACHE` (manual/advanced trigger)
    - → `context/auto-eat-queue.mdc` (prompt queue).
  - `PROCESS TASK QUEUE` (manual/advanced trigger)
    - → `context/auto-queue-processor.mdc` (task/roadmap queue).
  - `ROADMAP MODE` / `RESUME-ROADMAP` / `RECAL-ROAD` / etc. (queue-driven or manual)
    - → `context/auto-roadmap.mdc` after mode normalization (e.g. mapping RECAL-ROAD → RESUME-ROADMAP with params.action = recal).
- **Guidance-aware and Watcher contracts**:
  - Describe when a run is **guidance-aware** (pointer to `guidance-aware.mdc`), but keep details in that rule.
  - Describe when and how to append to `Watcher-Result.md` (pointer to watcher bridge rule), not re-defining the format.

---

## 3. Canonicalization and archival of rules

1. **Choose canonical rule implementations**:
  - As in v1: root `confidence-loops.mdc`, root `mcp-obsidian-integration.mdc`, root ingest/auto-* rules, root non-MD handling and ingest-processing.
2. **Archive Starter-Kit rules**:
  - Classify all `Second-Brain-Starter-Kit/.cursor/rules/`** rules as legacy/templates.
  - Plan to move them under a non-active path (e.g. `Second-Brain-Starter-Kit/rules-archive/`) or rename to `*-template.mdc`.
  - Update `Rules.md` to state that only root `.cursor/rules/`** are authoritative for this vault.
3. **Rule responsibility map**:
  - Extend `Rules.md` with a table mapping each rule to:
    - Layer (core, funnel, pipeline, helper, template),
    - Responsibilities,
    - "Not responsible for" notes (e.g. `auto-distill` does not decide when to run; system-funnels and prompt-crafter do).

---

## 4. Prompt-Crafter as primary entry door

1. **Clarify in `system-funnels` and docs**:
  - For regular users and “normal” automation, **Prompt-Crafter is the preferred door**:
    - It collects mode, params, and payload via strict Q&A.
    - It ensures queue payloads obey the v2 contract (mode + params + optional param_meta overlay).
  - Manual mode phrases are explicitly documented as **advanced entry points**:
    - They may be used by power users or by Commander flows.
    - They bypass some of the guardrails in Q&A (but never bypass `core-guardrails`).
2. **Doc alignment**:
  - In `Prompt-Crafter-Structure-Detailed.md`:
    - Add a short section explaining how crafted payloads map into modes handled by `auto-eat-queue` and `system-funnels`.
  - In `Queue-Sources.md`:
    - Distinguish between **Prompt-Crafter-sourced entries** and **manual entries** per mode.
  - In `Chat-Prompts.md` and user-flow docs:
    - Emphasize “We are making a prompt” as the supported way to spin up multi-step, high-safety runs.

---

## 5. Backbone & README separation (docs)

Same as v1, but explicitly referencing the new funnels and Prompt-Crafter role:

1. **README.md**:
  - Overview of the system, including:
    - Prompt-Crafter as primary door.
    - Manual mode phrases as advanced entry points.
    - Pointers to `core-guardrails`, `system-funnels`, and key pipeline docs.
2. **Backbone.md**:
  - Detailed architecture, including:
    - Description of the three main layers: core-guardrails, system-funnels, context rules & skills.
    - Clear explanation of safety flow: Prompt-Crafter → queue → auto-eat-queue/auto-roadmap → pipelines.
3. **Relationship notes** at the top of both files.

---

## 6. Prompt-Crafter documentation consolidation

Keep v1 actions, but add explicit ties into funnels & manual modes:

1. **Canonical invariants** remain in `Prompt-Crafter-Structure-Detailed.md`.
2. **Parameter tables** stay in `Prompt-Crafter-Param-Table.md`.
3. **Examples** stay in `Prompt-Crafter-Examples.md`.
4. **Links to funnels and queue docs**:
  - Add a small “Where does this go?” section explaining:
    - How crafted payloads become `prompt-queue.jsonl` entries.
    - How `auto-eat-queue` and `system-funnels` then dispatch them.
5. **User-flow split (High/Mid/Detailed)** as in v1, ensuring invariants are only in Detailed.

---

## 7. Queue & alias documentation de-duplication

Same as v1, but with explicit manual vs prompt-crafter separation:

1. **Queue-Sources.md**:
  - For each mode, indicate:
    - Whether it is **typically created by Prompt-Crafter**, **manual/advanced**, or both.
    - Any differences in behavior depending on origin (e.g. Prompt-Crafter entries have full params; manual may rely more on defaults).
2. **Queue-Alias-Table.md**:
  - Alias → canonical mode, plus a column “Origin” (Prompt-Crafter / Manual / Either).
  - Link each alias to the appropriate section in `Queue-Sources.md`.
3. **Pipelines, Mode-Success-Contracts, Backbone, Parameters**:
  - Shorter mode sections that point to `Queue-Sources.md`.

---

## 8. Link & path corrections

Same as v1, including:

- Fix `Second-Brain-Config` references.
- Sanity-check high-traffic links (README, Backbone, Pipelines, Queue-Sources, Logs, MCP-Tools).

---

## 9. Hub & context integration

Same as v1, but explicitly highlighting:

- Prompt-Crafter hub location.
- Queue hub (Queue-Sources + Queue-Alias).
- Rule funnel overview (core-guardrails + system-funnels) in README and Backbone.

---

## 10. Level & naming consistency

Same as v1: High/Mid/Detailed semantics, H1 normalization, and explicit "— Detailed" suffix for deep specs.

---

## 11. Safety & integration coverage (docs-only)

Same as v1, but now referencing:

- `always/core-guardrails.mdc` as the **single** canonical spec for safety invariants.
- `always/system-funnels.mdc` as the **single** canonical spec for entry routing and manual vs Prompt-Crafter semantics.

---

## 12. Hardening & shielding search pass (no edits; analysis only)

Define a read-only analysis pass over the codebase to identify places that must respect the new funnels/guardrails and manual/Prompt-Crafter distinction:

1. **Trigger phrase search**:
  - `INGEST MODE`, `DISTILL MODE`, `EXPRESS MODE`, `ARCHIVE MODE`, `EAT-QUEUE`, `EAT-CACHE`, `PROCESS TASK QUEUE`, `GARDEN REVIEW`, `CURATE CLUSTER`, `ROADMAP MODE`, `RESUME-ROADMAP`, `RECAL-ROAD`, `REVERT-PHASE`, `SYNC-PHASE-OUTPUTS`, `HANDOFF-AUDIT`, `EXPAND-ROAD`, `RESUME-FROM-LAST-SAFE`, etc.
  - Classify each hit: is it in `system-funnels`/queue rules (good) vs arbitrary rules/skills (needs refactor to route via funnels)?
2. **Confidence thresholds search**:
  - Look for patterns like `>= 85`, `>=85%`, band names, and references to mid/high/low.
  - Ensure each is:
    - Consistent with `core-guardrails` thresholds.
    - Documented as “per core-guardrails” rather than arbitrary.
3. **Destructive MCP calls search**:
  - `obsidian_move_note`, `obsidian_rename_note`, `obsidian_delete_note`, `obsidian_update_note` (overwrite), `obsidian_append_to_hub`, etc.
  - Check that each call:
    - Is gated by backup + snapshot.
    - Lives in pipeline/context rules and obeys `core-guardrails`.
4. **Queue and Watcher writes**:
  - Writes to `.technical/prompt-queue.jsonl`, `Task-Queue.md`, and `Watcher-Result.md`.
  - Ensure only queue processors and watcher bridge rules write to these, and formats match canonical contracts.
5. **Mobile vs laptop semantics**:
  - Search for references to `Mobile-Migration-Spec`, `approved: true` for wrappers, and mobile modes.
  - Ensure no code path allows mobile to bypass Prompt-Crafter or wrappers for destructive actions.

Produce a short checklist or internal note summarizing: places that are already aligned vs places that must be updated when implementing v2 funnels.

---

## 13. Validation checklist (post-refactor)

After implementing the new funnels, rule collapses, and doc edits, run this checklist:

1. **Per-trigger flow checks**:
  - For each manual mode phrase and for Prompt-Crafter flows, verify:
    - Which always rules are consulted (core-guardrails, system-funnels).
    - Which context rules run.
    - Where backups, snapshots, and confidence bands are enforced.
2. **Queue behavior**:
  - Test Prompt-Crafter → queue → auto-eat-queue path for a few representative modes (INGEST MODE, RESUME-ROADMAP, DISTILL MODE).
  - Test manual mode entry for the same modes and confirm they behave as documented (advanced, but still safe).
3. **Docs navigation**:
  - From README:
    - Prompt-Crafter → structure + param-table + examples.
    - Queues → Queue-Sources + Queue-Alias.
    - Ingest/Mobile → Cursor-Agent-Ingest-Workflow + Mobile-Migration-Spec.
  - From Backbone:
    - Funnels and guardrails → always rules.
4. **Link sanity**:
  - Spot-check for broken or obviously outdated links.
  - Confirm that each invariant (safety, prompt-crafter, queue modes, roadmap state) has exactly one primary home in docs.

---

## 14. Implementation phases (high-level)

Although actual edits are separate from this plan, the likely future implementation order is:

1. Create & populate `always/core-guardrails.mdc` and `always/system-funnels.mdc` (copying content from existing always rules, preserving behavior).
2. Update `Rules.md`, `Backbone.md`, and `README.md` to reflect the new layers and Prompt-Crafter/Manual distinction.
3. Archive/rename Starter-Kit rules and update docs to point to canonical root rules.
4. Apply prompt-crafter and queue doc consolidations.
5. Run the hardening search pass and adjust any remaining rules that bypass the funnels or misalign with `core-guardrails`.
6. Run the validation checklist.

