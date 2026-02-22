"""Recommend scaling actions from live telemetry."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "scaling_decision_engine",
    "description": "Evaluates telemetry against thresholds to suggest scale up/down/hold.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "current_metrics": {"type": "object"},
            "thresholds": {"type": "object"},
        },
        "required": ["current_metrics", "thresholds"],
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


def scaling_decision_engine(
    current_metrics: dict[str, Any],
    thresholds: dict[str, Any],
    **_: Any,
) -> dict[str, Any]:
    """Return the recommended scaling action and rationale."""
    try:
        cpu = float(current_metrics.get("cpu_pct", 0))
        memory = float(current_metrics.get("memory_pct", 0))
        queue = float(current_metrics.get("request_queue_depth", 0))
        latency = float(current_metrics.get("avg_latency_ms", 0))
        error_rate = float(current_metrics.get("error_rate_pct", 0))

        scale_up_cpu = float(thresholds.get("scale_up_cpu", 80))
        scale_down_cpu = float(thresholds.get("scale_down_cpu", 20))
        max_latency = float(thresholds.get("max_latency_ms", 500))

        decision = "hold"
        reason = "Within target ranges"
        urgency = "normal"
        recommended_instances = int(current_metrics.get("instances", 1))
        estimated_cost_change = 0.0

        if cpu > scale_up_cpu or memory > 85 or latency > max_latency or queue > 100:
            decision = "scale_up"
            reason = "Demand exceeds thresholds"
            urgency = "high" if latency > max_latency or error_rate > 2 else "medium"
            scale_factor = 1.5 if urgency == "high" else 1.25
            recommended_instances = max(1, int(round(recommended_instances * scale_factor)))
            estimated_cost_change = (scale_factor - 1) * 100
        elif cpu < scale_down_cpu and memory < 40 and queue < 10:
            decision = "scale_down"
            reason = "Resources underutilized"
            urgency = "low"
            scale_factor = 0.8
            recommended_instances = max(1, int(round(recommended_instances * scale_factor)))
            estimated_cost_change = (scale_factor - 1) * 100

        data = {
            "decision": decision,
            "reason": reason,
            "recommended_instances": recommended_instances,
            "estimated_cost_change": round(estimated_cost_change, 2),
            "urgency": urgency,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("scaling_decision_engine", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
