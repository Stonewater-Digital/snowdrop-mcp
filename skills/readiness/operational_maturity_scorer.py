"""Score Snowdrop operational maturity levels."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "operational_maturity_scorer",
    "description": "Rates capabilities across dimensions and assigns an overall maturity level.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "dimensions": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["dimensions"],
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


def operational_maturity_scorer(dimensions: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return maturity levels per dimension and overall."""
    try:
        dimension_scores = []
        total_score = 0.0
        priority_gaps: list[str] = []
        for dimension in dimensions:
            name = dimension.get("name", "unknown")
            capabilities = set(dimension.get("capabilities", []))
            targets = set(dimension.get("target_capabilities", [])) or {"baseline"}
            coverage = len(capabilities & targets) / len(targets)
            level = _level_from_coverage(coverage)
            dimension_scores.append(
                {
                    "name": name,
                    "coverage_pct": round(coverage * 100, 2),
                    "level": level,
                    "missing": sorted(targets - capabilities),
                }
            )
            total_score += coverage
            if coverage < 0.4:
                priority_gaps.append(name)

        overall_score = total_score / len(dimensions) if dimensions else 0.0
        overall_level = _level_from_coverage(overall_score)
        data = {
            "overall_level": overall_level,
            "overall_score": round(overall_score * 100, 2),
            "dimensions": dimension_scores,
            "priority_gaps": priority_gaps,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("operational_maturity_scorer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _level_from_coverage(coverage: float) -> int:
    if coverage >= 0.8:
        return 5
    if coverage >= 0.6:
        return 4
    if coverage >= 0.4:
        return 3
    if coverage >= 0.2:
        return 2
    if coverage > 0:
        return 1
    return 0


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
