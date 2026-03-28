---
name: roadmap-research-depth-migration
overview: Align RESUME-ROADMAP research triggering with depth-based roadmap structure so primaries never auto-research while secondary+ nodes can use util- and gap-based triggers safely.
todos:
  - id: analyze-current-auto-roadmap-logic
    content: Review current auto-roadmap RESUME-ROADMAP deepen branch to locate util-based research enabling and identify exact `current_phase > 2` usage.
    status: completed
  - id: switch-research-gate-to-depth
    content: Refactor auto-roadmap util-based research gate to use current_depth (from current_subphase_index) and require current_depth ≥ 2 instead of current_phase > 2.
    status: completed
  - id: enforce-depth-check-in-gap-fill
    content: Update roadmap-deepen gap-fill hook so research-agent-run (gap-fill) only executes when current_depth ≥ 2, protecting primaries even if enable_research is mis-set.
    status: completed
  - id: update-parameters-and-vault-layout-docs
    content: Revise Parameters.md and Vault-Layout.md to describe depth-based research gating and ensure examples use secondary/tertiary terminology instead of phase-based gating.
    status: completed
  - id: refresh-roadmap-upgrade-and-pipelines-docs
    content: Update Roadmap-Upgrade-Plan.md, Pipelines.md, and the inward-gap-triggered-research-upgrade plan to reference depth-aware (secondary+) research triggering.
    status: completed
  - id: sync-cursor-mirror-files
    content: Propagate rule and skill wording changes into .cursor/sync/rules/context/auto-roadmap.md and .cursor/sync/skills/roadmap-deepen.md per backbone-docs-sync.
    status: completed
isProject: false
---

## Roadmap Research Depth Migration Plan

### 1. Clarify desired behavior

- **Primary vs non-primary**: Treat any roadmap position with `current_subphase_index` representing only the phase (e.g. `"1"`, or no subphase) as **primary**, and anything with at least one "." (e.g. `"1.1"`, `"1.1.1"`, etc.) as **secondary+**.
- **Research eligibility rule**: Research (pre-deepen and gap-fill) should be **eligible only when current_depth ≥ 2**; primaries (depth 1) must not auto-trigger research regardless of util.
- **Gates to preserve**: Keep existing **util threshold**, **research_cooldown**, **research_conf_veto_threshold**, and **gap severity** checks; simply change the structural gate from phase-number based to depth-based.

### 2. Update auto-roadmap research enabling logic

- **File**: `[.cursor/rules/context/auto-roadmap.mdc](/home/darth/Documents/Second-Brain/.cursor/rules/context/auto-roadmap.mdc)`.
- **Change**:
  - Introduce or reuse a `**current_depth`** computation from `current_subphase_index` (same semantics as in `roadmap-deepen`: `"1"→1`, `"1.1"→2`, `"1.1.1"→3`, ...).
  - Replace the `**current_phase > 2`** condition in the util-based research gate with `**current_depth >= 2`**.
  - Ensure gap-aware triggers and tag/keyword-based triggers also **respect depth** where appropriate (e.g. only consider them when `current_depth ≥ 2`, unless you explicitly want gap-research even on primaries).
- **Result**: Util-based `enable_research_from_util` and derived `enable_research` will only ever become true for secondary+ positions, regardless of phase number.

### 3. Align roadmap-deepen gap-fill behavior with depth rule

- **File**: `[.cursor/skills/roadmap-deepen/SKILL.md](/home/darth/Documents/Second-Brain/.cursor/skills/roadmap-deepen/SKILL.md)`.
- **Change**:
  - In step **4.5 Gap analysis and optional gap-fill research**, add an explicit check that **gap-fill research only runs when `current_depth ≥ 2`** (using the same depth computation already documented in the skill).
  - Ensure `**research_used**` and `gaps` logging still occurs, but gap-fill cannot fire for primaries even if params mistakenly set `enable_research: true`.
