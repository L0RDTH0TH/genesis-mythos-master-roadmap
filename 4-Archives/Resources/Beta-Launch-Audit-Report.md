# Second Brain — Pre-Launch Beta Audit Report

**Project**: Second Brain (PARA-Zettel Autopilot) — personal knowledge management (PKM) with Obsidian + Cursor + MCP pipelines  
**Audit date**: 2026-03-01  
**Scope**: Code quality, security, performance, pipelines, UX, documentation, testing, and beta readiness

---

## Project Assumptions (Updated)

| Assumption | Actual / Notes |
|------------|----------------|
| **Tech stack** | **Obsidian** (markdown vault, Local REST API), **Cursor** (rules + skills in `.cursor/`), **MCP server** (obsidian-para-zettel-autopilot, external), **Python** (contract tests only, no backend service), **JavaScript** (Obsidian plugins: Watcher, QuickAdd, Dataview, etc.). No FastAPI/React/PostgreSQL. |
| **Core components** | Note storage (markdown in vault), search/retrieval (Obsidian + MCP `obsidian_global_search`, `obsidian_list_notes`), AI integration (Cursor agent + MCP classify/distill/suggest), no traditional user auth (single-user vault; API key in env for Local REST API), export/import (vault sync, backups, snapshots). |
| **Goals** | Stability (backup/snapshot/dry_run gates), security (no keys in repo; env-only), performance (batch caps, queue fast-path), usability (trigger phrases, Commander, Watcher-Result). Beta: gather feedback via Feedback-Log, Errors.md, and optional in-app surveys. |

---

## Phase 1: Code Quality and Bug Audit

### Findings

| Item | Severity | Description |
|------|----------|-------------|
| **Path exclusion contract mismatch** | **Fixed** | `helpers.is_excluded_path()` did not exclude `3-Resources/Second-Brain/tests/`. Vault-Layout.md and Testing.md require tests/ to be excluded from pipelines. **Fix applied**: added `Second-Brain/tests/` check in `tests/helpers.py`. All 64 tests now pass. |
| **Unused / optional pytest import** | Low | `helpers.py` optionally imports `pytest` for parametrize; no tests use it. Safe to leave for future use or remove to avoid confusion. |
| **Log/error format contract** | Strength | `sb_contracts/log_format.py` and unit tests enforce Errors.md entry structure and Watcher-Result line format — good for consistency. |
| **No Python style enforcement** | Low | No `pyproject.toml`, `pylint`, or `ruff` in repo. Python is limited to tests and contract helpers; style is readable and consistent. |
| **Error Handling Protocol** | Strength | Centralized in mcp-obsidian-integration.mdc: trace, summary, log to Errors.md, severity, recovery. Reduces ad-hoc error handling. |

### Recommendations

1. **Add tests folder to exclusion (done)**  
   In `3-Resources/Second-Brain/tests/helpers.py`, ensure `is_excluded_path()` returns `True` for paths under `Second-Brain/tests/` so pipeline rules never process test files. Implemented as:
   ```python
   # 3-Resources/Second-Brain/tests/** (test suite; not pipeline input; Vault-Layout)
   if "Second-Brain/tests/" in path_norm or path_norm.startswith("Second-Brain/tests/"):
       return True
   ```

2. **Optional: add Python lint for tests**  
   For future Python growth, add `pyproject.toml` with `ruff` or `pylint` and run in CI:
   ```toml
   [tool.ruff]
   line-length = 100
   target-version = "py312"
   ```

### Priority for beta

- **Path exclusion fix**: **High** (done; prevents pipelines from ever touching test files).
- **Pylint/ruff**: **Low** (nice-to-have for consistency).

### Feedback hooks

- **Log test failures to Errors.md**: Testing.md already suggests appending test failures to Errors.md for observability. Optional: in `run_tests.py`, on `result.failures` or `result.errors`, append a short entry to `3-Resources/Errors.md` with pipeline `automated-test`, severity `low`, and trace.

---

## Phase 2: Security Audit

### Findings

| Item | Severity | Description |
|------|----------|-------------|
| **API key handling** | Strength | OBSIDIAN_API_KEY documented as env-only (Configs.md, CONFIG-REFERENCE, mcp.json). Rules explicitly say "sanitize: no API keys or secrets" in error traces. No keys committed in repo. |
| **QuickAdd data.json** | Medium | `.obsidian/plugins/quickadd/data.json` contains `apiKey: ""` and `migrateProviderApiKeysToSecretStorage: true`. Empty key is safe; ensure beta users do not commit real keys. Document in onboarding: "Use Obsidian secret storage for AI provider keys." |
| **Ingest/Untitled.md** | Low | Contains example JSON with placeholder "OBSIDIAN_API_KEY": "...". Ensure this is clearly marked as example only and not used in production. |
| **SQL/NoSQL** | N/A | No database; vault is file-based. No SQL injection surface. |
| **XSS / CSRF** | Low | Obsidian renders markdown locally; no web app surface. MCP runs in Cursor context; no browser CSRF. |
| **Data privacy (GDPR)** | Medium | User notes are stored locally. If vault is synced to cloud or shared, document data residency and that logs (Ingest-Log, Errors.md, Feedback-Log) may contain note paths and excerpts — avoid PII in log content (already stated in Feedback-Log: "no PII"). |

