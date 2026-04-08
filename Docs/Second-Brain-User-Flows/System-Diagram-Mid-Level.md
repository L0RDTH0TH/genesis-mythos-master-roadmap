---
title: Second Brain System Diagram — Mid-Level
created: 2026-03-05
tags: [pkm, second-brain, diagram, level-2]
para-type: Resource
status: active
links: ["[[Resources Hub]]", "[[3-Resources/Second-Brain/README]]"]
---

# Second Brain System Diagram — Mid-Level

This document builds on the high-level diagram by adding pipeline mappings (trigger → pipeline from Pipelines.md), rule types (always vs context), skill groups by pipeline (from Skills.md), MCP tool groups (from MCP-Tools.md), queue branches (prompt-queue.jsonl vs Task-Queue.md from Queue-Sources.md), and basic flows such as the ingest skill chain and confidence-band decisions. It also includes the vault folder tree and exclusions. Use it to see how rules, skills, and tools group by pipeline and how queues branch.

---

## Trigger → rule → pipeline mapping

```mermaid
flowchart TD
  Input[Instruction or open file]
  Input --> Glob{Glob match?}
  Glob -->|Ingest/*.md| Ingest[para-zettel-autopilot]
  Glob -->|No| Phrase{Phrase match?}
  Phrase -->|EAT-QUEUE| Queue[auto-eat-queue]
  Phrase -->|PROCESS TASK QUEUE| TaskQ[auto-queue-processor]
  Phrase -->|DISTILL MODE| Distill[auto-distill]
  Phrase -->|ARCHIVE MODE| Archive[auto-archive]
  Phrase -->|EXPRESS MODE| Express[auto-express]
  Phrase -->|ORGANIZE MODE| Organize[auto-organize]
  Phrase -->|No match| Other[Other rules or none]
  Ingest --> fullIngest[full-autonomous-ingest]
  Queue --> queueProc[Queue processor]
  TaskQ --> taskQueue[Task queue]
  Distill --> autoDistill[autonomous-distill]
  Archive --> autoArchive[autonomous-archive]
  Express --> autoExpress[autonomous-express]
  Organize --> autoOrganize[autonomous-organize]
```

Context rules fire on phrase or glob; always rules (e.g. always-ingest-bootstrap, mcp-obsidian-integration) apply every run.

---

## Rule types: always vs context

```mermaid
flowchart LR
  subgraph Always [Always applied]
    A1[00-always-core]
    A2[mcp-obsidian-integration]
    A3[second-brain-standards]
    A4[confidence-loops]
    A5[guidance-aware]
    A6[always-ingest-bootstrap]
    A7[watcher-result-append]
    A8[backbone-docs-sync]
  end
  subgraph Context [Context triggered]
    C1[para-zettel-autopilot]
    C2[auto-eat-queue]
    C3[auto-distill / auto-archive / auto-express / auto-organize]
    C4[ingest-processing / non-markdown-handling]
    C5[auto-highlight-perspective / mobile-seed-detect]
  end
  Always --> Pipelines[Pipeline selection]
  Context --> Pipelines
```

Always rules define persona, backup/snapshot/dry_run, PARA standards, confidence bands, and Watcher-Result contract. Context rules map triggers to pipelines (ingest, queue, distill, archive, express, organize).

---

## Skills by pipeline

```mermaid
flowchart TB
  subgraph Ingest [Ingest]
    I1[frontmatter-enrich]
    I2[name-enhance]
    I3[subfolder-organize]
    I4[split-link-preserve]
    I5[distill-highlight-color]
    I6[next-action-extract]
    I7[task-reroute]
  end
  subgraph Distill [Distill]
    D1[auto-layer-select]
    D2[distill-highlight-color]
    D3[highlight-perspective-layer]
    D4[layer-promote]
    D5[callout-tldr-wrap]
    D6[readability-flag]
  end
  subgraph Archive [Archive]
    A1[archive-check]
    A2[subfolder-organize]
    A3[resurface-candidate-mark]
    A4[summary-preserve]
  end
  subgraph Express [Express]
    E1[version-snapshot]
    E2[related-content-pull]
    E3[express-mini-outline]
    E4[call-to-action-append]
  end
  subgraph Organize [Organize]
    O1[frontmatter-enrich]
    O2[subfolder-organize]
    O3[name-enhance]
  end
```

Skills are chained in order per Cursor-Skill-Pipelines-Reference; shared skills (e.g. frontmatter-enrich, subfolder-organize) appear in multiple pipelines with pipeline-specific slots.

---

## MCP tool groups

```mermaid
flowchart TB
  subgraph Core [Core]
    read_note[read_note]
    update_note[update_note]
    list_notes[list_notes]
    manage_frontmatter[manage_frontmatter]
  end
  subgraph Backup [Backup]
    create_backup[create_backup]
    ensure_backup[ensure_backup]
  end
  subgraph Move [Move/structure]
    move_note[move_note]
    rename_note[rename_note]
    ensure_structure[ensure_structure]
  end
  subgraph PARA [PARA/organize]
    classify_para[classify_para]
    subfolder_organize[subfolder_organize]
    propose_para_paths[propose_para_paths]
  end
  subgraph Content [Content]
    split_atomic[split_atomic]
    distill_note[distill_note]
    append_to_hub[append_to_hub]
  end
  subgraph Confidence [Confidence]
    calibrate_confidence[calibrate_confidence]
    verify_classification[verify_classification]
    propose_alternative_paths[propose_alternative_paths]
  end
  subgraph Other [Other]
    log_action[log_action]
  end
```

