---
title: Validator report — research_synthesis (second pass, regression guard) — genesis-mythos-master Phase-3-1-6
created: 2026-03-22
tags: [validator, research_synthesis, genesis-mythos-master, Phase-3-1-6, second-pass, regression-guard]
validation_type: research_synthesis
project_id: genesis-mythos-master
linked_phase: Phase-3-1-6
synth_note_paths:
  - Ingest/Agent-Research/tick-scoped-observable-bundle-after-mutation-apply-research-2026-03-22-2330.md
compare_to_report_path: .technical/Validator/research-synthesis-gmm-316-20260322T233100Z-first.md
severity: medium
recommended_action: needs_work
reason_codes:
  - safety_unknown_gap
primary_code: safety_unknown_gap
ready_for_handoff: maybe
potential_sycophancy_check: true
regression_vs_first_pass: no_softening
---

## Summary

The **current** synthesis note is **materially stronger** than the artifact the **first** validator pass quoted: zero-intent / pause semantics are **no longer** stranded in a “pending decisions” ghetto, telemetry has a **named** `SimObservableBundleTelemetry_v0` table, facet manifest has a **concrete** vault path proposal, and weak web anchors are **explicitly** fenced as **non-normative**. That is **real repair**, not lipstick. It is **still not** a closed, CI-falsifiable contract: the **golden hash is explicitly TODO**, the manifest registry **still** says “pick **one** location,” and **no** primary-spec evidence replaced the blog/Q&A/Gaffer chain. **Regression guard:** `severity`, `recommended_action`, and **`safety_unknown_gap`** stay **unchanged** from the first pass — rewarding this as “done” would be **dulling**.

## Regression guard (vs first report)

| First-pass failure mode | Status in current synthesis | Verdict |
|-------------------------|----------------------------|---------|
| §7 “pending” zero-intent / observable emission | Replaced by **§7** normative defaults (paused no advance; empty ledger carry-forward re-hash; `partial_tick_ledger`) | **Addressed** (new text; first-pass quotes are **obsolete**) |
| §4 “illustrative” telemetry names | Replaced by **§4b** `SimObservableBundleTelemetry_v0` table labeled **normative draft, research** | **Partially addressed** — still **research** tier, not repo-owned RFC |
| Facet manifest “D-027 until stack pinned” only | **§8** proposes `facet-manifest-v0.md` or decisions-log heading | **Partially addressed** — **dual** home still allowed |
| No byte-level / golden vector | **Appendix A** ordered preimage + toy entities | **Partially addressed** — **Expected hash** still **TODO** |
| Weak web sourcing for strong claims | §1/§2 mark EventSourcingDB + Stack Overflow as **non-normative**; Gaffer “illustrative” | **Partially addressed** — **demoted**, not **replaced** with primary sources |
| Grammar (“a explicit”) | Now “**an** explicit” | **Fixed** |

**No softening of validator strictness:** First pass = `medium` + `needs_work` + `safety_unknown_gap`. This pass **matches** that tuple. Omitting `safety_unknown_gap` because “IRA did a lot” would violate the regression contract.

## Structured verdict (machine-facing)

