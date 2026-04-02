---
created: 2026-03-29
pipeline: research
project_id: genesis-mythos-master
queue_entry_id: resume-deepen-gmm-415-research-enabled-20260329T120000Z
ira_call_index: 1
status: repair_plan
risk_summary:
  low: 5
  medium: 1
  high: 0
validator_report_path: .technical/Validator/research-synthesis-gmm-phase-4-1-5-pre-deepen-20260329T120700Z.md
synth_note_paths:
  - Ingest/Agent-Research/phase-4-1-5-pre-deepen-research-2026-03-29.md
---

# IRA report — research synthesis repair (validator-driven, call 1)

## Context

Nested pre-deepen research for `genesis-mythos-master` produced `Ingest/Agent-Research/phase-4-1-5-pre-deepen-research-2026-03-29.md`. Hostile validator returned `severity: medium`, `recommended_action: needs_work`, `primary_code: safety_unknown_gap`. IRA was invoked with `ira_after_first_pass: true`. This call proposes **read-only** repair guidance for the synthesis note only (Research pipeline applies edits under guardrails).

## Structural discrepancies

Validator minimum (accepted as floor; expanded below):

1. **Evidence inflation** — CQRS bullet uses "Operations research recommends…" while the chained citation is a **single vendor blog** (OneUptime), not OR literature or a standards normative claim.
2. **Pseudo-code vs correlation discipline** — `newStableId(tickKey, attemptOrdinal)` reads as deterministic/reusable; prose requires **new** correlation ids on retry. **`attemptOrdinal` is not defined** in the sketch (parameter appears without function signature or retry contract).
3. **Wikilink hygiene drift** — `source_phase_note` uses full vault path; **Raw sources (vault)** and **Explicit non-claims** use **basename-only** `[[phase-4-1-5-control-selection-…]]`, increasing ambiguous-resolution risk in large vaults.
4. **Coverage traceability** — No explicit map from phase **contract sketch** rows to this note's claims (validator flagged as optional gap; IRA treats as **medium** value for pre-deepen handoff).

**IRA expansion (beyond validator text):**

5. **TL;DR epistemic tone** — Opening promises "**industry patterns**" while external evidence mix is blog + W3C + dev article; without tiering, downstream readers may treat the note as stronger evidence than it is.
6. **Duplicate short-link pattern** — Same basename-style link appears in multiple sections (non-claims table, Raw sources); fixes should be **consistent** across all in-note references to the phase anchor, not only Raw sources.

## Proposed fixes

| # | risk | action_type | target_path | summary |
|---|------|-------------|-------------|---------|
| 1 | low | bounded_citation_rewrite | synthesis CQRS § | Replace "Operations research recommends…" with bounded language; add **primary** pointers (e.g. OpenTelemetry tracing concepts / span kinds, W3C trace context already cited) so read-vs-write separation is not laundered through OR framing. |
| 2 | low | clarify_pseudocode_contract | synthesis optional sketch | Rename helper (e.g. `newCorrelationIdForSelectionAttempt`); add **one-line invariant**: each retry increments `attemptOrdinal` **or** uses a fresh UUID so digest merge cannot attach partial retries to a prior attempt's id. Optionally add `attemptOrdinal` to the **function signature** shown in the fence. |
| 3 | low | normalize_wikilinks | synthesis body | Replace basename `[[phase-4-1-5-control-selection-observability-and-advisory-gates-roadmap-2026-03-27-0320]]` with the **same full path** as `source_phase_note` everywhere it appears (non-claims row, Raw sources, any inline link). |
| 4 | medium | add_traceability_subsection | synthesis note | Add short **Contract sketch row map**: which contract rows this synthesis **reinforces**, **defers**, or marks **out of scope** (table or bullet list only; no edits to the phase note). |
| 5 | low | soften_opening_claims | synthesis TL;DR | Nudge "industry patterns" toward **bounded** wording (e.g. common distributed-systems practice / illustrative external write-ups) unless primary citations are added. |
| 6 | low | epistemic_disclaimer | synthesis (CQRS or Sources) | One explicit sentence: external links are **illustrative**, not vault closure or normative proof for REGISTRY-CI / HR / deferred decisions. |

## Notes for future tuning

- Research synthesis template could require **evidence tier** tags (normative / secondary / opinion) beside external URLs.
- Agent prompts should ban "operations research" unless a **named** study or survey is cited.
- Pseudocode blocks for vault-adjacent notes should always **define** parameters that affect safety semantics (`attemptOrdinal`, retry policy).

## Machine `suggested_fixes` (for caller)

See parent return payload `suggested_fixes[]`.
