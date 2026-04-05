"""Queue lane filtering — aligned with queue.mdc A.2a and Queue-Sources."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import QueueEntry

DEFAULT_LANE = "default"
SHARED_LANE = "shared"

# When Config queue.allowed_lanes is unreadable; must match queue.mdc / Second-Brain-Config default.
FALLBACK_ALLOWED_LANES: frozenset[str] = frozenset(
    {"default", "shared", "sandbox", "godot", "core"}
)


def effective_queue_lane(entry: QueueEntry) -> str:
    raw = getattr(entry, "queue_lane", None)
    if isinstance(raw, str) and raw.strip():
        return raw.strip()
    return DEFAULT_LANE


def entry_in_lane_dispatch_subset(lane_filter: str | None, entry: QueueEntry) -> bool:
    """Return True if entry should be included when dispatching with the given filter."""
    if lane_filter is None:
        return True
    eff = effective_queue_lane(entry)
    if lane_filter == SHARED_LANE:
        return eff == SHARED_LANE
    if lane_filter == DEFAULT_LANE:
        return eff == DEFAULT_LANE
    # Track lanes (sandbox, godot, core, …): self ∪ shared
    return eff == lane_filter or eff == SHARED_LANE


def filter_entries_by_lane(
    entries: list[QueueEntry],
    lane_filter: str | None,
) -> list[QueueEntry]:
    if lane_filter is None:
        return list(entries)
    return [e for e in entries if entry_in_lane_dispatch_subset(lane_filter, e)]


def validate_lane_filter_token(token: str, allowed: frozenset[str] | None) -> bool:
    allow = allowed if allowed is not None else FALLBACK_ALLOWED_LANES
    return token in allow
