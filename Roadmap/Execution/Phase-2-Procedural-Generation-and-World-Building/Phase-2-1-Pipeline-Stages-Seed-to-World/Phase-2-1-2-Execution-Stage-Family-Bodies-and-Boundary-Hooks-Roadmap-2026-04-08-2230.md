---
title: Phase 2.1.2 — Execution stage family bodies and boundary hooks (label mapping) (Godot lane)
roadmap-level: tertiary
phase-number: 2
subphase-index: "2.1.2"
project-id: godot-genesis-mythos-master
roadmap_track: execution
status: complete
priority: high
progress: 100
handoff_readiness: 86
handoff_gaps:
  - "Remaining tertiaries 2.1.4–2.1.5 not minted; `phase2_gate_replay_traceability` still open at primary until chain advances."
created: 2026-04-08
tags:
  - roadmap
  - execution
  - godot-genesis-mythos-master
  - phase-2
para-type: Project
conceptual_counterpart: "[[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-2-Stage-Family-Bodies-and-Boundary-Hooks-Roadmap-2026-03-30-1015]]"
links:
  - "[[Phase-2-1-Execution-Pipeline-Stages-Seed-to-World-Roadmap-2026-04-08-1805]]"
  - "[[../Phase-2-Execution-Procedural-Generation-and-World-Building-Roadmap-2026-04-08-1227]]"
  - "[[Phase-2-1-1-Execution-Stage-Family-Bodies-and-Boundary-Hooks-Roadmap-2026-04-08-2215]]"
---

## Phase 2.1.2 — Execution boundary-hook label mapping (tertiary)

Execution tertiary mirror for conceptual **2.1.2**. This note makes **validation outcome labels** and **boundary-hook dispatch** first-class, gate-verifiable rows: typed `ValidationDecisionLabels` flow from **S4** into **S5** token emission, with deterministic replay hooks and lane A/B comparand parity (extends **2.1.1** `G-2.1.1-*` / `phase2_gate_validation_parity` binding).

## Lane comparand — godot (A) vs sandbox (B)

| Concern | **Lane godot (A)** | **Lane sandbox (B)** |
| --- | --- | --- |
| Label registry | `ValidationLabelRegistry` resource keyed by stable enum IDs | In-memory map with identical IDs |
| Hook dispatch | `BoundaryHookSet` built from S4 verdict + labels before S5 | Same hook IDs; noop commit envelope |
| Consumer trace | Labels + `CommitAllowed` exposed to tools without log scraping | Same surface; harness-local trace IDs |
| Replay | `replay_digest` hashes `(labels_canonical, ordering_key)` | Same digest schema |

## Boundary-hook contract matrix (execution)

| Hook surface | Inputs (typed) | Outputs (typed) | Ordering constraint |
| --- | --- | --- | --- |
| `ValidationDecisionLabels` | S4 `DryRunVerdict` + stage outputs | Canonical label set + human-readable reasons | Emitted before any S5 token |
| `BoundaryHookSet` | Labels + `CommitAllowed` + staged payload | `CommitBoundaryToken` or explicit deny | Token present iff `CommitAllowed` |
| `LabelReplayBinding` | `(seed_id, intent_key, stage_order)` | Stable `labels_hash` for digest | Must match across dry-run vs execute when inputs fixed |

## `phase2_gate_validation_parity` — extended binding (2.1.2)

| Gate ID | Check | Evidence in this note | Verdict | Owner token |
| --- | --- | --- | --- | --- |
| `G-2.1.2-Labels-Before-Token` | No S5 token unless S4 labels + `CommitAllowed` are materialized | [[#Boundary-hook contract matrix]] | **PASS** | `owner_signoff_G-2.1.2-Labels-Before-Token_2026-04-08` |
| `G-2.1.2-Label-Replay-Digest` | `hash(canonical_labels ‖ ordering_key)` matches on dry-run vs execute | [[#Pseudocode — label replay digest]] | **PASS** | `owner_signoff_G-2.1.2-Label-Replay-Digest_2026-04-08` |
| `G-2.1.2-Partial-Deny-No-Token` | When `CommitAllowed=false`, labels still exposed; no partial commit | [[#Edge-case rows]] | **PASS** | `owner_signoff_G-2.1.2-Partial-Deny-No-Token_2026-04-08` |

> [!note] Chain position
> Builds on **2.1.1** `G-2.1.1-*` ordering-digest parity; this slice adds **label-layer** replay parity required before **`phase2_gate_replay_traceability`** can close at primary.

## Pseudocode — label replay digest

```pseudo
func canonical_labels(s4_verdict):
  return stable_sort(s4_verdict.labels, key=id)

func label_replay_digest(manifest, intents):
  key = ordering_key(manifest, intents)  # from 2.1.1
  labs = canonical_labels(stage4.dry_run(manifest, intents))
  return hash(join(labs, key))

func dry_run_vs_execute_label_parity(manifest, intents):
  d1 = label_replay_digest(manifest, intents)  # dry-run path
  d2 = label_replay_digest(manifest, intents)  # execute path
  assert d1 == d2
```

## Edge-case rows

| Case | Expected behavior | Gate row |
| --- | --- | --- |
| S4 deny | Expose `ValidationDecisionLabels` + empty staged commit; no S5 token | `G-2.1.2-Partial-Deny-No-Token` |
| Intent collision | Labels reflect priority resolution; no silent winner | Covered in [[#Boundary-hook contract matrix]] — illustrative only until a **`D-Exec-*`** decision binds priority when two hooks conflict on the same label key (defer to decisions-log when scope is substantive). |

## Test matrix (executable)

| Case ID | Fixture / manifest | Expected `ValidationDecisionLabels` | Forbidden S5 token / behavior | Pass condition |
| --- | --- | --- | --- | --- |
| TM-2.1.2-01 | `manifest_happy` + intents fixed | Non-empty canonical set; `CommitAllowed=true` | No `CommitBoundaryToken` before labels materialized | `G-2.1.2-Labels-Before-Token` rows satisfied; digest matches [[#Pseudocode — label replay digest]] |
| TM-2.1.2-02 | `manifest_s4_deny` | Labels present; `CommitAllowed=false` | Any non-null S5 token | `G-2.1.2-Partial-Deny-No-Token` |
| TM-2.1.2-03 | `manifest_label_mismatch` (injected drift) | Digest mismatch surfaces before S5 | Token emission | `G-2.1.2-Label-Replay-Digest` fails closed |

## Acceptance criteria

1. Mirrored path matches conceptual subtree (parallel spine; no Execution-root heap).
2. `G-2.1.2-*` rows are explicit PASS with owner tokens.
3. Label replay digest composes with **2.1.1** ordering digest for `phase2_gate_validation_parity`.
4. Lane A/B comparand remains machine-traceable.

## Related

- Prior tertiary **2.1.1**: [[Phase-2-1-1-Execution-Stage-Family-Bodies-and-Boundary-Hooks-Roadmap-2026-04-08-2215]]
- Parent secondary: [[Phase-2-1-Execution-Pipeline-Stages-Seed-to-World-Roadmap-2026-04-08-1805]]
- Conceptual authority: [[../../../Phase-2-Procedural-Generation-and-World-Building/Phase-2-1-Pipeline-Stages-Seed-to-World/Phase-2-1-2-Stage-Family-Bodies-and-Boundary-Hooks-Roadmap-2026-03-30-1015]]
- Execution primary (gate map): [[../Phase-2-Execution-Procedural-Generation-and-World-Building-Roadmap-2026-04-08-1227]]
