---
title: Phase 2.2.3 — Intent & Hook Lifecycle and Sync
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.2.3"
project-id: genesis-mythos-master
status: archived
priority: high
progress: 0
created: 2026-03-09
tags: [roadmap, genesis-mythos-master, phase, subphase]
para-type: Archive
links:
  - "[[Phase-2-2-Intent-Schema-Hook-Graphs-Roadmap-2026-03-09-1335]]"
---

## Phase 2.2.3 — Intent & Hook Lifecycle and Sync

Define how intents and their derived hooks are created, updated, deprecated, and kept in sync with generated content and long-lived simulation state, so nothing drifts silently or becomes an untraceable ghost.

Mid-technical: interfaces and algorithm sketches for lifecycle flows, not full pseudo-code — focus on states, transitions, and invariants.

### Lifecycle states and transitions

- [ ] Enumerate lifecycle states for **intents** and **hooks**
  - [ ] Intents:
    - [ ] `drafted` — raw text plus minimal metadata; not yet trusted by the generator.
    - [ ] `normalized` — parsed into a typed structure with fields from 2.2.1; safe to feed into mapping rules.
    - [ ] `bound_to_seeds` — linked to concrete world anchors (regions, entities, factions) after generation.
    - [ ] `active` — currently influencing world/simulation through hooks.
    - [ ] `cooled_down` — still present for history but with reduced or zero mechanical effect.
    - [ ] `deprecated` — frozen for audit only; no further mechanical influence allowed.
  - [ ] Hooks:
    - [ ] `proposed` — derived from intents but not yet attached to concrete owners.
    - [ ] `attached` — owner_ref resolved; visible to pipeline and simulation, not yet fully active.
    - [ ] `active` — participates in evaluations each tick or generation run.
    - [ ] `suppressed` — temporarily disabled; preserved for potential reactivation.
    - [ ] `expired` — past its validity window; pending cleanup or archival.
    - [ ] `removed` — logically deleted; only retained in audit logs.
  - [ ] For each state pair (intent, hook), document:
    - [ ] Allowed transitions (state diagram).
    - [ ] Which subsystem may trigger the transition (UI, pipeline, simulation, maintenance jobs).
    - [ ] Whether the transition must be reversible, and under what constraints.
- [ ] Define transition triggers
  - [ ] User-driven:
    - [ ] DM/player creates or edits intent text.
    - [ ] DM explicitly archives or reactivates an intent or hook from a UI.
  - [ ] System-driven:
    - [ ] Generation re-runs rebind intents to new/updated seeds.
    - [ ] Simulation thresholds (e.g. cooled_down after N sessions without relevant events).
    - [ ] Conflict resolution outcomes (e.g. one of several competing hooks wins, others are suppressed or expired).
  - [ ] Error/rollback:
    - [ ] Invalid data detected (schema violations, missing owners).
    - [ ] Rule conflicts that cannot be auto-resolved.
    - [ ] Failed downstream projections that require rolling back to a previous lifecycle state.

### Creation and update flows

- [ ] Spell out canonical **creation flow** from raw text to normalized intent to hooks
  - [ ] Capture step:
    - [ ] Accept raw DM/player text plus metadata (author id, timestamp, campaign id, session context).
    - [ ] Store as an immutable capture record for audit.
  - [ ] Normalization step:
    - [ ] Run parser/classifier to map raw text to an intent type (e.g. faction rivalry, cursed artifact, regional omen).
    - [ ] Populate required fields (targets, strength, duration, narrative tags) per 2.2.1.
    - [ ] Mark the intent as `normalized` only when all required fields are present and validated.
  - [ ] Hook derivation step:
    - [ ] Evaluate mapping rules (from 2.2.2) to determine which hook templates apply.
    - [ ] For each template, create one or more hooks in `proposed` state, tagged with a shared provenance id.
    - [ ] When world anchors exist, immediately bind owner_ref and move hooks to `attached`.
  - [ ] Persistence step:
    - [ ] Write normalized intent and hooks in one logical transaction so provenance is never half-written.
    - [ ] Emit an event for downstream systems (e.g. “intent_normalized”, “hooks_created”) with references.
