"""Calculate net pay from gross pay with federal, state, and FICA deductions.

MCP Tool Name: gross_to_net_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "gross_to_net_calculator",
    "description": "Calculate net (take-home) pay from gross pay after federal tax, state tax, FICA, and pre-tax deductions.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "gross_pay": {
                "type": "number",
                "description": "Gross pay for the period in USD.",
            },
            "federal_rate": {
                "type": "number",
                "description": "Effective federal tax rate as a decimal.",
                "default": 0.22,
            },
            "state_rate": {
                "type": "number",
                "description": "State income tax rate as a decimal.",
                "default": 0.05,
            },
            "fica_rate": {
                "type": "number",
                "description": "FICA rate (Social Security + Medicare) as a decimal.",
                "default": 0.0765,
            },
            "pre_tax_deductions": {
                "type": "number",
                "description": "Pre-tax deductions (401k, HSA, health insurance, etc.) in USD.",
                "default": 0,
            },
        },
        "required": ["gross_pay"],
    },
}


def gross_to_net_calculator(
    gross_pay: float,
    federal_rate: float = 0.22,
    state_rate: float = 0.05,
    fica_rate: float = 0.0765,
    pre_tax_deductions: float = 0,
) -> dict[str, Any]:
    """Calculate net pay from gross pay."""
    try:
        if gross_pay < 0:
            return {
                "status": "error",
                "data": {"error": "gross_pay must be non-negative."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        taxable = gross_pay - pre_tax_deductions
        taxable = max(taxable, 0)

        federal_tax = taxable * federal_rate
        state_tax = taxable * state_rate
        fica_tax = gross_pay * fica_rate  # FICA is on gross, not reduced by pre-tax deductions (except certain cafeteria plans)

        total_deductions = pre_tax_deductions + federal_tax + state_tax + fica_tax
        net_pay = gross_pay - total_deductions

        total_tax_rate = (federal_tax + state_tax + fica_tax) / gross_pay * 100 if gross_pay > 0 else 0

        return {
            "status": "ok",
            "data": {
                "gross_pay": round(gross_pay, 2),
                "pre_tax_deductions": round(pre_tax_deductions, 2),
                "taxable_income": round(taxable, 2),
                "federal_tax": round(federal_tax, 2),
                "state_tax": round(state_tax, 2),
                "fica_tax": round(fica_tax, 2),
                "total_taxes": round(federal_tax + state_tax + fica_tax, 2),
                "total_deductions": round(total_deductions, 2),
                "net_pay": round(net_pay, 2),
                "effective_tax_rate_pct": round(total_tax_rate, 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
