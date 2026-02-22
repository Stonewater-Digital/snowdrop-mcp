"""Produce analytics for franchise operators."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "franchise_analytics_reporter",
    "description": "Summarizes revenue, royalties, and operational health per franchise operator.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "operator_id": {"type": "string"},
            "period": {"type": "string"},
            "requests": {"type": "array", "items": {"type": "object"}},
            "agent_count": {"type": "integer"},
        },
        "required": ["operator_id", "period", "requests", "agent_count"],
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

ROYALTY_RATE = 0.10


def franchise_analytics_reporter(
    operator_id: str,
    period: str,
    requests: list[dict[str, Any]],
    agent_count: int,
    **_: Any,
) -> dict[str, Any]:
    """Return revenue + health KPIs for a franchise partner."""
    try:
        gross_revenue = sum(float(item.get("revenue", 0.0)) for item in requests)
        royalty_due = gross_revenue * ROYALTY_RATE
        net_revenue = gross_revenue - royalty_due
        total_calls = sum(int(item.get("calls", 0)) for item in requests)
        errors = sum(int(item.get("errors", 0)) for item in requests)
        error_rate = (errors / total_calls) if total_calls else 0.0
        health_score = max(0.0, 1 - error_rate) * 0.6 + min(agent_count / 100, 1) * 0.4
        top_skills = sorted(requests, key=lambda item: item.get("revenue", 0), reverse=True)[:5]
        report = {
            "operator_id": operator_id,
            "period": period,
            "agent_count": agent_count,
            "total_calls": total_calls,
            "error_rate": round(error_rate * 100, 2),
            "top_skills": top_skills,
            "health_score": round(health_score * 100, 2),
        }
        data = {
            "report": report,
            "gross_revenue": round(gross_revenue, 2),
            "royalty_due": round(royalty_due, 2),
            "net_revenue": round(net_revenue, 2),
            "health_score": report["health_score"],
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("franchise_analytics_reporter", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