### Recommendations

1. **Add .cursorignore / .gitignore for sensitive plugin data**  
   If any plugin ever stores keys in vault, ensure `.obsidian/plugins/*/data.json` or secret files are in .cursorignore so they are not indexed. Currently .cursorignore focuses on `.technical/`, `*.jsonl`, `Watcher-*.md`. Optional: add a note in Configs.md: "Do not commit plugin data that contains API keys; use env or Obsidian secret storage."

2. **Backup directory**  
   BACKUP_DIR (e.g. Second-Brain-oops-Backups) should be on encrypted or access-controlled storage when vault is synced. Already noted in mcp-obsidian-integration.mdc; reiterate in beta release notes.

### Priority for beta

- **QuickAdd / plugin keys**: **Medium** — document in Install-and-Setup or README: "Store AI provider API keys in Obsidian secret storage only."
- **Backup dir encryption**: **Low** — documentation only.

### Feedback hooks

- **Security feedback**: Add optional "Report a security concern" link or template in README or 0-Onboarding pointing to a private channel (e.g. GitHub Security Advisories or email) so beta users can report without posting publicly.

---

## Phase 3: Performance and Scalability Audit

### Findings

| Item | Severity | Description |
|------|----------|-------------|
| **Batch size caps** | Strength | Second-Brain-Config `batch_size_for_snapshot: 5` and pipeline rules limit batch sizes (e.g. distill "up to ~5 notes"). Reduces risk of runaway batches. |
| **Queue fast-path** | Strength | auto-eat-queue: single-entry fast-path avoids full dedup/sort when only one item. Good for mobile single-tap. |
| **No database** | N/A | No DB indexing or query optimization; Obsidian and MCP operate on flat files. |
| **MCP server** | External | Performance of classify_para, distill_note, etc. depends on external MCP server (and any LLM calls). Not in vault repo. |
| **Async / preview cap** | Strength | async_preview_threshold and commander_macro_limits (e.g. 5) cap chained commands and preview overload. |

### Recommendations

1. **Document recommended batch sizes**  
   In Pipelines.md or Parameters.md, state recommended max batch sizes per pipeline (e.g. ingest 10, distill 5, archive 10) so beta users and scripts do not overload in one run.

2. **Health check frequency**  
   Rules suggest calling health_check every N notes or on first error. Document N (e.g. 10) in Logs.md or MCP-Health so operators know when to expect health entries.

### Priority for beta

- **Batch size docs**: **Medium** — reduces support burden.
- **Health check N**: **Low**.

### Feedback hooks

- **Performance feedback**: In Feedback-Log or a "Beta feedback" note, add optional fields: `batch_size`, `duration_seconds`, `notes_processed`. Skills/rules can append these when available so you can analyze slow runs.

---

## Phase 4: Pipeline and Integration Audit

### Findings

| Item | Severity | Description |
|------|----------|-------------|
| **Canonical pipeline order** | Strength | Cursor-Skill-Pipelines-Reference.md defines full-autonomous-ingest, autonomous-distill, archive, express, organize with fixed step order. Integration tests assert backup → … → move_note and dry_run before commit. |
| **CI/CD** | Strength | `.github/workflows/test.yml` runs Python tests on push/PR (unittest discover). No deploy step (vault is local/sync). |
| **MCP tool surface** | Strength | 40+ tools (read_note, update_note, move_note, classify_para, create_backup, etc.) with descriptors in mcps/user-obsidian-para-zettel-autopilot/tools/. Rollback: backup + per-change snapshots before destructive steps. |
| **ensure_structure + move_note** | Strength | Documented fallback: if move fails (e.g. parent missing), call obsidian_ensure_structure then retry. Deep-nested PARA behavior verified per mcp-obsidian-integration. |
| **Watcher bridge** | Strength | Watcher-Signal.md → Cursor; Watcher-Result.md with requestId, status, message, trace, completed. Clear contract for Obsidian Watcher plugin. |

### Recommendations

1. **CI: run from vault root**  
   Current workflow runs `python -m unittest discover -s 3-Resources/Second-Brain/tests -p "test_*.py"`. Ensure working directory is repo root so any path-dependent fixtures or config resolve correctly. Already correct if checkout is repo root.

