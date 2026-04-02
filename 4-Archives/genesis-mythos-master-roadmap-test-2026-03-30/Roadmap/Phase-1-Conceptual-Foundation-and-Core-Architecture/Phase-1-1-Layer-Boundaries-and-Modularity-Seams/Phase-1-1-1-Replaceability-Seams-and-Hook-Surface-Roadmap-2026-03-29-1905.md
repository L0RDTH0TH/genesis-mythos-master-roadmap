---
title: Phase 1.1.1 — Replaceability seams and hook surface
roadmap-level: tertiary
phase-number: 1
subphase-index: "1.1.1"
project-id: genesis-mythos-master
status: active
priority: high
progress: 15
created: 2026-03-29
tags: [roadmap, genesis-mythos-master, phase]
para-type: Project
links:
  - "[[Phase-1-1-Layer-Boundaries-and-Modularity-Seams-Roadmap-2026-03-29-1731]]"
  - "[[Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-03-29-1730]]"
handoff_readiness: 80
handoff_gaps:
  - "Further 1.1.2+ tertiaries optional; execution track types storage and wire formats"
---

## Phase 1.1.1 — Replaceability seams and hook surface

**Parent slice:** [[Phase-1-1-Layer-Boundaries-and-Modularity-Seams-Roadmap-2026-03-29-1731]]. This tertiary **instantiates** the seam list implied by Phase 1.1 diagrams and tables as a **checklist-backed contract surface**—still **stack-agnostic** per **[[decisions-log|D-027]]**: no engine, renderer, or language is selected here.

### Scope

- Enumerate **named replaceability seams** (what may be swapped or extended without rewriting the whole architecture).
- For each seam, give **minimal interface shape** (inputs/outputs/obligations) in words and **mid-technical** sketches—**not** concrete APIs or files (**execution track**).
- Align seams with **intent lanes** and **generation graph** boundaries from the parent note.

### Behavior

1. **Layer boundary seams** — Adjacent layers communicate only through the **allowed edges** in the parent Mermaid (input→intent→simulation→state; presentation←read models←state). Replaceability means: you can swap **implementations** behind each box if the **edge contract** (ordering, authority, fail-closed rules) holds.
2. **Generation stage seams** — Each stage is a **replaceable unit** when its **declared I/O manifest** (schema id + version, artifact kinds, stable ID namespaces) matches upstream/downstream expectations. Swapping a stage implementation must not change the **replay key** contract unless versioned as a breaking change.
3. **Rule / hook seams** — **Intent validation**, **post-validation hooks** (reputation, environment policy, scripted reactions), and **per-stage validators** are **injection points**. Replaceability = alternate policies/adapters that respect the same **invariants** (no silent authoritative mutation, observe-after-validation for world hooks).

### Interfaces (conceptual)

| Seam ID | What swaps | Consumer | Provider must expose (conceptual) | Hard invariant |
| --- | --- | --- | --- | --- |
| **S-L1** | Input normalization | Intent construction | Device-agnostic **intent candidates** + provenance metadata | No direct world writes |
| **S-L2** | Intent validation policy | Simulation | **Validated intent stream** + reject reasons + audit ids | Fail-closed on ambiguous authority |
| **S-L3** | Simulation core | Authoritative state | **State delta** + ordering witness + tick/run log slice | Single writer path to authoritative facts |
| **S-L4** | Read-model / projection | Presentation | **Stable read handles** / events; no back-channel writes | Presentation cannot author core facts |
| **S-G1** | Individual generation stage | Generation graph | **Typed manifest** in/out; deterministic key declaration | Namespace collision detection |
| **S-G2** | Graph scheduler | Generation graph | **Stage ordering** + cycle policy (DAG default) | Documented hazard if cycles allowed |
| **S-H1** | Hook adapter (player/operator lane) | Intent path | Policy checks: authority, dedupe, capability | Logged decisions |
| **S-H2** | Hook adapter (sim/world events lane) | Post-validation observation | Subscriptions / reactions without bypassing validation | Observe **after** validation |
| **S-H3** | Stage validator plugin | Generation pipeline | Validator output: pass / quarantine / fail with reason | Typed outputs only |

### Edge cases

- **Fat adapter** that bundles validation + simulation + IO in one module → must still **expose** the same logical seams for testability and replay; monolith is allowed only if **contracts** remain inspectable.
- **Synthetic events** that look like user intents → must carry **source class** so policies can reject or downgrade authority.
- **Third-party mods** (future phases) → seam IDs **S-H\*** and **S-G\*** are the primary extension loci; ownership and sandboxing **TBD** on execution track.

### Open questions

- Minimum **audit granularity** per seam (intent-level vs stage-level vs both) — **execution track** with CI goldens.
- Whether **event bus** is a single shared seam or multiple topic buses — defer until Phase 3–4 narrative needs it.

### Pseudo-code readiness (mid-technical)

```text
function ApplySeamContract(seamId, inboundManifest, context) -> OutboundManifest | Reject
  // conceptual: each seam validates manifest versions, records audit id, preserves replay key
  // execution: typed APIs, storage, and performance live on execution track
```

Reader can map each **Seam ID** to a future module boundary without assuming a programming language.

### Checklist (handoff-oriented)

- [x] **S-L1–S-L4** layer seams named with swap + invariant columns.
- [x] **S-G1–S-G2** generation graph seams tied to manifest + scheduler responsibilities.
- [x] **S-H1–S-H3** hook seams aligned with parent intent→hook table.
- [x] **1.1.2** tertiary: event-bus topology and mod-load order — [[Phase-1-1-2-Event-Bus-Topology-and-Mod-Load-Order-Roadmap-2026-03-29-1915]].

## Related

- [[Phase-1-1-Layer-Boundaries-and-Modularity-Seams-Roadmap-2026-03-29-1731]] — diagrams and stub stage table.
- [[Phase-1-Conceptual-Foundation-and-Core-Architecture-Roadmap-2026-03-29-1730]] — Phase 1 primary checklist.
- [[decisions-log]] — **D-027** stack-agnostic authority.
