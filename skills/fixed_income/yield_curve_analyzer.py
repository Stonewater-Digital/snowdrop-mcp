"""Analyze Treasury yield curve shapes and spreads."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "yield_curve_analyzer",
    "description": "Classifies curve shape and recession signals from key spreads.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "yields": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["yields"],
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


def yield_curve_analyzer(yields: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return spreads, shape classification, and stress metrics."""
    try:
        if not yields:
            raise ValueError("yields cannot be empty")
        term_map = {int(entry["maturity_months"]): float(entry["yield_pct"]) for entry in yields}
        required_terms = [3, 6, 12, 24, 60, 120, 360]
        for term in required_terms:
            term_map.setdefault(term, term_map.get(term, 0.0))
        spread_2y10y = round(term_map.get(24, 0) - term_map.get(120, 0), 3)
        spread_3m10y = round(term_map.get(3, 0) - term_map.get(120, 0), 3)
        ordered_points = sorted(term_map.items())
        shape = _classify_shape(ordered_points, spread_2y10y)
        recession_signal = spread_2y10y < 0 or spread_3m10y < -0.25
        bess_score = max(0.0, min(100.0, 50 + spread_2y10y * 10 + spread_3m10y * 5))
        data = {
            "shape": shape,
            "spread_2y10y": spread_2y10y,
            "spread_3m10y": spread_3m10y,
            "recession_signal": recession_signal,
            "bess_score": round(bess_score, 2),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("yield_curve_analyzer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _classify_shape(points: list[tuple[int, float]], spread_2y10y: float) -> str:
    values = [yield_pct for _, yield_pct in points]
    increasing = all(values[idx] <= values[idx + 1] for idx in range(len(values) - 1))
    decreasing = all(values[idx] >= values[idx + 1] for idx in range(len(values) - 1))
    if abs(spread_2y10y) < 0.25:
        return "flat"
    if spread_2y10y < 0:
        return "inverted"
    if increasing:
        return "normal"
    if decreasing:
        return "inverse_bear"
    return "humped"


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
