---
name: para-path-proposal-integration
overview: Integrate obsidian_propose_para_paths as the ranked PARA destination engine across ingest Decision Wrappers, organize/archive pipelines, and move-failure fallbacks, while preserving subfolder-organize as the structural path builder.
todos:
  - id: audit-current-references
    content: Scan rules and docs for all references to subfolder-organize, obsidian_subfolder_organize, and propose_alternative_paths to understand current usage and contracts.
    status: completed
  - id: ingest-wrapper-switch
    content: Change Decision Wrapper creation to use obsidian_propose_para_paths (context_mode wrapper) as the candidate source, wiring candidates[i].path/score/reason_short into the template.
    status: completed
  - id: ingest-midband-update
    content: Update ingest mid-band loop docs to describe using obsidian_propose_para_paths for ranked candidates feeding calibrate_confidence/verify_classification.
    status: completed
  - id: fallback-doc-update
    content: Align mcp-obsidian-integration and Backbone docs so that propose_alternative_paths is documented as backed by obsidian_propose_para_paths.
    status: completed
  - id: organize-archive-advisory
    content: Integrate obsidian_propose_para_paths as an advisory step in autonomous-organize and autonomous-archive, keeping subfolder-organize as the structural path builder and move source.
    status: completed
  - id: independent-usage-design
    content: Design manual and garden-review flows that call obsidian_propose_para_paths for suggestions without moving notes (PARA suggestions command, orphan relocation hints, path-review mode).
    status: completed
  - id: backbone-pipelines-docs
    content: Update Backbone, Pipelines, and related Second-Brain docs to describe obsidian_propose_para_paths, its context modes, and where it is used.
    status: completed
  - id: validation-and-tuning
    content: Run small-scope tests comparing obsidian_propose_para_paths recommendations vs subfolder-organize paths, and visually inspect Decision Wrappers to tune weights and rationale style as needed.
    status: completed
isProject: false
---

## PARA path proposal & Decision Wrapper integration plan

### 1. Confirm current behavior and contracts

- **Review MCP tools and server code**
  - Re-read `user-obsidian-para-zettel-autopilot` MCP descriptors for `obsidian_subfolder_organize`, `obsidian_classify_para`, and the new `obsidian_propose_para_paths`/`propose_para_paths` behavior.
  - Verify `propose_alternative_paths` is now a thin shim around `propose_para_paths` (context_mode `organize`) and confirm returned JSON shapes.
- **Review vault-side contracts**
  - In `[.cursor/rules/context/para-zettel-autopilot.mdc](/home/darth/Documents/Second-Brain/.cursor/rules/context/para-zettel-autopilot.mdc)` and its sync copy, re-check the Decision Wrapper creation section to see exactly where `obsidian_subfolder_organize` is referenced.
  - In `[3-Resources/Second-Brain/Cursor-Skill-Pipelines-Reference.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Cursor-Skill-Pipelines-Reference.md)`, locate all mentions of `subfolder-organize`, `obsidian_subfolder_organize`, and `propose_alternative_paths` across ingest, organize, archive, and fallback sections.
  - In `[.cursor/rules/always/mcp-obsidian-integration.mdc](/home/darth/Documents/Second-Brain/.cursor/rules/always/mcp-obsidian-integration.mdc)` and `[3-Resources/Second-Brain/Backbone.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Backbone.md)`, confirm the documented fallback chain around `propose_alternative_paths`.

### 2. Replace multi-candidate usage with obsidian_propose_para_paths

- **Ingest Decision Wrapper creation (Phase 1)**
  - In `para-zettel-autopilot.mdc` (and sync copy), change the wrapper-creation step to call `obsidian_propose_para_paths` instead of `obsidian_subfolder_organize` for multi-candidate proposals, using `context_mode: "wrapper"`, `rationale_style: "concise"`, and `max_candidates: 5`.
  - Map the response:
    - `candidate_a_path`…`candidate_e_path` from `candidates[i].path`.
    - `candidate_a_conf`…`candidate_e_conf` from `round(candidates[i].score)`.
    - `candidate_a_reason`…`candidate_e_reason` from `candidates[i].reason_short`.
  - Ensure this is documented as the **canonical source** of paths and reasoning for wrappers.
- **Ingest mid-band confidence loop**
  - In the ingest section of `Cursor-Skill-Pipelines-Reference.md`, replace the text that says to use `obsidian_subfolder_organize` for 2–3 candidates with language that calls `obsidian_propose_para_paths` (context_mode `midband`) for ranked candidates.
  - Keep `calibrate_confidence` and `verify_classification` usage, but clarify they now consume the top candidate(s) from `obsidian_propose_para_paths` rather than raw `subfolder_organize` output.
- **Move-failure fallback (`propose_alternative_paths`)**
  - In `mcp-obsidian-integration.mdc`, update the fallback table narrative so that when it says “trigger `propose_alternative_paths`”, it explicitly notes that this call is **backed by `obsidian_propose_para_paths`** and returns ranked `{path, score, rationale/reason_short}`.
  - Mirror this clarification anywhere `propose_alternative_paths` is mentioned in `Backbone.md` and `Autonomous-Runs-Options-Reference.md`.

