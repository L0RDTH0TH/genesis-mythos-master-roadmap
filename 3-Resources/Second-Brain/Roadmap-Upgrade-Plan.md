---
title: Roadmap Upgrade Plan – Automating Deep Hierarchy & Cursor Iteration
created: 2026-03-08
tags: [roadmap, automation, cursor, genesis-mythos-master, upgrade]
para-type: Resource
status: active
links: ["[[Backbone]]", "[[Roadmap-Quality-Guide]]", "[[Pipelines]]", "[[Roadmap Structure]]"]
---

# Roadmap Upgrade Plan – Automating Deep Hierarchy & Cursor Iteration

**Cursor version assumption:** Assumes Cursor ≥2.6.x (March 2026 stable builds, e.g. 2.6.11 per recent changelogs). Verify: Help → About Cursor. If <2.6, expect potential queued-message regressions (Jan–Feb 2026 reports). Prefer `.cursor/rules/*.mdc` format over legacy .cursorrules; fallback to legacy .cursorrules or single `.cursor/rules/main.mdc` if needed.

---

## 1. Goals of the upgrade

- **Full hierarchy adoption:** master → primary → secondary → tertiary → tasks per [[Roadmap Structure]] (generalized P×S×T×J model).
- **Progressive technical depth:** Phase 1 high-level conceptual; Phases 2–4 mid-technical (interfaces, data flows); Phases 5–6 pseudo-code/APIs/edges. Align with existing `tech_level` / `roadmap_tech_progression` in [[Queue-Sources]] and [[Parameters]] where applicable.
- **Semi-to-high automation:** Cursor Agent populates queue (EXPAND-ROAD, RESUME-ROADMAP), creates/expands notes and folders, updates state, chains iterations with minimal manual triggers; use existing EAT-QUEUE and `.technical/prompt-queue.jsonl`.
- **Safety:** Snapshots before changes (obsidian-snapshot, roadmap-state before/after), drift checks (RECAL-ROAD), approval gates (Plan mode, Decision Wrappers) per existing rules.
- **Target:** From current Phase 1 depth to 5–10× deeper content per phase, auto-chained across phases until complete or blocked.

---

## 2. Phase A: Preparation and setup (1–2 hours manual)

### Queue

- Queue file: **`.technical/prompt-queue.jsonl`** (not vault root). See [[Queue-Sources]].
- **.cursorignore:** Ensure `.technical/prompt-queue.jsonl` is **not** ignored; confirm Agent can read and write it (already per Queue-Sources; verify before running automation).

### State and automation tracking (Option B — adopted)

Add **workflow_state.md** under `1-Projects/<project_id>/Roadmap/` (e.g. `1-Projects/genesis-mythos-master/Roadmap/workflow_state.md`) as the single run-time automation state file. **Integration:** [[1-Projects/Test-Project/Versions/post-Monolithic/temp/roadmap-state]] remains the source of truth for phase completion and drift; workflow_state is read/written by the Agent loop and optionally by roadmap-resume/expand skills. Document in [[Vault-Layout]] § Roadmap state artifacts.

#### workflow_state.md schema (minimum + tracker)

**Frontmatter:**

| Field | Description |
|-------|-------------|
| `current_phase` | int (e.g. 1) |
| `current_subphase_index` | string or null (e.g. `"1.1.2"`) |
| `status` | `in-progress` \| `blocked` \| `complete` |
| `automation_level` | `semi` \| `high` \| `manual` |
| `last_auto_iteration` | ISO timestamp |
| `iterations_per_phase` | object: phase number → count (e.g. `"1": 3`, `"2": 0`) |
| `max_iterations_per_phase` | enforcement cap (default **80**; hard ceiling when set); synced with `prompt_defaults.roadmap.max_iterations_per_phase` in Config |
| `max_iterations_total` | optional global cap (e.g. 50) |

**Body:** `## Log` (append-only) — **10-column** table:

- **Header:**  
  `Timestamp | Action | Target | Iter Obj | Iter Phase | Ctx Util % | Leftover % | Threshold | Est. Tokens / Window | Status / Next`
