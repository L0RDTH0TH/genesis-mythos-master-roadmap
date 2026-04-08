---
name: Decision Tracking Enhancement
overview: "Implement a hybrid, system-wide decision-tracking upgrade: canonical global spec plus per-project decision-log adoption, with queue/harness integration and a Decision Codex surface specification."
todos:
  - id: canon-spec
    content: Define and publish canonical global decision-tracking schema and invariants
    status: completed
  - id: rules-enforcement
    content: Update decision-related rules and mirrored sync files to enforce schema
    status: completed
  - id: project-adoption
    content: Apply enhanced decision structure to key sandbox/godot decisions
    status: completed
  - id: queue-harness
    content: Integrate decision completeness expectations into queue/harness docs
    status: completed
  - id: codex-spec
    content: Draft Decision Codex UI/spec and optional lore mirror hook
    status: completed
isProject: false
---

# Decision Tracking Enhancement Plan

## Objective

Strengthen decision tracking as a deterministic, append-only, auditable layer across conceptual and execution tracks, with explicit option-tradeoff capture and clear linkage into queue/harness telemetry.

## Baseline Anchors

- Existing operator-pick conventions and grep-stable patterns are already defined in [Decisions-Log-Operator-Pick-Convention](3-Resources/Second-Brain/Docs/Decisions-Log-Operator-Pick-Convention.md).
- Track authority boundaries already exist in [Dual-Roadmap-Track](3-Resources/Second-Brain/Docs/Dual-Roadmap-Track.md).
- Queue dispatch + harness hooks live in [Queue-Pipeline](3-Resources/Second-Brain/Docs/Pipelines/Queue-Pipeline.md) and queue agent rules.
- Current project logs are rich but uneven in option-rationale structure: [sandbox decisions-log](1-Projects/sandbox-genesis-mythos-master/Roadmap/decisions-log.md), [godot decisions-log](1-Projects/godot-genesis-mythos-master/Roadmap/decisions-log.md).

## Implementation Phases

### Phase 1: Canonical Decision Framework (Global, Hybrid Canonical)

- Create/upgrade a canonical doc under `3-Resources/Second-Brain/Docs/` defining the mandatory decision schema:
  - append-only amendment model
  - required option tradeoff table for non-trivial decisions
  - required rationale block (`why selected`, `why rejected`)
  - required linkage fields (affected systems, execution refs, validator refs, queue IDs)
  - `World Impact` field (optional globally, but encouraged for decisions touching persistence, react matrix, player experience, or blindspots)
- Explicitly codify the hybrid model: global canonical spec in Second-Brain docs + per-project mirrors/templates in each roadmap area.
- Add a short worked example using the 2026-04-08 player UX authority decision so operators can apply the schema immediately.
- Align with current grep-stable labels so existing automations keep working.
- Add explicit “Grok/GitHub visibility” note for decision-authority sync requirements.

### Phase 2: Rule + Sync Enforcement Contract

- Update decision-related rules in `.cursor/rules/` to require:
  - option-tradeoff capture on new D-* decisions
  - append-only amendment entries instead of retroactive rewrites
  - explicit option-pick lines for operator commits where applicable
  - for front-end blindspots/living-world decisions, require `World Impact` plus at least one linkage to either a front-end flow or Markdown lore hook
- Mirror changes into `.cursor/sync/` per backbone sync rules.
- Document failure/repair behavior when required decision fields are missing.

### Phase 3: Per-Project Adoption (Sandbox + Godot)

- Add a compact “Decision Template” artifact per project roadmap area (hybrid model) referencing the global canonical spec.
- Normalize key high-impact existing decisions without rewriting historical meaning:
  - start with `D-2026-04-08-frontend-player-ux-authority`
  - include one simulation/react-matrix decision to prove the framework beyond UX
- Place `Decision-Template.md` in each project decisions area with a prominent backlink to the global canonical spec.
- Ensure conceptual and execution decision lines cross-link correctly (including execution state and validator evidence links).

### Phase 4: Queue/Harness Integration

- Extend queue/harness docs/rules so pipeline outputs include decision metadata expectations (option class, rationale presence, linkages) in advisory/strict validation modes.
- Define how decision-preflight and post-little-val checks should flag missing option rationale as structured hygiene findings.
- Ensure Watcher/queue traces remain parse-safe while carrying decision completeness signals.

### Phase 5: Decision Codex Surface Spec (No Runtime Build Yet)

- Produce a UI/spec document for a lightweight Decision Codex view:
  - DM view: full list + backlink/graph-style relationships, filters by date/phase/subsystem/`World Impact`, keyword search, and “decisions since last session”
  - player-facing mirror: read-only filtered view for player-visible decisions (e.g., linked to player-facing lore/journal/event surfaces)
  - lore integration contract: on decision commit (or manual trigger), append a human-readable summary into `Meta/Decisions/` through the spine event path
- Keep this as spec-level output (no app/runtime implementation in this pass).

## Deliverables

- Updated canonical decision framework doc in `3-Resources/Second-Brain/Docs/`.
- Updated rules + synced `.cursor/sync` counterparts enforcing enhanced decision structure.
- Updated sandbox and godot decision logs for selected priority decisions using new structure (UX authority + one simulation/react-matrix exemplar).
- Updated queue/harness docs for decision completeness validation semantics.
- Decision Codex surface specification doc with DM view, player-facing mirror, and lore append hook.

## Validation

- Grep checks confirm required labels/patterns still match legacy automation expectations.
- Sample D-* entries in both projects include explicit options + rationale + linkages; required `World Impact` present where applicable.
- Queue/harness docs describe expected decision completeness signals and outcomes.
- Cross-links resolve between decisions, execution state files, and validator artifacts.

