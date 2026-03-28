# Ingest Pipeline

**Version: 2026-03 – post-subagent migration**

Documents the full-autonomous-ingest pipeline: Ingest/ processing, Phase 1 propose + Decision Wrapper, Phase 2 apply-mode.

---

## Purpose

Single reference for ingest steps, confidence bands, and return format. Implementation in `.cursor/agents/ingest.md` and legacy-agents/ingest.mdc.

---

## Pipeline steps

1. **List Ingest** — `obsidian_list_notes("Ingest")` for .md; list non-.md in Ingest.
2. **Non-.md** — For each non-.md: create companion .md (title, created, tags, source embed); use Attachment-Subtype-Mapping; backup then attempt move to 5-Attachments/[subtype]; on failure leave in Ingest/ with #needs-manual-move.
3. **Embedded image normalization** — For .md in Ingest: rewrite image embeds to `![[5-Attachments/Images/...]]`; add callout and #needs-attachment-relocation. Never move image files via MCP.
4. **.md** — Run **Phase 1** (propose + Decision Wrapper) or **Phase 2 apply-mode** if this run was triggered by an approved wrapper (hard_target_path from feedback-incorporate).

**Exclusions:** Do not process `Ingest/Decisions/**`, `Ingest/watched-file.md`, watcher-protected notes, or Backups/.

<!-- Gap filled from old Queue-Sources.md -->
**tech_level injection (EAT-QUEUE):** When Second-Brain-Config has `roadmap_tech_progression: true`, the Queue rule may **inject** into `params` for **INGEST MODE** entries a **tech_level** value derived from the note's phase: `high-concept` (phases 1–2), `mid-tech` (phases 3–4), `pseudo-code` (phase 5+). Phase is inferred from note path (e.g. Phase-1, Phase-2) or frontmatter. The Ingest subagent uses tech_level for the Cursor-agent direct-move exception (see Cursor-Agent-Ingest-Workflow).

---

## Phase 1 — full-autonomous-ingest

- **Steps:** Classify PARA → frontmatter-enrich → name-enhance (propose only) → subfolder-organize. Optionally split (high conf), distill, append_to_hub, task-reroute per skill gates. **No move/rename in Phase 1** except Cursor-agent direct move (see below).
- **Confidence:** ≥85% → in-note destructive steps after snapshot; ≥78% → frontmatter, append_to_hub, task-reroute; 70–77% → propose only, #review-needed; <70% → no destructive actions.
- **Cursor-agent direct move:** When note under Ingest/Agent-Output/, Ingest/Agent-Research/ (research synthesis notes), or agent-generated: true; not FORCE-WRAPPER; ingest_conf ≥85%; single clear target. Snapshot → ensure_structure → move dry_run then commit → post-move frontmatter. Log #cursor-agent-direct.
- **Policy boundary:** Direct move above is an ingest auto-apply policy branch for eligible agent-generated notes; it is separate from Decision Wrapper approval semantics. `approved: true` remains wrapper-only state under `Ingest/Decisions/**`.
- **Validator behavior on direct-move branch:** With `prompt_defaults.ingest.validator_block_agent_generated_without_wrapper: false`, validator output is advisory-only for this direct-move branch and does not hard-block by itself. Wrapper/apply-mode and normal ingest paths remain validator-blocking on high severity.
- **Decision Wrapper:** Else create wrapper: propose_para_paths (context_mode wrapper, 7 candidates A–G); fill Templates/Decisions/Decision-Wrapper.md; write to Ingest/Decisions/Ingest-Decisions/Decision-for-{slug}--{date}.md; set decision_candidate, proposal_path on original; ensure CHECK_WRAPPERS entry in queue if missing. STOP move/rename; wait for EAT-QUEUE with approved wrapper.

---

## Phase 2 — apply-mode (from approved wrapper)

- feedback-incorporate → hard_target_path, guidance_text. Re-run classify + frontmatter-enrich + subfolder-organize with hard_target_path. After per-change snapshot and confidence ≥85%: ensure_structure(parent) → obsidian_move_note dry_run then commit → post-move frontmatter. Rename when name-enhance suggested and conf ≥85%. Update wrapper (used_at, processed: true). Queue processor moves wrapper to 4-Archives/Ingest-Decisions/ after apply.

---

## Batch and return

- Process **one note fully** before the next. Batch limit ~5 notes. On failure: log #review-needed in Ingest-Log.md; continue with next note.
- **Return:** One-paragraph summary; any new Decision Wrapper path or queue entry; Success / #review-needed / failure. Append Watcher-Result line when requestId provided.
