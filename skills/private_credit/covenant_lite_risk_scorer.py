"""Score covenant-lite loan risk."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "covenant_lite_risk_scorer",
    "description": "Assigns protection scores based on covenant packages and aggressive terms.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "covenants_present": {"type": "array", "items": {"type": "string"}},
            "covenants_absent": {"type": "array", "items": {"type": "string"}},
            "has_equity_cure": {"type": "boolean"},
            "portability": {"type": "boolean"},
            "incremental_capacity_pct": {"type": "number"},
        },
        "required": ["covenants_present", "covenants_absent", "has_equity_cure", "portability", "incremental_capacity_pct"],
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


def covenant_lite_risk_scorer(
    covenants_present: list[str],
    covenants_absent: list[str],
    has_equity_cure: bool,
    portability: bool,
    incremental_capacity_pct: float,
    **_: Any,
) -> dict[str, Any]:
    """Return covenant protection risk score."""
    try:
        score = 100.0
        missing_protections = []
        for covenant in covenants_absent:
            if "maintenance" in covenant:
                score -= 25
                missing_protections.append(covenant)
            else:
                score -= 10
                missing_protections.append(covenant)
        if has_equity_cure:
            score -= 15
        if portability:
            score -= 10
        score -= (incremental_capacity_pct // 10) * 5
        score = max(score, 0)
        grade = "A" if score > 80 else "B" if score > 60 else "C" if score > 40 else "D"
        red_flags = []
        if score < 50:
            red_flags.append("Term sheet highly issuer-friendly")
        data = {
            "risk_score": round(score, 1),
            "grade": grade,
            "missing_protections": missing_protections,
            "present_protections": covenants_present,
            "red_flags": red_flags,
            "comparison_to_market": "average" if 50 <= score <= 75 else "weaker" if score < 50 else "stronger",
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("covenant_lite_risk_scorer", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
