"""Compare term life vs whole life insurance: total cost and invest-the-difference analysis.

MCP Tool Name: term_vs_whole_life_comparator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "term_vs_whole_life_comparator",
    "description": "Compare term vs whole life insurance. Calculates total cost of each and models investing the premium difference at a given return rate.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "coverage_amount": {"type": "number", "description": "Death benefit / coverage amount."},
            "term_years": {"type": "integer", "description": "Term policy length in years (default 20).", "default": 20},
            "term_premium": {"type": "number", "description": "Monthly term life premium."},
            "whole_premium": {"type": "number", "description": "Monthly whole life premium."},
            "investment_return": {"type": "number", "description": "Annual return rate on invested difference as decimal (default 0.07).", "default": 0.07},
        },
        "required": ["coverage_amount", "term_premium", "whole_premium"],
    },
}


def term_vs_whole_life_comparator(
    coverage_amount: float,
    term_premium: float,
    whole_premium: float,
    term_years: int = 20,
    investment_return: float = 0.07,
) -> dict[str, Any]:
    """Compare term vs whole life insurance."""
    try:
        term_total = term_premium * 12 * term_years
        whole_total = whole_premium * 12 * term_years  # compare over same period

        # Invest the difference (whole - term) monthly
        monthly_diff = whole_premium - term_premium
        monthly_return = (1 + investment_return) ** (1 / 12) - 1

        # Future value of monthly investments
        if monthly_diff > 0 and monthly_return > 0:
            months = term_years * 12
            fv = monthly_diff * ((1 + monthly_return) ** months - 1) / monthly_return
        else:
            fv = monthly_diff * term_years * 12

        total_invested = monthly_diff * 12 * term_years
        investment_gain = fv - total_invested

        # Determine winner: buy term + invest the rest vs whole life
        # Whole life builds cash value (rough estimate ~60% of premiums paid)
        whole_cash_value = whole_total * 0.60

        return {
            "status": "ok",
            "data": {
                "coverage_amount": coverage_amount,
                "term_years": term_years,
                "term_monthly_premium": term_premium,
                "term_total_cost": round(term_total, 2),
                "whole_monthly_premium": whole_premium,
                "whole_total_cost": round(whole_total, 2),
                "monthly_premium_difference": round(monthly_diff, 2),
                "investment_return_pct": round(investment_return * 100, 2),
                "investment_future_value": round(fv, 2),
                "investment_gain": round(investment_gain, 2),
                "whole_life_estimated_cash_value": round(whole_cash_value, 2),
                "buy_term_invest_rest_wins": fv > whole_cash_value,
                "recommendation": "Buy term and invest the difference" if fv > whole_cash_value else "Whole life may be appropriate",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
