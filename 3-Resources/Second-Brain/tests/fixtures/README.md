# Test fixtures

- **sample_queue.jsonl**: Valid prompt-queue lines (DISTILL, SEEDED-ENHANCE, INGEST MODE).
- **sample_note_with_mark.md**: Note with `<mark>` for SEEDED-ENHANCE contract tests.
- **sample_config_snippet.md**: Second-Brain-Config-like snippet for config tests.
- **para-regression/**: Minimal notes for PARA regression; copy to `Ingest/` before running regression (see [[3-Resources/Second-Brain/tests/para-regression|para-regression]] and [[3-Resources/Second-Brain/Regression-Stability-Log|Regression-Stability-Log]]).

E2E: Use full MockMCP for temp-dir vaults; for real test vault add pre-test backup (create_backup).