- **Semantics:**  
  - **Iter Obj / Iter Phase** — iterations for the specific object and for the current phase (unchanged from earlier plan).  
  - **Ctx Util % / Leftover % / Threshold / Est. Tokens / Window** — context utilization tracking fields populated by roadmap-deepen when `enable_context_tracking` is true (see Parameters and Config). When tracking is off, these four columns are written as `"-"`.  
  - **Status / Next** — status plus the next queued action (e.g. `next deepen`, `RECAL-ROAD queued`, `paused-high-util`).

Example row (with tracking and a threshold breach):  
`2026-03-09T03:12 | deepen | Phase-5-Compute-Shader | 8 | 8 | 82% | 18% | 80% | 104832 / 128000 | RECAL-ROAD queued (paused-high-util)`

**Update rule:** After successful expand/create: increment `iterations_per_phase[phase]`; append one row to log. Before loop iteration: if `iterations_per_phase[current_phase] ≥ max_iterations_per_phase`, queue RECAL-ROAD and set `status: blocked` with note "cap reached"; do not append new EXPAND. Optionally enforce `max_iterations_total` across all phases.

- **Util-driven research injection (v1):** When the last workflow_state log row has a valid **Ctx Util %** value **below** `research_util_threshold` (default **30%**) and the current roadmap position is **secondary or deeper** (**`current_depth ≥ 2`**, derived from `current_subphase_index` as `1 + count('.')`), the auto-roadmap deepen branch may auto-set `enable_research` internally (subject to **research_cooldown**, e.g. every 3 iterations in that phase, and always respecting an explicit `params.enable_research === false` opt-out). **Primaries (phase containers at depth 1) are intentionally excluded from util-based research** so high-level planning remains internal. **Prefer frontmatter** `last_ctx_util_pct` on workflow_state (written by roadmap-deepen after each append); fallback to parsing the Log table. **Quality veto:** only enable from util when **last row confidence < research_conf_veto_threshold** (default 85). See Parameters § Research (pre-deepen) for `research_util_threshold` / `research_cooldown` and Queue-Sources § RESUME-ROADMAP params for async_research and injected_research_paths.

- **Inward gaps → targeted research:** During deepen, **gap detection** runs on the draft (step 4.5 in roadmap-deepen): word-count + **research_gap_markers** (e.g. pseudo-code, edges, examples) flag shallow or missing sections; **severity** (0–100) and **gap_severity_threshold** (default 60) determine whether to trigger outward research. When high-severity gaps exist, research-agent-run is invoked in **gap-fill** mode; **~70% of queries** target the gaps; results are injected as **## External Grounding** / Filled Gap sections before the note is written. **Confidence gates:** fill_conf ≥ 68% to inject; optional **research_verify** to re-query sources. **Async:** persist **injected_research_paths** in workflow_state (or state note) so the next RESUME-ROADMAP run can "resume from last injected" even if the queue batch failed. See Parameters § Gap detection, roadmap-deepen § Gap detection design, research-agent-run § gap-fill mode.

### Clean, consistent Cursor output

Reference and extend existing vault output (e.g. [[.cursor/rules/always/watcher-result-append]], pipeline log fields in [[Logs]], Ingest-Log format). Require:

1. **One-line summary per action** (e.g. "Expanded Phase 1.1 → 3 tertiary notes; iterations_phase_1: 2").
2. **Structured fields:** `action`, `target` (path or object_id), `iterations_this_object`, `iterations_this_phase`, `next_queued`.
3. **Append to workflow_state log** in a fixed format (e.g. `YYYY-MM-DD HH:MM | action=expand | target=1.1 | iterations=2 | next=1.2`).

### Rules

Add or extend `.cursor/rules/` (or a context rule): use `subphase-index` and `roadmap-level` per [[Roadmap Structure]]; escalate granularity by phase number; snapshot roadmap-state before edits; append queue entries in JSONL format to `.technical/prompt-queue.jsonl`; **read workflow_state before each automation step and write it after (including iteration tracker)**; reference [[.cursor/rules/always/mcp-obsidian-integration]].

