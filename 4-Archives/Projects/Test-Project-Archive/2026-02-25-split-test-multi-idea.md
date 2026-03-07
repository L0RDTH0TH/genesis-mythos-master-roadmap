---
title: Ingest split test — multi-idea note
created: 2026-02-25
para-type: Ingest
status: raw
---

# Ingest split test — multi-idea note

Raw capture for **full-autonomous-ingest** pipeline validation. Contains multiple distinct ideas so that `obsidian_split_atomic` can split it and **split-link-preserve** can add traceability (split_from / split_into).

**To test:** Copy this note to `Ingest/` then run the full ingest pipeline (process Ingest).

## First idea — progressive summarization

Progressive summarization means bolding key phrases first, then highlighting the most important, then adding a TL;DR. You do it in layers so you don't have to do everything at once.

## Second idea — archive heuristics

Archive candidates should have no open tasks, status complete, and be past an age threshold. Cross-check linked notes in the same project so you don't archive something that's still referenced by active work.

## Third idea — express pipeline

The express pipeline turns distilled notes into shareable output: related-content-pull finds similar notes, express-mini-outline adds an outline block, and call-to-action-append adds a Share/Publish-style callout at the end.

---

*Expect 3 atomic child notes and traceability links (split_from / split_into) after ingest.*
