---
name: Roadmap upgrade plan sketch
overview: Sketch a Roadmap Upgrade Plan document from the user's rough draft, aligned with the existing vault (queue in .technical, roadmap-state, EXPAND-ROAD/RESUME-ROADMAP, Roadmap Structure hierarchy) and structured as Phase A (prep) through Phase D (polish), with risks and integration points.
todos: []
isProject: false
---

# Roadmap Upgrade Plan — Sketch

## Purpose

Turn the provided rough draft into a single **Roadmap Upgrade Plan** document that:

- Evolves genesis-mythos-master from current state (6 phases, placeholder tasks, manual RESUME advances) to a **full hierarchy** (master → phases → secondary → tertiary → tasks) with **progressive technical depth** and **semi-to-high automation** via Cursor Agent and the existing queue/state machinery.
- Stays aligned with the vault: [Queue-Sources](3-Resources/Second-Brain/Queue-Sources.md) (queue in `.technical/`), [roadmap-state](1-Projects/genesis-mythos-master/Roadmap/roadmap-state.md), [auto-roadmap](.cursor/rules/context/auto-roadmap.mdc), [expand-road-assist](.cursor/skills/expand-road-assist/SKILL.md), and [Roadmap Structure](Roadmap Structure.md).

---

## Where the plan document lives

- **Recommended:** `3-Resources/Second-Brain/Roadmap-Upgrade-Plan.md` (alongside Roadmap-Quality-Guide, Pipelines, Backbone).
- **Optional:** Cross-link from [Backbone](3-Resources/Second-Brain/Backbone.md) and [Roadmap-Quality-Guide](3-Resources/Second-Brain/Roadmap-Quality-Guide.md) so the upgrade is discoverable.

---

## Document structure (to write)

### 1. Goals of the upgrade

- **Full hierarchy adoption:** master → phases → secondary → tertiary → tasks per [Roadmap Structure](Roadmap Structure.md) (generalized P×S×T×J model).
- **Progressive technical depth:** Phase 1 high-level conceptual; Phases 2–4 mid-technical (interfaces, data flows); Phases 5–6 pseudo-code/APIs/edges. Align with existing `tech_level` / `roadmap_tech_progression` in [Queue-Sources](3-Resources/Second-Brain/Queue-Sources.md) and [Parameters](3-Resources/Second-Brain/Parameters.md) where applicable.
- **Semi-to-high automation:** Cursor Agent populates queue (EXPAND-ROAD, RESUME-ROADMAP), creates/expands notes and folders, updates state, chains iterations with minimal manual triggers; use existing EAT-QUEUE and `.technical/prompt-queue.jsonl`.
- **Safety:** Snapshots before changes (obsidian-snapshot, roadmap-state before/after), drift checks (RECAL-ROAD), approval gates (Plan mode, Decision Wrappers) per existing rules.
- **Target:** From current Phase 1 depth to 5–10× deeper content per phase, auto-chained across phases until complete or blocked.

### 2. Phase A: Preparation and setup (1–2 hours manual)

- **Cursor version check and feature gating:** In the upgrade plan doc, add a frontmatter or early-section note: "Assumes Cursor ≥2.6.x (March 2026 stable builds, e.g. 2.6.11 per recent changelogs). Verify: Help → About Cursor. If <2.6, expect potential queued-message regressions (Jan–Feb 2026 reports). Prefer `.cursor/rules/*.mdc` format over legacy .cursorrules; fallback to legacy .cursorrules or single `.cursor/rules/main.mdc` if needed."
- **Queue:** Document that the queue is `**.technical/prompt-queue.jsonl`** (not vault root). **Clarify .cursorignore:** Ensure `.technical/prompt-queue.jsonl` is **not** ignored in `.cursorignore` (already per [Queue-Sources](3-Resources/Second-Brain/Queue-Sources.md)); confirm Agent can read and write it.
- **State and automation tracking (Option B — adopted):** Add **workflow_state.md** under `1-Projects/<project_id>/Roadmap/` (e.g. `1-Projects/genesis-mythos-master/Roadmap/workflow_state.md`) as the single run-time automation state file. **Schema:** frontmatter and body as below. **Integration:** roadmap-state.md remains the source of truth for phase completion and drift; workflow_state is read/written by the Agent loop and optionally by roadmap-resume/expand skills. Document in the upgrade plan and in [Vault-Layout](3-Resources/Second-Brain/Vault-Layout.md) § Roadmap state artifacts.
  - **workflow_state.md schema (minimum + tracker)** — Pick one format for parseability. Recommendation: **frontmatter + body table**.
    - **Frontmatter:** `current_phase`, `current_subphase_index` (e.g. `"1.1.2"` or null if at phase level), `status` (`in-progress` | `blocked` | `complete`), `automation_level` (`semi` | `high` | `manual`), `last_auto_iteration` (ISO timestamp), `iterations_per_phase` (object: phase number → count, e.g. `"1": 3`, `"2": 0`), `max_iterations_per_phase` (enforcement cap, e.g. 10). Optional: `max_iterations_total` for global cap (e.g. 50).
    - **Body:** ## Log (append-only) — table with columns: Timestamp | Action | Target | Iterations This Object | Iterations This Phase | Next Queued | **Status After** (e.g. `in-progress` → `in-progress` or `blocked` when cap reached, for visibility). Example row: `2026-03-08 12:34:56Z | expand | Phase-1-1-Core-Abstractions | 2 | 3 | EXPAND-ROAD for 1.2 | in-progress`.
    - **Update rule:** After successful expand/create: increment `iterations_per_phase[phase]`; append one row to log. Before loop iteration: if `iterations_per_phase[current_phase] ≥ max_iterations_per_phase`, queue RECAL-ROAD and set `status: blocked` with note "cap reached"; do not append new EXPAND. Optionally enforce `max_iterations_total` across all phases.
