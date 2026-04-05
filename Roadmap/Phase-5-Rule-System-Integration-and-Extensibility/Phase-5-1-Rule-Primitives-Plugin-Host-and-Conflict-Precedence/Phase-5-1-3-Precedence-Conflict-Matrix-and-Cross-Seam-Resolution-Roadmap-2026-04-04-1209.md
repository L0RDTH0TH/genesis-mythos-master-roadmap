---
title: Phase 5.1.3 - Precedence Conflict Matrix and Cross-Seam Resolution
roadmap-level: tertiary
phase-number: 5
subphase-index: "5.1.3"
project-id: godot-genesis-mythos-master
status: in-progress
priority: high
progress: 90
handoff_readiness: 86
created: 2026-04-04
tags:
  - roadmap
  - godot-genesis-mythos-master
  - phase-5
para-type: Project
links:
  - "[[Phase-5-1-2-Kernel-Evaluation-Schedule-and-Rule-Ordering-Roadmap-2026-04-04-0715]]"
  - "[[Phase-5-1-1-Ruleset-Manifest-Seam-Admission-and-Deterministic-Evaluation-Order-Roadmap-2026-04-04-0010]]"
  - "[[Phase-5-1-Rule-Primitives-Plugin-Host-and-Conflict-Precedence-Roadmap-2026-04-03-2330]]"
  - "[[Phase-3-4-1-Handoff-Seam-Catalog-and-Consumer-Contract-Rows-Roadmap-2026-04-03-0115]]"
  - "[[Phase-4-1-3-Consumer-Surface-Framing-and-Presentation-Time-Validation-Roadmap-2026-04-03-2110]]"
  - "[[Phase-5-Rule-System-Integration-and-Extensibility-Roadmap-2026-03-30-0430]]"
  - "[[Conceptual-Decision-Records/deepen-phase-5-1-3-precedence-conflict-matrix-cross-seam-2026-04-04-1209]]"
  - "[[decisions-log]]"
---

> [!note] #handoff-review
> `handoff_readiness: 86` — Tertiary **5.1.3** owns the **precedence conflict matrix**: explicit rows for **cross-seam** and **same-seam** conflict classes, deterministic winner policies, and operator-visible explanation handles after **5.1.2** schedule passes. **Tertiary chain 5.1.1–5.1.3** is structurally complete; next structural work is **secondary 5.1 rollup** (NL + **GWT-5.1** vs **5.1.1–5.1.3**).

## Scope

In scope:
- **ConflictMatrix** NL contract: a versioned table (or ordered row set) keyed by **(seam_id_a, seam_id_b, conflict_class)** when **seam_id_a ≠ seam_id_b** (cross-seam), and by **(seam_id, conflict_class)** for same-seam groups already partially covered in **5.1.2** — **5.1.3** unifies both so replay has one matrix authority.
- **Winner policy cells**: each row declares **precedence_class** ordering relative to **5.1.2** passes, **tie_break_reference** (tuple vs manifest ordinal vs host policy pin), and **explanation_handle** (name stable for **4.1.3** projection).
- **Seam vocabulary binding**: **seam_id** values must be **3.4.1** **SeamId** keys or explicitly declared aliases with deterministic normalization rules (no silent remapping).
- **Replay stability**: same frame + same matrix revision + same eligible candidates → same resolved winner per conflict group.

Out of scope:
- Serialized matrix interchange format, signing, marketplace distribution — execution-deferred.
- WASM / hot-reload of matrix rows mid-frame — execution-deferred.

## Behavior (natural language)

1. **Matrix revision:** Each ruleset pin carries an optional **conflict_matrix_revision** (monotonic integer or lexicographic id) used in audit traces alongside **5.1.1** manifest revision.
2. **Lookup order:** For a detected conflict group, kernel resolves **(seam_id, conflict_class)** first; if candidates span two seams, lookup **(seam_id_low, seam_id_high, conflict_class)** with deterministic seam ordering (lexicographic on **SeamId**).
3. **Cell application:** Winning policy from the matrix is applied **after** **5.1.2** tuple sort and **precedence_class** pass order — matrix may elevate a **cross-seam** rule over a local seam candidate only when the row explicitly declares **cross_seam_priority** (illustrative field name) at NL; otherwise **5.1.2** in-seam winner stands.
4. **Default row:** If no matrix row matches, fall back to **5.1** secondary digest + **5.1.2** deterministic panic-class vocabulary (named, not silent).
5. **Operator legibility:** Each applied row emits **explanation_handle** + **matrix_row_id** suitable for **4.1.3** presentation-time validation (execution payload deferred).

## Interfaces

Upstream:
- [[Phase-5-1-2-Kernel-Evaluation-Schedule-and-Rule-Ordering-Roadmap-2026-04-04-0715]] — EvaluationFrame, tuple sort, precedence passes.
- [[Phase-5-1-1-Ruleset-Manifest-Seam-Admission-and-Deterministic-Evaluation-Order-Roadmap-2026-04-04-0010]] — manifest fields that admit matrix revision and seam ids.
- [[Phase-3-4-1-Handoff-Seam-Catalog-and-Consumer-Contract-Rows-Roadmap-2026-04-03-0115]] — **SeamId** authority.

