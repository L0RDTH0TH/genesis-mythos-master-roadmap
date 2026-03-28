# Prompt-crafter fixtures

Samples for prompt-crafter and question-led prompt crafter contract tests.

- **config.yaml**: Minimal prompt_defaults snippet (ingest, organize).
- **base-prompt.md**: Assembly-order and trigger placeholder (INGEST MODE + params line).
- **expected-queue.jsonl**: One valid queue line with `params`; assert config + base-prompt assembly yields this shape. Assert no param leaks (invalid keys rejected). **Question-led crafter**: Given A/B/C answers (and manual text for params with accepts_manual_text), resolved payload should match this shape; see [Prompt-Crafter-Examples](3-Resources/Second-Brain/Prompt-Crafter-Examples.md) and C resolution rules.

**Tests**: `unit/test_prompt_crafter_contract.py` — fixture file exists, each line valid JSON with required fields (mode, validate_entry), INGEST params match expected shape and allowed set; resolved payload shape and param-leak check.

Expected line format: `{"mode":"INGEST MODE","params":{"context_mode":"strict-para","max_candidates":7,"rationale_style":"concise"},"id":"req-fixture-1"}`
