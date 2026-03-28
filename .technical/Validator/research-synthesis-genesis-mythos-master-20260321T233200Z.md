---
title: Validator report — research_synthesis (hostile) — genesis-mythos-master
created: 2026-03-21
tags: [validator, research_synthesis, genesis-mythos-master, hostile-review]
validation_type: research_synthesis
project_id: genesis-mythos-master
queue_entry_id: resume-roadmap-genesis-mythos-master-20260321-followup-deepen-next-followup
parent_run_id: eatq-20260321-gmm-l1-2249
synth_note_paths:
  - Ingest/Agent-Research/phase-2-3-3-emg2-alignment-golden-gate-wiring-research-2026-03-21-2315.md
---

# Validator verdict (machine-readable)

```yaml
severity: medium
recommended_action: needs_work
primary_code: safety_unknown_gap
reason_codes:
  - safety_unknown_gap
ready_for_handoff: maybe
potential_sycophancy_check: true
gap_citations:
  - reason_code: safety_unknown_gap
    quote: "## Raw sources (vault)\n\n- Phase 2.2.3 and 2.3.2 roadmap notes (see links above)."
  - reason_code: safety_unknown_gap
    quote: "| `lore_json` | object or path | Authoritative lore slice (or relative `fixture_path` + loader indirection) |"
  - reason_code: safety_unknown_gap
    quote: "## Sources (external)\n\n- [Golden File Testing: Output Comparison | Application Architect](https://www.application-architect.com/posts/golden-file-testing-output-comparison/)\n- [Hypothesis — The Threshold Problem](https://hypothesis.works/articles/threshold-problem/)"
structured_verdict:
  validation_type: research_synthesis
  project_id: genesis-mythos-master
  severity: medium
  recommended_action: needs_work
  reason_codes: [safety_unknown_gap]
  next_artifacts:
    - definition: Replace the boilerplate Raw sources block with at least one verbatim excerpt or bullet-level summary tied to DETERMINISTIC_GATE_V1 / G1–G3 naming from the linked 2.2.3 note, or cite decisions-log ids if registry policy is asserted.
      done_when: Raw sources section quotes or restates normative facts from linked vault notes, not only wikilinks.
    - definition: Resolve the `lore_json` representation (inline JSON vs external file vs indirection) in one normative sentence; pick one default for CI glob loading.
      done_when: Harness pseudo and schema table agree on a single loader contract with no "object or path" fork without resolution.
    - definition: Add one minimal end-to-end JSON example (e.g. G1) including `golden_expectations` for the pass path, or explicitly defer with a decision id in decisions-log.
      done_when: A maintainer can diff the example against the schema table without guessing field shapes.
    - definition: Either tie external URLs to project-specific claims or demote them to "background reading" and add repo-local evidence pointers (CI yaml snippet names, script entrypoints) when those exist.
      done_when: No critical claim about this repo's CI rests only on generic blog posts.
```

---

## Summary

The note is a **structured design sketch** (registry root, row schema, CI pseudo, calibration matrix) that **does not fail** basic internal consistency for its stated scope. It **does fail** hostile **sourcing and contract closure** standards for research synthesis: vault “Raw sources” is a **pointer stub**, the fixture schema leaves a **loader ambiguity** on `lore_json`, there is **no minimal worked JSON**, and **external** citations are **generic industry reading**, not evidence that this repository’s tooling matches the proposed flags and gates.

## Strengths

- Clear separation of EMG-2 root vs `intent_replay` and rationale for CI `paths:` hygiene.
- Discriminated `golden_expectations` shapes (OK / BELOW_FLOOR / INVALID_EMG2_SLICE) align with vocabulary already used in 2.3.2 framing.
- Bounded worst-acceptable matrix rows (WA-1…WA-4, X-1, X-2) are a sane calibration procedure; Hypothesis threshold link is on-point for numeric floors.
- CI pseudo captures version id checks and glob iteration at a minimal level.

## Concerns (hostile)

1. **Vault sourcing is non-evidentiary.** The “Raw sources (vault)” section is literally two generic bullets pointing at linked notes without excerpt, figure, or decision id — unacceptable as proof the synthesis tracks those artifacts.

2. **Unresolved machine contract.** `lore_json` as “object or path” plus optional indirection is **three** loading models; CI cannot implement that without a specified precedence rule.

3. **No canonical instance.** A schema table without at least one **full JSON** example invites implementer drift and false-green harnesses.

4. **External sources do not validate repo claims.** Golden-file blog + Hypothesis article do not establish that **this** project uses `RECORD_GOLDEN`, `DETERMINISTIC_GATE_V1`, or CODEOWNERS the way 2.2.3 claims — the note **inherits** those strings without showing a trace.

5. **Overclaim risk (soft).** Phrases like “must match harness” and “echo from … frontmatter” are fine as **targets**, but without the actual frontmatter keys quoted from the linked note, they are **floating requirements**.

## Recommended follow-up

Treat this as **input to deepen**, not as closure: add excerpts or decision anchors, collapse `lore_json` to one representation, paste one G1 JSON, and add repo-local CI references when available.

**Validator run status:** Success (report written; synthesis quality = needs_work).
