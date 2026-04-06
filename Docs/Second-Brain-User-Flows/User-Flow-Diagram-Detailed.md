---
title: User Flow Diagram — Detailed
created: 2026-03-05
tags: [pkm, second-brain, user-flow, diagram, level-3]
para-type: Resource
status: active
links: ["[[Resources Hub]]", "[[3-Resources/Second-Brain/README]]"]
---

# User Flow Diagram — Detailed

This document is the complete breakdown of every documented user choice: Decision Wrapper options (A–G, option 0, option R for re-try), phase-direction wrappers (roadmap → approve or re-try), mid-band refinement (preview → approve or feedback → re-queue), async preview (Mobile-Pending-Actions + Commander “Async Approve”), Commander macro and mobile toolbar choices, dry_run review before commit, queue modes (including EXPAND-ROAD, TASK-TO-PLAN-PROMPT) and banner cleanup, and guidance-aware re-run after user edits. It includes all confidence-band branches (high = silent proceed, mid = preview/loop, low = manual) and what happens if the user ignores a proposal.

---

## User Flow – Decision Wrapper: full option set

```mermaid
flowchart TD
  Wrapper[Decision Wrapper note under Ingest/Decisions/]
  Wrapper --> Presented[User is presented with:]
  Presented --> List[Options A, B, C, D, E, F, G — each a ranked PARA path]
  List --> Zero[Option 0 — reject all]
  List --> R[Option R — re-try with guidance]
  Zero --> Choices{User choice?}
  R --> Choices
  Choices -->|Check A–G| Path[One path selected]
  Choices -->|Check 0 or set re-wrap: true| Reject[Reject all]
  Choices -->|Check R or set re-try: true| ReTry[Re-try branch]
  Path --> Manual[User sets approved: true in frontmatter manually]
  Manual --> Watcher[Watcher never sets approved: true; only syncs checkbox → approved_option and approved_path when approved: true already set]
  Manual --> Optional[Optional: user adds user_guidance multiline YAML e.g. Move to Phase-2 using B because...]
  Optional --> EAT[User runs EAT-QUEUE]
  Watcher --> EAT
  EAT --> Resolve[feedback-incorporate resolves approved_path from frontmatter or parses A–G from body]
  Resolve --> Apply[Apply: ingest move/rename or phase-direction provenance + comment guidance]
  Reject --> EAT2[User runs EAT-QUEUE]
  EAT2 --> ReWrap[Re-wrap: archive wrapper to Re-Wrap/, create new wrapper with Thoughts as seed]
  ReTry --> EAT3[User runs EAT-QUEUE]
  EAT3 --> CapCheck{re_try_count < re_try_max_loops?}
  CapCheck -->|Yes| ReQueue[Append queue entry EXPAND-ROAD or TASK-TO-PLAN-PROMPT with guidance; wrapper → Roadmap-Decisions]
  CapCheck -->|No| CapHit[Create cap-hit wrapper; log #review-needed]
```

---

## User Flow – Confidence bands: high / mid / low (all pipelines)

```mermaid
flowchart TD
  Eval[Pipeline evaluates confidence]
  Eval --> High{High ≥85%?}
  Eval --> Mid{Mid 68–84%?}
  Eval --> Low{Low &lt;68%?}
  High --> Silent[No user choice: system proceeds]
  Silent --> Snap[Per-change snapshot]
  Snap --> Act[Destructive action: move / rename / split / distill / append]
  Mid --> OneLoop[One refinement loop only]
  OneLoop --> Async{Async preview enabled?}
  Async -->|Yes| Preview[Preview to Mobile-Pending-Actions]
  Async -->|No| Rescore[Re-score; post_loop_conf]
  Preview --> UserPreview[User is presented with: preview]
  UserPreview --> Approve{User sets approved: true or adds feedback?}
  Approve -->|Yes| ReQueue[User runs EAT-QUEUE or re-run]
  Approve -->|No / ignore| IgnoreMid[No destructive action; proposal remains; log loop_*]
  Rescore --> Post{post_loop_conf ≥85%?}
  Post -->|Yes| Snap
  Post -->|No| IgnoreMid
  Low --> Proposal[Proposal only; no loop]
  Proposal --> UserLow[User is presented with: proposal callout and/or Decision Wrapper]
  UserLow --> ActLow{User adds approved: true and optional user_guidance, then EAT-QUEUE?}
  ActLow -->|Yes| GuidanceRun[Guidance-aware run]
  ActLow -->|No / ignore| IgnoreLow[Note unchanged; manual review candidate; log #review-needed]
  GuidanceRun --> Snap
```

