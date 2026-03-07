---
title: User Flow — Skills (Detailed)
created: 2026-03-05
tags: [pkm, second-brain, user-flow, skills, diagram, level-3]
para-type: Resource
status: active
links: ["[[Resources Hub]]", "[[3-Resources/Second-Brain/README]]"]
---

# User Flow — Skills (Detailed)

This document maps every documented skill to the user’s flow: slot order (from Cursor-Skill-Pipelines-Reference), user-visible output (callouts, frontmatter changes, previews, proposals), and decision points (approve path, add user_guidance, dry_run review, async approve via Commander/mobile). It includes confidence-band branches that affect what the user sees, queue-triggered skill runs (SEEDED-ENHANCE, BATCH-DISTILL, NAME-REVIEW), and re-queue after user edit. All interactions are from Pipelines, Cursor-Skill-Pipelines-Reference, Skills, Parameters, Rules, Queue-Sources, Templates, Backbone, and Logs.

---

## User flow – Ingest: full skill order and user-visible outputs

```mermaid
flowchart TD
  subgraph Phase1 [Phase 1 skills in order]
    P1[classify_para]
    P2[frontmatter-enrich]
    P3[name-enhance propose only]
    P4[subfolder-organize]
    P5[split_atomic]
    P6[split-link-preserve]
    P7[distill_note]
    P8[distill-highlight-color]
    P9[next-action-extract]
    P10[task-reroute]
    P11[append_to_hub]
    P12[create/refresh Decision Wrapper]
  end
  P1 --> P2 --> P3 --> P4
  P4 --> Band{ingest_conf?}
  Band -->|≥85%| P5
  P5 --> P6 --> P7 --> P8 --> P9 --> P10 --> P11
  P11 --> P12
  Band -->|&lt;85%| P12
  P12 --> User[User sees: wrapper note with A–G; original note may have proposal callout]
  User --> Decision{User: check A–G, set approved: true, optionally add user_guidance, run EAT-QUEUE?}
```

---

## User flow – Decision Wrapper: exact options user is presented with

```mermaid
flowchart TD
  Wrap[Decision Wrapper note under Ingest/Decisions/]
  Wrap --> Options[User presented with: options A, B, C, D, E, F, G — each a PARA path]
  Wrap --> Zero[Option 0 — reject all]
  Options --> C1{User choice?}
  C1 -->|Check one of A–G| Path[One path selected]
  C1 -->|Check 0 or set re-wrap: true| Reject[Reject all]
  Path --> Manual[User sets approved: true in frontmatter]
  Manual --> Watcher[Watcher syncs checkbox → approved_option and approved_path when approved: true already set]
  Manual --> Opt[User may add user_guidance multiline]
  Opt --> EAT[User runs EAT-QUEUE]
  Reject --> EAT
  EAT --> Step0[Step 0 processes wrapper]
  Step0 --> Apply[Apply-mode ingest: move/rename to approved_path]
  Apply --> UserSees[User sees: note in PARA; wrapper moved to 4-Archives/Ingest-Decisions/]
```

---

## User flow – Proposal and preview callouts (Templates.md text)

```mermaid
flowchart TD
  subgraph Proposal [Low-confidence proposal]
    P1[User sees callout in note]
    P2[Add approved: true to frontmatter and run EAT-QUEUE to process]
    P3[Optional: Suggested user_guidance tip with YAML placeholder]
  end
  subgraph Preview [Mid-band / async preview]
    V1[User sees: preview in Mobile-Pending-Actions]
    V2[Pending highlight/distill/express — run EAT-QUEUE after review]
  end
  subgraph Success [After commit]
    S1[User sees: success or Watcher-Result line]
  end
  P1 --> P2
  P2 --> Act{User adds approved: true and optional user_guidance?}
  Act -->|Yes| EAT[User runs EAT-QUEUE]
  V1 --> Act2{User approves or adds feedback?}
  Act2 -->|Yes| EAT
```

---

## User flow – Confidence band and what user sees

```mermaid
flowchart TD
  Eval[Pipeline evaluates confidence]
  Eval --> High{≥85%?}
  Eval --> Mid{68–84%?}
  Eval --> Low{&lt;68%?}
  High --> Silent[No user choice]
  Silent --> Out1[User sees: updated note or move result; Watcher-Result]
  Mid --> Loop[One refinement loop]
  Loop --> Async{Async preview?}
  Async -->|Yes| Write[Preview to Mobile-Pending-Actions]
  Write --> Out2[User presented with: preview]
  Out2 --> Act{Choices: A) approved: true B) feedback C) ignore}
  Async -->|No| Rescore[Re-score]
  Rescore --> Post{post_loop_conf ≥85%?}
  Post -->|Yes| Out1
  Post -->|No| Out3[User sees: proposal or #review-needed; no destructive action]
  Low --> Wrapper[Decision Wrapper and/or proposal callout]
  Wrapper --> Out4[User presented with: Add user_guidance and approved: true, then EAT-QUEUE]
  Act -->|A or B| ReRun[User runs EAT-QUEUE]
  Act -->|C| Out3
  ReRun --> Out1
```

