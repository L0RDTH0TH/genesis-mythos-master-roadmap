---
title: Phase 2.2.1 (Execution) — Intent envelope normalization and identity binding
created: 2026-04-12
tags:
  - roadmap
  - execution
  - godot
project-id: godot-genesis-mythos-master
roadmap_track: execution
phase: 2
subphase: "2.2.1"
roadmap-level: tertiary
status: in-progress
handoff_readiness: 86
handoff_gaps:
  - "Rollup / registry / CI / HR proof rows remain execution-deferred per D-Exec-rollup-deferral — no fabricated ci_run_id."
handoff_audit_last: "2026-04-12T21:15:00Z"
conceptual_counterpart: "[[1-Projects/godot-genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building/Phase-2-2-Intent-Resolver-and-Hook-Mapping/Phase-2-2-1-Intent-Envelope-Normalization-and-Identity-Binding-Roadmap-2026-03-30-2338]]"
---

# Phase 2.2.1 (Execution) — Intent envelope normalization and identity binding

Execution remint for **Phase 2 tertiary 2.2.1** on the parallel spine. Binds conceptual NL from [[1-Projects/godot-genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building/Phase-2-2-Intent-Resolver-and-Hook-Mapping/Phase-2-2-1-Intent-Envelope-Normalization-and-Identity-Binding-Roadmap-2026-03-30-2338]] (canonical envelope, actor binding, frame/channel identity, dedupe/idempotency) to **`IIntentResolver`** **normalize** stage inputs feeding **classify** (next tertiary **2.2.2**). Parent seam: [[Phase-2-2-Intent-Resolver-and-Hook-Mapping-Roadmap-2026-04-12-2110]].

## Intent mapping (execution)

| Conceptual contract | Execution mechanism | Godot metaphor |
| --- | --- | --- |
| **RawIntentRecord** ingress | Surface-tagged records before canonical shape | [Array](https://docs.godotengine.org/en/stable/classes/class_array.html) of [Dictionary](https://docs.godotengine.org/en/stable/classes/class_dictionary.html) (or single dict stream) with stable iteration order for determinism |
| **CanonicalIntentEnvelope** | Post-normalize comparable object | [Dictionary](https://docs.godotengine.org/en/stable/classes/class_dictionary.html) with [StringName](https://docs.godotengine.org/en/stable/classes/class_stringname.html) keys: `intent_record_id`, `actor_binding`, `channel_id`, `frame_id`, `target_scope`, `payload_normalized`, `normalization_revision` |
| **IntentRecordId** / **ActorBinding** | Logical keys for dedupe + replay | [StringName](https://docs.godotengine.org/en/stable/classes/class_stringname.html) or [String](https://docs.godotengine.org/en/stable/classes/class_string.html) carriers; compare via StringName for hot path |
| **NormalizationPolicy** | Config snapshot for dedupe window + idempotency | [Dictionary](https://docs.godotengine.org/en/stable/classes/class_dictionary.html) embedded in resolver context; versioned `normalization_revision` token |
| **Normalize queue (per frame)** | Ordered batch before classify | [Array](https://docs.godotengine.org/en/stable/classes/class_array.html) of envelopes; optional `sort_custom` with explicit comparator from policy ([Callable](https://docs.godotengine.org/en/stable/classes/class_callable.html)) |

### Doc anchors (stable)

> Dictionary keys compare by value; StringName compares by name id — use for intent ids and hook keys in hot paths.  
> — [Dictionary](https://docs.godotengine.org/en/stable/classes/class_dictionary.html), [StringName](https://docs.godotengine.org/en/stable/classes/class_stringname.html)

## Normalize-stage binding (resolver)

| Step | Role | Reads | Produces |
| --- | --- | --- | --- |
| Ingest | Admit raw records | Allowed surfaces / adapters | `RawIntentRecord[]` |
| Normalize | Defaults + coercion + metadata | Raw records + `NormalizationPolicy` | Partial canonical fields |
| Bind identity | Stable ids + actor | Normalized fields | `intent_record_id`, `actor_binding`, `channel_id`, `frame_id` |
| Dedupe / fold | Windowed merge/reject | Id + scope + policy | Collapsed envelope list |
| Emit to classify | Handoff | Normalized envelopes | Input stream to **validate/classify** (**2.2.2**) — **no** skip of classify on “fast paths” |

## Runner sketch (non-authoritative; text only)

```text
# Pseudocode shape — not a committed engine API
func normalize_intents_for_frame(raw_records: Array, policy: Dictionary, frame_id: StringName) -> Array:
  var queue: Array = []
  for r in raw_records:
    var partial := coerce_to_canonical_fields(r, policy)
    var bound := bind_identity(partial, frame_id, policy)
    queue.append(bound)
  queue = dedupe_or_fold(queue, policy)
  return queue  # Array of Dictionary envelopes ready for classify stage
```

- **Determinism:** same raw bytes + same `policy` snapshot + same `frame_id` ⇒ same normalized array (including tie ordering from `Callable` comparator when used).

## Acceptance criteria (execution-first)

| ID | Criterion | Evidence | Status |
| --- | --- | --- | --- |
| AC-2.2.1-A | Every raw record becomes a **CanonicalIntentEnvelope** or explicit reject diagnostic | Schema check on dict keys + revision tag | Planned |
| AC-2.2.1-B | Actor / frame / channel binding is total for accepted envelopes | Missing-field reject path | Planned |
| AC-2.2.1-C | Dedupe policy is snapshot-stable across replay | Golden envelope list hash | Planned |

## Open decisions (execution-deferred; cite conceptual)

- **D-2.2.1-intent-id-scope** / **D-2.2.1-dedupe-window** — remain tracked under [[1-Projects/godot-genesis-mythos-master/Roadmap/decisions-log]]; no cryptographic closure claimed here.

## Explicit deferrals (D-Exec-rollup-deferral)

- **`GMM-2.4.5-*`**, registry hashes, CI run IDs, rollup HR — **not** claimed closed.
- Full **validate/classify** schema and hook mapping tables — **2.2.2**; conflict/merge policy — **2.2.3**+.

## Related

- Parent secondary **2.2**: [[Phase-2-2-Intent-Resolver-and-Hook-Mapping-Roadmap-2026-04-12-2110]]
- Next tertiary **2.2.2** (validate/classify schema): conceptual [[1-Projects/godot-genesis-mythos-master/Roadmap/Phase-2-Procedural-Generation-and-World-Building/Phase-2-2-Intent-Resolver-and-Hook-Mapping/Phase-2-2-2-Validate-Classify-Schema-and-Hook-Mapping-Roadmap-2026-03-31-0001]]
- Phase 2 execution primary: [[../../Phase-2-Procedural-Generation-and-World-Building-Roadmap-2026-04-12-1515]]
