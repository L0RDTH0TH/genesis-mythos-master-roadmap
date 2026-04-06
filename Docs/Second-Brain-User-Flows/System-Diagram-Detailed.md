---
title: Second Brain System Diagram — Detailed
created: 2026-03-05
tags: [pkm, second-brain, diagram, level-3]
para-type: Resource
status: active
links: ["[[Resources Hub]]", "[[3-Resources/Second-Brain/README]]"]
---

# Second Brain System Diagram — Detailed

This document is the full breakdown: per-pipeline skill chains and slots (from Cursor-Skill-Pipelines-Reference and Skills.md), individual MCP tool calls and key parameters (from MCP-Tools.md), log flows and entry structures (from Logs.md), config consumers (from Configs.md and Second-Brain-Config), queue modes and entry formats (from Queue-Sources and Parameters.md), testing layers (from Testing.md), highlight flows (from Color-Coded-Highlighting.md), naming conventions (from Naming-Conventions.md), and all safety flows (backup/snapshot/dry_run from Rules and Parameters). Mermaid from Backbone, Pipelines, and related docs is included. Use for implementation and debugging.

---

## System flow (from Backbone)

```mermaid
flowchart LR
  Triggers[User / Watcher triggers]
  Triggers --> Match[Phrase or glob match]
  Match --> Rules[Rules: always + context]
  Rules --> Pipeline[Pipeline selection]
  Pipeline --> Skills[Skills + MCP tools]
  Skills --> Vault[Obsidian vault]
  Skills -.->|before destructive| Backup[Backup / Snapshot]
  Backup -.-> Vault
```

---

## Safety flow (from Backbone)

```mermaid
flowchart TD
  Step[Destructive step?]
  Step -->|Yes| Conf{Confidence ≥85%?}
  Conf -->|Yes| CreateBackup[create_backup or ensure_backup]
  CreateBackup --> PerChange[Per-change snapshot]
  PerChange --> Execute[Execute move/rename/split/distill/append]
  Conf -->|No| Manual[Manual review; no destructive]
  Step -->|No| Proceed[Proceed]
```

**Invariants:** Never destructive MCP without backup (create_backup or ensure_backup). For move_note: ensure_structure(folder_path: parent of target) then move_note(..., dry_run: true), review effects, then move_note(..., dry_run: false). Per-change snapshot via obsidian-snapshot skill before each destructive step when confidence ≥85%.

---

## Full ingest flowchart (two-phase, Decision Wrapper–gated, from Pipelines)

```mermaid
flowchart TD
  Start[list_notes Ingest]
  Start --> Backup[create_backup]
  Backup --> Bootstrap{Optional bootstrap_project_batch}
  Bootstrap --> Classify[classify_para]
  Classify --> Frontmatter[frontmatter_enrich]
  Frontmatter --> Subfolder[subfolder_organize]
  Subfolder --> ConfGate{ingest_conf?}
  ConfGate -->|"≥85%"| Snap1[Per-change snapshot (in-note)]
  ConfGate -->|"68-84%"| Loop[Self-critique loop]
  ConfGate -->|"<68%"| Wrapper[Decision Wrapper (low-confidence)]
  Loop --> PostConf{post_loop_conf ≥85%?}
  PostConf -->|Yes| Snap1
  PostConf -->|No| Wrapper
  Snap1 --> Split[split_atomic]
  Split --> SplitLink[split_link_preserve]
  SplitLink --> Distill[distill_note]
  Distill --> Highlight[distill_highlight_color]
  Highlight --> NextAct[next_action_extract]
  NextAct --> TaskReroute[task_reroute]
  TaskReroute --> Hub[append_to_hub]
  Hub --> Log[log_action]
  Log --> DecWrap[Create/refresh Decision Wrapper (propose_para_paths max 7 candidates → A–G)]
  DecWrap --> EAT[EAT-QUEUE (wrapper approved?)]
  EAT --> ApplyRun[Apply-mode ingest (Phase 2)]
  ApplyRun --> MoveSnap[Snapshot + dry_run move/rename]
  MoveSnap --> Done[Note in PARA; wrapper logged]
```

---

## Ingest confidence loop (state diagram, from Cursor-Skill-Pipelines-Reference)