### 3. Integrate alongside subfolder-organize in organize/archive

- **Autonomous-organize pipeline**
  - In `auto-organize.mdc` and the organize section of `Cursor-Skill-Pipelines-Reference.md`, keep `subfolder-organize` as the path builder feeding `obsidian_move_note`.
  - Add an optional advisory step: call `obsidian_propose_para_paths` with `context_mode: "organize"` before move, compare its `recommended_index` path to the `subfolder-organize` path, and:
    - If paths match, optionally log `overall_confidence` and `reason_short` into `Organize-Log`.
    - If they diverge, log a soft note that the semantic recommendation differs but still trust the structural choice (no auto override).
- **Autonomous-archive pipeline**
  - In `auto-archive.mdc` and the archive section of `Cursor-Skill-Pipelines-Reference.md`, keep `subfolder-organize` for archive path computation.
  - Optionally call `obsidian_propose_para_paths` (context_mode `organize` or a future `archive`) after `archive-check` and before move; use `reason_short` as a human-facing “why this archive bucket” explanation in `Archive-Log`.
  - Document that in archive, `obsidian_propose_para_paths` is advisory and must never bypass `archive-check` gates.
- **Ingest apply-mode (approved wrappers)**
  - In the apply-mode section of `para-zettel-autopilot.mdc`, keep `hard_target_path` from the wrapper as the authoritative move destination.
  - Optionally call `obsidian_propose_para_paths` with `context_mode: "wrapper"` and log when user-chosen `hard_target_path` disagrees with the top recommended path; ensure rules state that user choice wins and recommendations are for logging/analysis only.

### 4. New independent usages (not tied to current folder)

- **Manual “Suggest PARA homes” command**
  - Define a simple context rule or Commander macro for actions like “Suggest PARA paths for this note”.
  - For the current note (Ingest or PARA), call `obsidian_propose_para_paths(context_mode: "manual" or "organize")` with `max_candidates` 3–5 and show candidates plus `reason_short` in a report or callout, without moving anything.
  - Document this flow in a small section of the Second-Brain docs (e.g., an "On-demand PARA suggestions" subsection).
- **Garden review and orphan handling**
  - In the Garden review and CHECK_WRAPPERS/orphan sections (`Cursor-Skill-Pipelines-Reference.md`, `auto-eat-queue.mdc`), plan an optional step for orphans/true-orphans: call `obsidian_propose_para_paths(context_mode: "manual")` on the recovered companion note and:
    - Either surface suggested new homes in the wrapper’s `Wrapper state` block, or
    - Create a new Decision Wrapper targeting the current location.
  - Clarify that this is non-destructive and advisory until the user approves moves.
- **Refile suggestions for existing PARA notes**
  - Sketch a future "PATH-REVIEW" or "ORGANIZE SUGGESTIONS" mode that:
    - Scans 1-Projects/2-Areas/3-Resources notes.
    - Calls `obsidian_propose_para_paths(context_mode: "organize")` for each.
    - Logs cases where the recommended path differs significantly from current, feeding into a manual refile queue (no auto-move).
  - Note this as an optional later phase, separate from the immediate ingest/Decision Wrapper integration.

### 5. Documentation and sync updates

- **Backbone and Pipelines docs**
  - In `[3-Resources/Second-Brain/Backbone.md]`, add a concise paragraph describing `obsidian_propose_para_paths` as the ranked PARA destination engine, built on top of `obsidian_subfolder_organize`, and list where it is used (Decision Wrappers, mid-band loops, move fallbacks).
  - In `[3-Resources/Second-Brain/Pipelines.md]`, update ingest/organize/archive descriptions so that any mention of “multiple candidates from subfolder_organize” now points to `obsidian_propose_para_paths`.
  - In `[3-Resources/Second-Brain/Rules.md]` or `Parameters.md`, briefly document `context_mode` values and the rationale styles, especially that wrappers use `reason_short` for their one-line explanations.
- **Sync rules and changelog**
  - Ensure any changes to `.cursor/rules/always/` or `.cursor/rules/context/` are mirrored into `.cursor/sync/rules/`** per `backbone-docs-sync.mdc`.
  - Append a short entry to `.cursor/sync/changelog.md` capturing the introduction of `obsidian_propose_para_paths` as the multi-candidate engine and its integration points.

### 6. Validation and calibration

- **Local dry-runs (no destructive changes)**
  - For a small set of test notes (Ingest + PARA), call `obsidian_propose_para_paths` and compare its `recommended_index` path against current `subfolder-organize` output to ensure:
    - Paths are structurally valid and respect PARA roots.
    - `reason_short` reads well in wrapper-style contexts.
  - Use these tests to tune `PROPOSE_PARA_WEIGHTS[context_mode]` if needed (e.g., increasing or decreasing neighbor/theme influence).
- **Wrapper UX sanity check**
  - Generate a few Decision Wrappers with the new engine and visually check that:
    - Options A–G look sensible.
    - Reason lines are concise and informative.
    - Confidence percentages feel aligned with the ordering.

This plan keeps `subfolder-organize` as the structural path authority, while making `obsidian_propose_para_paths` the unified source for ranked candidates and human-readable reasons across ingest wrappers, mid-band loops, and move fallbacks.