---
title: Mobile Migration Spec — Observe and Ingest Only
created: 2026-03-10
tags: [pkm, second-brain, mobile, migration, plan-mode]
para-type: Resource
status: active
links: ["[[Resources Hub]]", "[[3-Resources/Second-Brain/README]]", "[[Queue-Sources]]", "[[Backbone]]", "[[Vault-Layout]]", "[[Commander-Plugin-Usage]]"]
---

# Mobile Migration Spec — Observe and Ingest Only

Mobile is **fully migrated** to **manual observation** and **filling the Ingest folder** only. Queue-based prompting and prompt crafting from mobile are deprecated; all queue consumption and Plan-mode crafting happen on the **laptop**.

---

## Target state (mobile)

- **Manual observation** — User reads and reviews notes, MOCs, roadmap state on mobile. No queue appends, no prompt-crafting flows.
- **Filling Ingest folder** — User creates or moves content into `Ingest/` (e.g. quick captures, drafts, links to process later). Processing happens when the user is on the laptop (EAT-QUEUE or paste crafted payload); existing pipelines (full-autonomous-ingest, etc.) run unchanged.

---

## Wiring to rework

| Component | Change |
|-----------|--------|
| **Watcher** | On mobile: do not append to prompt-queue.jsonl (or restrict "Prompt Modal" / queue append to observation-only or disable). EAT-CACHE / copy-queue-to-clipboard remains a **laptop-side** flow (paste into Cursor Plan mode). |
| **Commander** | On mobile: hide or repurpose macros that append to prompt-queue or Task-Queue (e.g. "Resume Roadmap", "Craft Deepen Aggressive", "Async Approve" that inject queue entries). Show only commands that support **observation** and **Ingest** (e.g. "New note in Ingest", "Move to Ingest"). |
| **prompt-queue.jsonl / Task-Queue.md** | Written **only from laptop**: Plan-mode crafter, Commander macros on laptop, or manual edit. Mobile does **not** append. Document in Queue-Sources and Queue-Alias-Table. |
| **Mobile-Pending-Actions** | No longer used as a primary way to "queue" work from mobile. Optionally keep as a **read-only** checklist of things to do on laptop (e.g. "Process Ingest", "Run RESUME-ROADMAP for project X") without auto-appending to queue files. |
| **Rules: watcher-result-append** | Clarify that queue-based and task-queue runs are **laptop-originated**; mobile does not send queue entries. |
| **Rules: auto-eat-queue** | No expectation of mobile-originated queue entries; EAT-CACHE / prompt-queue.jsonl are filled by Plan-mode crafting or Commander on laptop. |
| **Rules: auto-queue-processor** | Same for Task-Queue.md — consumed on laptop only. |
| **Rules: confidence-loops** | Async approval (e.g. approved: true + re-queue) remains valid on **laptop**. Remove or reframe mobile-specific "Async Approve" as "approve on laptop when reviewing Mobile-Pending-Actions". |
| **Rules: mobile-seed-detect** | Mobile can add content (e.g. `<mark>`) into notes in Ingest or elsewhere; **triggering** SEEDED-ENHANCE is a **laptop** action (user runs EAT-QUEUE with a queue that references that note, or Plan-mode CODE → DISTILL/SEEDED-ENHANCE). |
| **Queue-Sources / Queue-Alias-Table** | State explicitly that prompt-queue.jsonl and Task-Queue.md are written only from laptop. Remove or qualify "Mobile stub" / "Mobile-Pending-Actions" that implied mobile-originated queue flow. |
| **Vault-Layout (toolbar / mobile)** | Document: mobile toolbar = observation + Ingest only; queue and crafting = laptop only. |
| **Backbone** | State: mobile = observe + fill Ingest; queue and crafting = laptop only. Update "Mobile veto incomplete" / remaining gaps to reflect this migration. |
| **Commander-Plugin-Usage** | Document configuration: on mobile, hide queue-append commands; show only observation and Ingest commands. |

---

## Processing (laptop)

All queue consumption (EAT-QUEUE, PROCESS TASK QUEUE) and Plan-mode crafting happen on the **laptop**. When the user returns to the laptop, they run EAT-QUEUE (or paste a crafted payload); anything in Ingest/ is then processed by existing pipelines. MCP and backup safety rules are unchanged.
