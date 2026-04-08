---
title: User Flow Diagram — Mid-Level
created: 2026-03-05
tags: [pkm, second-brain, user-flow, diagram, level-2]
para-type: Resource
status: active
links: ["[[Resources Hub]]", "[[3-Resources/Second-Brain/README]]"]
---

# User Flow Diagram — Mid-Level

This document builds on the high-level user flow by adding per-pipeline branches: what the user sees after ingest Phase 1 (Decision Wrapper with A–G and optional user_guidance), in the mid-band loop (preview and approve), and when choosing lens/view for distill and express, when reviewing proposed archive/organize moves, and when processing the queue. Each decision point lists the exact options the user is presented with.

---

## User Flow – Ingest Phase 1 → Decision Wrapper (options A–G)

```mermaid
flowchart TD
  Phase1[Phase 1 ingest completes]
  Phase1 --> Wrapper[Decision Wrapper created/updated under Ingest/Decisions/]
  Wrapper --> Presented[User is presented with: wrapper note containing]
  Presented --> Options[Exactly 7 lettered options A–G with candidate PARA paths]
  Presented --> R[Option R — re-try with guidance]
  Options --> Choice{User choice?}
  R --> Choice
  Choice -->|Check one of A–G| SetApproved[User sets approved: true in frontmatter]
  Choice -->|Reject all| SetReject[User sets re-wrap: true or approved_option: 0]
  Choice -->|Re-try| SetRetry[User sets re-try: true or approved_option: R]
  Choice -->|Ignore| Ignore[Note stays in Ingest; wrapper remains pending]
  SetApproved --> Optional[Optionally: user adds user_guidance multiline with reasoning]
  SetApproved --> WatcherSync[Watcher syncs checked option → approved_option and approved_path when approved: true already set]
  Optional --> RunEAT[User runs EAT-QUEUE]
  WatcherSync --> RunEAT
  RunEAT --> Apply[Step 0 runs apply-mode ingest: move/rename to approved_path]
  SetReject --> RunEAT2[User runs EAT-QUEUE]
  RunEAT2 --> ReWrap[Re-wrap branch: archive wrapper, create new wrapper from Thoughts]
```

---

## User Flow – Mid-band refinement loop (preview + approve)

```mermaid
flowchart TD
  Mid[Pipeline runs; confidence in mid-band 68–84%]
  Mid --> Loop[Single non-destructive refinement loop]
  Loop --> Preview{Async preview enabled?}
  Preview -->|Yes| Write[Preview written to Mobile-Pending-Actions]
  Preview -->|No| Score[Re-score; post_loop_conf computed]
  Write --> UserSee[User is presented with: preview in Mobile-Pending-Actions]
  UserSee --> UserAct{User action?}
  UserAct -->|Set approved: true on note| Approve[User runs EAT-QUEUE or re-run]
  UserAct -->|Add feedback text| Feedback[User runs EAT-QUEUE with feedback]
  UserAct -->|Ignore| NoChange[No destructive action; proposal remains]
  Approve --> Check{post_loop_conf ≥85%?}
  Feedback --> Check
  Check -->|Yes| Snap[Per-change snapshot then commit]
  Check -->|No| NoChange
  Score --> PostHigh{post_loop_conf ≥85%?}
  PostHigh -->|Yes| Snap
  PostHigh -->|No| Manual[Manual review; no destructive action]
```

---

## User Flow – Distill (lens choice)

```mermaid
flowchart TD
  Distill[User wants to distill a note]
  Distill --> Trigger{How does user trigger?}
  Trigger -->|Default| Say[User says DISTILL MODE or distill this note]
  Trigger -->|With lens| Lens[User says DISTILL LENS: angle e.g. beginner / expert]
  Say --> Run[autonomous-distill runs; default depth/layers]
  Lens --> SetLens[distill_lens set in frontmatter; pipeline uses it for depth/TL;DR indicators]
  SetLens --> Run
  Run --> Conf{distill_conf band?}
  Conf -->|High ≥85%| Auto[Full structural distill after snapshot]
  Conf -->|Mid| Loop[Depth self-critique; optional preview]
  Conf -->|Low| Meta[Only readability-flag and metadata]
  Auto --> Done[Done]
  Loop --> UserPreview[User is presented with: preview or shallower plan]
  UserPreview --> ReRun{User re-runs with approved or feedback?}
  ReRun -->|Yes| Done
  ReRun -->|No| Done
```

---

## User Flow – Express (view choice)

