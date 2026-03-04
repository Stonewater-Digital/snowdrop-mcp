"""Attribute repo value to individual contributors."""
from __future__ import annotations

from statistics import mean
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "contribution_attribution_engine",
    "description": "Weights lines of code, complexity, usage, and revenue to estimate contributor value.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "repo_skills": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["repo_skills"],
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


def contribution_attribution_engine(repo_skills: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return contributor value shares."""
    try:
        contributors: dict[str, dict[str, Any]] = {}
        total_value = 0.0
        for skill in repo_skills:
            contributor = skill.get("contributor_id", "unknown")
            score = skill.get("complexity_score", 1) * (skill.get("usage_count", 1) + 1) * (skill.get("revenue_generated", 0.0) + 1)
            total_value += score
            entry = contributors.setdefault(contributor, {"skills": [], "loc": 0, "value": 0.0})
            entry["skills"].append(skill.get("skill_name"))
            entry["loc"] += skill.get("lines_of_code", 0)
            entry["value"] += score
        contributor_list = []
        for contributor, info in contributors.items():
            percentage = info["value"] / total_value * 100 if total_value else 0.0
            contributor_list.append(
                {
                    "contributor_id": contributor,
                    "skills_contributed": info["skills"],
                    "total_loc": info["loc"],
                    "weighted_value": round(info["value"], 2),
                    "percentage_of_repo_value": round(percentage, 2),
                }
            )
        contributor_list.sort(key=lambda x: x["weighted_value"], reverse=True)
        gini = _gini([item["weighted_value"] for item in contributor_list])
        concentration = "high" if gini > 0.6 else "balanced"
        data = {
            "contributors": contributor_list,
            "total_repo_value_estimate": round(total_value, 2),
            "top_contributors": contributor_list[:5],
            "gini_coefficient": round(gini, 3),
            "concentration_risk": concentration,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("contribution_attribution_engine", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _gini(values: list[float]) -> float:
    if not values:
        return 0.0
    sorted_vals = sorted(values)
    n = len(values)
    cumulative = 0
    weighted_sum = 0
    for i, val in enumerate(sorted_vals, start=1):
        cumulative += val
        weighted_sum += i * val
    return (2 * weighted_sum) / (n * cumulative) - (n + 1) / n if cumulative else 0.0


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
