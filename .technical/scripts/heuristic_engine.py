#!/usr/bin/env python3
"""Control plane v2 — optional adaptive cap helper. See Control-Plane-Heuristics-v2.md."""
from __future__ import annotations
import json, math, sys

def compute_effective_cap(payload: dict) -> dict:
    cfg = payload.get("adaptive_cap_config") or {}
    if not cfg.get("enabled", False):
        return {"effective_cap_used": None, "H": None, "P": None, "V": None, "note": "adaptive_cap disabled"}
    base = float(cfg.get("base") or 8)
    min_cap = int(cfg.get("min_cap") or 3)
    max_cap = int(cfg.get("max_cap") or 12)
    h_max = float(cfg.get("h_max") or 0.4)
    cw = float(cfg.get("circling_weight") or 0.08)
    hints = payload.get("tail_hints") or {}
    circling = float(hints.get("circling_score") or 0.0)
    H = min(h_max, max(0.0, circling * cw))
    P = max(0.1, min(float(hints.get("progress_mult") or 1.0), 1.5))
    V = max(0.1, min(float(hints.get("velocity_mult") or 1.0), 1.5))
    raw = base * (1.0 - H) * P * V
    cap = max(min_cap, min(max_cap, int(math.floor(raw))))
    return {"effective_cap_used": cap, "H": round(H, 4), "P": round(P, 4), "V": round(V, 4), "note": "ok"}

def main() -> int:
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(json.dumps({"error": "invalid_json", "detail": str(e)}))
        return 2
    out = compute_effective_cap(data if isinstance(data, dict) else {})
    print(json.dumps(out))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

