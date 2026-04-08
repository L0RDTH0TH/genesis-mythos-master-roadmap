---
title: User Flow — Skills (Mid-Level)
created: 2026-03-05
tags: [pkm, second-brain, user-flow, skills, diagram, level-2]
para-type: Resource
status: active
links: ["[[Resources Hub]]", "[[3-Resources/Second-Brain/README]]"]
---

# User Flow — Skills (Mid-Level)

This document expands the high-level view to key skill sequences and user touchpoints per pipeline: the full ingest chain (classify_para → frontmatter-enrich → name-enhance propose → subfolder-organize → split → distill → highlights → next-action → task-reroute → hub), distill lens/perspective choice, express view choice, mid-band loop preview, and archive proposal review. Every decision diamond is a documented point where the user sees skill output or makes a choice.

---

## User flow – Ingest skill chain and user touchpoints

```mermaid
flowchart TD
  In[User runs INGEST MODE on Ingest note]
  In --> S1[classify_para + frontmatter-enrich]
  S1 --> S2[name-enhance propose only]
  S2 --> S3[subfolder-organize]
  S3 --> Band{ingest_conf?}
  Band -->|≥85%| S4[split_atomic, split-link-preserve, distill_note, distill-highlight-color, next-action-extract, task-reroute, append_to_hub]
  S4 --> Wrap[create/refresh Decision Wrapper]
  Band -->|68–84% or &lt;68%| Wrap
  Wrap --> User1[User presented with: Decision Wrapper note with options A–G]
  User1 --> C1{User choice?}
  C1 -->|Check one of A–G| Set[User adds approved: true in frontmatter]
  C1 -->|Option 0 or re-wrap: true| ReWrap[User runs EAT-QUEUE → re-wrap branch]
  Set --> Opt[User may add user_guidance multiline]
  Opt --> EAT[User runs EAT-QUEUE]
  EAT --> Apply[Apply-mode: move/rename to approved_path]
  Apply --> User2[User sees: note in PARA; Watcher-Result line]
```

---

## User flow – Ingest low-confidence: proposal callout and wrapper

```mermaid
flowchart TD
  Low[ingest_conf &lt;72 or mid-band failure]
  Low --> Create[Pipeline creates Decision Wrapper and proposal callouts]
  Create --> Callout[User sees: callout in note]
  Callout --> Text[Add user_guidance and approved: true to frontmatter, then run EAT-QUEUE]
  Create --> Wrapper[User sees: wrapper in Ingest/Decisions/ with A–G]
  Wrapper --> Tip[User may see: Suggested user_guidance tip callout with YAML placeholder]
  Text --> Act{User adds approved: true and user_guidance?}
  Act -->|Yes| EAT[User runs EAT-QUEUE]
  Act -->|No| Stay[Note and wrapper remain; manual review]
  EAT --> ReRun[Guidance-aware run; skills use user_guidance as soft hint]
```

---

## User flow – Distill: lens choice and skill output

```mermaid
flowchart TD
  D1[User triggers distill]
  D1 --> How{How?}
  How -->|DISTILL MODE| Default[Skills run with default depth]
  How -->|DISTILL LENS: angle| Lens[distill_lens set; skills use it for depth/TL;DR indicators]
  Default --> Chain[distill layers → distill-highlight-color → layer-promote → callout-tldr-wrap → readability-flag]
  Lens --> Chain
  Chain --> Out[User sees: note with TL;DR callout, highlights, readability warning if low]
  Chain --> Mid{Mid-band?}
  Mid -->|Yes| Preview[Preview written to Mobile-Pending-Actions]
  Preview --> UserPrev[User presented with: preview]
  UserPrev --> Approve{User sets approved: true and re-runs?}
  Approve -->|Yes| Out
  Approve -->|No| Stay[No structural commit]
```

---

## User flow – Express: view choice and skill output

