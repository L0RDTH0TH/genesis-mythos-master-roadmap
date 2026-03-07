---
name: Guidance-aware run contract
overview: "Implement the user-guidance closed loop: one new frontmatter field (user_guidance), one always-applied rule (Guidance-Aware Run Contract), and an extension to feedback-incorporate so approved/decision re-runs and queue entries with prompt natively use in-note or in-queue guidance as a soft hint for classify, path, split, and distill."
todos: []
isProject: false
---

# Guidance-Aware Run Contract — Implementation Plan

## Goal

Close the gap identified in the system queries: a single, explicit contract so that user refinement instructions (in the note as `user_guidance` or in the queue as `prompt`) are **loaded**, **passed into** the pipeline, and **used as guidance** (soft hint) for classification, path, split, and distill—without overriding safety (snapshot, dry_run, confidence bands).

---

## 1. New frontmatter field: `user_guidance`

**Semantics:** Optional, plain-text, multi-line. Single source of truth for guidance when re-processing a note (approved proposal, decision note, ASYNC-LOOP). Ignored if absent.

**Example:**

```yaml
user_guidance: |
  Atomize this into three atomic notes: one for maps export, one for Terrain3D import, one for biome rules.
  Prefer Resource under Phase-1-Maps. Use kebab-slug-date naming.
```

**Where to document:**

- **[3-Resources/Second-Brain/Parameters.md](3-Resources/Second-Brain/Parameters.md)** — Add a short subsection (e.g. "Optional frontmatter: user_guidance") stating: optional; plain text; used when note is processed in a guidance-aware run (see guidance-aware rule); queue entry `prompt` is fallback when present and note has no `user_guidance`. **YAML-block safe:** "Supports YAML block syntax (`|`) for readability; agent parses as single string. Avoid nested YAML inside it (escape if needed)." Prevents frontmatter parser confusion on re-reads. **Optional:** `guidance_conf_boost` (integer 0–20, e.g. 15): when present and guidance is followed, add that % to the final confidence score for this run (capped at 95%). Helps push marginal notes over the 85% move threshold without faking safety.
- **[3-Resources/Second-Brain/Templates.md](3-Resources/Second-Brain/Templates.md)** — In "Re-queue after edit (§ approved: true)", add one line: user may set `**user_guidance`** (YAML multiline) with refinement instructions; next EAT-QUEUE run will use it as guidance. Optionally add to the "Standard inputs" diagram or a one-line note under proposal callout.

**No change** to Roadmap-Standard-Format unless you want roadmap notes to support `user_guidance` for phase-level decisions (can be added later).

---

## 2. One new always-applied rule: Guidance-Aware Run Contract

**File:** Create **[.cursor/rules/always/guidance-aware.mdc](.cursor/rules/always/guidance-aware.mdc)** (new file; keeps [00-always-core.mdc](.cursor/rules/always/00-always-core.mdc) lean and gives the contract a single, findable home).

**Content (summary):**

- **Trigger (any of):**
  - Note has frontmatter `approved: true` **and** `user_guidance` is present, OR
  - Current queue entry has non-empty `prompt` **and** `source_file` points to a note that has `user_guidance` (or use `prompt` as the guidance when note has no `user_guidance`), OR
  - Note has tag `#guidance-aware`.
- **Behavior:**
  - Load guidance: from note `user_guidance` first; if missing and queue entry has `prompt`, use `prompt` as guidance for this run.
  - **Guidance is never mandatory.** Add one loud line in the rule: "Guidance is a soft hint only. If following it would drop confidence below 72% or violate any safety gate (backup missing, dry_run fail, exclusion match), ignore it and log `guidance_ignored: safety`." Keeps the contract explicit: the agent listens to guidance but does not override safety.
  - Treat it as a **soft hint** for this run only: pass to classify_para (extra context), subfolder-organize (path hint), name-enhance, distill_note, split_atomic. No new MCP parameters required—the agent includes the guidance text in its context when calling these steps.
  - **Length cap:** If `user_guidance` (or queue `prompt`) is very long (e.g. 2000+ words), it could bloat the context window. **Mitigation:** document a soft limit (~500 words); in the rule: "Truncate guidance to first 500 words if >500; log `guidance_truncated: true`."
  - **guidance_conf_boost (optional):** If note has frontmatter `guidance_conf_boost: N` (e.g. 15) and guidance is followed, add N to the final confidence score for this run (capped at 95%). Helps push marginal notes over the 85% move threshold without faking safety.
  - Log in pipeline log: `guidance_used: true | guidance_length: N` (and optionally first 80 chars for traceability); when truncated, `guidance_truncated: true`; when ignored for safety, `guidance_ignored: safety`.
  - **Safety:** Never let guidance override high-confidence (≥85%) destructive actions or safety gates (snapshot, dry_run, confidence bands). Guidance can inform classification/path/split so that confidence moves into mid/high band; it does not bypass snapshot or dry_run.
  - **After run (optional, configurable):** Document that clearing or archiving `user_guidance` after a successful run is configurable (e.g. in Second-Brain-Config: `clear_guidance_after_run: true`). Implementation of the clear step can be a follow-up (rule only documents the contract; skill or pipeline can implement clear when config is set).

