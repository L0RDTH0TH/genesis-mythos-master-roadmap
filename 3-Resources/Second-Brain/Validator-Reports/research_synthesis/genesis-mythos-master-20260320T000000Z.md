---
title: Validator — research_synthesis (genesis-mythos-master / Phase-2-1-5)
created: 2026-03-20
tags: [validator, research_synthesis, genesis-mythos-master]
validation_type: research_synthesis
project_id: genesis-mythos-master
linked_phase: Phase-2-1-5
queue_entry_id: resume-roadmap-genesis-mythos-master-phase2-deepen-20260319-2035-followup
parent_run_id: resume-roadmap-genesis-mythos-master-phase2-deepen-20260319-2035-followup
synth_notes_validated:
  - Ingest/Agent-Research/phase-2-1-5-spawn-commit-research-2026-03-19-2035.md
severity: medium
recommended_action: needs_work
ready_for_handoff: "no"
reason_codes:
  - safety_unknown_gap
  - missing_command_event_schemas
  - missing_task_decomposition
potential_sycophancy_check: true
---

# research_synthesis — hostile verdict

**Inputs:** `Ingest/Agent-Research/phase-2-1-5-spawn-commit-research-2026-03-19-2035.md`  
**Phase context (read-only cross-check):** `1-Projects/genesis-mythos-master/Roadmap/.../phase-2-1-5-spawn-commit-idempotent-entity-apply-replay-harness-roadmap-2026-03-19-2035.md`

## Machine-readable verdict (return payload)

```yaml
severity: medium
recommended_action: needs_work
ready_for_handoff: no
reason_codes:
  - safety_unknown_gap
  - missing_command_event_schemas
  - missing_task_decomposition
potential_sycophancy_check: true
gap_citations:
  safety_unknown_gap: "_(No raw URL captures this run; web_search snippets only.)_"
  missing_command_event_schemas: "second application with same **idempotency_ledger_key** must not create duplicate entities"
  missing_task_decomposition: "This note adds **industry patterns** for deferred command application and deterministic ordering"
```

## Summary

The note is a **three-bullet blog sketch**, not research you can safely inject into a **tertiary** roadmap slice without marking `#review-needed` on anything derived from it. The Unity ECB pointer is directionally useful; everything else is **under-evidenced** or **terminologically sloppy** relative to the phase note’s normative schema.

## Strengths

- States up front that **project ledger rules stay authoritative** — correct epistemic hygiene.
- Unity ECB doc link is a **real** primary-ish source for deferred structural commands and ordering pressure.
- `research_query` in frontmatter matches the intent of Phase 2.1.5 (command buffer + deterministic ordering).

## Failures (why this is not “synthesis done”)

1. **Provenance collapse:** The note confesses it has **no raw captures**. That means no one can audit what text the model actually saw; “web_search snippets only” is **research theater**, not traceable evidence.
2. **Wrong / invented binding surface:** Phase 2.1.5 specifies **`spawn_idempotency_key := (stream_id, spawn_batch_id, spawn_row_stable_id, spawn_commit_semver)`**. The synthesis invents **`idempotency_ledger_key`** and asserts ledger-hit semantics around it. That is **not** a harmless paraphrase — it is **schema drift** that will pollute deepen output if pasted blindly.
3. **Bevy “source” is a GitHub issue thread** — not API docs, not a merged design. Using it to justify idempotent spawn behavior is **anecdotal** at best; at worst it is **false precision** (issue ≠ shipped invariant).
4. **Coverage hole vs query and vs phase:** Almost **nothing** on **replay harness engineering** (golden vectors, world snapshots, double-apply tests) beyond what the phase note already says. No second engine (Flecs, EnTT, UE Mass, etc.), no determinism/replay papers, no test-harness patterns — for a phase whose title includes **“replay harness”**, that is **negligent coverage**.

## `reason_codes` × mandatory verbatim gap citations

| reason_code | Verbatim snippet (from validated synth note) |
|-------------|-----------------------------------------------|
| `safety_unknown_gap` | `_(No raw URL captures this run; web_search snippets only.)_` |
| `missing_command_event_schemas` | `second application with same **idempotency_ledger_key** must not create duplicate entities` — **does not align** with phase note’s `spawn_idempotency_key` / `spawn_row_stable_id` definitions; no explicit field-by-field mapping table. |
| `missing_task_decomposition` | `This note adds **industry patterns** for deferred command application and deterministic ordering` — claims industry patterns but delivers **two links** and **no** decomposed replay/idempotency **task-level** external practices (harness layout, CI replay, snapshot diff contracts). |

## `next_artifacts` (definition of done)

- [ ] **Raw or quotable captures:** At least one note under `Ingest/Agent-Research/Raw/` **or** inline fenced quotes with dates — enough to verify ECB ordering claims **without** trusting model memory.
- [ ] **Terminology repair:** Either delete `idempotency_ledger_key` or add a **mapping table**: Unity/Bevy concept → **exact** Phase 2.1.5 field names (`spawn_row_stable_id`, `spawn_idempotency_key`, `spawn_commit_semver`, reason_code `SPAWN_IDEMPOTENCY_REPLAY`).
- [ ] **Second independent ECS or replay source:** Non-Unity (e.g. Flecs deferred ops, EnTT registry stability, or a **deterministic replay** article) — **primary doc or paper**, not a random issue comment thread as the only idempotency anchor.
- [ ] **Replay harness slice:** A short subsection with **named external patterns** for golden snapshots / double-apply tests (even if “industry standard CI” rather than games-specific), tied to the phase’s `replay_spawn_commit` pseudo-code.

## `potential_sycophancy_check`

**true.** The obvious softening move is to praise the Unity analogy and the “authoritative ledger” disclaimer, then call the note “adequate pre-deepen context.” It is **not**. The missing raw captures + invented key name + issue-thread sourcing are **exactly** the kind of gloss that passes friendly review and **fails** engineering handoff.

---

**Return token:** **Success** (validator completed; `severity: medium` / `needs_work` is an observability signal for downstream deepen, not subagent failure).