- **Clean, consistent Cursor output:** Define a single convention so every automation run produces readable, parseable output (for logs, Watcher-Result, and workflow_state). If the vault already has this (e.g. via [watcher-result-append](.cursor/rules/always/watcher-result-append.mdc), pipeline log fields in [Logs](3-Resources/Second-Brain/Logs.md), or Ingest-Log format), the upgrade plan will **reference and extend** it for roadmap automation. Require: (1) **One-line summary per action** (e.g. "Expanded Phase 1.1 → 3 tertiary notes; iterations_phase_1: 2"). (2) **Structured fields** where applicable: `action`, `target` (path or object_id), `iterations_this_object`, `iterations_this_phase`, `next_queued`. (3) **Append to workflow_state log** in a fixed format (e.g. `YYYY-MM-DD HH:MM | action=expand | target=1.1 | iterations=2 | next=1.2`). This allows step tracking and caps without parsing freeform text.
- **Step / iteration tracker (in workflow_state):** As above: store `iterations_per_phase` and/or per-object counts; update after each run; read before each run to enforce per-phase cap (e.g. 8–10) and to report "Iteration X of Y for phase N" in Cursor output. The upgrade plan doc will specify the exact schema (frontmatter vs body table) and the rule: "After every expand/deepen, increment tracker for the current roadmap object and append one line to workflow_state log."
- **Rules:** Add or extend `.cursor/rules/` (or a context rule) with: use `subphase-index` and `roadmap-level` per Roadmap Structure; escalate granularity by phase number; snapshot roadmap-state before edits; append queue entries in JSONL format to `.technical/prompt-queue.jsonl`; **read workflow_state before each automation step and write it after (including iteration tracker)**; reference [mcp-obsidian-integration](.cursor/rules/always/mcp-obsidian-integration.mdc) for backup/snapshot.
- **Cursor setup:** Agent mode, queue “Send after current message” for chaining; Plan mode for approval gates; optional long-running/scheduled triggers if available. Short checklist in the doc.
- **Automations (March 2026+):** In the written doc, under "Optional: Hooks / auto-continue": "Automations (new March 5, 2026) run **cloud** agents (repo pulled to VM, background execution). For **local vault/Obsidian edits**, stick to **local Agent mode + self-queued follow-ups**. Use Automations only for non-vault tasks (e.g. code-gen in repo clone) or future extensions. See cursor.com/docs/cloud-agent/automations."

### 3. Phase B: Pilot on Phase 1 (high-level deepening, semi-manual)

- **Starter prompt:** Embed a concrete Agent prompt that:
  - References “genesis-mythos-master roadmap automator” and the hierarchy in [Roadmap Structure](Roadmap Structure.md).
  - Reads **roadmap-state.md** and **workflow_state.md**; treats Phase 1 as active; reads **iteration tracker** (e.g. iterations for phase 1, current subphase) and reports "Iteration X of cap Y for phase 1" in output.
  - Rules: Phase 1 = high-level conceptual; create folders/notes with correct paths and frontmatter (`roadmap-level`, `phase-number`, `subphase-index` e.g. `"1.1.1"`); tertiary notes get 4–8 checklist tasks; snapshot before changes (Backups/Per-Change); after expanding one secondary, append an **EXPAND-ROAD** entry to `.technical/prompt-queue.jsonl` for the next secondary or Phase 2 preview.
  - Queue entry format: `{"mode": "EXPAND-ROAD", "source_file": "<path>", "granularity": "secondary-tertiary", "user_guidance": "..."}` (align with [Queue-Sources](3-Resources/Second-Brain/Queue-Sources.md) EXPAND-ROAD contract; add `granularity` to docs if not already present).
  - **Update workflow_state:** log action; set current_subphase_index; **increment iteration count** for the roadmap object (e.g. phase 1 or "1.1"); append one line to log in the agreed format. If iterations for this phase ≥ cap, advance phase or queue RECAL-ROAD instead of another expand.
  - If drift risk high, queue RECAL-ROAD instead.