**Cross-references:** Link to confidence-loops.mdc (approved: true), auto-eat-queue.mdc (queue entry prompt), and Cursor-Skill-Pipelines-Reference (where guidance is passed).

---

## 3. Extend feedback-incorporate (no new skill)

**File:** [.cursor/skills/feedback-incorporate/SKILL.md](.cursor/skills/feedback-incorporate/SKILL.md).

**Current role:** Scans Mobile-Pending-Actions and note/queue for `approved: true` and text feedback; adapts **params** (lens, liberalness, depth); read-only; no destructive writes.

**Extension:**

- **Also read:** `user_guidance` from the note’s frontmatter (when the note being processed is known—e.g. from queue `source_file` or current context). If the current queue entry has a non-empty `prompt`, use it as **guidance** for this run (fallback when note has no `user_guidance`).
- **Output (in addition to adapted params):** A **guidance** object: `{ guidance_text: string | null, guidance_used: boolean, guidance_length: number }`. When guidance is present, the pipeline (ingest, organize, distill) must **include `guidance_text` in context** when invoking classify_para, subfolder-organize, name-enhance, distill_note, split_atomic—so the agent’s next steps “see” the user’s instructions as a soft hint.
- **Slot:** Already runs at queue start and for ASYNC-LOOP. No new slot; when the queue processor runs feedback-incorporate (optional at start, or when dispatching ASYNC-LOOP / approved proposal), it uses the skill’s output to set run context. When dispatching INGEST MODE / ORGANIZE MODE / DISTILL MODE with a `source_file`, the processor (or the pipeline’s first step) should pass the current entry’s `prompt` and the note’s `user_guidance` into feedback-incorporate and then pass `guidance_text` into the pipeline context for that run.

**Concrete additions to the skill:**

- Step: "If the note (from `source_file` or context) has frontmatter `user_guidance`, set `guidance_text` to that value; else if the current queue entry has non-empty `prompt`, set `guidance_text` to `prompt`. Set `guidance_used` and `guidance_length` accordingly."
- Output: "Emit `guidance_text`, `guidance_used`, `guidance_length` so the pipeline can include guidance in context for classify_para, subfolder-organize, name-enhance, distill_note, split_atomic."
- Reference: Link to the new guidance-aware.mdc rule.

---

## 4. Pipeline and queue integration

**auto-eat-queue.mdc:**

- **Pre-dispatch:** When scanning for notes with `approved: true` (and matching proposal id/tag), also treat notes with `approved: true` **and** `user_guidance` (or `#guidance-aware`) as guidance-aware; when injecting a queue entry for re-processing, set `prompt` from the note’s `user_guidance` if present so the entry carries guidance even if the pipeline reads the note again.
- **Dispatch:** When about to run a pipeline for an entry with non-empty `prompt` or when the note at `source_file` has `user_guidance` or `#guidance-aware`, ensure the run is **guidance-aware**: run feedback-incorporate (or a minimal “load guidance” step) and pass the resulting `guidance_text` into the pipeline context so that when the agent runs classify_para, subfolder-organize, name-enhance, distill_note, split_atomic, it has the guidance in context.

**Cursor-Skill-Pipelines-Reference.md:**

- In **full-autonomous-ingest** (and optionally autonomous-organize, autonomous-distill): add one bullet: “**Guidance-aware run:** When the run is guidance-aware (see guidance-aware.mdc), include `user_guidance` (or queue `prompt`) in context when calling classify_para, subfolder-organize, name-enhance, distill_note, split_atomic. Log `guidance_used`, `guidance_length` in Ingest-Log (or Organize-Log, Distill-Log).”
- No change to pipeline **order**; only to the contract that context may carry guidance when the rule triggers.