---

## User flow – dry_run review (move/rename)

```mermaid
flowchart TD
  Move[System will move or rename note]
  Move --> Dry[obsidian_move_note dry_run: true]
  Dry --> Effects[Effects returned: path, new_path, backup status, risks e.g. dangling links]
  Effects --> User[User presented with: dry_run output in run]
  User --> Review[Agent reviews effects]
  Review --> OK{Acceptable?}
  OK -->|Yes| Commit[obsidian_move_note dry_run: false]
  OK -->|No| Fallback[propose_alternative_paths → calibrate → verify → dry_run again]
  Commit --> Done[User sees: note moved]
  Fallback --> Dry
```

---

## User flow – Async approve (Commander / mobile)

```mermaid
flowchart TD
  Mid[Mid-band; preview in Mobile-Pending-Actions]
  Mid --> UserSees[User presented with: preview]
  UserSees --> How{How does user approve?}
  How -->|Frontmatter| Set[User sets approved: true in note frontmatter]
  How -->|Commander| Macro[User runs Commander macro e.g. Async Approve]
  Macro --> MacroAct[Macro scans Mobile-Pending-Actions, sets approved: true, re-queues]
  Set --> EAT[User runs EAT-QUEUE]
  MacroAct --> EAT
  EAT --> Load[feedback-incorporate loads approved/feedback]
  Load --> Run[Re-run; if post_loop_conf ≥85% then snapshot + commit]
  Run --> Out[User sees: committed result or Watcher-Result]
```

---

## User flow – Guidance-aware re-run (user adds user_guidance and approved: true)

```mermaid
flowchart TD
  Prop[Note has proposal or decision_candidate]
  Prop --> UserAdd[User adds to frontmatter: approved: true and optionally user_guidance multiline]
  UserAdd --> EAT[User runs EAT-QUEUE]
  EAT --> Load[feedback-incorporate loads user_guidance or queue prompt]
  Load --> Pass[Guidance passed to classify_para, subfolder-organize, name-enhance, distill_note, split_atomic]
  Pass --> Run[Pipeline re-runs with guidance as soft hint]
  Run --> Gate{Confidence ≥85% and snapshot?}
  Gate -->|Yes| Move[Apply move/rename or structural change]
  Gate -->|No| NoMove[Log guidance_ignored: safety if needed]
  Move --> UserSees[User sees: note updated or moved]
```

---

## User flow – Distill skills and user-visible output (slot order)

```mermaid
flowchart TD
  D0[User triggers DISTILL MODE or DISTILL LENS: angle]
  D0 --> D1[auto-layer-select optional — user may override e.g. distill with 2 layers]
  D1 --> D2[distill layers]
  D2 --> D3[distill-highlight-color]
  D3 --> D4[highlight-perspective-layer optional]
  D4 --> D5[layer-promote]
  D5 --> D6[distill-perspective-refine]
  D6 --> D7[callout-tldr-wrap]
  D7 --> D8[readability-flag]
  D8 --> Out[User sees: TL;DR in summary callout, highlights, needs-simplify warning if low readability]
  Out --> Mid{Mid-band?}
  Mid -->|Yes| Prev[Preview to Mobile-Pending-Actions]
  Prev --> UserPrev[User presented with: preview]
```

---

## User flow – Express skills and user-visible output (slot order)

```mermaid
flowchart TD
  E0[User triggers EXPRESS MODE or EXPRESS VIEW: angle]
  E0 --> E1[version-snapshot]
  E1 --> E2[related-content-pull or obsidian_suggest_connections]
  E2 --> E3[express-mini-outline]
  E3 --> E4[express-view-layer when express_view set]
  E4 --> E5[call-to-action-append]
  E5 --> Out[User sees: Related section, outline, CTA callout e.g. Share/Publish?]
  Out --> Mid{Mid-band?}
  Mid -->|Yes| Prev[Preview outline not written]
  Prev --> UserPrev[User presented with: short preview outline]
```

---

## User flow – Archive skills and user-visible output (slot order)

