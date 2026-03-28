---
title: Prompt-Crafter Param Table
created: 2026-03-10
tags: [pkm, second-brain, prompt-crafter, params, plan-mode]
para-type: Resource
status: active
links: ["[[Resources Hub]]", "[[3-Resources/Second-Brain/README]]", "[[Prompt-Crafter-Structure-Detailed]]", "[[Queue-Sources]]", "[[Parameters]]"]
---

# Prompt-Crafter Param Table

Single source for **which params** the question-led crafter asks, **in what order** (question_order), **who owns them** (parentage), **who consumes them** (used_by), and **which accept manual text** (accepts_manual_text). The agent uses this table to standardize the question list so it is always in a predictable order. New params added to Queue-Sources or Parameters should get a row here and a question_order. Canonical question text and option wording for the question-led crafter are in [[3-Resources/Second-Brain/User-Questions-and-Options-Reference|User-Questions-and-Options-Reference]] §1; the agent should use that doc for exact phrasing and order. The agent must ask every param in §1 "Param order by branch" for the chosen branch; no skips. For question-led crafting, the **order** in which questions are asked is defined **only** in User-Questions-and-Options-Reference §1 "Param order by branch". This table matches that order; if it diverges, §1 wins. Do not skip any param in that list.

---

## Column definitions

| Column                  | Meaning                                                                                                                        |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| **param**               | Param name (e.g. enable_research, user_guidance).                                                                              |
| **parentage / owner**   | Kickoff and sub-mode that owns it (e.g. ROADMAP → RESUME-ROADMAP, CODE → INGEST MODE).                                         |
| **used_by**             | Pipeline, skill, or queue processor that consumes it.                                                                          |
| **question_order**      | Position in the question list for that owner (integer); agent asks in this sequence.                                           |
| **accepts_manual_text** | true = param takes free-text input; when included, agent asks "What is the [param]?" in manual text phase after all optionals. |

---

## ROADMAP kickoff

### ROADMAP MODE (setup only)

| param | parentage / owner | used_by | question_order | accepts_manual_text |
|-------|-------------------|---------|----------------|---------------------|
| project_id | ROADMAP → ROADMAP MODE | roadmap-generate-from-outline | 1 | false |
| source_file / seed note path | ROADMAP → ROADMAP MODE | roadmap-generate-from-outline | 2 | true |

### RESUME-ROADMAP (continue)

| param | parentage / owner | used_by | question_order | accepts_manual_text |
|-------|-------------------|---------|----------------|---------------------|
| action | ROADMAP → RESUME-ROADMAP | auto-roadmap | 1 | false |
| project_id | ROADMAP → RESUME-ROADMAP | auto-roadmap, roadmap-deepen | 2 | false |
| phase | ROADMAP → RESUME-ROADMAP | auto-roadmap, roadmap-deepen | 3 | false |
| sectionOrTaskLocator | ROADMAP → RESUME-ROADMAP | expand-road-assist, roadmap-deepen | 4 | true |
| enable_context_tracking | ROADMAP → RESUME-ROADMAP | auto-roadmap, roadmap-deepen | 5 | false |
| enable_research | ROADMAP → RESUME-ROADMAP | auto-roadmap, research-agent-run | 6 | false |
| research_queries | ROADMAP → RESUME-ROADMAP | research-agent-run | 7 | true |
| research_result_preference | ROADMAP → RESUME-ROADMAP | research-agent-run | 8 | false |
| research_focus | ROADMAP → RESUME-ROADMAP | research-agent-run | 9 | false |
| candidate_urls | ROADMAP → RESUME-ROADMAP | research-agent-run | 10 | true |
| research_max_escalations | ROADMAP → RESUME-ROADMAP | research-agent-run | 11 | false |
| async_research | ROADMAP → RESUME-ROADMAP | auto-roadmap | 12 | false |
| research_distill | ROADMAP → RESUME-ROADMAP | auto-roadmap | 13 | false |
| handoff_gate | ROADMAP → RESUME-ROADMAP | auto-roadmap, hand-off-audit | 14 | false |
| min_handoff_conf | ROADMAP → RESUME-ROADMAP | auto-roadmap | 15 | false |
| inject_extra_state | ROADMAP → RESUME-ROADMAP | roadmap-deepen | 16 | false |
| token_cap | ROADMAP → RESUME-ROADMAP | roadmap-deepen | 17 | false |
| max_depth | ROADMAP → RESUME-ROADMAP | roadmap-deepen | 18 | false |
| branch_factor | ROADMAP → RESUME-ROADMAP | roadmap-deepen | 19 | false |
| profile | ROADMAP → RESUME-ROADMAP | auto-roadmap (merge prompt_defaults.roadmap) | 20 | false |
| userText | ROADMAP → RESUME-ROADMAP | expand-road-assist | 21 | true |
| queue_next | ROADMAP → RESUME-ROADMAP | auto-roadmap | 22 | false |
| roadmap_track | ROADMAP → RESUME-ROADMAP | auto-roadmap, Layer 1 effective_track | 23 | false |