---

## User Flow – Mid-band async preview (Mobile-Pending-Actions + Commander)

```mermaid
flowchart TD
  Mid[Confidence in mid-band 68–84%]
  Mid --> Gen[System generates preview non-destructively]
  Gen --> Write[Preview written to Mobile-Pending-Actions]
  Write --> UserSees[User is presented with: preview in Mobile-Pending-Actions]
  UserSees --> How{How does user approve?}
  How -->|Frontmatter| Set[User sets approved: true in note frontmatter]
  How -->|Commander| Macro[User runs Commander macro e.g. Async Approve]
  Macro --> MacroAction[Macro scans Mobile-Pending-Actions, sets approved: true, re-queues]
  Set --> ReRun[User runs EAT-QUEUE or re-run]
  MacroAction --> ReRun
  ReRun --> Load[feedback-incorporate loads approved/feedback]
  Load --> Check{post_loop_conf ≥85%?}
  Check -->|Yes| Snap[Per-change snapshot]
  Snap --> Commit[Destructive commit]
  Check -->|No| Write
```

---

## User Flow – Guidance-aware re-run (approved: true + user_guidance)

```mermaid
flowchart TD
  Proposal[Note has proposal or decision_candidate]
  Proposal --> UserAdd[User adds to frontmatter:]
  UserAdd --> Approved[approved: true]
  UserAdd --> Optional[Optionally user_guidance: multiline text]
  Optional --> Trigger[Guidance-aware trigger: approved: true and user_guidance present, or queue prompt + source_file, or #guidance-aware]
  Trigger --> EAT[User runs EAT-QUEUE]
  EAT --> Load[feedback-incorporate loads user_guidance or queue prompt]
  Load --> Pass[Guidance passed as soft hint to classify_para, subfolder-organize, name-enhance, distill_note, split_atomic]
  Pass --> Boost[Optional guidance_conf_boost 0–20 added to confidence if followed]
  Boost --> Gate{Safety: confidence ≥85% and snapshot?}
  Gate -->|Yes| Move[Apply move/rename or structural change]
  Gate -->|No| NoMove[Guidance never overrides safety; log guidance_ignored: safety if needed]
```

---

## User Flow – Dry_run review before commit (move/rename)

```mermaid
flowchart TD
  Move[System will move or rename note]
  Move --> Conf{Confidence ≥85%?}
  Conf -->|Yes| DryRun[System calls move_note with dry_run: true]
  DryRun --> Effects[Effects returned: path, new_path, backup status, risks e.g. dangling links]
  Effects --> Presented[User is presented with: dry_run output in run]
  Presented --> Review[Agent reviews effects]
  Review --> OK{dry_run acceptable?}
  OK -->|Yes| Commit[System calls move_note with dry_run: false]
  OK -->|No| Fallback[propose_alternative_paths → calibrate_confidence → verify_classification]
  Fallback --> DryRun
  Commit --> Done[Note moved]
  Conf -->|No| NoMove[No move; proposal only]
```

---

## User Flow – Queue modes and banner cleanup

```mermaid
flowchart TD
  Queue[User has entries in prompt-queue.jsonl or Task-Queue.md]
  Queue --> Eat[User says EAT-QUEUE or Process queue or PROCESS TASK QUEUE]
  Eat --> Process[Processor runs each entry by mode]
  Process --> Task{Entry from Task-Queue?}
  Task -->|Yes| Run[Task-complete-validate, add-roadmap-append, etc.]
  Task -->|No| Pipeline[Dispatch pipeline by mode]
  Run --> Result[Result to Watcher-Result + Mobile-Pending-Actions]
  Pipeline --> Result
  Result --> Banner{Task queue: success &gt; failure?}
  Banner -->|Yes| Clean[Banner cleanup: remove pending callout from note]
  Banner -->|No| NoClean[Do not remove pending callout from failed item]
  Clean --> UserSees[User sees: pending banner removed on success]
  NoClean --> UserSees
```

