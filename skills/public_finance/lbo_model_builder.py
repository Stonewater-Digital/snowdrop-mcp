"""Construct a simplified LBO model."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "lbo_model_builder",
    "description": "Models leverage, cash flows, and equity returns for a stylized LBO.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "purchase_price": {"type": "number"},
            "ebitda": {"type": "number"},
            "debt_tranches": {"type": "array", "items": {"type": "object"}},
            "equity_contribution": {"type": "number"},
            "ebitda_growth_rate": {"type": "number"},
            "exit_multiple": {"type": "number"},
            "hold_period_years": {"type": "integer", "default": 5},
            "capex_pct_revenue": {"type": "number"},
            "working_capital_pct_revenue": {"type": "number"},
        },
        "required": [
            "purchase_price",
            "ebitda",
            "debt_tranches",
            "equity_contribution",
            "ebitda_growth_rate",
            "exit_multiple",
            "capex_pct_revenue",
            "working_capital_pct_revenue",
        ],
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


def lbo_model_builder(
    purchase_price: float,
    ebitda: float,
    debt_tranches: list[dict[str, Any]],
    equity_contribution: float,
    ebitda_growth_rate: float,
    exit_multiple: float,
    hold_period_years: int = 5,
    capex_pct_revenue: float = 0.04,
    working_capital_pct_revenue: float = 0.02,
    **_: Any,
) -> dict[str, Any]:
    """Return yearly LBO model output and equity returns."""
    try:
        revenue_multiple = purchase_price / max(ebitda, 1)
        yearly_model = []
        total_debt = sum(tranche.get("amount", 0.0) for tranche in debt_tranches)
        debt_balance = total_debt
        ebitda_value = ebitda
        debt_paydown_total = 0.0
        for year in range(1, hold_period_years + 1):
            revenue = ebitda_value * revenue_multiple
            capex = revenue * capex_pct_revenue
            working_capital = revenue * working_capital_pct_revenue
            interest = sum(tranche.get("rate", 0.0) * tranche.get("amount", 0.0) for tranche in debt_tranches)
            cash_flow = ebitda_value - interest - capex - working_capital
            mandatory_amort = sum(
                tranche.get("amount", 0.0) * tranche.get("amortization_pct_annual", 0.0)
                for tranche in debt_tranches
            )
            paydown = min(mandatory_amort + max(cash_flow, 0.0) * 0.5, debt_balance)
            debt_balance -= paydown
            debt_paydown_total += paydown
            yearly_model.append(
                {
                    "year": year,
                    "ebitda": round(ebitda_value, 2),
                    "cash_flow": round(cash_flow, 2),
                    "debt_balance": round(debt_balance, 2),
                }
            )
            ebitda_value *= (1 + ebitda_growth_rate)
        exit_enterprise_value = ebitda_value * exit_multiple
        exit_equity_value = exit_enterprise_value - debt_balance
        moic = exit_equity_value / equity_contribution if equity_contribution else 0.0
        equity_irr = moic ** (1 / hold_period_years) - 1 if equity_contribution and hold_period_years else 0.0
        data = {
            "equity_irr": round(equity_irr, 4),
            "moic": round(moic, 2),
            "yearly_model": yearly_model,
            "entry_multiple": round(revenue_multiple, 2),
            "exit_equity_value": round(exit_equity_value, 2),
            "debt_paydown_total": round(debt_paydown_total, 2),
            "credit_stats": {"net_debt_exit": round(debt_balance, 2)},
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("lbo_model_builder", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