- [ ] Define **update semantics**
  - [ ] Field-level rules:
    - [ ] Non-structural changes (e.g. description, flavor text) update intent only; hooks remain untouched.
    - [ ] Parameter tweaks (e.g. weight, radius, cooldown) may update hook payloads in-place when safe.
    - [ ] Structural changes (e.g. different targets, new type) require deprecate‑and‑recreate for affected hooks.
  - [ ] Idempotency and monotonicity:
    - [ ] Re-applying the same edit should not create duplicate hooks or drift provenance.
    - [ ] When strengthening or weakening an effect, enforce monotonic constraints where appropriate (e.g. never silently invert intent meaning).
  - [ ] Downstream regeneration decisions:
    - [ ] Define when an intent edit should:
      - [ ] Trigger full regeneration for a narrow scope (e.g. a town, a faction network).
      - [ ] Apply only incremental deltas to simulation state.
      - [ ] Be deferred until a scheduled maintenance window.

### Deprecation, expiry, and garbage collection

- [ ] Define rules for **intent deprecation**
  - [ ] Criteria: explicit DM archive, age without references, campaign-phase shifts, or player resolution of the underlying narrative.
  - [ ] Effects: mark intent deprecated but keep provenance available for audit.
- [ ] Define rules for **hook expiry and removal**
  - [ ] Time-based expiry (e.g. after N sessions or ticks with no relevant events).
  - [ ] Condition-based expiry (e.g. when target entity or region is removed/merged).
  - [ ] Hard safety invariant: never silently delete a hook that still has active references in simulation state or UI views.
- [ ] Design a **maintenance pass**
  - [ ] Background job or command that:
    - [ ] Scans for stale hooks and intents per rules above.
    - [ ] Produces a report (per campaign) before applying destructive changes.
    - [ ] Applies changes transactionally with rollback or snapshot support.

### Sync between intents, hooks, and generated content

- [ ] Describe how to keep **generated content** aligned with evolving intents
  - [ ] Define a change-classification step that labels edits as:
    - [ ] “Local mechanical” (parameter-only, no world layout changes).
    - [ ] “Structural local” (affects a handful of entities/regions).
    - [ ] “Structural global” (affects many regions or core generators).
  - [ ] For each class, specify:
    - [ ] Whether to re-run generation for specific regions/entities.
    - [ ] Whether to apply incremental patches to world state only.
    - [ ] Whether to adjust simulation parameters without touching layout.
  - [ ] Specify diff surfaces:
    - [ ] Per-region and per-entity previews (“these towns gain +2 cult influence, these lose −1”).
    - [ ] Global summaries (pressure maps, faction strength deltas).
- [ ] Define **consistency checks**
  - [ ] Periodic scan to detect:
    - [ ] Hooks referencing missing owners.
    - [ ] Intents with no corresponding hooks in world/sim state.
    - [ ] Hooks with provenance pointing to deprecated or missing intents.
  - [ ] For each inconsistency type, decide:
    - [ ] Auto‑repair path (e.g. reattach hook, regenerate owner, or deprecate hook).
    - [ ] When to require explicit DM approval via a maintenance UI.

### Observability and audit for lifecycle

- [ ] Design audit trail requirements
  - [ ] Every change to an intent or hook (create, update, deprecate, suppress, expire) must be logged with:
    - [ ] Actor (user vs system module).
    - [ ] Reason (rule name, UI action, threshold crossed).
    - [ ] Before/after snapshots of key fields.
  - [ ] Decide log retention strategy and how to surface logs in‑game or via external tools.
- [ ] Define DM-facing lifecycle views
  - [ ] Per-intent history: timeline of all lifecycle events and linked hooks.
  - [ ] Per-hook history: how its payload and status evolved over time and why.
  - [ ] Campaign‑level view: aggregated stats (active vs cooled_down vs deprecated intents; active vs expired hooks).

### Test scenarios and invariants

- [ ] Scenario: intent edit without world regeneration
  - [ ] Edit an active intent’s weight/priority.
  - [ ] Verify hooks update correctly and downstream simulation changes without tearing up existing world structure.
- [ ] Scenario: narrative resolution and cleanup
  - [ ] Mark a story arc as resolved.
  - [ ] Confirm intents move to deprecated, hooks expire or are suppressed, and simulation gradually returns to baseline while preserving history.
- [ ] Scenario: campaign migration or fork
  - [ ] Fork a campaign state.
  - [ ] Ensure intents and hooks can diverge safely in each branch without corrupting shared provenance.
- [ ] Global invariants:
  - [ ] No hook exists without a valid intent provenance pointer.
  - [ ] No active intent exists whose hooks are all expired without a clear reason.
  - [ ] Lifecycle transitions are reversible or auditable enough to debug any surprising world behavior.

