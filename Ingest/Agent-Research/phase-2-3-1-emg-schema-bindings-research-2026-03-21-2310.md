---
title: Research — Phase 2.3.1 EMG schema bindings (golden matrix, PBT, canonical hash paths)
created: 2026-03-21
tags: [research, agent-research, genesis-mythos-master, phase-2-3-1, EMG, schema-bindings]
para-type: Project
project-id: genesis-mythos-master
linked_phase: Phase-2-3-1-EMG-Schema-Bindings
research_query: "deterministic simulation golden test matrix seed envelope fixture; property based testing stateful systems game simulation CI; schema binding replay hash ledger field paths best practice"
research_tools_used: [web_search, mcp_web_fetch]
research_escalations_used: 0
parent_context: "Nested pre-deepen for RESUME_ROADMAP; extends [[Ingest/Agent-Research/phase-2-3-validate-co-authored-world-emergence-research-2026-03-21-2230]]"
ira_validator_patch_applied: true
agent-generated: true
---

# Phase 2.3.1 — Bind EMG-1..3 to normative ledger/schema paths (external synthesis)

**Intent:** Give the tertiary **Phase-2-3-1-EMG-Schema-Bindings** concrete **industry patterns** for (1) **golden / seed-envelope fixtures**, (2) **stateful property-based testing** suited to sim + author command streams, and (3) **canonical bytes + field binding** so `replay_emergence_hash`, alignment scores, and denial closure can name **stable JSON paths** and **hash inputs** without ambiguous serialization.

**Do-not-duplicate (vault):** [[Ingest/Agent-Research/phase-2-3-validate-co-authored-world-emergence-research-2026-03-21-2230]] already defines EMG-1..3 at the metric level and points to Phase 2.2 harness vocabulary (G1–G3, F1–F2). This note **does not** re-derive EMG semantics; it focuses on **binding mechanics** and **test architecture**.

---

## 1. Golden matrix, seed envelope, and deterministic simulation rows

**Normative-style anchors (for fixtures / goldens):**

- **Session-scoped seeds + replayable failures:** centralize RNG policy per test session; persist minimal failing cases for CI — Hypothesis replay contract.