### Cursor setup checklist

- [ ] Agent mode enabled
- [ ] Queue: "Send after current message" for chaining
- [ ] Plan mode for approval gates on big expansions
- [ ] Optional: long-running/scheduled triggers if available

### Optional: Automations (March 2026+)

Automations (new March 5, 2026) run **cloud** agents (repo pulled to VM, background execution). For **local vault/Obsidian edits**, stick to **local Agent mode + self-queued follow-ups**. Use Automations only for non-vault tasks (e.g. code-gen in repo clone) or future extensions. See cursor.com/docs/cloud-agent/automations.

---

## 3. Phase B: Pilot on Phase 1 (high-level deepening, semi-manual)

- Read **roadmap-state.md** and **workflow_state.md**; treat Phase 1 as active; read iteration tracker and report "Iteration X of cap Y for phase 1" in output.
- Phase 1 = high-level conceptual; create folders/notes with correct paths and frontmatter (`roadmap-level`, `phase-number`, `subphase-index` e.g. `"1.1.1"`); tertiary notes get 4–8 checklist tasks; snapshot before changes (Backups/Per-Change).
- After expanding one secondary, append an EXPAND-ROAD entry to `.technical/prompt-queue.jsonl` for the next secondary or Phase 2 preview. Queue entry format: `{"mode": "EXPAND-ROAD", "source_file": "<path>", "granularity": "secondary-tertiary", "user_guidance": "..."}`.
- **Update workflow_state:** log action; set current_subphase_index; increment iteration count for the roadmap object; append one line to log. If iterations for this phase ≥ cap, advance phase or queue RECAL-ROAD instead of another expand. If drift risk high, queue RECAL-ROAD.
- **First task:** Expand Phase 1 (sections 1.1–1.4) into secondary/tertiary per hierarchy; queue self-follow-up: "Continue to next secondary after this chunk."
- **Exit condition:** When Phase 1 tree is solid (~12–20 secondary, 40–80 tertiary/tasks), set `current_phase: 2` in roadmap-state (manually or via Agent instruction).

---

## 4. Phase C: Escalate automation and depth (core loop)

- Read **workflow_state** (including iteration tracker) + distilled-core + roadmap-state. If `current_phase < 6` and status ≠ complete: check iteration count for current phase/object; if under cap, determine next target; expand with granularity by phase (1 = secondary-tertiary, 2–4 = tertiary mid-technical, 5–6 = full-technical pseudo-code); create/update notes/folders; increment iteration tracker and append to workflow_state log; append next EXPAND-ROAD or REVERT-PHASE to queue. If at cap, advance phase in roadmap-state and reset or advance tracker, or queue RECAL-ROAD.
- **Output:** Each run emits a consistent one-line summary plus structured fields (action, target, iterations_this_object, iterations_this_phase, next_queued).
- Queue self-follow-up exactly as: "Resume loop from current state after this completes. Read workflow_state.md first." Use Plan mode first for big expansions (e.g. full phase advance).
- **Queue overflow safeguard:** Before appending to prompt-queue.jsonl, check current line count; if >8 pending, emit warning and queue a 'cleanup-queue' entry (manual review) instead of new EXPAND.
- **Integration:** Use existing [[expand-road-assist]] for EXPAND-ROAD; extend or add a skill for folder/note creation at secondary and tertiary levels (Skill extension: expand-road-assist or new roadmap-deepen skill).
- **Long-running agents (Feb 2026+):** If on eligible plan, select 'Long-running' model in Agent picker for 25–50+ hour autonomous runs. Fallback: standard Agent + self-queued follow-ups. See cursor.com/agents.
- **Optional:** Hooks (`.cursor/hooks.json`) or script to auto-continue; if Automations enabled, consider schedule/webhook per cursor.com/docs/cloud-agent/automations.
- **Monitoring:** Queue file size, periodic EAT-QUEUE; log to Ingest-Log or Backup-Log.

---

