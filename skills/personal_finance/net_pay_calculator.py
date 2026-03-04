"""Calculate net pay from gross annual salary with tax breakdown.

MCP Tool Name: net_pay_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "net_pay_calculator",
    "description": "Calculate annual and periodic net pay from gross annual salary after federal, state, and FICA taxes and pre-tax deductions.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "gross_annual": {
                "type": "number",
                "description": "Gross annual salary.",
            },
            "federal_rate": {
                "type": "number",
                "description": "Effective federal income tax rate as decimal.",
                "default": 0.22,
            },
            "state_rate": {
                "type": "number",
                "description": "Effective state income tax rate as decimal.",
                "default": 0.05,
            },
            "fica_rate": {
                "type": "number",
                "description": "FICA rate as decimal (SS + Medicare).",
                "default": 0.0765,
            },
            "deductions": {
                "type": "number",
                "description": "Annual pre-tax deductions (401k, HSA, health insurance premiums, etc.).",
                "default": 0,
            },
        },
        "required": ["gross_annual"],
    },
}


def net_pay_calculator(
    gross_annual: float,
    federal_rate: float = 0.22,
    state_rate: float = 0.05,
    fica_rate: float = 0.0765,
    deductions: float = 0,
) -> dict[str, Any]:
    """Calculate net pay from gross annual salary."""
    try:
        taxable_income = gross_annual - deductions

        federal_tax = taxable_income * federal_rate
        state_tax = taxable_income * state_rate
        # FICA is on gross (pre-tax deductions don't reduce FICA)
        fica_tax = gross_annual * fica_rate
        total_tax = federal_tax + state_tax + fica_tax

        net_annual = gross_annual - total_tax - deductions
        net_monthly = net_annual / 12
        net_biweekly = net_annual / 26
        net_weekly = net_annual / 52

        effective_tax_rate = (total_tax / gross_annual * 100) if gross_annual > 0 else 0
        take_home_rate = ((net_annual / gross_annual) * 100) if gross_annual > 0 else 0

        return {
            "status": "ok",
            "data": {
                "gross_annual": round(gross_annual, 2),
                "pre_tax_deductions": round(deductions, 2),
                "taxable_income": round(taxable_income, 2),
                "taxes": {
                    "federal_income_tax": round(federal_tax, 2),
                    "state_income_tax": round(state_tax, 2),
                    "fica_tax": round(fica_tax, 2),
                    "total_taxes": round(total_tax, 2),
                },
                "net_annual": round(net_annual, 2),
                "net_monthly": round(net_monthly, 2),
                "net_biweekly": round(net_biweekly, 2),
                "net_weekly": round(net_weekly, 2),
                "effective_tax_rate_pct": round(effective_tax_rate, 2),
                "take_home_rate_pct": round(take_home_rate, 2),
                "note": "Uses flat effective tax rates. Pre-tax deductions reduce federal and state taxable income "
                "but NOT FICA. For more accurate results, use your actual marginal tax brackets. "
                "FICA includes Social Security (6.2%, capped at $168,600 in 2024) and Medicare (1.45%, no cap; "
                "additional 0.9% above $200k single / $250k married).",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
