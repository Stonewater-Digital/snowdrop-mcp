"""Calculate economics of invoice factoring."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "invoice_factoring_calculator",
    "description": "Computes advance, fees, and effective annual rate for factoring transactions.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "invoice_amount": {"type": "number"},
            "payment_terms_days": {"type": "integer"},
            "discount_rate_pct": {"type": "number", "default": 3.0},
            "advance_rate_pct": {"type": "number", "default": 80.0},
        },
        "required": ["invoice_amount", "payment_terms_days"],
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


def invoice_factoring_calculator(
    invoice_amount: float,
    payment_terms_days: int,
    discount_rate_pct: float = 3.0,
    advance_rate_pct: float = 80.0,
    **_: Any,
) -> dict[str, Any]:
    """Return factoring cost metrics."""
    try:
        if invoice_amount <= 0:
            raise ValueError("invoice_amount must be positive")
        if payment_terms_days <= 0:
            raise ValueError("payment_terms_days must be positive")
        advance_amount = invoice_amount * (advance_rate_pct / 100)
        factoring_fee = invoice_amount * (discount_rate_pct / 100) * (payment_terms_days / 30)
        net_proceeds = advance_amount - factoring_fee
        effective_annual_rate = (
            (factoring_fee / advance_amount) * (365 / payment_terms_days)
            if advance_amount
            else 0.0
        )
        cost_per_dollar = factoring_fee / invoice_amount

        data = {
            "advance_amount": round(advance_amount, 2),
            "factoring_fee": round(factoring_fee, 2),
            "net_proceeds": round(net_proceeds, 2),
            "effective_annual_rate_pct": round(effective_annual_rate * 100, 2),
            "cost_per_dollar": round(cost_per_dollar, 4),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("invoice_factoring_calculator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
