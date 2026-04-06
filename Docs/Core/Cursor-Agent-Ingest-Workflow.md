---
title: Cursor Agent Ingest Workflow
created: 2026-03-07
tags: [second-brain, ingest, cursor-agent, workflow]
para-type: Resource
status: active
links: ["[[3-Resources/Second-Brain/README]]", "[[3-Resources/Second-Brain/Vault-Layout]]"]
---

# Cursor Agent Ingest Workflow

How to get Markdown produced by **Composer** or **Cursor cloud agents** (and **research synthesis notes** from research-agent-run) into the vault and into PARA without manual wrapper approval when confidence is high.

## Flow

1. **Cursor agent** produces Markdown (from master goal or phase notes), with frontmatter: `agent-generated: true`, `confidence_override: high`, `project-id`, `roadmap-level`, `created`. **Research synthesis notes** are created by research-agent-run under `Ingest/Agent-Research/` and get the same direct-move exception when conditions hold.
2. **Drop** the file(s) into [Ingest/Agent-Output/](Ingest/Agent-Output/) (or set the same frontmatter if you drop elsewhere in Ingest). Research notes already live in [Ingest/Agent-Research/](Ingest/Agent-Research/).
3. **Run:** **INGEST MODE: batch on Ingest/Agent-Output/** (or on Ingest/Agent-Research/ for research notes; uses documented batch ingest trigger from Pipelines.md / Queue-Alias-Table).
4. **If conditions hold** (conf ≥ 85% or `confidence_override: high`; not FORCE-WRAPPER; single clear path; and when `tech_level` is present, either high conf or tech_level 1): note is **moved directly** to PARA with provenance callout; Ingest-Log gets **#cursor-agent-direct** (and **tech_level** when applicable). Applies to both Agent-Output and Agent-Research notes.
5. **Else:** A Decision Wrapper is created; review and approve, then run **EAT-QUEUE** to apply.

**Boundary:** Direct move is an ingest policy branch. It does not redefine wrapper semantics; `approved: true` still means an approved wrapper note under `Ingest/Decisions/**`.
With `prompt_defaults.ingest.validator_block_agent_generated_without_wrapper: false`, validator output on this branch is advisory-only and does not hard-block movement by itself.

See [[.cursor/rules/context/para-zettel-autopilot#Cursor-agent direct move (Phase 1 — skip wrapper)|para-zettel-autopilot § Cursor-agent direct move]].

## Frontmatter for agent output

Every output Markdown file should start with:

```yaml
---
agent-generated: true
confidence_override: high   # or medium if uncertain parts
project-id: genesis-mythos-master
roadmap-level: secondary   # or primary / tertiary / task as appropriate
created: {{current-date}}
---
```

## Composer / cloud prompt (phase-aware)

Ramp tech depth by phase so early phases stay conceptual and late phases get pseudo-code:

- **Early phases (1–2):** User impacts only (e.g. "smoother UX for DMs"). No jargon.
- **Mid (3–4):** Architecture + tradeoffs, no code (e.g. "use event bus for modularity", "decouple simulation from render loop").
- **Late (5+):** Pseudo-code per task (2–5 lines), edge cases, data shapes, invariants.

Output per sub-phase as separate Markdown files with the frontmatter above. Filename: `kebab-slug-YYYY-MM-DD-HHMM.md`. Drop to Ingest/Agent-Output/; ingest skips wrapper when conf high.

## Technical progression

When [Second-Brain-Config](3-Resources/Second-Brain-Config) has `roadmap_tech_progression: true`, queue payloads can carry **tech_level** (from phase number). Notes with **tech_level > 1** in the **mid-band** (68–84% conf) do **not** get the direct move; they go through the refinement loop. See [[3-Resources/Second-Brain/Parameters#Confidence bands|Parameters § Confidence bands]].

## MOC validation query (optional)

To flag late-phase notes missing required depth after ingest, add to roadmap master/phase notes or MOC template:

```dataview
TABLE tech_level, file.link AS "Incomplete?"
WHERE tech_level >= 5 AND !contains(file.content, "pseudo-code")
SORT file.name
```
