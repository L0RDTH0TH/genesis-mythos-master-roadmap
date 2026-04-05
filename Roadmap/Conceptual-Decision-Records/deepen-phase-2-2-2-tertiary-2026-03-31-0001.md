---
title: "CDR — Phase 2.2.2 validate/classify schema and hook mapping"
created: 2026-03-31
tags:
  - roadmap
  - conceptual-decision-record
  - sandbox-genesis-mythos-master
para-type: Project
project-id: sandbox-genesis-mythos-master
parent_roadmap_note: "[[Phase-2-2-2-Validate-Classify-Schema-and-Hook-Mapping-Roadmap-2026-03-31-0001]]"
decision_kind: deepen
queue_entry_id: resume-deepen-gmm-222-20260330T000100Z-forward
master_goal: "[[Source-sandbox-genesis-mythos-master-goal-2026-03-30-0430]]"
validation_status: pattern_only
related_research: []
---

# CDR — Phase 2.2.2 validate/classify schema and hook mapping

## Summary

Minted tertiary **2.2.2** as the resolver stage that **validates** normalized intent envelopes against a **HookSchemaCatalog**, **classifies** into `(hookNamespace, hookId, operationKind)`, and **maps** to a deterministic **HookPayloadOutline**—explicitly **before** conflict resolution or emission. Invalid or ambiguous intents produce structured defer/reject diagnostics without mutating downstream state.

## PMG alignment

Keeps procedural generation **deterministic and replay-safe**: classification and mapping are pure functions of catalog revision + normalized envelope, matching the master goal’s emphasis on auditable pipelines and stable hooks.

## Alternatives and tradeoffs

| Alternative | Upside | Downide | Why not chosen |
|---------------|--------|---------|----------------|
| Combine validate+classify with conflict resolution in one tertiary | Fewer nodes | Blurs failure modes; harder to test replay | Separates **schema** concerns from **merge** concerns per parent 2.2 spine |
| Classify before full structural validation | Faster path for “obvious” hooks | Risk of classifying malformed envelopes | Validation-first preserves ordering contract from **2.2.1** |
| Implicit hook mapping (no explicit outline) | Shorter note | Hidden coupling to emitter | Explicit **HookPayloadOutline** supports handoff to **2.2.3** |

## Validation evidence

- Pattern-only: typed schema catalogs and deterministic classification from envelope routing literature; no vault research notes attached this run.

## Links

- Parent: [[Phase-2-2-2-Validate-Classify-Schema-and-Hook-Mapping-Roadmap-2026-03-31-0001]]
- Workflow anchor: `workflow_state` Log row **2026-03-31 00:01** — Target **Phase-2-2-2-Validate-Classify-Schema-and-Hook-Mapping-Roadmap-2026-03-31-0001**
- Queue: `resume-deepen-gmm-222-20260330T000100Z-forward`
