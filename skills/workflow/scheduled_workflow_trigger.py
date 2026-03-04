"""Evaluate cron-style workflow triggers."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "scheduled_workflow_trigger",
    "description": "Determines due, overdue, and next trigger times for workflows.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "workflows": {"type": "array", "items": {"type": "object"}},
            "current_time": {"type": "string"},
        },
        "required": ["workflows", "current_time"],
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


CRON_FIELDS = [
    (0, 59),  # minute
    (0, 23),  # hour
    (1, 31),  # day of month
    (1, 12),  # month
    (0, 6),  # weekday (0=Monday)
]


def scheduled_workflow_trigger(
    workflows: list[dict[str, Any]],
    current_time: str,
    **_: Any,
) -> dict[str, Any]:
    """Return workflows that should run now and when they next run."""
    try:
        current_dt = datetime.fromisoformat(current_time.replace("Z", "+00:00"))
        due_now: list[str] = []
        next_trigger_times: dict[str, str] = {}
        overdue: list[dict[str, Any]] = []

        for workflow in workflows:
            name = workflow.get("name") or "unnamed_workflow"
            schedule = workflow.get("schedule_cron")
            enabled = workflow.get("enabled", True)
            if not schedule:
                continue

            is_match = _cron_matches(schedule, current_dt)
            if enabled and is_match:
                due_now.append(name)

            next_time = _next_cron_time(schedule, current_dt)
            next_trigger_times[name] = next_time.isoformat()

            last_triggered = workflow.get("last_triggered")
            last_dt = (
                datetime.fromisoformat(last_triggered.replace("Z", "+00:00"))
                if last_triggered
                else None
            )
            previous_match = _previous_cron_time(schedule, current_dt)
            if enabled and previous_match and (last_dt is None or last_dt < previous_match):
                overdue.append({
                    "name": name,
                    "missed_run": previous_match.isoformat(),
                })

        data = {
            "due_now": due_now,
            "next_trigger_times": next_trigger_times,
            "overdue": overdue,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("scheduled_workflow_trigger", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _cron_matches(schedule: str, moment: datetime) -> bool:
    fields = schedule.split()
    if len(fields) != 5:
        raise ValueError("cron expression must have 5 fields")
    values = [moment.minute, moment.hour, moment.day, moment.month, (moment.weekday())]
    for field, value, bounds in zip(fields, values, CRON_FIELDS):
        if not _field_matches(field, value, bounds[0], bounds[1]):
            return False
    return True


def _field_matches(field: str, value: int, min_value: int, max_value: int) -> bool:
    options = [token.strip() for token in field.split(",") if token.strip()]
    if not options:
        return False
    for token in options:
        if token == "*":
            return True
        if token.startswith("*/"):
            step = int(token[2:])
            if step <= 0:
                raise ValueError("cron step must be positive")
            if (value - min_value) % step == 0:
                return True
        if "-" in token:
            start, end = token.split("-")
            if int(start) <= value <= int(end):
                return True
        try:
            if int(token) == value:
                return True
        except ValueError:
            continue
    return False


def _next_cron_time(schedule: str, moment: datetime) -> datetime:
    probe = moment + timedelta(minutes=1)
    for _ in range(60 * 24 * 30):
        if _cron_matches(schedule, probe):
            return probe
        probe += timedelta(minutes=1)
    return probe


def _previous_cron_time(schedule: str, moment: datetime) -> datetime | None:
    probe = moment - timedelta(minutes=1)
    for _ in range(60 * 24 * 7):
        if probe <= datetime.min.replace(tzinfo=timezone.utc):
            break
        if _cron_matches(schedule, probe):
            return probe
        probe -= timedelta(minutes=1)
    return None


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
