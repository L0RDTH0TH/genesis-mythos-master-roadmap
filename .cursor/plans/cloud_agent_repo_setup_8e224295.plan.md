---
name: Cloud agent repo setup
overview: Set up the genesis-mythos-master Git repo with the four essentials (goals/, config/, agents/, existing Roadmap/) so a cloud agent can self-onboard and produce granular, pseudo-code-depth roadmaps from the master goal and tech-level ramp. Uses Phase/Subphase terminology and integrates master-goal normalization and SDLC alignment.
todos: []
isProject: false
---

# Cloud agent repo setup for genesis-mythos-master

## Master goal template & normalization (already in place)

- **Master goal template**: [Templates/Master-Goal.md](Templates/Master-Goal.md) defines the normalized structure (One-line, Vision, Phases, Technical Integration, TL;DR, Related). Phases use `### Phase N — <Name>` for roadmap parsing.
- **Normalization in roadmap pipeline**: The **normalize-master-goal** skill runs when **ROADMAP MODE – generate from outline** is used and the seed note is a PMG (`is_master_goal: true` or path matches `*Master*Goal`*). It restructures the note to the template before phase parsing; see [.cursor/skills/normalize-master-goal/SKILL.md](.cursor/skills/normalize-master-goal/SKILL.md) and [Cursor-Skill-Pipelines-Reference](3-Resources/Second-Brain/Cursor-Skill-Pipelines-Reference.md). The cloud repo’s `goals/` file can be normalized to this template before or when feeding the agent.

---

## Current state

- **Repo root**: [1-Projects/genesis-mythos-master/](1-Projects/genesis-mythos-master/) — already a Git repo (`.git` present), with [.gitignore](1-Projects/genesis-mythos-master/.gitignore) excluding OS/editor/temp files.
- **Master goal**: The file `genesis-mythos-master-goal-2026-03-07-0033.md` is **not** at project root (it was moved there per Ingest-Log but no longer exists there). The full vision lives in [Roadmap/Source-genesis-mythos-master-goal-2026-03-07-0033-2026-03-07-1200.md](1-Projects/genesis-mythos-master/Roadmap/Source-genesis-mythos-master-goal-2026-03-07-0033-2026-03-07-1200.md) (Source note used for roadmap generation).
- **Phase roadmaps**: Present under `Roadmap/` (e.g. [Phase-6-Prototype-Scope/Phase-6-Prototype-Scope-Roadmap-2026-03-07-1200.md](1-Projects/genesis-mythos-master/Roadmap/Phase-6-Prototype-Scope/Phase-6-Prototype-Scope-Roadmap-2026-03-07-1200.md)); high-level stubs, no pseudo-code yet — ideal for agent to deepen.
- **Tech progression**: Defined in vault at [3-Resources/Second-Brain-Config.md](3-Resources/Second-Brain-Config.md) (`roadmap_tech_progression`, `tech_levels`); not yet inside the cloned repo.
- **No** `goals/`, `config/`, or `agents/` in the repo today.

