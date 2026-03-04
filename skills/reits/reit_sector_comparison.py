"""Compare REIT metrics versus sector medians."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "reit_sector_comparison",
    "description": "Benchmarks company metrics versus sector medians across KPIs.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "company_metrics": {"type": "object"},
            "sector_medians": {"type": "object"},
        },
        "required": ["company_metrics", "sector_medians"],
    },
    "outputSchema": {"type": "object", "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}}},
}


def reit_sector_comparison(
    company_metrics: dict[str, float],
    sector_medians: dict[str, float],
    **_: Any,
) -> dict[str, Any]:
    """Return comparison table identifying beats vs lags."""
    try:
        comparisons = {}
        beats = 0
        lags = 0
        for metric, company_value in company_metrics.items():
            sector_value = sector_medians.get(metric)
            if sector_value is None:
                continue
            delta = company_value - sector_value
            percent_diff = delta / sector_value * 100 if sector_value else 0.0
            trend = "beat" if percent_diff > 0 else "lag" if percent_diff < 0 else "inline"
            if trend == "beat":
                beats += 1
            elif trend == "lag":
                lags += 1
            comparisons[metric] = {"delta": round(delta, 2), "percent_diff": round(percent_diff, 2), "trend": trend}
        data = {
            "comparisons": comparisons,
            "beats": beats,
            "lags": lags,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("reit_sector_comparison", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
