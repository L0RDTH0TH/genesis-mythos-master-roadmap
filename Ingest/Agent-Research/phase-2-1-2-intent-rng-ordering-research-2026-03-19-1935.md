---
title: Research — Phase 2.1.2 intent stream & hierarchical RNG ordering
created: 2026-03-19
tags: [research, agent-research, genesis-mythos-master]
linked_phase: Phase-2-1-2
project-id: genesis-mythos-master
research_query: "deterministic RNG substreams PCG splittable generators procedural pipeline stage ordering"
research_tools_used: [web_search]
agent-generated: true
research_escalations_used: 0
---

# Phase 2.1.2 — Intent / RNG ordering (pre-deepen synthesis)

## Summary

Industry and literature patterns for **deterministic multi-stage PCG** emphasize **independent RNG streams per stage or concern** so that skipping, reordering validation, or partial replay does not desynchronize downstream consumers. **PCG-family generators** expose explicit **stream identifiers** from a shared seed; **splittable / hash-based PRNGs** (e.g. SplitMix-style constructions, splittable generators via cryptographic hashing) support **structured seed splitting** for hierarchical pipelines. For Genesis, this reinforces Phase 2.1.1’s rule that **sub-stream ids** are derived from `(stage_name, stage_version_id, region_id, rule_id)` and that **topological stage order** governs **commit** order, not ad-hoc RNG consumption order across stages.

## Key takeaways (handoff-oriented)

- Assign **distinct stream IDs** (or splittable child generators) per stage so **omitting an optional stage** does not perturb RNG draws in later mandatory stages when replay identity is preserved.
- **Seal** stream state at stage publish boundaries and record **consumption checkpoints** if future optimization skips draws inside a stage (advanced; v0 may only seal at publish).
- **IntentAnnotate** (when enabled) should consume a **dedicated stream namespace** so intent noise cannot collide with lattice or manifest draws.
- **Traversal / sort order** for manifests remains orthogonal to RNG stream creation: both must be **explicit tokens** in the ledger (already started in 2.1.1).

## Decisions / constraints (candidate)

- **Constraint:** Any optional stage that can be skipped in v0 must prove **stream isolation** via tests: skip-run vs full-run manifest hashes match on mandatory stages when intent is disabled.
- **Pending:** Whether `IntentAnnotate` attaches **before** `LatticeSynthesis` or **between** `PolicyBind` and `ManifestEmit` — decision deferred to 2.1.2 DAG patch with cycle check.

## Raw sources (vault)

- External search only for this run; no raw URL fetch note.

## Sources

- [Source: PCG — multiple streams / distance](https://www.pcg-random.org/useful-features.html)
- [Source: Splittable PRNGs using cryptographic hashing (Chalmers)](https://research.chalmers.se/publication/183348)
- [Source: StackOverflow — PCG seed / stream discussion](https://stackoverflow.com/questions/67466830/rebase-pcg-seed)
- [Source: SplitMix / splittable generators (OOPSLA paper PDF index)](https://gee.cs.oswego.edu/dl/papers/oopsla14.pdf)