## 5. Phase D (or E): Polish and completion

- **Note:** Meta-roadmap uses A–D; label "Phase E" if a section is inserted earlier. For local vault edits, prefer local Agent + queue; use cloud Automations only for non-vault or future extensions (see Phase A).
- Queue **RECAL-ROAD** and **ROADMAP-VALIDATE**; fix drift via existing Decision Wrappers and REVERT-PHASE if needed.
- Update master roadmap and MOC with Dataview for new sub-levels (per [[Roadmap Structure]] Dataview table).
- Optional: Post-prototype phase (e.g. Phase 7).
- **Test:** One full chain Phase 1 → as far as it goes hands-off; document outcome and any blockers.

---

## 6. Risks and mitigations

| Risk | Mitigation |
|------|-------------|
| **Over-edits/hallucinations** | Use Plan mode + human approval for any change touching **>5 files** or **creating folders**; instruct Agent: "Propose plan in Plan mode first; wait for acceptance before execute." Per-phase iteration cap; snapshot every change. |
| **Queue overflow** | Limit pending (e.g. 5–10); before appending EXPAND, check line count (Phase C safeguard); manual flush or queue-cleanup; document in [[Queue-Sources]] if new caps added. |
| **Queued message regressions (Jan–Feb 2026)** | Toggle "Queue messages" (Chat → Queue messages) to "Send after current"; test with short loop first. Fallback: manual Enter after each chunk. |
| **Cursor limits (interrupts, long-run)** | Toggle settings; "Send after current"; fallback to manual RESUME-ROADMAP / EXPAND-ROAD. |
| **Recent Cursor bugs (March 2026, v2.6.11)** | Agent crashes, auto-apply diffs without preview, laggy agent chat, IDE "down" states. Pin to known-good build if issues arise; monitor forum.cursor.com/latest for hotfixes. |
| **Long-running cost / timeouts** | Phase 1 pilot only first; monitor via Cursor usage dashboard; set hard cap in workflow_state (e.g. `max_iterations_total: 50`). |
| **Cost/time** | Long runs (25–50+ hours) possible; start small, then scale. |

---

## 7. References and alignment

- [[Roadmap Structure]] — hierarchy, folder layout, Dataview
- [[Vault-Layout]] — Roadmap state artifacts, .technical
- [[Queue-Sources]] — prompt-queue location, EXPAND-ROAD, RESUME-ROADMAP, RECAL-ROAD, REVERT-PHASE
- [[.cursor/rules/context/auto-roadmap]], [[roadmap-resume]], [[expand-road-assist]]
- [[Roadmap-Quality-Guide]] — confidence, drift, wrappers
- **Cursor (March 2026):** cursor.com/docs/cloud-agent/automations; cursor.com/agents (long-running preview)

---

## 8. Timeline and milestones (brief)

- **Day 1:** Phase A setup + Phase B pilot on Phase 1 (semi-manual).
- **Day 2–3:** Phase C full chain (monitor queue, intervene on blocks).
- **Day 4+:** Phase D/E validation + optional Automations trigger.

---

## 9. Decisions (explicit)

1. **State: Option B adopted** — workflow_state.md in project Roadmap folder; schema as in §2; roadmap-state = phase completion/drift; workflow_state = run-time loop + step tracker.
2. **Iteration tracker:** Concrete schema in §2 (frontmatter + body Log table); after every expand, increment; before every run, if ≥ cap set status=blocked and queue RECAL-ROAD.
3. **Clean output:** Reference existing log/result format; add fields action, target, iterations_this_object, iterations_this_phase, next_queued and workflow_state log line format.
4. **Skill:** Extend expand-road-assist vs new roadmap-deepen for folder/note creation at secondary/tertiary.
5. **Queue entry fields:** Document `granularity` (and optionally `current_subphase_index`) in [[Queue-Sources]] / [[Queue-Alias-Table]] if adopted.
6. **Granularity mapping:** Document in [[Queue-Alias-Table]] or [[Parameters]]: Phase 1 → `secondary-tertiary-outline`, Phases 2–4 → `tertiary-mid-technical-interfaces`, Phases 5–6 → `full-pseudo-code-edges-hooks`.

