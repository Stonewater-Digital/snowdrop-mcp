"""Optimize invoice payment terms for discounts."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "payment_terms_optimizer",
    "description": "Evaluates early-pay discounts to maximize savings within cash constraints.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "invoices_payable": {"type": "array", "items": {"type": "object"}},
            "available_cash": {"type": "number"},
            "opportunity_cost_annual_pct": {"type": "number", "default": 5.0},
        },
        "required": ["invoices_payable", "available_cash"],
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


def payment_terms_optimizer(
    invoices_payable: list[dict[str, Any]],
    available_cash: float,
    opportunity_cost_annual_pct: float = 5.0,
    **_: Any,
) -> dict[str, Any]:
    """Return discount recommendations sorted by annualized return."""
    try:
        recommendations: list[dict[str, Any]] = []
        total_savings = 0.0
        cash_used = 0.0
        hurdle = opportunity_cost_annual_pct / 100

        scored: list[tuple[float, dict[str, Any]]] = []
        for invoice in invoices_payable:
            discount_pct = float(invoice.get("early_pay_discount_pct" or 0.0))
            window_days = invoice.get("discount_window_days")
            if not discount_pct or not window_days:
                continue
            amount = float(invoice.get("amount", 0.0))
            terms_days = max(int(invoice.get("terms_days", 30)), window_days)
            savings = amount * (discount_pct / 100)
            investment = amount
            period = terms_days - window_days
            annualized_return = (savings / investment) * (365 / period) if period else 0.0
            scored.append(
                (
                    annualized_return,
                    {
                        "vendor": invoice.get("vendor"),
                        "amount": amount,
                        "savings": round(savings, 2),
                        "annualized_return_pct": round(annualized_return * 100, 2),
                        "recommend": annualized_return > hurdle,
                    },
                )
            )

        for annualized_return, rec in sorted(scored, key=lambda item: item[0], reverse=True):
            if rec["recommend"] and cash_used + rec["amount"] <= available_cash:
                recommendations.append(rec)
                total_savings += rec["savings"]
                cash_used += rec["amount"]

        data = {
            "recommendations": recommendations,
            "total_savings": round(total_savings, 2),
            "cash_required": round(cash_used, 2),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("payment_terms_optimizer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
