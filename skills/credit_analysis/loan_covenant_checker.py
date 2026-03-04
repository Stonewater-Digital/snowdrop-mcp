"""Check covenant compliance."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "loan_covenant_checker",
    "description": "Tests financial covenants and highlights closest breaches.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "covenants": {"type": "array", "items": {"type": "object"}},
            "actuals": {"type": "object"},
        },
        "required": ["covenants", "actuals"],
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


def loan_covenant_checker(covenants: list[dict[str, Any]], actuals: dict[str, Any], **_: Any) -> dict[str, Any]:
    """Return compliance status for each covenant."""
    try:
        results = []
        headroom = {}
        closest = None
        all_compliant = True
        for covenant in covenants:
            metric = covenant.get("metric")
            threshold = covenant.get("threshold", 0.0)
            direction = covenant.get("direction", "min")
            actual = actuals.get(metric, 0.0)
            compliant = actual >= threshold if direction == "min" else actual <= threshold
            if not compliant:
                all_compliant = False
            delta = (actual - threshold) if direction == "min" else (threshold - actual)
            headroom[metric] = round(delta, 3)
            if closest is None or delta < closest["headroom"]:
                closest = {"metric": metric, "headroom": delta}
            results.append(
                {
                    "name": covenant.get("name"),
                    "metric": metric,
                    "actual": actual,
                    "threshold": threshold,
                    "compliant": compliant,
                }
            )
        data = {
            "all_compliant": all_compliant,
            "results": results,
            "closest_to_breach": closest,
            "headroom": headroom,
            "cure_note": "Monitor metrics with tight headroom.",
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("loan_covenant_checker", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
