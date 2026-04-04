---
title: Phase 5.1.1 - Ruleset Manifest, Seam Admission, Deterministic Evaluation Order
roadmap-level: tertiary
phase-number: 5
subphase-index: "5.1.1"
project-id: genesis-mythos-master
status: in-progress
priority: high
progress: 90
handoff_readiness: 85
created: 2026-04-04
reminted_to_active_tree: 2026-04-04
tags:
  - roadmap
  - genesis-mythos-master
  - phase-5
para-type: Project
links:
  - "[[Phase-5-1-Rule-Primitives-Plugin-Host-and-Conflict-Precedence-Roadmap-2026-04-03-2330]]"
  - "[[Phase-3-4-1-Handoff-Seam-Catalog-and-Consumer-Contract-Rows-Roadmap-2026-04-03-0115]]"
  - "[[Phase-5-Rule-System-Integration-and-Extensibility-Roadmap-2026-03-30-0430]]"
  - "[[Conceptual-Decision-Records/deepen-phase-5-1-1-manifest-seam-admission-eval-order-2026-04-04-0010]]"
  - "[[Phase-5-1-2-Kernel-Evaluation-Schedule-and-Rule-Ordering-Roadmap-2026-04-04-0715]]"
  - "[[decisions-log]]"
---

> [!note] #handoff-review
> `handoff_readiness: 85` — Tertiary **5.1.1** binds **RulesetManifest** data, **seam admission** against **3.4.1** **SeamId** / consumer rows only (no shadow catalog), and a **deterministic evaluation order** that matches the parent **5.1** **deterministic tie-break digest** tuple **before** **precedence_class** resolves conflicts (**5.1.2+**).

## Scope

In scope:
- Minimum **RulesetManifest** fields the host needs to admit a ruleset pin, validate declared seams, and sort eligible rule instances deterministically within an evaluation frame.
- **Seam admission** rules: every manifest-declared seam must map to an existing **3.4.1** row (forbidden: invent **SeamId** or consumer contract not present upstream).
- **Deterministic evaluation order**: total ordering of eligible **RuleCandidate** rows using the canonical tuple from secondary **5.1** — `(ruleset_pin_id, seam_id, rule_stable_id, trigger_ordinal)` — lexicographic, stable across replay.
- Named **load-time / admission failure classes** (deterministic strings) suitable for **4.1.3** presentation-time readout.

Out of scope:
- Concrete schema IDs, signing, registry transport, sandbox — execution-deferred.
- **Precedence_class** matrix and schedule slots — **5.1.2+**.

## Behavior (natural language)

1. **Admission:** On load, the host parses **RulesetManifest**; rejects with a named failure class if version pin, seam set, or stable rule ids are inconsistent or reference unknown **SeamId** vs **3.4.1**.
2. **Seam binding:** For each declared seam, the host records the **3.4.1** row pointer (catalog + consumer contract) as the sole authority; rules may not widen or reinterpret seam semantics.
3. **Evaluation frame:** For a committed snapshot + ruleset pin + trigger stream slice, the kernel builds the set of **RuleCandidate** rows that are eligible in the frame.
4. **Ordering:** Sort eligible candidates by the tuple `(ruleset_pin_id, seam_id, rule_stable_id, trigger_ordinal)` lexicographically. This order is **the** deterministic evaluation order **before** any conflict-resolution **precedence_class** application (**5.1.2+**).
5. **Failure surfaces:** Admission and load failures produce deterministic `RulesetHostFailureClass` values consumable by operator panels without bypassing Phase **2** commit semantics.

## Interfaces

Upstream:
- [[Phase-3-4-1-Handoff-Seam-Catalog-and-Consumer-Contract-Rows-Roadmap-2026-04-03-0115]] — **SeamId** vocabulary + consumer rows (authority).
- [[Phase-5-1-Rule-Primitives-Plugin-Host-and-Conflict-Precedence-Roadmap-2026-04-03-2330]] — **tie-break digest** tuple + **GWT-5.1-A–K**.

