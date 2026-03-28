---
title: PARA Regression Suite
created: 2026-03-06
tags: [pkm, second-brain, testing, para]
para-type: Resource
status: active
links: ["[[3-Resources/Second-Brain/Testing]]", "[[3-Resources/Second-Brain/PARA-Actionability-Rubric]]"]
---

# PARA Regression Suite

Small, hand-curated regression set for **PARA classification and path proposals**.  
Use these notes to sanity-check `obsidian_classify_para` and `propose_para_paths` after changes to descriptors, sampling parameters, or ingest rules.

## How to run a regression

For a regression run, **copy** `tests/fixtures/para-regression/*.md` into `Ingest/` (e.g. so they appear as `Ingest/ingest-project-fixture.md`, etc.). Then run INGEST MODE (Phase 1) on only those notes, and list their paths in the table below. See [[3-Resources/Second-Brain/Regression-Stability-Log|Regression-Stability-Log]] for the full baseline procedure (including clearing prior Decision Wrappers and running three times for flip rate).

## How to use this file

1. Ensure regression notes are in `Ingest/` (copy from fixtures as above).
2. The table lists `note_path` (vault-relative, under Ingest/ when testing), `content_snippet`, `golden_top_path` (expected top wrapper option), `acceptable_alts`, and `notes`.
3. After a change to PARA-related descriptors or sampling params, run ingest on all listed notes 2–3 times (or three for flip-rate) and compare the wrappers’ A–G options against `golden_top_path` / `acceptable_alts`.

## Regression notes

| note_path | content_snippet | golden_top_path | acceptable_alts | notes |
|-----------|-----------------|-----------------|-----------------|-------|
| Ingest/ingest-project-fixture.md | "Launch new app by 2026-04-01: features A/B, deadline critical." | 1-Projects/App-Launch/ | — | High actionability: deadline-bound project. |
| Ingest/ingest-area-fixture.md | "Ongoing fitness routine: track workouts, no end date." | 2-Areas/Health-and-Fitness/ | 1-Projects/Fitness-Challenge-2026-Q1 | Area: ongoing responsibility, no fixed end. |
| Ingest/ingest-resource-fixture.md | "CSS grid cheat sheet: patterns and examples." | 3-Resources/CSS/ | — | Pure reference; should not become Project/Area. |
| Ingest/ingest-archive-fixture.md | "Completed tax filing from 2025." | 4-Archives/Taxes/ | 3-Resources/OKR-Process | Completed archive vs reusable process. |
| Ingest/ingest-ambiguous-fixture.md | "Research on PKM tools" | 2-Areas/Knowledge-Management/ or 3-Resources/PKM/ | 3-Resources/PKM/, 2-Areas/ | May flip Resources/Areas; tests tie-breaker. |
| Ingest/ingest-edge-multitopic-fixture.md | "Q1 goals + CSS reference" (deadline + reference) | 1-Projects/Dashboard-Q1/ or 1-Projects/Goals-Q1/ | 3-Resources/CSS/ | Multi-topic; tie-breaker Projects > Resources. |
| Ingest/ingest-edge-finance-area-project-fixture.md | "Tax prep by Apr 15; ongoing budget tracking" | 1-Projects/Tax-2026/ | 2-Areas/Finances/ | Project vs Area blend; tie-breaker Projects > Areas. |

Add more rows as needed; keep the total small and high-signal.

