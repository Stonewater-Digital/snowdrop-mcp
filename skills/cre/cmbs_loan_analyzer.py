"""Analyze CMBS loan sizing metrics."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "cmbs_loan_analyzer",
    "description": "Computes LTV, DSCR, debt yield, and balloon risk for CMBS loans.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "loan_amount": {"type": "number"},
            "property_value": {"type": "number"},
            "noi": {"type": "number"},
            "interest_rate": {"type": "number"},
            "amortization_years": {"type": "integer"},
            "term_years": {"type": "integer"},
            "io_period_years": {"type": "integer"},
        },
        "required": ["loan_amount", "property_value", "noi", "interest_rate", "amortization_years", "term_years", "io_period_years"],
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}}},
}


def cmbs_loan_analyzer(
    loan_amount: float,
    property_value: float,
    noi: float,
    interest_rate: float,
    amortization_years: int,
    term_years: int,
    io_period_years: int,
    **_: Any,
) -> dict[str, Any]:
    """Return CMBS sizing metrics and constraint."""
    try:
        ltv = loan_amount / property_value * 100 if property_value else 0.0
        debt_yield = noi / loan_amount * 100 if loan_amount else 0.0
        io_debt_service = loan_amount * interest_rate
        amortizing_payment = (loan_amount * interest_rate) / (1 - (1 + interest_rate) ** -(amortization_years)) if interest_rate else loan_amount / amortization_years
        dscr_io = noi / io_debt_service if io_debt_service else 0.0
        dscr_amort = noi / amortizing_payment if amortizing_payment else 0.0
        balloon_balance = loan_amount
        remaining_years = amortization_years - (term_years - io_period_years)
        if remaining_years > 0:
            balloon_balance = amortizing_payment * (1 - (1 + interest_rate) ** -remaining_years) / interest_rate
        breakeven_occupancy = (io_debt_service / (property_value * 0.012 if property_value else 1)) * 100
        rating_metrics = {"ltv": round(ltv, 2), "debt_yield": round(debt_yield, 2), "dscr": round(dscr_io, 2)}
        sizing_constraint = min((ltv, "ltv"), (debt_yield * 10, "debt_yield"), (dscr_io * 50, "dscr"))[1]
        data = {
            "ltv_pct": round(ltv, 2),
            "dscr_io": round(dscr_io, 2),
            "dscr_amortizing": round(dscr_amort, 2),
            "debt_yield_pct": round(debt_yield, 2),
            "balloon_payment": round(balloon_balance, 2),
            "breakeven_occupancy_pct": round(breakeven_occupancy, 2),
            "rating_agency_metrics": rating_metrics,
            "sizing_constraint": sizing_constraint,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("cmbs_loan_analyzer", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
