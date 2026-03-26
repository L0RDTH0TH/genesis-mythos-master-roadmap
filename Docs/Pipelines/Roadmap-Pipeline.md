# Roadmap Pipeline

**Version: 2026-03 – post-subagent migration**

Documents the multi-run roadmap pipeline: ROADMAP MODE (setup only) and RESUME-ROADMAP (one action per run).

---

## Purpose

Single reference for roadmap steps, actions, and return format. Implementation in `.cursor/agents/roadmap.md` and legacy-agents/roadmap.mdc. Roadmap subagent owns roadmap-state.md and workflow_state.md under `1-Projects/<project_id>/Roadmap/`.

---

## Resolve project_id

From note path under `1-Projects/<project_id>/`, queue payload `project_id` or `source_file`, or user input. Roadmap dir: `1-Projects/{project_id}/Roadmap/`.

---

## ROADMAP MODE (setup only)

- Do **not** append RESUME-ROADMAP after setup; user crafts first resume separately.
- If ROADMAP-ONE-SHOT or one_shot: true → log deprecation; run classic roadmap-generate-from-outline; exit.
- Else: ensure_backup. If **roadmap-state.md** does not exist → create Phase 0 (roadmap-state.md, decisions-log.md, distilled-core.md) per Vault-Layout; run **roadmap-generate-from-outline** (creates workflow_state.md if missing). If roadmap-state.md exists → only ensure workflow_state.md exists; do **not** run resume logic in ROADMAP MODE.

---

## RESUME-ROADMAP (single action)

1. **Read params** — Merge queue entry + Config prompt_defaults.roadmap + prompt_defaults.profiles[params.profile]. Queue entry overrides. Derive effective_enable_context_tracking (default true). Pass token_cap, inject_extra_state to roadmap-deepen when action is deepen.
2. **action missing or "auto"** → run **smart dispatch**: scan Ingest/Decisions/Roadmap-Decisions/ for approved roadmap-next-step wrapper; if found, map approved_option to action per User-Questions-and-Options-Reference §4, mark processed, then branch by action. Else: read workflow_state, roadmap-state; check target reached (handoff or structural); if not, decide next step or create Decision Wrapper (options A–G per §4). Exit as soon as a branch is taken.
3. **Validate action** — deepen, recal, revert-phase, sync-outputs, handoff-audit, resume-from-last-safe, expand, advance-phase, compact-depth. Invalid → log Errors.md, Watcher-Result failure.
4. **Branch by action:**
   - **deepen** — (1) Pre-deepen research when enabled: resolve linked_phase, call research-agent-run; write to Ingest/Agent-Research/, queue INGEST (and DISTILL if research_distill); inject into deepen. (2) Optionally roadmap-resume for handoff context. (3) Run **roadmap-deepen** (one step; update workflow_state; append RESUME-ROADMAP to queue when params.queue_next !== false). (3b) Context-tracking postcondition: verify last Log row has valid Ctx Util %, Leftover %, Threshold, Est. Tokens; if tracking was true and any missing → fail run, Errors.md, Watcher-Result failure, #review-needed on roadmap-state.
   - **advance-phase** — roadmap-advance-phase (snapshot state; depth-aware gate; update roadmap-state and workflow_state).
   - **recal** — roadmap-audit (drift, wrapper, ignored_wrappers → auto-revert); optionally roadmap-phase-output-sync, roadmap-validate.
   - **revert-phase** — roadmap-revert (params.phase required).
   - **sync-outputs** — roadmap-phase-output-sync.
   - **handoff-audit** — hand-off-audit on phase.
   - **resume-from-last-safe** — find highest phase with conf ≥85%; run one deepen from there.
   - **expand** — expand-road-assist (sectionOrTaskLocator, userText).
   - **compact-depth** — COMPACT-DEPTH skill when implemented.

---

## Return

One-paragraph summary; any new wrapper or queue entry; Success / #review-needed / failure. Append Watcher-Result line with requestId. **Append workflow_state log row** when state was mutated (deepen/advance-phase).

**Skills:** roadmap-generate-from-outline, roadmap-deepen, roadmap-advance-phase, roadmap-resume, roadmap-audit, roadmap-revert, roadmap-phase-output-sync, hand-off-audit, expand-road-assist, research-agent-run (pre-deepen inline).
