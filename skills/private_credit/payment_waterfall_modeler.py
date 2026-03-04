"""Model cash waterfalls across structured credit tranches."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "payment_waterfall_modeler",
    "description": "Distributes cash through tranche priorities covering interest then principal.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "cash_available": {"type": "number"},
            "tranches": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "balance": {"type": "number"},
                        "coupon_pct": {"type": "number"},
                        "priority": {"type": "integer"},
                    },
                    "required": ["name", "balance", "coupon_pct", "priority"],
                },
            },
        },
        "required": ["cash_available", "tranches"],
    },
    "outputSchema": {"type": "object", "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}}},
}


def payment_waterfall_modeler(cash_available: float, tranches: list[dict[str, Any]], **_: Any) -> dict[str, Any]:
    """Return waterfall allocation with unpaid balances."""
    try:
        remaining = cash_available
        allocations = []
        for tranche in sorted(tranches, key=lambda item: item.get("priority", 0)):
            balance = tranche.get("balance", 0.0)
            coupon = tranche.get("coupon_pct", 0.0)
            interest_due = balance * (coupon / 100)
            interest_paid = min(interest_due, remaining)
            remaining -= interest_paid
            principal_paid = min(balance, remaining)
            remaining -= principal_paid
            allocations.append(
                {
                    "name": tranche.get("name", "unknown"),
                    "interest_paid": round(interest_paid, 2),
                    "principal_paid": round(principal_paid, 2),
                    "shortfall": round(max(interest_due - interest_paid, 0.0), 2),
                }
            )
        data = {
            "allocations": allocations,
            "residual_cash": round(remaining, 2),
            "all_interest_funded": remaining >= 0 and all(item["shortfall"] == 0 for item in allocations),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("payment_waterfall_modeler", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
