---
title: Second Brain Testing
created: 2026-03-01
tags: [pkm, second-brain, testing, cursor]
para-type: Resource
status: active
links: ["[[Resources Hub]]", "[[3-Resources/Second-Brain/README]]"]
---

# Second Brain Automated Testing

Automated tests for the Second Brain system: queue parsing, path exclusions, log/error formats, config contracts, frontmatter/snapshot/highlight contracts, pipeline order, confidence bands, and safety invariants. Skills are tested via **contracts** and **reference logic** (no live MCP or agent execution in unit/integration tests).

## Where tests live

- **Root**: `3-Resources/Second-Brain/tests/`
- **Unit**: `tests/unit/` — queue, path exclusions, log/error format, config, frontmatter, snapshot, highlight contracts
- **Integration**: `tests/integration/` — pipeline flow, confidence bands, safety (dry_run, backup/snapshot), async/mobile
- **Fixtures**: `tests/fixtures/` — sample queue lines, sample notes (e.g. with `<mark>` for SEEDED-ENHANCE), config snippets. **prompt-crafter**: `tests/fixtures/prompt-crafter/` — e.g. `config.yaml` snippet + `base-prompt.md` → `expected-queue.jsonl`; assert no param leaks (invalid keys rejected). **Integration test**: Mock MCP propose_para_paths return; assert stabilized A–G paths match expected (pad to 7 per Pipelines).
- **Contract helpers**: `tests/sb_contracts/` — queue, log_format, config (and `helpers.py`: parse_frontmatter, is_excluded_path, MockVault, MockMCP)

**Exclusion**: Do **not** process `tests/` as pipeline input; exclude in rules/docs so pipelines never ingest or move test files.

## How to run

From the vault root:

```bash
python -m unittest discover -s 3-Resources/Second-Brain/tests -p "test_*.py" -v
```

Or from the tests directory:

```bash
cd 3-Resources/Second-Brain/tests && python -m unittest discover -s . -p "test_*.py" -v
```

For **chat-based runs** (e.g. in Cursor `code_execution`), use **run_in_repl** mode so results are returned as a string:

```bash
cd 3-Resources/Second-Brain/tests && python run_tests.py --repl
```

## What is covered

| Layer | Scope |
|-------|--------|
| **Unit** | Queue parse/validate/dedup/sort, path exclusions, log and Errors.md format, config keys and confidence bands, frontmatter-enrich contract, snapshot frontmatter, highlight_angles/data-drift-level, basic `obsidian_propose_para_paths` contract (JSON shape, candidate fields present, score range) |
| **Integration** | Pipeline step order (full-autonomous-ingest), confidence bands (high/mid/low), dry_run before move, backup/snapshot before destructive, async preview and re-queue, Decision Wrapper creation using ranked PARA proposals (A–G mapping, no single-option fallback) |
| **E2E** | Documented in fixtures/README: use full MockMCP for temp-dir; optional test vault with pre-test backup |

## Test coverage by responsibility

Mapping from [[3-Resources/Second-Brain/Responsibilities-Breakdown|Responsibilities-Breakdown]] to test files (for audit alignment):

| Responsibility | Coverage | Notes |
|----------------|----------|-------|
| Pipelines: full-autonomous-ingest (Phase 1 wrapper) | Integration: test_pipeline_flow.py | Asserts chain order, no move. |
| Rules: mcp-obsidian-integration (backup gate) | Unit: test_safety_invariants.py | Mocks ensure_backup. |
| Skills: classify_para | Contract / fixtures | Fixture input → expected candidates (para-regression). |
| Queue parse/validate/dedup | Unit: test_queue.py | Queue parsing and validation. |
| Path exclusions | Unit: test_path_exclusions.py | Excluded paths not processed. |
| Log and Errors.md format | Unit: test_log_format.py | Log format contracts. |
| Config keys and confidence bands | Unit: test_config_contract.py | Config contract. |
| Frontmatter / snapshot / highlight | Unit: test_frontmatter_contract.py, test_snapshot_contract.py, test_highlight_contract.py | Metadata and highlight contracts. |
| Confidence bands (high/mid/low), async | Integration: test_confidence_bands.py, test_async_mobile.py | Bands and async preview. |
| Gaps | — | TODO: e.g. Mobile async preview integration. |

Test failures can be appended to **Errors.md** for unified observability (see [[3-Resources/Second-Brain/Logs|Logs]]).

## How to add tests

1. **Unit test**: Add a new `test_*.py` under `tests/unit/`. Use `helpers.parse_frontmatter`, `helpers.is_excluded_path`, or `sb_contracts.*` as needed. No MCP calls; use MockVault or inline dicts for note content.
2. **Integration test**: Add under `tests/integration/`. Use `unittest.mock` to patch MCP tools if needed; assert call order (e.g. dry_run=True before dry_run=False) or step sequence. For PARA proposals and Decision Wrappers, assert that ingest wrapper creation calls `obsidian_propose_para_paths` with the expected `context_mode` and that the rendered wrapper shows A–G options (up to 7 ranked candidates populated from the engine, with no single-option fallback) consistent with mocked candidates.
3. **Fixture**: Add sample data under `tests/fixtures/` and reference it from tests (or embed strings).
4. **Contract helper**: If a reusable validator or parser is needed, add it in `tests/sb_contracts/` (e.g. `log_format.py`, `config.py`) and keep it dependency-free (no pyyaml; simple frontmatter parse in helpers).

See [[3-Resources/Second-Brain/Pipelines|Pipelines]] and [[3-Resources/Second-Brain/Cursor-Skill-Pipelines-Reference|Cursor-Skill-Pipelines-Reference]] for pipeline order and snapshot triggers; [[.cursor/rules/always/mcp-obsidian-integration|mcp-obsidian-integration]] for safety and Error Handling Protocol.
