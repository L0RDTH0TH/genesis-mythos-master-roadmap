---
title: Phase 4 Artifacts — deferred (export repo only until restored)
created: 2026-03-28
tags: [roadmap, genesis-mythos-master, phase-4, artifact, stub, ops]
para-type: Project
project-id: genesis-mythos-master
status: deferred
---

# Phase 4 Artifacts — deferred (export repo only)

**TL;DR** — Three roadmap artifacts are **named and required** in [[phase-4-1-1-10-auditable-path-check-contract-and-example-witness-appendix-roadmap-2026-03-25-0003|phase-4-1-1-10]] (A-41110-01 … 03) but **do not live in this vault tree** yet. They **did** exist as real (non-empty) markdown in the **GMM GitHub export** repo. **Ignore** until you need them; then restore from git (or copy from export checkout) into **this folder**.

## Canonical relative paths (vault)

All three belong here:

`Roadmap/Phase-4-Perspective-Split-and-Control-Systems/Artifacts/`

| Anchor | File |
|--------|------|
| A-41110-01 | `rollup-gatechecklist-v0-evidence-index-2026-03-26.md` |
| A-41110-02 | `appendwitness-v0-outcome-matrix-2026-03-26.md` |
| A-41110-03 | `witnessrefhash-v0-registry-promotion-plan-2026-03-26.md` |

## Where they are until restored

- **Local export checkout (if present):** `/home/darth/Documents/gmm-roadmap-export` — use git history on that repo **before** commit `30d620f` (e.g. tree at `1722d1c`) for the three paths above under `Roadmap/Phase-4-Perspective-Split-and-Control-Systems/Artifacts/`.
- **Remote:** GitHub repo `genesis-mythos-master-roadmap` — same paths on an ancestor of `main` from before the vault→export sync that dropped those files.

## Policy

- **Until needed:** do not block roadmap work on these files; 4.1.1.10 already documents intent and acceptance hooks.
- **When needed:** restore the three files into this `Artifacts/` folder, then resume any closure work that assumes on-disk artifacts.

## Why this note exists

A one-way rsync from vault → export used `--delete` and removed the export copies because the vault had an **empty** `Artifacts/` directory. The artifact bodies were never present under the vault path at that time; only this stub records where to get them next time.