---

## Starter Prompts for Cursor Agent

Copy one of the prompts below into Cursor Agent (Cmd/Ctrl + I) to start a run.

### Phase B: Pilot on Phase 1 (starter)

```
You are the genesis-mythos-master roadmap automator. Goal: deepen the hierarchy per [[Roadmap Structure]] (master → primary → secondary → tertiary → tasks).

Current state: Read [[roadmap-state]] and [[workflow_state]]; Phase 1 is active.

Rules:
- Phase 1: high-level conceptual; create folders/notes with correct paths and frontmatter (roadmap-level, phase-number, subphase-index e.g. "1.1.1"); tertiary notes: 4–8 checklist tasks (- [ ]).
- Snapshot any changed file first (Backups/Per-Change).
- After expanding one secondary (e.g. 1.1 Core abstractions), append an EXPAND-ROAD entry to .technical/prompt-queue.jsonl for the next secondary or Phase 2 preview. Format: {"mode": "EXPAND-ROAD", "source_file": "<path>", "granularity": "secondary-tertiary", "user_guidance": "Phase 1 tone ..."}
- Update workflow_state: log action, current_subphase_index; increment iteration count for the roadmap object (e.g. phase 1 or "1.1"); append one line to log in agreed format. If iterations for this phase ≥ cap, advance phase or queue RECAL-ROAD instead of another expand.
- If drift risk high, queue RECAL-ROAD instead.
- Report in output: "Iteration X of cap Y for phase 1."

First task: Expand current Phase 1 note (sections 1.1–1.4) into secondary/tertiary per hierarchy. Queue self-follow-up: "Continue to next secondary after this chunk completes."
```

### Phase C: Full loop (resume / escalate)

```
You are the genesis-mythos-master roadmap automator. Goal: continue the automation loop per [[Roadmap Upgrade Plan]].

1. Read workflow_state.md (including iteration tracker) + distilled-core.md + roadmap-state.md.
2. If current_phase < 6 and status != complete:
   - Check iterations_per_phase[current_phase]; if ≥ max_iterations_per_phase, queue RECAL-ROAD and set status=blocked with note "cap reached"; do not append new EXPAND. Else:
   - Determine next target (next secondary/tertiary in current phase, or advance phase).
   - Expand with granularity: Phase 1=secondary-tertiary, 2–4=tertiary-mid-technical (interfaces, pseudo-flows), 5–6=full-technical-pseudo-code (signatures, edges, hooks).
   - Create/update notes/folders. Increment iteration tracker; append one row to workflow_state log (Timestamp | Action | Target | Iterations This Object | Iterations This Phase | Next Queued | Status After).
   - Before appending to prompt-queue.jsonl: if line count >8 pending, emit warning and queue cleanup-queue (manual review) instead of new EXPAND. Else append next EXPAND-ROAD or REVERT-PHASE.
3. Emit one-line summary + structured fields (action, target, iterations_this_object, iterations_this_phase, next_queued).
4. Queue self-follow-up exactly: "Resume loop from current state after this completes. Read workflow_state.md first."
5. For big expansions (e.g. full phase advance), use Plan mode first for approval gate before execute.

Start from current state. Cap per-phase iterations per workflow_state max_iterations_per_phase (e.g. 80).
```

---

## Deferred

- **Context vs pipeline audit:** Compare "context Cursor used" (workflow_state Ctx Util %, token estimates) with "what pipelines focused on" (distill lens, express view, highlights in logs). Implemented as queue-ready skill **context-vs-pipeline-audit** ([[.cursor/skills/context-vs-pipeline-audit/SKILL|context-vs-pipeline-audit]]): reads workflow_state, Distill-Log, Express-Log; computes delta/overlap; writes to **Audit-Context-Focus.md**. Trigger: queue mode **AUDIT-CONTEXT** ([[Queue-Alias-Table]]); add to queue and run once roadmap systems are stable.
