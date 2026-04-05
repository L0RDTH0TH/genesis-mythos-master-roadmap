---
title: Audit Context vs Pipeline Focus
created: 2026-04-05
tags: [audit, context, sandbox-genesis-mythos-master, queue]
para-type: Resource
status: active
source: "[[1-Projects/sandbox-genesis-mythos-master/Roadmap/workflow_state]] — AUDIT_CONTEXT queue entry gitforge-push-test-default-lane-202604041200000Z"
---

# Audit Context vs Pipeline Focus

**Project:** `sandbox-genesis-mythos-master`  
**Trigger:** Queue mode `AUDIT_CONTEXT` (EAT-QUEUE lane `default`, 2026-04-05).

## Workflow state (context)

| Source | Metric | Value |
|--------|--------|-------|
| Frontmatter | `last_ctx_util_pct` | 84 |
| Frontmatter | `last_injected_tokens` | 118000 |
| Frontmatter | `current_phase` / `current_subphase_index` | 6 / `"6.1"` |
| Last ## Log row (2026-04-05 15:05) | Ctx Util % | 84 |
| Last ## Log row | Est. Tokens / Window | 118000 / 128000 |
| Last ## Log row | Target | Phase 6 primary checklist complete → next mint **6.1** |

## Pipeline logs (Distill / Express)

Recent **Distill-Log** and **Express-Log** entries are dominated by **Test-Project** and **Genesis-Mythos** research notes; **no** lines in the sampled logs reference `sandbox-genesis-mythos-master` or `1-Projects/sandbox-genesis-mythos-master/` paths.

## Overlap heuristic

| Signal | Assessment |
|--------|------------|
| Topic / path overlap (workflow log vs Distill/Express) | **Low** — roadmap work is not mirrored in distill/express logs for this project in the visible window. |
| Context pressure vs roadmap depth | **High utilization** (84% ctx, ~118k/128k tokens) aligns with Phase **5→6** advance and Phase **6** primary deepen in workflow_state; pipelines are **not** the relief valve for that pressure in logs. |

## Verdict

**Context-heavy roadmap track; pipeline logs show no concurrent distill/express focus on this project** — expect **low measured overlap** until explicit DISTILL/EXPRESS runs target sandbox GMM roadmap or PMG notes. **No drift signal** between workflow_state and logs; **observability gap** only (pipelines not exercised on same artifacts).
