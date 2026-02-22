"""Compute time and cost analytics per Snowdrop task."""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "compute_time_tracker",
    "description": "Calculates task durations, idle time, and cost per skill/model.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "task_log": {
                "type": "array",
                "items": {"type": "object"},
            }
        },
        "required": ["task_log"],
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


_MODEL_RATES = {
    "opus": {"prompt": 0.02, "completion": 0.04},
    "sonnet": {"prompt": 0.008, "completion": 0.016},
    "haiku": {"prompt": 0.002, "completion": 0.004},
}


def compute_time_tracker(task_log: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Aggregate compute time, idle time, and financial impact for a task log."""
    try:
        if not isinstance(task_log, list):
            raise ValueError("task_log must be a list")

        sorted_tasks = sorted(task_log, key=lambda task: task.get("start_time", ""))
        cost_by_skill: dict[str, float] = defaultdict(float)
        cost_by_model: dict[str, float] = defaultdict(float)
        task_breakdown: list[dict[str, Any]] = []
        total_compute_ms = 0
        idle_ms = 0
        previous_end: datetime | None = None

        for entry in sorted_tasks:
            if not isinstance(entry, dict):
                raise ValueError("each task entry must be a dict")
            start = _parse_ts(entry.get("start_time"), "start_time")
            end = _parse_ts(entry.get("end_time"), "end_time")
            if end <= start:
                raise ValueError("end_time must be after start_time")
            duration_ms = int((end - start).total_seconds() * 1000)
            total_compute_ms += duration_ms
            if previous_end is not None and start > previous_end:
                idle_ms += int((start - previous_end).total_seconds() * 1000)
            previous_end = end

            model = str(entry.get("model_used", "unknown")).lower()
            tokens_in = int(entry.get("tokens_in", 0))
            tokens_out = int(entry.get("tokens_out", 0))
            cost = _estimate_cost(model, tokens_in, tokens_out)
            skill_name = str(entry.get("skill_name", "unknown"))
            cost_by_skill[skill_name] += cost
            cost_by_model[model] += cost

            task_breakdown.append(
                {
                    "task_id": entry.get("task_id"),
                    "skill_name": skill_name,
                    "model": model,
                    "duration_ms": duration_ms,
                    "cost": round(cost, 4),
                }
            )

        total_window_ms = total_compute_ms + idle_ms
        utilization = total_compute_ms / total_window_ms if total_window_ms else 0.0

        data = {
            "total_compute_ms": total_compute_ms,
            "total_cost": round(sum(cost_by_skill.values()), 4),
            "utilization_pct": round(utilization * 100, 2),
            "cost_by_skill": {k: round(v, 4) for k, v in cost_by_skill.items()},
            "cost_by_model": {k: round(v, 4) for k, v in cost_by_model.items()},
            "task_breakdown": task_breakdown,
            "idle_time_ms": idle_ms,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("compute_time_tracker", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _estimate_cost(model: str, tokens_in: int, tokens_out: int) -> float:
    rates = _MODEL_RATES.get(model, _MODEL_RATES.get("sonnet"))
    prompt_cost = (tokens_in / 1000) * rates["prompt"]
    completion_cost = (tokens_out / 1000) * rates["completion"]
    return prompt_cost + completion_cost


def _parse_ts(value: Any, field_name: str) -> datetime:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be an ISO timestamp string")
    try:
        ts = datetime.fromisoformat(value)
    except ValueError as exc:  # noqa: B904
        raise ValueError(f"Invalid {field_name}: {value}") from exc
    if ts.tzinfo is None:
        ts = ts.replace(tzinfo=timezone.utc)
    return ts


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
