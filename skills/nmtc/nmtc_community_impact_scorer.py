"""Score NMTC project community impact."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

WEIGHTS = {
    "jobs": 0.25,
    "community_need": 0.25,
    "services": 0.2,
    "environmental": 0.15,
    "sustainability": 0.15,
}

TOOL_META: dict[str, Any] = {
    "name": "nmtc_community_impact_scorer",
    "description": "Scores NMTC projects across jobs, needs, and community benefits.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "project": {"type": "object"},
            "census_tract": {"type": "object"},
        },
        "required": ["project", "census_tract"],
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


def nmtc_community_impact_scorer(project: dict[str, Any], census_tract: dict[str, Any], **_: Any) -> dict[str, Any]:
    """Return impact score and supporting metrics."""
    try:
        jobs_score = min(project.get("jobs_created", 0) + project.get("jobs_retained", 0), 500) / 500
        need_score = 1 if census_tract.get("poverty_rate", 0) > 30 or census_tract.get("unemployment_rate", 0) > 10 else 0.5
        service_score = len(project.get("community_services", [])) / 5
        env_score = 1 if census_tract.get("food_desert") or census_tract.get("healthcare_shortage") else 0.3
        sustainability = (project.get("construction_jobs", 0) / max(project.get("square_footage", 1), 1))
        impact_score = sum(
            [
                jobs_score * WEIGHTS["jobs"],
                need_score * WEIGHTS["community_need"],
                service_score * WEIGHTS["services"],
                env_score * WEIGHTS["environmental"],
                sustainability * WEIGHTS["sustainability"],
            ]
        )
        jobs_per_dollar = (project.get("jobs_created", 0) + project.get("jobs_retained", 0)) / max(project.get("project_cost", 1), 1)
        need_level = "severe" if need_score >= 0.8 else "moderate"
        data = {
            "impact_score": round(impact_score * 100, 1),
            "score_breakdown": {
                "jobs": round(jobs_score, 2),
                "community_need": round(need_score, 2),
                "services": round(service_score, 2),
                "environmental": round(env_score, 2),
                "sustainability": round(sustainability, 2),
            },
            "jobs_per_dollar_invested": round(jobs_per_dollar, 6),
            "community_need_level": need_level,
            "competitive_assessment": "strong" if impact_score > 0.7 else "average",
            "narrative_summary": "Project addresses critical needs with high job creation.",
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("nmtc_community_impact_scorer", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
