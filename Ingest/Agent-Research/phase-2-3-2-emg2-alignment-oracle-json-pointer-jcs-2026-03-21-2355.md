---
title: Research — Phase 2.3.2 EMG-2 floor F (alignment score testing, oracle, JSON path freeze)
created: 2026-03-21
tags: [research, agent-research, genesis-mythos-master, phase-2-3-2, EMG-2, alignment, testing]
para-type: Project
project-id: genesis-mythos-master
linked_phase: Phase-2-3-2-EMG-2-Floor-F-AlignmentFn
research_query: "deterministic 0-100 lore vs sim counter alignment; property-based stateful simulation oracle; JSON Pointer canonical paths for nested flags/counters"
research_tools_used: [web_search, mcp_web_fetch]
research_escalations_used: 0
parent_context: "Nested research helper for RESUME_ROADMAP deepen; follows [[phase-2-3-1-emg-normative-schema-bindings-and-seed-matrix-v0-roadmap-2026-03-21-2205]] and [[Ingest/Agent-Research/phase-2-3-1-emg-schema-bindings-research-2026-03-21-2310]]"
queue_entry_id: resume-roadmap-genesis-mythos-master-20260321-followup-deepen-next-next
parent_run_id: eatq-20260321-gmm-deepen-2245
agent-generated: true
---

# Phase 2.3.2 — EMG-2 floor **F**: testing authoritative lore flags vs sim counters

**Intent:** External patterns to **freeze** `AlignmentFn_v0(lore, sim) → 0..100`, compare **authoritative** lore boolean/bitset views to **sim-observed** counters, and **fail closed** when paths are missing, types disagree, or score &lt; **F**. Complements (does not replace) the PBT command alphabet and binding table in [[Ingest/Agent-Research/phase-2-3-1-emg-schema-bindings-research-2026-03-21-2310]].

**Do-not-duplicate (vault):** Phase 2.3.1 research already covers golden matrix rows, float/GPU tiers for hashing, and the generic EMG-2 binding table (`QueryLoreFlags` / `QueryObservedCounters`). This note focuses on **operational test design** for the **0–100 alignment score**, **oracle construction**, and **normative path strings**.

---

## 1. Freeze JSON paths with RFC 6901 (Pointer), not ad hoc “dot paths”

**Contract:** Store `authoritative_lore_flags_path` and `sim_observed_counters_path` as **RFC 6901 JSON Pointer** strings (e.g. `/lore/flags`, `/sim/counters`), not ambiguous `$.a.b` dialect mixes.

- **Syntax:** slash-separated reference tokens; `~` → `~0`, `/` → `~1` in tokens; array indices **without** leading zeros; evaluation fails if any token does not resolve — applications **SHOULD** define error handling (fail-closed for EMG-2).

[Source: RFC 6901 — JSON Pointer](https://www.rfc-editor.org/rfc/rfc6901.html)

**EMG-2 implications:**

- **Canonical registry row:** one pointer per side; version bump when pointer changes (align with `emg1_allow_list_version` style discipline from 2.3.1).
- **Nested counters/flags:** document whether leaves are **objects of ints**, **arrays**, or **bitset-as-hex strings**; pointer must target the **same structural type** on both sides before `AlignmentFn_v0` runs.
- **Fail-closed:** if either pointer fails evaluation at test time → treat as **alignment failure** (score 0 or explicit `INVALID_PATH` outcome), not silent default.

---

## 2. Deterministic comparison at frozen subtrees: JCS on extracted slices

When `AlignmentFn_v0` needs **stable bytes** (for golden tests, hashes, or cross-language CI), extract the JSON values at the two pointers and canonicalize with **JSON Canonicalization Scheme (JCS, RFC 8785)** before comparing or hashing.

- **Why:** signing/hashing requires invariant serialization; JCS sorts properties and constrains data to I-JSON-compatible rules so independent implementations agree.

[Source: RFC 8785 — JSON Canonicalization Scheme (JCS)](https://www.rfc-editor.org/rfc/rfc8785.html)

**EMG-2 implications:**

- **0–100 score inputs:** define whether the score is computed from **raw structured values** (ints/bools only) or from **JCS bytes** of a **bounded** projection object (e.g. `{ "lore": <slice>, "sim": <slice> }`). Mixed float paths remain subject to Tier A/B/C from 2.3.1 research.
- **Golden tests:** prefer **integer-only** alignment fixtures for floor **F** calibration; add JCS snapshot of the **projection** only when the spec commits to that representation.

---

## 3. Property-based / stateful harness: model oracle vs system under test

**Pattern:** Maintain a **pure reference model** that predicts observable state; drive the **real** sim + API with generated **command sequences**; after each step (or after bounded `SimTick` runs), read **both** lore-flag and sim-counter slices and assert invariants.

- **Oracle for EMG-2:** the model exposes expected counters (or expected flag-derived counts); `AlignmentFn_v0` compares **authoritative lore** projection to **sim** projection — in tests, the model can stand in for “ground truth” when the spec defines that equivalence.
- **Shrinking:** minimal failing sequences localize drift between model and implementation.

[Source: Well-Typed — quickcheck-state-machine in depth](https://www.well-typed.com/blog/2019/01/qsm-in-depth/)

**Hypothesis (Python ecosystem):** stateful tests use `RuleBasedStateMachine` / strategies to generate valid command sequences and check postconditions; combine with **explicit replay** of reduced failures in CI.

[Source: Hypothesis — Stateful testing](https://hypothesis.readthedocs.io/en/latest/stateful.html)

---

## 4. Deterministic “alignment score 0–100” in CI

**Suggested test layers (for tertiary spec text):**

| Layer | Purpose | Fail-closed behavior |
|-------|---------|----------------------|
| **Unit** | `AlignmentFn_v0` on hand-crafted lore/sim pairs | Missing key → 0 or error bit; never coerce |
| **Golden** | Fixed fixtures → expected score + expected JCS of projection | Mismatch fails build |
| **PBT** | Sequences from finite alphabet (2.3.1); oracle checks score ≥ **F** when model says aligned | Counterexample saved with replay blob |

**Floor F:** choose **F** from **worst acceptable** calibrated fixture set (not from happy-path only). Document **F** in frontmatter + pseudo-code when paths are frozen (per D-022/D-023 checklist).

---

## 5. Decision-ready constraints (for Phase 2.3.2 tertiary)

1. **Pointers:** RFC 6901 strings in registry; no duplicate member names in objects at resolved nodes (RFC 6901: duplicate names → undefined).
2. **Extraction failure:** fail-closed (no default “100” alignment).
3. **Canonical bytes:** if cross-language goldens use hashing, specify JCS profile (RFC 8785) on an explicit projection object.
4. **Oracle:** for PBT, reference model must be **pure** and **versioned** alongside sim schema version.
5. **Score semantics:** document whether partial overlap yields partial credit or hard fail per missing counter — operators need one rule, not two.

---

## Raw sources (vault)

- Prior synthesis (bindings + alphabet): [[Ingest/Agent-Research/phase-2-3-1-emg-schema-bindings-research-2026-03-21-2310]]

---

## Sources

- [RFC 6901 — JSON Pointer](https://www.rfc-editor.org/rfc/rfc6901.html)
- [RFC 8785 — JSON Canonicalization Scheme (JCS)](https://www.rfc-editor.org/rfc/rfc8785.html)
- [Well-Typed — An in-depth look at quickcheck-state-machine](https://www.well-typed.com/blog/2019/01/qsm-in-depth/)
- [Hypothesis — Stateful testing](https://hypothesis.readthedocs.io/en/latest/stateful.html)
