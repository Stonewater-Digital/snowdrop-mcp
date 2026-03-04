"""Community leverage dashboard for Snowdrop."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "community_leverage_dashboard",
    "description": "Summarizes how community contributions amplify internal capacity.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "period": {"type": "string"},
            "internal_stats": {"type": "object"},
            "community_stats": {"type": "object"},
        },
        "required": ["period", "internal_stats", "community_stats"],
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}}},
}


def community_leverage_dashboard(
    period: str,
    internal_stats: dict[str, Any],
    community_stats: dict[str, Any],
    **_: Any,
) -> dict[str, Any]:
    """Return leverage ratios and savings metrics."""
    try:
        leverage_ratio = (community_stats.get("tokens_spent_by_community", 0) / internal_stats.get("tokens_spent", 1)) if internal_stats.get("tokens_spent") else float("inf")
        savings = internal_stats.get("cost_usd", 0) + community_stats.get("review_cost_usd", 0) - community_stats.get("tokens_spent_by_community", 0) / 1000 * 3
        community_fte_equiv = community_stats.get("skills_contributed", 0) / max(internal_stats.get("skills_built", 1), 1)
        panels = [
            {"title": "Leverage", "value": round(leverage_ratio, 2)},
            {"title": "Savings", "value": round(savings, 2)},
        ]
        headline = f"Community delivered {community_stats.get('skills_contributed', 0)} skills vs {internal_stats.get('skills_built', 0)} internal"
        data = {
            "leverage_ratio": round(leverage_ratio, 2) if leverage_ratio != float("inf") else float("inf"),
            "effective_team_multiplier": round(leverage_ratio + 1, 2) if leverage_ratio != float("inf") else float("inf"),
            "savings_usd": round(savings, 2),
            "community_fte_equivalent": round(community_fte_equiv, 2),
            "dashboard_panels": panels,
            "headline": headline,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("community_leverage_dashboard", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
