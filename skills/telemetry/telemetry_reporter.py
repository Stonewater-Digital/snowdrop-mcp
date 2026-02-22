"""Generate telemetry summaries."""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "telemetry_reporter",
    "description": "Aggregates telemetry events by dimension with latency/error metrics.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "events": {"type": "array", "items": {"type": "object"}},
            "period": {"type": "string"},
            "group_by": {"type": "string", "enum": ["skill", "event_type", "tier", "hour"]},
        },
        "required": ["events", "period", "group_by"],
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


def telemetry_reporter(
    events: list[dict[str, Any]],
    period: str,
    group_by: str,
    **_: Any,
) -> dict[str, Any]:
    """Return grouped telemetry metrics."""
    try:
        grouped: dict[str, list[dict[str, Any]]] = {}
        for event in events:
            properties = event.get("properties", {}) or {}
            if group_by == "skill":
                key = properties.get("skill_name", "unknown")
            elif group_by == "tier":
                key = properties.get("tier", "unknown")
            elif group_by == "hour":
                timestamp = event.get("timestamp")
                hour = timestamp[11:13] if isinstance(timestamp, str) and len(timestamp) >= 13 else "00"
                key = hour
            else:
                key = event.get("event_type", "unknown")
            grouped.setdefault(str(key), []).append(event)

        report = {}
        latency_values = []
        fastest = (None, math.inf)
        slowest = (None, -math.inf)
        for key, bucket in grouped.items():
            count = len(bucket)
            errors = len([ev for ev in bucket if ev.get("event_type") == "error" or not ev.get("properties", {}).get("success", True)])
            latencies = [ev.get("properties", {}).get("latency_ms") for ev in bucket if ev.get("properties", {}).get("latency_ms") is not None]
            latency_values.extend(latencies)
            avg_latency = sum(latencies) / len(latencies) if latencies else 0.0
            if latencies:
                if avg_latency < fastest[1]:
                    fastest = (key, avg_latency)
                if avg_latency > slowest[1]:
                    slowest = (key, avg_latency)
            report[key] = {
                "count": count,
                "error_rate": round((errors / count) if count else 0.0, 4),
                "avg_latency_ms": round(avg_latency, 2),
            }

        latency_values.sort()
        p95 = _percentile(latency_values, 0.95)
        data = {
            "report": report,
            "total_events": len(events),
            "error_rate": round(
                len([ev for ev in events if ev.get("event_type") == "error"]) / len(events) if events else 0.0,
                4,
            ),
            "p95_latency_ms": p95,
            "fastest_skill": fastest[0],
            "slowest_skill": slowest[0],
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("telemetry_reporter", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _percentile(values: list[float], percentile: float) -> float:
    if not values:
        return 0.0
    index = int(round((len(values) - 1) * percentile))
    return round(values[index], 2)


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