```mermaid
flowchart TD
  Express[User wants to express a note]
  Express --> Trigger{How does user trigger?}
  Trigger -->|Default| Say[User says EXPRESS MODE or express this note]
  Trigger -->|With view| View[User says EXPRESS VIEW: angle e.g. stakeholder / dev technical]
  Say --> Run[autonomous-express runs]
  View --> SetView[express_view set in frontmatter; outline and Related section shaped by view]
  SetView --> Run
  Run --> Conf{express_conf band?}
  Conf -->|High ≥85%| Full[Version snapshot, related-content, outline, CTA]
  Conf -->|Mid| Soft[Preview outline; user may re-run]
  Conf -->|Low| Min[Optional minimal CTA only]
  Full --> Done[Done]
  Soft --> UserSee[User is presented with: short preview outline]
  UserSee --> ReRun{User re-runs?}
  ReRun -->|Yes, post ≥85%| Commit[Shorter or full outline + CTA]
  ReRun -->|No| Skip[Skip outline blocks; optional small CTA]
```

---

## User Flow – Archive / Organize (review proposed move)

```mermaid
flowchart TD
  Archive[User says ARCHIVE MODE or ORGANIZE MODE on scope]
  Archive --> Run[Pipeline runs: archive-check or subfolder-organize]
  Run --> Conf{archive_conf or path_conf?}
  Conf -->|High ≥85%| DryRun[System runs dry_run: true for move_note]
  Conf -->|Mid 68–84%| Loop[Refinement loop; optional 2–3 path candidates]
  Conf -->|Low &lt;68%| Proposal[Proposal only; no move]
  DryRun --> Review[User is presented with: dry_run effects path, new_path, backup, risks in run output]
  Review --> Commit{Agent reviews then calls move_note dry_run: false}
  Commit --> Done[Note moved]
  Loop --> UserCand[User is presented with: alternative paths and scores]
  UserCand --> ReRun{User approves and re-runs?}
  ReRun -->|post_loop_conf ≥85%| DryRun
  ReRun -->|No| Log[Log #review-needed; no move]
  Proposal --> Log
```

---

## User Flow – Roadmap / phase-direction (expand → wrapper → approve or re-try)

```mermaid
flowchart TD
  Roadmap[Master goal or roadmap phase]
  Roadmap --> Expand[EXPAND-ROAD or roadmap-generate-from-outline]
  Expand --> Fork{Phase has direction choices?}
  Fork -->|Yes| PhaseWrap[Phase-direction wrapper under Roadmap-Decisions/]
  Fork -->|No| Next[Next expand or TASK-TO-PLAN-PROMPT]
  PhaseWrap --> User[User: check A–G or R]
  User --> Approve[approved: true → Step 0 applies provenance + comment guidance]
  User --> Retry[re-try: true or R → re-queue with guidance]
  Approve --> Archive[Wrapper → 4-Archives/Ingest-Decisions/Roadmap-Decisions/]
  Retry --> Next
  Next --> Prompt[TASK-TO-PLAN-PROMPT: task → Cursor-ready prompt]
```

---

## User Flow – Queue processing (EAT-QUEUE choices)

**Step 0 runs first**, before reading the queue file. The processor enumerates `Ingest/Decisions/**`, applies any approved (or re-wrap/re-try) wrappers, then reads and dispatches the rest of the queue.

```mermaid
flowchart TD
  Eat[User says EAT-QUEUE or Process queue]
  Eat --> Step0[Step 0: Always-check wrappers first]
  Step0 --> Enum[Enumerate Ingest/Decisions/**]
  Enum --> WrapperApply[Apply approved: move note → archive wrapper to 4-Archives/Ingest-Decisions/]
  WrapperApply --> Read[Read prompt-queue.jsonl or Task-Queue.md]
  Read --> Single{Valid entries === 1?}
  Single -->|Yes| Fast[Dispatch immediately no dedup/sort]
  Single -->|No| Dedup[Dedup, sort by canonical order]
  Dedup --> ForEach[For each entry]
  Fast --> ForEach
  ForEach --> Mode[Dispatch by mode: INGEST MODE, EXPAND-ROAD, TASK-TO-PLAN-PROMPT, DISTILL MODE, TASK-COMPLETE, etc.]
  Mode --> Result[Append Watcher-Result line]
  Result --> UserSees[User is presented with: Watcher-Result.md line per request]
  UserSees --> Task{Task queue entry? success &gt; failure?}
  Task -->|Yes| Banner[Banner cleanup: pending callout removed from note]
  Task -->|No| NoBanner[No banner change]
```

---

## User Flow – Highlight perspective (optional lens)

```mermaid
flowchart TD
  Highlight[User wants highlight with a specific lens]
  Highlight --> Trigger{Trigger?}
  Trigger -->|Phrase| Say[User says HIGHLIGHT PERSPECTIVE: lens e.g. combat systems]
  Trigger -->|Commander| Macro[Commander macro e.g. Queue Highlight Combat]
  Say --> Set[highlight_perspective or queue payload set]
  Macro --> Queue[Entry added to queue with perspective]
  Set --> Run[Distill or highlight pass runs with lens]
  Queue --> Eat[User runs EAT-QUEUE]
  Eat --> Run
  Run --> Done[Highlighting applied with analogous colors for lens]
```
