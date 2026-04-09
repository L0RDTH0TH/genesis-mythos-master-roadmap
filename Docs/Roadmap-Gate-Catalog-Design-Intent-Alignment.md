---
title: Roadmap gate catalog — Design intent alignment (execution overlays)
created: 2026-04-14
tags: [second-brain, roadmap, gates, execution, design-intent]
para-type: Resource
status: active
links:
  - "[[3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-Godot-Execution|Roadmap-Gate-Catalog-Godot-Execution]]"
  - "[[3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-Sandbox-Execution|Roadmap-Gate-Catalog-Sandbox-Execution]]"
  - "[[3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-By-Track|Roadmap-Gate-Catalog-By-Track]]"
  - "[[3-Resources/Second-Brain/Docs/Validator-Tiered-Blocks-Spec|Validator-Tiered-Blocks-Spec]]"
  - "[[3-Resources/Second-Brain/Docs/Dual-Roadmap-Track|Dual-Roadmap-Track]]"
---

# Roadmap gate catalog — Design intent alignment (execution overlays)

## Purpose

This note defines the execution-track gate family **`design_intent_alignment`** for both lane overlays. It closes the gap between technical correctness and **intent correctness**: every execution item must demonstrate that it implements the higher-level design intent captured by conceptual authority and inspirations (for example Halo 3 commit orchestration, GTA 5 world persistence feel, BG3 dialogue signal semantics, Dwarf Fortress rollback discipline, Kingdom Come / Skyrim / Oblivion simulation expectations, World Anvil knowledge surfaces).

This gate is lane-neutral in structure and lane-isolated in execution: lane guards enforce it with lane-specific precision gates after §0 whitelist.

---

## Gate family — `design_intent_alignment`

**Goal:** Prevent roadmap drift from approved design direction and reduce late refactors by forcing explicit intent traceability on each execution item.

| Requirement | Normative behavior |
|-------------|-------------------|
| **Conceptual linkage** | Execution item must carry frontmatter **`conceptual_counterpart`** wikilink to the conceptual sibling (same mirror rule as Dual-Roadmap-Track). |
| **Inspiration evidence** | Execution item must cite one or more concrete studied inspiration sources relevant to the decision (for example Halo 3 orchestration cadence, BG3 dialogue signaling, Dwarf Fortress rollback robustness). |
| **Intent Mapping block** | Execution item must include a short **Intent Mapping** block that states: (1) selected design intent, (2) implementation mechanism in this execution item, (3) success signal / acceptance anchor. |
| **Validator alignment** | Missing or untraceable intent mapping is **`primary_code: design_intent_alignment_violation`** with **`recommended_action: block_destructive`** on execution track. |

---

## Minimal block format (required)

Use this exact structure (or semantically equivalent wording) in execution items:

```markdown
## Intent Mapping
- Design intent: <named target behavior tied to conceptual decision>
- Inspiration anchor(s): <specific source(s) studied, with short citation bullets>
- Execution implementation: <what this item changes to realize intent>
- Validation signal: <how validator/operator can confirm intent was preserved>
```

The block must be short, concrete, and tied to the current item (not generic project prose).

---

## Failure handling

When any required element is missing or not traceable:

- Emit **`reason_code: design_intent_alignment_violation`**
- Set **`primary_code: design_intent_alignment_violation`** (unless a higher-precedence hard blocker from Validator-Tiered-Blocks-Spec applies)
- Set **`recommended_action: block_destructive`**
- Do not claim Success for destructive continuation on the blocked scope

---

## Cross-references

- [[3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-Godot-Execution|Roadmap-Gate-Catalog-Godot-Execution]]
- [[3-Resources/Second-Brain/Docs/Roadmap-Gate-Catalog-Sandbox-Execution|Roadmap-Gate-Catalog-Sandbox-Execution]]
- [[3-Resources/Second-Brain/Docs/Validator-Tiered-Blocks-Spec|Validator-Tiered-Blocks-Spec]]
- [[3-Resources/Second-Brain/Docs/Dual-Roadmap-Track|Dual-Roadmap-Track]]