---

## User Flow – What happens if user ignores proposal (low confidence)

```mermaid
flowchart TD
  Low[Pipeline ends in low confidence &lt;68%]
  Low --> Create[System creates/updates Decision Wrapper or proposal callout]
  Create --> Callout[Proposal callout: Add approved: true to frontmatter and run EAT-QUEUE to process]
  Callout --> UserIgnores{User ignores?}
  UserIgnores -->|Yes| Stay[Note stays in Ingest or current location]
  Stay --> Log[Logged with #review-needed; best-guess path in log]
  Stay --> Wrapper[Wrapper remains under Ingest/Decisions/ pending]
  UserIgnores -->|No| Act[User adds approved: true and optionally user_guidance]
  Act --> EAT[User runs EAT-QUEUE]
  EAT --> Apply[Next run: guidance-aware apply or re-process]
```

---

## User Flow – What happens if user ignores mid-band preview

```mermaid
flowchart TD
  Mid[Pipeline in mid-band; async preview written to Mobile-Pending-Actions]
  Mid --> UserSees[User is presented with: preview]
  UserSees --> Ignore{User ignores preview?}
  Ignore -->|Yes| NoCommit[System does not commit destructive action]
  NoCommit --> Log[Log loop_attempted, loop_band, pre_loop_conf, post_loop_conf, loop_outcome]
  NoCommit --> Stay[Note unchanged; proposal/preview remains]
  Ignore -->|No| Approve[User sets approved: true or adds feedback]
  Approve --> ReRun[User runs EAT-QUEUE or re-run]
  ReRun --> Check{post_loop_conf ≥85%?}
  Check -->|Yes| Commit[Snapshot then destructive commit]
  Check -->|No| NoCommit
```

---

## User Flow – Roadmap / phase-direction (master goal → prompt)

```mermaid
flowchart TD
  Master[User has master goal roadmap]
  Master --> Gen[roadmap-generate-from-outline or EXPAND-ROAD]
  Gen --> Expand[expand-road-assist runs]
  Expand --> Fork{Phase implies direction choices?}
  Fork -->|phase_forks or heuristic| Wrapper[Phase-direction wrapper created under Ingest/Decisions/Roadmap-Decisions/]
  Fork -->|No| Next[Next expand or TASK-TO-PLAN-PROMPT]
  Wrapper --> UserChoice[User is presented with: A–G conceptual end-state options + option R; technical in background]
  UserChoice --> Approve[User checks A–G and sets approved: true]
  UserChoice --> ReTry[User checks R or sets re-try: true]
  Approve --> EAT[User runs EAT-QUEUE]
  EAT --> Step0[Step 0: phase-direction apply]
  Step0 --> Provenance[Append provenance callout + comment guidance on roadmap note]
  Provenance --> Archive[Wrapper → 4-Archives/Ingest-Decisions/Roadmap-Decisions/]
  ReTry --> EAT2[User runs EAT-QUEUE]
  EAT2 --> ReQueue[Re-try branch: append EXPAND-ROAD or TASK-TO-PLAN-PROMPT with guidance]
  ReQueue --> Next
  Next --> Prompt[TASK-TO-PLAN-PROMPT: task → Cursor-ready prompt]
  Prompt --> Done[Prompt in note or Planning-Prompt-Task template]
```

---

## User Flow – Re-wrap branch (option 0 / re-wrap: true)

```mermaid
flowchart TD
  Wrapper[User has Decision Wrapper open]
  Wrapper --> Reject{User rejects all paths?}
  Reject -->|Check option 0 or set re-wrap: true| Set[re-wrap: true or approved_option: 0]
  Set --> EAT[User runs EAT-QUEUE]
  EAT --> Step0[Step 0 finds wrapper with re-wrap: true or approved_option: 0]
  Step0 --> Branch[Re-wrap branch]
  Branch --> Archive[Current wrapper moved to 4-Archives/Ingest-Decisions/Re-Wrap/]
  Archive --> New[New wrapper created under Ingest/Decisions/]
  New --> Seed[Thoughts block used as seed for new wrapper]
  Seed --> Link[Link to archived wrapper in new note]
  Link --> UserSees[User is presented with: new wrapper with fresh A–G from Thoughts]
```

