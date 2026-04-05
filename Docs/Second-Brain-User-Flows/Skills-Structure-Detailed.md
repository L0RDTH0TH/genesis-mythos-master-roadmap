---
title: Skills Structure — Detailed
created: 2026-03-05
tags: [pkm, second-brain, architecture, skills, diagram, level-3]
para-type: Resource
status: active
links: ["[[Resources Hub]]", "[[3-Resources/Second-Brain/README]]"]
---

# Skills Structure — Detailed

This document is the full breakdown: skill-by-skill sequence for ingest, distill, archive, express, and organize (including every listed skill and slot from Cursor-Skill-Pipelines-Reference), exact MCP tool order and params (dry_run pattern, ensure_structure, calibrate_confidence), confidence-band logic with loop_* fields, every documented snapshot trigger, queue dispatch to skill invocation, highlight-flow integration, and error/fallback paths from mcp-obsidian-integration. No steps are invented; all chains match the canonical docs.

---

## Ingest: full skill and MCP sequence (Phase 1)

```mermaid
flowchart LR
  subgraph Bootstrap [Bootstrap]
    L[list_notes Ingest]
    LP[list_projects]
    BP[bootstrap_project_batch optional]
  end
  subgraph Backup [Backup]
    CB[create_backup]
  end
  subgraph Classify [Classify]
    CP[classify_para]
  end
  subgraph Skills1 [Skills]
    FE[frontmatter-enrich]
    NE[name-enhance propose only]
    SO[subfolder-organize]
  end
  subgraph Mid [Mid-band optional]
    SFO[obsidian_subfolder_organize max_candidates]
    CAL[calibrate_confidence]
    VER[verify_classification]
  end
  subgraph Content [Content]
    SA[split_atomic]
    SLP[split_link_preserve]
    DN[distill_note]
    DHC[distill_highlight_color]
    NAE[next_action_extract]
    TR[task_reroute when ≥78% task-like]
  end
  subgraph Hub [Hub]
    MF[manage_frontmatter / manage_tags]
    AH[append_to_hub]
  end
  subgraph Wrapper [Wrapper]
    PP[propose_para_paths context_mode: wrapper max_candidates: 7]
    DW[Create/refresh Decision Wrapper A–G]
  end
  subgraph Log [Log]
    LA[log_action]
  end
  L --> LP --> BP --> CB --> CP --> FE --> NE --> SO
  SO --> Mid
  Mid --> SA --> SLP --> DN --> DHC --> NAE --> TR --> MF --> AH --> PP --> DW --> LA
```

Phase 1: no move_note. Guidance-aware: pass user_guidance (or queue prompt) to classify_para, subfolder-organize, name-enhance, distill_note, split_atomic.

---

## Ingest: snapshot triggers (per Cursor-Skill-Pipelines-Reference)

```mermaid
flowchart TD
  subgraph Triggers [Per-change snapshot before]
    T1[split_atomic]
    T2[distill_note when rewriting]
    T3[append_to_hub]
    T4[task-reroute: snapshot target note before append_tasks]
    T5[move_note Phase 2 only]
    T6[rename_note Phase 2 only]
  end
  subgraph Batch [Batch]
    B1[Every 5 notes]
  end
  Triggers --> Obs[obsidian-snapshot skill type: per-change]
  Batch --> BatchDir[BATCH_SNAPSHOT_DIR when batch &gt; batch_size_for_snapshot]
```

name-enhance in ingest proposes only; subfolder-organize commits name via move in Phase 2.

---

## Distill: full skill sequence with highlight flow

```mermaid
flowchart LR
  A[create_backup]
  B[auto-layer-select when enabled read distill_lens]
  C[optional mid-band depth loop]
  D[distill layers]
  E[distill-highlight-color]
  F[highlight-perspective-layer optional]
  G[layer-promote]
  H[distill-perspective-refine]
  I[callout-tldr-wrap]
  J[readability-flag]
  A --> B --> C --> D --> E --> F --> G --> H --> I --> J
```

Distill snapshot triggers: before first structural rewrite (distill layers, highlight-perspective-layer, layer-promote, distill-perspective-refine, heavy update_note). Batch: ~every 3 notes.

---

## Archive: full sequence with move flow

```mermaid
flowchart LR
  A[create_backup]
  B[classify_para]
  C[archive-check]
  D[optional mid-band: calibrate_confidence → verify_classification → move_note dry_run → commit after snapshot]
  E[subfolder-organize]
  F[resurface-candidate-mark]
  G[summary-preserve]
  H[ensure_structure folder_path: parent of target]
  I[move_note dry_run: true]
  J[review effects]
  K[move_note dry_run: false]
  L[log_action]
  A --> B --> C --> D --> E --> F --> G --> H --> I --> J --> K --> L
```

Archive snapshot: after archive-check ≥85% but before subfolder-organize, summary-preserve, move. Batch: once per archive sweep.

---

## Express: full sequence with version-snapshot

