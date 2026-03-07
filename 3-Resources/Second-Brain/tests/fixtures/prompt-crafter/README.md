# Prompt-crafter fixtures

Samples for prompt-crafter contract tests.

- **config.yaml**: Minimal prompt_defaults snippet (ingest, organize).
- **base-prompt.md**: Assembly-order and trigger placeholder (INGEST MODE + params line).
- **expected-queue.jsonl**: One valid queue line with `params`; assert config + base-prompt assembly yields this shape. Assert no param leaks (invalid keys rejected). Integration test: mock MCP propose_para_paths; assert A–G paths pad to 7 per Pipelines.

Expected line format: `{"mode":"INGEST MODE","params":{"context_mode":"strict-para","max_candidates":7,"rationale_style":"concise"},"id":"req-fixture-1"}`
