"""Track development pipeline progress."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "development_pipeline_tracker",
    "description": "Summarizes pipeline by stage, budget, and delivery exposure.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "projects": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "stage": {"type": "string", "enum": ["pre_dev", "under_construction", "stabilizing"]},
                        "budget": {"type": "number"},
                        "expected_noi": {"type": "number"},
                    },
                    "required": ["name", "stage", "budget", "expected_noi"],
                },
            }
        },
        "required": ["projects"],
    },
    "outputSchema": {"type": "object", "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}}},
}


def development_pipeline_tracker(projects: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return pipeline exposure by stage."""
    try:
        stage_totals: dict[str, float] = {"pre_dev": 0.0, "under_construction": 0.0, "stabilizing": 0.0}
        noi_totals: dict[str, float] = {"pre_dev": 0.0, "under_construction": 0.0, "stabilizing": 0.0}
        for project in projects:
            stage = project.get("stage", "pre_dev")
            stage_totals[stage] += project.get("budget", 0.0)
            noi_totals[stage] += project.get("expected_noi", 0.0)
        total_budget = sum(stage_totals.values())
        data = {
            "budget_by_stage": {stage: round(amount, 2) for stage, amount in stage_totals.items()},
            "noi_by_stage": {stage: round(amount, 2) for stage, amount in noi_totals.items()},
            "pre_dev_pct": round(stage_totals["pre_dev"] / total_budget * 100, 2) if total_budget else 0.0,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("development_pipeline_tracker", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