```mermaid
flowchart LR
  eval[Evaluate ingest_conf] --> high[High (>=85)]
  eval --> mid[Mid (68-84)]
  eval --> low[Low (<68)]

  high --> snap_ingest[Per-change snapshot]
  snap_ingest --> ingest_actions[Split / distill / hub / move]

  mid --> loop_ingest[Non-destructive self-critique loop]
  loop_ingest --> post_high[post_loop_conf >= 85]
  loop_ingest --> post_low[post_loop_conf < 85 or <= pre_loop_conf]

  post_high --> snap_ingest
  post_low --> manual_ingest[Manual review (no destructive actions)]

  low --> manual_ingest
```

---

## Distill / Archive / Express / Organize (overview, from Pipelines)

```mermaid
flowchart TB
  subgraph distill [autonomous-distill]
    D1[backup]
    D2[auto-layer-select]
    D3[distill layers]
    D4[distill-highlight-color]
    D5[highlight-perspective-layer]
    D6[layer-promote]
    D7[distill-perspective-refine]
    D8[callout-tldr-wrap]
    D9[readability-flag]
    D1 --> D2 --> D3 --> D4 --> D5 --> D6 --> D7 --> D8 --> D9
  end
  subgraph archive [autonomous-archive]
    A1[backup]
    A2[classify_para]
    A3[archive-check]
    A4[subfolder-organize]
    A5[resurface-candidate-mark]
    A6[summary-preserve]
    A7[move_note]
    A8[log_action]
    A1 --> A2 --> A3 --> A4 --> A5 --> A6 --> A7 --> A8
  end
  subgraph express [autonomous-express]
    E1[backup]
    E2[version-snapshot]
    E3[related-content-pull]
    E4[express-mini-outline]
    E5[express-view-layer]
    E6[call-to-action-append]
    E1 --> E2 --> E3 --> E4 --> E5 --> E6
  end
  subgraph organize [autonomous-organize]
    O1[backup]
    O2[classify_para]
    O3[frontmatter-enrich]
    O4[subfolder-organize]
    O5[rename_note optional]
    O6[move_note]
    O7[log_action]
    O1 --> O2 --> O3 --> O4 --> O5 --> O6 --> O7
  end
```

---

## Snapshot triggers (per pipeline)

```mermaid
flowchart LR
  subgraph Pipelines [Pipelines]
    I[ingest]
    D[distill]
    A[archive]
    E[express]
    O[organize]
  end
  subgraph When [Trigger]
    P["Per-change: before move/rename/split/structural distill"]
    B["Batch: when batch size > batch_size_for_snapshot"]
  end
  I --> P
  I --> B
  D --> P
  D --> B
  A --> P
  E --> P
  O --> P
```

| Pipeline | Per-change triggers | Batch frequency |
|----------|---------------------|------------------|
| full-autonomous-ingest | Before split_atomic, distill_note (rewrite), append_to_hub, task-reroute (target note); Phase 2: before move_note, rename_note | Every 5 notes |
| autonomous-distill | Before first structural rewrite (distill layers, highlight-perspective-layer, layer-promote, distill-perspective-refine, heavy update_note) | ~Every 3 notes |
| autonomous-archive | After archive-check ≥85% but before subfolder-organize, summary-preserve, move | Once per sweep |
| autonomous-express | Before large appends (related-content-pull, express-mini-outline, express-view-layer, call-to-action-append); alongside version-snapshot | Optional per batch |
| autonomous-organize | Before obsidian_rename_note and before obsidian_move_note (when confidence ≥85% for each) | ~Every 3 notes |

batch_size_for_snapshot (from Second-Brain-Config): when queue/batch size > this value, use BATCH_SNAPSHOT_DIR; else per-change only.

---

## MCP tool groups and key parameters (from MCP-Tools)

```mermaid
flowchart TB
  subgraph Core [Core]
    read_note[read_note]
    update_note[update_note]
    search_replace[search_replace]
    list_notes[list_notes]
    global_search[global_search]
    manage_frontmatter[manage_frontmatter]
    manage_tags[manage_tags]
  end
  subgraph Backup [Backup]
    create_backup[create_backup]
    ensure_backup[ensure_backup]
  end
  subgraph Move [Move/structure]
    move_note[move_note dry_run then commit]
    rename_note[rename_note]
    ensure_structure[ensure_structure folder_path]
  end
  subgraph PARA [PARA/organize]
    classify_para[classify_para mode]
    subfolder_organize[subfolder_organize]
    propose_para_paths[propose_para_paths context_mode, max_candidates]
  end
  subgraph Content [Content]
    split_atomic[split_atomic]
    distill_note[distill_note]
    append_to_hub[append_to_hub]
    suggest_connections[suggest_connections]
  end
  subgraph Confidence [Confidence]
    calibrate_confidence[calibrate_confidence]
    verify_classification[verify_classification]
    propose_alternative_paths[propose_alternative_paths]
  end
  subgraph Other [Other]
    log_action[log_action changes string: include backup_path, snapshot path]
  end
```