- **First task:** Expand Phase 1 (sections 1.1–1.4) into secondary/tertiary per hierarchy; queue self-follow-up: “Continue to next secondary after this chunk.”
- **Exit condition:** When Phase 1 tree is solid (~12–20 secondary, 40–80 tertiary/tasks), set `current_phase: 2` in roadmap-state (manually or via Agent instruction).

### 4. Phase C: Escalate automation and depth (core loop)

- **Refined loop prompt:** Same rules as Phase B, plus:
  - **Loop:** Read **workflow_state** (including iteration tracker) + distilled-core + roadmap-state; if `current_phase < 6` and status ≠ complete: check **iteration count for current phase/object**; if under cap, determine next target (next secondary/tertiary or advance phase); expand with granularity by phase (1 = secondary-tertiary, 2–4 = tertiary mid-technical, 5–6 = full-technical pseudo-code); create/update notes/folders; **increment iteration tracker and append to workflow_state log**; append next EXPAND-ROAD or REVERT-PHASE to queue. If at cap, advance phase in roadmap-state and reset or advance tracker, or queue RECAL-ROAD.
  - Note: “Ready for EAT-QUEUE” when queue has entries; queue self-follow-up “Resume loop from current state.”
  - **Output:** Each run emits a **consistent one-line summary** plus structured fields (action, target, iterations_this_object, iterations_this_phase, next_queued) so the step tracker is visible and logs are parseable.
  - **Cap:** Per-phase iteration limit (e.g. 8–10) enforced via workflow_state iteration tracker; document in workflow_state `rules` or in the upgrade plan.
- **Integration:** Use existing [expand-road-assist](.cursor/skills/expand-road-assist/SKILL.md) for EXPAND-ROAD; extend or add a skill for **folder/note creation** at secondary and tertiary levels when the target is a path pattern from Roadmap Structure (expand-road-assist currently appends under a section; upgrade may need “create Phase-N-M folder and note” behavior). Document in the plan as “Skill extension: expand-road-assist or new roadmap-deepen skill.”
- **Long-running agents (Feb 2026+):** Add bullet: "Leverage long-running agents research preview (cursor.com/agents) if on eligible plan: select 'Long-running' model in Agent picker for 25–50+ hour autonomous runs. Fallback to standard Agent + self-queued follow-ups if not available."
- **Self-chaining phrasing:** Strengthen prompt snippet: "Queue self-follow-up exactly as: 'Resume loop from current state after this completes. Read workflow_state.md first.' Use Plan mode first for big expansions (e.g. full phase advance) to generate approval gate before execute."
- **Queue overflow safeguard:** "Before appending to prompt-queue.jsonl, check current line count; if >8 pending, emit warning in output and queue a 'cleanup-queue' entry (manual review) instead of new EXPAND."
- **Optional:** Hooks (e.g. `.cursor/hooks.json`) or script to auto-continue on stop; reference community patterns (workflow_state loop). If Automations enabled (see Phase A), consider schedule/webhook trigger per cursor.com/docs/cloud-agent/automations.
- **Monitoring:** Queue file size, periodic EAT-QUEUE (manual or script); log to Ingest-Log or Backup-Log per existing pipeline.

### 5. Phase D (or E): Polish and completion

- **Note:** Current meta-roadmap uses A–D; the written doc may label this "Phase E" if a section is inserted earlier. Optionally renumber to 0–5 for meta-roadmap consistency. **Automations:** For local vault edits, prefer local Agent + queue; use cloud Automations only for non-vault or future extensions (see Phase A).
- Queue **RECAL-ROAD** and **ROADMAP-VALIDATE** (or run via Agent); fix drift via existing Decision Wrappers and REVERT-PHASE if needed.
- Update master roadmap and MOC with Dataview for new sub-levels (per [Roadmap Structure](Roadmap Structure.md) Dataview table).
- Optional: Post-prototype phase (e.g. Phase 7) if desired.
- **Test:** One full chain Phase 1 → as far as it goes hands-off; document outcome and any blockers.

### 6. Risks and mitigations

