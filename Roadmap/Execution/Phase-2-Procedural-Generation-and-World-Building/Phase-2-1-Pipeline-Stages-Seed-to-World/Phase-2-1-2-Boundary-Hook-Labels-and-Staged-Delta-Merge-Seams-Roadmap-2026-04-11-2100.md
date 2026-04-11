---
title: Phase 2.1.2 (Execution) — Boundary hook labels and staged delta merge seams
created: 2026-04-11
tags:
  - roadmap
  - execution
  - sandbox
  - procedural-generation
  - phase-2-1-2
project-id: sandbox-genesis-mythos-master
roadmap_track: execution
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.1.2"
status: in-progress
handoff_readiness: 85
priority: high
progress: 35
conceptual_counterpart: "[[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-2-Stage-Family-Bodies-and-Boundary-Hooks-Roadmap-2026-03-30-1015]]"
para-type: Project
links:
  - "[[Phase-2-1-Pipeline-Stages-Seed-to-World-Roadmap-2026-04-11-2359]]"
  - "[[Phase-2-1-1-Stage-Family-Bodies-and-Boundary-Hooks-Roadmap-2026-04-12-1825]]"
---

# Phase 2.1.2 (Execution) — Boundary hook labels and staged delta merge seams

Execution tertiary **2.1.2** on the parallel spine under `Phase-2-1-Pipeline-Stages-Seed-to-World/`, mirroring conceptual **2.1.2** ([[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-2-Stage-Family-Bodies-and-Boundary-Hooks-Roadmap-2026-03-30-1015]]). **Linkage note:** the conceptual filename slug predates scope refinement; the conceptual note body is authoritative for **2.1.2** boundary-hook labels + merge seams (see conceptual § Scope / Behavior). This slice makes **boundary-hook outputs** explicit for execution: **validation outcome labels** flowing from Stage **4** into **merge seams** for **staged typed delta bundles** before the **commit boundary token** path—**text-only** interface contracts and `text` pseudocode only (no verbatim C++; **sandbox_code_precision** deferred).

## Scope (execution)

**In scope:**

- **ValidationDecisionLabels** (typed consumer-facing reasons) as a first-class seam artifact between Stage **4** dry-run validation and Stage **5** commit boundary.
- **Staged delta bundle merge seams:** how `TypedStageDeltaBundle` outputs from Stage **2** combine with validation labels and intent-merge policy inputs (aligns to Phase **1.2** graph “skip downstream / empty delta” vocabulary).
- **BoundaryHookSet** contract: `{ validation_labels, commit_allowed, commit_token_present }` as opaque execution-facing shapes (names only—no stdlib/engine headers this pass).
- Deterministic replay at the **label + merge** boundary: outputs depend only on typed Stage **4** artifacts + prior staged deltas + intent hook set (matches conceptual NL).

**Out of scope:**

- Verbatim C++, `static_assert`, or allowlisted URL citations (**sandbox_code_precision** — future slice with nested **Task(research)**).
- Registry–CI / **GMM-2.4.5** closure rows (execution-deferred unless evidenced).

## Behavior (execution contract)

Actors: **pipeline runner**, **dry-run validator**, **commit boundary** consumer from Phase **2** primary vocabulary.

**Merge seam story (execution):**

1. Stage **2** emits a **typed staged delta bundle** (`TypedStageDeltaBundle`) with optional per-stage fragments.
2. Stage **4** emits **validation artifact** + **ValidationDecisionLabels** + **`commit_allowed`** (boolean/enum).
3. **Merge seam** combines: (a) staged deltas, (b) labels, (c) intent-merge policy inputs—**no silent winner**; collisions surface as structured merge inputs (consistent with tertiary **2.1.1**).
4. Stage **5** emits **CommitBoundaryToken** only when **`commit_allowed`** is true **and** merge seam reports **no blocking validation label** (execution-level predicate names only).

**Regeneration:** Re-run with identical **seed bundle identity** + **intent hook set**; label and merge outputs must replay deterministically from typed inputs (per **1.2.4** replay contracts).

## Interfaces (text — depth-3 tertiary)

Natural-language shapes (not APIs):

