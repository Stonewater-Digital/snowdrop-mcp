"""Track Stonewater Solutions LLC compliance requirements."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "llc_compliance_tracker",
    "description": "Calculates upcoming compliance deadlines for Stonewater Solutions LLC.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "state": {"type": "string", "default": "MO"},
            "formation_date": {"type": "string"},
            "last_annual_report": {"type": ["string", "null"]},
            "registered_agent_expiry": {"type": ["string", "null"]},
        },
        "required": ["formation_date"],
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

FEES = {
    "MO": {"annual_report": 20, "registered_agent": 100},
    "DE": {"annual_report": 75, "registered_agent": 125},
}


def llc_compliance_tracker(
    formation_date: str,
    state: str = "MO",
    last_annual_report: str | None = None,
    registered_agent_expiry: str | None = None,
    **_: Any,
) -> dict[str, Any]:
    """Return compliance deadlines with status and fees."""

    try:
        today = datetime.now(timezone.utc).date()
        formation = datetime.fromisoformat(formation_date).date()
        annual_base = (
            datetime.fromisoformat(last_annual_report).date() if last_annual_report else formation
        )
        next_annual = annual_base + timedelta(days=365)
        agent_expiry = (
            datetime.fromisoformat(registered_agent_expiry).date()
            if registered_agent_expiry
            else formation + timedelta(days=365)
        )
        deadlines = [
            _build_entry("Annual Report", next_annual, today, FEES.get(state, {}).get("annual_report", 50)),
            _build_entry(
                "Registered Agent Renewal",
                agent_expiry,
                today,
                FEES.get(state, {}).get("registered_agent", 150),
            ),
        ]
        data = {"requirements": deadlines, "state": state}
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("llc_compliance_tracker", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _build_entry(name: str, due_date: datetime.date, today: datetime.date, fee: float) -> dict[str, Any]:
    days_until = (due_date - today).days
    if days_until < 0:
        status = "overdue"
    elif days_until <= 30:
        status = "due_soon"
    else:
        status = "current"
    return {
        "requirement": name,
        "due_date": due_date.isoformat(),
        "days_until_due": days_until,
        "status": status,
        "estimated_fee": fee,
    }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
