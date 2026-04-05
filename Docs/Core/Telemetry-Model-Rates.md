---
title: Telemetry Model Rates
created: 2026-03-15
tags: [second-brain, telemetry, run-telemetry]
para-type: Resource
status: active
---

# Telemetry Model Rates

Reference for computing **cost_estimate_usd** in Run-Telemetry notes. When this table (or an equivalent in Config) is populated, writers that have token estimates (e.g. roadmap-deepen) may set `input_tokens`, `output_tokens`, `total_tokens`, and `cost_estimate_usd` in the Run-Telemetry note.

## Format

- **Model id** — e.g. `gpt-4o`, `claude-3.5-sonnet-20241022`, `o1-preview`, `local-llama-70b`. Must match the `model` field used in Run-Telemetry when present.
- **Input $/1K tokens** — optional; if absent, use a single rate.
- **Output $/1K tokens** — optional; if absent, use input rate for both.
- **Single rate $/1K tokens** — when input/output are not split, use this for total_tokens.

## Example (placeholder)

| Model | Input $/1K | Output $/1K | Notes |
|-------|------------|-------------|-------|
| (add rows) | — | — | Source: provider pricing pages; update periodically. |

Agents multiply (input_tokens/1000 × input_rate) + (output_tokens/1000 × output_rate), or total_tokens/1000 × single_rate, and write **cost_estimate_usd** to the Run-Telemetry note. See [[3-Resources/Second-Brain/Logs#Run-Telemetry|Logs § Run-Telemetry]] Phase 2 and [[.cursor/skills/roadmap-deepen/SKILL|roadmap-deepen]] Run-Telemetry step.
