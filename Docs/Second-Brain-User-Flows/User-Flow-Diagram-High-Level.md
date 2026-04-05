---
title: User Flow Diagram — High-Level
created: 2026-03-05
tags: [pkm, second-brain, user-flow, diagram, level-1]
para-type: Resource
status: active
links: ["[[Resources Hub]]", "[[3-Resources/Second-Brain/README]]"]
---

# User Flow Diagram — High-Level

This document shows the big picture of how the user moves through the Second Brain: how they start (triggers, phrases, Commander, mobile), which pipeline runs, and the main decision gates (auto vs manual review, EAT-QUEUE). It answers “what does the user do and what choices do they see?” without per-pipeline detail.

---

## User Flow – How the user starts (trigger choice)

```mermaid
flowchart TD
  Start[User wants to run a pipeline]
  Start --> How{How does user trigger?}
  How -->|Say phrase in Cursor| Phrase[User says INGEST MODE / DISTILL MODE / ARCHIVE MODE / EXPRESS MODE / ORGANIZE MODE / Process Ingest / run ingests / EAT-QUEUE for roadmap]
  How -->|Obsidian Watcher| Watcher[Watcher plugin writes signal; run triggered by Watcher request]
  How -->|Commander or mobile toolbar| Commander[Commander macro or mobile toolbar adds entry to queue]
  How -->|Process queue| Eat[User says EAT-QUEUE or Process queue or pastes EAT-CACHE]
  Phrase --> Pipeline[Corresponding pipeline runs]
  Watcher --> Pipeline
  Commander --> Queue[Entry in prompt-queue.jsonl or Task-Queue.md]
  Eat --> Queue
  Queue --> Dispatch[Queue processor dispatches by mode]
  Dispatch --> Pipeline
```

---

## User Flow – Auto vs manual review (main gate)

```mermaid
flowchart TD
  Run[Pipeline runs on note(s)]
  Run --> Conf{Confidence band?}
  Conf -->|High ≥85%| Auto[System proceeds: snapshot, then destructive step e.g. move / distill / append]
  Conf -->|Mid 68–84%| Mid[Single refinement loop; optional async preview]
  Conf -->|Low &lt;68%| Manual[Proposal only; no destructive action]
  Auto --> Done1[Done; note updated or moved]
  Mid --> UserMid{User is presented with: preview or proposal}
  UserMid --> Approve{User adds approved: true or feedback?}
  Approve -->|Yes, then EAT-QUEUE| ReRun[Re-run; if post_loop_conf ≥85% then snapshot + commit]
  Approve -->|No / ignore| Stay1[Note unchanged; proposal remains]
  Manual --> UserLow[User is presented with: proposal callout and/or Decision Wrapper]
  UserLow --> Act{User adds approved: true + optional user_guidance, then EAT-QUEUE?}
  Act -->|Yes| Apply[Guidance-aware apply run]
  Act -->|No / ignore| Stay2[Note stays; manual review candidate]
  ReRun --> Done1
  Apply --> Done1
```

---

## User Flow – Ingest: Phase 1 vs Phase 2 (EAT-QUEUE gate)

**Phase 1** never moves or renames; the note stays in Ingest/ until you approve a wrapper and run EAT-QUEUE. **Phase 2** runs only when EAT-QUEUE Step 0 (always-check wrappers) finds your wrapper with `approved: true` and applies the move.

```mermaid
flowchart TD
  Ingest[User adds file to Ingest/ and runs INGEST MODE or Process Ingest]
  Ingest --> Phase1[Phase 1: classify, enrich, distill, hub, create/refresh Decision Wrapper]
  Phase1 --> NoMove[No move/rename in Phase 1; note stays in Ingest/]
  NoMove --> Wrapper[Decision Wrapper created under Ingest/Decisions/ with options A–G]
  Wrapper --> UserChoice{User is presented with: wrapper with 7 paths A–G, option 0, option R}
  UserChoice --> Pick[User checks one option A–G and sets approved: true]
  UserChoice --> Reject[User sets re-wrap: true or approved_option: 0 reject all]
  UserChoice --> Retry[User sets re-try: true or option R]
  Pick --> EAT[User runs EAT-QUEUE]
  EAT --> Step0[Step 0 runs first: always-check wrappers; finds approved wrapper]
  Step0 --> Phase2[Apply: move/rename to approved_path; archive wrapper → 4-Archives/Ingest-Decisions/]
  Phase2 --> Done[Note in PARA; wrapper archived]
  Reject --> EAT2[User runs EAT-QUEUE]
  EAT2 --> ReWrap[Re-wrap branch: archive wrapper, create new wrapper from Thoughts]
  Retry --> EAT3[User runs EAT-QUEUE]
  EAT3 --> ReQueue[Re-try branch: append EXPAND-ROAD or TASK-TO-PLAN-PROMPT; wrapper → Roadmap-Decisions]
```

---

## User Flow – EAT-QUEUE: what the user gets

**Step 0 runs first**, before the queue file is read. Approved wrappers under `Ingest/Decisions/**` are applied (move note, archive wrapper); then the rest of the queue is processed by mode.

```mermaid
flowchart TD
  UserEAT[User says EAT-QUEUE or Process queue]
  UserEAT --> Step0[Step 0: Always-check wrappers first]
  Step0 --> Enum[Enumerate Ingest/Decisions/**]
  Enum --> AnyApproved{Any approved: true or re-wrap or re-try?}
  AnyApproved -->|Yes| Handle[Apply: move note to approved_path; archive wrapper to 4-Archives/Ingest-Decisions/]
  AnyApproved -->|No| Read[Read prompt-queue.jsonl or EAT-CACHE]
  Handle --> Read
  Read --> Dispatch[Dispatch remaining entries by mode: INGEST MODE, DISTILL MODE, TASK-COMPLETE, etc.]
  Dispatch --> Result[Watcher-Result.md updated per request]
  Result --> UserSees[User sees: Watcher-Result line; success or failure message]
  UserSees --> Banner{Task queue entry? success &gt; failure?}
  Banner -->|Yes| Clean[Banner cleanup: pending callout removed from note]
  Banner -->|No or mixed| NoClean[Pending callout remains if failure]
```

---

## User Flow – Roadmap breakdown (master goal → prompts)

```mermaid
flowchart TD
  Goal[User has master goal roadmap]
  Goal --> Expand[EXPAND-ROAD or roadmap-generate-from-outline]
  Expand --> Fork{Phase has direction choices?}
  Fork -->|Yes| Wrapper[Phase-direction wrapper: A–G + R under Roadmap-Decisions/]
  Fork -->|No| Next[Continue expand or TASK-TO-PLAN-PROMPT]
  Wrapper --> User[User approves A–G or re-tries with R]
  User --> EAT[EAT-QUEUE: Step 0 applies or re-queues]
  EAT --> Next
  Next --> Prompt[TASK-TO-PLAN-PROMPT: task → Cursor-ready prompt]
  Prompt --> Done[Prompts in note; plan evolution in Wrapper-MOC]
```
