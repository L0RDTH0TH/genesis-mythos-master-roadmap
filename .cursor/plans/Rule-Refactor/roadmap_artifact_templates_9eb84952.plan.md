---
name: Roadmap artifact templates
overview: Add canonical templates for ROADMAP state artifacts (workflow_state, roadmap-state, decisions-log, distilled-core, phase output) and update roadmap skills to instantiate missing artifacts from these templates so templates become the single source of truth.
todos:
  - id: add-artifact-templates
    content: Create `Templates/Roadmap/Artifacts/` with templates for workflow_state, roadmap-state, decisions-log, distilled-core, phase-output.
    status: completed
  - id: update-roadmap-generate
    content: Update `roadmap-generate-from-outline` to create missing artifacts by reading/filling templates instead of inline skeletons.
    status: completed
  - id: update-roadmap-deepen-bootstrap
    content: Update `roadmap-deepen` to bootstrap any missing artifacts from templates before proceeding.
    status: completed
  - id: update-phase-output-sync
    content: Update `roadmap-phase-output-sync` to create missing phase output files from template.
    status: completed
  - id: docs-sync
    content: Update `Templates.md` (and any related docs) to document the new artifact templates as authoritative.
    status: completed
isProject: false
---

## Goal

Make ROADMAP’s generated artifacts template-backed (single source of truth), so new projects get consistent schemas and any future schema changes happen in templates rather than scattered inline strings.

## What exists today (baseline)

- ROADMAP skills **define artifact schemas inline** and in docs, not via templates.
- `workflow_state.md` creation is specified inline in `[.cursor/skills/roadmap-generate-from-outline/SKILL.md](/home/darth/Documents/Second-Brain/.cursor/skills/roadmap-generate-from-outline/SKILL.md)` (see “5b. Create workflow_state.md if missing”).
- Artifact contracts are documented under “Roadmap state artifacts (multi-run)” in `[3-Resources/Second-Brain/Vault-Layout.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Vault-Layout.md)`.

## Templates to add (new files)

Create a new folder `Templates/Roadmap/Artifacts/` and add:

- `Templates/Roadmap/Artifacts/roadmap-state.md`
  - Frontmatter keys per Vault-Layout (at minimum `current_phase`, `status`, `version`, `last_run`, `completed_phases`, `drift_score_last_recal`, `handoff_drift_last_recal`).
  - Body sections for phase summaries + a spot for RECAL consistency reports.
- `Templates/Roadmap/Artifacts/workflow_state.md`
  - Frontmatter keys per Vault-Layout (incl. `current_phase`, `current_subphase_index`, `status`, `automation_level`, `iterations_per_phase`, optional `max_iterations_per_phase`, `iteration_guidance_ranges`, `chained_branch_count`, `last_ctx_util_pct`, `last_conf`).
  - Body includes **exact canonical `## Log` 12-column header + mandatory separator row** (per Vault-Layout).
- `Templates/Roadmap/Artifacts/decisions-log.md`
  - Minimal frontmatter and an append-friendly section structure (e.g. `## Decisions` + optional per-phase subsections).
- `Templates/Roadmap/Artifacts/distilled-core.md`
  - Frontmatter `core_decisions: []` plus required sections (e.g. Phase 0 anchors + Mermaid dependency graph placeholder) per Vault-Layout expectations.
- `Templates/Roadmap/Artifacts/phase-output.md`
  - A generic phase output skeleton (frontmatter placeholders for `phase-number`, `project-id`, etc.) that `roadmap-phase-output-sync` can create when missing.

## Skill changes (make templates authoritative)

Update roadmap skills so **on first creation** they read templates and fill placeholders, instead of embedding long literal skeletons.

- Update `[.cursor/skills/roadmap-generate-from-outline/SKILL.md](/home/darth/Documents/Second-Brain/.cursor/skills/roadmap-generate-from-outline/SKILL.md)`
  - In step **5b** (“Create workflow_state.md if missing”), replace inline schema construction with:
    - Read `Templates/Roadmap/Artifacts/workflow_state.md`.
    - Fill placeholders for `project_id`, timestamps, and any config-derived defaults (e.g. `iteration_guidance_ranges`, `max_iterations_per_phase`).
    - Create the file via MCP write (same behavior, but templated content).
  - Add parallel “create if missing” steps for:
    - `roadmap-state.md`
    - `decisions-log.md`
    - `distilled-core.md`
    (If those are currently created elsewhere, consolidate creation to a single “Phase 0 bootstrap” section in this skill.)
- Update `[.cursor/skills/roadmap-deepen/SKILL.md](/home/darth/Documents/Second-Brain/.cursor/skills/roadmap-deepen/SKILL.md)`
  - Add a **bootstrap guard** early (after path resolution, before heavy logic): if any required artifact is missing, create it from its template (without altering existing artifacts).
  - Keep existing invariants: never write context tracking columns as `"-"` when tracking is enabled; preserve the first `## Log` table semantics.
- Update `[.cursor/skills/roadmap-phase-output-sync/SKILL.md](/home/darth/Documents/Second-Brain/.cursor/skills/roadmap-phase-output-sync/SKILL.md)`
  - When `phase-X-output.md` is missing, create it from `Templates/Roadmap/Artifacts/phase-output.md` before syncing.

## Documentation sync (backbone)

Because this changes backbone behavior, update docs to match:

- `[3-Resources/Second-Brain/Templates.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Templates.md)`
  - Add a section listing the new `Templates/Roadmap/Artifacts/`* templates and which skill reads each.
- `[3-Resources/Second-Brain/Vault-Layout.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Vault-Layout.md)`
  - Add a note that artifact schemas are instantiated from templates (still keep schema definition here as the spec).

## Safety/compatibility notes

- **No migration required**: existing project artifacts remain as-is; templates only affect creation when missing.
- For future migrations (optional), a separate “normalize roadmap artifacts” operation could reconcile old artifacts with updated templates, but that’s intentionally out of scope for this change.

## Quick validation (after implementation)

- Run ROADMAP_MODE on a new test project and confirm these files appear under `1-Projects/<project_id>/Roadmap/`:
  - `workflow_state.md` with a valid `## Log` table (header + separator).
  - `roadmap-state.md`, `decisions-log.md`, `distilled-core.md`.
- Run one RESUME_ROADMAP deepen and verify workflow_state appends a row to the first `## Log` table and updates `last_ctx_util_pct` / `last_conf` frontmatter per spec.

