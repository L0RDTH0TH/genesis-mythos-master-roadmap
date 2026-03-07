---
name: Finish Testing System
overview: Complete the Second Brain testing system by populating the PARA regression suite with runnable fixtures, documenting the baseline run procedure, and making the Regression-Stability-Log baseline row actionable. Optionally add test-coverage-by-responsibility to Testing.md.
todos: []
isProject: false
---

# Finish Second Brain Testing System

## Current state

- **tests/ layout and run instructions**: Documented in [Testing.md](3-Resources/Second-Brain/Testing.md); `run_tests.py` and unittest discover work.
- **Regression-Stability-Log**: [Regression-Stability-Log.md](3-Resources/Second-Brain/Regression-Stability-Log.md) defines flip-rate metric and table, but the baseline row is **TODO** (no real run yet).
- **para-regression**: [para-regression.md](3-Resources/Second-Brain/tests/para-regression.md) has table structure but all rows are placeholders (`_TODO_`); no real `note_path` or `golden_top_path` values, so the regression run cannot be executed.

Ingest Phase 1 processes notes under **Ingest/** (per always-ingest-bootstrap and mcp-obsidian-integration). So regression notes must be **in Ingest** (or copied there) for the three-run procedure to apply.

## Goal

1. Make the **PARA regression suite runnable**: real or fixture notes + filled table in para-regression.md.
2. Make the **Regression-Stability-Log baseline** actionable: clear procedure to run, then fill the first row (and document rubric version).
3. (Optional) Add **test coverage by responsibility** in Testing.md per System-Audit-Report.

**Must-add for completeness (per docs):** (1) **Fixture coverage for rubric edges** — at least 1–2 edge-case fixtures (multi-topic / tie-breaker) so "notes with flips" is representative (PARA-Actionability-Rubric § Tie-breaker). (2) **Ingest reset** — step 1.5 in procedure: clear or archive prior Decision Wrappers from Ingest/Decisions/ (snapshot first) to avoid false stability from re-processing (Pipelines Phase 1 non-destructiveness). (3) **Rubric version lock** — step 7: explicitly reference current PARA-Actionability-Rubric.md version in the log row; ties baselines to rubric changes ("Add a new row for each intentional change").

---

## 1. PARA regression fixtures and table

**Fixture notes under tests, copy into Ingest for runs**

- Create **5–10** simple fixture notes in `3-Resources/Second-Brain/tests/fixtures/para-regression/`. Keep each **100–300 words** to mimic ingest inputs. Naming and examples per rubric (PARA-Actionability-Rubric v1.0):
  - **Project**: `ingest-project-fixture.md` — e.g. "Launch new app by 2026-04-01: features A/B, deadline critical." → Golden: `1-Projects/App-Launch/...`
  - **Area**: `ingest-area-fixture.md` — e.g. "Ongoing fitness routine: track workouts, no end date." → Golden: `2-Areas/Health/...`
  - **Resource**: `ingest-resource-fixture.md` — e.g. "CSS grid cheat sheet: patterns and examples." → Golden: `3-Resources/CSS/...`
  - **Archive**: `ingest-archive-fixture.md` — e.g. "Completed tax filing from 2025." → Golden: `4-Archives/Taxes/...`
  - **Edge/Ambiguous**: `ingest-ambiguous-fixture.md` — e.g. "Research on PKM tools" (may flip Resources/Areas; tests tie-breaker).
- **Must-add: 1–2 rubric edge-case fixtures** (per Regression-Stability-Log flip-rate target). Include at least one **multi-topic note** that triggers the tie-breaker (Projects > Areas > Resources > Archives) so "notes with flips" in the log table is representative, not artificially zero. Evidence: [PARA-Actionability-Rubric](3-Resources/Second-Brain/PARA-Actionability-Rubric.md) § Tie-breaker. Extensibility: makes future runs representative without extra effort.
- **Extensibility**: Start with 5; add more for coverage (e.g. multi-topic notes for max_candidates=7 padding per MCP-Tools → obsidian_propose_para_paths).
- Copy fixtures to **Ingest/** before each run (manual `cp` or agent phrase "Prep regression ingest"; optional Commander macro per Plugins.md).
- In [para-regression.md](3-Resources/Second-Brain/tests/para-regression.md):
  - Document: "For a regression run, copy `tests/fixtures/para-regression/*.md` into `Ingest/` (e.g. `Ingest/ingest-project-fixture.md`); then list those paths in the table below."
  - **Fill the table** with columns: `note_path` (e.g. `Ingest/ingest-project-fixture.md`), `content_snippet`, `golden_top_path` (e.g. `1-Projects/App-Launch/2026-03-06-app-launch-plan.md`), `acceptable_alts`, `notes` (e.g. "High actionability: deadline-bound.").

---

## 2. Regression-Stability-Log baseline procedure and row

- In [Regression-Stability-Log.md](3-Resources/Second-Brain/Regression-Stability-Log.md), add a **"Baseline Run Procedure"** subsection (after "How to compute flip rate") with these steps (markdown for easy agent updates):
  1. **Pin MCP params** — e.g. via prompt-crafter: ingest + default profile (per Prompt-Crafter-Structure-Detailed.md).
  1.5. **Clear or archive prior Decision Wrappers** from `Ingest/Decisions/` (per mcp-obsidian-integration: **snapshot first**). Prevents false stability from re-processing cached/prior artifacts; Phase 1 is non-destructive but repeated runs on the same Ingest/ notes can loop or reuse wrappers (Pipelines.md).
  1. **Copy fixtures** from `tests/fixtures/para-regression/` to `Ingest/`. Clear Ingest first if needed; take snapshot per mcp-obsidian-integration.
  2. **Run INGEST MODE (Phase 1)** on the regression notes **three times** independently (clear mid-run state if needed; non-destructive until EAT-QUEUE per Pipelines).
  3. **Per note/run**: Extract `top_path` from Decision Wrapper (option A or top candidate from `obsidian_propose_para_paths`).
  4. **Compute flip rate**: Notes with >1 unique `top_path` across the three runs / total notes (%).
  5. **Avg confidence**: Mean of `ingest_conf` or top candidate score across all notes.
  6. **Fill table row**: Date, **Rubric version** (reference the current [PARA-Actionability-Rubric.md](3-Resources/Second-Brain/PARA-Actionability-Rubric.md) version in the row—e.g. v1.0), Flip rate %, Notes with flips (count or list), Avg conf %, Notes (e.g. "Baseline after fixtures"). Ties baselines to rubric changes; per the log: "Add a new row for each intentional change" to PARA-related descriptors.
- **Expectations**: First run may show ~10–20% flip if MCP temp/top_p not zeroed (tunable per Parameters.md). Log issues (e.g. "Flips on ambiguous due to rubric tie-breaker"). If flips >15%, tweak MCP descriptors to reference rubric more explicitly (Backbone → stabilize via pinned params).
- Keep existing table; first row TODO with Notes: "First baseline pending; run procedure above and replace TODO values."

---

## 3. Optional: Test coverage by responsibility

- In [Testing.md](3-Resources/Second-Brain/Testing.md), add subsection **"Test coverage by responsibility"** (after "What is covered"). Map from [Responsibilities-Breakdown](3-Resources/Second-Brain/Responsibilities-Breakdown.md). Example table format:
  - **Responsibility** (from Responsibilities-Breakdown) | **Coverage** | **Notes**
  - Pipelines: full-autonomous-ingest (Phase 1 wrapper) → Integration: test_pipeline_flow.py — Asserts chain order, no move.
  - Rules: mcp-obsidian-integration (backup gate) → Unit: test_safety_invariants.py — Mocks ensure_backup.
  - Skills: classify_para → Contract/fixtures — Fixture input → expected candidates.
  - Gaps → Stub: e.g. "TODO: Mobile async preview integration."
  Pull from existing tests (e.g. queue in unit/test_queue.py). Low priority; unit/integration already cover contracts.

---

## 4. Files to touch


| File                                                       | Action                                                                                                                                                                                                         |
| ---------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `3-Resources/Second-Brain/tests/fixtures/para-regression/` | **Create** 5–10 fixture `.md` notes (100–300 words): core 5 + **1–2 edge-case** (multi-topic / tie-breaker per Rubric § Tie-breaker); ingest-project, -area, -resource, -archive, -ambiguous, + edge fixtures. |
| `3-Resources/Second-Brain/tests/fixtures/README.md`        | Add line: `para-regression/` — minimal notes for PARA regression; copy to `Ingest/` before running regression.                                                                                                 |
| `3-Resources/Second-Brain/tests/para-regression.md`        | Add "How to run" (copy fixtures to Ingest); **fill** table with note_path (e.g. `Ingest/ingest-project-fixture.md`), golden_top_path, content_snippet, acceptable_alts, notes.                                 |
| `3-Resources/Second-Brain/Regression-Stability-Log.md`     | Add **"Baseline Run Procedure"** (7 steps: pin params, copy fixtures, run 3x, extract top_path, compute flip rate, avg conf, fill row); keep first row TODO with note.                                         |
| `3-Resources/Second-Brain/Testing.md`                      | Optional: add **"Test coverage by responsibility"** subsection with table mapping Responsibilities-Breakdown → tests.                                                                                          |


---

## 5. Out of scope (no code/automation)

- **No script** to run the three ingest passes or aggregate flip rate: the procedure remains human/agent-driven (INGEST MODE three times, then manual or agent fill of the log row).
- **No change** to run_tests.py or Python tests: they already cover unit/integration contracts; PARA regression is a separate, MCP/ingest-based procedure documented in Regression-Stability-Log and para-regression.

---

## Summary and next actions

- **Runnable regression**: Add 5–10 fixtures (including **1–2 edge-case** for tie-breaker / flip-rate representativeness) and fill [para-regression.md](3-Resources/Second-Brain/tests/para-regression.md) with paths (after copy to Ingest) and golden_top_path + notes.
- **Actionable baseline**: Add "Baseline Run Procedure" (7 steps) in [Regression-Stability-Log.md](3-Resources/Second-Brain/Regression-Stability-Log.md); first row remains TODO until first run; target **flip rate <10%** (re-run after any rubric/MCP tweak to track stability).
- **Optional**: "Test coverage by responsibility" in [Testing.md](3-Resources/Second-Brain/Testing.md) (table mapping to Responsibilities-Breakdown).
- **Effort**: ~30–60 min (write fixtures, fill table, run 3x INGEST MODE, compute and fill log).
- **If stuck**: If MCP proposals vary wildly, use strict-para `context_mode` via queue params (Queue-Sources.md). Add automation only if you run this weekly; keeping it human-driven avoids brittle scripts.

