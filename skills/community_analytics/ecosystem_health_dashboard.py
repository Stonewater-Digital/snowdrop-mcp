"""Public-facing ecosystem health summary."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "ecosystem_health_dashboard",
    "description": "Aggregates community metrics into a public health score and highlights.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "metrics": {"type": "object"},
        },
        "required": ["metrics"],
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


def ecosystem_health_dashboard(metrics: dict[str, Any], **_: Any) -> dict[str, Any]:
    """Compute the health score and supporting insights."""
    try:
        score = _score(metrics)
        status = "stable"
        if score > 80:
            status = "thriving"
        elif score < 50:
            status = "watchlist"
        highlights = _highlights(metrics)
        data = {
            "health_score": round(score, 2),
            "status": status,
            "public_metrics": metrics,
            "month_over_month": metrics.get("mom", {}),
            "highlights": highlights,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("ecosystem_health_dashboard", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _score(metrics: dict[str, Any]) -> float:
    total_agents = metrics.get("total_agents", 0)
    active_ratio = metrics.get("active_agents_30d", 0) / max(total_agents, 1)
    response_score = max(0, 1 - metrics.get("avg_response_time_ms", 0) / 2000)
    uptime_score = metrics.get("uptime_pct", 0) / 100
    sentiment = (metrics.get("community_sentiment", 0) + 1) / 2
    revenue = min(metrics.get("total_revenue_30d", 0) / 100000, 1)
    open_bounties = metrics.get("open_bounties", 1)
    bounty_score = max(0, 1 - open_bounties / 100)
    return (active_ratio * 25 + response_score * 15 + uptime_score * 15 + sentiment * 15 + revenue * 15 + bounty_score * 15)


def _highlights(metrics: dict[str, Any]) -> list[str]:
    highlights = []
    if metrics.get("active_agents_30d", 0) / max(metrics.get("total_agents", 1), 1) > 0.5:
        highlights.append("Organic engagement above 50% of total agents")
    if metrics.get("community_sentiment", 0) > 0.3:
        highlights.append("Community sentiment positive on Moltbook")
    if metrics.get("open_bounties", 0) < 10:
        highlights.append("Bounties closing quickly")
    if metrics.get("resolved_tickets", 0) > metrics.get("open_tickets", 0):
        highlights.append("Support backlog shrinking")
    return highlights


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