Downstream:
- **Secondary 5.1 rollup** — NL checklist + **GWT-5.1** parity vs **5.1.1–5.1.3**.

Outward guarantees:
- **Single matrix authority** per admitted manifest revision for cross-seam and same-seam conflict resolution at conceptual NL.
- **No duplicate winners** for the same **(frame_id, conflict_group_id)** after matrix application.

## Edge cases

- **Symmetric cross-seam rows:** **(A,B)** and **(B,A)** must normalize to one canonical key — use ordered pair **(min(A,B), max(A,B))**.
- **Matrix row conflicts with manifest precedence_ordinal:** manifest wins for **same-seam** groups unless matrix row declares **override_manifest_ordinal: true** (illustrative) — document as open decision **D-5.1.3-matrix-vs-manifest** in [[decisions-log]] when ambiguous.
- **Partial matrix coverage:** undeclared **conflict_class** for a seam pair → deterministic **deny_evaluate** or **defer_rule_class** (host policy enum at NL — execution strings deferred).

## Open questions

- Whether **cross_seam_priority** rows are ruleset-local only or may be overridden by campaign **policy_pin** — execution-deferred.

## Pseudo-code readiness (algorithm sketches)

```text
function resolveWithMatrix(frame, group, matrixRevision):
  key = canonicalConflictKey(group.seams, group.conflict_class)
  row = matrixLookup(matrixRevision, key)
  if row == null:
    return fallback5_1_2(group)  # 5.1.2 winner + named panic class if tie
  winner = applyPolicy(row, group.candidatesOrdered)  # after 5.1.2 ordering
  return Outcome(winner, explanation_handle=row.explanation_handle, matrix_row_id=row.id)
```

## Deliverable tables (matrix scaffold)

| matrix_row_id | seam_id_a | seam_id_b | conflict_class | precedence_class | cross_seam | explanation_handle |
| --- | --- | --- | --- | --- | --- | --- |
| M-5.1.3-01 | (same) | (same) | `rule_outcome_collision` | `host_core` | false | `explain.same_seam.core` |
| M-5.1.3-02 | `SeamId:observation` | `SeamId:rules` | `cross_surface_hint` | `manifest_declared` | true | `explain.cross.obs_rules` |
| M-5.1.3-03 | `SeamId:session` | `SeamId:persistence` | `checkpoint_interlock` | `host_core` | true | `explain.cross.session_persist` |
| M-5.1.3-04 | (wildcard) | (wildcard) | `unclassified_cross` | `defer_host_policy` | true | `explain.cross.defer` |

> Rows are **scaffold** — expand in execution track; conceptual authority is the **shape** and **deterministic lookup** contract.

## Tertiary slice GWT (GWT-5.1.3-A–K) — narrowed vs GWT-5.1.2-A–K

| ID | Given | When | Then | Evidence (narrowed here) |
| --- | --- | --- | --- | --- |
| GWT-5.1.3-A | **5.1.2** schedule complete | Cross-seam conflict detected | Canonical matrix key resolves | § Behavior |
| GWT-5.1.3-B | **3.4.1** **SeamId** | Matrix lookup | No seam id outside catalog unless declared alias | § Interfaces |
| GWT-5.1.3-C | Matrix row present | Apply policy | Single winner per **(frame_id, conflict_group_id)** | § Behavior |
| GWT-5.1.3-D | **GWT-5.1.2-C** same-seam winner | Row silent for pair | **5.1.2** winner retained | § Behavior |
| GWT-5.1.3-E | **4.1.3** envelope | Outcome emitted | **explanation_handle** + **matrix_row_id** legible | § Behavior |
| GWT-5.1.3-F | **GWT-5.1.2-E** defer | Frame deferred | Matrix does not emit authoritative cross-seam winner | **5.1.2** |
| GWT-5.1.3-G | Symmetric seam pair **(A,B)** | Lookup | Same result as **(B,A)** | § Edge cases |
| GWT-5.1.3-H | Missing row | Unknown class | Named fallback / defer class — no silent pick | § Edge cases |
| GWT-5.1.3-I | **GWT-5.1.2-I** observation authority | Cross-seam read | **3.2.1** **authority_class** still respected | Phase 3 |
| GWT-5.1.3-J | Matrix revision bump | New pin | Audit trace shows revision + row set delta | § Behavior |
| GWT-5.1.3-K | Conceptual waiver | Validator advisory | Registry / CI / HR closure execution-deferred | [[roadmap-state]] / [[distilled-core]] |

## Related

- CDR: [[Conceptual-Decision-Records/deepen-phase-5-1-3-precedence-conflict-matrix-cross-seam-2026-04-04-1209]]
