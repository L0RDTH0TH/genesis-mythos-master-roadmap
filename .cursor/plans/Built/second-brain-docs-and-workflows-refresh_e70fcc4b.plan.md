---
name: second-brain-docs-and-workflows-refresh
overview: Refresh and extend the Second Brain backbone documentation and workflow/architecture descriptions so they exactly match current behavior, with no undocumented or stale features, focusing on rules, skills, and pipelines.
todos: []
isProject: false
---

## Goal

Bring the Second Brain backbone documentation (rules, skills, pipelines, ingest/express/distill/archive, roadmap) into exact alignment with the current implemented behavior, and surface any hidden or undocumented features. This includes checking for staleness, updating or adding docs, and validating that user workflows and architectures are fully covered end-to-end.

## High-level approach

- **Discover current backbone surface area**: Map all relevant rules, skills, and backbone docs to understand what "authoritative" documentation currently exists.
- **Detect stale or inconsistent docs**: For each backbone component, compare described behavior with actual implementation and log mismatches.
- **Update and extend documentation**: Revise existing docs to match real behavior and add missing sections for undocumented features or workflows.
- **Validate coverage of user workflows/architectures**: Ensure end-to-end flows (ingest → organize → distill/express → archive, plus roadmap flows) are fully documented with no gaps.

## Detailed steps

### 1. Inventory backbone artifacts

- **Rules & skills inventory**
  - Scan `.cursor/rules/always/` and `.cursor/rules/context/` to list all active rules.
  - Scan `.cursor/skills/` to list all skills that participate in ingest, organize, distill, express, archive, and roadmap pipelines.
  - Cross-check with `.cursor/sync/` to see which rules/skills already have synced reference copies.
- **Backbone docs inventory**
  - Read the main backbone docs under `3-Resources/Second-Brain/`, focusing on at least:
    - `Backbone.md`
    - `Vault-Layout.md`
    - `Pipelines.md`
    - `Rules.md`
    - `Skills.md`
    - `MCP-Tools.md`, `Configs.md`
    - `Parameters.md`
    - `Logs.md`
    - `Queue-Queues.md` or `Queue-Alias-Table.md` (already open)
  - Note which files appear to be intended as **sources of truth** vs. supporting notes.

### 2. Map rules/skills to docs and pipelines

- **Create a mapping between implementation and docs**
  - For each rule in `.cursor/rules/`**, identify:
    - Which pipeline(s) or workflows it affects (e.g. ingest, organize, archive, express, distill, roadmap, queue processing).
    - Where, if anywhere, it is referenced in the docs (`Rules.md`, `Pipelines.md`, etc.).
  - For each skill in `.cursor/skills/`**, identify:
    - Its purpose and parameters from `SKILL.md`.
    - The pipelines or queue modes that use it (leveraging `Cursor-Skill-Pipelines-Reference` if present).
  - Build a concise internal matrix (for us) of *rule/skill ↔ pipeline ↔ doc file* so we can spot un-documented or under-documented items.

### 3. Check for stale or inaccurate documentation

- **Compare docs vs implementation for each major area**
  - For ingest/organize/archive/express/distill pipelines:
    - Compare the described step order, safety gates (backups, snapshots, dry_run, confidence bands), and decision wrapper behavior in docs vs actual rules/skills (e.g. `confidence-loops`, `always-ingest-bootstrap`, `mcp-obsidian-integration`, pipeline-specific skills).
  - For roadmap system:
    - Compare `Roadmap Structure.md` and any roadmap docs under `3-Resources/Second-Brain/` with roadmap-related skills (`roadmap-`*, `hand-off-audit`, `research-agent-run`, etc.) and rules.
  - For MCP and Obsidian integration:
    - Compare `MCP-Tools.md`, `Configs.md`, and `mcp-obsidian-integration` with the actual MCP descriptors under `mcps/*`* (especially obsidian-related servers) and the always rules.
  - For queue and watcher integration:
    - Compare `Queue-Alias-Table.md`, any queue docs, and `watcher-result-append` rule with queue-processing rules (`auto-eat-queue`) and skills (`feedback-incorporate`, `queue-cleanup`, etc.).
- **Flag staleness and gaps**
  - Identify cases where docs:
    - Describe behavior that no longer exists in rules/skills.
    - Omit new safety steps (e.g. `obsidian-snapshot`, refined confidence loops, guidance-aware logic).
    - Lack coverage for new modes (e.g. NAME-REVIEW, ROADMAP, RESEARCH-AGENT, restore-queue) if present in rules/skills.
  - Maintain a simple checklist of mismatches with references to both implementation and doc locations.

### 4. Update documentation to match accurate behavior

- **Revise core backbone docs**
  - Update `Backbone.md` to give an accurate, high-level picture of the system:
    - PARA structure & constraints.
    - Ingest → organize → distill/express → archive lifecycle.
    - Roadmap system and multi-run behavior.
    - Safety invariants (backups, snapshots, confidence bands, decision wrappers).
  - Update `Vault-Layout.md` to match current folder rules (Ingest, Templates, 5-Attachments, PARA roots, Backups, etc.) and exclusions.
- **Align pipeline documentation**
  - Update `Pipelines.md` and `Cursor-Skill-Pipelines-Reference` (if present) so each pipeline:
    - Lists ordered steps (including which skills are used and in what mode).
    - Clearly documents confidence bands and refinement loops.
    - Describes how decision wrappers, Mobile-Pending-Actions, and async approvals are used.
