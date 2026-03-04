"""Attribute platform impact to community or internal skills."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "community_impact_attributor",
    "description": "Splits revenue, usage, and profit between community and internal skills.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "skills_with_revenue": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["skills_with_revenue"],
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


def community_impact_attributor(skills_with_revenue: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return revenue share and ROI for community skills."""
    try:
        community = [s for s in skills_with_revenue if s.get("contributor_type") == "community"]
        internal = [s for s in skills_with_revenue if s.get("contributor_type") == "internal"]
        community_revenue = sum(s.get("monthly_revenue", 0) for s in community)
        internal_revenue = sum(s.get("monthly_revenue", 0) for s in internal)
        community_calls = sum(s.get("monthly_calls", 0) for s in community)
        internal_calls = sum(s.get("monthly_calls", 0) for s in internal)
        community_cost = sum((s.get("cost_to_review_tokens", 0) + s.get("cost_to_build_tokens", 0)) * 0.0005 for s in community)
        internal_cost = sum((s.get("cost_to_review_tokens", 0) + s.get("cost_to_build_tokens", 0)) * 0.001 for s in internal)
        community_profit = community_revenue - community_cost
        internal_profit = internal_revenue - internal_cost
        roi = community_profit / max(community_cost, 1e-6)
        mvp_skill = max(community, key=lambda s: s.get("monthly_revenue", 0)) if community else {}
        revenue_per_review_token = community_revenue / max(sum(s.get("cost_to_review_tokens", 0) for s in community), 1)
        data = {
            "community_revenue_pct": round(community_revenue / max(community_revenue + internal_revenue, 1) * 100, 2),
            "community_usage_pct": round(community_calls / max(community_calls + internal_calls, 1) * 100, 2),
            "community_profit": round(community_profit, 2),
            "internal_profit": round(internal_profit, 2),
            "community_roi": round(roi, 2),
            "most_valuable_community_skill": mvp_skill,
            "revenue_per_review_token": round(revenue_per_review_token, 4),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("community_impact_attributor", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