All paths below are relative to **1-Projects/genesis-mythos-master/** (the repo the cloud agent clones).

---

## 1. Master goal (must-have)

- **Create** `goals/` and add `**goals/genesis-mythos-master-goal-2026-03-07-0033.md`**.
- **Content**: Use the existing Source note [Roadmap/Source-genesis-mythos-master-goal-2026-03-07-0033-2026-03-07-1200.md](1-Projects/genesis-mythos-master/Roadmap/Source-genesis-mythos-master-goal-2026-03-07-0033-2026-03-07-1200.md) as the source of truth. Optionally trim the "AI Output Capture" wrapper so the file is a direct master-goal doc (title + frontmatter + Full output / Master Goal v2.0 + Technical Integration + Target prototype scope); keep `user_guidance` in frontmatter for future agent nudges (e.g. "Force exhaustive tasks with pseudo-code on phases 5+").
- **Why**: Agent starts here for full vision; dashboard prompt can say "From goals/genesis-mythos-master-goal-2026-03-07-0033.md".

---

## 2. Config / progression reference (recommended)

- **Create** `config/` and add `**config/roadmap-config.yaml`**.
- **Content**: Extract from [3-Resources/Second-Brain-Config.md](3-Resources/Second-Brain-Config.md) (lines 43–47) and mirror in YAML for easy parsing:

```yaml
roadmap_tech_progression: true
tech_levels:
  level_1: high-concept   # Phase 1 - Subphase 1
  level_2: mid-tech       # Subphase 3 - Subphase 4
  level_3: pseudo-code   # Subphase 5+
```

- **Why**: Agent can "Read config/roadmap-config.yaml → apply tech_levels ramp" so outputs follow early user-impact, late pseudo-code. Terminology aligns with Phase/Subphase granularity (not raw phase ranges).

---

## 3. Prompt template (high-value)

- **Create** `agents/` and add `**agents/roadmap-prompt-template.md`**.
- **Content**: Use the template below (Core Requirement, Technical Progression Ramp with Phase/Subphase wording, Output Format, Input Sources). Paths are relative to this repo.
- **Why**: Single source of truth for the locked prompt; cloud dashboard says "Follow agents/roadmap-prompt-template.md exactly. Use the master goal from goals/genesis-mythos-master-goal-2026-03-07-0033.md."

### Full template (agents/roadmap-prompt-template.md)

```markdown
# Roadmap Generation Prompt Template

**Core Requirement**
A Roadmap is **not complete** unless a competent mid-level programmer could implement it blind from this alone — every task broken to smallest implementable units with pseudo-code (2–5 lines max per task), key edge cases (1–4 bullets), data shapes/invariants (YAML-like or prose).

**Technical Progression Ramp** (enforced by phase/subphase)
- **Phase 1 – Subphase 1**: High-concept only (user impacts, UX/timeline effects, no jargon/tech details)
- **Subphase 3 – Subphase 4**: Mid-tech (architecture patterns, tradeoffs, modularity seams — no code)
- **Subphase 5+**: Pseudo-code depth (exhaustive tasks, edges, data shapes, invariants)

**Output Format**
- One Markdown file per phase/subphase
- Each file MUST start with this exact YAML frontmatter (example; in the real file use a fenced ```yaml block):

      ---
      agent-generated: true
      confidence_override: high
      project-id: genesis-mythos-master
      roadmap-level: subphase
      tech_level: 3
      created: "{{current-date}}"
      ---

- Structured content: Headings (# Phase X — Title), checklists (- [ ] Task title), pseudo-code blocks (```pseudo), edge cases bullets, data shapes section
- Commit to new branch (e.g. agent-roadmap-vX) with clear messages
- If possible, produce video demo/logs/screenshots of generation process

**Input Sources**
- Master goal: goals/genesis-mythos-master-goal-2026-03-07-0033.md
- Config: config/roadmap-config.yaml (tech_levels ramp: Phase 1 - Subphase 1 → Subphase 5+)
- Existing phases: Roadmap/Phase-1-Perspective-Split/, … , Roadmap/Phase-6-Prototype-Scope/ (Phase-N-*-Roadmap-*.md inside each)

Generate exhaustive roadmap now.
```

---

## 4. Existing phase / roadmap notes (optional but boosts depth)

- **No structural change.** Phase roadmaps already live under `Roadmap/`:
  - `Roadmap/Phase-1-Perspective-Split/Phase-1-Perspective-Split-Roadmap-2026-03-07-1200.md`
  - … through Phase-6.
- **Prompt template** will explicitly list these paths under "Input Sources" so the agent deepens them (e.g. turn Phase 6 stubs into pseudo-code tasks/edges) instead of reinventing from scratch.

---

## 5. Optional: README at repo root

- **Add** `README.md` in the repo root (one short section) explaining:
  - This repo is context for the cloud roadmap agent.
  - Start from `goals/genesis-mythos-master-goal-2026-03-07-0033.md`; follow `agents/roadmap-prompt-template.md`; apply `config/roadmap-config.yaml`; deepen `Roadmap/Phase-`* if present.
  - Where useful, align agent deliverables with **Software Development Life Cycle (SDLC)** expectations (phases, quality gates, hand-off readiness).
- **Why**: Self-onboarding and future you; no overstuff.

---

## File layout (after setup)

```text
genesis-mythos-master/
├── README.md                    # optional: how agent uses this repo
├── goals/
│   └── genesis-mythos-master-goal-2026-03-07-0033.md
├── config/
│   └── roadmap-config.yaml
├── agents/
│   └── roadmap-prompt-template.md
├── Roadmap/                     # existing
│   ├── genesis-mythos-master-Roadmap-2026-03-07-1200.md
│   ├── Source-genesis-mythos-master-goal-2026-03-07-0033-2026-03-07-1200.md
│   ├── Phase-1-Perspective-Split/...
│   ├── ... Phase-2–5 ...
│   └── Phase-6-Prototype-Scope/...
├── genesis-mythos-roadmap.md
├── genesis-mythos-master-Roadmap-MOC.md
└── .gitignore
```

---

## Usage (dashboard prompt)

After setup, the cloud agent prompt can be:

- "Follow the instructions in **agents/roadmap-prompt-template.md** exactly. Use the master goal from **goals/genesis-mythos-master-goal-2026-03-07-0033.md** as input. Apply the tech ramp from **config/roadmap-config.yaml**. Deepen existing phase notes under **Roadmap/** where present. Generate exhaustive roadmap; commit to branch agent-roadmap-v1 (or similar)."

---

## Out of scope (per your note)

- **fixtures/** for agent self-testing: Not present yet; when added, use **Software Development Life Cycle (SDLC)** as the standard for test inputs, acceptance criteria, or quality gates so agent outputs align with lifecycle phases and hand-off readiness.
- **Vault ingest after run**: Agent commits branch/PR; you pull/download Markdowns and drop to `Ingest/Agent-Output/` for vault autopilot — no change in this plan.

---

## Summary


| Item                                 | Action                                                                                                                                            |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| Master goal template & normalization | Already in vault: [Templates/Master-Goal.md](Templates/Master-Goal.md); normalize-master-goal runs in ROADMAP MODE when seed is PMG               |
| Master goal                          | Create `goals/` and `goals/genesis-mythos-master-goal-2026-03-07-0033.md` from Roadmap Source note (normalize to Master-Goal template if desired) |
| Config                               | Create `config/roadmap-config.yaml` with `tech_levels`: level_1 = Phase 1 - Subphase 1, level_2 = Subphase 3 - Subphase 4, level_3 = Subphase 5+  |
| Prompt template                      | Create `agents/roadmap-prompt-template.md` with full template (see §3 above); Phase/Subphase terminology                                          |
| Phase notes                          | Leave as-is; reference in template as `Roadmap/Phase-*/...`                                                                                       |
| README                               | Optional: root `README.md`; mention SDLC alignment for agent deliverables                                                                         |
| Fixtures                             | None yet; when added, use SDLC as standard for test inputs / quality gates                                                                        |


No edits to existing Roadmap files or .gitignore are required unless you want the README to be the only new root file.