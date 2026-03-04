"""Track community growth metrics over time."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "community_growth_tracker",
    "description": "Calculates growth rates, viral coefficient, and projections from snapshots.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "snapshots": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["snapshots"],
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


def community_growth_tracker(snapshots: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Compute community growth KPIs."""
    try:
        if len(snapshots) < 2:
            raise ValueError("At least two snapshots required")
        ordered = sorted(snapshots, key=lambda snap: snap["date"])
        latest = ordered[-1]
        wow = _growth_rate(ordered, 7)
        mom = _growth_rate(ordered, 30)
        viral = latest.get("referral_agents", latest.get("agents_count", 0) * 0.1) / max(latest.get("agents_count", 1), 1)
        network_effect_score = min(1.0, latest.get("revenue", 0) / max(latest.get("agents_count", 1), 1) / 100)
        projected_agents = int(latest.get("agents_count", 0) * (1 + mom) ** (90 / 30))
        data = {
            "growth_rate_wow": round(wow * 100, 2),
            "growth_rate_mom": round(mom * 100, 2),
            "viral_coefficient": round(viral, 2),
            "network_effect_score": round(network_effect_score * 100, 2),
            "projected_agents_90d": projected_agents,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("community_growth_tracker", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _growth_rate(snapshots: list[dict[str, Any]], days: int) -> float:
    latest = snapshots[-1]
    target_date = datetime.fromisoformat(latest["date"].replace("Z", "+00:00")) - timedelta(days=days)
    prior = min(snapshots, key=lambda snap: abs(datetime.fromisoformat(snap["date"].replace("Z", "+00:00")) - target_date))
    prior_agents = prior.get("agents_count", 1)
    return (latest.get("agents_count", 0) - prior_agents) / max(prior_agents, 1)


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
