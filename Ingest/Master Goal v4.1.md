---
title: Untitled
created: "2026-03-05 21:09"
tags: ["project", "master-goal", "second-brain"]
para-type: Project
status: active
ingest-type: stray-thought
proposal_path: Ingest/Decisions/Ingest-Decisions/Decision-for-master-goal-v4-1--2026-03-07-0541.md
decision_priority: high
---
# Stray Thought

## What am I thinking?

_Write the single core thought or observation in 1–3 sentences._


Here’s **Master Goal v4.1** with your four directions applied. You can paste this into your canonical Master Goal note (or switch to Agent mode if you want it written into a file).

---

## Master Goal v4.1

**Building a (mostly) fully autonomous, post-capture Second Brain in Obsidian using PARA + Zettelkasten (inspired by Tiago Forte’s Building a Second Brain), where:**

**Capture and the ingest trigger remain the only steps that are always manual.** You capture into Ingest and decide when to run ingest (e.g. “INGEST MODE”, “Process Ingest”, or by opening an Ingest note to trigger the agent). A future watcher may support other signals but will not auto-run ingest; ingest is always manually initiated. The aim is **mostly zero-manual input**: Cursor’s nature requires pipelines to be launched by you (phrase, Commander, or EAT-QUEUE), but once launched the system runs with minimal further input. The mobile–laptop split is central: you can add to the queue, set options, and refine content on mobile, then run Cursor on laptop to process and get results—so your input is light and asynchronous.

**Once triggered, pipelines run in two phases where moves are involved.** Phase 1 proposes paths and creates Decision Wrappers (options A–G); Phase 2 applies moves only after you set `approved: true` (and optionally `user_guidance`) and run EAT-QUEUE. Processing is triggered by phrases, Commander, or queue entries (EAT-QUEUE), including batch and refinement modes (e.g. BATCH-DISTILL, NAME-REVIEW, ASYNC-LOOP). Pipelines (INGEST, DISTILL, ARCHIVE, ORGANIZE, or EXPRESS MODE) then run autonomously: organizing into PARA (with intelligent subfolders up to 4 levels), preprocessing Ingest (companion .md for non-markdown, embedded image normalization), atomic splitting, progressive distillation, color-coded highlighting that semantically links and relates ideas within and across projects (liberal application, perspective-based lenses, drift gradients, and multi-angle layering/switching), frontmatter enrichment, hub/MOC linking, action extraction, archiving, resurface-candidate marking, and early express/output generation.

**Decision Wrappers and user guidance are core.** Low- or ambiguous-confidence outcomes flow into Decision Wrappers (A–G, `approved_path`, `user_guidance`); you approve or refine, then EAT-QUEUE applies. That is the primary mechanism for AI guidance. Log flags such as #review-needed may remain as a **complementary** signal where useful, but the core path is wrapper + approval + re-run.

**Task and roadmap tracking** stay manual-first and central, with AI assistance for validation, formatting, and logging. Roadmaps are where you interact with progress (add, complete, expand, reorder, duplicate, merge, export, or report via mobile toolbar queues). Processing only runs on explicit triggers like EAT-QUEUE, so user intent drives changes. Roadmaps live in 1-Projects/…/Roadmap/ with standard formats for Dataview/Tasks integration. Onboarding focuses on real-project immersion: discovery → minimal setup → project feeding → personalization.

**The system leverages the mobile–laptop divide:** mobile as the agile hub for quick input (manual highlights/seeds, queuing actions during “brain ingestion”), async queues as reflection buffers for iterative shaping and refinement, and laptop (via Cursor) as the engine for deep AI processing (e.g. blending perspectives, simulating impacts, generating previews). This hybrid gives resilient human–AI synergy—shallow mobile triggers lead to deeper laptop outcomes, with async pauses for review, personalization, and error resilience.

**Trustworthiness:** High-confidence (≥85%) actions follow per-change snapshots; moves use dry-run then commit. **Mid-confidence (68–84%)** uses async refinement loops (self-critique plus user-seeded feedback via mobile previews), proceeding only when post-loop confidence is ≥85% and a snapshot succeeds. Low confidence remains propose-only, with mobile-synced callouts for approval and shaping.

**Safety** is multi-layer: external backups first, in-vault per-change and batch snapshots, and async previews for pre-commit review.

**Observability and provenance:** Pipeline logs, loop-outcome fields, and Dataview provide a **clear provenance trail**—what changed, when, and from which run—plus queue analytics and feedback logs for auditing async flows and system evolution.

You get **maximum visual and relational clarity** without clutter: frontmatter, Dataview tables, callouts, project-linked Highlightr colors via **highlight_key** (project-level overrides), gradients for drift, layers for angles, and seeded weights from manual input, task lists, and graph hints—all shaped iteratively by user triggers.

**Highlightr colors** are a dynamic visual language: analogous for cohesion, complementary for contrasts, **project overrides via highlight_key**, perspective lenses (e.g. “combat systems” vs “performance”), drift gradients (relevance fade), and multi-angle switching/syncing (layered views, mobile exports during ingestion).

Optional flows (e.g. Garden review, Curate cluster) feed batches into pipelines, with async batch-shaping for vault-wide insights.

**In short:** Transform Obsidian into an external brain that ingests raw material and, once you trigger pipelines, autonomously organizes, distills, and expresses it—with mostly zero-manual input per run, Decision Wrappers and approval at the core of guidance, clear provenance, and a mobile–laptop split that keeps you in control while the system adapts resiliently to your inputs and delivers clear, actionable progress via roadmaps and tasks.

---

**Summary of v4.1 vs v4**

| Change | v4.1 |
|--------|------|
| Zero-Manual | Reframed as **“mostly zero-manual input”**; manual pipeline launch (Cursor limitation); mobile queue + laptop run as the pattern. |
| #review-needed | **Decision Wrappers** (and user guidance) described as **core**; #review-needed as **complementary** if kept. |
| highlight_key | **Restored** as the way to get “project overrides” (explicit **highlight_key** in the clarity and Highlightr bullets). |
| Audit trail | Renamed to **“clear provenance trail”** (what changed, when, which run); “provenance” used in the observability sentence. |

## What does this seem to mean?

_Quick reflection: why does this matter, how might it connect to existing notes, or what might you do with it?_

-  

## TL;DR

_Short summary so future-you can scan quickly._

-

## Review Needed
Proposed para-type: project. Assigned based on content/frontmatter (confidence ~70%). Do not move until reviewed.