- **Result**: Even if a caller misconfigures params, primaries will not run gap-fill research; secondaries and deeper keep the current gap-driven behavior.

### 4. Keep workflow_state + Parameters in sync

- **Files**:
  - `[1-Projects/genesis-mythos-master/Roadmap/workflow_state.md](/home/darth/Documents/Second-Brain/1-Projects/genesis-mythos-master/Roadmap/workflow_state.md)` (schema reference).
  - `[3-Resources/Second-Brain/Parameters.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Parameters.md)`.
  - `[3-Resources/Second-Brain/Vault-Layout.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Vault-Layout.md)`.
- **Change**:
  - Update the **Research (pre-deepen)** section in `Parameters.md` to describe the **depth-based gate**: mention that util-based research is considered only when `last_ctx_util_pct < research_util_threshold` **and current_depth ≥ 2**, not `current_phase > 2`.
  - In `Vault-Layout.md`, clarify that `last_ctx_util_pct` is used in combination with **current_depth** (derived from `current_subphase_index`) to decide research eligibility.

### 5. Update higher-level docs and upgrade plan

- **Files**:
  - `[3-Resources/Second-Brain/Roadmap-Upgrade-Plan.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Roadmap-Upgrade-Plan.md)`.
  - `[3-Resources/Second-Brain/Pipelines.md](/home/darth/Documents/Second-Brain/3-Resources/Second-Brain/Pipelines.md)`.
  - `[.cursor/plans/inward-gap-triggered-research-upgrade_a8ff0070.plan.md](/home/darth/Documents/Second-Brain/.cursor/plans/inward-gap-triggered-research-upgrade_a8ff0070.plan.md)` if it encodes assumptions about phase-based triggers.
- **Change**:
  - Replace any textual references to `**current_phase > 2`** for research auto-enable with **depth-based language** (`current_depth ≥ 2`, secondary+ notes).
  - In the Roadmap Upgrade Plan, explicitly call out: *“Primaries (phase containers) do not trigger external research; secondary and deeper nodes may, based on util + conf + gaps.”*
  - Ensure Pipelines.md’s RESUME-ROADMAP description mentions **depth-aware** research triggers.

### 6. Sync .cursor/sync mirror files

- **Files**:
  - `[.cursor/sync/rules/context/auto-roadmap.md](/home/darth/Documents/Second-Brain/.cursor/sync/rules/context/auto-roadmap.md)`.
  - `[.cursor/sync/skills/roadmap-deepen.md](/home/darth/Documents/Second-Brain/.cursor/sync/skills/roadmap-deepen.md)`.
- **Change**:
  - Mirror the updated text/logic from the primary rule and skill into the corresponding `.cursor/sync` files, per **backbone-docs-sync.mdc**.

### 7. Sanity-check behavior on the current project

- **Dry-run reasoning only (no edits here)**:
  - Conceptually simulate a RESUME-ROADMAP deepen run at:
    - **Primary**: `current_subphase_index: "1"`, low util → verify that, under new logic, no research path would fire.
    - **Secondary/Tertiary**: `current_subphase_index: "1.2.3"`, low util (e.g. 1%) → confirm that util + cooldown + conf gates would allow `enable_research_from_util = true` and potentially run research.
  - Confirm that **gap-fill** in `roadmap-deepen` can run for 1.2.3 but never for a pure phase container.

### 8. Regression considerations

- Ensure that changing from phase-based to depth-based gating does **not** break late-phase behavior:
  - Phases 3–6 primaries still won’t auto-research (by design), but their **secondary+ children** will continue to use research just as before when util is low.
  - Existing `research_cooldown`, `research_synth_cap_tokens`, and error paths (`#research-failed`, `#research-empty`) remain unchanged.
- Note for future: if you ever want **explicit override** (e.g. research even on primary for a special phase), that should come from **explicit `enable_research: true` in the queue entry**, not from util-based auto-enable.