Parent:
- Secondary **5.1** — RuleOutcome schedule intent; this note materializes manifest + ordering hooks.

Downstream:
- [[Phase-5-1-2-Kernel-Evaluation-Schedule-and-Rule-Ordering-Roadmap-2026-04-04-0715]] — kernel evaluation schedule + precedence pass order after tuple sort.
- **5.1.3+** — explicit precedence matrix rows, cross-seam conflict winner + explanation payloads.

Outward guarantees:
- **No duplicate consumer truth:** seam admission is **subset + exact key** of **3.4.1** rows.
- **Replay-stable order:** same inputs → same sorted candidate list before precedence.

## Edge cases

- **Manifest declares seam not in 3.4.1:** deterministic rejection class `SEAM_NOT_IN_CATALOG` (name illustrative; execution strings deferred).
- **Duplicate `rule_stable_id` within one manifest:** rejection or deterministic merge policy at NL — default **reject** with `DUPLICATE_STABLE_ID`.
- **Empty eligible set:** valid — no rule evaluation for that frame; no implicit defaults.

## Open questions

- Whether community-published manifests allow optional **opaque** extension buckets that must be ignored by the kernel until a future catalog revision — **execution-deferred**.

## Pseudo-code readiness (algorithm sketches)

```text
function admitManifest(manifest, seamCatalog341):
  for seam_decl in manifest.declared_seams:
    if seam_decl.seam_id not in seamCatalog341:
      return Fail(SEAM_NOT_IN_CATALOG, seam_decl.seam_id)
  return Ok()

function evaluationOrder(candidates):
  return sort(candidates, key = λ c: (c.ruleset_pin_id, c.seam_id, c.rule_stable_id, c.trigger_ordinal))
```

## Tertiary slice GWT (GWT-5.1.1-A–K) — narrowed vs GWT-5.1-A–K

| ID | Given | When | Then | Evidence (narrowed here) |
| --- | --- | --- | --- | --- |
| GWT-5.1.1-A | **3.4.1** seam catalog | Manifest lists seams | Every **seam_id** resolves to an existing catalog row | § Behavior admission + § Interfaces |
| GWT-5.1.1-B | **RulesetManifest** with **ruleset_pin_id** | Load requested | Pin is validated before any rule graph is active | § Behavior |
| GWT-5.1.1-C | Two manifest rows share **rule_stable_id** | Admission | Deterministic reject (or explicit merge policy) — default reject | § Edge cases |
| GWT-5.1.1-D | Eligible **RuleCandidate** set built | Sort for evaluation | Order matches **5.1** tuple lexicographic order | § Behavior + parent digest |
| GWT-5.1.1-E | **GWT-5.1-F** (collision) | Precedence not yet applied | Tuple order is authoritative **before** **precedence_class** | Secondary tie-break digest |
| GWT-5.1.1-F | **4.1.3** presentation envelope | Admission fails | Failure class is operator-legible | § Behavior |
| GWT-5.1.1-G | **GWT-5.1-H** Phase 2 boundary | Rule proposes world change | Still routes via Phase 2 — manifest does not bypass | Parent + Phase 5 primary |
| GWT-5.1.1-H | **GWT-5.1-I** **D-3.4-*** rows | Rules target seams | Targets reference **3.4.1** rows only | § Scope |
| GWT-5.1.1-I | **ObservationChannel** (**3.2.1**) | Rule inputs classified | Inputs respect authority_class; no new sim truth | Primary Phase 5 + **5.1** |
| GWT-5.1.1-J | **GWT-5.1-J** ecosystem seam | Operator swaps ruleset | New pin goes through same admission + ordering | § Behavior |
| GWT-5.1.1-K | Conceptual waiver | Validator advisory | Execution marketplace/CI gaps remain deferred | [[roadmap-state]] / [[distilled-core]] |

## Related

- CDR: [[Conceptual-Decision-Records/deepen-phase-5-1-1-manifest-seam-admission-eval-order-2026-04-04-0010]]