```json
{
  "validation_type": "research_synthesis",
  "project_id": "genesis-mythos-master",
  "linked_phase": "Phase-3-1-6",
  "compare_to_report_path": ".technical/Validator/research-synthesis-gmm-316-20260322T233100Z-first.md",
  "severity": "medium",
  "recommended_action": "needs_work",
  "primary_code": "safety_unknown_gap",
  "reason_codes": ["safety_unknown_gap"],
  "ready_for_handoff": "maybe",
  "potential_sycophancy_check": true,
  "regression_vs_first_pass": "no_softening",
  "first_pass_reason_codes_addressed": {
    "safety_unknown_gap": "partial"
  },
  "gap_citations": [
    {
      "reason_code": "safety_unknown_gap",
      "quote": "**Expected hash:** `TODO: fill after serialization_profile_id frozen in repo` — replace with **literal** `committed_sim_observable_hash` from the reference harness once **float-free** numeric encoding is pinned under **D-027**.",
      "artifact": "Ingest/Agent-Research/tick-scoped-observable-bundle-after-mutation-apply-research-2026-03-22-2330.md (Appendix A)"
    },
    {
      "reason_code": "safety_unknown_gap",
      "quote": "`1-Projects/genesis-mythos-master/Roadmap/facet-manifest-v0.md` (or a named section in [[decisions-log|decisions-log]] with stable heading **`### Facet manifest registry v0`** — pick **one** location per project and link it from phase **3.1.6** when that note exists).",
      "artifact": "Ingest/Agent-Research/tick-scoped-observable-bundle-after-mutation-apply-research-2026-03-22-2330.md (§8)"
    },
    {
      "reason_code": "safety_unknown_gap",
      "quote": "## 4b. `SimObservableBundleTelemetry_v0` (normative draft, research)",
      "artifact": "Ingest/Agent-Research/tick-scoped-observable-bundle-after-mutation-apply-research-2026-03-22-2330.md (§4b heading)"
    },
    {
      "reason_code": "safety_unknown_gap",
      "quote": "[Source: [Stack Overflow — deterministic replay / ordering in CQRS](https://stackoverflow.com/questions/60050722/how-to-replay-in-a-deterministic-way-in-cqrs-event-sourcing) — **non-normative**]",
      "artifact": "Ingest/Agent-Research/tick-scoped-observable-bundle-after-mutation-apply-research-2026-03-22-2330.md (§2)"
    }
  ]
}
```

## Strengths (current note)

- **Replay-critical §7** now **commits** to carry-forward hashing for advanced ticks with empty ledger instead of leaving “duplicate vs skip” open.
- **Barrier / ordering** narrative stays aligned with vault total order; thread-pool staging is correctly subordinated to commit order.
- **Facet model + Merkle** option and RNG single-authority warning remain **on-mission** for D-027-class determinism.
- **Scope fence** (“Do not duplicate” prior slices) still reduces duplicate-truth risk.

## Hostile concerns (residual)

1. **Execution gate is explicit:** `TODO` on the expected hash is an **admission** the byte contract is **not** frozen — first pass demanded falsifiable golden material; **one toy table** without hex **does not** clear the bar.
2. **Registry ambiguity persists:** “Pick **one**” between two vault locations is **still** a fork surface for two teams “following the note.”
3. **“Normative draft, research”** is honest labeling — it also means **downstream CI** must **not** treat §4b as frozen schema until repo + `replay_row_version` coordination lands.
4. **Evidence pedigree:** Demoting blog/Q&A to non-normative is **correct**; it **does not** add **primary** references the first pass asked for as an alternative.

## Verbatim gap citations (required per `reason_code`)

All rows support **`safety_unknown_gap`** (bytes, ownership, and evidence still floating).

| reason_code | Verbatim snippet (from current synthesis note) |
|-------------|-----------------------------------------------|
| `safety_unknown_gap` | "**Expected hash:** `TODO: fill after serialization_profile_id frozen in repo`" |
| `safety_unknown_gap` | "pick **one** location per project and link it from phase **3.1.6**" |
| `safety_unknown_gap` | "`SimObservableBundleTelemetry_v0` (normative draft, research)" |
| `safety_unknown_gap` | "[Stack Overflow — …](https://stackoverflow.com/questions/60050722/… ) — **non-normative**" |

## next_artifacts (definition of done)

- [ ] **Replace `TODO` hash** in Appendix A with a **literal** hex (or state “blocked on harness issue #…”) — empty TODO is not acceptable for “golden trajectory” claims.
- [ ] **Delete the fork:** choose **exactly one** canonical home for `facet_manifest_id` registry; link it from the Phase 3.1.6 roadmap note when that note exists.
- [ ] **Promote or freeze §4b:** either land field names in repo-owned schema docs **or** keep a single banner that §4b is **non-binding** until bump — no mixed audience confusion.
- [ ] **Optional hardening:** add **one** primary reference (spec, paper, or project harness note) **if** any paragraph still reads like **architecture law** rather than **vault contract**.

## potential_sycophancy_check

**true.** The §7 rewrite and §4b table invite calling the note **“basically handoff-ready.”** That would **erase** the still-open **TODO hash**, **dual registry** path, and **research** status of telemetry — all of which keep **`safety_unknown_gap`** **mandatory**. **Rejected.**
