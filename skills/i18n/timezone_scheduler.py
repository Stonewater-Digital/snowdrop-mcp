"""Map UTC events into stakeholder time zones."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from zoneinfo import ZoneInfo

TOOL_META: dict[str, Any] = {
    "name": "timezone_scheduler",
    "description": "Converts event timestamps into relevant time zones and flags off-hour meetings.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "events": {"type": "array", "items": {"type": "object"}},
            "display_timezone": {"type": "string", "default": "America/Chicago"},
        },
        "required": ["events"],
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


def timezone_scheduler(
    events: list[dict[str, Any]],
    display_timezone: str = "America/Chicago",
    **_: Any,
) -> dict[str, Any]:
    """Convert events into multiple time zones and flag conflicts."""
    try:
        if not events:
            raise ValueError("events cannot be empty")
        display_tz = ZoneInfo(display_timezone)
        converted_events = []
        conflicts = []
        all_times_local = []
        for event in events:
            utc_time = event.get("utc_time")
            if not utc_time:
                raise ValueError("utc_time is required for each event")
            utc_dt = datetime.fromisoformat(utc_time.replace("Z", "+00:00"))
            conversions = []
            for tz_name in event.get("relevant_timezones", []):
                tz = ZoneInfo(tz_name)
                local_dt = utc_dt.astimezone(tz)
                conversions.append({"timezone": tz_name, "local_time": local_dt.isoformat()})
                if local_dt.hour < 9 or local_dt.hour >= 17:
                    conflicts.append(
                        {
                            "event": event.get("name"),
                            "timezone": tz_name,
                            "local_time": local_dt.isoformat(),
                        }
                    )
            converted_events.append({"name": event.get("name"), "schedule": conversions})
            all_times_local.append(
                {
                    "name": event.get("name"),
                    "local_time": utc_dt.astimezone(display_tz).isoformat(),
                }
            )
        data = {
            "events": converted_events,
            "all_times_local": all_times_local,
            "business_hours_conflicts": conflicts,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("timezone_scheduler", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