2. **Add smoke test badge**  
   In README, add a badge linking to GitHub Actions "Run Tests" workflow so beta users see at a glance that tests pass.

3. **Rollback documentation**  
   Restore-queue mode is user-triggered; document in Backup-Log or Logs.md the exact format for restore list (e.g. Restore-Queue.md with columns snapshot_path, original_path) so users can self-serve.

### Priority for beta

- **Smoke badge**: **Low** — improves confidence.
- **Restore-queue format**: **Medium** — reduces confusion after a bad run.

### Feedback hooks

- **Pipeline failure feedback**: Errors.md already captures pipeline and stage. Optional: add `user_reported: true` and a short "What did you do before this?" template for beta users to paste in when reporting.

---

## Phase 5: User Experience and Accessibility Audit

### Findings

| Item | Severity | Description |
|------|----------|-------------|
| **Trigger phrases** | Strength | Natural-language triggers (INGEST MODE, DISTILL MODE, EAT-QUEUE, etc.) and Backbone/README trigger cheat sheet improve discoverability. |
| **Commander** | Strength | Optional Commander plugin surfaces macros (e.g. Queue Highlight Perspective, Async Approve) for mobile and desktop. Reduces reliance on typing. |
| **Watcher-Result** | Strength | Popup-friendly format (requestId, status, message, completed) so Watcher plugin can show success/failure and lag. |
| **Error messages** | Strength | Error Handling Protocol requires Summary with Root cause, Impact, Suggested fixes, Recovery. Good for support. |
| **UI/UX** | N/A | No custom web UI; Obsidian provides the UI. Accessibility (ARIA, contrast) is Obsidian’s responsibility. |
| **Onboarding** | Strength | Second-Brain-Starter-Kit has 0-Onboarding (Welcome, Install-and-Setup, Mobile-Setup). Templates and README explain PARA and triggers. |

### Recommendations

1. **Beta onboarding**  
   Add a short "Beta feedback" section in Welcome or Install: "We’re in beta. If something breaks or feels wrong, note it in Feedback-Log or open an issue; we use it to prioritize fixes."

2. **Feedback button / quick action**  
   Add a Commander macro or QuickAdd capture that opens Mobile-Pending-Actions or a "Beta feedback" note with template: date, trigger used, what happened, what you expected. One-tap from mobile.

3. **Accessibility**  
   For any future custom UI (e.g. dashboard in Obsidian), ensure ARIA labels and keyboard navigation. Current scope is markdown + Obsidian core; no change required for beta.

### Priority for beta

- **Beta feedback callout**: **High** — sets expectations and channels feedback.
- **Feedback quick action**: **Medium** — increases likelihood users report.

### Feedback hooks

- **Telemetry**: Feedback-Log and pipeline logs already provide usage data (loop outcomes, commander_macro, batch sizes). Optional: add a voluntary "Feedback type: bug | feature | unclear" field in the feedback template for easier triage.

---

## Phase 6: Documentation and Testing Audit

### Findings

| Item | Severity | Description |
|------|----------|-------------|
| **README** | Strength | Vault README explains PARA, Ingest, MCP rebuild, and optional zip distribution. Second-Brain/README adds trigger cheat sheet and troubleshooting. |
| **Backbone docs** | Strength | 3-Resources/Second-Brain/ indexes Rules, Skills, Pipelines, Plugins, MCP-Tools, Configs, Parameters, Logs, Vault-Layout, Queue-Sources, Templates, Testing. Mermaid diagrams in multiple docs. |
| **API specs** | N/A | No REST API; MCP tools are documented via descriptor JSON and MCP-Tools.md. |
| **Test coverage** | Strength | 64 tests: unit (queue, path exclusions, log format, config, frontmatter, snapshot, highlight) and integration (pipeline order, confidence bands, dry_run, backup/snapshot order, async/mobile). All pass after path-exclusion fix. |
| **E2E** | Low | Testing.md mentions E2E with MockMCP and optional test vault; no automated E2E in CI. Acceptable for beta. |
| **Smoke tests** | Strength | CI runs full unittest suite; effectively smoke tests for contracts and safety invariants. |

### Recommendations

1. **Changelog**  
   Maintain a short CHANGELOG.md or "Releases" section in README with version and date (e.g. "Beta 0.1 — 2026-03-01: path exclusion fix, 64 tests passing, Feedback-Log and Errors.md for beta feedback").

2. **Testing.md**  
   Add one line: "Test failures can be appended to Errors.md (pipeline: automated-test) for unified observability." Aligns with existing Testing.md suggestion.

