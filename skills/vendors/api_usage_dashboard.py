"""Aggregate API usage statistics for vendors."""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "api_usage_dashboard",
    "description": "Summarizes token usage, costs, and trends across providers/models/purposes.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "usage_logs": {"type": "array", "items": {"type": "object"}},
            "budget_limit": {"type": "number", "default": 0.0},
        },
        "required": ["usage_logs"],
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


def api_usage_dashboard(
    usage_logs: list[dict[str, Any]],
    budget_limit: float = 0.0,
    **_: Any,
) -> dict[str, Any]:
    """Return consolidated cost dashboard."""
    try:
        total_cost = 0.0
        cost_by_provider: dict[str, float] = defaultdict(float)
        cost_by_purpose: dict[str, float] = defaultdict(float)
        top_calls = sorted(usage_logs, key=lambda log: log.get("cost", 0.0), reverse=True)[:10]
        daily_trend: dict[str, float] = defaultdict(float)
        for log in usage_logs:
            cost = float(log.get("cost", 0.0))
            total_cost += cost
            provider = log.get("provider", "unknown")
            cost_by_provider[provider] += cost
            purpose = log.get("purpose", "general")
            cost_by_purpose[purpose] += cost
            timestamp = log.get("timestamp")
            day = str(timestamp)[:10]
            daily_trend[day] += cost
        budget_utilization = (total_cost / budget_limit * 100) if budget_limit else 0.0
        data = {
            "total_cost": round(total_cost, 2),
            "cost_by_provider": {k: round(v, 2) for k, v in cost_by_provider.items()},
            "cost_by_purpose": {k: round(v, 2) for k, v in cost_by_purpose.items()},
            "top_10_expensive_calls": top_calls,
            "daily_trend": {k: round(v, 2) for k, v in sorted(daily_trend.items())},
            "budget_utilization_pct": round(budget_utilization, 2),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("api_usage_dashboard", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
