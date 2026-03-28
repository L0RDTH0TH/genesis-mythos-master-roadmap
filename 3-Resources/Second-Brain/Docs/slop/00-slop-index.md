---
title: Docs slop — flat mirror of Second-Brain/Docs
created: 2026-03-21
tags: [second-brain, docs, mirror]
para-type: Resource
status: active
source: "Flattened copy of sibling files under 3-Resources/Second-Brain/Docs/ (excluding this slop folder)."
---

# Slop folder (flat mirror)

This directory is a **flattened copy** of everything under **`3-Resources/Second-Brain/Docs/`** except **`slop/`** itself (no recursion).

- **Naming:** Each path under `Docs/` becomes one filename: `/` → `--`. Examples: `README.md` stays `README.md`; `Pipelines/Ingest-Pipeline.md` → `Pipelines--Ingest-Pipeline.md`; `Subagents/Architecture.md` → `Subagents--Architecture.md`.
- **Authoritative tree:** Browse the real folders (`Pipelines/`, `Subagents/`, `Rules/`, etc.) in `Docs/`; this folder is for search, export, or tools that want a single flat directory.
- **Regeneration:** Delete everything in `slop/` except this index (or delete all and recreate), then re-run the flatten copy from `Docs/` excluding `slop/`.
