"""Calculate the forward exchange rate using interest rate parity.

MCP Tool Name: forward_rate_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "forward_rate_calculator",
    "description": "Calculate forward exchange rate using covered interest rate parity: forward = spot * (1 + domestic_rate * days/360) / (1 + foreign_rate * days/360).",
    "inputSchema": {
        "type": "object",
        "properties": {
            "spot_rate": {
                "type": "number",
                "description": "Current spot exchange rate.",
            },
            "domestic_rate": {
                "type": "number",
                "description": "Domestic (quote currency) annualized interest rate as a decimal.",
            },
            "foreign_rate": {
                "type": "number",
                "description": "Foreign (base currency) annualized interest rate as a decimal.",
            },
            "days": {
                "type": "integer",
                "description": "Forward contract period in days.",
                "default": 90,
            },
        },
        "required": ["spot_rate", "domestic_rate", "foreign_rate"],
    },
}


def forward_rate_calculator(
    spot_rate: float,
    domestic_rate: float,
    foreign_rate: float,
    days: int = 90,
) -> dict[str, Any]:
    """Calculate forward exchange rate using interest rate parity."""
    try:
        if spot_rate <= 0:
            return {
                "status": "error",
                "data": {"error": "spot_rate must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if days <= 0:
            return {
                "status": "error",
                "data": {"error": "days must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        denominator = 1 + foreign_rate * days / 360
        if denominator == 0:
            return {
                "status": "error",
                "data": {"error": "Denominator is zero — foreign rate creates invalid calculation."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        forward = spot_rate * (1 + domestic_rate * days / 360) / denominator
        forward_premium_discount = forward - spot_rate
        annualized_premium_pct = (forward_premium_discount / spot_rate) * (360 / days) * 100

        status_label = "premium" if forward > spot_rate else "discount" if forward < spot_rate else "flat"

        return {
            "status": "ok",
            "data": {
                "spot_rate": spot_rate,
                "domestic_rate_pct": round(domestic_rate * 100, 4),
                "foreign_rate_pct": round(foreign_rate * 100, 4),
                "days": days,
                "forward_rate": round(forward, 6),
                "forward_points": round(forward_premium_discount, 6),
                "annualized_premium_discount_pct": round(annualized_premium_pct, 4),
                "forward_status": status_label,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
