---
name: Master plan pipeline gaps
overview: "Update the Rule-Refactor master rollout plan to incorporate the identified gaps: Prompt-Crafter unchanged, triggers without subagents, global invariants, recurring sync/changelog, shared config, rollback wording, Mobile/Commander unchanged, and optional post-rollout cleanup."
todos: []
isProject: false
---

# Master Plan Pipeline Gaps Integration

Update [.cursor/plans/rule-refactor_master_rollout_4b464e6c.plan.md](.cursor/plans/rule-refactor_master_rollout_4b464e6c.plan.md) so the refactor is explicit about primary vs secondary entry, triggers without subagents, invariants, sync, config, rollback, mobile/Commander, and optional cleanup.

---

## 1. Primary entry and triggers without subagents

**Where:** New subsection after the opening "Rule-Refactor Master Rollout Plan" intro (before "Pre-coding polish"), or as the first bullet block under a new **"Scope and boundaries"** section.

**Add:**

- **Prompt-Crafter unchanged:** The refactor applies only to **secondary** (manual/queue) triggers. **Prompt-Crafter** ("We are making a prompt" / question-led flow in [plan-mode-prompt-crafter.mdc](.cursor/rules/context/plan-mode-prompt-crafter.mdc)) remains the **primary entry** and is **not** replaced by a subagent. It continues to write validated payloads to the queue; only the **handler** of those payloads (dispatcher → subagent) changes.
- **Triggers with no subagent (yet):** **GARDEN REVIEW** and **CURATE CLUSTER** (and any other manual triggers not in the six phases) keep routing to their **existing context rules** ([auto-garden-review.mdc](.cursor/rules/context/auto-garden-review.mdc), [auto-curate-cluster.mdc](.cursor/rules/context/auto-curate-cluster.mdc)). The dispatcher routes **only** modes that have a dedicated subagent. This avoids confusion when looking for a "garden" or "curate" phase in the rollout.

---

## 2. Global invariants

**Where:** New short subsection (e.g. **"Global invariants"**) under the same "Scope and boundaries" or immediately after "Pre-coding polish."

**Add:**

- Error Handling Protocol, Decision Wrapper creation, CHECK_WRAPPERS, exclusions, and Watcher-Result contract live in **always** rules and shared contracts.
- **Invariant:** Subagents **depend on** these; they must **not** duplicate or relax them. **Source of truth** remains: [core-guardrails.mdc](.cursor/rules/always/core-guardrails.mdc), [mcp-obsidian-integration.mdc](.cursor/rules/always/mcp-obsidian-integration.mdc), [confidence-loops.mdc](.cursor/rules/always/confidence-loops.mdc), [watcher-result-append.mdc](.cursor/rules/always/watcher-result-append.mdc).

---

## 3. Recurring: sync and backbone docs after each phase

**Where:** In **"Validation strategy (after each phase)"**, add a sixth checklist item (or a separate "After each phase" list).

**Add:**

- **Sync and backbone:** After each phase, update the **sync mirror** (`.cursor/sync/rules/...`, `.cursor/sync/skills/...`) for any rule or skill touched by that phase, update **backbone docs** (e.g. [Cursor-Skill-Pipelines-Reference](3-Resources/Cursor-Skill-Pipelines-Reference.md), [Queue-Sources](3-Resources/Second-Brain/Queue-Sources.md), [Rules](3-Resources/Second-Brain/Rules.md)) as needed, and append a line to [.cursor/sync/changelog.md](.cursor/sync/changelog.md) so the refactor is traceable.

---

## 4. Shared config touchpoints

**Where:** One-line note in "Pre-coding polish" table or a small **"Shared config"** bullet list.

**Add:**

- **Queue-Sources**, **Parameters**, and **Second-Brain-Config** are **single source of truth**. When multiple phases change them, merge carefully and avoid conflicting defaults or mode lists.

---

## 5. Rollback (strengthen existing)

**Where:** In **"Validation strategy (after each phase)"**, expand the existing "revert the one-line route" sentence.

**Change:**

- Current: "If any check fails, revert the one-line route in the dispatcher (or the subagent inclusion) and fix before proceeding."
- **Add:** Old context rules are **kept in place (slimmed)**, not deleted. Rollback = **point the dispatcher back at the old rule**; no need to restore deleted files, so revert is fast and safe.

---

## 6. Mobile and Commander unchanged

**Where:** One sentence in "Scope and boundaries" or at the end of "How to use this master plan."

**Add:**

- **Mobile and Commander:** Flows are unchanged: same triggers and queue; only the **handler** (subagent vs old context rule) changes. Mobile still observes and fills Ingest; Commander macros still invoke the same modes.

---

## 7. Optional post-rollout cleanup

**Where:** New short **"Post-rollout (optional)"** subsection after "How to use this master plan" or after the dependency summary.

**Add:**

- After all phases, optional follow-ups: move skills into domain folders (e.g. `skills/roadmap/`), slim [system-funnels.mdc](.cursor/rules/always/system-funnels.mdc) to pure documentation, add a short **Subagent index** (e.g. in Pipelines or Rules.md) listing `agents/*.mdc` and their triggers.

---

## Suggested structure in the plan file

1. **Title and overview** (existing).
2. **Scope and boundaries** (new): Prompt-Crafter unchanged; triggers without subagents; global invariants; shared config; Mobile/Commander.
3. **Pre-coding polish** (existing table + shared config line).
4. **Rollout order** Phases 1–6 (unchanged).
5. **Validation strategy** (existing 5 items + sync/backbone item + rollback wording).
6. **Dependency summary** (existing mermaid + text).
7. **How to use this master plan** (existing 4 steps; optional: add Mobile/Commander sentence).
8. **Post-rollout (optional)** (new): cleanup and Subagent index.

No changes to phase deliverables or execution order; only clarifications and recurring steps so the master plan is self-contained and gap-free.