"""Estimate term premium from yield vs expected short-rate path."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Sequence

TOOL_META: dict[str, Any] = {
    "name": "term_premium_calculator",
    "description": "Compares observed term yield to expected average of policy rates.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "term_yield_pct": {"type": "number"},
            "expected_short_path_pct": {"type": "array", "items": {"type": "number"}},
            "convexity_adjustment_bps": {"type": "number", "default": 0.0},
        },
        "required": ["term_yield_pct", "expected_short_path_pct"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {"type": "object"},
            "timestamp": {"type": "string"},
        },
    },
}


def term_premium_calculator(
    term_yield_pct: float,
    expected_short_path_pct: Sequence[float],
    convexity_adjustment_bps: float = 0.0,
    **_: Any,
) -> dict[str, Any]:
    """Return simple term premium estimate."""
    try:
        if not expected_short_path_pct:
            raise ValueError("expected_short_path_pct cannot be empty")
        avg_expected = sum(expected_short_path_pct) / len(expected_short_path_pct)
        premium = term_yield_pct - avg_expected - convexity_adjustment_bps / 100
        data = {
            "average_expected_short_rate_pct": round(avg_expected, 3),
            "term_premium_pct": round(premium, 3),
            "convexity_adjustment_bps": convexity_adjustment_bps,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        _log_lesson(f"term_premium_calculator: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
