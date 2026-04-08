---
title: Second Brain System Diagram — High-Level
created: 2026-03-05
tags: [pkm, second-brain, diagram, level-1]
para-type: Resource
status: active
links: ["[[Resources Hub]]", "[[3-Resources/Second-Brain/README]]"]
---

# Second Brain System Diagram — High-Level

This document gives a high-level overview of the Second Brain automation stack. It shows major components (Obsidian vault with PARA layout, Cursor rules and skills, MCP server and tools, Watcher/Commander for triggers and queues, logs and dashboards) and key flows such as capture → ingest pipeline → PARA move, without drilling into individual skills or tool parameters. Use it to orient before reading mid-level and detailed diagrams.

---

## Major components

```mermaid
flowchart TB
  subgraph Vault [Obsidian vault]
    PARA[PARA: 1-Projects, 2-Areas, 3-Resources, 4-Archives]
    Ingest[Ingest]
    Backups[Backups / Per-Change, Batch]
    PARA --> Ingest
    PARA --> Backups
  end
  subgraph Cursor [Cursor]
    Rules[Rules: always + context]
    Skills[Skills: pipeline steps]
    Rules --> Skills
  end
  subgraph MCP [MCP server]
    Tools[Obsidian tools: read, move, classify, backup, etc.]
  end
  subgraph Triggers [Triggers]
    Watcher[Watcher plugin]
    Commander[Commander plugin]
    User[User phrase]
  end
  Triggers --> Cursor
  Cursor --> MCP
  MCP --> Vault
  Vault --> Logs[Logs / dashboards]
  Cursor --> Logs
```

---

## Capture to PARA flow (high-level)

```mermaid
flowchart LR
  Capture[New file in Ingest]
  IngestPipe[Ingest pipeline]
  PARA[Note in PARA]
  Capture --> IngestPipe
  IngestPipe --> PARA
```

All new/unknown files land in **Ingest**. Saying **INGEST MODE** or **Process Ingest** runs the full-autonomous-ingest pipeline (classify → enrich → organize → distill → hub → Decision Wrapper in Phase 1; apply-mode move in Phase 2 after user approval). The note ends up in 1-Projects, 2-Areas, or 3-Resources (or stays in Ingest with a Decision Wrapper for manual choice).

---

## Triggers to pipelines

```mermaid
flowchart TD
  subgraph Triggers [Triggers]
    T1[INGEST MODE / Process Ingest]
    T2[EAT-QUEUE / Process queue]
    T3[DISTILL MODE]
    T4[ARCHIVE MODE]
    T5[EXPRESS MODE]
    T6[ORGANIZE MODE]
  end
  subgraph Pipelines [Pipelines]
    P1[full-autonomous-ingest]
    P2[Queue processor]
    P3[autonomous-distill]
    P4[autonomous-archive]
    P5[autonomous-express]
    P6[autonomous-organize]
  end
  T1 --> P1
  T2 --> P2
  T3 --> P3
  T4 --> P4
  T5 --> P5
  T6 --> P6
```

User phrases, Watcher signals, or queue entries match rules and select the pipeline. EAT-QUEUE runs the queue processor, which dispatches by mode to the appropriate pipeline (ingest, distill, archive, etc.).

---

## Safety gates (high-level)

```mermaid
flowchart TD
  Destructive[Destructive step?]
  Destructive -->|Yes| Conf{Confidence ≥85%?}
  Conf -->|Yes| Backup[Backup / ensure_backup]
  Backup --> Snapshot[Per-change snapshot]
  Snapshot --> DryRun[dry_run then commit]
  DryRun --> Execute[Execute move/rename/split/append]
  Conf -->|No| Manual[Manual review; no destructive]
  Destructive -->|No| Proceed[Proceed]
```

No destructive MCP action runs without backup (create_backup or ensure_backup) and, for moves, dry_run first then commit. Destructive steps are allowed only at high confidence (≥85%) and after a successful per-change snapshot.

---

## Logs and observability

```mermaid
flowchart LR
  subgraph Pipelines [Pipelines]
    Ingest[Ingest]
    Distill[Distill]
    Archive[Archive]
    Express[Express]
    Organize[Organize]
  end
  subgraph Logs [Logs]
    IL[Ingest-Log]
    DL[Distill-Log]
    AL[Archive-Log]
    EL[Express-Log]
    OL[Organize-Log]
    BL[Backup-Log]
    ERR[Errors]
  end
  subgraph MOC [Dashboard]
    Monitor[Vault-Change-Monitor MOC]
  end
  Pipelines --> Logs
  Logs --> Monitor
  Pipelines -->|on error| ERR
```

Pipeline runs write to pipeline-specific logs (and Backup-Log when snapshots/backups are involved). Errors go to Errors.md. The Vault-Change-Monitor MOC aggregates recent activity and health.
