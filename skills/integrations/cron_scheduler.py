"""Evaluate cron schedules for Snowdrop tasks."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "cron_scheduler",
    "description": "Checks which scheduled tasks are due and when the next run occurs.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "current_time": {"type": "string"},
            "schedule": {
                "type": "array",
                "items": {"type": "object"},
            },
        },
        "required": ["current_time", "schedule"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "due": {"type": "array", "items": {"type": "object"}},
                    "next_up": {"type": "array", "items": {"type": "object"}},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def cron_scheduler(
    current_time: str,
    schedule: list[dict[str, Any]],
    **_: Any,
) -> dict[str, Any]:
    """Return due tasks and upcoming run timings."""

    try:
        now = datetime.fromisoformat(current_time)
        due_tasks: list[dict[str, Any]] = []
        next_runs: list[dict[str, Any]] = []
        for task in schedule:
            name = task.get("task_name")
            expression = task.get("cron_expression")
            last_run_raw = task.get("last_run")
            if not name or not expression:
                raise ValueError("Each task must include task_name and cron_expression")
            last_run = datetime.fromisoformat(last_run_raw) if last_run_raw else None
            is_due = _matches_cron(now, expression) and (not last_run or last_run < now)
            next_run_dt = _next_run(now, expression)
            next_runs.append(
                {
                    "task_name": name,
                    "seconds_until": int((next_run_dt - now).total_seconds()),
                }
            )
            if is_due:
                due_tasks.append({"task_name": name, "status": "pending_thunder_approval"})

        return {
            "status": "success",
            "data": {"due": due_tasks, "next_up": next_runs},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("cron_scheduler", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _matches_cron(moment: datetime, expression: str) -> bool:
    minute, hour, dom, month, dow = expression.split()
    return all(
        [
            _field_matches(minute, moment.minute, 0, 59),
            _field_matches(hour, moment.hour, 0, 23),
            _field_matches(dom, moment.day, 1, 31),
            _field_matches(month, moment.month, 1, 12),
            _field_matches(dow, moment.weekday(), 0, 6),
        ]
    )


def _next_run(moment: datetime, expression: str) -> datetime:
    candidate = moment
    for _ in range(60 * 24 * 14):  # search up to 14 days ahead
        if _matches_cron(candidate, expression):
            return candidate
        candidate += timedelta(minutes=1)
    raise ValueError("Unable to compute next run within 14 days")


def _field_matches(field: str, value: int, min_value: int, max_value: int) -> bool:
    if field == "*":
        return True
    for part in field.split(","):
        if "/" in part:
            base, step = part.split("/")
            step = int(step)
            values = range(min_value if base == "*" else int(base), max_value + 1, step)
            if value in values:
                return True
            continue
        if "-" in part:
            start, end = map(int, part.split("-"))
            if start <= value <= end:
                return True
            continue
        if int(part) == value:
            return True
    return False


def _log_lesson(skill_name: str, error: str) -> None:
    """Append a Ralph Wiggum lesson entry."""

    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
