---
title: Phase 4.1.5 junior handoff — control selection observability & advisory gates
research_query: phase-4-1-5 control selection observability SelectionWitnessEnvelope advisory gates junior handoff
linked_phase: "4.1.5"
project_id: genesis-mythos-master
created: 2026-03-27
tags: [research, agent-research, genesis-mythos-master, phase-4-1-5, observability]
research_tools_used: [web_search, vault_context]
research_focus: junior_handoff
research_preference_used: [official_docs, with_code, recent]
research_escalations_used: 0
sanity_check_rating: "4.2/5 (proceed — scoped to conceptual envelope + prior-art patterns)"
agent-generated: true
source_phase_note: "[[1-Projects/genesis-mythos-master/Roadmap/Phase-4-Perspective-Split-and-Control-Systems/phase-4-1-5-control-selection-observability-and-advisory-gates-roadmap-2026-03-27-0320]]"
---

## Purpose

Pre-deepen research consumable for **Phase 4.1.5** (control selection observability, `SelectionWitnessEnvelope_v0`, advisory gates). Targets a **junior implementer** with stack-agnostic guidance (**D-027**): cite observability *patterns*, not a chosen engine or language.

## Vault anchors (do not contradict)

| Artifact | Role |
| --- | --- |
| [[phase-4-1-5-control-selection-observability-and-advisory-gates-roadmap-2026-03-27-0320]] | Tertiary phase note — contract table: witness → advisory gates → operator digest |
| [[phase-4-1-4-control-read-model-and-golden-row-selection-contract-roadmap-2026-03-27-0320]] | Upstream selection: `SelectedGoldenRows_v0`, `tick_key`, read-only path |
| [[decisions-log]] | **D-032** (replay header / literal layout TBD), **D-043** (canonical preimage / sort order vault-TBD), **D-060** (CQRS vocabulary: presentation **read-model** vs **sim write** path; high-Ctx automation matrix), **D-027** (cross-runtime contracts, examples illustrative only) |

## Non-claims (explicit)

- Do **not** assert **handoff readiness ≥ 93** or any **rollup HR** closure; vault-honest debt remains **HR 92 < 93** where cited in project narrative.
- Do **not** assert **REGISTRY-CI PASS** or clear **G-P\*** registry rows; **REGISTRY-CI HOLD** stays execution-deferred.
- Do **not** freeze **replay row literals**, **canonical hash registry**, or **D-032/D-043** bindings in this slice — remain **OPEN_STUB** / `@skipUntil(D-032)` as in phase notes.

## Conceptual implementation map

### 1. `SelectionWitnessEnvelope_v0` (read-only witness)

- **Inputs:** `SelectedGoldenRows_v0` (from 4.1.4), `tick_key`, optional correlation id for trace join.
- **Behavior:** Immutable snapshot of *what was selected* for observability — no mutation of sim state, apply ledger, or golden files.
- **CQRS alignment (D-060):** This artifact lives on the **presentation / read-model side** of the boundary; it must not become a **sim-write** or **command** channel.

### 2. `SelectionGateAdvisory_v0` (advisory only)

- **Inputs:** witness envelope + `gate_policy` (versioned policy object, not CI truth).
- **Output:** Labeled signals (e.g. OPEN / HOLD / UNKNOWN) **without** mutating pass/fail bits in registry or rollup machinery.
- **Non-claim:** Advisory output may recommend operator action; it does **not** substitute for REGISTRY-CI or golden harness closure.

### 3. `ControlSelectionDigest_v0` (operator-facing)

- **Semantics:** **HOLD** vs **OPEN** (and explicit **no closure inflation** copy) per phase note table.
- **Trace join:** Stable ids linking digest rows back to witness envelope and phase note sections for audit.

## External prior art (illustrative, D-027)

Industry practice for **audit-friendly observability** often uses **structured spans** and **span events** with explicit attributes (actor, action, resource, outcome) so that traces double as audit trails without mixing policy enforcement into the telemetry layer — analogous separation to “witness vs advisory gate” here.

[Source: OpenTelemetry span events and audit-oriented attributes (conceptual overview)](https://oneuptime.com/blog/post/2026-02-06-opentelemetry-span-events-security-audit-trail/view)

[Source: Event audit trail patterns with OpenTelemetry](https://oneuptime.com/blog/post/2026-02-06-event-audit-trail-opentelemetry-spans/view)

## Suggested acceptance tests (Given / When / Then)

1. **Witness read-only**
   - **Given** a valid `SelectedGoldenRows_v0` and `tick_key`
   - **When** the system emits `SelectionWitnessEnvelope_v0`
   - **Then** no sim observable mutation, apply ledger append, or golden file write occurs as a side effect of emission.

2. **Advisory non-mutation**
   - **Given** a witness envelope and policy
   - **When** `SelectionGateAdvisory_v0` is computed
   - **Then** registry CI status bits and rollup HR fields are unchanged; only advisory records are produced.

3. **Digest semantics**
   - **Given** advisory output
   - **When** `ControlSelectionDigest_v0` is rendered for operators
   - **Then** HOLD/OPEN labels are present and documentation states no REGISTRY-CI PASS or HR≥93 closure from this path.

## Raw sources (vault)

- This run used vault-first context from phase notes and [[decisions-log]]; no new Raw note was required for external URLs (short-form citations inline above).

## Sources

- [OpenTelemetry span events — security audit trail (OneUptime blog)](https://oneuptime.com/blog/post/2026-02-06-opentelemetry-span-events-security-audit-trail/view)
- [Event audit trail with OpenTelemetry spans (OneUptime blog)](https://oneuptime.com/blog/post/2026-02-06-event-audit-trail-opentelemetry-spans/view)
