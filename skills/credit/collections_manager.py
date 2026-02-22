"""Prioritize overdue tabs for collections sequencing."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "collections_manager",
    "description": "Tiers overdue accounts into reminder, notice, suspension, or write off stages.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "overdue_accounts": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["overdue_accounts"],
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


def collections_manager(
    overdue_accounts: list[dict[str, Any]],
    **_: Any,
) -> dict[str, Any]:
    """Map days overdue onto collections actions."""
    try:
        actions = []
        total_overdue = 0.0
        highest_risk: list[dict[str, Any]] = []
        write_off_candidates: list[dict[str, Any]] = []
        for account in overdue_accounts:
            days = int(account.get("days_overdue", 0))
            amount = float(account.get("amount_due", 0))
            total_overdue += amount
            stage, action = _determine_stage(days)
            entry = {
                "agent_id": account.get("agent_id"),
                "action": action,
                "stage": stage,
                "amount": amount,
            }
            actions.append(entry)
            if days >= 31:
                highest_risk.append(entry)
            if days >= 90:
                write_off_candidates.append(entry)

        data = {
            "actions": actions,
            "total_overdue": round(total_overdue, 2),
            "highest_risk": highest_risk,
            "write_off_candidates": write_off_candidates,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("collections_manager", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _determine_stage(days: int) -> tuple[str, str]:
    if days <= 7:
        return ("reminder", "Send friendly reminder message")
    if days <= 14:
        return ("formal_notice", "Issue formal notice and payment link")
    if days <= 30:
        return ("suspension_warning", "Warn of service suspension and Thunder escalation")
    return ("suspension", "Suspend access; coordinate with Thunder")


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
