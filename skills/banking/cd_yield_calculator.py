"""Calculate Certificate of Deposit yield and maturity value.

MCP Tool Name: cd_yield_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "cd_yield_calculator",
    "description": "Calculate CD maturity value and interest earned given principal, APY, and term in months.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "principal": {
                "type": "number",
                "description": "Initial deposit amount.",
            },
            "apy": {
                "type": "number",
                "description": "Annual Percentage Yield as a decimal (e.g., 0.045 for 4.5%).",
            },
            "term_months": {
                "type": "integer",
                "description": "CD term length in months.",
            },
        },
        "required": ["principal", "apy", "term_months"],
    },
}


def cd_yield_calculator(principal: float, apy: float, term_months: int) -> dict[str, Any]:
    """Calculate CD maturity value and interest earned."""
    try:
        if principal <= 0:
            return {
                "status": "error",
                "data": {"error": "Principal must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if term_months <= 0:
            return {
                "status": "error",
                "data": {"error": "term_months must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        years = term_months / 12
        maturity_value = principal * (1 + apy) ** years
        interest_earned = maturity_value - principal

        return {
            "status": "ok",
            "data": {
                "principal": principal,
                "apy": apy,
                "apy_pct": round(apy * 100, 4),
                "term_months": term_months,
                "maturity_value": round(maturity_value, 2),
                "interest_earned": round(interest_earned, 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