```mermaid
flowchart LR
  A[create_backup]
  B[version-snapshot obsidian_update_note mode: create Versions/ slug--timestamp]
  C[related-content-pull or obsidian_suggest_connections]
  D[optional mid-band soft express loop]
  E[express-mini-outline]
  F[express-view-layer when express_view set]
  G[optional obsidian_append_to_moc / obsidian_generate_moc]
  H[call-to-action-append]
  A --> B --> C --> D --> E --> F --> G --> H
```

Express snapshot: before large appends (related-content-pull, express-mini-outline, express-view-layer, call-to-action-append); alongside version-snapshot. Batch: optional per batch.

---

## Organize: full sequence with rename optional

```mermaid
flowchart LR
  A[create_backup]
  B[classify_para]
  C[frontmatter-enrich]
  D[subfolder-organize or obsidian_subfolder_organize 2–3 candidates mid-band]
  E[optional mid-band: calibrate_confidence → verify_classification → move_note dry_run → commit]
  F[name-enhance context organize]
  G[obsidian_rename_note when name-enhance applies snapshot before rename]
  H[ensure_structure folder_path: parent of target]
  I[move_note dry_run: true]
  J[move_note dry_run: false]
  K[log_action]
  A --> B --> C --> D --> E --> F --> G --> H --> I --> J --> K
```

Organize snapshot: before obsidian_rename_note (when name-enhance applies) and before obsidian_move_note when confidence ≥85%. Batch: ~every 3 notes.

---

## MCP move pattern (exact order and params)

```mermaid
flowchart TD
  Ready[Path computed; confidence ≥85%]
  Ready --> Snap[obsidian-snapshot per-change for note]
  Snap --> ES[obsidian_ensure_structure folder_path: parent directory of new_path]
  ES --> Dry[obsidian_move_note path, new_path, dry_run: true]
  Dry --> Rev[Review: path, new_path, backup status, risks e.g. dangling links]
  Rev --> OK{dry_run acceptable?}
  OK -->|Yes| Com[obsidian_move_note path, new_path, dry_run: false]
  OK -->|No| Fall[propose_alternative_paths → calibrate_confidence → verify_classification]
  Fall --> Dry
```

Documented in mcp-obsidian-integration. ensure_structure creates full path recursively with folder_path; move_note does not create parents.

---

## Mid-band fallback chain (move failure or dry_run risk)

```mermaid
flowchart LR
  Fail[move_note fails or dry_run reports high risk]
  Fail --> PA[propose_alternative_paths propose_para_paths context_mode: fallback]
  PA --> Cal[calibrate_confidence prior_output: classification + path]
  Cal --> Ver[verify_classification note_path, calibrated_output]
  Ver --> Dry[obsidian_move_note dry_run: true again]
  Dry --> Commit{Acceptable?}
  Commit -->|Yes| Com[move_note dry_run: false]
  Commit -->|No| Log[Append dry_run output + error to log with #review-needed; pause note]
```

Same chain for ingest, organize, archive; do not duplicate per pipeline (mcp-obsidian-integration).

---

## Confidence band logic with loop_* (all pipelines)

```mermaid
flowchart TD
  Sig[Primary signal: ingest_conf / path_conf / archive_conf / express_conf / distill_conf]
  Sig --> High{≥85%?}
  Sig --> Mid{68–84%?}
  Sig --> Low{&lt;68%?}
  High --> Snap[Per-change snapshot]
  Snap --> Do[Execute destructive steps]
  Mid --> Pre[Store pre_loop_conf]
  Pre --> Loop[Single non-destructive loop]
  Loop --> MCP[Subfolder candidates / calibrate / verify / preview]
  MCP --> Post[Compute post_loop_conf]
  Post --> Fields[Write loop_attempted: true, loop_band: 68-84, pre_loop_conf, post_loop_conf, loop_outcome, loop_type, loop_reason]
  Post --> Check{post_loop_conf ≥85% and &gt; pre_loop_conf?}
  Check -->|Yes| Snap
  Check -->|No| NoAct[No destructive action; log #review-needed]
  Low --> NoAct
```

Decay rule: if post_loop_conf ≤ pre_loop_conf, fall back to user decision; no destructive action (confidence-loops).

---

## Snapshot triggers table (all pipelines)

```mermaid
flowchart TB
  subgraph Ingest [full-autonomous-ingest]
    I1[Before split_atomic]
    I2[Before distill_note when rewriting]
    I3[Before append_to_hub]
    I4[Before task-reroute target note]
    I5[Before move_note Phase 2]
    I6[Before rename_note Phase 2]
  end
  subgraph Distill [autonomous-distill]
    D1[Before distill layers / highlight-perspective-layer / layer-promote / distill-perspective-refine / heavy update_note]
  end
  subgraph Archive [autonomous-archive]
    A1[After archive-check ≥85% before subfolder-organize / summary-preserve / move]
  end
  subgraph Express [autonomous-express]
    E1[Before related-content-pull / express-mini-outline / express-view-layer / call-to-action-append]
  end
  subgraph Organize [autonomous-organize]
    O1[Before obsidian_rename_note when name-enhance applies]
    O2[Before obsidian_move_note]
  end
  Ingest --> Obs[obsidian-snapshot type: per-change]
  Distill --> Obs
  Archive --> Obs
  Express --> Obs
  Organize --> Obs
```

