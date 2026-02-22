"""Manage franchise and premium subscription billing cycles."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "subscription_manager",
    "description": "Identifies subscriptions due for billing and drafts charge records.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "subscriptions": {
                "type": "array",
                "items": {"type": "object"},
            },
            "current_date": {"type": "string"},
        },
        "required": ["subscriptions", "current_date"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "due_subscriptions": {"type": "array", "items": {"type": "object"}},
                    "pending_charges": {"type": "array", "items": {"type": "object"}},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def subscription_manager(
    subscriptions: list[dict[str, Any]],
    current_date: str,
    **_: Any,
) -> dict[str, Any]:
    """Return billing-ready subscriptions and pending charge markers."""

    try:
        if not subscriptions:
            raise ValueError("subscriptions list cannot be empty")
        today = datetime.fromisoformat(current_date).date()

        due_subscriptions: list[dict[str, Any]] = []
        charges: list[dict[str, Any]] = []
        for subscription in subscriptions:
            last_billed_at = _resolve_last_billed(subscription)
            if last_billed_at + timedelta(days=30) > today:
                continue
            due_subscriptions.append(subscription)
            charges.append(
                {
                    "agent_id": subscription.get("agent_id"),
                    "plan": subscription.get("plan"),
                    "amount": float(subscription.get("monthly_rate", 0)),
                    "status": "pending_thunder_approval",
                    "scheduled_for": today.isoformat(),
                }
            )

        return {
            "status": "success",
            "data": {
                "due_subscriptions": due_subscriptions,
                "pending_charges": charges,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("subscription_manager", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _resolve_last_billed(subscription: dict[str, Any]) -> datetime.date:
    if subscription.get("last_billed"):
        return datetime.fromisoformat(str(subscription["last_billed"])).date()
    start = subscription.get("start_date")
    if not start:
        raise ValueError("subscription missing start_date and last_billed")
    return datetime.fromisoformat(str(start)).date()


def _log_lesson(skill_name: str, error: str) -> None:
    """Append a Ralph Wiggum lesson entry."""

    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
