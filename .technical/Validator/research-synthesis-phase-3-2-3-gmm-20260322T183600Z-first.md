---
title: Validator report — research_synthesis (Phase 3.2.3) — genesis-mythos-master
created: 2026-03-22
tags: [validator, research_synthesis, genesis-mythos-master, phase-3-2-3]
validation_type: research_synthesis
project_id: genesis-mythos-master
synth_note_paths:
  - Ingest/Agent-Research/phase-3-2-3-replay-regen-ledger-tickcommit-serialization-research-2026-03-22-1830.md
compare_to_report_path: null
severity: medium
recommended_action: needs_work
reason_codes:
  - missing_task_decomposition
  - safety_unknown_gap
primary_code: missing_task_decomposition
ready_for_handoff: maybe
potential_sycophancy_check: true
---

## Summary

The note is **readable narrative scaffolding** for Phase 3.2.3, not consumable **spec** for deepen-to-code. It **name-drops** vault anchors and repeats **regen-before-merge** correctly, but it **punts** the hardest preimage/serialization decisions into a **future checklist**, leaves **multi-regen ordering** at “e.g. StableMergeKey-style” without a pinned key, and leans on **Stack Overflow + Medium + generic blogs** for “industry” idempotency — the same failure mode as prior `research_synthesis` passes on this project. **Verdict:** allow roadmap to **proceed** with this as **input**, but **do not** treat it as definition-of-done for 3.2.3; **`needs_work`**.

## Structured verdict (machine-facing)

```json
{
  "validation_type": "research_synthesis",
  "project_id": "genesis-mythos-master",
  "severity": "medium",
  "recommended_action": "needs_work",
  "primary_code": "missing_task_decomposition",
  "reason_codes": ["missing_task_decomposition", "safety_unknown_gap"],
  "ready_for_handoff": "maybe",
  "potential_sycophancy_check": true,
  "gap_citations": [
    {
      "reason_code": "missing_task_decomposition",
      "quote": "**Checklist for 3.2.3 deliverables:** Document **which preimage fields** in `TickCommitRecord_v0` include `regen_apply_sequence_digest` vs **only** post-regen intent stream digest.",
      "artifact": "Ingest/Agent-Research/phase-3-2-3-replay-regen-ledger-tickcommit-serialization-research-2026-03-22-1830.md §4"
    },
    {
      "reason_code": "missing_task_decomposition",
      "quote": "| `regen_subgraph_outcome_row` (optional split) | Per-request **structured result** for goldens: e.g. `subgraph_hash_out`, `denial_reason_code`, `manifest_pre_delta_ref` — whatever the harness needs to diff **without** re-running ML or external IO. |",
      "artifact": "Ingest/Agent-Research/phase-3-2-3-replay-regen-ledger-tickcommit-serialization-research-2026-03-22-1830.md §1 table"
    },
    {
      "reason_code": "safety_unknown_gap",
      "quote": "if multiple: stable sort by a published key, e.g. `StableMergeKey`-style tuple **scoped to regen lane** to avoid collision with player/DM keys).",
      "artifact": "Ingest/Agent-Research/phase-3-2-3-replay-regen-ledger-tickcommit-serialization-research-2026-03-22-1830.md §3 step 2"
    },
    {
      "reason_code": "safety_unknown_gap",
      "quote": "[Source: Medium — idempotency in CQRS/ES projections](https://medium.com/@arsalan.valoojerdi/idempotency-in-cqrs-es-projections-strategies-and-implementation-techniques-e21a7cd06575)",
      "artifact": "Ingest/Agent-Research/phase-3-2-3-replay-regen-ledger-tickcommit-serialization-research-2026-03-22-1830.md §2"
    }
  ]
}
```

## Strengths (limited)

- **Regen-before-merge** is stated in plain policy language and aligned with cited vault phases (3.2.1 / 3.2.2).
- **D-027** is repeatedly fenced as **illustrative**; that is correct discipline for this stack.
- **Phase separator** argument (regen vs intent streams) is the right *class* of hazard for lockstep/replay.
- **Idempotency story** at `regen_request_id` + `regen_gate_version_id` matches the 3.2.2 spirit the note claims.

## Hostile concerns

1. **No actual TickCommitRecord contract:** The note never lists **field-level** preimage members, canonical byte rules, or one **worked example** row. A tertiary phase that is supposed to **close serialization** cannot ship with “v0 sketch” tables only.
2. **Deferred deliverables masquerading as synthesis:** §4 explicitly **assigns** the critical preimage decision to “deliverables” — that means **this research output did not complete the job** it was framed to support.
3. **Unspecified total order for multi-regen:** “e.g. StableMergeKey-style” is **not** a published key; replay divergence is exactly what you are trying to prevent. Without a **named tuple definition** or “single regen per tick” invariant, this is **floating scope**.
4. **Optional row split is a foot-gun:** “optional split” without **decision criteria** invites two implementers to pick incompatible golden layouts.
5. **Weak / noisy citations for normative claims:** Medium + Stack Overflow are **not** acceptable primary backing for **fail-closed** ledger semantics; they are reading-list fluff at best.
6. **Cross-tick / crash boundary absent:** Idempotency is discussed as **duplicate command** handling but not **where the ledger persists relative to tick commit**, **partial failure**, or **replay of a truncated tail** — standard ES/CQRS hard parts are **missing**.

## next_artifacts (definition of done)

- [ ] **Preimage table:** One subsection that **maps** each proposed digest (`regen_apply_sequence`, optional `regen_subgraph_outcome_row`, intent-stream digest) to **named** `TickCommitRecord_v0` fields (or explicitly “out of band in ledger tail ref X”) — no “document later” hand-off.
- [ ] **Single concrete example:** One **toy** tick with **two** `RegenRequest_v0` instances showing **ordered** `regen_apply_sequence` elements, then merged intents — JSON or pseudocode **with hashes**, even if illustrative.
- [ ] **Pin the multi-regen sort key:** Either define the **exact** tuple (fields + endianness / canonicalization profile) or state a **hard invariant** (“at most one accepted regen per tick”) with **failure mode** when violated.
- [ ] **Decide optional split:** Rule for when `regen_subgraph_outcome_row` is **required** vs folded into `regen_apply_sequence` — test-golden viewpoint.
- [ ] **Replace or demote weak web sources:** Keep Fowler / vendor docs if needed; **drop or quarantine** Medium/SO unless paired with **primary** spec or your own vault norm.
- [ ] **Persistence / replay edge:** Short paragraph on **ledger durability vs tick commit** and how replay reproduces **ledger-hit** without double-apply across **crash** boundaries.

## potential_sycophancy_check

**true** — The note is **organized**, cites **known-good** vault links, and repeats **correct high-level ordering**; it is tempting to call that “good enough for pre-deepen” and **downgrade** to `log_only` or empty `reason_codes`. **Rejected:** the **checklist deferral**, **unpinned sort key**, and **blog-grade** citations are **exactly** the class of gaps that produce **silent replay fork** in production. I did **not** soften those.

## Return metadata

**Status:** **Success** (validator run completed; report written at hand-off path; verdict **needs_work**, not “pipeline green”).