All require confidence ≥85% for the underlying action; else skip snapshot and destructive step, log #review-needed.

---

## Queue dispatch → pipeline → skills

```mermaid
flowchart TD
  Q[EAT-QUEUE reads prompt-queue.jsonl or Task-Queue.md]
  Q --> Step0[Step 0: approved wrappers / re-wrap]
  Step0 --> Mode[Dispatch by mode]
  Mode --> ING[INGEST MODE → full-autonomous-ingest]
  Mode --> DIST[DISTILL MODE → autonomous-distill]
  Mode --> ARCH[ARCHIVE MODE → autonomous-archive]
  Mode --> EXPR[EXPRESS MODE → autonomous-express]
  Mode --> ORG[ORGANIZE MODE → autonomous-organize]
  Mode --> TASK[TASK-COMPLETE etc. → task-complete-validate / add-roadmap-append / expand-road-assist]
  ING --> IngestSkills[Ingest skill chain]
  DIST --> DistillSkills[Distill skill chain]
  ARCH --> ArchiveSkills[Archive skill chain]
  EXPR --> ExpressSkills[Express skill chain]
  ORG --> OrganizeSkills[Organize skill chain]
  TASK --> TaskSkills[Task/roadmap skills]
```

feedback-incorporate at start or re-run: load user_guidance / approved_path for guidance-aware runs.

---

## Highlight flow integration (distill and ingest)

```mermaid
flowchart LR
  subgraph Triggers [Triggers / config]
    T1[distill_lens frontmatter]
    T2[highlight_perspective]
    T3[Second-Brain-Config coverage 50–70%]
  end
  subgraph Ingest [Ingest]
    I1[distill_note]
    I2[distill-highlight-color]
  end
  subgraph Distill [Distill]
    D1[distill-highlight-color]
    D2[highlight-perspective-layer]
    D3[layer-promote]
  end
  T1 --> D1
  T2 --> D1
  T3 --> D1
  I1 --> I2
  D1 --> D2 --> D3
  D2 --> Log[Distill-Log: drift levels, highlight_angles]
```

Skills.md: distill-highlight-color after distill_note (ingest) or after distill layers (distill); highlight-perspective-layer after distill-highlight-color; layer-promote after highlight-perspective-layer or distill-highlight-color.

---

## ensure_structure before move (exact param)

```mermaid
flowchart TD
  NewPath[new_path from subfolder_organize or approved_path]
  NewPath --> Parent[Parent directory of new_path]
  Parent --> ES[obsidian_ensure_structure folder_path: parent]
  ES --> Create[Server creates path recursively os.makedirs exist_ok]
  Create --> Move[move_note path, new_path]
```

folder_path = parent directory of new_path (e.g. 4-Archives/Project-X-Archive/Subtheme). Without folder_path, only top-level PARA created. Documented mcp-obsidian-integration.

---

## Error handling path (all pipelines)

```mermaid
flowchart TD
  Err[Pipeline or MCP error]
  Err --> Trace[Capture: timestamp, pipeline, stage, note path, raw error sanitized]
  Trace --> Summary[Summarize: error_type, root_cause, impact, suggested_fixes, recovery]
  Summary --> Entry[Append one entry to 3-Resources/Errors.md]
  Entry --> Format[Heading: ### YYYY-MM-DD HH:MM — Title]
  Format --> Meta[Metadata table: pipeline, severity, approval, timestamp, error_type]
  Meta --> TraceSec[#### Trace]
  Meta --> SumSec[#### Summary: Root cause, Impact, Suggested fixes, Recovery]
  Err --> Ref[One-line reference in pipeline log]
  Err --> High{High severity or critical?}
  High -->|Yes| Flag[#review-needed; approval: pending; pause destructive for this note]
  High -->|No| Continue[Continue batch with next note]
```

create_backup failure: abort pipeline for that note. Snapshot failure before destructive: skip destructive step, log Backup-Log with #review-needed.

---

## Backup gate (ensure_backup vs create_backup)

```mermaid
flowchart TD
  Before[Before long batch or after gap]
  Before --> EB[obsidian_ensure_backup path, max_age_minutes]
  EB --> Fresh{Recent backup exists?}
  Fresh -->|Yes| Use[Use existing; no create_backup]
  Fresh -->|No| CB[obsidian_create_backup]
  CB --> Proceed[Proceed with destructive steps]
  Use --> Proceed
```

ensure_backup(max_age_minutes e.g. 1440); only call create_backup when ensure_backup indicates needed. Every ingest starts with backup; destructive MCP uses internal ensure_backup gate.
