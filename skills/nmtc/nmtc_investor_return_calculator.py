"""Model NMTC investor returns."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "nmtc_investor_return_calculator",
    "description": "Calculates investor IRR over NMTC compliance period with tax credits and fees.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "investor_equity": {"type": "number"},
            "tax_credits": {"type": "array", "items": {"type": "object"}},
            "leverage_loan_interest_received": {"type": "number"},
            "cde_fees_received": {"type": "number"},
            "put_price_at_year_7": {"type": "number"},
            "investor_tax_rate": {"type": "number"},
        },
        "required": ["investor_equity", "tax_credits", "leverage_loan_interest_received", "cde_fees_received", "put_price_at_year_7", "investor_tax_rate"],
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


def nmtc_investor_return_calculator(
    investor_equity: float,
    tax_credits: list[dict[str, Any]],
    leverage_loan_interest_received: float,
    cde_fees_received: float,
    put_price_at_year_7: float,
    investor_tax_rate: float,
    **_: Any,
) -> dict[str, Any]:
    """Return after-tax IRR and cash flow schedule."""
    try:
        cashflows = [-investor_equity]
        for year in range(1, 8):
            credit_amount = next((tc.get("amount", 0.0) for tc in tax_credits if tc.get("year") == year), 0.0)
            net_credit = credit_amount * investor_tax_rate
            cash = leverage_loan_interest_received + cde_fees_received + net_credit
            if year == 7:
                cash += put_price_at_year_7
            cashflows.append(cash)
        irr = _irr(cashflows)
        total_credits = sum(tc.get("amount", 0.0) for tc in tax_credits)
        total_cash = sum(cashflows[1:])
        net_cost = investor_equity - total_cash
        payback = next((idx for idx, cf in enumerate(_cumulative(cashflows)) if cf >= 0), None)
        data = {
            "after_tax_irr": round(irr, 4),
            "total_tax_credits": round(total_credits, 2),
            "total_cash_received": round(total_cash, 2),
            "net_cost_of_investment": round(net_cost, 2),
            "year_by_year": cashflows,
            "effective_yield": round(irr * investor_tax_rate, 4),
            "payback_year": payback,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("nmtc_investor_return_calculator", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _irr(cashflows: list[float]) -> float:
    low, high = -0.99, 1.5
    for _ in range(100):
        mid = (low + high) / 2
        npv = sum(cf / (1 + mid) ** idx for idx, cf in enumerate(cashflows))
        if abs(npv) < 1e-4:
            return mid
        if npv > 0:
            low = mid
        else:
            high = mid
    return mid


def _cumulative(values: list[float]) -> list[float]:
    total = 0.0
    cumulatives = []
    for value in values:
        total += value
        cumulatives.append(total)
    return cumulatives


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
