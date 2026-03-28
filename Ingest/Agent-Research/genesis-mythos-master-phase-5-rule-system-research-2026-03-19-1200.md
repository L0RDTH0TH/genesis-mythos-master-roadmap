---
title: Phase 5 — Rule System Integration & Extensibility — Research
created: 2026-03-19
tags: [research, agent-research, genesis-mythos-master]
para-type: Resource
status: active
project-id: genesis-mythos-master
linked_phase: 4-Archives/test-2-genesis-mythos-master/Roadmap/Phase-5-Rule-System-Integration-Extensibility/Phase-5-Rule-System-Integration-Extensibility-Roadmap-2026-03-10-1200.md
agent-generated: true
research_tools_used: [web_search]
---

## Key takeaways

- Modern RPG rule engines tend to use a plugin-based core where systems (rulesets, combat modules, progression) are separate packages loaded via stable interfaces rather than hard-coded branches.
- Event- or topic-based buses (with ordered stages) are a proven way to let features hook into damage, resolution, and progression flows without breaking each other.
- Open-source engines like OpenRpg and OpenPF2 separate framework primitives from concrete rulesets, allowing communities to ship alternative rule packs without forking core code.
- Typed or schema-checked events (rather than stringly-typed hooks) make extension safer and easier to refactor as the engine evolves.
- Demonstration scenarios (e.g. swapping biome/event generators) are critical: they validate that modular seams are real, not aspirational.

## Notes

### Plugin-based cores and rule packs

- OpenPF2’s Unreal-based framework treats the PF2 rules as a plugin on top of a more general ability and rules engine, illustrating the “ruleset-as-plugin” pattern.
- OpenRpg provides generic building blocks (templates, effects, game entities) and leaves concrete mechanics to higher-level modules, which mirrors the desired separation between “engine primitives” and “project-specific rules”.

### Hooks, events, and staged processing

- The Go-based RPG Toolkit uses a typed topic bus with chained topics for staged damage and resolution calculations; this significantly reduced complexity while increasing test coverage.
- Having explicit stages (e.g. base damage, mitigation, clamping, post-effects) provides natural extension points and makes it easier to reason about interactions between plugins.

### Extensibility demonstrations and community seams

- Community-driven systems document “extension seams” explicitly: which interfaces to implement, what invariants to respect, and where to register plugins.
- Example swaps (e.g. alternative biome generators, event schedulers) are often shipped as separate packages in the same org, serving as living documentation for third-party contributors.

## Sources

- [Source: OpenPF2 Core Framework (plugin-based PF2 rules)](https://github.com/OpenPF2/Core)
- [Source: OpenRpg — modular .NET RPG engine](https://github.com/openrpg/OpenRpg)
- [Source: RPG Toolkit — typed topics and chained damage resolution](https://pkg.go.dev/github.com/KirkDiggler/rpg-toolkit/rulebooks/dnd5e)

