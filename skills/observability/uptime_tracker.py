"""Compute Snowdrop uptime metrics."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "uptime_tracker",
    "description": "Calculates uptime %, MTBF, MTTR, and outage extremes from heartbeat logs.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "heartbeat_log": {
                "type": "array",
                "items": {"type": "object"},
            },
            "period_hours": {"type": "integer", "default": 720},
        },
        "required": ["heartbeat_log"],
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

STATUS_WEIGHT = {"ok": 1.0, "degraded": 0.5, "down": 0.0}


def uptime_tracker(
    heartbeat_log: list[dict[str, Any]],
    period_hours: int = 720,
    **_: Any,
) -> dict[str, Any]:
    """Return uptime metrics for the requested period."""

    try:
        if not heartbeat_log:
            raise ValueError("heartbeat_log cannot be empty")
        now = datetime.now(timezone.utc)
        cutoff = now - timedelta(hours=period_hours)
        entries = [
            {"timestamp": datetime.fromisoformat(item["timestamp"]), "status": item.get("status", "ok")}
            for item in heartbeat_log
            if datetime.fromisoformat(item["timestamp"]) >= cutoff
        ]
        if len(entries) < 2:
            raise ValueError("Not enough heartbeat samples in the selected window")
        entries.sort(key=lambda x: x["timestamp"])
        entries.append({"timestamp": now, "status": entries[-1]["status"]})
        uptime_seconds = 0.0
        downtime_segments: list[float] = []
        current_down = 0.0
        total_seconds = 0.0
        last_timestamp = entries[0]["timestamp"]
        for idx in range(1, len(entries)):
            entry = entries[idx]
            prev_entry = entries[idx - 1]
            delta = (entry["timestamp"] - prev_entry["timestamp"]).total_seconds()
            weight = STATUS_WEIGHT.get(prev_entry["status"], 1.0)
            uptime_seconds += delta * weight
            total_seconds += delta
            status = prev_entry["status"]
            if status == "down":
                current_down += delta
            elif current_down > 0:
                downtime_segments.append(current_down)
                current_down = 0.0
            last_timestamp = entry["timestamp"]
        if current_down > 0:
            downtime_segments.append(current_down)
        uptime_pct = 0 if total_seconds == 0 else uptime_seconds / total_seconds * 100
        mtbf = _mean_time_between_failures(entries)
        mttr = _average(downtime_segments)
        longest_outage = max(downtime_segments or [0]) / 60
        data = {
            "uptime_pct": round(uptime_pct, 4),
            "mean_time_between_failures_hours": round(mtbf / 3600, 2) if mtbf else None,
            "mean_time_to_recovery_minutes": round(mttr / 60, 2) if mttr else None,
            "longest_outage_minutes": round(longest_outage, 2),
            "SLA_met": uptime_pct >= 99.5,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": now.isoformat(),
        }
    except Exception as exc:
        _log_lesson("uptime_tracker", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _mean_time_between_failures(entries: list[dict[str, Any]]) -> float | None:
    failure_times: list[datetime] = [entry["timestamp"] for entry in entries if entry["status"] == "down"]
    if len(failure_times) < 2:
        return None
    intervals = [
        (failure_times[i + 1] - failure_times[i]).total_seconds()
        for i in range(len(failure_times) - 1)
    ]
    return sum(intervals) / len(intervals)


def _average(values: list[float]) -> float | None:
    return sum(values) / len(values) if values else None


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
