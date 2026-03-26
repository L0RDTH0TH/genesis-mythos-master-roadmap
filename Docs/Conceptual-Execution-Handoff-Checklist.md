---
title: Conceptual → execution handoff checklist (NL completeness)
created: 2026-03-26
tags: [second-brain, roadmap, conceptual, execution, handoff]
para-type: Resource
status: active
links:
  - "[[3-Resources/Second-Brain/Docs/Dual-Roadmap-Track|Dual-Roadmap-Track]]"
  - "[[3-Resources/Second-Brain/Parameters|Parameters]]"
---

# Conceptual → execution handoff checklist (NL completeness)

## Purpose

**Ready for handoff to execution** means: **every** roadmap node at **primary, secondary, tertiary, quaternary, and deeper** indices that exists in the project tree has **behavior fully described in natural language**—not that CI, registry, or rollup tables are green. Those are **execution-track** concerns.

Use this checklist **per phase roadmap note** (recurse for each subphase note). **Done** for that note = every required row below is satisfied for **behavior** in plain language.

## Per-note checklist

| # | Requirement | Done when |
|---|-------------|-----------|
| 1 | **Scope** | One paragraph states what this slice covers and what it explicitly does *not* cover. |
| 2 | **Behavior** | Actors, inputs, outputs, and ordering are described in NL (no reliance on “see code”). |
| 3 | **Interfaces** | What this slice expects from adjacent slices and what it guarantees outward (contracts in words). |
| 4 | **Edge cases** | Known edge cases or failure modes named; deferrals labeled **TBD** if intentional. |
| 5 | **Open questions** | Remaining ambiguities listed or explicitly empty. |
| 6 | **Pseudo-code readiness** | Reader can start sketching pseudo-code without guessing core behavior (may reference headings for detail). |

## Recursion

- **Primary** phase notes: all six rows for the phase container + **each** linked **secondary** note.
- **Secondary → tertiary → quaternary:** repeat the same six rows for **every** child note in the tree until leaves (task-level notes) meet row **2** at minimum.

## Conceptual “complete” (lighter bar)

**Conceptual complete** for the whole project (before full handoff): the system is explained in coherent NL end-to-end; decomposition is stable enough to resume; **pseudo-code can begin** at leaves. Full **handoff** requires this checklist **complete for every** phase/subphase note in scope.

## Related

- [[3-Resources/Second-Brain/Docs/Dual-Roadmap-Track|Dual-Roadmap-Track]] — Definitions and authority
- [[3-Resources/Second-Brain/Vault-Layout|Vault-Layout]] — Dual roadmap track, Conceptual-Amendments
- [[3-Resources/Second-Brain/Parameters|Parameters]] — Conceptual autopilot, canonical target
