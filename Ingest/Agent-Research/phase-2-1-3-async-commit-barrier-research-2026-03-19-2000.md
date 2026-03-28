---
title: Pre-deepen research — Phase 2.1.3 async commit barrier
created: 2026-03-19
tags: [research, agent-research, genesis-mythos-master]
linked_phase: Phase-2-1-3
project-id: genesis-mythos-master
research_query: deterministic async generation commit barrier stage ledger reconciliation
research_tools_used: [web_search, mcp_web_fetch]
agent-generated: true
---

# Phase 2.1.3 — External grounding (async / barriers)

## Synthesis

Mature PCG stacks stress **reproducibility from seeds** and **layered dependencies** so parallel work does not violate ordering invariants. **Layer-based** frameworks separate layer inputs/outputs so downstream consumers never see partial scratch state—conceptually adjacent to a **single publish** per stage. Engine write-ups emphasize **DAG-shaped dependency graphs** (e.g. rendering) where synchronization is explicit; the analogy for generation is **no visible partial manifests** until a **commit record** closes the stage.

For **async workers**, the safe pattern is: **compute privately → validate hashes → append one ledger record** (barrier). Partial worker failure must surface as **replay events**, not silent merge into `EntityManifest`.

## Key takeaways (for injection)

- Treat **commit barrier** as a *ledger tail* invariant: one ordered append per stage completion, never interleaved writes from concurrent tasks.
- **Layer / stage isolation** (inputs frozen, outputs immutable) matches Genesis **published handles** from 2.1.1.
- **DAG scheduling** in engines is a useful metaphor: dependencies are explicit; our StageGraph already provides the DAG—the barrier is the **publish gate** at each node.

## Sources

- [Source: LayerProcGen (layer-based procedural generation)](https://github.com/runevision/LayerProcGen)
- [Source: Godot — rendering DAG synchronization (parallelism with explicit deps)](https://godotengine.org/article/rendering-acyclic-graph/)
- [Source: ProcGen — production determinism themes](https://procgen.com/)

## Raw sources (vault)

_(No separate raw note this run; web snippets summarized inline.)_
