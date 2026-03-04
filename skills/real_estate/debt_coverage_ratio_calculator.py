"""Calculate debt coverage ratio (DCR / DSCR) for a property.

MCP Tool Name: debt_coverage_ratio_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "debt_coverage_ratio_calculator",
    "description": "Calculate debt coverage ratio (DSCR = NOI / Annual Debt Service). Lenders typically require DSCR >= 1.20-1.25.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "net_operating_income": {
                "type": "number",
                "description": "Annual net operating income in USD.",
            },
            "annual_debt_service": {
                "type": "number",
                "description": "Total annual debt service (principal + interest payments) in USD.",
            },
        },
        "required": ["net_operating_income", "annual_debt_service"],
    },
}


def debt_coverage_ratio_calculator(
    net_operating_income: float,
    annual_debt_service: float,
) -> dict[str, Any]:
    """Calculate debt coverage ratio."""
    try:
        if annual_debt_service <= 0:
            return {
                "status": "error",
                "data": {"error": "annual_debt_service must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        dcr = net_operating_income / annual_debt_service
        surplus = net_operating_income - annual_debt_service

        if dcr >= 1.25:
            assessment = "Strong — meets most lender requirements."
        elif dcr >= 1.20:
            assessment = "Acceptable — meets minimum for many lenders."
        elif dcr >= 1.0:
            assessment = "Thin — covers debt but leaves little margin. May not qualify for conventional financing."
        else:
            assessment = "Negative coverage — NOI does not cover debt service. Cash shortfall expected."

        return {
            "status": "ok",
            "data": {
                "net_operating_income": round(net_operating_income, 2),
                "annual_debt_service": round(annual_debt_service, 2),
                "debt_coverage_ratio": round(dcr, 3),
                "annual_surplus_deficit": round(surplus, 2),
                "monthly_surplus_deficit": round(surplus / 12, 2),
                "assessment": assessment,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
