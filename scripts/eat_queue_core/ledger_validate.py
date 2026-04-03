"""Post-hoc validation of nested_subagent_ledger / executed_micro_workflow against plan micro_workflow."""

from __future__ import annotations

import re
from typing import Any

from .workflows import ledger_steps_from_micro

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore[misc, assignment]


def _ensure_yaml() -> None:
    if yaml is None:
        raise RuntimeError(
            "ledger_validate requires PyYAML: pip install pyyaml (see scripts/eat_queue_core/requirements.txt)"
        )


def extract_fenced_yaml_blocks(text: str) -> list[str]:
    """Return inner content of ```yaml ... ``` or ``` ... ``` blocks (best-effort)."""
    blocks: list[str] = []
    for m in re.finditer(r"```(?:yaml|yml)?\s*\n([\s\S]*?)```", text, re.IGNORECASE):
        blocks.append(m.group(1).strip())
    return blocks


def _parse_yaml_document(blob: str) -> Any:
    _ensure_yaml()
    return yaml.safe_load(blob)


def _nested_ledger_root(parsed: Any) -> dict[str, Any] | None:
    if isinstance(parsed, dict):
        if "nested_subagent_ledger" in parsed and isinstance(parsed["nested_subagent_ledger"], dict):
            return parsed["nested_subagent_ledger"]
        return parsed
    return None


def validate_executed_micro_workflow(expected: list[str], text_or_yaml: str) -> tuple[bool, str]:
    """
    Parse YAML (optionally from fenced blocks) and compare top-level executed_micro_workflow
    to expected (exact list equality).
    """
    try:
        parsed = _parse_yaml_document(text_or_yaml)
    except Exception:
        blocks = extract_fenced_yaml_blocks(text_or_yaml)
        if not blocks:
            return False, "could not parse YAML"
        parsed = _parse_yaml_document(blocks[0])
    if not isinstance(parsed, dict):
        return False, "root is not a mapping"
    got = parsed.get("executed_micro_workflow")
    if not isinstance(got, list):
        return False, "executed_micro_workflow missing or not a list"
    got_s = [str(x) for x in got]
    if got_s != list(expected):
        return False, f"executed_micro_workflow mismatch: got {got_s!r} want {list(expected)!r}"
    return True, ""


def validate_ledger_steps_executed(expected_micro: list[str], text_or_yaml: str) -> tuple[bool, str]:
    """
    Parse nested_subagent_ledger.steps and verify that the subsequence of step ids that appear
    in the ledger (in execution order) and are listed in ledger_steps_from_micro(expected_micro)
    equals ledger_steps_from_micro(expected_micro) exactly (same length and order).
    """
    expected_ledger = ledger_steps_from_micro(expected_micro)
    if not expected_ledger:
        return True, ""

    blob = text_or_yaml
    try:
        parsed = _parse_yaml_document(blob)
    except Exception:
        blocks = extract_fenced_yaml_blocks(text_or_yaml)
        if not blocks:
            return False, "could not parse YAML"
        parsed = _parse_yaml_document(blocks[0])

    ledger = _nested_ledger_root(parsed)
    if not isinstance(ledger, dict):
        return False, "nested_subagent_ledger root missing"
    steps = ledger.get("steps")
    if not isinstance(steps, list):
        return False, "steps missing or not a list"

    exp_set = set(expected_ledger)
    actual: list[str] = []
    for row in steps:
        if not isinstance(row, dict):
            continue
        sid = row.get("step")
        if isinstance(sid, str) and sid in exp_set:
            actual.append(sid)

    if actual != expected_ledger:
        return False, f"ledger step sequence mismatch: got {actual!r} want {expected_ledger!r}"
    return True, ""
