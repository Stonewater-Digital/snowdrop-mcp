"""Alert on upcoming contract renewals."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "contract_renewal_alerter",
    "description": "Identifies contracts requiring renewal action and quantifies value at risk.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "contracts": {"type": "array", "items": {"type": "object"}},
            "current_date": {"type": "string"},
        },
        "required": ["contracts", "current_date"],
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


def contract_renewal_alerter(
    contracts: list[dict[str, Any]],
    current_date: str,
    **_: Any,
) -> dict[str, Any]:
    """Return renewal alerts within notice periods."""
    try:
        today = datetime.fromisoformat(current_date).date()
        renewals_due = []
        total_value = 0.0
        action_required_by: dict[str, str] = {}
        auto_renewing: list[str] = []

        for contract in contracts:
            end_date_raw = contract.get("end_date")
            notice_days = int(contract.get("notice_period_days", 30))
            auto_renew = bool(contract.get("auto_renew", False))
            if auto_renew:
                auto_renewing.append(contract.get("contract_id", "unknown"))
            if not end_date_raw:
                continue
            end_date = datetime.fromisoformat(end_date_raw).date()
            notice_deadline = end_date - timedelta(days=notice_days)
            if notice_deadline <= today <= end_date:
                optimal_action = notice_deadline.isoformat()
                renewals_due.append(
                    {
                        "contract_id": contract.get("contract_id"),
                        "counterparty": contract.get("counterparty"),
                        "end_date": end_date.isoformat(),
                        "notice_period_days": notice_days,
                        "auto_renew": auto_renew,
                        "annual_value": float(contract.get("annual_value", 0.0)),
                        "action_date": optimal_action,
                    }
                )
                total_value += float(contract.get("annual_value", 0.0))
                action_required_by[contract.get("contract_id", "unknown")] = optimal_action

        data = {
            "renewals_due": renewals_due,
            "total_value_at_risk": round(total_value, 2),
            "action_required_by": action_required_by,
            "auto_renewing": auto_renewing,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("contract_renewal_alerter", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
