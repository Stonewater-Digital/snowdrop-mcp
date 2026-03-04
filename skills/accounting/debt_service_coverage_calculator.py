"""Calculate the debt service coverage ratio (DSCR).

MCP Tool Name: debt_service_coverage_calculator
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "debt_service_coverage_calculator",
    "description": (
        "Calculates the debt service coverage ratio (net operating income / total "
        "debt service), used by lenders to assess repayment ability."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "net_operating_income": {
                "type": "number",
                "description": "Net operating income for the period.",
            },
            "total_debt_service": {
                "type": "number",
                "description": "Total debt service (principal + interest payments).",
            },
        },
        "required": ["net_operating_income", "total_debt_service"],
    },
}


def debt_service_coverage_calculator(
    net_operating_income: float, total_debt_service: float
) -> dict[str, Any]:
    """Calculate the debt service coverage ratio."""
    try:
        net_operating_income = float(net_operating_income)
        total_debt_service = float(total_debt_service)

        if total_debt_service == 0:
            raise ValueError("total_debt_service must not be zero.")

        ratio = net_operating_income / total_debt_service

        return {
            "status": "ok",
            "data": {
                "dscr": round(ratio, 4),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