Server: obsidian-para-zettel-autopilot. move_note uses dry_run then commit; ensure_structure creates target parent before move.

---

## Queue branches: prompt-queue vs Task-Queue

```mermaid
flowchart LR
  subgraph Entry1 [prompt-queue.jsonl]
    E1[Watcher / EAT-QUEUE]
    M1[INGEST, ORGANIZE, TASK-ROADMAP, DISTILL, EXPRESS, ARCHIVE, TASK-COMPLETE, ADD-ROADMAP-ITEM, SEEDED-ENHANCE, BATCH-DISTILL, BATCH-EXPRESS, ASYNC-LOOP, NAME-REVIEW]
  end
  subgraph Entry2 [Task-Queue.md]
    E2[PROCESS TASK QUEUE]
    M2[TASK-ROADMAP, TASK-COMPLETE, ADD-ROADMAP-ITEM, EXPAND-ROAD, REORDER-ROADMAP, DUPLICATE-ROADMAP, MERGE-ROADMAPS, EXPORT-ROADMAP, PROGRESS-REPORT]
  end
  E1 --> M1
  E2 --> M2
  M1 --> WR[Watcher-Result.md]
  M2 --> WR
  M2 --> Mobile[Mobile-Pending-Actions.md]
```

Location: `.technical/prompt-queue.jsonl` (one JSON object per line; mode, prompt, source_file, id). Task-Queue.md: same line format; task/roadmap modes. Single valid entry → fast-path dispatch without dedup/sort.

---

## Ingest skill chain (simplified)

```mermaid
flowchart LR
  A0[bootstrap_optional]
  A[create_backup]
  B[classify_para]
  C[frontmatter_enrich]
  N[name_enhance_propose]
  D[subfolder_organize]
  E[split_atomic]
  E2[split_link_preserve]
  F[distill_note]
  G[distill_highlight_color]
  H[next_action_extract]
  I[append_to_hub]
  J[move_note_dry_run_then_commit]
  K[log_action]
  A0 --> A --> B --> C --> N --> D --> E --> E2 --> F --> G --> H --> I --> J --> K
```

Phase 1 ends with create/refresh Decision Wrapper (no move); Phase 2 apply-mode (after approved wrapper) runs move/rename with snapshot and dry_run. Moving a skill (e.g. name-enhance) would break path/commit semantics; order is fixed in Cursor-Skill-Pipelines-Reference.

---

## Confidence band decisions

```mermaid
flowchart TD
  Eval[Evaluate confidence]
  Eval --> High[High ≥85%]
  Eval --> Mid[Mid 68-84%]
  Eval --> Low[Low <68%]
  High --> Snapshot[Per-change snapshot]
  Snapshot --> Act[Execute destructive actions]
  Mid --> Loop[One refinement loop]
  Loop --> Post{post_loop_conf ≥85%?}
  Post -->|Yes| Snapshot
  Post -->|No| Manual[Manual review; no destructive]
  Low --> Manual
  Manual --> Log[Log loop_* fields]
```

Primary signals: ingest_conf, path_conf, archive_conf, express_conf, distill_conf. Tunable via Second-Brain-Config confidence_bands when set.

---

## Vault folder tree and exclusions

```mermaid
flowchart TB
  Root[Vault root]
  Root --> P1[1-Projects]
  Root --> P2[2-Areas]
  Root --> P3[3-Resources]
  Root --> P4[4-Archives]
  P4 --> IngestDecisions[Ingest-Decisions]
  IngestDecisions --> ReWrap[Re-Wrap/]
  Root --> Ingest[Ingest]
  Root --> Backups[Backups]
  Root --> Templates[Templates]
  Root --> Attachments[5-Attachments]
  Root --> Tech[".technical (Obsidian excluded)"]
  Backups --> PerChange[Per-Change]
  Backups --> Batch[Batch]
  P1 -.->|optional| VersionsNode[Versions/ under project or area]
  P2 -.->|optional| VersionsNode
  Attachments --> PDFs[PDFs]
  Attachments --> Images[Images]
  Attachments --> Other[Audio, Documents, Other]
```

**Exclusions (do not process):** Backups/ (any subtree), **/Log*.md, **/* Hub.md, 3-Resources/Second-Brain/tests/, Watcher paths (Ingest/watched-file.md, Watcher-Signal.md, Watcher-Result.md), .technical/, watcher-protected: true, Ingest/Decisions/** (wrappers as control notes). Blacklist names: never use 00 Inbox, 10 Zettelkasten, 99 Attachments, 99 Templates; use Ingest, Templates, 5-Attachments, PARA roots only.