**para-zettel-autopilot.mdc (ingest):**

- Add one short line: when a run is guidance-aware (per guidance-aware.mdc), include the loaded guidance as soft context for classification, path, split, and distill; do not override confidence gates or safety.

---

## 5. Logging and observability

- **Pipeline logs** (Ingest-Log, Organize-Log, Distill-Log): when guidance was used, append or structure log line to include `guidance_used: true | guidance_length: N`. Optional: first 80 chars of guidance for debugging.
- **Feedback-Log.md:** feedback-incorporate already logs param adaptation; add optional line when guidance was passed (e.g. “guidance_used: true; length: N”).

---

## 6. Decision note workflow (documentation only)

- In the plan or in [3-Resources/Second-Brain/Queue-Sources.md](3-Resources/Second-Brain/Queue-Sources.md) (or a short “Decision workflow” note): when the user approves a decision note, the macro (or manual edit) sets `approved: true` and `user_guidance: "Move to Phase-2-Terrain3D using option B because..."`. Next EAT-QUEUE sees the contract, runs a guidance-aware ingest (or move) on the original file, and the original moves to the chosen path with the instructions respected and a snapshot created. No code change required beyond the contract and feedback-incorporate; the existing “approve and re-queue” flow becomes guidance-aware when `user_guidance` or queue `prompt` is present.

---

## 7. Backbone docs and sync

Per [backbone-docs-sync.mdc](.cursor/rules/always/backbone-docs-sync.mdc):

- **Rules.md:** Add a row or short subsection for the Guidance-Aware Run Contract (trigger, behavior, safety).
- **Skills.md:** Update feedback-incorporate row to mention guidance output (`guidance_text`, `guidance_used`, `guidance_length`) and that it is used by ingest/organize/distill when guidance-aware.
- **Parameters.md:** Already updated in §1 (user_guidance). Add optional `clear_guidance_after_run` to config options if you document the clear-after-run behavior.
- **Queue-Sources.md:** Clarify that queue entry `prompt` is used as guidance when the run is guidance-aware (and note has no `user_guidance`).
- **Templates.md:** Already updated in §1 (Re-queue + user_guidance).
- **.cursor/sync/:** Add `.cursor/sync/rules/always/guidance-aware.md` (copy of guidance-aware.mdc content). Update `.cursor/sync/skills/feedback-incorporate.md` to match extended SKILL.md. Append changelog entry in `.cursor/sync/changelog.md`.
- **One-line changelog (after implementation):** Add to the changelog section in Pipelines.md or Rules.md (or dedicated changelog): "**2026-03-02:** Added Guidance-Aware Run Contract — user_guidance frontmatter + rule + feedback-incorporate extension. Re-runs now natively respect user refinement instructions."

---

## 8. Implementation order

1. **Parameters.md + Templates.md** — Document `user_guidance` and optional clear behavior.
2. **guidance-aware.mdc** — New rule; then sync to `.cursor/sync/rules/always/guidance-aware.md`.
3. **feedback-incorporate SKILL.md** — Extend with guidance read + output; then sync to `.cursor/sync/skills/feedback-incorporate.md`.
4. **auto-eat-queue.mdc** — Pre-dispatch and dispatch: when injecting entry for approved+user_guidance, set prompt from user_guidance; when dispatching, ensure guidance-aware runs pass guidance into pipeline context.
5. **Cursor-Skill-Pipelines-Reference.md** — Add guidance-aware bullet to full-autonomous-ingest (and optionally organize/distill).
6. **para-zettel-autopilot.mdc** — One line: include guidance in context when guidance-aware.
7. **Queue-Sources.md** — Prompt-as-guidance fallback; optional Decision workflow sentence.
8. **Rules.md, Skills.md** — Tables/diagrams; changelog.

---

## Out of scope (by design)

- **MCP API changes:** classify_para, subfolder_organize, etc. are not given a new “guidance” parameter; the agent simply includes the guidance in its own context when calling them.
- **Automatic clear of user_guidance:** Documented as configurable; implementation of the clear step (e.g. after successful move) can be a separate small change when `clear_guidance_after_run` is set.
- **New skill:** Use feedback-incorporate only; no separate guidance-apply skill unless you later find the extension too heavy.
- **Decision-note integration (future):** Decision notes can auto-populate `user_guidance` from the selected option + user explanation when `approved: true` is set (via Commander macro). This ties the two workflows together without forcing implementation now. See future enhancement in Queue-Sources.md.