```mermaid
flowchart TD
  A0[User triggers ARCHIVE MODE]
  A0 --> A1[archive-check]
  A1 --> A2[subfolder-organize]
  A2 --> A3[resurface-candidate-mark]
  A3 --> A4[summary-preserve]
  A4 --> Dry[ensure_structure then move_note dry_run: true]
  Dry --> User1[User presented with: dry_run effects in run]
  User1 --> Commit[move_note dry_run: false]
  Commit --> User2[User sees: note in 4-Archives]
  A1 --> Low{archive_conf &lt;68%?}
  Low -->|Yes| Cand[User sees: archive candidate only; no move]
```

---

## User flow – Organize skills and user-visible output (slot order)

```mermaid
flowchart TD
  O0[User triggers ORGANIZE MODE]
  O0 --> O1[classify_para]
  O1 --> O2[frontmatter-enrich]
  O2 --> O3[subfolder-organize]
  O3 --> O4[name-enhance optional]
  O4 --> O5[obsidian_rename_note when name-enhance applies]
  O5 --> O6[ensure_structure then move_note dry_run then commit]
  O6 --> Out[User sees: dry_run then note moved/renamed]
  O3 --> Mid{Mid-band?}
  Mid -->|Yes| Cand[User presented with: 2–3 path candidates]
  Cand --> ReRun{User re-runs?}
  ReRun -->|post ≥85%| O6
```

---

## User flow – Queue modes and which skills run (user adds entry)

```mermaid
flowchart TD
  Entry[User or Watcher/Commander adds queue entry]
  Entry --> Mode{Mode?}
  Mode -->|INGEST MODE| I[full-autonomous-ingest skills]
  Mode -->|DISTILL MODE| D[autonomous-distill skills]
  Mode -->|SEEDED-ENHANCE| SE[highlight-seed-enhance]
  Mode -->|BATCH-DISTILL| BD[autonomous-distill on batch]
  Mode -->|BATCH-EXPRESS| BE[autonomous-express on batch]
  Mode -->|NAME-REVIEW| NR[name-enhance batch]
  Mode -->|ASYNC-LOOP| AL[feedback-incorporate then re-run pipeline]
  I --> UserI[User sees: ingest outcome; wrapper or move]
  D --> UserD[User sees: distill outcome]
  SE --> UserSE[User sees: extended highlights from user marks]
  BD --> UserBD[User sees: batch results; Watcher-Result]
  NR --> UserNR[User sees: Name-Review-Log; suggested_name]
  AL --> UserAL[User sees: re-run outcome]
```

---

## User flow – Re-queue after user edit (approved: true)

```mermaid
flowchart TD
  Edit[User edits note or wrapper]
  Edit --> Add[User adds approved: true to frontmatter]
  Add --> Opt[User may add user_guidance or check wrapper option A–G]
  Opt --> EAT[User runs EAT-QUEUE]
  EAT --> Step0{Step 0: approved wrapper?}
  Step0 -->|Yes| Apply[Apply-mode ingest or re-wrap]
  Step0 -->|No| Dispatch[Dispatch by queue mode]
  Apply --> Scan[feedback-incorporate loads approved_path, user_guidance]
  Scan --> Run[Pipeline runs with guidance]
  Run --> Out[User sees: note moved or re-wrap new wrapper]
  Dispatch --> Run2[Corresponding pipeline/skills run]
  Run2 --> Out2[User sees: Watcher-Result line]
```

---

## User flow – Re-wrap branch (user choice option 0)

```mermaid
flowchart TD
  Wrap[User has Decision Wrapper open]
  Wrap --> Reject[User sets re-wrap: true or checks option 0]
  Reject --> EAT[User runs EAT-QUEUE]
  EAT --> Step0[Step 0 finds re-wrap: true or approved_option: 0]
  Step0 --> Archive[Current wrapper moved to 4-Archives/Ingest-Decisions/Re-Wrap/]
  Archive --> New[New wrapper created with Thoughts as seed]
  New --> UserSees[User presented with: new wrapper with fresh A–G from Thoughts]
  UserSees --> Link[Link to archived wrapper in new note]
```

---

## User flow – Task queue and banner cleanup (user sees)

```mermaid
flowchart TD
  Task[User or toolbar adds Task-Queue entry e.g. TASK-COMPLETE]
  Task --> EAT[User runs EAT-QUEUE or PROCESS TASK QUEUE]
  EAT --> Run[task-complete-validate or add-roadmap-append etc.]
  Run --> Result[Result to Watcher-Result and Mobile-Pending-Actions]
  Result --> Banner{Pipeline: success &gt; failure?}
  Banner -->|Yes| Clean[Banner cleanup: pending callout removed from note]
  Clean --> UserSees[User sees: pending banner removed; task marked complete]
  Banner -->|No| NoClean[User sees: Watcher-Result line; pending callout remains if failure]
```
