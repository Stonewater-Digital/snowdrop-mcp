"""Generate hourly/day-of-week usage heatmap."""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from typing import Any

from skills.utils import SkillTelemetryEmitter, get_iso_timestamp, log_lesson

DAY_LABELS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

TOOL_META: dict[str, Any] = {
    "name": "usage_heatmap_generator",
    "description": "Buckets skill requests into hour/day heatmap bins for usage insights.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "requests": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["requests"],
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


def usage_heatmap_generator(requests: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return hourly/day heatmap counts."""
    emitter = SkillTelemetryEmitter(
        "usage_heatmap_generator",
        {"request_count": len(requests or [])},
    )
    try:
        heatmap: dict[str, dict[int, int]] = {day: defaultdict(int) for day in DAY_LABELS}
        total_requests = 0
        for req in requests:
            ts = req.get("timestamp")
            if not ts:
                continue
            try:
                dt = datetime.fromisoformat(ts)
            except ValueError:
                continue
            dt = dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
            day = DAY_LABELS[dt.weekday()]
            hour = dt.hour
            heatmap[day][hour] += 1
            total_requests += 1

        flattened = {(day, hour): count for day, hours in heatmap.items() for hour, count in hours.items()}
        peak = max(flattened.items(), key=lambda item: item[1], default=(("Mon", 0), 0))
        quiet = min(flattened.items(), key=lambda item: item[1], default=(("Mon", 0), 0))
        avg_per_hour = total_requests / (len(DAY_LABELS) * 24) if total_requests else 0.0
        data = {
            "heatmap": {day: dict(hours) for day, hours in heatmap.items()},
            "peak_hour": peak[0][1],
            "peak_day": peak[0][0],
            "quietest_hour": quiet[0][1],
            "total_requests": total_requests,
            "avg_requests_per_hour": round(avg_per_hour, 2),
        }
        emitter.record(
            "ok",
            {
                "total_requests": total_requests,
                "peak_day": peak[0][0] if peak else None,
                "peak_hour": peak[0][1] if peak else None,
                "quietest_hour": quiet[0][1] if quiet else None,
            },
        )
        return {
            "status": "success",
            "data": data,
            "timestamp": get_iso_timestamp(),
        }
    except Exception as exc:  # noqa: BLE001
        log_lesson(f"usage_heatmap_generator: {exc}")
        emitter.record("error", {"error": str(exc)})
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": get_iso_timestamp(),
        }
