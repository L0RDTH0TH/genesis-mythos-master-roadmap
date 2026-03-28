# Subagent Architecture — Parity + Superiority Audit

**Date**: 2026-03-13  
**Scope**: Dispatcher + agents/* subagents vs pre-refactor monolithic/context rules.  
**Goal**: Confirm exact behavioral parity or measurable superiority; flag regressions.

---

## AUDIT SUMMARY

- **Overall verdict**: **PARITY MAINTAINED** (with minor doc/loading caveats)
- **Context size improvement**: ~25–40% estimated reduction per run (only the dispatched subagent + always core is needed when queue/mode is known; no single monolithic bundle)
- **Critical safety**: **✅ All preserved** — backup-first, per-change snapshot, dry_run→commit, Error Handling Protocol, Watcher-Result, guidance-aware, and roadmap state invariants are delegated to shared always rules and subagent text; no relaxation observed.

---

## Detailed Checklist

### 1. Dispatcher correctness

| Item | Status | Notes |
|------|--------|--------|
| Queue triggers (EAT-QUEUE, Process queue, EAT-CACHE, PROCESS TASK QUEUE) route to Queue subagent | ✅ | `dispatcher.mdc` L12–26: explicit "Load and follow … queue.mdc". |
| Other triggers (INGEST, DISTILL, EXPRESS, ARCHIVE, ORGANIZE, ROADMAP, RESUME-ROADMAP, GARDEN REVIEW, CURATE CLUSTER) documented | ✅ | L28–30: "continue to map … per system-funnels"; system-funnels.mdc points each to the correct agent or context rule. |
| Shared core invariants still enforced | ✅ | L10: core-guardrails, confidence-loops, guidance-aware, mcp-obsidian-integration, watcher-result-append, backbone-docs-sync — all listed; subagents "depend on" the same set. |
| Every trigger phrase / queue mode covered | ✅ | system-funnels + queue.mdc A.4 ordering and A.5 dispatch cover INGEST, FORCE-WRAPPER, ORGANIZE, TASK-ROADMAP, RESEARCH-AGENT, NORMALIZE-MASTER-GOAL, EXPAND-ROAD, TASK-TO-PLAN-PROMPT, ROADMAP MODE, RESUME-ROADMAP (+ aliases), DISTILL, EXPRESS, SCOPING, ARCHIVE, AUDIT-CONTEXT, TASK-COMPLETE, ADD-ROADMAP-ITEM, SEEDED-ENHANCE, BATCH-*, ASYNC-LOOP, NAME-REVIEW, GARDEN-REVIEW, CURATE-CLUSTER. |

**Caveat (non-blocking)**  
- **Trigger-based loading**: Agents use `alwaysApply: false` and file-based globs (e.g. `Ingest/**`, `1-Projects/**/Roadmap/**`). When the user says "INGEST MODE" with no file in `Ingest/`, Cursor may not auto-include `agents/ingest.mdc` by glob. Parity relies on the agent being instructed by system-funnels to "run IngestSubagent agents/ingest.mdc" and therefore loading that rule when the trigger is detected. **Recommendation**: In dispatcher or system-funnels, add an explicit line: "When the user instruction matches a mode phrase (e.g. INGEST MODE), load and follow the corresponding agent rule from agents/ so the full pipeline is in context."

---

### 2. Routing & loading integrity

| Item | Status | Notes |
|------|--------|--------|
| Each subagent loads only its own pipeline + shared always | ✅ | agents/*.mdc "Depends on" list only always rules (core-guardrails, confidence-loops, guidance-aware, mcp-obsidian-integration, watcher-result-append). No subagent references another subagent's rule file. |
| Skills are referenced by name, not by "folder" | ✅ | Subagents reference skills by name (e.g. archive-check, roadmap-deepen); Cursor/skills are a shared pool. No cross-subagent skill bleed; each agent lists only the skills its pipeline uses. |
| Queue subagent delegates Step 0 to auto-eat-queue | ✅ | queue.mdc A.0 and footnote: "Full Step 0 semantics … are as specified in auto-eat-queue.mdc §§ Wrapper-check requeue semantics and Always-check wrappers. Follow that rule verbatim." |
| Globs and exclusions respected | ✅ | agents have narrow globs or empty; always rules use globs: "*" or alwaysApply: true. Backups/, Watcher paths, Ingest/Decisions/ exclusions stated in each pipeline. |
| agents/ folder not pulled by unrelated context | ✅ | No always rule globs "agents/**"; agents are loaded by reference from dispatcher/system-funnels or by file glob when context matches. |

---

### 3. Behavioral parity checklist

| Pipeline / mode | Status | Evidence |
|-----------------|--------|----------|
| **INGEST MODE** (Phase 1 propose + DW; Phase 2 apply-mode) | ✅ | ingest.mdc: Phase 1 (confidence bands, Cursor-agent direct move when tech_level/conf ok, DW creation, CHECK_WRAPPERS append); Phase 2 apply from Step 0; non-MD, embedded image norm, classify→frontmatter-enrich→name-enhance (propose)→subfolder-organize→split-link-preserve, distill-highlight-color, next-action-extract, task-reroute, link-to-pmg. |
| **DISTILL MODE** (layers, highlight-color, layer-promote, readability-flag) | ✅ | distill.mdc: backup, auto-layer-select, distill layers, distill-highlight-color, highlight-perspective-layer, layer-promote, distill-perspective-refine, callout-tldr-wrap, readability-flag; mid/low → Decision Wrapper Refinements/Low-Confidence; Step 0 distill-apply-from-wrapper. |
| **EXPRESS MODE** (related-content-pull, research-scope, mini-outline, CTA) | ✅ | express.mdc: version-snapshot, related-content-pull, research-scope (PMG), express-mini-outline, express-view-layer, call-to-action-append; mid/low wrappers; Step 0 express-apply-from-wrapper. |
| **ARCHIVE MODE** (archive-check → subfolder-organize → resurface-mark → summary-preserve → move + ghost-folder sweep) | ✅ | archive.mdc: archive-check, mid/low loops, per-change snapshot, subfolder-organize, resurface-candidate-mark, summary-preserve, move, post-move frontmatter, archive-ghost-folder-sweep. |
| **ORGANIZE MODE** (re-classify, name-enhance, subfolder-organize, rename/move) | ✅ | organize.mdc: classify_para, frontmatter-enrich, subfolder-organize, mid/low wrappers, name-enhance (organize context), snapshot before rename/move, ensure_structure, dry_run then commit. |
| **ROADMAP MODE** (setup only: Phase 0 + roadmap-generate-from-outline) | ✅ | roadmap.mdc: ROADMAP MODE = setup only; no resume in ROADMAP MODE; Phase 0 artifacts, workflow_state creation, roadmap-generate-from-outline; one-shot deprecated. |
| **RESUME-ROADMAP** (deepen, recal, advance-phase, revert-phase, handoff-audit, expand, resume-from-last-safe) | ✅ | roadmap.mdc: branch by params.action (deepen with pre-deepen research, advance-phase, recal, revert-phase, sync-outputs, handoff-audit, resume-from-last-safe, expand, compact-depth); smart dispatch when action "auto"; context-tracking postcondition; research 0-notes Watcher-Result suffix. |
| **EAT-QUEUE** (Step 0, CHECK_WRAPPERS, stale removal, failed tagging, processed_success_ids) | ✅ | queue.mdc A.0 → auto-eat-queue verbatim; A.4 ordering CHECK_WRAPPERS first; A.5 CHECK_WRAPPERS no-op; A.7 re-read file, omit processed_success_ids, add queue_failed: true for failed, append CHECK_WRAPPERS if approved_wrappers_remaining. |
| **FORCE-WRAPPER, ASYNC-LOOP, SEEDED-ENHANCE, RESEARCH-AGENT, GARDEN-REVIEW, CURATE-CLUSTER, NAME-REVIEW** | ✅ | queue.mdc A.5: FORCE-WRAPPER → infer from source_file; SEEDED-ENHANCE → highlight-seed-enhance; RESEARCH-AGENT → ResearchSubagent; BATCH-DISTILL/EXPRESS, ASYNC-LOOP, NAME-REVIEW, GARDEN-REVIEW, CURATE-CLUSTER → per auto-eat-queue dispatch table (which defines the flows). |
| **Decision Wrapper flows** (mid-band, low-confidence, re-wrap, re-try, phase-direction, error) | ✅ | Step 0 in auto-eat-queue (referenced by queue.mdc) defines Branch A path-apply by wrapper_type/pipeline (ingest, phase-direction, handoff-readiness, organize, archive, distill/express-apply-from-wrapper, low-confidence, error), re-try cap and re-wrap branch, Branch B orphan/true-orphan; CHECK_WRAPPERS requeue when approved_wrappers_remaining. |
| **Mobile-seed-detect + highlight-seed-enhance** | ✅ | SEEDED-ENHANCE dispatched per queue; mobile-seed-detect.mdc remains context rule for trigger phrases; highlight-seed-enhance skill invoked by queue or explicit trigger. |
| **Prompt-Crafter** (question-led Q&A, scratchpad, queue append, no .plan.md, session-end) | ✅ | plan-mode-prompt-crafter.mdc unchanged (alwaysApply: true); trigger "We are making a prompt"; no reference to agents/; queue append and session-end message as in rule. |

---

### 4. Safety & state invariants

| Invariant | Status | Notes |
|-----------|--------|--------|
| Backup + per-change snapshot before destructive action | ✅ | core-guardrails + mcp-obsidian-integration + each subagent (backup first; snapshot before move/rename/split/rewrite/append_to_hub). |
| dry_run → commit for all moves | ✅ | mcp-obsidian-integration and each agent (archive, organize, ingest) state dry_run then commit. |
| Roadmap state (roadmap-state.md, workflow_state.md) only in RoadmapSubagent | ✅ | roadmap.mdc is sole owner; queue only dispatches to RoadmapSubagent for ROADMAP MODE and RESUME-ROADMAP. |
| CHECK_WRAPPERS requeue and wrapper archiving to 4-Archives/Ingest-Decisions/ | ✅ | queue A.0/A.7 and auto-eat-queue Step 0: after apply, move wrapper to 4-Archives/Ingest-Decisions/ (ensure_structure, per-change snapshot, move); approved_wrappers_remaining → append CHECK_WRAPPERS at A.8. |
| Ghost-folder sweep, version-snapshot, research pre-deepen | ✅ | archive.mdc: archive-ghost-folder-sweep after moves; express.mdc: version-snapshot before major append; roadmap.mdc: pre-deepen research (research-agent-run) with enable conditions, Errors backstop, inject into deepen. |

---

### 5. Superiority metrics

| Metric | Assessment |
|--------|------------|
| **Context size** | Smaller per run: only always rules + one agent (or queue + one dispatched agent) instead of always + all of auto-archive, auto-distill, auto-express, auto-organize, para-zettel-autopilot, auto-roadmap, auto-eat-queue. Estimate ~25–40% fewer tokens when running a single pipeline. |
| **Isolation** | Changing one subagent (e.g. adding a new roadmap action) does not require editing other agents; queue dispatch table and system-funnels are the only cross-references. |
| **Error handling** | Each subagent and queue point to the same Error Handling Protocol (mcp-obsidian-integration.mdc); Errors.md, error_type, and severity behavior unchanged. |
| **Maintainability** | New flows (e.g. CurateSubagent) can be added by creating agents/curate.mdc and adding one dispatch line in queue.mdc and system-funnels; context rules can stay as thin rollback stubs. |

---

### 6. Edge cases & regressions

| Edge case | Status | Notes |
|-----------|--------|--------|
| Empty queue, missing state | ✅ | queue.mdc A.1: missing/unreadable file → treat empty, optionally Watcher-Result, exit. RESUME-ROADMAP bootstrap: if no roadmap-state, run ROADMAP MODE same project from queue if present. |
| re-wrap: true, true-orphan wrappers | ✅ | auto-eat-queue Step 0 Branch A (re-wrap branch) and Branch B (orphan/true-orphan, ## Wrapper state idempotency); queue follows it verbatim. |
| tech_level > 1 mid-band direct-move bypass | ✅ | ingest.mdc: "When tech_level > 1 and confidence mid-band (68–84%), do **not** direct-move; fall through to Decision Wrapper." Queue injects tech_level when roadmap_tech_progression and INGEST MODE. |
| Guidance-aware, crafted params, profile presets | ✅ | guidance-aware.mdc always; queue merges params (entry, user_guidance, Config, profiles); roadmap effectiveParams and profile-vs-lock; prompt_crafter unchanged. |
| Batch checkpoints, high-util research gate | ✅ | roadmap.mdc: research enable from util (last_ctx_util_pct < threshold, depth ≥ 2, conf veto, research_cooldown); distill/archive/organize batch snapshot every N notes. |
| Watcher-Result for every requestId (including research 0-notes) | ✅ | queue A.6 one line per processed request; roadmap.mdc: "research ran, 0 notes" suffix in success message when research invoked but 0 notes; ResearchSubagent: 0 notes → failure, do not add to processed_success_ids. |

**Doc inconsistency (cosmetic)**  
- Cursor-Skill-Pipelines-Reference.md Quick Reference Table (L22–23) still says "auto-distill" and "auto-archive" for pipeline rule; the Trigger → rule mapping correctly says DistillSubagent and ArchiveSubagent. **Fix**: Update the Quick Reference Table to "DistillSubagent (agents/distill.mdc)" and "ArchiveSubagent (agents/archive.mdc)".

---

## Regressions & Fixes

- **None** requiring code or rule changes for behavioral parity or safety.
- **Optional**: Add one sentence to `dispatcher.mdc` or `system-funnels.mdc`: "When the user instruction matches a mode phrase (e.g. INGEST MODE, DISTILL MODE), load and follow the corresponding agent rule from `.cursor/rules/agents/` so the full pipeline is in context."
- **Doc fix**: In `3-Resources/Second-Brain/Cursor-Skill-Pipelines-Reference.md`, Quick Reference Table, change "auto-distill" → "DistillSubagent (agents/distill.mdc)" and "auto-archive" → "ArchiveSubagent (agents/archive.mdc)" for the Rule(s) column.

---

## Superiority wins

1. **Single pipeline in context** per run (plus always core) reduces token load and clarifies which steps apply.
2. **Explicit dispatch table** in queue.mdc (A.5) and system-funnels makes it easy to see which mode maps to which agent.
3. **Rollback path** is documented: context rules (auto-archive, auto-distill, etc.) are kept as stubs pointing at agents; restoring full content from version control reverts to pre-refactor behavior.
4. **Step 0 and CHECK_WRAPPERS** remain in one place (auto-eat-queue); queue subagent delegates there, avoiding duplication and drift.
5. **Roadmap state and research** are confined to RoadmapSubagent and ResearchSubagent, reducing risk of accidental mutation from other flows.

---

## Recommended next steps

1. **If everything is green**:  
   - Apply the optional dispatcher/system-funnels sentence for trigger-based loading.  
   - Update Cursor-Skill-Pipelines-Reference.md Quick Reference Table as above.  
   - Run a small test: EAT-QUEUE with one INGEST MODE, one DISTILL MODE, and one RESUME-ROADMAP entry; confirm Step 0 runs first, CHECK_WRAPPERS requeue when a wrapper remains, and Watcher-Result lines are appended per entry.

2. **Next extraction**: Consider a dedicated **GardenReviewSubagent** / **CurateSubagent** (or a single **GardenCurateSubagent**) if GARDEN-REVIEW and CURATE-CLUSTER flows grow; currently they are "per auto-eat-queue dispatch table" (inline/callback), which is acceptable.

3. **Test suite**: Add a one-page checklist in `3-Resources/Second-Brain/` or `.cursor/plans/` that an operator can run manually: e.g. "Create Decision Wrapper in Ingest → run EAT-QUEUE → confirm wrapper applied and archived; run RESUME-ROADMAP with action deepen → confirm workflow_state log row and context-tracking; run RESEARCH-AGENT with 0 notes → confirm Errors.md + Watcher-Result failure."

---

*Audit performed against current vault state; rules under `.cursor/rules/always/`, `.cursor/rules/context/`, and `.cursor/rules/agents/` and references to Queue-Sources, Cursor-Skill-Pipelines-Reference, and Parameters.*
