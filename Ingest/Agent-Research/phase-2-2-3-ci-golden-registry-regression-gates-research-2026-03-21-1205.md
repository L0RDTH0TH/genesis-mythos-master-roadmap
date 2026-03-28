---
title: Phase 2.2.3 — CI golden registry + boundary regression gates (research)
created: 2026-03-21
tags: [research, agent-research, genesis-mythos-master, roadmap]
para-type: Resource
project-id: genesis-mythos-master
linked_phase: Phase-2-2-3
research_query: "golden file testing deterministic replay CI regression gates"
research_tools_used: [web_search]
agent-generated: true
---

# Phase 2.2.3 — CI golden registry + boundary regression gates

Synthesis for **RESUME_ROADMAP** pre-deepen (`enable_research: true`), project **genesis-mythos-master**, linked phase **Phase-2-2-3**.

## Summary

Golden-file / snapshot comparison is the standard pattern for locking complex deterministic outputs: generate, diff against an approved reference, fail on any drift, and require an explicit human-reviewed update when behavior intentionally changes. For replay harnesses, non-deterministic fields (timestamps, UUIDs, wall-clock) must be masked or excluded before comparison so CI stays stable. Tooling ecosystems (pytest-golden, goldenfile/Rust, Bellwether-style workflows) converge on **treat golden updates like code changes** — version-controlled, reviewed, and attributable.

## Key takeaways (for roadmap injection)

- Register **G1/G2/G3** and **F1/F2** vectors as first-class **golden artifacts** (checksums + expected event payloads), not only prose tables.
- CI should run **ReplayAndVerify** on every PR touching intent canonicalization, schema validation, hash-chain wiring, or ledger apply paths.
- Golden updates require **two-person or CODEOWNER review** and a **deterministic_gate_version** bump when semantics change.
- Normalize or strip volatile fields before byte comparison; keep harness inputs aligned with `stable_run_context` (no wall-clock in preimage).

## Decisions / constraints

- Fail CI on golden mismatch; no soft approval in automation (human override lives in PR review + golden refresh).
- Keep golden files **small and curated** — minimal set that proves boundary + denial + double-apply semantics.
- Record **harness CLI version** and **`DETERMINISTIC_GATE_V1`** in CI environment matrix for traceability.

## Raw sources (vault)

- (none — web discovery only for this run)

## Sources

- [Golden File Testing: Output Comparison | Application Architect](https://www.application-architect.com/posts/golden-file-testing-output-comparison/)
- [pytest-golden · PyPI](https://pypi.org/project/pytest-golden/)
- [goldenfile · crates.io](https://crates.io/crates/goldenfile)
