---
title: Skills Structure — High-Level
created: 2026-03-05
tags: [pkm, second-brain, architecture, skills, diagram, level-1]
para-type: Resource
status: active
links: ["[[Resources Hub]]", "[[3-Resources/Second-Brain/README]]"]
---

# Skills Structure — High-Level

This document describes the high-level architecture of the Second Brain skill and pipeline stack: major skill groups per pipeline, the canonical MCP flow (backup → classify → organize → content → move), confidence and safety gates, and log destinations. It does not list every skill slot; that is covered in the mid-level and detailed docs.

---

## Overall stack: rules, skills, MCP tools

```mermaid
flowchart TB
  subgraph Rules [Rules]
    Always[always: mcp-obsidian-integration, confidence-loops, guidance-aware]
    Context[context: para-zettel-autopilot, auto-distill, auto-archive, auto-express, auto-organize, auto-eat-queue]
  end
  subgraph Skills [Skills by pipeline]
    Ingest[Ingest: frontmatter-enrich, name-enhance, subfolder-organize, split-link-preserve, distill-highlight-color, next-action-extract, task-reroute]
    Distill[Distill: auto-layer-select, distill-highlight-color, highlight-perspective-layer, layer-promote, distill-perspective-refine, callout-tldr-wrap, readability-flag]
    Archive[Archive: archive-check, subfolder-organize, resurface-candidate-mark, summary-preserve]
    Express[Express: version-snapshot, related-content-pull, express-mini-outline, express-view-layer, call-to-action-append]
    Organize[Organize: frontmatter-enrich, subfolder-organize, name-enhance]
  end
  subgraph MCP [MCP tool groups]
    Backup[create_backup, ensure_backup]
    PARA[classify_para, subfolder_organize, obsidian_propose_para_paths]
    Content[split_atomic, distill_note, append_to_hub]
    Move[move_note, rename_note, ensure_structure]
    Conf[calibrate_confidence, verify_classification, propose_alternative_paths]
  end
  Rules --> Skills
  Skills --> MCP
```

---

## High-level MCP flow (backup → classify → organize → content → move)

```mermaid
flowchart LR
  subgraph Backup [Backup]
    B[create_backup or ensure_backup]
  end
  subgraph Classify [Classify]
    C[classify_para]
  end
  subgraph Organize [Organize]
    O[subfolder_organize / path proposal]
  end
  subgraph Content [Content]
    CO[split_atomic, distill_note, append_to_hub]
  end
  subgraph Move [Move]
    M[ensure_structure then move_note dry_run then commit]
  end
  B --> C --> O --> CO --> M
```

Documented order: backup first; then classify; then path/organize (skills use subfolder_organize or obsidian_propose_para_paths); then content ops (split, distill, append_to_hub); move last with ensure_structure(folder_path: parent) then move_note(dry_run: true) then move_note(dry_run: false).

---

## Confidence and safety gates (high-level)

```mermaid
flowchart TD
  subgraph Gate1 [Backup gate]
    G1[create_backup or ensure_backup before any destructive step]
  end
  subgraph Gate2 [Confidence band]
    High[High ≥85%: snapshot then destructive]
    Mid[Mid 68–84%: single refinement loop; post_loop_conf ≥85% to proceed]
    Low[Low &lt;68%: no destructive; proposal only]
  end
  subgraph Gate3 [Snapshot]
    G3[obsidian-snapshot per-change before split_atomic, distill_note rewrite, append_to_hub, task-reroute append, move_note, rename_note]
  end
  subgraph Gate4 [Move]
    G4[ensure_structure then move_note dry_run: true then review then move_note dry_run: false]
  end
  Gate1 --> Gate2
  Gate2 --> Gate3
  Gate3 --> Gate4
```

---

## Pipeline → log destinations

```mermaid
flowchart TB
  subgraph Pipelines [Pipelines]
    Ingest[full-autonomous-ingest]
    Distill[autonomous-distill]
    Archive[autonomous-archive]
    Express[autonomous-express]
    Organize[autonomous-organize]
  end
  subgraph Logs [Log files]
    IL[Ingest-Log.md]
    DL[Distill-Log.md]
    AL[Archive-Log.md]
    EL[Express-Log.md]
    OL[Organize-Log.md]
    BL[Backup-Log.md]
    FL[Feedback-Log.md]
    ERR[Errors.md]
  end
  Ingest --> IL
  Ingest --> BL
  Distill --> DL
  Distill --> BL
  Archive --> AL
  Archive --> BL
  Express --> EL
  Express --> BL
  Organize --> OL
  Organize --> BL
  Pipelines -->|loop outcomes, queue-cleanup| FL
  Pipelines -->|on error| ERR
```

Every pipeline calls obsidian_log_action after processing; include backup_path and snapshot path in changes string. Loop fields (loop_attempted, loop_band, pre_loop_conf, post_loop_conf, loop_outcome, loop_type, loop_reason) written when applicable.

---

## Safety invariant flow (mcp-obsidian-integration)

```mermaid
flowchart TD
  Destructive[Destructive MCP call?]
  Destructive -->|Yes| Conf{Confidence ≥85%?}
  Conf -->|Yes| Backup[create_backup or ensure_backup]
  Backup --> Snap[obsidian-snapshot per-change]
  Snap --> Ensure{Move or rename?}
  Ensure -->|Yes| ES[obsidian_ensure_structure folder_path: parent of new_path]
  ES --> Dry[obsidian_move_note dry_run: true]
  Dry --> Review[Review effects]
  Review --> Commit[obsidian_move_note dry_run: false]
  Ensure -->|No| Do[Execute split_atomic / distill_note / append_to_hub / etc.]
  Conf -->|No| Skip[No destructive action; log #review-needed]
```

If create_backup fails: abort pipeline for that note. If move_note fails (e.g. parent missing): ensure_structure then retry. If dry_run shows high risk: propose_alternative_paths → calibrate_confidence → verify_classification → dry_run again → commit or log and pause.
