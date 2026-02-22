"""Priority queue manager for Watering Hole requests."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "request_queue_manager",
    "description": "Manages enqueue/dequeue/peek/stats for agent request queues.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "enum": ["enqueue", "dequeue", "peek", "stats"],
            },
            "request": {"type": ["object", "null"]},
            "queue_state": {
                "type": "array",
                "items": {"type": "object"},
            },
        },
        "required": ["operation", "queue_state"],
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

PRIORITY_ORDER = {"critical": 0, "premium": 1, "standard": 2, "free": 3}


def request_queue_manager(
    operation: str,
    queue_state: list[dict[str, Any]],
    request: dict[str, Any] | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Return queue operation result and updated state."""

    try:
        queue = list(queue_state)
        now = datetime.now(timezone.utc)
        if operation == "enqueue":
            if not request:
                raise ValueError("request payload required for enqueue")
            request = {
                **request,
                "priority": request.get("priority", "standard"),
                "queued_at": now.isoformat(),
            }
            queue.append(request)
            queue = _sort_queue(queue)
            data = {"enqueued": request, "queue_state": queue}
        elif operation == "dequeue":
            queue = _sort_queue(queue)
            next_item = queue.pop(0) if queue else None
            data = {"dequeued": next_item, "queue_state": queue}
        elif operation == "peek":
            queue = _sort_queue(queue)
            data = {"next_request": queue[0] if queue else None, "queue_state": queue}
        else:  # stats
            queue = _sort_queue(queue)
            stats = _queue_stats(queue)
            data = {"stats": stats, "queue_state": queue}

        return {
            "status": "success",
            "data": data,
            "timestamp": now.isoformat(),
        }
    except Exception as exc:
        _log_lesson("request_queue_manager", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _sort_queue(queue: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        queue,
        key=lambda item: (
            PRIORITY_ORDER.get(item.get("priority", "standard"), 3),
            item.get("queued_at", ""),
        ),
    )


def _queue_stats(queue: list[dict[str, Any]]) -> dict[str, Any]:
    counts: dict[str, int] = {priority: 0 for priority in PRIORITY_ORDER}
    for item in queue:
        priority = item.get("priority", "standard")
        counts[priority] = counts.get(priority, 0) + 1
    estimated_wait = {priority: count * 30 for priority, count in counts.items()}  # seconds
    return {
        "depth": len(queue),
        "counts": counts,
        "estimated_wait_seconds": estimated_wait,
    }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
