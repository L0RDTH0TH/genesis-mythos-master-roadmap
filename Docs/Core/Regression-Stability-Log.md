---
title: Regression Stability Log
created: 2026-03-06
tags: [pkm, second-brain, testing, para, regression]
para-type: Resource
status: active
links: ["[[3-Resources/Second-Brain/Testing]]", "[[3-Resources/Second-Brain/PARA-Actionability-Rubric]]"]
---

# Regression Stability Log

Track **ingest PARA stability** over time using a simple flip-rate metric on the PARA regression suite.

## How to compute flip rate

For each test run:

1. Ensure MCP config (temperature, top_p, descriptors) is in the desired state.
2. Run ingest Phase 1 on all notes listed in [[3-Resources/Second-Brain/tests/para-regression|para-regression]] **three times** with identical settings.
3. For each note, record the set of unique `top_path` values that appear as the **top-ranked** Decision Wrapper option (or top candidate from `propose_para_paths`).
4. Define:
   - **Flip count** = number of notes that showed **more than one** unique `top_path` across the three runs.
   - **Flip rate** = `flip_count / total_notes` (expressed as a %).
5. Optionally compute **average confidence** (e.g. mean of top candidate score or `ingest_conf`) across all notes.

Target after hardening: **flip rate < 15%**, ideally **< 5–10%**.

**Research-injected deepens (roadmap):** After smoke-testing RESUME-ROADMAP with `enable_research: true`, verify in this log that **research-injected deepens do not flip PARA paths > 5%** more than non-research runs. Use baseline from current logs (recent non-research deepen/ingest path outcomes); compare path changes for notes touched in research vs non-research runs. See Research agent roadmap integration plan §10.

## Baseline Run Procedure

Follow these steps to establish or update a baseline row (see [[3-Resources/Second-Brain/tests/para-regression|para-regression]] and [[3-Resources/Second-Brain/Testing|Testing]]):

1. **Pin MCP params** — e.g. via prompt-crafter: ingest + default profile (per Prompt-Crafter-Structure-Detailed.md).
1.5. **Clear or archive prior Decision Wrappers** from `Ingest/Decisions/` (per mcp-obsidian-integration: **snapshot first**). Prevents false stability from re-processing cached/prior artifacts; Phase 1 is non-destructive but repeated runs on the same Ingest/ notes can loop or reuse wrappers (Pipelines.md).
2. **Copy fixtures** from `tests/fixtures/para-regression/` to `Ingest/`. Clear Ingest first if needed; take snapshot per mcp-obsidian-integration.
3. **Run INGEST MODE (Phase 1)** on the regression notes **three times** independently (clear mid-run state if needed; non-destructive until EAT-QUEUE per Pipelines).
4. **Per note/run**: Extract `top_path` from Decision Wrapper (option A or top candidate from `propose_para_paths`).
5. **Compute flip rate**: Notes with >1 unique `top_path` across the three runs / total notes (%).
6. **Avg confidence**: Mean of `ingest_conf` or top candidate score across all notes.
7. **Fill table row**: Date, **Rubric version** (reference the current [[3-Resources/Second-Brain/PARA-Actionability-Rubric|PARA-Actionability-Rubric]] version in the row—e.g. v1.0), Flip rate %, Notes with flips (count or list), Avg conf %, Notes (e.g. "Baseline after fixtures"). Ties baselines to rubric changes; per the log: "Add a new row for each intentional change" to PARA-related descriptors.

## Runs

| Date | Rubric version | Flip rate | Notes with flips | Avg confidence | Notes |
|------|----------------|----------:|------------------|----------------|-------|
| TODO | v1.0           |   TODO %  | TODO/NN          | TODO %         | First baseline pending; run procedure above and replace TODO values. |

Add a new row for each intentional change to PARA-related descriptors, sampling parameters, or ingest/organize rules.

## Hand-off readiness (roadmap)

**handoff_flip_rate**: When hand-off-audit is run on phase traces (fixtures in `tests/fixtures/handoff-regression/`), the % of phases that change band (e.g. high→mid, mid→low) across runs or after heuristic/config changes. Baseline row (optional): run audit on sample phase traces, record band distribution; add row when first baseline is established.

| Date | handoff_flip_rate | Notes |
|------|-------------------|------|
| —    | —                 | Baseline pending; run hand-off-audit on handoff-regression fixtures and fill. |

## Roadmap util stability (context utilization 80% integration)

When running roadmap deepen with **inject_extra_state**, **token_cap**, and high-util params (e.g. DEEPEN-AGGRESSIVE), track:

- **avg_util_flip_rate**: % of runs where Ctx Util % swung **>15%** run-over-run (util_delta > 15). Record **average Ctx Util %** per run and flip count.
- **Limit-pushing**: Run PARA regression at **70% util sim** (mock context at 70% full); baseline **drift_score**; ensure drift remains below 0.08 or document acceptable delta. See Testing § High-util roadmap fixtures.

| Date | Avg Ctx Util % | avg_util_flip_rate | Drift (70% sim) | Notes |
|------|----------------|--------------------|-----------------|-------|
| —    | —              | —                  | —               | Baseline pending; run high-util fixtures and 70% util sim. |