**Key params:** move_note: dry_run (true = preview only; always dry_run first, then commit). update_note: mode overwrite | create (create for new version files; server skips destination backup). ensure_backup: max_age_minutes (e.g. 1440). propose_para_paths: context_mode (wrapper | midband | organize | fallback), max_candidates ("3"–"8").

---

## Log destinations and entry structure (from Logs)

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
  Pipelines -->|queue-cleanup, loop outcomes| FL
  Pipelines -->|on error| ERR
```

**Log line format:** `YYYY-MM-DD HH:MM | Excerpt: [snippet] | PARA: [type] | Changes: [list; include Backup: [path] when processing] | Confidence: X% | Proposed MV: [path or 'stay'] | Flag: [none or #review-needed + reason] | Loop: [attempted, type, pre, post, outcome, reason]`. **Error entry:** Heading `### YYYY-MM-DD HH:MM — Short Title`; metadata table (pipeline, severity, approval, timestamp, error_type); #### Trace; #### Summary (Root cause, Impact, Suggested fixes, Recovery).

---

## Log → MOC flow (from Logs)

```mermaid
flowchart LR
  subgraph logs [Pipeline and support logs]
    IL[Ingest-Log]
    DL[Distill-Log]
    AL[Archive-Log]
    EL[Express-Log]
    OL[Organize-Log]
    FL[Feedback-Log]
    BL[Backup-Log]
    ERR[Errors]
  end
  subgraph fields [Consistent fields]
    F[timestamp, note_path, pipeline, confidence, actions]
  end
  subgraph moc [Vault-Change-Monitor MOC]
    MOC_Q[Dataview: last 50 entries]
    MOC_C[Commander Dashboard]
    MOC_H[System Health]
    MOC_L[Links to full logs]
  end
  IL --> F
  DL --> F
  AL --> F
  EL --> F
  OL --> F
  FL --> F
  F --> MOC_Q
  F --> MOC_C
  BL --> MOC_H
  ERR --> MOC_L
  MOC_Q --> MOC_L
```

---

## Config sources and consumers (from Configs)

```mermaid
flowchart LR
  subgraph sources [Config sources]
    SBC[Second-Brain-Config]
    ENV[MCP env]
  end
  subgraph consumers [Consumers]
    Pipelines[Pipelines]
    Skills[Skills]
    Hubs[append_to_hub hub_names]
    ArchiveCheck[archive-check archive.age_days, no_activity_days]
    Highlight[distill-highlight-color, layer-promote highlight.default_key]
    Depths[batch_size_for_snapshot, async_preview_threshold]
    Backup[create_backup BACKUP_DIR]
    Snap[SNAPSHOT_DIR, BATCH_SNAPSHOT_DIR]
  end
  SBC --> Hubs
  SBC --> Pipelines
  SBC --> ArchiveCheck
  SBC --> Highlight
  SBC --> Depths
  ENV --> Backup
  ENV --> Snap
  ENV --> Pipelines
```

MCP env: OBSIDIAN_API_KEY, OBSIDIAN_REST_URL, OBSIDIAN_VAULT_PATH, BACKUP_DIR, SNAPSHOT_DIR, BATCH_SNAPSHOT_DIR, MAX_BACKUP_AGE_MINUTES.

---

## Queue processor flow (from Queue-Sources)

```mermaid
flowchart TD
  Read[Read file or EAT-CACHE payload]
  Read --> Parse[Parse line-by-line]
  Parse --> Validate[Validate: mode required]
  Validate --> Filter[Filter queue_failed]
  Filter --> Single{Valid entries === 1?}
  Single -->|Yes| Dispatch[Dispatch immediately]
  Single -->|No| Dedup[Dedup same mode, prompt, source_file]
  Dedup --> Sort[Sort by canonical order]
  Sort --> ForEach[For each entry]
  ForEach --> CheckFile{source_file exists?}
  CheckFile -->|No| Skip[Skip; log failure]
  CheckFile -->|Yes| Dispatch
  Dispatch --> Run[Run pipeline]
  Run --> Append[Append Watcher-Result]
  Append --> ForEach
```

**prompt-queue.jsonl format:** One JSON per line: mode, prompt, source_file, id (requestId). **Canonical order (horizontal):** INGEST → ORGANIZE → TASK-ROADMAP → DISTILL → EXPRESS → ARCHIVE → TASK-COMPLETE → ADD-ROADMAP-ITEM. Task-Queue.md: same line format; modes TASK-ROADMAP, TASK-COMPLETE, ADD-ROADMAP-ITEM, EXPAND-ROAD, etc.

---

## Highlighter flow (from Skills / Color-Coded-Highlighting)

```mermaid
flowchart LR
  subgraph triggers [Triggers and config]
    T1["HIGHLIGHT PERSPECTIVE: lens"]
    T2[Second-Brain-Config coverage 50-70%]
    T3["SWITCH HIGHLIGHT ANGLE: angle"]
    T4["HIGHLIGHT MULTI-ANGLE: list"]
  end
  subgraph skills [Skills and output]
    S1[distill-highlight-color]
    S2[highlight-perspective-layer]
    S3[layer-promote]
    S1 -->|"coverage %, perspective"| Log1[Distill-Log]
    S2 -->|"drift levels, angles"| Log1
  end
  subgraph frontmatter [Frontmatter]
    F1[highlight_perspective]
    F2[highlight_angles]
    F3[highlight_active_angle]
  end
  T1 --> S1
  T2 --> S1
  T3 --> F3
  T4 --> S2
  S1 --> S2
  S2 --> S3
  S1 --> F1
  S2 --> F2
```

Master key: Highlightr-Color-Key.md; project override: highlight_key. Analogous = related ideas; complementary = contrast/tension.

---

## Naming conventions (from Naming-Conventions)

**Regular notes:** `kebab-slug-YYYY-MM-DD-HHMM.md` — slug first, date and time at end (24h; unknown time → 0000). Slug: max ~60–70 chars, lowercase kebab-case; source priority: first heading > TL;DR > first sentence. **MOCs:** Topic MOC.md; avoid auto-rename. **Hubs:** X Hub.md; excluded from pipelines. **Path segment format** (subfolder-organize, name-enhance): kebab-slug-YYYY-MM-DD-HHMM per Naming-Conventions (date and time at end).

---

## Testing layers (from Testing)

```mermaid
flowchart TB
  subgraph Tests [3-Resources/Second-Brain/tests/]
    Unit[tests/unit/]
    Integration[tests/integration/]
    Fixtures[tests/fixtures/]
    Contracts[tests/sb_contracts/]
  end
  Unit --> Queue[Queue parse/validate/dedup/sort]
  Unit --> Exclusions[Path exclusions]
  Unit --> LogFormat[Log and Errors.md format]
  Unit --> Config[Config keys, confidence bands]
  Unit --> Propose[propose_para_paths contract]
  Integration --> PipelineOrder[Pipeline step order]
  Integration --> ConfidenceBands[High/mid/low bands]
  Integration --> DryRun[dry_run before move]
  Integration --> BackupSnapshot[Backup/snapshot before destructive]
  Integration --> Wrapper[Decision Wrapper A–G mapping]
  Tests -->|failures| Errors[Errors.md]
```

Exclusion: pipelines must not process tests/ as input.

---

## Move fallback and dry_run (from mcp-obsidian-integration)

```mermaid
flowchart TD
  Move[obsidian_move_note]
  Move --> Ensure[obsidian_ensure_structure folder_path: parent of new_path]
  Ensure --> DryRun[move_note dry_run: true]
  DryRun --> Review[Review effects: path, new_path, backup, risks]
  Review --> OK{dry_run acceptable?}
  OK -->|Yes| Commit[move_note dry_run: false]
  OK -->|No| Fallback[propose_alternative_paths → calibrate_confidence → verify_classification]
  Fallback --> DryRun
```

Path before every move: ensure_structure so target parent exists. No move commit without prior successful dry_run review.
