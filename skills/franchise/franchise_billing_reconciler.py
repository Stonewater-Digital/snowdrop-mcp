"""Reconcile franchise royalties owed vs payments."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "franchise_billing_reconciler",
    "description": "Calculates royalty balances for each franchise operator.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "operators": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["operators"],
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


def franchise_billing_reconciler(operators: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return royalty balances per operator."""
    try:
        reconciliation = []
        total_owed = total_paid = 0.0
        delinquent: list[str] = []
        for operator in operators:
            operator_id = operator.get("operator_id")
            gross = float(operator.get("gross_revenue", 0.0))
            rate = float(operator.get("royalty_rate", 0.10))
            owed = gross * rate
            paid = sum(float(payment.get("amount", 0.0)) for payment in operator.get("payments_made", []) or [])
            balance = round(owed - paid, 2)
            total_owed += owed
            total_paid += paid
            if balance > 0:
                delinquent.append(operator_id)
            reconciliation.append(
                {
                    "operator_id": operator_id,
                    "owed": round(owed, 2),
                    "paid": round(paid, 2),
                    "balance": balance,
                }
            )
        data = {
            "reconciliation": reconciliation,
            "total_owed": round(total_owed, 2),
            "total_paid": round(total_paid, 2),
            "outstanding": round(total_owed - total_paid, 2),
            "delinquent_operators": delinquent,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("franchise_billing_reconciler", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
