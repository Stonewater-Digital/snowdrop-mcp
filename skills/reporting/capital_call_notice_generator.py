"""Produce capital call notices for LPs."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "capital_call_notice_generator",
    "description": "Creates LP-specific capital call instructions awaiting Thunder sign-off.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "fund_name": {"type": "string"},
            "call_amount": {"type": "number"},
            "purpose": {"type": "string"},
            "due_date": {"type": "string"},
            "lp_allocations": {
                "type": "array",
                "items": {"type": "object"},
            },
        },
        "required": [
            "fund_name",
            "call_amount",
            "purpose",
            "due_date",
            "lp_allocations",
        ],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "notice": {"type": "object"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def capital_call_notice_generator(
    fund_name: str,
    call_amount: float,
    purpose: str,
    due_date: str,
    lp_allocations: list[dict[str, Any]],
    **_: Any,
) -> dict[str, Any]:
    """Return a fund-level call notice and LP breakdown."""

    try:
        if call_amount <= 0:
            raise ValueError("call_amount must be positive")
        if not lp_allocations:
            raise ValueError("lp_allocations cannot be empty")

        lp_items: list[dict[str, Any]] = []
        for entry in lp_allocations:
            lp_name = entry.get("lp_name")
            lp_call = float(entry.get("call_amount", 0))
            if not lp_name or lp_call <= 0:
                raise ValueError("Each LP allocation needs lp_name and positive call_amount")
            lp_items.append(
                {
                    "lp_name": lp_name,
                    "call_amount": round(lp_call, 2),
                    "status": "pending_thunder_approval",
                    "notes": entry.get("notes"),
                }
            )

        total_lp = sum(item["call_amount"] for item in lp_items)
        if abs(total_lp - call_amount) > 0.01:
            raise ValueError("LP allocation totals must equal call_amount")

        notice = {
            "fund_name": fund_name,
            "call_amount": round(call_amount, 2),
            "purpose": purpose,
            "due_date": due_date,
            "lp_breakdown": lp_items,
            "status": "pending_thunder_approval",
        }
        return {
            "status": "success",
            "data": {"notice": notice},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("capital_call_notice_generator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    """Append a Ralph Wiggum lesson entry."""

    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
