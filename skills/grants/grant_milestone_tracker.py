"""Track grant milestones and disbursements."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "grant_milestone_tracker",
    "description": "Summarizes milestone completion, disbursements, and deadlines for grants.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "grant_id": {"type": "string"},
            "milestones": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["grant_id", "milestones"],
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


def grant_milestone_tracker(
    grant_id: str,
    milestones: list[dict[str, Any]],
    **_: Any,
) -> dict[str, Any]:
    """Calculate progress metrics for grant milestones."""
    try:
        completed = [m for m in milestones if m.get("status") == "approved"]
        total_disbursed = sum(float(m.get("disbursement_amount", 0)) for m in completed)
        completion_pct = (len(completed) / max(len(milestones), 1)) * 100
        pending = [m for m in milestones if m.get("status") in {"pending", "submitted"}]
        next_due = min(pending, key=lambda m: m.get("due_date")) if pending else None
        remaining_budget = sum(float(m.get("disbursement_amount", 0)) for m in milestones) - total_disbursed
        on_track = all(m.get("status") != "rejected" for m in milestones)
        days_until_next = _days_until(next_due["due_date"]) if next_due else 0
        data = {
            "grant_progress": {
                "grant_id": grant_id,
                "completion_pct": round(completion_pct, 2),
                "total_disbursed": round(total_disbursed, 2),
                "remaining_budget": round(max(remaining_budget, 0), 2),
            },
            "next_disbursement": next_due,
            "on_track": on_track,
            "days_until_next_deadline": days_until_next,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("grant_milestone_tracker", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _days_until(due_date: str) -> int:
    due = datetime.fromisoformat(due_date.replace("Z", "+00:00"))
    delta = due - datetime.now(timezone.utc)
    return max(delta.days, 0)


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