```mermaid
flowchart TD
  E1[User triggers express]
  E1 --> How{How?}
  How -->|EXPRESS MODE| Default[Skills run default]
  How -->|EXPRESS VIEW: angle| View[express_view set; outline and Related shaped by view]
  Default --> Chain[version-snapshot → related-content-pull → express-mini-outline → express-view-layer → call-to-action-append]
  View --> Chain
  Chain --> Out[User sees: Related section, outline, CTA callout at end]
  Chain --> Mid{Mid-band?}
  Mid -->|Yes| Prev[Preview outline not written]
  Prev --> UserPrev[User presented with: short preview outline]
  UserPrev --> ReRun{User re-runs?}
  ReRun -->|Yes, post ≥85%| Out
  ReRun -->|No| Skip[Optional small CTA only]
```

---

## User flow – Mid-band loop: preview and user choice

```mermaid
flowchart TD
  Mid[Pipeline in mid-band 68–84%]
  Mid --> Loop[Single refinement loop]
  Loop --> Async{Async preview enabled?}
  Async -->|Yes| Write[Preview written to Mobile-Pending-Actions]
  Write --> User1[User presented with: preview in Mobile-Pending-Actions]
  User1 --> Choices{Choices: A) Set approved: true on note B) Add feedback text C) Ignore}
  Choices -->|A or B| ReRun[User runs EAT-QUEUE or re-run]
  Choices -->|C| NoCommit[No destructive action; proposal remains]
  ReRun --> Check{post_loop_conf ≥85%?}
  Check -->|Yes| Commit[Snapshot then commit]
  Check -->|No| NoCommit
  Async -->|No| Rescore[Re-score; post_loop_conf]
  Rescore --> High{post_loop_conf ≥85%?}
  High -->|Yes| Commit
  High -->|No| NoCommit
```

---

## User flow – Archive / Organize: dry_run review and proposal

```mermaid
flowchart TD
  Arch[User triggers ARCHIVE MODE or ORGANIZE MODE]
  Arch --> Skills[Skills: archive-check or frontmatter-enrich, subfolder-organize, summary-preserve or name-enhance]
  Skills --> Conf{archive_conf or path_conf?}
  Conf -->|≥85%| Dry[System runs move_note dry_run: true]
  Dry --> User1[User presented with: dry_run effects in run output path, new_path, backup status, risks]
  User1 --> Commit[Agent reviews; move_note dry_run: false]
  Commit --> User2[User sees: note moved]
  Conf -->|68–84%| Cand[Alternative paths and scores]
  Cand --> User3[User presented with: 2–3 path candidates]
  User3 --> ReRun{User approves and re-runs?}
  ReRun -->|post_loop_conf ≥85%| Dry
  ReRun -->|No| Log[Log #review-needed; no move]
  Conf -->|&lt;68%| Log
```

---

## User flow – Highlight perspective (user-triggered lens)

```mermaid
flowchart TD
  H1[User wants highlight with lens]
  H1 --> Trigger{Trigger?}
  Trigger -->|Phrase| Say[User says HIGHLIGHT PERSPECTIVE: lens]
  Trigger -->|Commander| Macro[User runs macro e.g. Queue Highlight Combat]
  Say --> Set[highlight_perspective or queue payload set]
  Macro --> Queue[Entry added to queue]
  Set --> Run[Distill or highlight pass runs]
  Queue --> EAT[User runs EAT-QUEUE]
  EAT --> Run
  Run --> Out[User sees: highlighting applied with analogous colors for lens]
```

---

## User flow – Queue-triggered skill runs (user adds entry then EAT-QUEUE)

```mermaid
flowchart TD
  Q1[User or Watcher/Commander adds queue entry]
  Q1 --> Modes{Mode?}
  Modes -->|SEEDED-ENHANCE| SE[highlight-seed-enhance runs on source_file]
  Modes -->|BATCH-DISTILL| BD[autonomous-distill on batch]
  Modes -->|NAME-REVIEW| NR[name-enhance batch runs]
  Modes -->|ASYNC-LOOP| AL[Re-process after async preview; feedback-incorporate loads approved/feedback]
  SE --> User1[User sees: extended highlights from user marks]
  BD --> User2[User sees: batch distill results; Watcher-Result per note]
  NR --> User3[User sees: Name-Review-Log; suggested_name applied or proposed]
  AL --> User4[User sees: re-run outcome; preview committed if post ≥85%]
```
