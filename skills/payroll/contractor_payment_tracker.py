"""Track contractor payouts for 1099 readiness."""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "contractor_payment_tracker",
    "description": "Aggregates contractor payments and flags 1099 thresholds.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "payments": {
                "type": "array",
                "items": {"type": "object"},
            }
        },
        "required": ["payments"],
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


def contractor_payment_tracker(payments: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return per-payee totals and 1099 triggers."""

    try:
        totals: dict[str, float] = defaultdict(float)
        details: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for payment in payments:
            payee = payment.get("payee_id")
            if not payee:
                continue
            amount = float(payment.get("amount", 0))
            totals[payee] += amount
            details[payee].append(payment)
        summaries = []
        required = []
        for payee, total in totals.items():
            if total >= 600:
                required.append(payee)
            summaries.append({"payee_id": payee, "ytd_total": round(total, 2), "payments": details[payee]})
        data = {"per_payee": summaries, "1099_required": required}
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("contractor_payment_tracker", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