- **Over-edits/hallucinations:** Use Plan mode + human approval for any change touching **>5 files** or **creating folders**; instruct Agent: "Propose plan in Plan mode first; wait for acceptance before execute." Per-phase iteration cap; snapshot every change (roadmap-state and notes).
- **Queue overflow:** Limit pending (e.g. 5–10); before appending EXPAND, check line count (safeguard in Phase C); manual flush or queue-cleanup; document in [Queue-Sources](3-Resources/Second-Brain/Queue-Sources.md) if new caps are added.
- **Queued message regressions (Jan–Feb 2026):** Messages may not dequeue automatically or may interrupt unexpectedly. **Mitigation:** Toggle "Queue messages" (Chat → Queue messages) to "Send after current"; test with short loop first. Fallback: manual Enter after each chunk.
- **Cursor limits (interrupts, long-run):** Toggle settings; “Send after current”; fallback to manual RESUME-ROADMAP / EXPAND-ROAD.
- **Recent Cursor bugs (March 2026, v2.6.11):** Agent crashes, auto-apply diffs without preview, laggy agent chat, IDE "down" states post-update. **Mitigation:** Pin to known-good build if issues arise; monitor forum.cursor.com/latest for hotfixes.
- **Long-running cost / timeouts:** Automations or long-running agents can rack up high token usage. **Mitigation:** Start with Phase 1 pilot only; monitor via Cursor usage dashboard; set hard cap in workflow_state (e.g. `max_iterations_total: 50`).
- **Cost/time:** Long runs (e.g. 25–50+ hours); start small (Phase 1 pilot), then scale.

### 7. References and alignment

- [Roadmap Structure](Roadmap Structure.md) — hierarchy, folder layout, Dataview.
- [Vault-Layout](3-Resources/Second-Brain/Vault-Layout.md) — Roadmap state artifacts, .technical.
- [Queue-Sources](3-Resources/Second-Brain/Queue-Sources.md) — prompt-queue location, EXPAND-ROAD, RESUME-ROADMAP, RECAL-ROAD, REVERT-PHASE.
- [auto-roadmap](.cursor/rules/context/auto-roadmap.mdc), [roadmap-resume](.cursor/skills/roadmap-resume/SKILL.md), [expand-road-assist](.cursor/skills/expand-road-assist/SKILL.md).
- [Roadmap-Quality-Guide](3-Resources/Second-Brain/Roadmap-Quality-Guide.md) — confidence, drift, wrappers.
- **Cursor (March 2026):** Cursor Automations docs — cursor.com/docs/cloud-agent/automations. Long-running agents preview — cursor.com/agents.

### 8. Timeline and milestones (brief)

- **Day 1:** Phase A setup + Phase B pilot on Phase 1 (semi-manual).
- **Day 2–3:** Phase C full chain (monitor queue, intervene on blocks).
- **Day 4+:** Phase D/E validation + optional Automations trigger.

---

## Implementation notes (for the writer)

- **One doc:** Write the above as a single markdown file at `3-Resources/Second-Brain/Roadmap-Upgrade-Plan.md` with frontmatter. **Suggested frontmatter for the written doc:**

```
  ---
  title: Roadmap Upgrade Plan – Automating Deep Hierarchy & Cursor Iteration
  created: 2026-03-08
  tags: [roadmap, automation, cursor, genesis-mythos-master, upgrade]
  links: [[Backbone]], [[Roadmap-Quality-Guide]], [[Pipelines]], [[Roadmap Structure]]
  ---
  

```

- **Prompts:** In the written doc, add a section **"## Starter Prompts for Cursor Agent"** and paste the **Phase B starter prompt** and **Phase C loop prompt** (from the rough draft / plan sections 3–4) in code blocks so they can be copied into Cursor Agent.
- **Decisions to make explicit in the doc:** (1) **State: Option B adopted** — workflow_state.md in project Roadmap folder; schema (current_phase, current_subphase_index, status, automation_level, last_auto_iteration, iteration tracker fields or table); integration with roadmap-state (roadmap-state = phase completion/drift; workflow_state = run-time loop + step tracker). (2) **Iteration tracker:** Use the concrete schema in section 2 (frontmatter `iterations_per_phase`, `max_iterations_per_phase`, optional `max_iterations_total` + body Log table); update rule (after every expand, increment; before every run, if ≥ cap set status=blocked and queue RECAL-ROAD). (3) **Clean output:** Reference existing log/result format; add required fields (action, target, iterations_this_object, iterations_this_phase, next_queued) and workflow_state log line format. (4) Skill: extend expand-road-assist vs new roadmap-deepen for folder/note creation. (5) Queue entry fields: document `granularity` (and optionally `current_subphase_index`) in Queue-Sources/Queue-Alias-Table if adopted. (6) **Granularity mapping:** Document in [Queue-Alias-Table](3-Resources/Second-Brain/Queue-Alias-Table.md) or [Parameters](3-Resources/Second-Brain/Parameters.md): Phase 1 → `secondary-tertiary-outline`, Phases 2–4 → `tertiary-mid-technical-interfaces`, Phases 5–6 → `full-pseudo-code-edges-hooks`.
- **No code edits in this plan:** This sketch only defines the content and location of the upgrade plan document; actual edits to rules, skills, or queue format are follow-up work.

