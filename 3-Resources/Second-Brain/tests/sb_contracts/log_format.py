"""Log and error format validators (Logs.md, Parameters.md)."""

import re


def validate_pipeline_log_line(line: str) -> bool:
    """Pipeline log line: timestamp, Excerpt, PARA, Changes, Confidence, Proposed MV, Flag, Loop."""
    required = ["| Excerpt:", "| PARA:", "| Changes:", "| Confidence:", "| Proposed MV:", "| Flag:", "| Loop:"]
    if not all(r in line for r in required):
        return False
    return re.search(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}", line) is not None


def validate_watcher_result_line(line: str) -> bool:
    """Watcher-Result: requestId | status | message | trace | completed."""
    parts = ["requestId:", "| status:", "| message:", "| trace:", "| completed:"]
    return all(p in line for p in parts)


def validate_errors_entry(content: str) -> bool:
    """Errors.md entry: ### heading, #### Trace, #### Summary."""
    return "#### Trace" in content and "#### Summary" in content
