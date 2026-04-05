---
title: Phase 2.3 - Pipeline validation and pre-commit verification
roadmap-level: secondary
phase-number: 2
subphase-index: "2.3"
project-id: godot-genesis-mythos-master
status: active
priority: high
progress: 40
handoff_readiness: 82
created: 2026-03-30
tags:
  - roadmap
  - godot-genesis-mythos-master
  - phase-2
para-type: Project
links:
  - "[[Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-03-30-0430]]"
  - "[[Phase-2-1-Pipeline-Stages-Seed-to-World-Roadmap-2026-03-30-2205]]"
  - "[[Phase-2-2-Intent-Resolver-and-Hook-Mapping-Roadmap-2026-03-30-2310]]"
---

## Phase 2.3 - Pipeline validation and pre-commit verification

This secondary slice defines how staged outputs and hook envelopes are **validated as a coherent bundle** before any commit boundary mutates world state. It sits **after** the **2.1** stage spine and **2.2** intent resolver + hook mapping, and **before** the collaborative commit loop described on the Phase 2 primary note.

## Scope

**In scope:**
- Validation gate taxonomy (what must pass for a dry-run frame to advance toward commit).
- Pre-commit verification bundle: what is checked together (staged deltas + hook payloads + validation labels) **at NL** for conceptual design authority.
- Traceability between **2.1** typed outputs / **2.2** envelopes and the pass/fail surface that blocks commit.
- Contract for **test-plan rows** and **acceptance criteria** (scaffolded under **2.3.1**; executable tests/CI deferred).

**Out of scope:**
- Concrete test harness code, CI job names, or benchmark thresholds.
- Cryptographic proofs of bundle integrity (execution-deferred; see **2.1.4** waiver pattern).
- UX for showing validation failures to players/DMs.

## Behavior (natural language)

Inputs: a **dry-run validation frame** containing staged outputs from the pipeline spine, **HookPayloadOutline**-compatible envelopes from **2.2**, and **validation labels** from **2.2.5** chunk boundaries.  
The validation subsystem evaluates the bundle against the gate taxonomy; failures produce **no partial commit** and **actionable diagnostics** (at NL).

Ordering:
1. Assemble a **PreCommitVerificationBundle** (conceptual aggregate) from staged deltas + hook payloads + validation labels.
2. Run **gate stages** in spine-aligned order (stage-order consistency with **2.1** apply ordering).
3. Emit deterministic **pass/fail** per gate + rollup for commit eligibility.
4. Hand off pass/fail + diagnostics to the collaborative commit loop (Phase 2 primary glue) without mutating world state on failure.

## Interfaces

Upstream:
- Consumes **StagedDeltaBundle** + merge semantics from **2.1.3** (and replay/diff from **2.1.4** / **2.1.5** as applicable).
- Consumes **deterministic hook emission + pre-commit handoff** contracts from **2.2.4** and **validation labels + chunking** from **2.2.5**.

Downstream:
- Tertiary notes under **2.3** refine **test-plan matrices**, **acceptance criteria** rows, and **failure taxonomy** for operators.

Outward guarantees:
- **No commit** when any gate in the **mandatory** set fails.
- Same inputs + same catalog revisions → same validation outcome (deterministic at NL; execution replay proofs deferred).

## Edge cases

- Partial validation failure mid-gate: downstream gates are **skipped**; bundle remains **uncommitted**.
- Oversized bundles: chunk boundaries from **2.2.5** must still yield a **single** rollup decision for commit eligibility (conceptual contract).
- Catalog drift: validation rules may reference **HookSchemaCatalog** and **validation label** revisions; pinning behavior is **execution-deferred** per **2.2.2** open questions.

## Open questions

- **D-2.3-diagnostics-granularity:** Whether operator-facing diagnostics should be **per-gate** or **rolled up** into a single human-readable failure code (execution UX deferred) — see [[decisions-log]].
- **D-2.3-warm-cache-shortcuts:** Whether **warm-cache** validation shortcuts are allowed for repeated dry-run frames (perf deferred) — see [[decisions-log]].

## Pseudo-code readiness

At this primary secondary depth, pseudo-code is not required. Readers should be able to sketch gate ordering, bundle composition, and pass/fail rollup without algorithm-level detail; **2.3.1** holds **test-plan** and **acceptance-criteria** scaffolding.

## Research integration

> [!note] External grounding
> No `Ingest/Agent-Research/` notes were bound this run; alignment is pattern-only from deterministic validation-gate pipelines.

## Tertiary notes

```dataview
TABLE WITHOUT ID roadmap-level AS "Level", file.link AS "Note", subphase-index AS "Index", status, progress AS "%"
FROM "1-Projects/godot-genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building/Phase-2-3-Pipeline-Validation-and-Pre-Commit-Verification"
WHERE roadmap-level = "tertiary" OR roadmap-level = "task"
SORT subphase-index ASC, file.name ASC
```
