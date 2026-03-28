# Mobile Seed–Enhance Flow

**Version: 2026-03 – post-subagent migration**

Describes how mobile users can add highlights (seeds) in notes and how SEEDED-ENHANCE extends them when EAT-QUEUE runs on the laptop.

---

## Purpose

Single reference for the mobile → Ingest/observe + laptop EAT-QUEUE path: mobile fills Ingest and may add `<mark>` seeds; queue and pipelines run on laptop; SEEDED-ENHANCE extends seeds with AI and color.

---

## Flow overview

1. **Mobile:** User observes and fills **Ingest/** (e.g. quick captures, pasted text). Mobile does **not** append to prompt-queue.jsonl or Task-Queue.md; queue writes are **laptop-only** (see Mobile-Migration-Spec). User may add **`<mark>`** highlights in a note as "seeds" for later enhancement.
2. **Laptop:** User (or automation) adds queue entries (e.g. INGEST MODE for new Ingest notes, or **SEEDED-ENHANCE** for notes that have user `<mark>` and should be extended with AI highlights). User runs **EAT-QUEUE** (or Process queue).
3. **Queue:** Dispatcher loads Queue rule. Step 0 runs; queue is read and ordered. Entry with **mode: SEEDED-ENHANCE** is dispatched to the **highlight-seed-enhance** skill (not to a pipeline subagent). Skill may be invoked in main context or via a small rule that runs the skill and logs Watcher-Result.
4. **highlight-seed-enhance:** Detects user `<mark>` with no `data-highlight-source`; treats them as cores (solid color). Extends with AI using analogous color and optional drift gradient. Does not move or rename notes; only adds/extends highlights and metadata.
5. **Watcher-Result:** One line per processed SEEDED-ENHANCE entry appended to Watcher-Result.md (requestId, status, message, trace, completed).

---

## Key points

- **Mobile = observe + fill Ingest.** No queue writes from mobile. Commander / Crafter / manual edit on laptop add queue entries; EAT-QUEUE runs on laptop.
- **SEEDED-ENHANCE** is a **queue mode**; it is dispatched by the Queue rule (per auto-eat-queue dispatch table). It uses the **highlight-seed-enhance** skill. Optional: **mobile-seed-detect** context rule can tag or surface notes with `<mark>` for later SEEDED-ENHANCE queue entry.
- **highlight-seed-enhance** is non-destructive in the move/rename sense; it updates note content (highlights) and frontmatter. Backup and snapshot policies still apply if the skill does substantial rewrites; see skill definition and core-guardrails.

---

## References

- Mobile-Migration-Spec (laptop-only queue, mobile Ingest)
- [Skills/Distill-Highlight-Skills](../Skills/Distill-Highlight-Skills.md) (highlight-seed-enhance)
- `.cursor/rules/context/mobile-seed-detect.mdc` (if present)
- Queue-Sources (SEEDED-ENHANCE mode)
