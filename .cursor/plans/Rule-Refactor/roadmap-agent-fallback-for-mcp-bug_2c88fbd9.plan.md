---
name: roadmap-agent-fallback-for-mcp-bug
overview: Plan to integrate an inline fallback in the roadmap agent to cope with Cursor MCP schema bugs, and to rely on an existing RESUME_ROADMAP queue item plus EAT-QUEUE in Layer 0 for orchestration, without adding separate manual Phase 5 reset prompts.
todos:
  - id: inspect-roadmap-agent
    content: Inspect `/.cursor/agents/roadmap.md` and note existing structure, safety rules, and MCP usage.
    status: completed
  - id: insert-fallback-block
    content: Add the provided MCP schema bug fallback block at the absolute top of `/.cursor/agents/roadmap.md`, ensuring clear separation and correct formatting.
    status: completed
  - id: align-with-existing-rules
    content: Reconcile any conflicting roadmap agent rules so they explicitly defer to the new top-level MCP-fallback override when schema is degraded.
    status: completed
  - id: prepare-doc-sync
    content: Plan corresponding documentation and sync-file updates to reflect the new fallback behavior (without applying them yet).
    status: completed
  - id: draft-reset-prompt
    content: (Removed) No separate manual Phase 5 reset prompt; rely on existing RESUME_ROADMAP queue item and EAT-QUEUE in Layer 0.
    status: cancelled
isProject: false
---

## Goal

Add an explicit inline fallback rule at the top of the `roadmap` agent so that when the Task-based subagent sees a broken MCP CallMcpTool schema (missing `arguments`), it degrades gracefully to basic file tools instead of hard-blocking RESUME_ROADMAP/deepen runs. Rely on the existing RESUME_ROADMAP queue item (e.g. the Phase 5-2 mint deepen entry) and EAT-QUEUE in Layer 0 for orchestration, instead of introducing a separate manual Phase 5 reset prompt.

## Files to inspect

- `/.cursor/agents/roadmap.md` — current roadmap subagent definition, including Iteration-2 sections, safety contracts, and any existing MCP checks.
- `/.cursor/rules/agents/roadmap.mdc` (if present) — context rules that may reference or constrain roadmap behavior.
- `/.cursor/rules/always/core-guardrails.mdc` and related always rules — to ensure the fallback text does not contradict core safety contracts (even though it is declared as overriding for degraded MCP conditions).

## Implementation steps for the roadmap agent fallback

- **1. Review existing roadmap agent structure**
  - Open `/.cursor/agents/roadmap.md` and scan the current top sections to understand headings, iteration labels, and how safety rules and MCP usage are documented.
  - Identify the earliest point in the file (before Iteration-2 or safety-rule sections) where a prominent, top-level markdown block can be inserted without breaking frontmatter or any required header structure.
- **2. Insert the high-priority fallback block**
  - Add the provided markdown block (starting with `**CURSOR MCP SCHEMA BUG + INLINE FALLBACK OVERRIDE...`**) at the absolute top of `/.cursor/agents/roadmap.md`, ahead of other narrative or rule sections.
  - Preserve the wording and emphasis, including the explicit description of the MCP schema bug, the inline fallback rule bullets, and the mandated behavior (switch to basic-tools-only mode, drift detection, minimal safe updates, nested helpers, `queue_next` handling, `partial_success_mcp_schema_limited` status, and explicit log line).
  - Ensure the new block is clearly separated by blank lines from the content that follows so it renders as a distinct high-priority notice.
- **3. Check for consistency with existing contracts**
  - Scan the rest of `roadmap.md` for any rules that might conflict with the new override (e.g., material-change gates, todo-orchestrator invariants, structural no-op rules).
  - If there are explicit “no-op on missing MCP” or “hard-block on MCP failure” clauses, plan to adjust their wording so they explicitly defer to the new top-level fallback (e.g., add short references like “except when MCP schema is degraded per top-level fallback override”).
  - Keep the behavior hierarchy clear in the text: normal MCP-backed path first; when MCP schema is broken, apply the new basic-tools-only fallback while still honoring global safety constraints as much as possible.
- **4. Plan any necessary documentation touch-ups**
  - Note that, after editing, backbone docs should be updated in a follow-up implementation pass:
    - Add a brief note about the MCP-schema fallback behavior to the relevant roadmap documentation in `3-Resources/Second-Brain/Docs/` (e.g., the roadmap or subagent safety docs).
    - If `.cursor/sync/rules/agents/roadmap.md` or similar sync files exist, mirror any substantive rule changes there per `backbone-docs-sync`.

## -## Validation and next steps (once executed)

- **5. After implementing the plan (future run, not now)**
  - Re-run EAT-QUEUE with a RESUME_ROADMAP `deepen` entry similar to the provided sample payload for Phase 5-2 mint, and observe whether the roadmap agent now:
    - Detects the MCP schema limitation,
    - Enters the basic-tools-only fallback,
    - Writes the expected log/status (`partial_success_mcp_schema_limited` and explicit bug note),
    - And still emits a `queue_followups.next_entry` for forward progress.
  - If the fallback still does not trigger as expected, use the prepared main-chat Phase 5 reset prompt to perform the reset manually via Obsidian MCP, then iterate on the agent text to tighten detection or clarify behavior.

