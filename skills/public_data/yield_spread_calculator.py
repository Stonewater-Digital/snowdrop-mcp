"""Calculate yield spread between long-term and short-term interest rates.

MCP Tool Name: yield_spread_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "yield_spread_calculator",
    "description": "Calculate the yield spread between a long-term and short-term interest rate. Detects yield curve inversion and provides historical context.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "long_rate": {
                "type": "number",
                "description": "Long-term interest rate (e.g., 10-year Treasury yield as percentage, like 4.25).",
            },
            "short_rate": {
                "type": "number",
                "description": "Short-term interest rate (e.g., 2-year Treasury yield as percentage, like 3.90).",
            },
        },
        "required": ["long_rate", "short_rate"],
    },
}


def yield_spread_calculator(
    long_rate: float,
    short_rate: float,
) -> dict[str, Any]:
    """Calculate yield spread between long and short rates."""
    try:
        spread = long_rate - short_rate
        spread_bps = spread * 100
        is_inverted = spread < 0

        if spread > 2.0:
            assessment = "Wide spread — steep yield curve, typical of early recovery or high growth expectations"
        elif spread > 1.0:
            assessment = "Normal spread — healthy yield curve, moderate growth expectations"
        elif spread > 0.25:
            assessment = "Narrow spread — flattening yield curve, possible slowdown ahead"
        elif spread > 0:
            assessment = "Very narrow spread — nearly flat yield curve, significant caution warranted"
        elif spread > -0.5:
            assessment = "Mildly inverted — yield curve inversion, historically a recession warning signal"
        else:
            assessment = "Deeply inverted — significant yield curve inversion, strong recession signal historically"

        return {
            "status": "ok",
            "data": {
                "long_rate_pct": long_rate,
                "short_rate_pct": short_rate,
                "spread_pct": round(spread, 4),
                "spread_bps": round(spread_bps, 2),
                "is_inverted": is_inverted,
                "assessment": assessment,
                "historical_context": "The 10Y-2Y spread has inverted before each of the last 8 US recessions. "
                "However, the lead time between inversion and recession onset varies from 6 to 24 months. "
                "The average historical 10Y-2Y spread is approximately 0.93%.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
