"""Track the Goodwill cask (free-tier) budget for the day."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Iterable

TOOL_META: dict[str, Any] = {
    "name": "goodwill_cask_allocator",
    "description": "Allocates the daily Goodwill cask budget until depleted, then closes the tap.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "daily_budget": {"type": "number", "description": "USD daily Goodwill limit."},
            "requests": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "agent_id": {"type": "string"},
                        "requested_amount": {"type": "number"},
                    },
                },
                "description": "Sequence of Goodwill draws.",
            },
            "spent_to_date": {
                "type": "number",
                "description": "Amount already granted before this run.",
                "default": 0.0,
            },
        },
        "required": ["daily_budget", "requests"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "allocations": {"type": "array"},
                    "remaining_budget": {"type": "number"},
                    "is_closed": {"type": "boolean"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def goodwill_cask_allocator(
    daily_budget: float,
    requests: Iterable[dict[str, Any]],
    spent_to_date: float = 0.0,
    **_: Any,
) -> dict[str, Any]:
    """Process Goodwill requests until the cask closes.

    Args:
        daily_budget: Total USD budget for the day.
        requests: Iterable of Goodwill requests.
        spent_to_date: Already consumed portion.
        **_: Ignored keyword arguments.

    Returns:
        Allocation records and closure state.
    """
    try:
        if daily_budget <= 0:
            raise ValueError("daily_budget must be positive")
        if spent_to_date < 0:
            raise ValueError("spent_to_date cannot be negative")
        remaining = max(daily_budget - spent_to_date, 0.0)

        allocations = []
        for request in requests:
            agent_id = request.get("agent_id")
            requested_amount = float(request.get("requested_amount", 0.0))
            if not agent_id:
                raise ValueError("Each request requires agent_id")
            if requested_amount < 0:
                raise ValueError(f"requested_amount cannot be negative (agent={agent_id})")

            approved = min(requested_amount, remaining)
            remaining -= approved
            allocations.append({
                "agent_id": agent_id,
                "requested_amount": round(requested_amount, 2),
                "approved_amount": round(approved, 2),
                "status": "approved" if approved > 0 else "closed",
            })

        data = {
            "allocations": allocations,
            "remaining_budget": round(remaining, 2),
            "is_closed": remaining <= 0,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("goodwill_cask_allocator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
