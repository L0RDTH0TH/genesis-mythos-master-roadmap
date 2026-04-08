---
title: Skills Structure — Mid-Level
created: 2026-03-05
tags: [pkm, second-brain, architecture, skills, diagram, level-2]
para-type: Resource
status: active
links: ["[[Resources Hub]]", "[[3-Resources/Second-Brain/README]]"]
---

# Skills Structure — Mid-Level

This document builds on the high-level view by adding per-pipeline skill chains with slots (from Cursor-Skill-Pipelines-Reference), key MCP call sequences (e.g. classify_para → subfolder_organize → move_note dry_run), confidence-loop structure, per-change vs batch snapshot usage, and log append points. Skill order and slots are taken from the canonical reference only.

---

## Ingest skill chain (slots from Cursor-Skill-Pipelines-Reference)

```mermaid
flowchart LR
  subgraph Pre [Pre]
    A0[bootstrap_optional]
    A[create_backup]
    B[classify_para]
  end
  subgraph Enrich [Enrich / organize]
    C[frontmatter-enrich]
    N[name_enhance propose only]
    D[subfolder_organize]
  end
  subgraph Content [Content]
    E[split_atomic]
    E2[split_link_preserve]
    F[distill_note]
    G[distill_highlight_color]
    H[next_action_extract]
    I[task_reroute when task-like ≥78%]
    J[append_to_hub]
  end
  subgraph Out [Out]
    K[create/refresh Decision Wrapper]
    L[log_action]
  end
  A0 --> A --> B --> C --> N --> D --> E --> E2 --> F --> G --> H --> I --> J --> K --> L
```

Phase 1: no move_note; Phase 2 apply-mode runs after user approves wrapper (separate run). Slots: frontmatter-enrich after classify_para; name-enhance after frontmatter-enrich; subfolder-organize after name-enhance; split-link-preserve after split_atomic; distill-highlight-color after distill_note; next-action-extract after distill-highlight-color; task-reroute after next-action-extract.

---

## Distill skill chain (slots)

```mermaid
flowchart LR
  A[create_backup]
  B[auto-layer-select optional]
  C[distill layers]
  D[distill_highlight_color]
  E[highlight_perspective_layer optional]
  F[layer_promote]
  G[distill_perspective_refine]
  H[callout_tldr_wrap]
  I[readability_flag]
  A --> B --> C --> D --> E --> F --> G --> H --> I
```

Pipeline order: (backup) → auto-layer-select when enabled → distill layers → distill-highlight-color → highlight-perspective-layer (optional) → layer-promote → distill-perspective-refine → callout-tldr-wrap → readability-flag.

---

## Archive skill chain (slots)

```mermaid
flowchart LR
  A[create_backup]
  B[classify_para]
  C[archive_check]
  D[subfolder_organize]
  E[resurface_candidate_mark]
  F[summary_preserve]
  G[ensure_structure then move_note dry_run then commit]
  H[log_action]
  A --> B --> C --> D --> E --> F --> G --> H
```

Optional mid-band loop: calibrate_confidence → verify_classification → move_note(dry_run: true) → then commit after snapshot.

---

## Express skill chain (slots)

```mermaid
flowchart LR
  A[create_backup]
  B[version_snapshot]
  C[related_content_pull or obsidian_suggest_connections]
  D[express_mini_outline]
  E[express_view_layer when express_view set]
  F[call_to_action_append]
  A --> B --> C --> D --> E --> F
```

Optional: obsidian_append_to_moc / obsidian_generate_moc after outline. version-snapshot uses obsidian_update_note(..., mode: "create") for Versions/ path.

---

## Organize skill chain (slots)

```mermaid
flowchart LR
  A[create_backup]
  B[classify_para]
  C[frontmatter_enrich]
  D[subfolder_organize]
  E[name_enhance optional]
  F[obsidian_rename_note when name-enhance applies]
  G[ensure_structure then move_note dry_run then commit]
  H[log_action]
  A --> B --> C --> D --> E --> F --> G --> H
```

Mid-band: obsidian_subfolder_organize for 2–3 candidates → calibrate_confidence → verify_classification → move_note(dry_run: true) → commit.

---

## Key MCP sequence: move path (ensure_structure → dry_run → commit)

```mermaid
flowchart TD
  Path[Target path computed]
  Path --> Ensure[obsidian_ensure_structure folder_path: parent of new_path]
  Ensure --> Dry[obsidian_move_note path, new_path, dry_run: true]
  Dry --> Review[Review effects: path, new_path, backup status, risks]
  Review --> OK{Acceptable?}
  OK -->|Yes| Commit[obsidian_move_note path, new_path, dry_run: false]
  OK -->|No| Fallback[propose_alternative_paths → calibrate_confidence → verify_classification]
  Fallback --> Dry
```

Required for every move (ingest apply-mode, archive, organize). Documented in mcp-obsidian-integration.

---

## Confidence loop structure (loop_* fields)

```mermaid
flowchart TD
  Eval[Evaluate primary signal: ingest_conf / path_conf / archive_conf / express_conf / distill_conf]
  Eval --> High{≥85%?}
  Eval --> Mid{68–84%?}
  Eval --> Low{&lt;68%?}
  High --> Snap[Per-change snapshot]
  Snap --> Act[Execute destructive steps]
  Mid --> Loop[Single non-destructive refinement loop]
  Loop --> MCP[Optional: obsidian_subfolder_organize max_candidates, calibrate_confidence, verify_classification]
  MCP --> Post[Compute post_loop_conf]
  Post --> Log[Write loop_attempted, loop_band, pre_loop_conf, post_loop_conf, loop_outcome, loop_type, loop_reason]
  Post --> Check{post_loop_conf ≥85%?}
  Check -->|Yes| Snap
  Check -->|No| Manual[No destructive; log #review-needed]
  Low --> Manual
```

Loop fields written to pipeline log and obsidian_log_action changes string (Logs.md, Cursor-Skill-Pipelines-Reference).

---

## Per-change vs batch snapshot (batch_size_for_snapshot)

```mermaid
flowchart TD
  Run[Pipeline run on batch]
  Run --> Size{Batch or queue size &gt; batch_size_for_snapshot?}
  Size -->|Yes| Batch[Use BATCH_SNAPSHOT_DIR: one batch snapshot for group]
  Size -->|No| Per[Per-change snapshot per note before each destructive step]
  Batch --> Log[Log to Backup-Log + pipeline log]
  Per --> Log
```

batch_size_for_snapshot from Second-Brain-Config (e.g. 5). Ingest: every 5 notes batch; distill/organize: ~every 3 notes; archive: once per sweep; express: optional per batch.

---

## Log append points (after each note)

```mermaid
flowchart LR
  Process[Process one note through pipeline]
  Process --> Log[obsidian_log_action]
  Log --> Append[Append to pipeline log]
  Append --> IL[Ingest-Log / Distill-Log / Archive-Log / Express-Log / Organize-Log]
  Log --> BL{Snapshots or backup used?}
  BL -->|Yes| BackupLog[Append to Backup-Log.md]
  Process --> Err{Error?}
  Err -->|Yes| Errors[Append to Errors.md per Error Handling Protocol]
```

Log line includes timestamp, pipeline, note path, confidence, actions, backup path, snapshot path(s), flag; plus loop_* when applicable. Include backup_path and snapshot path in log_action changes string (no dedicated param).