- **`ValidationDecisionLabels`:** finite set of typed labels explaining allow/deny (machine- and operator-facing).
- **`MergeSeamInput`:** `{ staged_delta_bundle, validation_labels, intent_merge_inputs }`
- **`BoundaryHookSet`:** `{ validation_labels, commit_allowed, commit_token_if_allowed }`

Per-stage carry (execution sketch):

- Stage **4** → produces **`ValidationArtifact` + `ValidationDecisionLabels` + `commit_allowed`**.
- Merge seam → **`MergedStagedPayload`** (or explicit **blocked** with empty downstream deltas).
- Stage **5** → **`CommitBoundaryToken`** iff merge seam + Stage **4** allow.

## Edge cases (execution)

- **Partial validation failure:** If **`commit_allowed`** is false, downstream treats **staged deltas as non-authoritative** for mutation; labels remain available for tooling (matches conceptual “no partial commit”).
- **Label vs delta mismatch:** Merge seam must **fail closed** (block commit) if staged bundle hash disagrees with validation artifact inputs—surface as typed merge error inputs, not narrative drift.
- **Intent collisions:** Resolved only via explicit merge policy inputs (tertiary **2.1.1** alignment).

## Pseudocode readiness (text — no verbatim C++)

```text
seam boundary_hook_merge(staged_deltas, validation_artifact, labels, intent_merge_inputs, mode):
  if not validation_artifact.commit_allowed:
    return blocked(empty_delta=true, labels=labels)
  merged = merge_seam(staged_deltas, labels, intent_merge_inputs)
  if merged.blocked:
    return blocked(empty_delta=true, labels=labels)
  if mode == dry_run:
    return preview_only(merged)
  token = commit_boundary(merged, validation_artifact)
  return commit_ready(token=token, merged=merged, labels=labels)
```

Verbatim C++ / standard quotes → later slice with **Task(research)** + allowlisted citations per **sandbox_code_precision**.

## Acceptance criteria (execution-first)

| ID | Criterion | Evidence target | Status |
| --- | --- | --- | --- |
| AC-2.1.2.E1 | Validation labels are stable function of Stage **4** typed artifact | `label_digest_from_validation_artifact` | Scaffolded (inline) — receipt: [[../../../workflow_state-execution]] log row **2026-04-11 21:05** (`queue_entry_id: followup-deepen-exec-phase2-secondary21-sandbox-20260412T151500Z`) |
| AC-2.1.2.E2 | Merge seam blocks commit when labels + deltas disagree | `merge_seam_block_trace` | Planned |
| AC-2.1.2.E3 | Commit token only when `commit_allowed` **and** merge seam clears | `token_iff_allow_and_merge_ok` | Planned |
| AC-2.1.2.E4 | Replay: same inputs → same labels + merge outcome | `replay_label_merge_digest` | Planned |

## Intent Mapping

| Design intent target | Inspiration anchors | Execution mechanism | Validation signal |
| --- | --- | --- | --- |
| Label-bearing boundary | Conceptual **2.1.2** Stage **4→5** hook NL | `boundary_hook_merge` + label seam | AC-2.1.2.E1 |
| Staged delta merge seams | Conceptual merge + **1.2** skip semantics | `merge_seam` inputs | AC-2.1.2.E2–E3 |
| Safe commit | Phase **2** primary dry-run / commit tables | token path after merge | AC-2.1.2.E3–E4 |

## Lane comparand

| Concern | Sandbox (this lane) | Godot (reference) | Shared contract |
| --- | --- | --- | --- |
| Validation labels | Typed consumer-facing reasons | Editor diagnostics | Deterministic replay |
| Merge seam | Policy-driven delta merge | Resource staging merges | No silent winner |

## Related

- Parent secondary **2.1:** [[Phase-2-1-Pipeline-Stages-Seed-to-World-Roadmap-2026-04-11-2359]]
- Prior tertiary **2.1.1:** [[Phase-2-1-1-Stage-Family-Bodies-and-Boundary-Hooks-Roadmap-2026-04-12-1825]]
- Conceptual authority: [[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-2-Stage-Family-Bodies-and-Boundary-Hooks-Roadmap-2026-03-30-1015]]
- Next structural target (execution cursor): tertiary **2.1.3** — [[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-3-Staged-Delta-Bundles-Merge-Seams-and-Apply-Ordering-Roadmap-2026-03-30-1041]] (conceptual peer for spine ordering).
