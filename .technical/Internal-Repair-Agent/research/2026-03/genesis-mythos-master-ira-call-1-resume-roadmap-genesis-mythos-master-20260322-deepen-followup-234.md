---
created: 2026-03-22
pipeline: research
project_id: genesis-mythos-master
queue_entry_id: resume-roadmap-genesis-mythos-master-20260322-deepen-followup-234
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 2
  medium: 3
  high: 0
validator_report_path: .technical/Validator/research-synthesis-phase-3-1-1-20260321T220000Z.md
synth_note_path: Ingest/Agent-Research/simulation-tick-scheduling-time-quanta-commit-barrier-research-2026-03-21.md
---

## Context

Post–first-pass **research_synthesis** validator (`severity: medium`, `recommended_action: needs_work`, `primary_code: safety_unknown_gap`) on the Phase **3.1.1** synthesis note. Invocation is **validator-driven** with `ira_after_first_pass: true`. Per contaminated-report handling, treat the validator’s list as a **floor**: evidence breadth, replay architecture, and traceability gaps are likely **worse** than stated if the second pass is lenient. Repair targets are **limited** to `Ingest/Agent-Research/**` (and machine telemetry); **no** edits to roadmap phase notes or PMG.

## Structural discrepancies

1. **Claim vs evidence:** Opening frames “industry patterns” and broad replay alignment while the bibliography is **two Gaffer on Games articles**—a **safety_unknown_gap** (overstated external generality).
2. **Vault traceability:** The synthesis **asserts** Phase 2.1.3 **`shard_sequence` / lattice traversal** without an **inline quoted anchor**; readers cannot verify from this file alone (validator gap citation).
3. **research_query coverage debt:** Query names **replay loops** and **tick preimage**; the note sketches preimage and fixed-`dt` replay but omits a minimal **record format / desync / restart** story (validator `next_artifacts` item 3)—under-reported if treated as “complete” for deepen.
4. **Determinism policy:** Validator mentions but softens **second-source** determinism (fixed-point, compiler/SIMD); synthesis should either **cite** or **explicitly defer** as project-local policy to avoid silent unknowns.

## Proposed fixes (for ResearchSubagent to apply)

Apply in **low → medium** order when gates allow. All content edits target:

`Ingest/Agent-Research/simulation-tick-scheduling-time-quanta-commit-barrier-research-2026-03-21.md`

| # | risk | action_type | description |
|---|------|-------------|-------------|
| 1 | low | `adjust_frontmatter` | Add explicit synthesis stance fields, e.g. `research_synthesis_scope: seed` and `external_evidence_basis: gaffer-two-source` (or equivalent), plus `validator_followup_codes: [safety_unknown_gap]` so downstream deepen treats the note as **seed / scoped**, not full industry due diligence. |
| 2 | low | `append_verbatim_quote` | Immediately after the paragraph that cites Phase 2.1.3 ordering (currently ~line 34), insert a **blockquote** of the canonical Phase 2.1.3 bullet: *“**Ordering:** coordinator assigns **deterministic `shard_sequence`** from lattice traversal (e.g. `CellCoord` batches), never from scheduler timing.”* Attribute with wikilink to `[[phase-2-1-3-deterministic-async-commit-barrier-and-stage-ledger-reconciliation-roadmap-2026-03-19-2000|Phase 2.1.3 roadmap note]]` under **### Async without nondeterminism**. |
| 3 | medium | `rewrite_section` | **Either** add **≥2 independent non-Gaffer** sources (engine tick docs, netcode/determinism postmortem, ECS/sim scheduling reference, or formal spec) with short in-text citations and **Sources** list entries, **or** rewrite the **opening paragraph** to remove “industry patterns” language and state clearly: **Gaffer-centric baseline + vault bridge**; no broad industry claim without receipts. |
| 4 | medium | `append_section` | Add **## Replay and record format** (or **###** under section 1): minimum one paragraph on **what is logged per tick index**, how it ties to **commit-barrier / ledger visibility**, and **hash mismatch → fail-closed diagnostic / restart policy**—each sentence either **sourced** or tagged as **project-local policy (TBD)**. |
| 5 | medium | `append_section` | Add a short **Determinism and build policy** bullet block: fixed-point vs float, cross-architecture caveats, optional **explicit “unknown / TBD”** where no second source exists—closes residual `safety_unknown_gap` beyond the validator’s two snippets. |

## Notes for future tuning

- **Research synth template:** Consider a required **Evidence breadth** frontmatter key (`single_author` / `multi_source`) auto-set by research-agent-run when external URL count by domain is below threshold.
- **Validator→IRA:** For `research_synthesis`, empty `suggested_fixes` is rare when `needs_work`; default `ira_after_first_pass` still produces actionable content fixes in Agent-Research without touching roadmap files.