3. **Beta test scenarios**  
   Document 3–5 "Beta test scenarios" in Testing.md or 0-Onboarding: e.g. (1) Drop note in Ingest → INGEST MODE → check PARA placement; (2) EAT-QUEUE with one Task-Complete; (3) DISTILL MODE on one note; (4) Archive one completed project note; (5) Run tests locally. Helps beta users validate setup.

### Priority for beta

- **Changelog / release note**: **High** — single place for "what’s in beta."
- **Beta test scenarios**: **Medium** — improves quality of feedback.
- **E2E in CI**: **Low** — post-beta.

### Feedback hooks

- **Doc feedback**: In README or Second-Brain/README, add: "Docs unclear? Log in Feedback-Log with source: documentation and the page/section."

---

## Phase 7: Overall Recommendations for Beta Launch

### Top 10 priorities

| # | Priority | Action | Phase |
|---|----------|--------|-------|
| 1 | **Path exclusion for tests/** | Done: `helpers.is_excluded_path()` now excludes `Second-Brain/tests/`. | 1 |
| 2 | **Beta feedback callout** | Add short "We’re in beta" + where to report (Feedback-Log, issues) in Welcome or README. | 5 |
| 3 | **Changelog / release note** | Add CHANGELOG.md or Beta 0.1 entry in README with date and main changes. | 6 |
| 4 | **Plugin API key guidance** | Document "Use Obsidian secret storage for AI provider keys" in Install-and-Setup or README. | 2 |
| 5 | **Restore-queue format** | Document Restore-Queue.md format (snapshot_path, original_path) in Logs.md or Backup-Log. | 4 |
| 6 | **Beta test scenarios** | Add 3–5 step-by-step scenarios (Ingest, EAT-QUEUE, Distill, Archive, run tests) in Testing or Onboarding. | 6 |
| 7 | **Feedback quick action** | Commander macro or QuickAdd that opens feedback note with template (date, trigger, what happened). | 5 |
| 8 | **Batch size recommendations** | State recommended max batch sizes per pipeline in Parameters or Pipelines. | 3 |
| 9 | **CI badge** | Add GitHub Actions "Run Tests" badge to README. | 4 |
| 10 | **Optional: test failures → Errors.md** | In run_tests.py, optionally append failed run summary to Errors.md (pipeline: automated-test). | 1 |

### Proposed changelog for beta release

```markdown
## Beta 0.1 (2026-03-01)

- **Ingest / Organize / Distill / Archive / Express**: Full pipeline set with backup, snapshot, dry_run, and confidence gates.
- **Queue**: EAT-QUEUE and Task-Queue with fast-path, dedup, and Watcher-Result contract.
- **Safety**: Path exclusions include tests/, Backups/, Logs, Watcher paths; Error Handling Protocol and Errors.md.
- **Observability**: Ingest-Log, Distill-Log, Archive-Log, Express-Log, Organize-Log, Backup-Log, Feedback-Log, Errors.md; Vault-Change-Monitor MOC.
- **Testing**: 64 automated tests (unit + integration) for queue, path exclusions, config, frontmatter, snapshot, pipeline order, confidence bands, safety invariants. CI on push/PR.
- **Fix**: Path exclusion for `3-Resources/Second-Brain/tests/` so pipelines never process test files.
- **Docs**: Backbone, Pipelines, Logs, Parameters, Vault-Layout, Queue-Sources, Testing, Configs.
```

### Post-beta feedback plan

| Channel | Purpose |
|---------|---------|
| **Feedback-Log.md** | Loop outcomes, queue analytics, commander_macro; optional user refinements and batch stats. Create if missing; rotate with log-rotate. |
| **Errors.md** | Pipeline and test failures; Error Handling Protocol. Users can add "user_reported" or paste "what I did" for support. |
| **GitHub issues** | Bugs, feature requests. Link from README or Beta feedback section. |
| **In-vault "Beta feedback" note** | Optional template: date, trigger, what happened, expected; link from Commander or QuickAdd. |
| **Evolution monitoring** | Periodically analyze Feedback-Log (e.g. drift_avg, loop_refinements_count, commander_macro usage) and document in Backbone or a dedicated note; use for prioritization. |

---

## Summary

The Second Brain project is **well-structured for a beta launch**: clear PARA/CODE model, strong safety (backup, snapshot, dry_run, confidence bands), centralized error handling and logging, and a solid test suite (64 tests, all passing after the path-exclusion fix). The main gaps are **documentation and feedback instrumentation**: beta callout, changelog, plugin key guidance, restore-queue format, and optional feedback quick action and test-failure logging. Applying the top 10 priorities will polish the beta and make it easier to collect and act on user feedback.

---

*Audit performed per structured phases. Tech stack and assumptions updated to reflect Obsidian + Cursor + MCP (no traditional backend).*
