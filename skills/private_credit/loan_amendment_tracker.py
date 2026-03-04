"""Score loan amendments for severity and drift."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "loan_amendment_tracker",
    "description": "Scores cumulative impact of loan amendments to highlight covenant drift.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "amendments": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "covenant_relief_turns": {"type": "number"},
                        "pricing_increase_bps": {"type": "number"},
                        "documentation_change_score": {"type": "number"},
                    },
                    "required": [
                        "name",
                        "covenant_relief_turns",
                        "pricing_increase_bps",
                        "documentation_change_score",
                    ],
                },
            }
        },
        "required": ["amendments"],
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


def loan_amendment_tracker(amendments: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return severity scores for amendments."""
    try:
        scored = []
        total_score = 0.0
        for amendment in amendments:
            covenant_relief = amendment.get("covenant_relief_turns", 0.0)
            pricing_increase = amendment.get("pricing_increase_bps", 0.0)
            documentation = amendment.get("documentation_change_score", 0.0)
            score = covenant_relief * 1.5 + pricing_increase / 100 + documentation
            total_score += score
            scored.append(
                {
                    "name": amendment.get("name", "unknown"),
                    "severity_score": round(score, 2),
                    "classification": "high" if score > 3 else "moderate" if score > 1.5 else "low",
                }
            )
        avg_score = total_score / len(amendments) if amendments else 0.0
        data = {
            "amendment_scores": scored,
            "average_severity": round(avg_score, 2),
            "covenant_drift_alert": avg_score > 2.0 or total_score > 6,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("loan_amendment_tracker", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
