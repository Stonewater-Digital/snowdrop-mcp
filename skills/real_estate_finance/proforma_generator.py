"""Generate a real estate investment pro forma."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "proforma_generator",
    "description": "Projects multi-year cash flows, NOI, and returns for income properties.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "purchase_price": {"type": "number"},
            "units": {"type": "integer"},
            "gross_potential_rent_annual": {"type": "number"},
            "vacancy_rate_pct": {"type": "number", "default": 5.0},
            "operating_expense_ratio_pct": {"type": "number", "default": 40.0},
            "capex_reserve_pct": {"type": "number", "default": 5.0},
            "loan": {"type": "object"},
            "hold_period_years": {"type": "integer", "default": 5},
            "rent_growth_pct": {"type": "number", "default": 3.0},
            "exit_cap_rate": {"type": "number"},
        },
        "required": ["purchase_price", "gross_potential_rent_annual", "exit_cap_rate"],
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


def proforma_generator(
    purchase_price: float,
    gross_potential_rent_annual: float,
    exit_cap_rate: float,
    units: int | None = None,
    vacancy_rate_pct: float = 5.0,
    operating_expense_ratio_pct: float = 40.0,
    capex_reserve_pct: float = 5.0,
    loan: dict[str, Any] | None = None,
    hold_period_years: int = 5,
    rent_growth_pct: float = 3.0,
    **_: Any,
) -> dict[str, Any]:
    """Return year-by-year cash flows and return metrics."""
    try:
        vacancy_rate = vacancy_rate_pct / 100
        opex_ratio = operating_expense_ratio_pct / 100
        capex_ratio = capex_reserve_pct / 100
        rent_growth = 1 + rent_growth_pct / 100
        loan_payment = _annual_debt_service(loan) if loan else 0.0
        year_by_year = []
        noi_total = 0.0
        cash_total = 0.0
        rent = gross_potential_rent_annual
        for year in range(1, hold_period_years + 1):
            egi = rent * (1 - vacancy_rate)
            operating_expenses = egi * opex_ratio
            reserves = egi * capex_ratio
            noi = egi - operating_expenses - reserves
            noi_total += noi
            debt_service = loan_payment
            cash_flow = noi - debt_service
            cash_total += cash_flow
            year_by_year.append(
                {
                    "year": year,
                    "egi": round(egi, 2),
                    "noi": round(noi, 2),
                    "debt_service": round(debt_service, 2),
                    "cash_flow": round(cash_flow, 2),
                }
            )
            rent *= rent_growth
        sale_price = year_by_year[-1]["noi"] / exit_cap_rate if year_by_year else 0.0
        equity = purchase_price - (loan.get("amount") if loan else 0.0)
        cash_on_cash_year1 = year_by_year[0]["cash_flow"] / equity if equity else 0.0
        avg_cash_on_cash = (cash_total / hold_period_years) / equity if equity else 0.0
        equity_irr = ((cash_total + sale_price) / equity) ** (1 / hold_period_years) - 1 if equity else 0.0
        data = {
            "year_by_year": year_by_year,
            "entry_cap_rate": round(noi_total / purchase_price, 4) if purchase_price else 0.0,
            "cash_on_cash_year1": round(cash_on_cash_year1, 3),
            "avg_cash_on_cash": round(avg_cash_on_cash, 3),
            "equity_irr": round(equity_irr, 4),
            "equity_multiple": round((cash_total + sale_price) / equity, 2) if equity else 0.0,
            "sale_price": round(sale_price, 2),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("proforma_generator", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _annual_debt_service(loan: dict[str, Any] | None) -> float:
    if not loan:
        return 0.0
    amount = loan.get("amount", 0.0)
    rate = loan.get("rate", 0.0)
    term = loan.get("term_years", 30)
    if rate == 0:
        return amount / term
    annuity = (rate * amount) / (1 - (1 + rate) ** -term)
    return annuity


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
