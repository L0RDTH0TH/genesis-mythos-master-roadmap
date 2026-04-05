---
title: User Flow — Skills (High-Level)
created: 2026-03-05
tags: [pkm, second-brain, user-flow, skills, diagram, level-1]
para-type: Resource
status: active
links: ["[[Resources Hub]]", "[[3-Resources/Second-Brain/README]]"]
---

# User Flow — Skills (High-Level)

This document shows when and where the user is involved as skills run: major skill groups per pipeline as the user experiences them (e.g., ingest → classification + frontmatter + organize proposal → distill layers + highlights → hub append). It focuses only on user touchpoints—what the user sees or chooses—without per-skill slot detail. Mid-level and detailed docs add full skill sequences and every decision point.

---

## User flow – Ingest: major skill groups and user touchpoints

```mermaid
flowchart TD
  Start[User adds file to Ingest and runs INGEST MODE]
  Start --> Classify[Skills: classify_para + frontmatter-enrich]
  Classify --> Organize[Skills: name-enhance propose + subfolder-organize]
  Organize --> Conf{Confidence band?}
  Conf -->|High| Content[Skills: split_atomic, distill_note, distill-highlight-color, next-action-extract, task-reroute, append_to_hub]
  Conf -->|Mid/Low| Wrapper[Skill output: Decision Wrapper created]
  Content --> Wrapper
  Wrapper --> User1[User sees: wrapper with options A–G]
  User1 --> Choice1{User choice?}
  Choice1 -->|Check A–G, set approved: true| EAT[User runs EAT-QUEUE]
  Choice1 -->|Re-wrap or ignore| Stay[Note or wrapper stays]
  EAT --> Phase2[Apply-mode: move/rename to approved path]
  Phase2 --> User2[User sees: note in PARA; Watcher-Result line]
```

---

## User flow – Distill / Express / Archive: major skill groups and user touchpoints

```mermaid
flowchart TD
  subgraph Distill [Distill]
    D1[User triggers DISTILL MODE or BATCH-DISTILL]
    D1 --> D2[Skills: distill layers, distill-highlight-color, layer-promote, callout-tldr-wrap, readability-flag]
    D2 --> D3{Confidence?}
    D3 -->|High| D4[User sees: note updated with TL;DR callout and highlights]
    D3 -->|Mid| D5[User sees: preview in Mobile-Pending-Actions]
    D5 --> D6{User adds approved: true and re-runs?}
    D6 -->|Yes| D4
    D6 -->|No| D7[Preview remains]
  end
  subgraph Express [Express]
    E1[User triggers EXPRESS MODE]
    E1 --> E2[Skills: version-snapshot, related-content-pull, express-mini-outline, call-to-action-append]
    E2 --> E3[User sees: Related section, outline, CTA callout]
  end
  subgraph Archive [Archive]
    A1[User triggers ARCHIVE MODE]
    A1 --> A2[Skills: archive-check, subfolder-organize, summary-preserve]
    A2 --> A3[User sees: dry_run effects in run output before move]
    A3 --> A4[Note moved to 4-Archives; user sees result]
  end
```

---

## User flow – When user sees proposal or preview callouts

```mermaid
flowchart TD
  Run[Pipeline runs on note]
  Run --> Band{Confidence band?}
  Band -->|Low &lt;68%| Prop[Skill output: proposal callout in note]
  Prop --> UserProp[User sees: Add approved: true to frontmatter and run EAT-QUEUE to process]
  UserProp --> Act{User adds approved: true and optional user_guidance?}
  Act -->|Yes, then EAT-QUEUE| ReRun[Guidance-aware re-run]
  Act -->|No| Stay1[Note unchanged]
  Band -->|Mid 68–84%| Prev[Skill output: preview to Mobile-Pending-Actions]
  Prev --> UserPrev[User sees: preview in Mobile-Pending-Actions]
  UserPrev --> Act2{User approves or adds feedback?}
  Act2 -->|Yes, then EAT-QUEUE| ReRun
  Act2 -->|No| Stay2[No commit; proposal remains]
  Band -->|High ≥85%| Silent[No user choice; skills run to completion]
  Silent --> Done[User sees: updated note or Watcher-Result]
```

---

## User flow – Queue and Watcher-Result (user sees skill outcome)

```mermaid
flowchart TD
  Q[User runs EAT-QUEUE or Process queue]
  Q --> Dispatch[Queue processor dispatches by mode to pipelines/skills]
  Dispatch --> Run[Pipelines and skills run]
  Run --> Result[One line per request appended to Watcher-Result.md]
  Result --> UserSees[User sees: requestId, status success or failure, message, completed timestamp]
  UserSees --> Task{Task queue entry? success &gt; failure?}
  Task -->|Yes| Banner[User sees: pending banner removed from note]
  Task -->|No| NoBanner[User sees: Watcher-Result line only]
```
