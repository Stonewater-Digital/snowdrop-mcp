"""Calculate the interest coverage ratio (times interest earned).

MCP Tool Name: interest_coverage_calculator
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "interest_coverage_calculator",
    "description": (
        "Calculates the interest coverage ratio (EBIT / interest expense), "
        "measuring a company's ability to meet its interest obligations."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "ebit": {
                "type": "number",
                "description": "Earnings before interest and taxes.",
            },
            "interest_expense": {
                "type": "number",
                "description": "Total interest expense for the period.",
            },
        },
        "required": ["ebit", "interest_expense"],
    },
}


def interest_coverage_calculator(
    ebit: float, interest_expense: float
) -> dict[str, Any]:
    """Calculate the interest coverage ratio."""
    try:
        ebit = float(ebit)
        interest_expense = float(interest_expense)

        if interest_expense == 0:
            raise ValueError("interest_expense must not be zero.")

        ratio = ebit / interest_expense

        return {
            "status": "ok",
            "data": {
                "interest_coverage_ratio": round(ratio, 4),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