---

## User Flow – Commander and mobile toolbar (documented options)

```mermaid
flowchart TD
  User[User on mobile or in Obsidian]
  User --> Toolbar{Mobile toolbar or Commander}
  Toolbar --> Queue[Queue Highlight: Combat etc. — adds queue entry with perspective/lens]
  Toolbar --> Process[Process Queue — triggers EAT-QUEUE]
  Toolbar --> Async[Async Approve — scan Mobile-Pending-Actions, set approved: true, re-queue]
  Toolbar --> Task[Task toolbar: TASK-COMPLETE, ADD-ROADMAP-ITEM, etc. — append to Task-Queue.md]
  Queue --> Entry[Entry in prompt-queue.jsonl with mode + payload]
  Process --> Eat[EAT-QUEUE runs]
  Async --> Eat
  Task --> TaskQueue[Entry in Task-Queue.md]
  TaskQueue --> Eat
  Entry --> Eat
  Eat --> Result[Watcher-Result; Commander macros log commander_source, commander_macro for MOC]
```

---

## User Flow – EAT-QUEUE Step 0 (approved wrappers always first)

Step 0 runs **before** reading `prompt-queue.jsonl`. Processed wrappers are moved to `4-Archives/Ingest-Decisions/` with subfolders mirrored (e.g. `Ingest/Decisions/Ingest-Decisions/` → `4-Archives/Ingest-Decisions/Ingest-Decisions/`).

```mermaid
flowchart TD
  Eat[User runs EAT-QUEUE]
  Eat --> Step0[Step 0: enumerate Ingest/Decisions/** — before reading queue file]
  Step0 --> Scan[For each wrapper: approved: true or re-wrap: true or re-try: true and not yet processed?]
  Scan --> Found{Any found?}
  Found -->|Yes| Inc[feedback-incorporate: resolve approved_path, re-wrap, or re-try intent]
  Found -->|No| Rest[Continue to rest of queue]
  Inc --> Branch{Which branch?}
  Branch -->|re-wrap / option 0| DoReWrap[Re-wrap: archive wrapper to Re-Wrap/, create new from Thoughts]
  Branch -->|re-try / option R| ReTry[Re-try: cap check; append EXPAND-ROAD or TASK-TO-PLAN-PROMPT; wrapper → Roadmap-Decisions]
  Branch -->|approved A–G| WrapperType{wrapper_type?}
  WrapperType -->|ingest| Apply[Apply-mode ingest: backup, snapshot, move/rename to approved_path]
  WrapperType -->|phase-direction| PhaseApply[Phase-direction apply: provenance + comment guidance on roadmap]
  Apply --> Move[Move wrapper to 4-Archives/Ingest-Decisions/ — subfolders mirrored]
  PhaseApply --> Move
  DoReWrap --> Rest
  ReTry --> Rest
  Move --> Rest
  Rest --> Read[Read prompt-queue.jsonl]
  Read --> Dispatch[Process remaining queue entries by mode]
  Dispatch --> Result[Watcher-Result per request]
```

---

## User Flow – Decision Wrapper Watcher sync (user sets approved only)

```mermaid
flowchart TD
  Wrapper[Decision Wrapper under Ingest/Decisions/]
  Wrapper --> UserCheck[User checks one option A–G in body]
  UserCheck --> UserSet[User sets approved: true in frontmatter manually]
  UserSet --> Watcher[Watcher plugin on modify]
  Watcher --> Check{approved: true already set?}
  Check -->|Yes| Sync[Watcher syncs checked letter → approved_option and approved_path in frontmatter]
  Check -->|No| NoSync[Watcher never sets approved: true]
  NoSync --> Safety[Safety: no accidental auto-approval]
  Sync --> Log[Sync/skip/conflict → Wrapper-Sync-Log.md]
  Log --> Ready[Wrapper ready for EAT-QUEUE Step 0]
```
