---
title: Research Log
created: 2026-03-11
tags: [pkm, second-brain, logs, research, observability]
para-type: Resource
status: active
---

# Research Log

One line per research run (pre-deepen, RESEARCH-AGENT, or gap-fill). Enables visibility when research ran but produced 0 notes.

**Format:** `timestamp | project_id | linked_phase | outcome: notes_created | empty | failed | exception | reason_if_not_notes_created | note_count`

**Who writes:** research-agent-run (skill) appends one line when the run finishes; optionally auto-roadmap (pre-deepen caller) or roadmap-deepen (gap-fill) may append when they invoke research. See [[3-Resources/Second-Brain/Logs#Pipeline logs|Logs § Pipeline logs]].

2026-03-15 12:35 | genesis-mythos-master | Phase-1 | outcome: notes_created | reason: 1 note | note_count: 1
2026-03-15 12:05 | genesis-mythos-master | Phase-1 | outcome: notes_created | reason: pre-deepen RESEARCH_AGENT; 1 synthesized note | note_count: 1
2026-03-15 12:21 | genesis-mythos-master | Phase-1-1 | outcome: notes_created | reason: pre-deepen RESEARCH_AGENT; 1 note for Key Abstractions | note_count: 1
2026-03-19 19:12 | genesis-mythos-master | Phase-2-1 | outcome: notes_created | reason: pre-deepen inline research-agent-run; web_search synthesis | note_count: 1

