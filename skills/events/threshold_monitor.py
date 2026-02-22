"""Generic metric threshold monitoring."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "threshold_monitor",
    "description": "Evaluates metrics against warning and critical thresholds.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "metrics": {
                "type": "array",
                "items": {"type": "object"},
            }
        },
        "required": ["metrics"],
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


def threshold_monitor(metrics: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Check each metric and return aggregated health."""
    try:
        if not isinstance(metrics, list):
            raise ValueError("metrics must be a list")

        violations: list[dict[str, Any]] = []
        healthy_count = 0
        warning_count = 0
        critical_count = 0

        for metric in metrics:
            if not isinstance(metric, dict):
                raise ValueError("each metric must be a dict")
            name = str(metric.get("name", "unnamed"))
            current = float(metric.get("current_value"))
            warning = float(metric.get("warning_threshold"))
            critical = float(metric.get("critical_threshold"))
            direction = str(metric.get("direction", "above")).lower()

            severity = _evaluate_threshold(current, warning, critical, direction)
            if severity == "healthy":
                healthy_count += 1
            elif severity == "warning":
                warning_count += 1
                violations.append({"metric": name, "severity": severity, "current_value": current})
            elif severity == "critical":
                critical_count += 1
                violations.append({"metric": name, "severity": severity, "current_value": current})

        if critical_count > 0:
            overall = "critical"
        elif warning_count > 0:
            overall = "warning"
        else:
            overall = "healthy"

        result = {
            "overall_status": overall,
            "violations": violations,
            "healthy_count": healthy_count,
            "warning_count": warning_count,
            "critical_count": critical_count,
        }
        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("threshold_monitor", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _evaluate_threshold(
    current: float,
    warning: float,
    critical: float,
    direction: str,
) -> str:
    if direction not in {"above", "below"}:
        raise ValueError("direction must be 'above' or 'below'")

    if direction == "above":
        if current >= critical:
            return "critical"
        if current >= warning:
            return "warning"
    else:
        if current <= critical:
            return "critical"
        if current <= warning:
            return "warning"
    return "healthy"


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
