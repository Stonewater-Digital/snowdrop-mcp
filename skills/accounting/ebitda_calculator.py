"""Calculate EBITDA from its component parts.

MCP Tool Name: ebitda_calculator
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "ebitda_calculator",
    "description": (
        "Calculates EBITDA (Earnings Before Interest, Taxes, Depreciation, and "
        "Amortization) by summing net income with non-cash and financing charges."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "net_income": {
                "type": "number",
                "description": "Net income for the period.",
            },
            "interest": {
                "type": "number",
                "description": "Interest expense.",
            },
            "taxes": {
                "type": "number",
                "description": "Tax expense.",
            },
            "depreciation": {
                "type": "number",
                "description": "Depreciation expense.",
            },
            "amortization": {
                "type": "number",
                "description": "Amortization expense.",
            },
        },
        "required": ["net_income", "interest", "taxes", "depreciation", "amortization"],
    },
}


def ebitda_calculator(
    net_income: float,
    interest: float,
    taxes: float,
    depreciation: float,
    amortization: float,
) -> dict[str, Any]:
    """Calculate EBITDA."""
    try:
        net_income = float(net_income)
        interest = float(interest)
        taxes = float(taxes)
        depreciation = float(depreciation)
        amortization = float(amortization)

        ebitda = net_income + interest + taxes + depreciation + amortization

        return {
            "status": "ok",
            "data": {
                "ebitda": round(ebitda, 2),
                "components": {
                    "net_income": round(net_income, 2),
                    "interest": round(interest, 2),
                    "taxes": round(taxes, 2),
                    "depreciation": round(depreciation, 2),
                    "amortization": round(amortization, 2),
                },
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