[Source: Hypothesis — replaying failures](https://hypothesis.readthedocs.io/en/latest/tutorial/replaying-failures.html)

- **Golden / approval-style comparisons:** pytest ecosystem uses snapshot or approval patterns for frozen expected outputs; pick **one** project-standard plugin and document it in the golden registry note.

[Source: pytest documentation — snapshot / regression patterns](https://docs.pytest.org/en/stable/)

- **CLI golden runner (pattern):** **goldplate** automates “run command → compare to checked-in expected output” for deterministic CLIs — useful mental model for **headless sim harness** rows in a matrix.

[Source: jaspervdj/goldplate — golden test runner for CLI applications](https://github.com/jaspervdj/goldplate)

> [!info] Optional reading (non-normative)
> The following article is **blog-level** context on ML-style fixtures/seeds/goldens — **not** a contract anchor next to RFC 8785 or vendor determinism docs.
>
> [Medium — fixtures, seeds, golden files (overview)](https://medium.com/@connect.hashblock/10-ways-to-test-ml-code-fixtures-seeds-golden-files-811310517cae)

**Binding proposal for EMG-1 (`replay_emergence_hash`):**

| Ledger concept | Suggested binding (spec task) |
|----------------|------------------------------|
| **Seed envelope** | One **frozen JSON object** (I-JSON-safe) per matrix row: e.g. `seed`, `scenario_id`, `rng_policy_version`, `fixture_id`; store **path** in golden registry row, not inline duplication. |
| **Inputs to emergence hash** | Canonicalize **subset** of post-tick manifest / ledger tail (see §3) with an explicit **field allow-list** per schema version — hash **only** listed paths. |
| **Golden matrix row** | Columns: `fixture_id`, `seed_envelope_ref` (path or content-hash), `tick_n`, `expected_emergence_hash` (hex), optional `tolerance_tier` for float-excluded branches. |

**CI envelope:** Treat each matrix row as an **immutable triple** `(seed_envelope_ref, intent_ledger_tail_ref_or_hash, tick_n)` so CI replays are byte-stable when inputs are pulled by hash.

---

## 1a. Float and GPU fence before EMG-1 hashing (normative draft for tertiary)

**Draft for Phase 2.3.1 tertiary — not a repo assertion until frozen with the sim stack.**

Cross-language **replay hashes** (EMG-1) must declare which **determinism tier** applies to values feeding JCS:

| Tier | What may feed EMG-1 allow-list | Hash posture |
|------|-------------------------------|--------------|
| **A — bit-exact** | Integers, fixed-point or string-encoded rationals, enums, stable IDs only | Full JCS subtree allowed in allow-list |
| **B — soft-float / CPU sim** | IEEE floats allowed in sim state | Either **exclude** float-bearing JSON paths from the EMG-1 allow-list **or** hash a **stability manifest** (`schema_id`, `canonicalization_profile_version`, `determinism_tier`, fixture refs) instead of raw float subgraphs |
| **C — GPU or vendor math** | Kernels, reductions, non-associative parallel accumulations | **Default:** subgraph is **non-hashable for EMG-1** unless a **GPU determinism contract** exists (kernel subset, reduction order, documented ULP / tolerance policy). Without that contract, EMG-1 **must not** hash GPU-derived fields. |

Floating-point non-associativity and rounding modes are why naive “hash the whole manifest” fails across toolchains.

[Source: Goldberg — What Every Computer Scientist Should Know About Floating-Point Arithmetic (ACM Computing Surveys)](https://dl.acm.org/doi/10.1145/103162.103163)

GPU stacks document limits on bitwise reproducibility; treat vendor guidance as **input** to Tier C policy.

[Source: NVIDIA CUDA C Programming Guide — reproducibility / deterministic results (deployment and math modes)](https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html)

**Link to §1 table:** the optional column `tolerance_tier` should reference **A / B / C** (or project sub-variants), not an ad hoc string.

---

## 2. Property-based testing for stateful simulation + “co-author” command streams

**Model vs system under test:** Stateful PBT generates **sequences of commands**; the harness keeps a **pure model** of expected state and compares **responses** from the real pipeline (sim + boundaries). Dependencies between commands (e.g. spawn before tick) are enforced by the generator/shrinker — the same structure applies when interleaving **author intents** and **sim ticks** if both are reified as commands.

[Source: Well-Typed — quickcheck-state-machine in depth](https://www.well-typed.com/blog/2019/01/qsm-in-depth/)

**Reproducibility requirement:** Generation and shrinking must **not** depend on values only known after execution; **reify** commands as data first, then execute — matches Hypothesis/replay style **minimal failing examples** you already cited in Phase 2.3 research.

[Source: Hypothesis — replaying failures](https://hypothesis.readthedocs.io/en/latest/tutorial/replaying-failures.html)  
*(Vault-first raw: [[Ingest/Agent-Research/Raw/phase-2-2-intent-parser-procedural-hooks-determinism-integration-research-raw-2026-03-20-0233]].)*

**Binding proposal for EMG-2 (`lore_sim_alignment_score`):**

| Element | Bind to |
|--------|---------|
| **Command alphabet** | Finite set in spec: e.g. `AuthorIntent`, `SimTick`, `QueryObservedCounters` — each maps to schema-valid payloads. |
| **Oracle** | Pure function over model state producing `sim_observed_counters` slice; real system must expose **same slice** at named paths after `SimTick*`. |
| **Score** | Document formula + floors in Phase 2.3.1 table; inputs are **values read at frozen JSON paths** on both sides. |

**Binding proposal for EMG-3 (`denial_invariant_closed`):** Reuse frozen **denial taxonomy** from Phase 2.2.1; PBT command set may include **force-denial** paths only if taxonomy codes are enumerated — property = “no observed code outside allow-list.”

---

## 3. Schema binding, replay hash, and canonical field paths

**Canonical bytes before hash:** For any cross-language **replay hash** or **manifest hash**, use a **documented canonicalization profile**. **RFC 8785 (JCS)** is the standard informational reference: deterministic property sorting, I-JSON constraints, ECMAScript-compatible serialization — produces a **hashable** UTF-8 string from a logical JSON value.

[Source: RFC 8785 — JSON Canonicalization Scheme (JCS)](https://www.rfc-editor.org/rfc/rfc8785.html)

**Practical binding rules (for EMG path table):**

1. **`schema_id` + `schema_version`** on every envelope and ledger fragment included in a hash (minor/major rules as in your vault backlog).
2. **Allow-list paths** — e.g. `$.manifest.entities[*].id` — stored in the spec, not inferred at runtime.
3. **Numbers in hashed payloads:** Prefer **strings** for fixed-point / integer semantics that must match across runtimes (per JCS guidance on IEEE doubles vs high-precision).
4. **Omit optional fields** vs explicit `null` — pick one convention per version and enforce in schema; canonical form must match.
5. **Replay:** When recomputing EMG-1, use the **same canonicalization profile** as golden generation; bump **profile version** when JCS or allow-list changes.

JSON Schema itself describes structure; **hash stability** is a **separate profile** (JCS or equivalent) — bind both in the normative note.

[Source: JSON Schema draft reference (vault raw index)](https://json-schema.org/draft/2020-12)

---

## 4. Traceability table (this run)

| Topic | External anchor | Vault raw |
|-------|-----------------|-----------|
| JCS / hashable JSON | RFC 8785 | [[Ingest/Agent-Research/Raw/phase-2-3-1-emg-schema-bindings-raw-2026-03-21-2310]] |
| Stateful PBT / command reification | Well-Typed QSM | same |
| Golden CLI pattern | goldplate | same |
| Hypothesis replay | Hypothesis docs | [[Ingest/Agent-Research/Raw/phase-2-2-intent-parser-procedural-hooks-determinism-integration-research-raw-2026-03-20-0233]] |

---

## 5. Draft binding artifacts (EXAMPLE — replace paths on schema freeze)

All paths below are **placeholders** until the normative schema and golden registry land in Phase 2.2 / 2.3 notes.

### EMG ↔ path ↔ profile ↔ registry (draft table)

| EMG-ID | JSON path(s) (EXAMPLE) | canonicalization_profile | golden_registry_column |
|--------|------------------------|--------------------------|-------------------------|
| EMG-1 `replay_emergence_hash` | `$.seed_envelope`, `$.intent_ledger_tail`, `$.manifest.post_tick.entities[*].id` **(EXAMPLE)** | `JCS-RFC8785@v1` + allow-list `emg1-v0` | `expected_emergence_hash` |
| EMG-2 `lore_sim_alignment_score` | `$.lore.flags`, `$.sim.counters` **(EXAMPLE)** | *(value read only; hash optional)* | `alignment_score_floor` |
| EMG-3 `denial_invariant_closed` | `$.denials[*].code` **(EXAMPLE)** | sorted code list → JCS | `unexpected_denial_count` |

### Finite PBT command alphabet (draft)

Each command maps to a **schema-valid** payload type from Phase 2.2 IntentPlan / tick contracts (replace type names with wiki-linked spec IDs on freeze).

- **`AuthorIntent`** — enqueue one canonicalized intent; model advances author-facing state.
- **`SimTick`** — advance simulation one logical tick; model advances sim counters used for EMG-2.
- **`QueryObservedCounters`** — read-only observation at frozen JSON paths for oracle comparison.
- **`SpawnCommit`** — (if in scope for emergence path) exercise spawn/manifest leg matching Phase 2.1 harness vocabulary.

**Property template (draft):** For all generated sequences respecting preconditions, after each `SimTick`, **EMG-3** observes no denial code outside the frozen taxonomy allow-list.

---

## Sources

- https://www.rfc-editor.org/rfc/rfc8785.html  
- https://www.well-typed.com/blog/2019/01/qsm-in-depth/  
- https://github.com/jaspervdj/goldplate  
- https://hypothesis.readthedocs.io/en/latest/tutorial/replaying-failures.html  
- https://docs.pytest.org/en/stable/  
- https://json-schema.org/draft/2020-12  
- https://dl.acm.org/doi/10.1145/103162.103163  
- https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html  

### Optional / non-normative

- https://medium.com/@connect.hashblock/10-ways-to-test-ml-code-fixtures-seeds-golden-files-811310517cae  

---

## Raw sources (vault)

- [[Ingest/Agent-Research/Raw/phase-2-3-1-emg-schema-bindings-raw-2026-03-21-2310]]  
- [[Ingest/Agent-Research/Raw/phase-2-2-intent-parser-procedural-hooks-determinism-integration-research-raw-2026-03-20-0233]] (Hypothesis + Isaac + replay patterns)  
- [[Ingest/Agent-Research/Raw/phase-2-3-world-emergence-raw-2026-03-21-2230]] (prior Phase 2.3 run)