---

## CODE kickoff

### CODE → INGEST MODE

Order matches User-Questions-and-Options-Reference §1 Message sequence (pipeline set by Message 2, then context_mode → max_candidates → rationale_style → optional distill_lens → source_file → user_guidance).

| param | parentage / owner | used_by | question_order | accepts_manual_text |
|-------|-------------------|---------|----------------|---------------------|
| context_mode | CODE → INGEST MODE | classify_para, propose_para_paths | 1 | false |
| max_candidates | CODE → INGEST MODE | propose_para_paths, wrapper pad | 2 | false |
| rationale_style | CODE → INGEST MODE | MCP propose_para_paths | 3 | false |
| distill_lens | CODE → INGEST MODE | distill-highlight-color, highlight-perspective | 4 | true (if included) |
| source_file | CODE → INGEST MODE | auto-eat-queue, full-autonomous-ingest | 5 | true |
| user_guidance / prompt | CODE → INGEST MODE | guidance-aware, distill/classify | 6 | true |
| profile | CODE → INGEST MODE | auto-eat-queue (merge prompt_defaults) | 7 | false |

### CODE → ORGANIZE MODE

| param | parentage / owner | used_by | question_order | accepts_manual_text |
|-------|-------------------|---------|----------------|---------------------|
| source_file | CODE → ORGANIZE MODE | auto-eat-queue, autonomous-organize | 1 | true |
| context_mode | CODE → ORGANIZE MODE | subfolder-organize, propose_para_paths | 2 | false |
| max_candidates | CODE → ORGANIZE MODE | propose_para_paths | 3 | false |
| profile | CODE → ORGANIZE MODE | auto-eat-queue | 4 | false |
| user_guidance / prompt | CODE → ORGANIZE MODE | guidance-aware | 5 | true |

### CODE → DISTILL MODE

| param | parentage / owner | used_by | question_order | accepts_manual_text |
|-------|-------------------|---------|----------------|---------------------|
| source_file | CODE → DISTILL MODE | auto-eat-queue, autonomous-distill | 1 | true |
| distill_lens | CODE → DISTILL MODE | auto-layer-select, distill-perspective-refine | 2 | true |
| depth / layers | CODE → DISTILL MODE | auto-layer-select | 3 | false |

### CODE → EXPRESS MODE

| param | parentage / owner | used_by | question_order | accepts_manual_text |
|-------|-------------------|---------|----------------|---------------------|
| source_file | CODE → EXPRESS MODE | auto-eat-queue, autonomous-express | 1 | true |
| express_view | CODE → EXPRESS MODE | express-mini-outline, express-view-layer | 2 | true |

### CODE → ARCHIVE MODE

| param | parentage / owner | used_by | question_order | accepts_manual_text |
|-------|-------------------|---------|----------------|---------------------|
| source_file | CODE → ARCHIVE MODE | auto-eat-queue, autonomous-archive | 1 | true |

### CODE → Task modes (TASK-ROADMAP, TASK-COMPLETE, ADD-ROADMAP-ITEM, EXPAND-ROAD, etc.)

| param | parentage / owner | used_by | question_order | accepts_manual_text |
|-------|-------------------|---------|----------------|---------------------|
| source_file | CODE → Task | auto-queue-processor, task skills | 1 | true |
| task_id | CODE → TASK-COMPLETE | task-complete-validate | 2 | true |
| prompt | CODE → ADD-ROADMAP-ITEM, EXPAND-ROAD | add-roadmap-append, expand-road-assist | 3 | true |
| sectionOrTaskLocator | CODE → EXPAND-ROAD | expand-road-assist | 4 | true |
| userText | CODE → EXPAND-ROAD | expand-road-assist | 5 | true |

---

## Sync and maintenance

- When adding a new param to [[3-Resources/Second-Brain/Queue-Sources|Queue-Sources]] or [[3-Resources/Second-Brain/Parameters|Parameters]], add a row here with parentage, used_by, question_order (append or slot into the right group), and accepts_manual_text.
- Question order is per **owner** (e.g. RESUME-ROADMAP has its own 1..18; INGEST MODE has 1..6). The question-led crafter filters rows by the selected kickoff and sub-mode, then sorts by question_order.
- Human-facing descriptions and defaults for each param live in [[3-Resources/Second-Brain/User-Questions-and-Options-Reference#param-descriptors-for-agents-and-param_meta-overlay|User-Questions-and-Options-Reference §1, Param descriptors (for agents and param_meta overlay)]]. Agents use that section to populate the optional `param_meta` overlay (`param_meta.<paramName>.description` / `defaultWhenC`); queue processors and pipelines treat `param_meta` as advisory-only and may ignore it without behavior change.
