"""Track adoption of community versus internal skills."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "community_skill_adoption_tracker",
    "description": "Compares usage, revenue, and growth metrics between internal and community skills.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "skills": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["skills"],
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


def community_skill_adoption_tracker(skills: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return adoption KPIs for community skills."""
    try:
        community = [s for s in skills if s.get("contributor_type") == "community"]
        internal = [s for s in skills if s.get("contributor_type") == "internal"]
        community_calls = sum(s.get("total_calls", 0) for s in community)
        internal_calls = sum(s.get("total_calls", 0) for s in internal)
        community_revenue = sum(s.get("revenue_generated", 0) for s in community)
        internal_revenue = sum(s.get("revenue_generated", 0) for s in internal)
        community_adoption = community_calls / max(len(community), 1)
        internal_adoption = internal_calls / max(len(internal), 1)
        zero_usage = [s.get("skill_name") for s in community if s.get("total_calls", 0) == 0]
        top_community = sorted(community, key=lambda s: s.get("total_calls", 0), reverse=True)[:5]
        outperform = [s.get("skill_name") for s in community if s.get("total_calls", 0) > internal_adoption]
        data = {
            "community_adoption_rate": round(community_adoption, 2),
            "internal_adoption_rate": round(internal_adoption, 2),
            "top_community_skills": top_community,
            "zero_usage_community_skills": zero_usage,
            "community_revenue_pct": round(community_revenue / max(community_revenue + internal_revenue, 1) * 100, 2),
            "community_outperforming_internal": outperform,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("community_skill_adoption_tracker", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