- **Align rules/skills documentation**
  - Update `Rules.md` to reflect all active always/context rules, especially any recently-edited ones like `confidence-loops`, `guidance-aware`, `mcp-obsidian-integration`, `always-ingest-bootstrap`, `watcher-result-append`, `backbone-docs-sync`.
  - Update `Skills.md` to include concise entries for all skills that are user-relevant, summarizing:
    - What the skill does.
    - Which pipelines/modes call it.
    - Any important parameters or behaviors (e.g. read-only vs destructive, snapshot expectations).
- **Sync and align MCP / config docs**
  - Update `MCP-Tools.md` with any new tools or behavior for the Obsidian MCP server and others in `mcps/`**.
  - Refresh `Configs.md` to accurately describe relevant MCP/backup/snapshot config knobs from `~/.cursor/mcp.json` and any vault-local config notes.
- **Refresh parameters and logs docs**
  - Update `Parameters.md` to reflect current tunables (confidence bands, crafted_params_conf_boost, high_util_conf_boost, batch_size_for_snapshot, etc.).
  - Update `Logs.md` and any `*-Log.md` references to reflect current log formats (including loop_* fields, watcher result lines, error logging protocol).
- **Queue and watcher workflows**
  - Ensure `Queue-Alias-Table.md` and any queue docs match actual queue modes supported by rules/skills.
  - Document the full Watcher ↔ queue ↔ pipelines interaction so that user-facing flows are clear.

### 5. Document user workflows and architectures end-to-end

- **Ingest and organize workflows**
  - Write/update sections describing how a typical capture moves from `Ingest/` to its final PARA location, including:
    - Non-markdown handling and attachment moves.
    - Decision wrappers and low-confidence paths.
    - Async approval loop (Mobile-Pending-Actions) where relevant.
- **Distill and express workflows**
  - Clarify how distill runs (layers, highlight coloring, perspective gradients, readability flags) and express runs (related-content pull, express views, call-to-action, version snapshots) fit into a user’s daily flow.
- **Archive workflows**
  - Document archive decision logic (archive-check, summary-preserve, resurface-candidate-mark, organize/archive move, ghost folder cleanup).
- **Roadmap workflows**
  - Document roadmap creation, resume, deepen/advance/revert, audit, and handoff flows, using `genesis-mythos-master` as a concrete example where useful.
- **Architecture overviews (mermaid diagrams)**
  - Add or update a small set of mermaid diagrams in relevant docs to illustrate:
    - High-level system architecture (user ↔ Obsidian ↔ Cursor ↔ MCP server ↔ vault).
    - Main pipeline flows (ingest, distill, express, archive).
    - Roadmap multi-run state machine (simplified view of roadmap-state and workflow_state).

### 6. Surface hidden or undocumented features

- **Search for hidden features in code/rules/skills**
  - Use semantic search and grep across `.cursor/rules/`**, `.cursor/skills/`**, and `3-Resources/Second-Brain/**` to find:
    - Queue modes, pipeline names, or tags that aren’t yet documented.
    - Specialized safety or error-handling paths (e.g. restore-queue, error decision wrappers, MCP health checks).
    - Features gated by frontmatter flags (`approved`, `loop-skip`, `guidance-aware`, etc.) not clearly described for the user.
- **Add documentation entries**
  - For any such features, add concise entries in the appropriate docs:
    - Pipeline-specific behavior in `Pipelines.md` or the relevant pipeline section.
    - Rule/flag behavior in `Rules.md`, `Parameters.md`, or `Backbone.md`.
    - User-facing workflows for special modes in the relevant workflow docs.

### 7. Consistency and gap check

- **Cross-check coverage**
  - Verify that every always/context rule and every core skill has at least one mention in the docs where a power user could discover and understand it.
  - Ensure that all core workflows (capture, organize, think/distill, express, archive, roadmap) have:
    - A narrative explanation.
    - Pointers to relevant rules/skills.
    - Notes on safety behavior and approval flows.
- **Spot-check user stories**
  - Walk through a few representative user stories (e.g. "I just dropped a PDF in Ingest", "I want to distill a dense research note", "I want to archive an old project", "I want to advance a roadmap phase") and ensure the docs answer:
    - What commands/modes to run.
    - What will happen step-by-step.
    - How to recover or override when confidence is low or errors occur.

### 8. Prepare for implementation and iterations

- **Prioritized edit list**
  - Produce a concise prioritized list of specific doc edits/additions to make (file + section + brief change description), starting with the highest impact gaps.
- **Iteration plan**
  - Propose an iteration order (e.g. ingest & PARA basics → pipelines & safety → roadmap → advanced/async flows) so we can update docs in coherent passes.

## Todos

- **inventory-backbone**: Inventory rules, skills, and backbone docs related to Second Brain pipelines and roadmap.
- **map-rules-skills-docs**: Map each rule/skill to pipelines and existing doc mentions.
- **detect-stale-docs**: Compare docs vs implementation to find stale or inaccurate descriptions.
- **update-core-docs**: Update `Backbone.md`, `Vault-Layout.md`, and core pipeline docs to match actual behavior.
- **document-workflows**: Ensure ingest, distill, express, archive, and roadmap user workflows are fully documented end-to-end.
- **surface-hidden-features**: Identify and document hidden or undocumented features and flags.
- **final-gap-check**: Run a coverage pass so every core rule/skill/workflow is discoverable and accurately described.

