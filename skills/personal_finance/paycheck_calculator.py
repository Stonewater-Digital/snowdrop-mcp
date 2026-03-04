"""Calculate net pay from gross pay after taxes and deductions.

MCP Tool Name: paycheck_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "paycheck_calculator",
    "description": "Calculate net take-home pay from gross pay after federal, state, and FICA taxes. Supports multiple pay frequencies.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "gross_pay": {
                "type": "number",
                "description": "Gross pay per pay period.",
            },
            "pay_frequency": {
                "type": "string",
                "description": "Pay frequency: 'weekly', 'biweekly', 'semimonthly', 'monthly'.",
                "default": "biweekly",
                "enum": ["weekly", "biweekly", "semimonthly", "monthly"],
            },
            "federal_rate": {
                "type": "number",
                "description": "Effective federal income tax rate as decimal (e.g., 0.22 for 22%).",
                "default": 0.22,
            },
            "state_rate": {
                "type": "number",
                "description": "Effective state income tax rate as decimal (e.g., 0.05 for 5%).",
                "default": 0.05,
            },
            "fica_rate": {
                "type": "number",
                "description": "FICA rate as decimal (Social Security 6.2% + Medicare 1.45% = 7.65%).",
                "default": 0.0765,
            },
        },
        "required": ["gross_pay"],
    },
}

_PERIODS_PER_YEAR = {
    "weekly": 52,
    "biweekly": 26,
    "semimonthly": 24,
    "monthly": 12,
}


def paycheck_calculator(
    gross_pay: float,
    pay_frequency: str = "biweekly",
    federal_rate: float = 0.22,
    state_rate: float = 0.05,
    fica_rate: float = 0.0765,
) -> dict[str, Any]:
    """Calculate net take-home pay from gross pay."""
    try:
        freq = pay_frequency.lower()
        if freq not in _PERIODS_PER_YEAR:
            return {
                "status": "error",
                "data": {"error": f"Invalid pay_frequency '{pay_frequency}'. Use: weekly, biweekly, semimonthly, monthly."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        periods = _PERIODS_PER_YEAR[freq]
        annual_gross = gross_pay * periods

        federal_tax = gross_pay * federal_rate
        state_tax = gross_pay * state_rate
        fica_tax = gross_pay * fica_rate
        total_tax = federal_tax + state_tax + fica_tax
        net_pay = gross_pay - total_tax

        total_tax_rate = (federal_rate + state_rate + fica_rate) * 100

        return {
            "status": "ok",
            "data": {
                "per_paycheck": {
                    "gross_pay": round(gross_pay, 2),
                    "federal_tax": round(federal_tax, 2),
                    "state_tax": round(state_tax, 2),
                    "fica_tax": round(fica_tax, 2),
                    "total_deductions": round(total_tax, 2),
                    "net_pay": round(net_pay, 2),
                },
                "annualized": {
                    "gross_annual": round(annual_gross, 2),
                    "federal_tax_annual": round(federal_tax * periods, 2),
                    "state_tax_annual": round(state_tax * periods, 2),
                    "fica_tax_annual": round(fica_tax * periods, 2),
                    "total_deductions_annual": round(total_tax * periods, 2),
                    "net_annual": round(net_pay * periods, 2),
                },
                "pay_frequency": freq,
                "periods_per_year": periods,
                "effective_total_tax_rate_pct": round(total_tax_rate, 2),
                "take_home_rate_pct": round(100 - total_tax_rate, 2),
                "note": "Uses flat effective tax rates. Actual withholding varies by W-4 elections, "
                "pre-tax deductions (401k, HSA), and progressive tax brackets. "
                "FICA rate of 7.65% = 6.2% Social Security (up to wage base) + 1.45% Medicare.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
